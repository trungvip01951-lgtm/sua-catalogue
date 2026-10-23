#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kiem_catalogue.py - phiếu kiểm tự động 10 mục cho catalogue PDF (dự án Sửa catalogue bơm).

Căn cứ: claude/PHUONG_AN_DA_DUYET_20261013.md (mục Công cụ, Chuẩn biểu đồ và bảng, Chuẩn chữ/tệp,
Định nghĩa hoàn thành) và rules/HO_SO_HANG.json. MỌI ngưỡng chuẩn đọc từ HO_SO_HANG.json; trong mã chỉ
có tham số đo hình học (dung sai toạ độ) và vài giá trị mặc định ghi rõ nguồn khi json chưa có khoá.

Dùng:
  kiem_catalogue.py <pdf hoặc thư mục> [--bo3 <pdf AQUARIS> <pdf PEROTAC> <pdf REDPUMP>]
                    [--du-lieu DU_LIEU/<nhóm>.xlsx] [--json <tệp ra>] [--muc 1,2,...]
                    [--nhanh] [--tu-ghep-bo3] [--day-du] [--khong-dong-co]
Mỗi mục: ĐẠT / CHƯA ĐẠT / CHƯA THỂ XÁC MINH (BỎ QUA khi không chạy). "Cảnh báo" không đổi trạng thái.
Nguyên tắc: không đoán. Máy không đo được thì ghi CHƯA THỂ XÁC MINH, không bao giờ ghi ĐẠT thay.
Công cụ chỉ ĐỌC PDF; chỉ ghi tệp --json nếu người dùng chỉ định.

Tệp số liệu --du-lieu (xlsx): dạng chính giống tools/ve_duong_cong.py - sheet QH cột hang | model | q_m3h | h_m
(lọc theo hãng của PDF; hang trống/"*"/"CHUNG" = cả 3 hãng). Dạng phụ: bảng rộng có hàng tiêu đề "Model..." và
>=3 ô số là các mức Q (m³/h). Không nhận ra dạng nào thì phần so số của mục 4 ghi CHƯA THỂ XÁC MINH.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np
import pymupdf

KHO = Path(__file__).resolve().parents[1]
TEP_HO_SO = KHO / 'rules' / 'HO_SO_HANG.json'
THU_MUC_DA_DUYET = KHO / 'CATALOG SUA' / 'CATALOGUE DA DUYET'
TEP_DANH_SACH = THU_MUC_DA_DUYET / 'DANH SACH.txt'
HANG = ('AQUARIS', 'PEROTAC', 'REDPUMP')

DAT, CHUA, KXM, BO = 'ĐẠT', 'CHƯA ĐẠT', 'CHƯA THỂ XÁC MINH', 'BỎ QUA'
TEN_MUC = {
    1: 'Chữ cấm + "50 Hz" trang 1', 2: 'Điện / pha', 3: 'Bảng số Q–H', 4: 'Đường cong',
    5: 'Chữ chồng + cỡ chữ', 6: 'Ảnh', 7: 'Tương phản màu chữ',
    8: 'Tệp: khổ, dung lượng, phông, CMYK, khoảng trống', 9: 'Khác giao diện giữa 3 hãng',
    10: 'Mã kiểm khớp DANH SACH',
}
# Nhóm không có động cơ (không bắt buộc "50 Hz" trang 1) - theo đề bài: đĩa phân phối khí.
NHOM_KHONG_DONG_CO = ('đĩa phân phối khí', 'dia phan phoi khi')
# Thiết bị không có đường Q–H (tự nhận theo tên nhóm; cờ --khong-qh ép tay)
NHOM_KHONG_QH = ('máy thổi khí', 'máy khuấy', 'định lượng', 'đĩa phân phối khí')
# Giá trị mặc định khi HO_SO_HANG.json CHƯA có khoá (phiếu ghi rõ nguồn):
MAC_DINH_MOT_PHA_KW = 3.0     # phương án 13/10: mã 1 pha tối đa 3 kW (CDLFM… "đến 3 kW")
MAC_DINH_GIONG_TOI_DA = 0.6   # ngưỡng ĐỀ XUẤT độ giống ảnh giữa 2 hãng (chưa được anh duyệt)
MAC_DINH_SO_PHONG_TOI_DA = 2  # phương án 13/10 "Chuẩn chữ, tệp": ≤2 phông/tệp
# Tham số đo (không phải chuẩn): dung sai hình học, đơn vị pt.
DUNG_SAI_KHO_PT = 2.0
DASH = {'–', '-', '—', '−', '‒'}
RE_SO = re.compile(r'^[+]?\d+(?:[.,]\d+)?$')
RE_DON_VI_Q = re.compile(r'^\(?(m³/h|m3/h|m³/min|m3/min)\)?[,;:]?$', re.I)
KY_TU_CHI_SO = set('¹²³⁰⁴⁵⁶⁷⁸⁹⁺⁻®™°')  # chỉ số trên, ký hiệu: không đếm vào cỡ chữ
RE_VIET = re.compile(r'[ăâđêôơưĂÂĐÊÔƠƯẠ-ỹ]')


def doc_ho_so():
    return json.loads(TEP_HO_SO.read_text(encoding='utf-8-sig'))


def sha256_tep(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for k in iter(lambda: f.read(1 << 20), b''):
            h.update(k)
    return h.hexdigest()


def so(t):
    t = t.strip().rstrip(',;')
    if not RE_SO.match(t):
        return None
    return float(t.replace(',', '.'))


def ten_hang_nhom(path):
    ten = Path(path).stem
    m = re.match(r'^(AQUARIS|PEROTAC|REDPUMP)\s*-\s*(.+)$', ten)
    if m:
        return m.group(1), m.group(2).strip()
    return None, ten


class Muc:
    def __init__(self, so_muc):
        self.so = so_muc
        self.loi, self.canh_bao, self.kxm, self.ghi_chu = [], [], [], []
        self.loi_goc = []  # với --goc: lỗi đã có ở bản gốc / ngoài trang vá — không tính
        self.ep = None

    def trang_thai(self):
        if self.ep:
            return self.ep
        if self.loi:
            return CHUA
        if self.kxm:
            return KXM
        return DAT

    def dict(self):
        return {'muc': self.so, 'ten': TEN_MUC[self.so], 'trang_thai': self.trang_thai(), 'loi': self.loi,
                'chua_the_xac_minh': self.kxm, 'canh_bao': self.canh_bao, 'ghi_chu': self.ghi_chu,
                'loi_co_tu_ban_goc': self.loi_goc}


# ----------------------------------------------------------------------------- tiện ích hình học / chữ
def hang_tu(words, tol=2.5):
    rows = []
    for w in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
        y = (w[1] + w[3]) / 2
        if rows and abs(rows[-1][0] - y) < tol:
            rows[-1][1].append(w)
        else:
            rows.append([y, [w]])
    for r in rows:
        r[1].sort(key=lambda w: w[0])
    return rows


def xc(w):
    return (w[0] + w[2]) / 2


def yc(w):
    return (w[1] + w[3]) / 2


def lay_mau_items(items, n_c=24):
    """Tách path thành các đoạn liền (subpath) - trả list [(np.array Nx2, có_cong, số_đoạn_thẳng)]."""
    subs, cur, has_c, n_l, last = [], [], False, 0, None
    t = np.linspace(0, 1, n_c)[:, None]
    for it in items:
        k = it[0]
        if k == 'l':
            pts = np.array([[it[1].x, it[1].y], [it[2].x, it[2].y]])
        elif k == 'c':
            p = [np.array([q.x, q.y]) for q in it[1:5]]
            pts = (1 - t) ** 3 * p[0] + 3 * (1 - t) ** 2 * t * p[1] + 3 * (1 - t) * t ** 2 * p[2] + t ** 3 * p[3]
        else:  # re / qu: không phải đường cong
            if cur:
                subs.append((np.vstack(cur), has_c, n_l))
            cur, has_c, n_l, last = [], False, 0, None
            continue
        if last is not None and math.hypot(pts[0][0] - last[0], pts[0][1] - last[1]) > 0.6:
            subs.append((np.vstack(cur), has_c, n_l))
            cur, has_c, n_l = [], False, 0
        cur.append(pts if not cur else pts[1:])
        has_c = has_c or k == 'c'
        n_l += k == 'l'
        last = pts[-1]
    if cur:
        subs.append((np.vstack(cur), has_c, n_l))
    return subs


def la_net_dut(d):
    ds = d.get('dashes')
    if not ds:
        return False
    m = re.match(r'\[\s*([^\]]*)\]', str(ds))
    return bool(m and m.group(1).strip())


def tim_bieu_do(drawings, words):
    """Vùng biểu đồ = khung lưới (>=3 đường ngang cùng bề ngang + >=1 đường đứng) - lọc tiếp ở chỗ có đường cong."""
    H, V = [], []
    for d in drawings:
        typ = d.get('type') or ''
        for it in d['items']:
            if it[0] == 'l' and 's' in typ:
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 0.6 and abs(a.x - b.x) >= 25:
                    H.append((min(a.x, b.x), max(a.x, b.x), (a.y + b.y) / 2))
                elif abs(a.x - b.x) < 0.6 and abs(a.y - b.y) >= 25:
                    V.append((min(a.y, b.y), max(a.y, b.y), (a.x + b.x) / 2))
            elif it[0] == 're':
                r = it[1]
                if 's' in typ and r.width >= 25 and r.height >= 25:
                    H += [(r.x0, r.x1, r.y0), (r.x0, r.x1, r.y1)]
                    V += [(r.y0, r.y1, r.x0), (r.y0, r.y1, r.x1)]
                elif typ == 'f' and min(r.width, r.height) <= 1.2:
                    if r.width >= 25:
                        H.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
                    elif r.height >= 25:
                        V.append((r.y0, r.y1, (r.x0 + r.x1) / 2))
    nhom = []
    for h in sorted(H):
        for g in nhom:
            if abs(g[0] - h[0]) < 3 and abs(g[1] - h[1]) < 3:
                g[2].append(h[2])
                break
        else:
            nhom.append([h[0], h[1], [h[2]]])
    hop = []
    for x0, x1, ys in nhom:
        ys = sorted(set(round(y, 0) for y in ys))
        if len(ys) < 3 or x1 - x0 < 60 or ys[-1] - ys[0] < 40:
            continue
        y0, y1 = ys[0], ys[-1]
        dung = [v for v in V if x0 - 2 <= v[2] <= x1 + 2 and min(v[1], y1) - max(v[0], y0) >= 0.7 * (y1 - y0)]
        if dung:
            vy0, vy1 = min(v[0] for v in dung), max(v[1] for v in dung)
            hop.append([x0, max(y0, vy0 - 1), x1, min(y1, vy1 + 1)])
    hop.sort(key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))
    kq = []
    for b in hop:
        if any(min(b[2], k[2]) - max(b[0], k[0]) > 0.8 * (b[2] - b[0]) and
               min(b[3], k[3]) - max(b[1], k[1]) > 0.8 * (b[3] - b[1]) for k in kq):
            continue
        kq.append(b)
    return [pymupdf.Rect(b) for b in kq]


def duong_cong_trong(drawings, box, vat_can=None):
    """Đường cong (nét liền, nét đứt) nằm trong khung box."""
    cong, dut = [], []
    vung = pymupdf.Rect(box.x0 - 6, box.y0 - 6, box.x1 + 6, box.y1 + 6)
    for d in drawings:
        typ = d.get('type') or ''
        if 's' not in typ or d.get('fill') is not None or d.get('closePath'):
            continue
        for P, has_c, n_l in lay_mau_items(d['items']):
            if len(P) < 3 or (not has_c and n_l < 2):
                continue
            x0, y0 = P.min(0)
            x1, y1 = P.max(0)
            if max(x1 - x0, y1 - y0) < 15 or x1 - x0 < 6:
                continue
            if math.hypot(*(P[0] - P[-1])) < 1.0:
                continue
            seg = np.diff(P, axis=0)
            L = np.hypot(seg[:, 0], seg[:, 1])
            if L.sum() <= 0:
                continue
            truc = (np.abs(seg[:, 0]) < 0.05) | (np.abs(seg[:, 1]) < 0.05)
            if L[truc].sum() > 0.95 * L.sum():
                continue
            trong = ((P[:, 0] >= box.x0 - 2) & (P[:, 0] <= box.x1 + 2) & (P[:, 1] >= box.y0 - 2) & (P[:, 1] <= box.y1 + 2))
            if not (vung.contains(pymupdf.Point(x0, y0)) and vung.contains(pymupdf.Point(x1, y1))) and trong.mean() < 0.7:
                continue
            vuot = max(box.x0 - x0, x1 - box.x1, box.y0 - y0, y1 - box.y1, 0)
            if P[-1][0] < P[0][0]:
                P = P[::-1]
            rec = {'P': P, 'seqno': d.get('seqno', 0), 'width': d.get('width') or 0, 'color': d.get('color'),
                   'rect': pymupdf.Rect(x0, y0, x1, y1), 'dut': la_net_dut(d), 'vuot': vuot}
            cong.append(rec)
    return ghep_manh(cong, vat_can or []), dut


def _huong(v):
    return math.degrees(math.atan2(v[1], v[0]))


def ghep_manh(cong, vat_can=()):
    """Ghép các mảnh cùng màu, cùng nét, nối đuôi nhau (≤1 pt, lệch hướng ≤20°) thành một đường."""
    cong = list(cong)
    doi = True
    while doi:
        doi = False
        for a in range(len(cong)):
            for b in range(len(cong)):
                if a == b:
                    continue
                A, B = cong[a], cong[b]
                if abs(A['width'] - B['width']) > 0.05 or A['dut'] != B['dut']:
                    continue
                ca, cb = A['color'] or (0, 0, 0), B['color'] or (0, 0, 0)
                if len(ca) != len(cb) or max(abs(x - y) for x, y in zip(ca, cb)) > 0.02:
                    continue
                ho = math.hypot(*(A['P'][-1] - B['P'][0]))
                if ho > 25 or B['P'][0][0] < A['P'][-1][0] - 0.5:
                    continue
                g = abs(_huong(A['P'][-1] - A['P'][-2]) - _huong(B['P'][1] - B['P'][0]))
                if min(g, 360 - g) > 20:
                    continue
                if ho > 1.0:
                    # khe ho có chủ ý để đặt nhãn (chữ / dấu tròn số) → vẫn là một đường
                    cau = pymupdf.Rect(A['P'][-1][0], min(A['P'][-1][1], B['P'][0][1]),
                                       B['P'][0][0], max(A['P'][-1][1], B['P'][0][1])) + (-1, -1, 1, 1)
                    if not any(cau.intersects(r) for r in vat_can):
                        continue
                    g2 = abs(_huong(B['P'][0] - A['P'][-1]) - _huong(A['P'][-1] - A['P'][-2]))
                    if min(g2, 360 - g2) > 25:
                        continue
                A.update({'P': np.vstack([A['P'], B['P'][1:]]), 'rect': A['rect'] | B['rect'],
                          'seqno': max(A['seqno'], B['seqno'])})
                cong.pop(b)
                doi = True
                break
            if doi:
                break
    return cong


def fit_truc(vals_pos):
    if len(vals_pos) < 3:
        return None
    pos = np.array([p for p, v in vals_pos])
    val = np.array([v for p, v in vals_pos])
    if len(set(val)) < 3:
        return None
    a, b = np.polyfit(pos, val, 1)
    rng = val.max() - val.min()
    if rng <= 0 or np.abs(a * pos + b - val).max() > 0.02 * rng:
        return None
    return float(a), float(b)


def chuan_truc(box, words):
    """Quy đổi toạ độ → giá trị theo nhãn số trên trục: {'x': (a,b)|None, 'x_don_vi', 'y': (a,b)|None}."""
    kq = {'x': None, 'y': None, 'x_don_vi': None}
    cand = [w for w in words if so(w[4]) is not None and box.x0 - 12 <= xc(w) <= box.x1 + 12
            and box.y1 + 0.5 <= yc(w) <= box.y1 + 30]
    fits = []
    for y, r in hang_tu(cand, 2.0):
        f = fit_truc([(xc(w), so(w[4])) for w in r])
        if f and f[0] > 0:
            dv = None
            for w in words:
                if abs(yc(w) - y) < 2.5:
                    mt = RE_DON_VI_Q.match(w[4]) or re.match(r'^\(?(l/min|l/s)\)?', w[4], re.I)
                    if mt:
                        dv = mt.group(1).replace('m3', 'm³').lower()
            fits.append((y, f, dv))
    kq['x_rows'] = [f[0] for f in fits]
    if len(fits) == 1 and fits[0][2] is None:
        nhan = ' '.join(w[4] for w in words if box.x0 - 60 <= xc(w) <= box.x1 + 60 and box.y1 <= yc(w) <= box.y1 + 42)
        if re.search(r'm³/h|m3/h', nhan) and not re.search(r'l/min|m³/min', nhan):
            fits = [(fits[0][0], fits[0][1], 'm³/h')]
    if fits:
        chon = [f for f in fits if f[2] == 'm³/h']
        if not chon and len(fits) >= 2 and all(f[2] is None for f in fits):
            fs = sorted(fits, key=lambda f: f[1][0])
            if abs(fs[1][1][0] / fs[0][1][0] - 16.667) / 16.667 < 0.06:
                chon = [(fs[0][0], fs[0][1], 'm³/h')]
        if not chon:
            chon = [fits[0]]
        kq['x'], kq['x_don_vi'] = chon[0][1], chon[0][2]
    best = None
    for ben, lo, hi in (('trai', box.x0 - 40, box.x0 - 0.3), ('phai', box.x1 + 0.3, box.x1 + 40)):
        cand = [w for w in words if so(w[4]) is not None and lo <= xc(w) <= hi and box.y0 - 6 <= yc(w) <= box.y1 + 6]
        if len(cand) < 3:
            continue
        cols = {}
        for w in cand:
            cols.setdefault(round((w[2] if ben == 'trai' else w[0]) / 4), []).append(w)
        for ws in cols.values():
            f = fit_truc([(yc(w), so(w[4])) for w in ws])
            if f and f[0] < 0:
                d = min(abs((w[2] if ben == 'trai' else w[0]) - (box.x0 if ben == 'trai' else box.x1)) for w in ws)
                if best is None or d < best[0]:
                    best = (d, f, ben)
    if best:
        kq['y'], kq['y_ben'] = best[1], best[2]
    return kq


def chu_trong(words, *rects):
    return ' '.join(w[4] for w in words if any(r.contains(pymupdf.Point(xc(w), yc(w))) for r in rects))


def nhan_dang_qh(box, words):
    """Biểu đồ Q–H: nhãn trục đứng có H/Head/(m), nhãn trục ngang có Q/m³/h/l/min."""
    ytxt = chu_trong(words, pymupdf.Rect(box.x0 - 120, box.y0 - 30, box.x0 + 2, box.y1 + 5),
                     pymupdf.Rect(box.x1 - 2, box.y0 - 30, box.x1 + 120, box.y1 + 5),
                     pymupdf.Rect(box.x0 - 60, box.y0 - 30, box.x0 + 90, box.y0 + 1))
    xtxt = chu_trong(words, pymupdf.Rect(box.x0 - 60, box.y1, box.x1 + 60, box.y1 + 45))
    co_h = re.search(r'(^|\s)H(\s|$)|\(m\)', ytxt) or \
        (re.search(r'\bhead\b', ytxt, re.I) and not re.search(r'loss|k?Pa\b|mbar|mmAq', ytxt, re.I))
    co_q = re.search(r'm³/h|m3/h|l/min', xtxt)
    return bool(co_h and co_q)


def danh_dau_phu(c, words):
    """Đánh dấu đường phụ (hiệu suất η, công suất...) để không đếm là đường model:
    - kiểu nét (màu+độ dày) khác nhóm chính khi nhóm chính có >=3 đường;
    - đường có bướu (lên rồi xuống) khi quanh biểu đồ có chữ η/Eff/%."""
    from collections import Counter
    key = lambda cc: (tuple(round(x, 2) for x in (cc['color'] or ())), round(cc['width'], 2))  # noqa
    st = Counter(key(cc) for cc in c['cong'])
    chinh, n = st.most_common(1)[0] if st else (None, 0)
    b = c['box']
    eta = re.search(r'η|eff|%', chu_trong(words, pymupdf.Rect(b.x0 - 60, b.y0 - 30, b.x1 + 60, b.y1 + 45)), re.I)
    for cc in c['cong']:
        cc['phu'] = None
        if n >= 3 and st[key(cc)] == 1 and not cc['dut']:
            cc['phu'] = 'kiểu nét khác nhóm chính'
        elif eta:
            dy = np.diff(cc['P'][:, 1])
            up, tot = -dy.clip(max=0).sum(), np.abs(dy).sum()
            if tot > 0 and up > 0.3 * tot and dy.clip(min=0).sum() > 0.2 * tot:
                cc['phu'] = 'đường có bướu (hiệu suất η?)'
    c['chinh'] = [cc for cc in c['cong'] if not cc['phu']]


def phan_tich_duong(c, box):
    # (lỗi[], cảnh báo[]) cho một đường Q–H; c['P'] toạ độ trang (y hướng xuống), đã xếp Q tăng.
    loi, cb = [], []
    P = c['P'] if c['P'][0][0] <= c['P'][-1][0] else c['P'][::-1]
    seg = np.diff(P, axis=0)
    xr = P[:, 0].max() - P[:, 0].min()
    back = -seg[:, 0][seg[:, 0] < -0.05].sum()
    if back > max(1.0, 0.01 * xr):
        loi.append(f'đường quay ngược theo trục ngang {back:.1f} pt (móc/vòng)')
    L = np.hypot(seg[:, 0], seg[:, 1])
    cum = np.r_[0, np.cumsum(L)]
    tol = max(1.0, 0.01 * box.height)
    up = -seg[:, 1].clip(max=0)
    if up.sum() > tol:
        idx = np.nonzero(up > 0.02)[0]
        frac = (cum[idx].mean() / cum[-1]) if len(idx) and cum[-1] else 0.5
        vt = 'đầu đường (móc đầu)' if frac < 0.2 else ('cuối đường (móc cuối)' if frac > 0.8 else 'giữa đường (gợn)')
        loi.append(f'H tăng khi Q tăng: tổng {up.sum():.1f} pt ở {vt}')
    # hình dạng trong toạ độ chuẩn hoá theo khung (Q sang phải, H lên trên, 0..1)
    U = np.c_[(P[:, 0] - box.x0) / max(box.width, 1e-6), (box.y1 - P[:, 1]) / max(box.height, 1e-6)]
    su = np.diff(U, axis=0)
    cu = np.r_[0, np.cumsum(np.hypot(su[:, 0], su[:, 1]))]
    if cu[-1] < 0.05:
        return loi, cb
    N = 80
    sx = np.linspace(0, cu[-1], N + 1)
    V = np.c_[np.interp(sx, cu, U[:, 0]), np.interp(sx, cu, U[:, 1])]
    ang = np.degrees(np.unwrap(np.arctan2(np.diff(V[:, 1]), np.diff(V[:, 0]))))
    da = ang[4:] - ang[:-4]  # đổi hướng trong 5% chiều dài
    j = int(np.argmax(np.abs(da)))
    dau_cuoi = None
    a_end, a_ref = ang[-4:].mean(), ang[-20:-4].mean()
    if abs(a_end - a_ref) > 40:
        loi.append(f'gãy góc {abs(a_end - a_ref):.0f}° ở cuối đường (móc cuối)')
        dau_cuoi = 'cuoi'
    a_st, a_rf = ang[:4].mean(), ang[4:20].mean()
    if abs(a_st - a_rf) > 40:
        loi.append(f'gãy góc {abs(a_st - a_rf):.0f}° ở đầu đường (móc đầu)')
        dau_cuoi = 'dau'
    vi_tri = j / len(da)
    if abs(da[j]) > 25 and not (dau_cuoi == 'cuoi' and vi_tri > 0.85) and not (dau_cuoi == 'dau' and vi_tri < 0.15):
        loi.append(f'đường không cong đều: đổi hướng {abs(da[j]):.0f}° trong 5% chiều dài ở {vi_tri:.0%} đường '
                   f'(dốc {ang[j]:.0f}° → {ang[j + 4]:.0f}°, đoạn phẳng rồi dốc gắt / gãy)')
    khuc = []
    for x in np.diff(ang):
        if abs(x) <= 1e-3:
            continue
        sg = 1 if x > 0 else -1
        if khuc and khuc[-1][0] == sg:
            khuc[-1][1] += abs(x)
        else:
            khuc.append([sg, abs(x)])
    khuc = [k for k in khuc if k[1] >= 2.0]
    gop = []
    for k in khuc:
        if gop and gop[-1][0] == k[0]:
            gop[-1][1] += k[1]
        else:
            gop.append(list(k))
    n_uon = max(0, len(gop) - 1)
    c['n_uon'] = n_uon
    if n_uon > 1:
        loi.append(f'đường không cong đều: {n_uon} điểm uốn (chuẩn: tối đa 1)')
    return loi, cb


def noi_dau_duong(cong, tr=None, box=None, qh=True):
    """Đầu/cuối của 2 đường khác nhau chạm nhau (≤2,5 pt, không nằm trên mép khung) → nhìn như một
    đường gãy (móc). Thêm: 2 đường vẽ trùng khít nhau."""
    kq = []
    dau = [(k, c['P']) for k, c in enumerate(cong)]

    def tren_mep(p):
        return box is not None and (abs(p[0] - box.x0) < 2 or abs(p[0] - box.x1) < 2 or
                                    abs(p[1] - box.y0) < 2 or abs(p[1] - box.y1) < 2)
    for a in range(len(dau)):
        for b in range(a + 1, len(dau)):
            ka, A = dau[a]
            kb, B = dau[b]
            if abs(A[0][0] - B[0][0]) < 1 and abs(A[-1][0] - B[-1][0]) < 1 and A[-1][0] - A[0][0] > 5:
                xs = np.linspace(A[0][0], A[-1][0], 30)
                if np.abs(np.interp(xs, A[:, 0], A[:, 1]) - np.interp(xs, B[:, 0], B[:, 1])).mean() < 0.8:
                    kq.append(f'đường {ka + 1} và đường {kb + 1} vẽ trùng khít nhau (một đường bị vẽ 2 lần)')
                    continue
            if not qh:
                continue
            for ea, pa, va, eb, pb, vb in (('cuối', A[-1], A[-1] - A[-3], 'đầu', B[0], B[2] - B[0]),
                                           ('đầu', A[0], A[2] - A[0], 'cuối', B[-1], B[-1] - B[-3])):
                if True:
                    if math.hypot(*(pa - pb)) <= 2.5 and not tren_mep(pa) and not tren_mep(pb):
                        g = abs(math.degrees(math.atan2(va[1], va[0]) - math.atan2(vb[1], vb[0])))
                        g = min(g, 360 - g)
                        vt = f'({pa[0]:.0f},{pa[1]:.0f})'
                        if tr and tr.get('x') and tr.get('y'):
                            vt += f' [Q≈{tr["x"][0] * pa[0] + tr["x"][1]:.3g}, H≈{tr["y"][0] * pa[1] + tr["y"][1]:.3g}]'
                        kq.append(f'{ea} đường {ka + 1} chạm {eb} đường {kb + 1} tại {vt}, lệch hướng {g:.0f}° '
                                  f'→ nhìn như một đường gãy (móc)')
    return kq


# ----------------------------------------------------------------------------- bảng số
def tim_bang(words, charts):
    rows = hang_tu(words)
    bangs = []
    for i, (y, r) in enumerate(rows):
        don_vi = [j for j, w in enumerate(r) if RE_DON_VI_Q.match(w[4]) or re.match(r'^\(?(l/min|l/s)\)?$', w[4])]
        x_min = None
        for j, w in enumerate(r):
            if not RE_DON_VI_Q.match(w[4]):
                continue
            if j > 0 and so(r[j - 1][4]) is not None:
                continue  # "156 m³/h" là số lượng, không phải tiêu đề cột
            if w[4].startswith('(') and j > 0 and r[j - 1][4] == 'Q' and not any(
                    re.match(r'^(MODEL|Model|kW)$', x[4]) for yy, rr in rows if y - 45 <= yy <= y + 20 for x in rr):
                continue  # "Q (m³/h)" không có chữ bảng quanh đó → nhãn trục biểu đồ
            sau = [jj for jj in don_vi if jj > j]
            nums = [x for x in r[j + 1:(sau[0] if sau else len(r))] if so(x[4]) is not None]
            if len(nums) < 3:  # tiêu đề lệch dòng: đơn vị và các mức Q cách nhau ≤4 pt
                ke = [x for yy, rr in rows if 0 < abs(yy - y) <= 4 for x in rr if x[0] > w[2]]
                dv_ke = [x[0] for x in ke if RE_DON_VI_Q.match(x[4]) or re.match(r'^\(?(l/min|l/s)\)?$', x[4])]
                het_x = min(dv_ke) if dv_ke else 1e9
                if sau:
                    het_x = min(het_x, r[sau[0]][0])
                nums = sorted([x for x in ke if so(x[4]) is not None and x[0] < het_x], key=lambda x: x[0])
                if nums and nums[0][0] - w[2] > 80:
                    nums = []
            if len(nums) < 3:
                continue
            if any(abs(y - yy) < 3 and xc(nums[0]) >= c['box'].x0 - 12 and xc(nums[-1]) <= c['box'].x1 + 12
                   for c in charts for yy in c['truc'].get('x_rows', [])):
                continue  # hàng nhãn trục biểu đồ
            vals = [so(x[4]) for x in nums]
            if any(b <= a for a, b in zip(vals, vals[1:])):
                continue
            b = doc_bang(rows, y, w, nums, vals, x_min)
            if b and b['rows']:
                bangs.append(b)
            qx = [xc(x) for x in nums]
            x_min = qx[-1] + 0.45 * min(bb - aa for aa, bb in zip(qx, qx[1:]))
    return bangs


def la_ma(t):
    return bool(re.search(r'[A-Za-z]', t) and re.search(r'\d', t) and len(t) >= 3
                and not re.match(r'^(IP\d+|G\d|DN\d|PG\d)', t) and 'phase' not in t.lower() and '~' not in t and '=' not in t
                and t.lower() not in ('m³/h', 'l/min', 'm³/min'))


def doc_bang(rows, y_hdr, unit_w, nums, vals, x_min=None):
    """Đọc bảng dạng hàng: mỗi model một hàng, cột là các mức Q. Hàng tên model có thể lệch dòng với hàng số."""
    qx = [xc(x) for x in nums]
    tol = 0.45 * min(b - a for a, b in zip(qx, qx[1:]))
    band = [w for y, r in rows if y_hdr - 45 <= y <= y_hdr + 20 for w in r]
    kw = [w for w in band if w[4].strip('()').lower() == 'kw' and w[0] < qx[0] - tol]
    kw_x = xc(max(kw, key=lambda w: w[0])) if kw else None  # chữ "kW" sát cột Q nhất (bỏ "kW" trong lời bên lề)
    lim = (kw_x - 10) if kw_x else qx[0] - tol
    if x_min is not None:
        band = [w for w in band if w[0] >= x_min]
    keys = [w for w in band if re.match(r'^(MODEL|Model|TYPE|Type|No\.?|3~|1~)$', w[4]) and w[0] < lim]
    left = (min(w[0] for w in keys) - 60) if keys else None
    if x_min is not None:
        left = max(left or x_min, x_min)
    seq, last_y, pitch = [], y_hdr, None
    for y, r in rows:
        if y <= y_hdr + 3:
            continue
        if y - last_y > (max(30.0, 2.6 * pitch) if pitch else 60.0):
            break
        chu_cot = [w for w in r if re.search(r'[A-Za-z]', w[4]) and so(w[4]) is None and
                   min(abs(xc(w) - q) for q in qx) <= tol]
        if len(set(int(np.argmin([abs(xc(w) - q) for q in qx])) for w in chu_cot)) >= 3:
            break  # hàng tiêu đề của bảng khác (vd bảng kích thước)
        dv = [w for w in r if re.match(r'^\(?(l/min|l/s|m³/min|m3/min|m³/h|m3/h)\)?$', w[4], re.I)
              and xc(w) < qx[0] - tol and (left is None or w[0] >= left)]
        if dv:
            sau_dv = [so(w[4]) for w in r if so(w[4]) is not None and w[0] > dv[0][2]]
            tang = len(sau_dv) >= 3 and all(b2 > a2 for a2, b2 in zip(sau_dv, sau_dv[1:]))
            if tang and any(RE_DON_VI_Q.match(w[4]) for w in dv):
                break  # bảng mới
            if tang:
                continue  # hàng đơn vị phụ (l/min)
            # còn lại: chữ đơn vị nằm trong lời bên lề (vd "Max. flow rate 60 m³/h") → xử lý hàng như thường
        cells = {}
        for w in r:
            if xc(w) < qx[0] - tol:
                continue
            k = int(np.argmin([abs(xc(w) - q) for q in qx]))
            if abs(xc(w) - qx[k]) > tol:
                continue
            v = so(w[4])
            if v is not None:
                cells[k] = v
            elif w[4] in DASH:
                cells[k] = '–'
        so_o = {k: v for k, v in cells.items() if v != '–'}
        if len(so_o) >= 3 and all(abs(v - vals[k] * 16.667) <= max(1.0, 0.02 * v) for k, v in so_o.items()):
            continue  # hàng quy đổi l/min (= Q × 16,667), không phải hàng H
        trai = [w for w in r if w[2] <= qx[0] - tol * 0.5 and (left is None or w[0] >= left)]
        toks = []
        for w in trai:
            if toks and re.fullmatch(r'[A-Za-z]{1,6}', toks[-1][4]) and w[0] - toks[-1][2] < 6 and xc(w) < lim:
                toks[-1] = (toks[-1][0], toks[-1][1], w[2], w[3], toks[-1][4] + ' ' + w[4])
            else:
                toks.append(tuple(w[:5]))
        seq.append({'y': y, 'cells': cells, 'toks': toks, 'gan': []})
        if len(cells) >= 2:
            if pitch is None and last_y != y_hdr:
                pitch = y - last_y
            last_y = y
    gia_tri = [x for x in seq if len(x['cells']) >= 2]
    if not gia_tri:
        return None
    for x in seq:
        if len(x['cells']) >= 2 or not any(la_ma(t[4]) and xc(t) < lim for t in x['toks']):
            continue
        v = min(gia_tri, key=lambda g: abs(g['y'] - x['y']))
        if abs(v['y'] - x['y']) <= 10:
            v['gan'].append(x)
    # cột pha theo tiêu đề: chỉ dùng khi tên model thẳng cột dưới "3~"/"1~"
    pha = {}
    for w in band:
        if w[4] in ('1~', '3~') and xc(w) < lim and w[4] not in pha:
            pha[w[4]] = xc(w)
    if len(pha) == 2 and abs(pha['3~'] - pha['1~']) >= 25:
        ds = [min(abs(xc(t) - px) for px in pha.values()) for g in gia_tri for src in [g] + g['gan']
              for t in src['toks'] if la_ma(t[4]) and xc(t) < lim]
        if not ds or float(np.median(ds)) > min(30.0, 0.45 * abs(pha['3~'] - pha['1~'])):
            pha = {}
    else:
        pha = {}
    data = []
    for g in gia_tri:
        m3, m1, ma, dash3 = [], [], [], False
        kwv = None
        for src in [g] + sorted(g['gan'], key=lambda z: z['y']):
            dau = [t[4] for t in src['toks'] if t[4] in ('1~', '3~')]
            for t in src['toks']:
                cx = xc(t)
                if kw_x is not None and kwv is None and so(t[4]) is not None and abs(cx - kw_x) <= 14:
                    kwv = so(t[4])
                if cx >= lim:
                    continue
                if t[4] in DASH and pha and abs(cx - pha['3~']) < abs(cx - pha['1~']) and abs(cx - pha['3~']) <= 15:
                    dash3 = True
                if not la_ma(t[4]):
                    continue
                ma.append(t[4])
                if len(set(dau)) == 1:
                    (m3 if dau[0] == '3~' else m1).append(t[4])
                elif pha:
                    (m3 if abs(cx - pha['3~']) <= abs(cx - pha['1~']) else m1).append(t[4])
        if not ma:
            continue
        ten = (m3 or ma)[0]
        data.append({'y': g['y'], 'model': ten, 'm3': m3, 'm1': m1, 'ma': ma, 'thieu3': bool(m1 and not m3 and dash3),
                     'kw': kwv, 'h': g['cells']})
    return {'y': y_hdr, 'q': vals, 'qx': qx, 'unit': unit_w[4], 'kw_x': kw_x, 'pha': pha, 'rows': data}


def tim_bang_cot(words):
    # Bảng xoay (AQUARIS / ve_duong_cong): hàng "Model 3~" / "Model 1~" chứa tên model theo cột, hàng "kW",
    # hàng tiêu đề "Q (m³/h) … H (m)" rồi mỗi hàng: Q ở cột trái, H của từng model thẳng cột tên model.
    rows = hang_tu(words)
    kq = []
    for i, (y, r) in enumerate(rows):
        nhan = [w for w in r if re.match(r'^(MODEL|Model)$', w[4])]
        if not nhan:
            continue
        lim_x = nhan[0][2] + 80
        pha = next((w[4] for w in r if w[4] in ('1~', '3~') and w[0] < lim_x), None)
        toks = []
        for w in r:
            if w[0] < lim_x - 10:
                continue
            if toks and re.fullmatch(r'[A-Za-z]{1,6}', toks[-1][4]) and w[0] - toks[-1][2] < 6:
                toks[-1] = (toks[-1][0], toks[-1][1], w[2], w[3], toks[-1][4] + ' ' + w[4])
            else:
                toks.append(tuple(w[:5]))
        cot = [t for t in toks if la_ma(t[4]) or t[4] in DASH]
        if len([t for t in cot if la_ma(t[4])]) < 2 or pha is None:
            continue
        kq.append((y, pha, cot))
    if not kq:
        return []
    # gom các hàng Model 3~/1~ gần nhau thành một bảng
    bangs, nhom = [], []
    for y, pha, cot in kq:
        if nhom and y - nhom[-1][0] > 40:
            bangs.append(nhom)
            nhom = []
        nhom.append((y, pha, cot))
    bangs.append(nhom)
    ra = []
    for nhom in bangs:
        goc = max(nhom, key=lambda z: len(z[2]))
        cx = [xc(t) for t in goc[2]]
        if len(cx) < 2:
            continue
        tol = 0.45 * min(b - a for a, b in zip(cx, cx[1:]))
        ten = {'3~': [None] * len(cx), '1~': [None] * len(cx)}
        for y, pha, cot in nhom:
            for t in cot:
                k = int(np.argmin([abs(xc(t) - c) for c in cx]))
                if abs(xc(t) - cx[k]) <= tol:
                    ten[pha][k] = t[4]
        y_cuoi = nhom[-1][0]
        kw = [None] * len(cx)
        y_hdr = None
        x_q = None
        for y, r in rows:
            if y <= y_cuoi or y > y_cuoi + 140:
                continue
            nhan = ' '.join(w[4] for w in r if w[2] < cx[0] - tol)
            if re.search(r'\bkW\b', nhan) and kw == [None] * len(cx):
                for w in r:
                    v = so(w[4])
                    if v is not None and w[0] >= cx[0] - tol:
                        k = int(np.argmin([abs(xc(w) - c) for c in cx]))
                        if abs(xc(w) - cx[k]) <= tol:
                            kw[k] = v
            dv = [w for w in r if RE_DON_VI_Q.match(w[4]) and w[2] < cx[0] - tol]
            if dv and y_hdr is None:
                y_hdr, x_q = y, xc(dv[0])
        if y_hdr is None:
            continue
        qs, h = [], [dict() for _ in cx]
        last = y_hdr
        for y, r in rows:
            if y <= y_hdr + 2:
                continue
            if y - last > 30:
                break
            trai = [w for w in r if so(w[4]) is not None and w[2] < cx[0] - tol]
            if not trai:
                continue
            q = so(min(trai, key=lambda w: abs(xc(w) - x_q))[4])
            if qs and q <= qs[-1]:
                break
            qs.append(q)
            last = y
            for w in r:
                v = so(w[4])
                if w[0] < cx[0] - tol or (v is None and w[4] not in DASH):
                    continue
                k = int(np.argmin([abs(xc(w) - c) for c in cx]))
                if abs(xc(w) - cx[k]) <= tol:
                    h[k][len(qs) - 1] = v if v is not None else '–'
        if len(qs) < 2:
            continue
        data = []
        for k in range(len(cx)):
            m3, m1 = ten['3~'][k], ten['1~'][k]
            m3 = m3 if m3 and m3 not in DASH else None
            m1 = m1 if m1 and m1 not in DASH else None
            if not (m3 or m1) or not h[k]:
                continue
            data.append({'y': y_hdr, 'model': m3 or m1, 'm3': [m3] if m3 else [], 'm1': [m1] if m1 else [],
                         'ma': [x for x in (m3, m1) if x], 'thieu3': bool(m1 and not m3 and ten['3~'][k] in DASH),
                         'kw': kw[k], 'h': h[k]})
        if data:
            ra.append({'y': y_hdr, 'q': qs, 'qx': None, 'unit': 'm³/h', 'kw_x': (0 if any(kw) else None),
                       'pha': {}, 'rows': data, 'xoay': True})
    return ra


def khoa_day(model):
    m = re.sub(r'[/\-][^/\-]*$', '', model)
    return m if m != model else None


def ung_vien_3pha(m1):
    kq = {re.sub(r'^(\d*[A-Za-z]+?)M(?=\d)', r'\1', m1)}
    if re.search(r'M$', m1):
        kq |= {m1[:-1], m1[:-1] + 'T'}
    kq.discard(m1)
    return kq


def mot_pha_theo_ten(models):
    """Mã 1 pha nhận qua cặp tên: chèn 'M' sau nhóm chữ đầu của mã 3 pha (CDX70/05 → CDXM70/05)."""
    s = set(models)
    kq = {}
    for t in s:
        mm = re.sub(r'^(\d*[A-Za-z]+)', r'\1M', t)
        if mm != t and mm in s:
            kq[mm] = t
    return kq


def khop_hang(o, hang):
    s = str(o or '').strip().upper()
    if not s or s in ('*', 'CHUNG') or not hang:
        return True
    return hang.upper() in [x.strip() for x in s.split(',')]


def doc_du_lieu(path, hang=None):
    """Đọc điểm Q–H theo model. Dạng chính (giống tools/ve_duong_cong.py): sheet QH cột hang | model | q_m3h | h_m.
    Dạng phụ: bảng rộng (hàng tiêu đề "Model…" + các mức Q)."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    kq = {}
    if 'QH' in wb.sheetnames:
        rows = [list(r) for r in wb['QH'].iter_rows(values_only=True)]
        hdr = [str(c or '').strip().lower() for c in (rows[0] if rows else [])]
        if all(k in hdr for k in ('model', 'q_m3h', 'h_m')):
            im, iq, ih = hdr.index('model'), hdr.index('q_m3h'), hdr.index('h_m')
            ig = hdr.index('hang') if 'hang' in hdr else None
            for r in rows[1:]:
                if not r or (ig is not None and not khop_hang(r[ig], hang)):
                    continue
                q, h = r[iq], r[ih]
                if r[im] and isinstance(q, (int, float)) and isinstance(h, (int, float)):
                    kq.setdefault(str(r[im]).strip(), []).append((float(q), float(h)))
            return {k: sorted(v) for k, v in kq.items() if len(v) >= 2}
    for ws in wb.worksheets:
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        for i, r in enumerate(rows):
            nums = [(j, float(v)) for j, v in enumerate(r) if isinstance(v, (int, float)) and not isinstance(v, bool)]
            txt = [(j, str(v)) for j, v in enumerate(r) if isinstance(v, str) and 'model' in v.lower()]
            if len(nums) < 3 or not txt:
                continue
            qs = [v for j, v in nums]
            if any(b <= a for a, b in zip(qs, qs[1:])):
                continue
            col_m = next((j for j, t in txt if '3' in t), txt[0][0])
            for r2 in rows[i + 1:]:
                if not r2 or col_m >= len(r2) or not r2[col_m]:
                    continue
                pts = [(q, float(r2[j])) for j, q in nums
                       if j < len(r2) and isinstance(r2[j], (int, float)) and not isinstance(r2[j], bool)]
                if len(pts) >= 2:
                    kq[str(r2[col_m]).strip()] = pts
            if kq:
                return kq
    return kq


def lum(rgb):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def ti_le(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def ve_rgb(col):
    if col is None:
        return None
    if isinstance(col, (int, float)):
        col = (col,)
    col = tuple(col)
    if len(col) == 1:
        return (col[0],) * 3
    if len(col) == 4:
        c, m, y, k = col
        return ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
    return col[:3]


def hexc(rgb):
    return '#%02X%02X%02X' % tuple(int(round(max(0, min(1, v)) * 255)) for v in rgb)


# ----------------------------------------------------------------------------- KIỂM MỘT PDF
class KiemPDF:
    def __init__(self, path, cfg, args):
        self.path = Path(path)
        self.cfg = cfg
        self.C = cfg['chung']
        self.args = args
        self.hang, self.nhom = ten_hang_nhom(path)
        self.doc = pymupdf.open(str(path))
        self.cache = {}

    def trang(self, i):
        if i in self.cache:
            return self.cache[i]
        pg = self.doc[i]
        dr = pg.get_drawings()
        words = pg.get_text('words')
        ch = []
        for b in tim_bieu_do(dr, words):
            vat_can = [pymupdf.Rect(w[:4]) for w in words] + [d['rect'] for d in dr if d.get('fill') is not None
                                                              and d['rect'].width <= 16 and d['rect'].height <= 16]
            cong, dut = duong_cong_trong(dr, b, vat_can)
            if not cong:
                continue
            tr = chuan_truc(b, words)
            if not (tr['x'] or tr['y']):
                continue  # khung không có nhãn số trục → không phải biểu đồ (bảng/khung trang trí)
            c = {'box': b, 'cong': cong, 'dut': dut, 'truc': tr}
            danh_dau_phu(c, words)
            ch.append(c)
        self.cache[i] = {'pg': pg, 'dr': dr, 'words': words, 'charts': ch}
        return self.cache[i]

    def bang(self, i):
        t = self.trang(i)
        if 'bang' not in t:
            t['bang'] = tim_bang(t['words'], t['charts']) + tim_bang_cot(t['words'])
        return t['bang']

    # ---- mục 1: chữ cấm + 50 Hz
    def muc1(self):
        m = Muc(1)
        for i, pg in enumerate(self.doc):
            txt = re.sub(r'\s+', ' ', pg.get_text('text'))
            for term in self.C.get('chu_cam', []):
                pat = r'(?<![A-Za-z0-9])' + re.escape(term).replace(r'\ ', r'\s*') + r'(?![A-Za-z0-9])'
                for mt in re.finditer(pat, txt, re.I):
                    ng = f'…{txt[max(0, mt.start() - 30):mt.end() + 30]}…'
                    if re.match(r'kg\s*/\s*(d?m³|dm3|m3|l\b|cm)', txt[mt.start():mt.end() + 6], re.I):
                        m.canh_bao.append(f'tr.{i + 1}: "{term}" trong đơn vị khối lượng riêng (không phải cân nặng) — {ng}')
                    else:
                        m.loi.append(f'tr.{i + 1}: chữ cấm "{term}" — {ng}')
            ws = self.trang(i)['words']
            viet = sorted(set(w[4] for w in ws if RE_VIET.search(w[4])))
            if viet:
                m.loi.append(f'tr.{i + 1}: có chữ tiếng Việt (phương án 13/10 cấm): {", ".join(viet[:8])}')
            sao = [w for w in ws if w[4] == '*']
            if sao:
                m.loi.append(f'tr.{i + 1}: {len(sao)} ô/ký hiệu "*" đứng riêng (phương án 13/10 cấm ô "*")')
        dong_co = not (self.args.khong_dong_co or any(k in self.nhom.lower() for k in NHOM_KHONG_DONG_CO))
        if self.doc.page_count:
            t1 = re.sub(r'\s+', ' ', self.doc[0].get_text('text'))
            co = re.search(r'(?<!\d)50\s*Hz', t1, re.I)
            if not dong_co:
                m.ghi_chu.append('nhóm không có động cơ: không bắt buộc "50 Hz" trang 1')
            elif not co:
                m.loi.append('tr.1: thiếu "50 Hz" (sản phẩm có động cơ)')
            else:
                m.ghi_chu.append('tr.1 có "50 Hz"')
        m.ghi_chu.append('chữ cấm lấy từ HO_SO_HANG.json chung.chu_cam: ' + ', '.join(self.C.get('chu_cam', [])))
        return m

    # ---- mục 2: điện / pha
    def muc2(self):
        m = Muc(2)
        dien = self.C.get('dien', {}) or {}
        cho_phep = set()
        for s in dien.values():
            if isinstance(s, str):
                for a, b in re.findall(r'(\d{2,3})\s*[–-]\s*(\d{2,3})\s*V', s):
                    cho_phep.add((int(a), int(b)))
        kw_max = dien.get('mot_pha_kw_toi_da', MAC_DINH_MOT_PHA_KW)
        nguon_kw = 'HO_SO_HANG.json chung.dien.mot_pha_kw_toi_da (đề xuất, chưa anh duyệt)' if 'mot_pha_kw_toi_da' in dien else \
            'mặc định 3 kW theo phương án 13/10 (json chưa có khoá chung.dien.mot_pha_kw_toi_da)'
        pat = re.compile(r'(?<![\d.,])(\d{2,3})(?:\s*[–\-/]\s*(\d{2,3}))?\s*V(?![A-Za-z])')
        chuan = ' / '.join(f'{x}–{y} V' for x, y in sorted(cho_phep))
        for i, pg in enumerate(self.doc):
            txt = re.sub(r'\s+', ' ', pg.get_text('text'))
            for mt in pat.finditer(txt):
                a = int(mt.group(1))
                b = int(mt.group(2)) if mt.group(2) else None
                if b is not None and (a, b) in cho_phep:
                    continue
                if a < 100 and b is None:
                    continue
                m.loi.append(f'tr.{i + 1}: chuỗi điện áp "{mt.group(0).strip()}" khác chuẩn {chuan}')
        all_rows = [(i, r) for i in range(self.doc.page_count) for b in self.bang(i) for r in b['rows']]
        tat_ca = set(t for _, r in all_rows for t in r['ma'])
        cap = mot_pha_theo_ten(tat_ca)
        da_dem = set()
        for i, r in all_rows:
            mot = list(r['m1']) + [t for t in r['ma'] if t in cap and t not in r['m1']]
            for m1 in mot:
                da_dem.add(m1)
                if r['kw'] is not None and r['kw'] > kw_max + 1e-9:
                    m.loi.append(f'tr.{i + 1}: mã 1 pha {m1} = {r["kw"]:g} kW > {kw_max:g} kW')
                if r['thieu3']:
                    m.loi.append(f'tr.{i + 1}: mã 1 pha {m1} không có bản 3 pha (ô 3~ là "–")')
                elif not r['m3'] and not (set(ung_vien_3pha(m1)) & tat_ca):
                    m.canh_bao.append(f'tr.{i + 1}: mã 1 pha {m1}: không thấy mã 3 pha tương ứng trong bảng')
        m.ghi_chu.append(f'đã đọc {len(all_rows)} hàng model trong bảng, {len(da_dem)} mã 1 pha; ngưỡng 1 pha: {nguon_kw}')
        if not all_rows:
            m.kxm.append('không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha')
        return m

    # ---- mục 3: bảng số
    def khong_qh(self):
        if getattr(self.args, 'khong_qh', False):
            return '--khong-qh: thiết bị không có Q–H → không áp phép bảng/đường Q–H'
        if any(k in self.nhom.lower() for k in NHOM_KHONG_QH):
            return f'nhóm "{self.nhom}" là thiết bị không có Q–H (máy thổi khí/máy khuấy/định lượng/đĩa) → không áp phép Q–H'
        return None

    def muc3(self):
        m = Muc(3)
        if self.khong_qh():
            m.ep = BO
            m.ghi_chu.append(self.khong_qh())
            return m
        n_bang = 0
        for i in range(self.doc.page_count):
            bangs = self.bang(i)
            t = self.trang(i)
            for b in bangs:
                n_bang += 1
                for r in b['rows']:
                    seq = [(k, r['h'][k]) for k in sorted(r['h'])]
                    idx = [j for j, (k, v) in enumerate(seq) if v != '–']
                    if idx and any(v == '–' for k, v in seq[idx[0]:idx[-1] + 1]):
                        m.loi.append(f'tr.{i + 1}: {r["model"]}: ô "–" nằm giữa dãy H')
                    vals = [(k, v) for k, v in seq if v != '–']
                    for (k1, v1), (k2, v2) in zip(vals, vals[1:]):
                        if v2 > v1 + 1e-9:
                            m.loi.append(f'tr.{i + 1}: {r["model"]}: H tăng khi Q tăng '
                                         f'(Q {b["q"][k1]:g}→{b["q"][k2]:g}: H {v1:g}→{v2:g})')
                        elif abs(v2 - v1) < 1e-9:
                            m.canh_bao.append(f'tr.{i + 1}: {r["model"]}: H bằng nhau ở Q {b["q"][k1]:g} và {b["q"][k2]:g}')
                nhom = {}
                for r in b['rows']:
                    k = khoa_day(r['model'])
                    if k and r['kw'] is not None:
                        nhom.setdefault(k, []).append(r)
                for k, rs in nhom.items():
                    rs = sorted(rs, key=lambda r: r['kw'])
                    for a, c in zip(rs, rs[1:]):
                        if c['kw'] <= a['kw']:
                            continue
                        for q in sorted(set(a['h']) & set(c['h'])):
                            va, vc = a['h'][q], c['h'][q]
                            if va != '–' and vc != '–' and vc < va - 1e-9:
                                m.loi.append(f'tr.{i + 1}: dải {k}: {c["model"]} ({c["kw"]:g} kW) có H {vc:g} < '
                                             f'{a["model"]} ({a["kw"]:g} kW) H {va:g} tại Q {b["q"][q]:g}')
                if b['kw_x'] is None:
                    m.canh_bao.append(f'tr.{i + 1}: bảng y={b["y"]:.0f} không thấy cột kW → không kiểm thứ tự công suất')
            qh = [c for c in t['charts'] if nhan_dang_qh(c['box'], t['words'])]
            if bangs and qh and len(bangs) != len(qh):
                m.ghi_chu.append(f'tr.{i + 1}: {len(bangs)} bảng / {len(qh)} biểu đồ Q–H → không so số model với số đường')
            elif bangs and qh:
                # dòng 1 pha trùng số với dòng 3 pha (cùng một đường) chỉ tính một model
                n_model = sum(len({tuple(sorted((k2, v) for k2, v in r['h'].items())) for r in b['rows']}) for b in bangs)
                n_duong = sum(len(c['chinh']) for c in qh)
                n_nhan = self.dem_nhan(t, qh, [r['model'] for b in bangs for r in b['rows']])
                if n_duong != n_model:
                    m.loi.append(f'tr.{i + 1}: bảng có {n_model} model nhưng biểu đồ có {n_duong} đường')
                if n_nhan and n_nhan != n_model:
                    m.canh_bao.append(f'tr.{i + 1}: bảng có {n_model} model nhưng biểu đồ có {n_nhan} nhãn')
                m.ghi_chu.append(f'tr.{i + 1}: {n_model} model / {n_duong} đường / {n_nhan or "?"} nhãn')
        self.kiem_wc_qd19(m)
        if n_bang == 0:
            m.kxm.append('không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng')
        else:
            m.ghi_chu.insert(0, f'đã đọc {n_bang} bảng Q–H')
        return m

    def kiem_wc_qd19(self, m):
        # QĐ 19 (rules/QUYET_DINH_ANH.md, QTH 4.9): bơm cắt rác WC, trong cùng cỡ họng, H tại Qmax của model công suất
        # bé nhất = 1 m, mỗi nấc công suất lớn hơn +1 m (2, 3, 4, …). Chỉ áp cho mã có dạng <cỡ họng>WC…
        nhom = {}
        for i in range(self.doc.page_count):
            for b in self.bang(i):
                for r in b['rows']:
                    mt = re.match(r'^(\d+)WC', r['model'].replace(' ', ''))
                    if not mt:
                        continue
                    v = [x for kk, x in sorted(r['h'].items()) if x != '–']
                    kw = r['kw']
                    if kw is None:
                        mk = re.search(r'-([\d.]+)$', r['model'])
                        kw = float(mk.group(1)) if mk else None
                    nhom.setdefault(mt.group(1), {})[r['model']] = (i, kw, v[-1] if v else None)
        if not nhom:
            return
        dung = sai = 0
        for co, ds in sorted(nhom.items(), key=lambda kv: int(kv[0])):
            khong_kw = [t for t, (i, kw, h) in ds.items() if kw is None]
            for t in khong_kw:
                m.kxm.append(f'WC cỡ {co}: {t} không đọc được công suất → chưa kiểm QĐ 19')
            nac = sorted(set(kw for i, kw, h in ds.values() if kw is not None))
            for t, (i, kw, h) in ds.items():
                if kw is None:
                    continue
                can = nac.index(kw) + 1
                if h is None or abs(h - can) > 1e-9:
                    sai += 1
                    m.loi.append(f'tr.{i + 1}: QĐ 19 WC cỡ {co}: {t} ({kw:g} kW, nấc {can}) có H tại Qmax = '
                                 f'{h if h is None else format(h, "g")} m, phải = {can} m')
                else:
                    dung += 1
        m.ghi_chu.append(f'QĐ 19 (WC, H tại Qmax theo nấc công suất trong cùng cỡ họng): {dung} mã đúng, {sai} mã sai, '
                         f'{len(nhom)} cỡ họng')

    def dem_nhan(self, t, charts, models):
        n = 0
        mk = [d for d in t['dr'] if d.get('fill') is not None and 5 <= d['rect'].width <= 16 and d['rect'].height <= 16]
        norm = set(x.replace(' ', '') for x in models)
        for c in charts:
            b = c['box']
            vung = pymupdf.Rect(b.x0 - 60, b.y0 - 10, b.x1 + 60, b.y1 + 10)
            ws = [w for w in t['words'] if vung.contains(pymupdf.Point(xc(w), yc(w)))]
            so_tron = set(w[4] for w in ws if re.fullmatch(r'\d{1,2}', w[4]) and b.contains(pymupdf.Point(xc(w), yc(w))) and
                          any(d['rect'].contains(pymupdf.Point(xc(w), yc(w))) for d in mk))
            ten = set(w[4] for w in ws if w[4].replace(' ', '') in norm)
            ws2 = sorted(ws, key=lambda w: (round(yc(w)), w[0]))
            for u, v in zip(ws2, ws2[1:]):
                if abs(yc(u) - yc(v)) < 2 and 0 <= v[0] - u[2] < 6 and (u[4] + v[4]) in norm:
                    ten.add(u[4] + ' ' + v[4])
            n += max(len(so_tron), len(ten))
        return n

    # ---- mục 4: đường cong
    def muc4(self):
        m = Muc(4)
        nmax = self.C.get('so_duong_toi_da_moi_bieu_do', 8)
        net_min = self.C.get('net_duong_pt_min')
        n_chart, cong_qh, du_lieu = 0, [], None
        if self.args.du_lieu:
            try:
                du_lieu = doc_du_lieu(self.args.du_lieu, self.hang)
                if not du_lieu:
                    m.kxm.append('tệp số liệu không đúng dạng bảng chuẩn (Model + các mức Q) → chưa so được đường với bảng')
            except Exception as e:  # noqa
                m.kxm.append(f'không đọc được tệp số liệu {self.args.du_lieu}: {e}')
        if self.khong_qh():
            m.ep = BO
            m.ghi_chu.append(self.khong_qh())
            return m
        n_qh = 0
        for i in range(self.doc.page_count):
            t = self.trang(i)
            for c in t['charts']:
                n_chart += 1
                b = c['box']
                qh = nhan_dang_qh(b, t['words'])
                ten = f'tr.{i + 1} biểu đồ ({b.x0:.0f},{b.y0:.0f})–({b.x1:.0f},{b.y1:.0f})'
                if not qh:
                    m.loi += [f'{ten}: {e}' for e in noi_dau_duong(c['cong'], c['truc'], b, False)]
                    m.ghi_chu.append(f'{ten}: trục không phải Q (m³/h) – H (m) → không áp ≤{nmax} đường và các phép Q–H '
                                     f'({len(c["cong"])} đường)')
                    continue
                n_qh += 1
                if len(c['chinh']) > nmax:
                    m.loi.append(f'{ten}: {len(c["chinh"])} đường > {nmax} (HO_SO_HANG.json)')
                mong = [cc['width'] for cc in c['chinh'] if net_min and cc['width'] < net_min - 1e-6]
                if mong:
                    m.canh_bao.append(f'{ten}: {len(mong)} đường nét {min(mong):.2f} pt < {net_min} pt')
                tr = c['truc']
                phu = [cc for cc in c['cong'] if cc['phu']]
                if phu:
                    m.ghi_chu.append(f'{ten}: {len(phu)} đường phụ không đếm/không kiểm đơn điệu ({phu[0]["phu"]})')
                for k, cc in enumerate(c['chinh']):
                    loi, cb = phan_tich_duong(cc, b)
                    if cc.get('vuot', 0) > 3:
                        loi.append(f'đường vượt ra ngoài khung biểu đồ {cc["vuot"]:.0f} pt')
                    vt = f'đường {k + 1} ({cc["rect"].x0:.0f},{cc["rect"].y0:.0f})'
                    if tr['x'] and tr['y']:
                        P0 = cc['P'][0] if cc['P'][0][0] <= cc['P'][-1][0] else cc['P'][-1]
                        vt += f' [đầu đường Q≈{tr["x"][0] * P0[0] + tr["x"][1]:.3g}, H≈{tr["y"][0] * P0[1] + tr["y"][1]:.3g}]'
                    m.loi += [f'{ten} {vt}: {e}' for e in loi]
                    m.canh_bao += [f'{ten} {vt}: {e}' for e in cb]
                m.loi += [f'{ten}: {e}' for e in noi_dau_duong(c['chinh'], tr, b, qh)]
                n_dut = sum(1 for cc in c['chinh'] if cc['dut'])
                if n_dut:
                    m.ghi_chu.append(f'{ten}: trong đó {n_dut} đường nét đứt')
                m.ghi_chu.append(f'{ten}: {len(c["chinh"])} đường Q–H, quy đổi trục '
                                 f'{"được (Q " + str(tr.get("x_don_vi")) + ")" if tr["x"] and tr["y"] else "KHÔNG"}')
                cong_qh.append((i, b, c, tr))
        if n_chart == 0:
            m.kxm.append('không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường')
        elif n_qh == 0:
            m.kxm.append('có biểu đồ nhưng không biểu đồ nào có trục Q (m³/h) – H (m) → chưa kiểm phép Q–H')
        if du_lieu:
            self.so_du_lieu(m, du_lieu, cong_qh)
        return m

    def so_du_lieu(self, m, du_lieu, cong_qh):
        dung = [(i, c, tr) for i, b, c, tr in cong_qh if tr['x'] and tr['y'] and tr.get('x_don_vi') == 'm³/h']
        if not dung:
            m.kxm.append('không quy đổi được trục (thiếu nhãn số trục Q m³/h hoặc H) → chưa so được đường với bảng ≤5%')
            return
        ds = []
        for i, c, tr in dung:
            for cc in c['cong']:
                Q = tr['x'][0] * cc['P'][:, 0] + tr['x'][1]
                H = tr['y'][0] * cc['P'][:, 1] + tr['y'][1]
                o = np.argsort(Q)
                ds.append((i, Q[o], H[o]))
        lech_max = []
        for ten, pts in du_lieu.items():
            best = None
            for i, Q, H in ds:
                dq = 0.01 * (Q[-1] - Q[0]) + 1e-6
                trong = [(q, h) for q, h in pts if Q[0] - dq <= q <= Q[-1] + dq and h > 0]
                if len(trong) < 2:
                    continue
                lech = [abs(np.interp(q, Q, H) - h) / h for q, h in trong]
                sc = float(np.mean(lech))
                if best is None or sc < best[0]:
                    best = (sc, max(lech), i, len(trong), len(pts), Q[0], Q[-1])
            if best is None:
                m.loi.append(f'{ten}: không có đường nào phủ ≥2 điểm Q của tệp số liệu')
                continue
            sc, mx, i, n_in, n_all, qa, qb = best
            lech_max.append((mx, ten))
            if mx > 0.05:
                m.loi.append(f'{ten}: đường gần nhất (tr.{i + 1}) lệch tối đa {mx * 100:.1f}% > 5%')
            if n_in < n_all:
                m.canh_bao.append(f'{ten}: đường tr.{i + 1} chỉ phủ {n_in}/{n_all} điểm Q (Q {qa:.3g}–{qb:.3g})')
        lm = max(lech_max) if lech_max else None
        m.ghi_chu.append(f'so {len(du_lieu)} model của tệp số liệu với {len(ds)} đường (ghép theo đường gần nhất)'
                         + (f'; lệch lớn nhất {lm[0] * 100:.1f}% ({lm[1]})' if lm else ''))

    # ---- mục 5: chữ chồng + cỡ chữ
    def muc5(self):
        m = Muc(5)
        cs = self.C.get('co_chu_pt', {})
        bang_min, than_min = cs.get('bang_min', 7), cs.get('than_min', 9)
        nhan = ['<6', f'6–<{bang_min:g}', f'{bang_min:g}–<{than_min:g}', f'≥{than_min:g}']
        dem = dict.fromkeys(nhan, 0)
        nho_trang, than_nho, min_size = {}, {}, 99.0
        for i, pg in enumerate(self.doc):
            hop = []
            bl = pg.get_bboxlog()
            o_to = [(j, pymupdf.Rect(r)) for j, (tp, r) in enumerate(bl) if tp in ('fill-path', 'fill-image')]
            for s in pg.get_texttrace():
                if s.get('type', 0) == 3 or s.get('opacity', 1) <= 0:
                    continue
                n = sum(1 for ch in s['chars'] if chr(ch[0]).strip() and chr(ch[0]) not in KY_TU_CHI_SO)
                sz = s['size']
                if not n or sz < 1:
                    continue
                min_size = min(min_size, sz)
                dem[nhan[0 if sz < 6 else 1 if sz < bang_min else 2 if sz < than_min else 3]] += n
                if sz < bang_min - 1e-6:
                    v = nho_trang.setdefault(i + 1, [0, 99.0])
                    v[0] += n
                    v[1] = min(v[1], sz)
                x0, y0, x1, y1 = s['bbox']
                h = y1 - y0
                hop.append((x0, y0 + 0.18 * h, x1, y1 - 0.18 * h, s))
            for bl in pg.get_text('dict')['blocks']:
                for ln in bl.get('lines', []):
                    tx = ''.join(sp['text'] for sp in ln['spans'])
                    if len(tx.split()) < 6 or ln['bbox'][2] - ln['bbox'][0] < 100:
                        continue
                    if sum(ch.isalpha() for ch in tx) / max(1, len(tx.replace(' ', ''))) < 0.7:
                        continue
                    sz = max(sp['size'] for sp in ln['spans'])
                    if sz < than_min - 1e-6:
                        than_nho.setdefault(i + 1, []).append((sz, tx[:40]))
            grid = {}
            for k, b in enumerate(hop):
                for gx in range(int(b[0] // 40), int(b[2] // 40) + 1):
                    for gy in range(int(b[1] // 40), int(b[3] // 40) + 1):
                        grid.setdefault((gx, gy), []).append(k)
            seen = set()
            for ks in grid.values():
                for a in range(len(ks)):
                    for c in range(a + 1, len(ks)):
                        p, q = ks[a], ks[c]
                        if (p, q) in seen:
                            continue
                        seen.add((p, q))
                        A, B = hop[p], hop[q]
                        if min(A[2], B[2]) - max(A[0], B[0]) <= 0.8 or min(A[3], B[3]) - max(A[1], B[1]) <= 0.8:
                            continue
                        ov = self.chong_ky_tu(A[4], B[4])
                        if not ov:
                            continue
                        ta = ''.join(chr(c[0]) for c in A[4]['chars']).strip()
                        tb = ''.join(chr(c[0]) for c in B[4]['chars']).strip()
                        duoi, tren = (A, B) if A[4].get('seqno', 0) < B[4].get('seqno', 0) else (B, A)
                        rd = pymupdf.Rect(duoi[4]['bbox'])
                        bi_che = any(duoi[4].get('seqno', 0) < j < tren[4].get('seqno', 0) and
                                     (r & rd).get_area() >= 0.6 * max(rd.get_area(), 1e-6) for j, r in o_to)
                        if bi_che:
                            tx = ''.join(chr(c[0]) for c in duoi[4]['chars']).strip()
                            m.canh_bao.append(f'tr.{i + 1}: chữ cũ bị ô/ảnh che nhưng vẫn còn trong PDF (tìm/chép được): '
                                              f'"{tx[:30]}" tại ({rd.x0:.0f},{rd.y0:.0f})')
                        elif ta == tb and abs(A[0] - B[0]) < 1 and abs(A[1] - B[1]) < 1:
                            m.canh_bao.append(f'tr.{i + 1}: chữ "{ta[:25]}" in 2 lần khít nhau tại ({A[0]:.0f},{A[1]:.0f})')
                        else:
                            m.loi.append(f'tr.{i + 1}: chữ chồng nhau tại ({max(A[0], B[0]):.0f},{max(A[1], B[1]):.0f}): '
                                         f'"{ta[:25]}" ⟂ "{tb[:25]}" (đè {ov:.0%} ký tự)')
        for p, (n, mn) in sorted(nho_trang.items()):
            m.loi.append(f'tr.{p}: {n} ký tự cỡ < {bang_min:g} pt (nhỏ nhất {mn:.1f} pt)')
        for p, ls in sorted(than_nho.items()):
            m.loi.append(f'tr.{p}: {len(ls)} dòng chữ thân < {than_min:g} pt (vd {ls[0][0]:.1f} pt "{ls[0][1]}…")')
        m.ghi_chu.append('số ký tự theo cỡ: ' + ', '.join(f'{k} pt: {v}' for k, v in dem.items())
                         + (f'; nhỏ nhất {min_size:.1f} pt' if min_size < 99 else ''))
        m.ghi_chu.append(f'ngưỡng HO_SO_HANG.json: bảng/nhãn ≥{bang_min:g} pt, thân ≥{than_min:g} pt; chữ thân nhận '
                         'theo dòng ≥6 từ, ≥70% chữ cái, rộng ≥100 pt')
        return m

    @staticmethod
    def chong_ky_tu(a, b):
        ba = [c[3] for c in a['chars'] if chr(c[0]).strip()]
        bb = [c[3] for c in b['chars'] if chr(c[0]).strip()]
        best = 0.0
        for x0, y0, x1, y1 in ba:
            h = y1 - y0
            y0, y1 = y0 + 0.18 * h, y1 - 0.18 * h
            for u0, v0, u1, v1 in bb:
                k = v1 - v0
                v0, v1 = v0 + 0.18 * k, v1 - 0.18 * k
                iw, ih = min(x1, u1) - max(x0, u0), min(y1, v1) - max(y0, v0)
                if iw > 0 and ih > 0:
                    ar = min((x1 - x0) * (y1 - y0), (u1 - u0) * (v1 - v0))
                    if ar > 0:
                        best = max(best, iw * ih / ar)
        return best if best >= 0.25 else 0

    # ---- mục 6: ảnh
    def muc6(self):
        m = Muc(6)
        a = self.C.get('anh', {})
        ppi_min, ppi_bia = a.get('ppi_min', 200), a.get('ppi_bia_min', 300)
        n = 0
        for i, pg in enumerate(self.doc):
            W, Hh = pg.rect.width, pg.rect.height
            infos = pg.get_image_info(hashes=True, xrefs=True)
            for im in infos:
                n += 1
                tr = im['transform']
                dw, dh = math.hypot(tr[0], tr[1]), math.hypot(tr[2], tr[3])
                if dw < 1 or dh < 1:
                    continue
                ppi = min(im['width'] / (dw / 72), im['height'] / (dh / 72))
                ng = ppi_bia if i == 0 else ppi_min
                bb = im['bbox']
                if ppi < ng - 0.5:
                    m.loi.append(f'tr.{i + 1}: ảnh {im["width"]}×{im["height"]} px đặt {dw:.0f}×{dh:.0f} pt tại '
                                 f'({bb[0]:.0f},{bb[1]:.0f}) = {ppi:.0f} ppi < {ng}' + (' (trang bìa)' if i == 0 else ''))
                if bb[0] < -1 or bb[1] < -1 or bb[2] > W + 1 or bb[3] > Hh + 1:
                    rb = pymupdf.Rect(bb)
                    ngoai = 1 - (rb & pg.rect).get_area() / max(rb.get_area(), 1e-6)
                    ca_trang = dw >= 0.9 * W and dh >= 0.9 * Hh
                    m.loi.append(f'tr.{i + 1}: ảnh ({bb[0]:.0f},{bb[1]:.0f},{bb[2]:.0f},{bb[3]:.0f}) tràn ra ngoài trang '
                                 f'{W:.0f}×{Hh:.0f}, {ngoai:.0%} diện tích ảnh nằm ngoài'
                                 + (' — ảnh cỡ cả trang đặt lệch (nghi ảnh dán chồng lên trang)' if ca_trang else ''))
            for p in range(len(infos)):
                for q in range(p + 1, len(infos)):
                    A, B = infos[p], infos[q]
                    if A['digest'] != B['digest'] and A['xref'] != B['xref']:
                        continue
                    ra, rb = pymupdf.Rect(A['bbox']), pymupdf.Rect(B['bbox'])
                    inter = ra & rb
                    iou = 0.0 if inter.is_empty else inter.get_area() / max(1e-6, (ra | rb).get_area())
                    if iou > 0.9:
                        m.loi.append(f'tr.{i + 1}: cùng một ảnh đặt chồng 2 lần cùng chỗ ({ra.x0:.0f},{ra.y0:.0f},{ra.x1:.0f},{ra.y1:.0f})')
                    elif i == 0:
                        m.canh_bao.append(f'tr.1: 1 ảnh nhiều cỡ/vị trí: ({ra.x0:.0f},{ra.y0:.0f}) {ra.width:.0f}×{ra.height:.0f} pt '
                                          f'và ({rb.x0:.0f},{rb.y0:.0f}) {rb.width:.0f}×{rb.height:.0f} pt')
        m.ghi_chu.append(f'{n} lượt đặt ảnh; ngưỡng ppi HO_SO_HANG.json: trang 1 = {ppi_bia}, trang khác = {ppi_min}')
        return m

    # ---- mục 7: tương phản
    def muc7(self):
        m = Muc(7)
        tp = self.C.get('tuong_phan', {})
        t_chu, t_lon = tp.get('chu', 4.5), tp.get('chu_lon_va_net', 3.0)
        gom, nen_anh, n_span = {}, 0, 0
        for i, pg in enumerate(self.doc):
            bl = pg.get_bboxlog()
            if not bl:
                continue
            types = np.array([t for t, r in bl])
            R = np.array([r for t, r in bl], dtype=float)
            idx = np.arange(len(bl))
            fill = {d.get('seqno'): d.get('fill') for d in self.trang(i)['dr'] if d.get('fill') is not None}
            ok = np.isin(types, ['fill-path', 'fill-image', 'fill-imgmask', 'fill-shade'])
            for s in pg.get_texttrace():
                if s.get('type', 0) == 3 or s.get('opacity', 1) <= 0 or not any(chr(c[0]).strip() for c in s['chars']):
                    continue
                n_span += 1
                x0, y0, x1, y1 = s['bbox']
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                mask = ok & (idx < s.get('seqno', len(bl))) & (R[:, 0] <= cx) & (R[:, 2] >= cx) & (R[:, 1] <= cy) & (R[:, 3] >= cy)
                nen, nguon = (1.0, 1.0, 1.0), 'nền trắng (không có ô nền)'
                if mask.any():
                    j = int(np.nonzero(mask)[0].max())
                    if types[j] != 'fill-path' or fill.get(j) is None:
                        nen_anh += 1
                        continue
                    nen, nguon = ve_rgb(fill[j]), 'ô nền'
                c = ve_rgb(s.get('color')) or (0, 0, 0)
                op = s.get('opacity', 1)
                if op < 1:
                    c = tuple(op * a + (1 - op) * b for a, b in zip(c, nen))
                bold = bool(re.search(r'bold|black|heavy', s.get('font', ''), re.I)) or bool(s.get('flags', 0) & 16)
                ng = t_lon if (s['size'] >= 18 or (bold and s['size'] >= 14)) else t_chu
                r = ti_le(c, nen)
                if r < ng - 1e-6:
                    g = gom.setdefault((hexc(c), hexc(nen), round(r, 2), ng),
                                       {'n': 0, 'trang': set(), 'vd': ''.join(chr(ch[0]) for ch in s['chars'])[:30], 'nguon': nguon})
                    g['n'] += 1
                    g['trang'].add(i + 1)
        for (cc, nn, r, ng), g in sorted(gom.items(), key=lambda kv: -kv[1]['n']):
            tr = sorted(g['trang'])
            m.loi.append(f'chữ {cc} trên {nn} ({g["nguon"]}): tỉ lệ {r:.2f} < {ng} — {g["n"]} cụm chữ, tr.'
                         f'{",".join(map(str, tr[:8]))}{"…" if len(tr) > 8 else ""} (vd "{g["vd"].strip()}")')
        if nen_anh:
            m.canh_bao.append(f'{nen_anh} cụm chữ nằm trên ảnh/nền chuyển màu → không đo được tương phản')
        m.ghi_chu.append(f'đã đo {n_span} cụm chữ (công thức WCAG; ngưỡng {t_chu} / chữ lớn {t_lon} theo HO_SO_HANG.json)')
        return m

    # ---- mục 8: tệp
    def muc8(self):
        m = Muc(8)
        C = self.C
        kd, kn = C.get('kho_A4_doc', [595, 842]), C.get('kho_A4_ngang', [842, 595])
        sai, huong = [], set()
        for i, pg in enumerate(self.doc):
            w, h = pg.rect.width, pg.rect.height
            if abs(w - kd[0]) <= DUNG_SAI_KHO_PT and abs(h - kd[1]) <= DUNG_SAI_KHO_PT:
                huong.add('A4_doc')
            elif abs(w - kn[0]) <= DUNG_SAI_KHO_PT and abs(h - kn[1]) <= DUNG_SAI_KHO_PT:
                huong.add('A4_ngang')
            else:
                sai.append(f'tr.{i + 1} {w:.1f}×{h:.1f} pt ({w / 72 * 25.4:.0f}×{h / 72 * 25.4:.0f} mm)')
        if sai:
            m.loi.append(f'{len(sai)} trang không phải A4 (±{DUNG_SAI_KHO_PT:g} pt): ' + '; '.join(sai[:6]))
        if len(huong) > 1:
            m.canh_bao.append('PDF lẫn trang dọc và ngang')
        k = self.cfg.get('hang', {}).get(self.hang or '', {}).get('kho')
        if k and huong and huong != {k}:
            m.canh_bao.append(f'hướng khổ {"/".join(sorted(huong))} khác hồ sơ hãng {self.hang} ({k}) — chuẩn cho bản mới')
        mb = self.path.stat().st_size / 1e6
        dl = C.get('dung_luong_mb', {})
        if mb > dl.get('toi_da', 10):
            m.loi.append(f'dung lượng {mb:.1f} MB > tối đa {dl.get("toi_da")} MB')
        elif mb > dl.get('muc_tieu', 5):
            m.canh_bao.append(f'dung lượng {mb:.1f} MB > mục tiêu {dl.get("muc_tieu")} MB')
        m.ghi_chu.append(f'dung lượng {mb:.2f} MB; khổ {"/".join(sorted(huong)) or "?"}')
        fonts = {}
        for p in range(self.doc.page_count):
            for f in self.doc.get_page_fonts(p):
                fonts[f[0]] = f
        dem, khong_nhung, ho = {}, set(), set()
        for f in fonts.values():
            base = f[3].split('+')[-1]
            if f[1] in ('n/a', ''):
                khong_nhung.add(base)
            else:
                dem[base] = dem.get(base, 0) + 1
            fam = re.sub(r'[-,_ ]?(Bold|Italic|Regular|Light|Medium|Semi[Bb]old|Black|Heavy|Oblique|Thin|Book|Roman|'
                         r'Condensed|Narrow|MT|PS)+.*$', '', base)
            ho.add(fam.replace(' ', '').lower())
        lap = {b: n for b, n in dem.items() if n > 1}
        if lap:
            m.loi.append('phông nhúng lặp: ' + ', '.join(f'{b} ×{n}' for b, n in sorted(lap.items())))
        if khong_nhung:
            m.canh_bao.append('phông không nhúng: ' + ', '.join(sorted(khong_nhung)))
        if len(ho) > MAC_DINH_SO_PHONG_TOI_DA:
            m.canh_bao.append(f'{len(ho)} họ phông ({", ".join(sorted(ho))}) > {MAC_DINH_SO_PHONG_TOI_DA} (phương án 13/10)')
        mong = set(x.replace(' ', '').lower() for x in self.cfg.get('hang', {}).get(self.hang or '', {}).get('phong', []))
        la = sorted(h for h in ho if h and h not in mong)
        if mong and la:
            m.canh_bao.append(f'họ phông khác hồ sơ hãng ({", ".join(sorted(mong))}): {", ".join(la)}')
        cmyk = set()
        for p in range(self.doc.page_count):
            for im in self.doc.get_page_images(p, full=True):
                if im[0] not in cmyk and self.la_cmyk(im[0], im[5], im[6]):
                    cmyk.add(im[0])
                    m.loi.append(f'tr.{p + 1}: ảnh xref {im[0]} ({im[2]}×{im[3]} px) hệ màu CMYK')
        if not self.args.nhanh:
            tl = C.get('khoang_trong_lien_toi_da', 0.10)
            for i, pg in enumerate(self.doc):
                pm = pg.get_pixmap(dpi=50, colorspace=pymupdf.csGRAY, alpha=False)
                a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.stride)[:, :pm.width].astype(np.int16)
                gx = (np.abs(np.diff(a, axis=1)) > 24).sum(1)
                gy = np.r_[0, np.abs(np.diff(a, axis=0)).mean(1)]
                trong = (gx <= max(2, 0.004 * pm.width)) & (gy < 6)
                best = cur = st = bst = 0
                for r, v in enumerate(trong):
                    if v:
                        st = r if cur == 0 else st
                        cur += 1
                        if cur > best:
                            best, bst = cur, st
                    else:
                        cur = 0
                if best > tl * pm.height:
                    y0 = bst / pm.height * pg.rect.height
                    y1 = (bst + best) / pm.height * pg.rect.height
                    m.loi.append(f'tr.{i + 1}: vùng trống liền {best / pm.height:.1%} chiều cao trang (y {y0:.0f}–{y1:.0f} pt) > {tl:.0%}')
        else:
            m.ghi_chu.append('--nhanh: bỏ đo vùng trống')
        return m

    def la_cmyk(self, xref, cs, alt):
        if 'CMYK' in (cs or '') or 'CMYK' in (alt or ''):
            return True
        try:
            t, v = self.doc.xref_get_key(xref, 'ColorSpace')
            mt = re.search(r'/ICCBased\s+(\d+)\s+0\s+R', v or '')
            if mt:
                return self.doc.xref_get_key(int(mt.group(1)), 'N')[1].strip() == '4'
            if t == 'xref':
                v2 = self.doc.xref_object(int(v.split()[0]))
                mt = re.search(r'/ICCBased\s+(\d+)\s+0\s+R', v2)
                if mt:
                    return self.doc.xref_get_key(int(mt.group(1)), 'N')[1].strip() == '4'
                return 'DeviceCMYK' in v2
            return 'DeviceCMYK' in (v or '')
        except Exception:  # noqa
            return False

    # ---- mục 10: mã kiểm
    def muc10(self):
        m = Muc(10)
        sha = sha256_tep(self.path)
        m.ghi_chu.append(f'sha256 {sha}')
        goc = self.path.resolve().parent.parent
        ds_tep = goc / 'DANH SACH.txt'
        trong = goc.name == THU_MUC_DA_DUYET.name and self.path.resolve().parent.name in HANG
        if not trong:
            m.ep = BO
            m.ghi_chu.append('tệp không nằm trong CATALOG SUA/CATALOGUE DA DUYET/<HÃNG> → không đối chiếu DANH SACH')
            return m
        if not ds_tep.exists():
            m.kxm.append('không thấy DANH SACH.txt')
            return m
        dong = [ln for ln in ds_tep.read_text(encoding='utf-8-sig').splitlines()
                if re.match(r'^\s*-\s*' + re.escape(self.path.name) + r'\s*\|', ln)]
        mk = [x.group(1).lower() for x in (re.search(r'mã kiểm\s+([0-9a-fA-F]{6,64})', ln) for ln in dong) if x]
        if not mk:
            m.loi.append('DANH SACH.txt không có dòng (mã kiểm) cho tệp này')
        elif sha.startswith(mk[-1]):
            m.ghi_chu.append(f'khớp dòng cuối DANH SACH (mã kiểm {mk[-1]})')
            if len(dong) > 1:
                m.canh_bao.append(f'DANH SACH có {len(dong)} dòng cùng tên tệp (mã: {", ".join(dict.fromkeys(mk))})')
        elif any(sha.startswith(x) for x in mk):
            m.loi.append(f'chỉ khớp một dòng cũ; dòng cuối ghi {mk[-1]} ≠ {sha[:12]}')
        else:
            m.loi.append(f'không khớp: DANH SACH ghi {", ".join(dict.fromkeys(mk))} ≠ sha {sha[:12]}')
        return m

    def chay(self, muc_set):
        kq = {}
        for k in range(1, 11):
            if k == 9:
                continue
            if k not in muc_set:
                mm = Muc(k)
                mm.ep = BO
                mm.ghi_chu.append('không chạy (--muc)')
                kq[k] = mm
                continue
            try:
                kq[k] = getattr(self, f'muc{k}')()
            except Exception as e:  # noqa
                mm = Muc(k)
                mm.kxm.append(f'lỗi khi đo: {type(e).__name__}: {e}')
                kq[k] = mm
        return kq

    def trang_bieu_do_dau(self):
        for i in range(self.doc.page_count):
            t = self.trang(i)
            if any(nhan_dang_qh(c['box'], t['words']) for c in t['charts']):
                return i
        for i in range(self.doc.page_count):
            if self.trang(i)['charts']:
                return i
        return None


# ----------------------------------------------------------------------------- mục 9 (bộ 3 hãng)
def anh_xam(doc, i, n=256, clip=None, m=None):
    import cv2
    pm = doc[i].get_pixmap(dpi=72, colorspace=pymupdf.csGRAY, alpha=False, clip=clip)
    a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.stride)[:, :pm.width]
    return cv2.resize(a, (n, m or n), interpolation=cv2.INTER_AREA).astype(np.float64)


def ssim(a, b):
    import cv2
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    g = lambda x: cv2.GaussianBlur(x, (7, 7), 1.5)  # noqa
    ma, mb = g(a), g(b)
    saa, sbb, sab = g(a * a) - ma ** 2, g(b * b) - mb ** 2, g(a * b) - ma * mb
    s = ((2 * ma * mb + C1) * (2 * sab + C2)) / ((ma ** 2 + mb ** 2 + C1) * (saa + sbb + C2))
    return float(s.mean())


def trung_net(a, b):
    """Độ trùng nét vẽ (Dice) của 2 ảnh xám: điểm mực = xám < 200, nới 1 điểm ảnh."""
    import cv2
    k = np.ones((3, 3), np.uint8)
    ma = cv2.dilate((a < 200).astype(np.uint8), k)
    mb = cv2.dilate((b < 200).astype(np.uint8), k)
    t = ma.sum() + mb.sum()
    return float(2 * (ma & mb).sum() / t) if t else 1.0


def tuong_quan(a, b):
    a, b = a.ravel() - a.mean(), b.ravel() - b.mean()
    d = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else 1.0


def mau_chu_dao(doc):
    pm = doc[0].get_pixmap(dpi=36, alpha=False)
    a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.stride)[:, :pm.width * 3]
    px = a.reshape(-1, 3).astype(int)
    px = px[~((px.min(1) > 200) & (px.max(1) - px.min(1) < 20))]  # bỏ trắng và xám nhạt (nền)
    if not len(px):
        return None
    key = (px // 16) @ np.array([256, 16, 1])
    keys, cnt = np.unique(key, return_counts=True)
    return tuple(int(round(v)) for v in px[key == keys[np.argmax(cnt)]].mean(0))


def kiem_bo3(kiems, cfg):
    """kiems: {HÃNG: KiemPDF} → Muc(9) dùng chung cho cả bộ."""
    m = Muc(9)
    nguong = cfg['chung'].get('nguong_giong_giao_dien', MAC_DINH_GIONG_TOI_DA)
    nguon = ('HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt' if 'nguong_giong_giao_dien' in cfg['chung']
             else 'mặc định trong mã — ngưỡng ĐỀ XUẤT, chưa được anh duyệt')
    anh1, anhbd, vung, mau = {}, {}, {}, {}
    for h, k in kiems.items():
        anh1[h] = anh_xam(k.doc, 0)
        j = k.trang_bieu_do_dau()
        if j is not None:
            anhbd[h] = (j, anh_xam(k.doc, j))
            qh = [c for c in k.trang(j)['charts'] if nhan_dang_qh(c['box'], k.trang(j)['words'])] or k.trang(j)['charts']
            vung[h] = anh_xam(k.doc, j, 256, qh[0]['box'], 192)
        mau[h] = mau_chu_dao(k.doc)
    hs = list(kiems)
    for x in range(len(hs)):
        for y in range(x + 1, len(hs)):
            a, b = hs[x], hs[y]
            s1 = ssim(anh1[a], anh1[b])
            dong = f'{a}–{b}: trang 1 SSIM {s1:.2f} (tương quan {tuong_quan(anh1[a], anh1[b]):.2f})'
            vuot = s1 > nguong
            if a in anhbd and b in anhbd:
                s2 = ssim(anhbd[a][1], anhbd[b][1])
                s3 = trung_net(vung[a], vung[b])
                dong += (f'; trang biểu đồ tr.{anhbd[a][0] + 1}/tr.{anhbd[b][0] + 1} SSIM {s2:.2f}; '
                         f'vùng biểu đồ trùng nét {s3:.2f}')
                vuot = vuot or s2 > nguong or s3 > nguong
            elif (a in anhbd) != (b in anhbd):
                dong += "; chỉ một bản có biểu đồ"
            else:
                dong += "; cả hai bản không có biểu đồ"
            if mau[a] and mau[b]:
                dm = math.dist(mau[a], mau[b])
                dong += f'; màu chủ đạo #{"%02X%02X%02X" % mau[a]} / #{"%02X%02X%02X" % mau[b]} (cách {dm:.0f})'
                if dm < 40:
                    m.canh_bao.append(f'{a}–{b}: màu chủ đạo gần nhau (khoảng cách RGB {dm:.0f} < 40)')
            (m.loi if vuot else m.ghi_chu).append(dong + (f' → vượt {nguong:g} ({nguon})' if vuot else ''))
    for h in hs:
        hm = cfg.get('hang', {}).get(h, {}).get('mau', {}).get('chinh')
        if hm and mau[h]:
            ref = tuple(int(hm[i:i + 2], 16) for i in (1, 3, 5))
            m.ghi_chu.append(f'{h}: màu chủ đạo tr.1 #{"%02X%02X%02X" % mau[h]}, màu chính hồ sơ {hm} (cách {math.dist(ref, mau[h]):.0f})')
    m.ghi_chu.append(f'ngưỡng giống {nguong:g}: {nguon}; SSIM trên ảnh xám 72 dpi thu về 256×256; '
                     'vùng biểu đồ so bằng độ trùng nét vẽ (Dice) vì nền trắng làm SSIM vùng biểu đồ luôn cao')
    return m


# ----------------------------------------------------------------------------- in phiếu / CLI
def in_phieu(ten, info, kq, day_du=False, out=None):
    out = out or sys.stdout
    dem = {DAT: 0, CHUA: 0, KXM: 0, BO: 0}
    lim = 10 ** 6 if day_du else 12
    print(f'=== PHIẾU KIỂM: {ten}\n    {info}', file=out)
    for k in range(1, 11):
        mm = kq[k]
        tt = mm.trang_thai()
        dem[tt] += 1
        print(f' {k:>2}. {TEN_MUC[k]:<48} {tt}', file=out)
        for nh, ds in (('✗', mm.loi), ('?', mm.kxm), ('≈', mm.loi_goc), ('!', mm.canh_bao)):
            for s in ds[:lim]:
                print(f'      {nh} {s}', file=out)
            if len(ds) > lim:
                print(f'      {nh} … còn {len(ds) - lim} dòng (xem --json hoặc --day-du)', file=out)
        for s in (mm.ghi_chu if day_du else mm.ghi_chu[:3]):
            print(f'      · {s}', file=out)
    print(f' TỔNG KẾT: ĐẠT {dem[DAT]} · CHƯA ĐẠT {dem[CHUA]} · CHƯA THỂ XÁC MINH {dem[KXM]} · BỎ QUA {dem[BO]}', file=out)
    print('    (✗ lỗi → CHƯA ĐẠT · ? chưa thể xác minh · ≈ lỗi có từ bản gốc/ngoài trang vá — không tính · '
          '! cảnh báo, không đổi trạng thái · · ghi chú)\n', file=out)
    return dem


def khoa_loi(s):
    # (trang | None, dạng lỗi đã bỏ số liệu) để so lỗi bản mới với bản gốc
    mt = re.match(r'^tr\.(\d+)\b', s)
    t = re.sub(r'^tr\.\d+\s*', '', s)
    t = re.sub(r'"[^"]*"', '"…"', t)
    t = re.sub(r'\(vd [^)]*\)', '', t)
    t = re.sub(r'#[0-9A-Fa-f]{6}', lambda x: 'MAU' + x.group(0)[1:], t)
    t = re.sub(r'(?<![A-Za-z])\d+(?:[.,]\d+)?', '#', t)
    t = re.sub(r'tr\.[#,…\s]+', 'tr.#', t)
    return (int(mt.group(1)) if mt else None), re.sub(r'\s+', ' ', t).strip()


def tru_ban_goc(kq, kq_goc, trang=None):
    # Chỉ giữ CHƯA ĐẠT cho lỗi MỚI; lỗi đã có ở bản gốc (cùng trang, cùng dạng) hoặc ngoài các trang vá → loi_goc.
    for k, mm in kq.items():
        if k in (9, 10) or k not in kq_goc:
            continue
        goc = {khoa_loi(x) for x in kq_goc[k].loi}
        goc_dang = {d for _, d in goc}
        moi, cu = [], []
        for x in mm.loi:
            tr, d = khoa_loi(x)
            if trang and tr is not None and tr not in trang:
                cu.append(f'{x} — ngoài trang vá, không tính')
            elif (tr, d) in goc or (tr is None and d in goc_dang):
                cu.append(f'{x} — có từ bản gốc, không tính')
            else:
                moi.append(x)
        mm.loi, mm.loi_goc = moi, cu


def kiem_mot(path, muc_set, args=None, cfg=None):
    """Gọi từ công cụ khác (vd nhan_ban_chinh.py): trả (KiemPDF, {mục: Muc})."""
    cfg = cfg or doc_ho_so()
    if args is None:
        args = argparse.Namespace(du_lieu=None, nhanh=False, khong_dong_co=False, khong_qh=False)
    k = KiemPDF(path, cfg, args)
    return k, k.chay(set(muc_set))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Phiếu kiểm tự động 10 mục cho catalogue PDF (ngưỡng đọc từ rules/HO_SO_HANG.json).')
    ap.add_argument('duong_dan', nargs='?', help='PDF hoặc thư mục chứa PDF')
    ap.add_argument('--bo3', nargs=3, metavar=('AQUARIS', 'PEROTAC', 'REDPUMP'), help='3 PDF cùng dòng → mục 9')
    ap.add_argument('--du-lieu', help='DU_LIEU/<nhóm>.xlsx để so đường với bảng (≤5%%)')
    ap.add_argument('--json', help='ghi kết quả đầy đủ ra tệp JSON')
    ap.add_argument('--muc', help='chỉ chạy các mục, vd 1,2,8')
    ap.add_argument('--nhanh', action='store_true', help='bỏ đo vùng trống (mục 8) và mục 9')
    ap.add_argument('--tu-ghep-bo3', action='store_true', help='thư mục: tự ghép bộ 3 hãng theo tên "HÃNG - <dòng>.pdf" → mục 9')
    ap.add_argument('--day-du', action='store_true', help='in mọi dòng chi tiết')
    ap.add_argument('--khong-dong-co', action='store_true', help='sản phẩm không có động cơ (không bắt buộc "50 Hz")')
    ap.add_argument('--khong-qh', action='store_true', help='thiết bị không có Q–H (máy thổi khí, máy khuấy, định lượng, đĩa): '
                    'bỏ phép bảng/đường Q–H (mặc định tự nhận theo tên nhóm và nhãn trục)')
    ap.add_argument('--goc', help='PDF bản gốc đã duyệt: chỉ tính CHƯA ĐẠT lỗi MỚI so với bản gốc')
    ap.add_argument('--trang', help='với --goc: các trang đã vá (vd 2,3); lỗi ở trang khác không tính')
    args = ap.parse_args(argv)
    if not args.duong_dan and not args.bo3:
        ap.error('cần <pdf hoặc thư mục> hoặc --bo3')
    try:
        cfg = doc_ho_so()
    except Exception as e:  # noqa
        print(f'LỖI: không đọc được {TEP_HO_SO}: {e}', file=sys.stderr)
        return 2
    muc_set = set(range(1, 11)) if not args.muc else set(int(x) for x in re.split(r'[,\s]+', args.muc) if x)
    tep = []
    if args.duong_dan:
        p = Path(args.duong_dan)
        if p.is_dir():
            tep = sorted(x for x in p.rglob('*.pdf') if x.is_file())
        elif p.is_file():
            tep = [p]
        else:
            print(f'LỖI: không thấy {p}', file=sys.stderr)
            return 2
    bo3 = []
    if args.bo3:
        b = [Path(x) for x in args.bo3]
        for x in b:
            if not x.is_file():
                print(f'LỖI: không thấy {x}', file=sys.stderr)
                return 2
            if all(x.resolve() != t.resolve() for t in tep):
                tep.append(x)
        bo3.append(b)
    if args.tu_ghep_bo3:
        nhom = {}
        for t in tep:
            h, n = ten_hang_nhom(t)
            if h:
                # FS (AQUARIS) và FC (PEROTAC/REDPUMP) là cùng dòng (phương án 13/10, bảng "Phạm vi hãng")
                n = re.sub(r'(nước thải) F[SC]\b', r'\1 FS/FC', n)
                nhom.setdefault(n, {})[h] = t
        bo3 += [[d[h] for h in HANG] for n, d in sorted(nhom.items()) if all(h in d for h in HANG)]
    trang_va = set(int(x) for x in re.split(r'[,\s]+', args.trang) if x) if args.trang else None
    kq_goc = None
    if args.goc:
        if len(tep) != 1:
            print('LỖI: --goc chỉ dùng với đúng một PDF bản mới', file=sys.stderr)
            return 2
        if not Path(args.goc).is_file():
            print(f'LỖI: không thấy bản gốc {args.goc}', file=sys.stderr)
            return 2
        kq_goc = KiemPDF(Path(args.goc), cfg, args).chay(muc_set - {9, 10})
    obj = {}
    for t in tep:
        t0 = time.time()
        k = KiemPDF(t, cfg, args)
        kq = k.chay(muc_set)
        if kq_goc is not None:
            tru_ban_goc(kq, kq_goc, trang_va)
            kq[1].ghi_chu.append(f'so với bản gốc {Path(args.goc).name}' + (f', trang vá {sorted(trang_va)}' if trang_va else '')
                                 + ': chỉ lỗi MỚI tính CHƯA ĐẠT')
        obj[str(t.resolve())] = [k, kq, time.time() - t0]
    m9 = {}
    if 9 in muc_set and not args.nhanh:
        for b in bo3:
            t0 = time.time()
            try:
                mm = kiem_bo3({h: obj[str(x.resolve())][0] for x, h in zip(b, HANG)}, cfg)
            except Exception as e:  # noqa
                mm = Muc(9)
                mm.kxm.append(f'lỗi khi đo: {type(e).__name__}: {e}')
            for x in b:
                m9[str(x.resolve())] = mm
                obj[str(x.resolve())][2] += (time.time() - t0) / 3
    ket_qua, tong = [], {DAT: 0, CHUA: 0, KXM: 0, BO: 0}
    for key, (k, kq, dt) in obj.items():
        if key in m9:
            kq[9] = m9[key]
        else:
            mm = Muc(9)
            mm.ep = BO
            mm.ghi_chu.append('chỉ chạy khi có --bo3 / --tu-ghep-bo3' + (' (đang --nhanh)' if args.nhanh else ''))
            kq[9] = mm
        info = (f'{k.hang or "?"} · {k.nhom} · {k.doc.page_count} trang · {k.path.stat().st_size / 1e6:.2f} MB · '
                f'{dt:.1f} s · ngưỡng HO_SO_HANG.json bản {cfg.get("phien_ban")}')
        dem = in_phieu(k.path.name, info, kq, args.day_du)
        for x in dem:
            tong[x] += dem[x]
        ket_qua.append({'tep': str(k.path), 'ten': k.path.name, 'hang': k.hang, 'nhom': k.nhom,
                        'so_trang': k.doc.page_count, 'giay': round(dt, 1),
                        'muc': {str(i): kq[i].dict() for i in range(1, 11)}})
    if len(ket_qua) > 1:
        print(f'### TỔNG {len(ket_qua)} tệp: ĐẠT {tong[DAT]} · CHƯA ĐẠT {tong[CHUA]} · CHƯA THỂ XÁC MINH {tong[KXM]} · '
              f'BỎ QUA {tong[BO]} (đếm theo mục)')
    if args.json:
        Path(args.json).write_text(json.dumps({'phien_ban_ho_so': cfg.get('phien_ban'), 'tep': ket_qua},
                                              ensure_ascii=False, indent=1), encoding='utf-8')
    return 1 if tong[CHUA] else 0


if __name__ == '__main__':
    sys.exit(main())
