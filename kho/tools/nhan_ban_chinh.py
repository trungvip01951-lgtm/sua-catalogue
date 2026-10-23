#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nhan_ban_chinh.py - nhận một PDF ứng viên đã được anh duyệt thành BẢN CHÍNH trong CATALOG SUA/CATALOGUE DA DUYET.

Dùng:
  nhan_ban_chinh.py --ung-vien <pdf> --dich "<HÃNG>/<HÃNG> - <Tên dòng>.pdf" --ly-do "<câu>" [--thu]
                    [--nguoi "Claude, <phiên>"] [--sao-luu history]

Các bước (theo claude/PHUONG_AN_DA_DUYET_20261013.md, mục Công cụ):
  1. Chạy tools/kiem_catalogue.py mục 1, 2, 8 trên ứng viên: mục 1 CHƯA ĐẠT thì DỪNG; mục 2, 8 chỉ cảnh báo.
  2. Sao lưu bản đang có (nếu có) sang <kho>/history/<UTC>_<tên>/ (không xoá gì).
  3. Chép đúng từng byte vào CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/, đọc lại sha256 phải khớp.
  4. Cập nhật dòng của tệp trong DANH SACH.txt (đúng định dạng dòng hiện có) + dòng tiêu đề "cập nhật".
  5. Nối 1 dòng vào sổ TIEN DO.md theo định dạng dòng cuối hiện có.
--thu: chạy thử, chỉ in việc sẽ làm, KHÔNG ghi gì.
Mã thoát: 0 xong/không cần làm · 2 tham số sai · 3 mục 1 CHƯA ĐẠT (dừng) · 4 lỗi ghi/đọc lại.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

KHO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kiem_catalogue as KC  # noqa: E402

DA_DUYET = KHO / 'CATALOG SUA' / 'CATALOGUE DA DUYET'
DANH_SACH = DA_DUYET / 'DANH SACH.txt'
TIEN_DO = KHO / 'CATALOG SUA' / 'BẢN MỚI 03-10-2026 (ChatGPT)' / '_BAO CAO' / 'TIEN DO.md'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for k in iter(lambda: f.read(1 << 20), b''):
            h.update(k)
    return h.hexdigest()


def doc_txt(p):
    raw = Path(p).read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    txt = raw.decode('utf-8-sig')
    nl = '\r\n' if '\r\n' in txt else '\n'
    return txt, nl, bom


def ghi_txt(p, txt, bom):
    Path(p).write_bytes((b'\xef\xbb\xbf' if bom else b'') + txt.encode('utf-8'))


def dong_danh_sach(txt, nl, ten, hang, sha12, mb, ly_do, gio):
    """Trả (văn bản mới, dòng cũ hoặc None, dòng mới)."""
    lines = txt.split(nl)
    mau = re.compile(r'^\s*-\s*' + re.escape(ten) + r'\s*\|')
    idx = [i for i, ln in enumerate(lines) if mau.match(ln)]
    cu = lines[idx[-1]] if idx else None
    ghi_chu_cu = ''
    if cu:
        phan = cu.split('|', 3)
        ghi_chu_cu = phan[3].strip() if len(phan) == 4 else ''
    ghi_chu = ly_do.strip().rstrip('.') + '.' + (f'  {ghi_chu_cu}' if ghi_chu_cu else '')
    moi = f'  - {ten}  |  mã kiểm {sha12}  |  {mb:.1f} MB  |  {ghi_chu}'
    if idx:
        lines[idx[-1]] = moi
    else:
        # chèn cuối mục hãng (trước dòng trống / mục hãng kế tiếp)
        try:
            dau = next(i for i, ln in enumerate(lines) if ln.strip() == hang)
        except StopIteration:
            lines += ['', hang]
            dau = len(lines) - 1
        cuoi = dau + 1
        while cuoi < len(lines) and lines[cuoi].strip() and lines[cuoi].strip() not in KC.HANG:
            cuoi += 1
        lines.insert(cuoi, moi)
    if lines and lines[0].startswith('CATALOGUE ĐÃ DUYỆT'):
        lines[0] = re.sub(r'cập nhật .*$', f'cập nhật {gio} UTC (nhan_ban_chinh.py: {ten})', lines[0])
    return nl.join(lines), cu, moi


def main(argv=None):
    ap = argparse.ArgumentParser(description='Nhận PDF ứng viên thành bản chính trong CATALOGUE DA DUYET (sao lưu, chép, '
                                             'đọc lại mã kiểm, cập nhật DANH SACH và TIEN DO).')
    ap.add_argument('--ung-vien', required=True, help='PDF ứng viên đã được anh duyệt')
    ap.add_argument('--dich', required=True, help='"<HÃNG>/<HÃNG> - <Tên dòng>.pdf"')
    ap.add_argument('--ly-do', required=True, help='một câu: vì sao thay / anh duyệt lúc nào')
    ap.add_argument('--thu', action='store_true', help='chạy thử, không ghi gì')
    ap.add_argument('--nguoi', default='Claude, nhan_ban_chinh.py', help='ghi vào sổ, vd "Claude điều phối, phiên ..."')
    ap.add_argument('--sao-luu', default='history', help='thư mục sao lưu trong kho (mặc định history)')
    a = ap.parse_args(argv)

    uv = Path(a.ung_vien)
    if not uv.is_file() or uv.suffix.lower() != '.pdf':
        print(f'LỖI: không thấy PDF ứng viên: {uv}')
        return 2
    phan = a.dich.replace('\\', '/').split('/')
    if len(phan) != 2 or phan[0] not in KC.HANG:
        print(f'LỖI: --dich phải dạng "<HÃNG>/<tên>.pdf", HÃNG ∈ {", ".join(KC.HANG)}; nhận: {a.dich}')
        return 2
    hang, ten = phan
    if not ten.lower().endswith('.pdf') or not ten.startswith(f'{hang} - ') or '..' in ten:
        print(f'LỖI: tên tệp phải theo chuẩn "{hang} - <Tên dòng>.pdf"; nhận: {ten}')
        return 2
    if not a.ly_do.strip():
        print('LỖI: --ly-do không được trống')
        return 2
    try:
        import pymupdf
        pymupdf.open(str(uv)).close()
    except Exception as e:  # noqa
        print(f'LỖI: ứng viên không mở được như PDF: {e}')
        return 2

    print(f'== NHẬN BẢN CHÍNH {"(CHẠY THỬ - không ghi gì)" if a.thu else ""}')
    print(f'   ứng viên: {uv}')
    print(f'   đích    : {DA_DUYET / hang / ten}')
    # 1) kiểm mục 1, 2, 8 (dùng tên đích để nhận hãng/nhóm)
    cfg = KC.doc_ho_so()
    ns = argparse.Namespace(du_lieu=None, nhanh=False, khong_dong_co=False)
    k = KC.KiemPDF(uv, cfg, ns)
    k.hang, k.nhom = KC.ten_hang_nhom(ten)
    kq = {1: k.muc1(), 2: k.muc2(), 8: k.muc8()}
    for so_muc, mm in kq.items():
        print(f'   kiểm mục {so_muc} {KC.TEN_MUC[so_muc]}: {mm.trang_thai()}')
        for s in (mm.loi + mm.kxm)[:8]:
            print(f'      - {s}')
    if kq[1].trang_thai() == KC.CHUA:
        print('DỪNG: mục 1 (chữ cấm / "50 Hz") CHƯA ĐẠT - không nhận bản chính.')
        return 3
    if kq[2].trang_thai() != KC.DAT or kq[8].trang_thai() != KC.DAT:
        print('   cảnh báo: mục 2 / 8 chưa đạt - vẫn nhận theo lệnh (anh đã duyệt), ghi rõ ở trên.')

    s_moi = sha(uv)
    mb = uv.stat().st_size / 1e6
    dich = DA_DUYET / hang / ten
    s_cu = sha(dich) if dich.exists() else None
    if s_cu == s_moi:
        print(f'KHÔNG CẦN LÀM: bản chính đã giống hệt ứng viên (sha256 {s_moi[:16]}…).')
        return 0
    bay_gio = datetime.now(timezone.utc)
    utc = bay_gio.strftime('%Y%m%dT%H%M%SZ')
    gio = bay_gio.strftime('%d/%m/%Y %H:%M')
    thu_muc_sl = KHO / a.sao_luu / f'{utc}_{Path(ten).stem}'
    txt, nl, bom = doc_txt(DANH_SACH)
    txt_moi, dong_cu, dong_moi = dong_danh_sach(txt, nl, ten, hang, s_moi[:12], mb, a.ly_do, gio)
    td_txt, td_nl, td_bom = doc_txt(TIEN_DO)
    cuoi = [ln for ln in td_txt.split(td_nl) if ln.strip()][-1]
    dong_td = (f'- {gio} ({a.nguoi}): NHẬN BẢN CHÍNH {hang}/{ten} — {a.ly_do.strip().rstrip(".")}; '
               f'SHA {s_moi[:16]}…, {mb:.1f} MB'
               + (f'; bản cũ SHA {s_cu[:16]}… sao lưu {a.sao_luu}/{thu_muc_sl.name}/' if s_cu else '; tệp mới (chưa có bản cũ)')
               + '.')
    if not cuoi.startswith('- '):
        print('   lưu ý: dòng cuối sổ TIEN DO không theo dạng "- dd/mm/yyyy hh:mm (...)": vẫn ghi dạng gạch đầu dòng')
    print(f'   sha256 ứng viên: {s_moi}')
    print(f'   bản đang có    : {s_cu or "(chưa có)"}')
    print(f'   sao lưu        : {thu_muc_sl if s_cu else "(không cần)"}')
    print(f'   DANH SACH cũ   : {dong_cu or "(không có dòng — sẽ thêm vào mục " + hang + ")"}')
    print(f'   DANH SACH mới  : {dong_moi}')
    print(f'   TIEN DO + dòng : {dong_td}')
    if a.thu:
        print('CHẠY THỬ XONG: không ghi gì.')
        return 0
    # 2) sao lưu
    if s_cu:
        thu_muc_sl.mkdir(parents=True, exist_ok=False)
        shutil.copy2(dich, thu_muc_sl / ten)
        if sha(thu_muc_sl / ten) != s_cu:
            print('LỖI: bản sao lưu không khớp mã kiểm - dừng, chưa thay bản chính.')
            return 4
    # 3) chép đúng byte + đọc lại
    dich.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(uv, dich)
    if sha(dich) != s_moi:
        print('LỖI: đọc lại bản chính KHÔNG khớp mã kiểm ứng viên!')
        if s_cu:
            shutil.copyfile(thu_muc_sl / ten, dich)
            print('   đã chép trả bản cũ từ sao lưu.')
        return 4
    # 4) DANH SACH, 5) TIEN DO
    ghi_txt(DANH_SACH, txt_moi, bom)
    them = ('' if td_txt.endswith(td_nl) else td_nl) + dong_td + td_nl
    with open(TIEN_DO, 'ab') as f:
        f.write(them.encode('utf-8'))
    print(f'XONG: bản chính {hang}/{ten} = sha256 {s_moi[:16]}… (đọc lại khớp); '
          f'{"đã sao lưu bản cũ; " if s_cu else ""}đã cập nhật DANH SACH.txt và TIEN DO.md.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
