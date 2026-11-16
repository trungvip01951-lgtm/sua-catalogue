# -*- coding: utf-8 -*-
"""AQUARIS: thêm dải CDLF65/85/120/150/200 vào 'AQUARIS - Bơm trục đứng CDLF.pdf' đã duyệt (nhân bản tr.11 CDLF42; mỗi trang ≤ 12 mã, chia theo số tầng).
Dùng: python dung_aquaris.py <tệp ra>"""
import sys, pymupdf, lib, so_lieu
from lib import rgb, g, lmin
GOC = lib.KHO + '/CATALOG SUA/CATALOGUE DA DUYET/AQUARIS/AQUARIS - Bơm trục đứng CDLF.pdf'
FR, FB = lib.KHO + '/vendor/fonts/LiberationSans-Regular.ttf', lib.KHO + '/vendor/fonts/LiberationSans-Bold.ttf'
LB, LL = lib.KHO + '/vendor/fonts/Lato-Bold.ttf', 'Lato-Light.ttf'
XANH, XAM, TXT, NEN, KE, WHITE = rgb('0D6159'), rgb('5C6E73'), rgb('1F3036'), rgb('EFF7F4'), rgb('D3E0DD'), (1, 1, 1)
MAU = [rgb(x) for x in ['0b6158', 'c0392b', '1f5fa8', 'd9791a', '6b3fa0', '2e8b3a', 'b0237a', '8a5a2b', '0e8fa3', '7a8b14', '1b2f6b', 'c99700', 'a61e3c']]
CHIA = {'65': [(1, 4), (5, 8)], '85': [(1, 6)], '120': [(1, 4), (5, 7)], '150': [(1, 3), (4, 6)], '200': [(1, 2), (3, 4)]}
D = so_lieu.doc(); goc = pymupdf.open(GOC); doc = pymupdf.open(GOC); T = 10
class ChuLato(lib.Chu):      # tiêu đề + ô số liệu nổi bật dùng Lato (Bold / Light) như trang mẫu
    def dam_bao(s):
        co = {f[4] for f in s.p.get_fonts()}
        if 'LTB' not in co: s.p.insert_font(fontname='LTB', fontfile=s.bold)
        if 'LTL' not in co: s.p.insert_font(fontname='LTL', fontfile=s.reg)
    def __call__(s, x, ytop, t, size, bold=False, color=(0, 0, 0), align='l'):
        w = s.w(t, size, bold); s.dam_bao(); x = x - w if align == 'r' else x - w / 2 if align == 'c' else x
        s.p.insert_text((x, ytop + size * s.asc), t, fontname='LTB' if bold else 'LTL', fontsize=size, color=color); return w
for dai, d in D.items():
    for a, b in CHIA[dai]:
        ms = [m for m in d['models'] if a <= lib.so_tang(m) <= b]; assert 0 < len(ms) <= 13
        doc.insert_pdf(goc, from_page=T, to_page=T); pg = doc[-1]; c = lib.Chu(pg, FR, FB); L = ChuLato(pg, LL, LB, asc=0.99)
        lib.xoa(pg, chu=[(38, 24, 420, 76), (38, 76, 760, 90), (120, 372, 262, 385)] + [(382, 128, 1166, 152)])
        w = L(40, 26.5, 'CDLF', 40, True, XANH); L(40 + w + 2.9, 26.5, dai, 40, False, XANH)
        c(41, 78.4, f"CDLF SERIES   ·   LIGHT STAINLESS STEEL VERTICAL MULTI-STAGE CENTRIFUGAL PUMP   ·   50 Hz  ·  n ≈ {d['n']} /min   ·   STAGE{'S' if b > a else ''} {a}{'–' + str(b) if b > a else ''}", 8.4, True, XANH, gian=0.485)
        c(190, 374.1, 'Illustrative photo', 7.6, True, XAM, 'c')
        for i, (_, v) in enumerate(lib.dac_tinh(dai, d)): L(380 + 132.84 * i + 61.4, 132.2, v, 15, True, XANH, 'c')
        lib.xoa(pg, vung=[(372, 182, 836, 478), (840, 212, 1169, 480), (378, 512, 1169, 745), (60, 408, 330, 714)])
        lib.bieu_do(c, (426, 195, 808, 448), ms, d['Q'], dict(luoi=KE, co_truc=7.2, mau_truc=XAM, co_q=7.6, mau_q=XANH, co_l=7.0, q_dy=4.1, l_dy=15.7, khung=XAM,
                    co_tieu_h=7.8, x_tieu_h=377.7, mau_duong=lambda k: MAU[k % len(MAU)], net=1.2, co_nhan=7.4, mau_nhan=XANH, nhan_mau_duong=True, dan=13, cat_day=a > 1, h_vach=8))
        sk = f'sk{dai}.png'; w_, h_ = lib.anh_so_do(dai, d, sk); H = 296; Wd = H * w_ / h_
        pg.insert_image(pymupdf.Rect(190 - Wd / 2, 414, 190 + Wd / 2, 414 + H), filename=sk)
        # kích thước
        rows = lib.gop_kich_thuoc(ms); pg.draw_rect(pymupdf.Rect(842, 214, 1167, 242), color=None, fill=NEN); pg.draw_line((842, 214), (1167, 214), color=XANH, width=0.8)
        c(848, 224.1, 'MODEL', 7.6, True, XANH); c(1066, 217.8, 'SIZE (mm)', 7.4, True, XANH, 'c'); cx = [980 + 41.5 * i for i in range(5)]
        for x, t in zip(cx, ['B1', 'B2', 'B1+B2', 'D1', 'D2']): c(x, 230.2, t, 7, False, XAM, 'c')
        y = 242; rh = min(15, (478 - 242) / len(rows))
        for ten, dim in rows:
            c(848, y + (rh - 8.3) / 2, ten, 7.4, True, TXT)
            for x, v in zip(cx, dim): c(x, y + (rh - 8.5) / 2, str(v), 7.6, False, TXT, 'c')
            y += rh; pg.draw_line((842, y), (1167, y), color=KE, width=0.5)
        pg.draw_line((842, y), (1167, y), color=XANH, width=0.8)
        # hiệu năng
        Q = d['Q']; pg.draw_rect(pymupdf.Rect(380, 514, 1167, 546), color=None, fill=NEN); pg.draw_line((380, 514), (1167, 514), color=XANH, width=0.8)
        c(390, 519.6, 'MODEL', 8, True, XANH); c(390, 533.9, '3~ 380–415 V', 7, False, XAM); c(556, 525.8, 'STAGES', 8, True, XANH, 'c')
        w = c(621.5, 519, 'P', 8.6, True, XANH); c(621.5 + w, 523.4, '2', 5.8, True, XANH); c(604, 533.7, 'kW', 7.2, False, XAM, 'c'); c(648, 533.7, 'HP', 7.2, False, XAM, 'c')
        c(675, 525.4, 'Q', 8.4, True, XANH); c(716, 520.5, 'm³/h', 7, False, XANH, 'r'); c(716, 533.9, 'l/min', 7, False, XAM, 'r')
        cw = (1167 - 720) / len(Q); qx = [720 + cw * (i + 0.5) for i in range(len(Q))]
        for x, q in zip(qx, Q): c(x, 519.7, g(q), 7.8, True, XANH, 'c'); c(x, 533.9, lmin(q), 7, False, XAM, 'c')
        y = 546.6; rh = 15.4
        pg.draw_rect(pymupdf.Rect(670, y, 720, y + rh * len(ms)), color=None, fill=NEN)
        for k, m in enumerate(ms):
            pg.draw_rect(pymupdf.Rect(390, y + 6.2, 398, y + 9.2), color=None, fill=MAU[k % len(MAU)])
            c(403, y + 3.1, m['ten'], 8.2, True, TXT); c(515.8, y + 3.9, '3~', 7.2, False, XANH); c(556, y + 3.1, str(lib.so_tang(m)), 8.2, False, XAM, 'c')
            c(604, y + 3.1, g(m['kw']), 8.2, False, TXT, 'c'); c(648, y + 3.1, g(m['hp']), 8.2, False, TXT, 'c')
            for x, v in zip(qx, m['h']): c(x, y + 3.1, g(v), 8.2, False, TXT, 'c')
            y += rh; pg.draw_line((380, y), (670, y), color=KE, width=0.5); pg.draw_line((720, y), (1167, y), color=KE, width=0.5)
        c(695, (546.6 + y) / 2 - 4.5, 'H (m)', 8.2, True, XANH, 'c'); pg.draw_line((380, y), (1167, y), color=XANH, width=0.8)
# ---------- trang 1: ô số liệu nổi bật + bảng PRODUCT RANGE 13 cột + tiêu đề
p1 = doc[0]; cot, rows = lib.doc_bang_dai(p1, (378, 458, 1169, 748)); cot, rows = lib.bang_dai_moi(cot, rows, D)
cu = {s['text'].strip() for s in lib._spans(p1, pymupdf.Rect(378, 126, 1169, 154))}; assert {'2–42 m³/h', '1–55 m³/h', '21–30 bar', '0.37–45 kW'} <= cu, cu
lib.xoa(p1, chu=[(382, 128, 902, 152)]); L = ChuLato(p1, LL, LB, asc=0.99)
kwmax = max(m['kw'] for d in D.values() for m in d['models']); qmax = max(d['Q'][-1] for d in D.values()); barmin = min(int(lib.PR[k]['bar']) for k in D)
for i, v in enumerate(['2–200 m³/h', f'1–{qmax} m³/h', f'{barmin}–30 bar', f'0.37–{g(kwmax)} kW']): L(380 + 132.84 * i + 61.4, 132.2, v, 15, True, XANH, 'c')
lib.xoa(p1, vung=[(378, 458, 1169, 752)]); c = lib.Chu(p1, FR, FB); y = 460; cw = (1167 - 500) / 13; xs = [500 + cw * (j + 0.5) for j in range(13)]
p1.draw_rect(pymupdf.Rect(380, y, 1167, y + 15), color=None, fill=NEN); p1.draw_line((380, y), (1167, y), color=XANH, width=1.1); p1.draw_line((380, y + 15), (1167, y + 15), color=XANH, width=0.8)
c(386, y + 3.9, 'DESCRIPTION', 7.2, True, XANH)
for x, t in zip(xs, cot): c(x, y + 3.7, t, 7.4, True, XANH, 'c')
y += 15
for nhan, v in rows:
    c(386, y + 7.5, nhan, 8.4, True, TXT)
    if len(v) == 1: c((xs[0] + xs[-1]) / 2, y + 7.5, v[0], 8.4, False, TXT, 'c')
    else:
        for x, t in zip(xs, v): c(x, y + 7.5, t, 8.4, False, TXT, 'c')
    y += 25; p1.draw_line((380, y), (1167, y), color=KE, width=0.5)
p1.draw_line((380, y), (1167, y), color=XANH, width=1.1)
print('đổi tiêu đề:', lib.doi_tieu_de(doc, FR, FB))
import cau_tao
cau_tao.them(doc, goc, lambda pg: lib.Chu(pg, FR, FB), 1, dict(x=40, w=357, y1=117.5, y2=483.5, bang_dy=18.5, anh=(70, 142, 370, 462), vung=(38, 104, 1169, 760), trang_ma=0,
    hd=dict(co=9.4, mau=XANH), bang=dict(nen_dau=NEN, chu_dau=XANH, cot=[4, 30, 162, 258], rh=13, co=8, chu=TXT, ke=KE, ghi=XAM, co_ghi=7.6),
    ma=dict(x=486, y=117.5, w=357, d0=19, p=11, dx=30, co_k=8.3, co_t=8.0, mau_k=XANH, mau_vd=XAM, mau_t=TXT)))
N = doc.page_count
for i, pg in enumerate(doc):
    lib.xoa(pg, chu=[(1100, 800, 1169, 814)]); c = lib.Chu(pg, FR, FB); c(1167, 802.8, f'{i + 1:02d} / {N}', 8, False, XAM, 'r')
doc.subset_fonts(); doc.save(sys.argv[1], garbage=4, deflate=True); print('saved', sys.argv[1], N, 'trang')
