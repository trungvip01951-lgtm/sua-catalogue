"""Điều phối dùng chung; không ghi catalogue, không sửa catfix, không cài đặt.

Chỉ dùng thư viện Python chuẩn. Khóa hỗ trợ các phiên tuân thủ quy trình;
không thể cưỡng chế một chương trình khác cố tình ghi ngoài công cụ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import time
import uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


class ProjectError(Exception):
    pass


class ClosingConnection(sqlite3.Connection):
    """Context SQLite chuẩn không đóng handle; Windows cần đóng rõ sau lô."""
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def digest(path):
    p = Path(path)
    h = hashlib.sha256()
    before = p.stat()
    with p.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    after = p.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ProjectError('INPUT_CHANGED: tệp đổi trong lúc đọc: ' + str(p))
    return h.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def under(path, parent):
    return Path(path).resolve().is_relative_to(Path(parent).resolve())


def manifest():
    return read_json(ROOT / 'manifest.json')


def controls():
    seal = read_json(ROOT / 'state' / 'control_manifest.json')
    changed = []
    for row in seal['files']:
        p = (ROOT / row['relative_path']).resolve()
        if not under(p, ROOT):
            raise ProjectError('Đường dẫn luật nằm ngoài dự án')
        actual = digest(p) if p.is_file() else None
        if actual != row['sha256']:
            changed.append({'file': row['relative_path'], 'expected': row['sha256'], 'actual': actual})
    return {'seal_sha256': digest(ROOT / 'state' / 'control_manifest.json'), 'changed': changed}


def find_row(file):
    index = read_json(ROOT / 'state' / 'catalogues.json')
    normalized = file.replace('\\', '/')
    matches = [r for r in index['catalogues'] if r['source_relative'] == normalized
               or Path(r['source_relative']).name == normalized]
    if len(matches) != 1:
        raise ProjectError('Cần đúng một tên/đường dẫn tương đối trong danh mục; tìm được ' + str(len(matches)))
    return matches[0]


def context(file):
    m = manifest()
    row = find_row(file)
    source = (Path(m['paths']['source']) / row['source_relative']).resolve()
    current = (Path(m['paths']['output']) / row['current_relative']).resolve()
    if not under(source, m['paths']['source']) or not under(current, m['paths']['output']):
        raise ProjectError('Đường dẫn thoát khỏi thư mục đã giao')
    if under(current, m['paths']['source']) or source == current:
        raise ProjectError('Đích trùng hoặc nằm trong nguồn')
    source_sha = digest(source) if source.is_file() else None
    current_sha = digest(current) if current.is_file() else None
    rule_check = controls()
    changed = source_sha != row['source_sha256'] or current_sha != row['current_sha256']
    return {'file': row['source_relative'], 'source': str(source), 'current': str(current),
            'source_sha256': source_sha, 'current_sha256': current_sha,
            'snapshot_source_sha256': row['source_sha256'], 'snapshot_current_sha256': row['current_sha256'],
            'inputs_changed_since_snapshot': changed, 'controls': rule_check,
            'groups': row.get('groups', []), 'tasks': row.get('tasks', []),
            'canonical_selection_note': row.get('canonical_selection_note', ''),
            'progress_ledger': m['paths']['progress'],
            'acceptance_not_inferred_from_file_or_hash': True}


def connect():
    database = ROOT / 'state' / 'coordination.sqlite'
    c = sqlite3.connect(database, timeout=15, isolation_level=None, factory=ClosingConnection)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA busy_timeout=15000')
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('CREATE TABLE IF NOT EXISTS locks (file TEXT PRIMARY KEY, actor TEXT NOT NULL, session TEXT NOT NULL, token TEXT UNIQUE NOT NULL, acquired REAL NOT NULL, expires REAL NOT NULL, source_sha TEXT, current_sha TEXT, controls_sha TEXT NOT NULL, purpose TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, actor TEXT NOT NULL, session TEXT NOT NULL, kind TEXT NOT NULL, file TEXT, payload TEXT NOT NULL)')
    return c


def event(db, actor, session, kind, file, payload):
    db.execute('INSERT INTO events(at,actor,session,kind,file,payload) VALUES (?,?,?,?,?,?)',
               (timestamp(), actor, session, kind, file, json.dumps(payload, ensure_ascii=False)))


def validate_context(ctx):
    if ctx['controls']['changed']:
        raise ProjectError('LUẬT ĐỔI: đọc và kiểm lại luật; chưa được ghi theo gói cũ')
    if ctx['inputs_changed_since_snapshot']:
        raise ProjectError('INPUT_CHANGED: đọc lại bản hiện hành/bằng chứng và cập nhật ảnh chụp trạng thái trước khi nhận việc')
    if ctx['source_sha256'] is None:
        raise ProjectError('THIẾU NGUỒN: không nhận việc ghi')


def claim(file, actor, session, purpose, ttl):
    ctx = context(file)
    validate_context(ctx)
    if not actor.strip() or not session.strip() or not purpose.strip():
        raise ProjectError('Thiếu tên AI, mã phiên hoặc phạm vi')
    if not 60 <= ttl <= 3600:
        raise ProjectError('Thời hạn khóa từ60 đến3600 giây')
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        old = db.execute('SELECT * FROM locks WHERE file=?', (ctx['file'],)).fetchone()
        if old:
            raise ProjectError('ĐÃ CÓ BÊN GHI: ' + json.dumps(dict(old), ensure_ascii=False) + '; hết hạn cũng không tự chiếm khóa')
        # Kiểm lại ngay trong giao dịch khóa, không dựa duy nhất vào gói đã đọc.
        fresh = context(file)
        validate_context(fresh)
        if any(fresh[k] != ctx[k] for k in ['source_sha256', 'current_sha256']):
            raise ProjectError('INPUT_CHANGED trong lúc nhận khóa')
        token = str(uuid.uuid4())
        now = time.time()
        db.execute('INSERT INTO locks VALUES (?,?,?,?,?,?,?,?,?,?)',
                   (ctx['file'], actor, session, token, now, now + ttl, ctx['source_sha256'],
                    ctx['current_sha256'], ctx['controls']['seal_sha256'], purpose))
        event(db, actor, session, 'CLAIM', ctx['file'], {'token': token, 'purpose': purpose, 'ttl': ttl})
        db.commit()
    return {'token': token, 'file': ctx['file'], 'actor': actor, 'session': session,
            'expires_unix': now + ttl, 'context': ctx, 'permission_not_granted_by_claim': True}


def owned(db, token, actor, session):
    row = db.execute('SELECT * FROM locks WHERE token=?', (token,)).fetchone()
    if not row or row['actor'] != actor or row['session'] != session:
        raise ProjectError('KHÓA KHÔNG THUỘC PHIÊN NÀY')
    return dict(row)


def check(token, actor, session):
    with connect() as db:
        row = owned(db, token, actor, session)
    if row['expires'] <= time.time():
        raise ProjectError('KHÓA HẾT HẠN: chưa được ghi; đọc lại trước gia hạn/tiếp quản')
    ctx = context(row['file'])
    validate_context(ctx)
    if (ctx['source_sha256'], ctx['current_sha256'], ctx['controls']['seal_sha256']) != (
            row['source_sha'], row['current_sha'], row['controls_sha']):
        raise ProjectError('INPUT_CHANGED: khóa gắn với phiên bản trước')
    return {'result': 'ĐẠT KHÓA VÀ ĐẦU VÀO', 'lock': row, 'context': ctx,
            'numeric_graphic_print_acceptance_not_claimed': True}


def heartbeat(token, actor, session, ttl):
    if not 60 <= ttl <= 3600:
        raise ProjectError('Thời hạn khóa từ60 đến3600 giây')
    verified = check(token, actor, session)
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        owned(db, token, actor, session)
        expiry = time.time() + ttl
        db.execute('UPDATE locks SET expires=? WHERE token=?', (expiry, token))
        event(db, actor, session, 'HEARTBEAT', verified['lock']['file'], {'expires': expiry})
        db.commit()
    return {'token': token, 'expires_unix': expiry}


def release(token, actor, session, note):
    if not note.strip():
        raise ProjectError('Phải ghi bàn giao/kết quả và đường dẫn bằng chứng trước khi nhả khóa')
    with connect() as db:
        db.execute('BEGIN IMMEDIATE')
        row = owned(db, token, actor, session)
        event(db, actor, session, 'RELEASE', row['file'], {'note': note, 'old_lock': row})
        db.execute('DELETE FROM locks WHERE token=?', (token,))
        db.commit()
    return {'result': 'ĐÃ NHẢ KHÓA CHÍNH CHỦ', 'file': row['file'], 'note': note,
            'catalogue_not_deleted_or_modified': True}


def receipt(actor, session, note):
    if not note.strip():
        raise ProjectError('Cần ghi đúng phạm vi và bước tiếp theo sau khi chính AI đã đọc')
    seal = controls()
    if seal['changed']:
        raise ProjectError('Luật đã đổi: chưa được xác nhận đã đọc phiên bản cũ')
    with connect() as db:
        event(db, actor, session, 'READ_RECEIPT', None, {'controls_sha': seal['seal_sha256'], 'note': note,
              'self_reported_by_caller_not_proof_other_AI_read': True})
    return {'result': 'ĐÃ GHI XÁC NHẬN CỦA PHIÊN GỌI', 'actor': actor, 'session': session,
            'controls_sha': seal['seal_sha256'], 'note': note}


def health():
    m = manifest()
    missing = [name for name in ['source', 'output', 'reports', 'package', 'python', 'progress']
               if not Path(m['paths'][name]).exists()]
    rules = controls()
    db_path = ROOT / 'state' / 'coordination.sqlite'
    integrity = 'CHƯA KHỞI TẠO'
    if db_path.is_file():
        with sqlite3.connect('file:' + db_path.as_posix() + '?mode=ro', uri=True, factory=ClosingConnection) as db:
            integrity = db.execute('PRAGMA integrity_check').fetchone()[0]
    return {'project': m['name'], 'version': m['version'], 'root': str(ROOT),
            'missing_paths': missing, 'controls': rules, 'coordination_integrity': integrity,
            'result': 'ĐẠT CẤU TRÚC DỰ ÁN' if not missing and not rules['changed'] and integrity in ('ok', 'CHƯA KHỞI TẠO') else 'CHƯA ĐẠT',
            'this_is_not_BUOC0_43_tests_or_catalogue_acceptance': True,
            'read_shared_ledger_first': m['paths']['progress']}


def status():
    m = manifest()
    ledger = Path(m['paths']['progress'])
    lines = ledger.read_text(encoding='utf-8-sig').splitlines()
    locks = []
    db_path = ROOT / 'state' / 'coordination.sqlite'
    if db_path.is_file():
        with sqlite3.connect('file:' + db_path.as_posix() + '?mode=ro', uri=True, factory=ClosingConnection) as db:
            db.row_factory = sqlite3.Row
            locks = [dict(r) for r in db.execute('SELECT * FROM locks ORDER BY file')]
    return {'ledger': str(ledger), 'ledger_sha256': digest(ledger),
            'last_progress_rows': [line for line in lines if line.startswith('| 20')][-12:],
            'locks': locks, 'catalogue_acceptance_not_inferred_from_lock': True,
            'checkpoint_document': str(ROOT / 'state' / 'CURRENT_CHECKPOINT.md')}


def main():
    p = argparse.ArgumentParser(description='Điều phối dự án Sửa catalogue; không sửa PDF/Excel')
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ['health', 'status']:
        sub.add_parser(name)
    c = sub.add_parser('context'); c.add_argument('--file', required=True)
    c = sub.add_parser('claim'); c.add_argument('--file', required=True); c.add_argument('--purpose', required=True); c.add_argument('--ttl', type=int, default=1800)
    for name in ['check', 'heartbeat', 'release']:
        a = sub.add_parser(name); a.add_argument('--token', required=True)
        if name == 'heartbeat': a.add_argument('--ttl', type=int, default=1800)
        if name == 'release': a.add_argument('--note', required=True)
    a = sub.add_parser('receipt'); a.add_argument('--note', required=True)
    for a in sub.choices.values():
        if a.prog.rsplit(' ', 1)[-1] not in ['health', 'status', 'context']:
            a.add_argument('--actor', required=True); a.add_argument('--session', required=True)
    a = p.parse_args()
    try:
        if a.cmd == 'health': result = health()
        elif a.cmd == 'status': result = status()
        elif a.cmd == 'context': result = context(a.file)
        elif a.cmd == 'claim': result = claim(a.file, a.actor, a.session, a.purpose, a.ttl)
        elif a.cmd == 'check': result = check(a.token, a.actor, a.session)
        elif a.cmd == 'heartbeat': result = heartbeat(a.token, a.actor, a.session, a.ttl)
        elif a.cmd == 'release': result = release(a.token, a.actor, a.session, a.note)
        else: result = receipt(a.actor, a.session, a.note)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('result') != 'CHƯA ĐẠT' else 2
    except (ProjectError, FileNotFoundError, sqlite3.Error, ValueError) as e:
        print(json.dumps({'result': 'CHƯA ĐẠT', 'reason': str(e)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
