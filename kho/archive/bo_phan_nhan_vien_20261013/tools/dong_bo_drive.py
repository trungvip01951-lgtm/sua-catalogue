#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dong_bo_drive.py - đồng bộ MỘT CHIỀU kho "Sửa catalogue" → gói Drive cho nhân viên "Sửa catalogue - DRIVE NV".

Dùng:  dong_bo_drive.py [--thu] [--goi <thư mục gói>] [--chi rules,tools,...] [--nhanh] [--day-du]
  --thu   : chỉ in danh sách sẽ chép, KHÔNG ghi gì.
  --chi   : chỉ chạy các mục bản đồ có nguồn bắt đầu bằng các tiền tố này (vd rules,tools,CATALOG SUA).
  --nhanh : tệp cùng cỡ và đích không cũ hơn nguồn thì coi là giống (không băm sha256).
Quy tắc: chỉ chép tệp mới / khác sha256; KHÔNG xoá gì trong gói (tệp thừa chỉ liệt kê để người quyết);
không đụng NV_LAM/ của gói; ghi <gói>/PHIEN_BAN.txt (phiên bản rules/HO_SO_HANG.json + giờ UTC + số tệp chép).
Thư mục gói dò lần lượt: --goi, $HOME/mnt/ChatGPT/Sửa catalogue - DRIVE NV, <cha của kho>/Sửa catalogue - DRIVE NV,
D:\\ChatGPT\\Sửa catalogue - DRIVE NV.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

KHO = Path(__file__).resolve().parents[1]
TEN_GOI = 'Sửa catalogue - DRIVE NV'
# (nguồn trong kho, đích trong gói)
BAN_DO = [
    ('rules', 'QUY_TAC/rules'),
    ('procedures', 'QUY_TAC/procedures'),
    ('knowledge', 'QUY_TAC/knowledge'),
    ('templates', 'CONG_CU/templates'),
    ('tools/kiem_catalogue.py', 'CONG_CU/tools/kiem_catalogue.py'),
    ('tools/ve_duong_cong.py', 'CONG_CU/tools/ve_duong_cong.py'),
    ('vendor/catfix_original', 'CONG_CU/catfix_original'),
    ('rules/QUYET_DINH_ANH.md', 'QUYET_DINH_ANH/QUYET_DINH_ANH.md'),
    ('claude/TRANG_THAI_CLAUDE.md', 'QUYET_DINH_ANH/TRANG_THAI_CLAUDE.md'),
    ('claude/VIEC_CHO_ANH.md', 'QUYET_DINH_ANH/VIEC_CHO_ANH.md'),
    ('claude/THAY_DOI_MA_20261009.csv', 'QUYET_DINH_ANH/THAY_DOI_MA_20261009.csv'),
    ('CATALOG SUA', 'CATALOG SUA'),
    ('DU_LIEU', 'DU_LIEU'),
    ('KHO_ANH', 'KHO_ANH'),
    ('deliverables', 'BAN_GIAO_RIENG'),
    ('rules/HO_SO_HANG.json', 'CONG_CU/rules/HO_SO_HANG.json'),
    ('claude/goi_drive/00_CLAUDE_DOC_TRUOC.md', '00_CLAUDE_DOC_TRUOC.md'),
    ('claude/goi_drive/00_CLAUDE_DOC_TRUOC.docx', '00_CLAUDE_DOC_TRUOC.docx'),
    ('claude/goi_drive/HUONG_DAN_ANH_TRUNG.md', 'HUONG_DAN_ANH_TRUNG.md'),
    ('claude/goi_drive/HUONG_DAN_ANH_TRUNG.docx', 'HUONG_DAN_ANH_TRUNG.docx'),
]
# Tệp kho đóng thêm vào skill nhân viên lúc zip (luôn lấy bản mới nhất, một nguồn): (nguồn trong kho, đường trong skill)
SKILL_THEM = [
    ('rules/QUY_TAC_HIEN_HANH.md', 'reference/QUY_TAC_HIEN_HANH.md'),
    ('rules/HO_SO_HANG.md', 'reference/HO_SO_HANG.md'),
    ('rules/CHUAN_TRINH_BAY.md', 'reference/CHUAN_TRINH_BAY.md'),
    ('rules/LOI_DA_GAP.md', 'reference/LOI_DA_GAP.md'),
    ('rules/HO_SO_HANG.json', 'rules/HO_SO_HANG.json'),
    ('tools/kiem_catalogue.py', 'scripts/kiem_catalogue.py'),
    ('tools/ve_duong_cong.py', 'scripts/ve_duong_cong.py'),
]
SKILL_NGUON = 'claude/skill_nv/sua-catalogue'
SKILL_ZIP = 'sua-catalogue.zip'
BO_QUA_TEN = {'__pycache__', '.DS_Store', 'Thumbs.db', 'desktop.ini', '.git'}
KHONG_DUNG = 'NV_LAM'


def bo_qua(p: Path):
    return any(x in BO_QUA_TEN or x.startswith('_CHO_XOA') or x.startswith('~$') for x in p.parts) or p.suffix == '.pyc'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for k in iter(lambda: f.read(1 << 20), b''):
            h.update(k)
    return h.hexdigest()


def tim_goi(chi_dinh=None):
    ung = [Path(chi_dinh)] if chi_dinh else []
    ung += [Path.home() / 'mnt' / 'ChatGPT' / TEN_GOI, KHO.parent / TEN_GOI, Path('D:/ChatGPT') / TEN_GOI]
    for p in ung:
        if p.is_dir():
            return p
    return None


def liet_ke(nguon: Path):
    if nguon.is_file():
        return [(nguon, Path())]
    return sorted((p, p.relative_to(nguon)) for p in nguon.rglob('*') if p.is_file() and not bo_qua(p.relative_to(nguon)))


def giong(a: Path, b: Path, nhanh):
    if not b.exists():
        return False, 'mới'
    sa, sb = a.stat(), b.stat()
    if sa.st_size != sb.st_size:
        return False, 'khác'
    if nhanh and sb.st_mtime >= sa.st_mtime - 2:
        return True, 'giống'
    return (True, 'giống') if sha(a) == sha(b) else (False, 'khác')


def zip_skill(nguon: Path):
    """Zip thư mục skill trong bộ nhớ, thư mục sua-catalogue ở cấp cao nhất. Trả (bytes, {tên: crc})."""
    buf = io.BytesIO()
    crc = {}
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(nguon.rglob('*')):
            if p.is_file() and not bo_qua(p.relative_to(nguon)):
                ten = 'sua-catalogue/' + p.relative_to(nguon).as_posix()
                data = p.read_bytes()
                z.writestr(ten, data)
                crc[ten] = zlib.crc32(data) & 0xFFFFFFFF
        for nguon_kho, dich in SKILL_THEM:
            q = KHO / nguon_kho
            if q.is_file():
                ten = 'sua-catalogue/' + dich
                data = q.read_bytes()
                z.writestr(ten, data)
                crc[ten] = zlib.crc32(data) & 0xFFFFFFFF
            else:
                print('CẢNH BÁO: thiếu tệp đóng vào skill:', nguon_kho)
    return buf.getvalue(), crc


def main(argv=None):
    ap = argparse.ArgumentParser(description='Đồng bộ một chiều kho → gói "Sửa catalogue - DRIVE NV" (không xoá gì).')
    ap.add_argument('--thu', action='store_true', help='chỉ in danh sách sẽ chép, không ghi gì')
    ap.add_argument('--goi', help='thư mục gói (mặc định tự dò)')
    ap.add_argument('--chi', help='chỉ các nguồn bắt đầu bằng tiền tố này (phẩy ngăn cách)')
    ap.add_argument('--nhanh', action='store_true', help='cùng cỡ + đích không cũ hơn thì coi là giống, không băm')
    ap.add_argument('--day-du', action='store_true', help='in đủ mọi tệp')
    a = ap.parse_args(argv)
    goi = tim_goi(a.goi)
    if goi is None:
        print(f'LỖI: không tìm thấy gói "{TEN_GOI}" (đã dò $HOME/mnt/ChatGPT, cạnh kho, D:\\ChatGPT).')
        return 2
    try:
        phien_ban = json.loads((KHO / 'rules' / 'HO_SO_HANG.json').read_text(encoding='utf-8-sig')).get('phien_ban', '?')
    except Exception as e:  # noqa
        print(f'LỖI: không đọc được rules/HO_SO_HANG.json: {e}')
        return 2
    chi = [x.strip() for x in a.chi.split(',')] if a.chi else None
    print(f'== ĐỒNG BỘ MỘT CHIỀU {"(CHẠY THỬ - không ghi gì)" if a.thu else ""}\n   kho : {KHO}\n   gói : {goi}\n'
          f'   quy tắc phiên bản {phien_ban}')
    lim = 10 ** 9 if a.day_du else 25
    tong_chep, tong_thua, loi = 0, 0, 0
    for src_rel, dst_rel in BAN_DO:
        if chi and not any(src_rel.startswith(c) for c in chi):
            continue
        src, dst = KHO / src_rel, goi / dst_rel
        if dst_rel.split('/')[0] == KHONG_DUNG:
            continue
        if not src.exists():
            print(f' - {src_rel} → {dst_rel}: không có nguồn trong kho, bỏ qua')
            continue
        ds = liet_ke(src)
        can = []
        n_giong = 0
        for p, rel in ds:
            d = dst / rel if rel.parts else dst
            ok, ly = giong(p, d, a.nhanh)
            if ok:
                n_giong += 1
            else:
                can.append((p, d, ly))
        thua = []
        if src.is_dir() and dst.is_dir():
            co = {rel for _, rel in ds}
            thua = sorted(p.relative_to(dst) for p in dst.rglob('*')
                          if p.is_file() and p.relative_to(dst) not in co and not bo_qua(p.relative_to(dst)))
        print(f' - {src_rel} → {dst_rel}: {len(ds)} tệp nguồn · giống {n_giong} · cần chép {len(can)} · thừa trong gói {len(thua)}')
        for p, d, ly in can[:lim]:
            print(f'      {ly:<5} {d.relative_to(goi)}')
        if len(can) > lim:
            print(f'      … còn {len(can) - lim} tệp')
        for t in thua[:lim]:
            print(f'      thừa  {Path(dst_rel) / t}  (không xoá — người quyết)')
        if len(thua) > lim:
            print(f'      … còn {len(thua) - lim} tệp thừa')
        tong_thua += len(thua)
        if not a.thu:
            for p, d, ly in can:
                try:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, d)
                    if sha(p) != sha(d):
                        raise IOError('đọc lại không khớp sha256')
                    tong_chep += 1
                except Exception as e:  # noqa
                    loi += 1
                    print(f'      LỖI chép {d}: {e}')
        else:
            tong_chep += len(can)
    # tệp thừa trong các thư mục đích của bản đồ từng tệp (vd CONG_CU/tools, QUYET_DINH_ANH)
    don = {}
    for src_rel, dst_rel in BAN_DO:
        if (KHO / src_rel).is_file() or Path(src_rel).suffix:
            don.setdefault(str(Path(dst_rel).parent), set()).add(Path(dst_rel).name)
    for thu_muc, ten in sorted(don.items()):
        if chi and not any(s_.startswith(c) for s_, d_ in BAN_DO if str(Path(d_).parent) == thu_muc for c in chi):
            continue
        d = goi / thu_muc
        if not d.is_dir():
            continue
        thua = sorted(p.name for p in d.iterdir() if p.is_file() and p.name not in ten and not bo_qua(Path(p.name)))
        if thua:
            print(f' - {thu_muc}/: {len(thua)} tệp thừa (không có trong bản đồ, không xoá — người quyết): '
                  + ', '.join(thua[:lim]) + (' …' if len(thua) > lim else ''))
            tong_thua += len(thua)
    # skill NV
    sk = KHO / SKILL_NGUON
    if not chi or any(SKILL_NGUON.startswith(c) or c.startswith('claude') for c in chi):
        if sk.is_dir():
            data, crc = zip_skill(sk)
            zp = goi / SKILL_ZIP
            cu = {}
            if zp.exists():
                try:
                    with zipfile.ZipFile(zp) as z:
                        cu = {i.filename: i.CRC for i in z.infolist() if not i.is_dir()}
                except zipfile.BadZipFile:
                    cu = {}
            if cu == crc:
                print(f' - {SKILL_NGUON} → {SKILL_ZIP}: giống, không đóng lại')
            else:
                print(f' - {SKILL_NGUON} → {SKILL_ZIP}: {"đóng mới" if not cu else "khác → đóng lại"} ({len(crc)} tệp)')
                if not a.thu:
                    zp.write_bytes(data)
                tong_chep += 1
        else:
            print(f' - {SKILL_NGUON}: chưa có trong kho → không đóng {SKILL_ZIP} (giữ nguyên bản đang có trong gói)')
    gio = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    noi_dung = (f'PHIÊN BẢN QUY TẮC: {phien_ban}\nĐỒNG BỘ LÚC: {gio}\nSỐ TỆP CHÉP LẦN NÀY: {tong_chep}\n'
                f'NGUỒN: kho Sửa catalogue (tools/dong_bo_drive.py, một chiều, không xoá tệp trong gói)\n')
    if a.thu:
        print(f'CHẠY THỬ XONG: sẽ chép {tong_chep} tệp; {tong_thua} tệp thừa trong gói (không xoá). Không ghi gì.')
    else:
        (goi / 'PHIEN_BAN.txt').write_text(noi_dung, encoding='utf-8')
        print(f'XONG: đã chép {tong_chep} tệp ({loi} lỗi); {tong_thua} tệp thừa trong gói (không xoá); đã ghi PHIEN_BAN.txt.')
    return 1 if loi else 0


if __name__ == '__main__':
    sys.exit(main())
