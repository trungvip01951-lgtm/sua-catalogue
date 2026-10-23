"""Chụp trạng thái và khóa bản tài liệu dùng chung; không sửa catalogue."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import uuid
import unicodedata
import catalogue as project

ROOT = Path(__file__).resolve().parents[1]


def normalized(value):
    return unicodedata.normalize('NFC', str(value)).casefold()


def tasks_for_file(tasks, relative):
    """Tách việc đúng tệp; nhiều tệp cùng nhóm không có cùng mọi mã việc."""
    matching = []
    for group in tasks['groups']:
        files = [f for f in group['files'] if normalized(f['input'].removeprefix('BẢN MỚI 01-10-2026/')) == normalized(relative)]
        if files:
            matching.append((group['id'], files))
    names = {normalized(f['name']) for _, files in matching for f in files}
    ids = sorted({task['id'] for task in tasks['tasks']
                  if any(normalized(name) in names for name in task['files'])})
    return [group for group, _ in matching], ids


def fresh_json(path, obj):
    p=Path(path); assert p.resolve().is_relative_to(ROOT.resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x',encoding='utf8') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)


def replace_state(path, obj):
    p=Path(path).resolve(); assert p.is_relative_to((ROOT/'state').resolve())
    temp=p.with_name(p.name+'.'+uuid.uuid4().hex+'.new')
    fresh_json(temp,obj)
    os.replace(temp,p)
    assert json.loads(p.read_text(encoding='utf8'))==obj


def snapshot(m):
    previous=ROOT/'state/catalogues.json'
    old=json.loads(previous.read_text(encoding='utf8')) if previous.exists() else {'catalogues':[]}
    oldrows={r['source_relative']:r for r in old['catalogues']}
    source=Path(m['paths']['source']); out=Path(m['paths']['output'])
    tasks=json.loads((ROOT/m['original_tasks_copy']).read_text(encoding='utf8'))
    rows=[]
    for p in sorted(source.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in ('.pdf','.xlsx','.docx'): continue
        rel=p.relative_to(source).as_posix(); actualsource=project.digest(p)
        canonical=m.get('canonical_overrides',{}).get(rel,rel)
        current=(out/canonical).resolve()
        assert current.is_relative_to(out.resolve()) and not current.is_relative_to(source.resolve())
        groups, taskids = tasks_for_file(tasks, rel)
        oldrow=oldrows.get(rel,{})
        # Không âm thầm chấp nhận thay đổi nguồn gốc sau lần chụp đầu.
        anchor=oldrow.get('source_sha256',actualsource)
        rows.append({'source_relative':rel,'current_relative':canonical,
             'source_sha256':anchor,'source_actual_at_snapshot_sha256':actualsource,
             'source_changed_from_initial_anchor':actualsource!=anchor,
             'current_sha256':project.digest(current) if current.is_file() else None,
             'source_bytes':p.stat().st_size,'current_bytes':current.stat().st_size if current.is_file() else None,
             'groups':groups,'tasks':sorted(set(taskids)),
             'canonical_selection_note':m.get('canonical_notes',{}).get(rel,'Cùng tên và thư mục con')})
    sourcehash={r['source_relative']:r['source_actual_at_snapshot_sha256'] for r in rows}
    for rel, expected in sourcehash.items():
        assert project.digest(source/rel)==expected,'Nguồn đổi khi chụp trạng thái'
    return {'captured_utc':datetime.now(timezone.utc).isoformat(),
            'scope':'Ảnh chụp trạng thái tệp; không phải nghiệm thu số/đồ họa',
            'catalogue_count':len(rows),'catalogues':rows,
            'progress_ledger':m['paths']['progress'], 'progress_ledger_sha256':project.digest(m['paths']['progress'])}


def seal(m):
    files=[]
    for rel in m['mandatory_controls']:
        p=(ROOT/rel).resolve(); assert p.is_relative_to(ROOT.resolve()) and p.is_file(),rel
        files.append({'relative_path':rel,'sha256':project.digest(p),'bytes':p.stat().st_size})
    return {'sealed_utc':datetime.now(timezone.utc).isoformat(),'files':files,
            'scope':'Khóa phiên bản quy tắc và công cụ dự án, không phải QA catalogue'}


def main():
    parser=argparse.ArgumentParser(description='Điều phối viên cập nhật state sau khi đã đọc/kiểm nguồn')
    parser.add_argument('--actor',required=True,choices=['ROOT'])
    parser.add_argument('--reason',required=True)
    parser.add_argument('--seal-controls',action='store_true')
    a=parser.parse_args()
    if not a.reason.strip(): parser.error('Cần lý do và bằng chứng đã đối chiếu')
    m=project.manifest(); snap=snapshot(m)
    tag=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    record=ROOT/'history'/('inventory-'+tag+'.json')
    fresh_json(record,dict(snap,actor=a.actor,reason=a.reason))
    replace_state(ROOT/'state/catalogues.json',snap)
    if a.seal_controls:
        control=seal(m)
        prior=ROOT/'state/control_manifest.json'
        if prior.exists(): fresh_json(ROOT/'history'/('controls-before-'+tag+'.json'),json.loads(prior.read_text(encoding='utf8')))
        fresh_json(ROOT/'history'/('controls-'+tag+'.json'),control)
        replace_state(prior,control)
    print(json.dumps({'result':'ĐÃ LƯU VÀ ĐỌC LẠI STATE','catalogues':len(snap['catalogues']),
          'snapshot':str(record),'snapshot_sha256':project.digest(record),
          'source_changed':[r['source_relative'] for r in snap['catalogues'] if r['source_changed_from_initial_anchor']],
          'seal_controls':a.seal_controls,'no_catalogue_written':True},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
