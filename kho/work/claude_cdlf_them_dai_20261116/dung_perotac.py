# -*- coding: utf-8 -*-
"""PEROTAC: thêm dải CDLF65/85/120/150/200 vào 'PEROTAC - Bơm trục đứng CDLF.pdf' đã duyệt (mỗi dải 2 trang, nhân bản tr.11–12 CDLF42).
Dùng: python dung_perotac.py <tệp ra>"""
import sys, pymupdf, lib, so_lieu
from lib import rgb, g, lmin
GOC = lib.KHO + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm trục đứng CDLF.pdf'
FR, FB = lib.KHO + '/vendor/fonts/LiberationSans-Regular.ttf', lib.KHO + '/vendor/fonts/LiberationSans-Bold.ttf'
NAVY, BLUE, TXT, GREY, WHITE, ROW, KE = rgb('13334D'), rgb('1A669E'), rgb('1F3847'), rgb('5C6E78'), (1, 1, 1), rgb('EDF4F9'), rgb('D6E0E5')
D = so_lieu.doc(); goc = pymupdf.open(GOC); doc = pymupdf.open(GOC); T1, T2 = 10, 11
def dau(pg, c, dai, d, phu):
    lib.xoa(pg, chu=[(180, 18, 330, 51), (420, 34, 770, 46)])
    c(182, 19.6, 'CDLF' + dai, 27, True, NAVY)
    c(768, 35.9, f"Light stainless steel vertical multi-stage centrifugal pump  |  50 Hz  |  n ≈ {d['n']} /min", 7.8, False, TXT, 'r')
for dai, d in D.items():
    ms = d['models']
    doc.insert_pdf(goc, from_page=T1, to_page=T1); pg = doc[-1]; c = lib.Chu(pg, FR, FB); dau(pg, c, dai, d, 0)
    lib.xoa(pg, chu=[(102, 88, 208, 153)]); y = 89.1
    for _, v in lib.dac_tinh(dai, d): c(104, y, v, 7.6, False, TXT); y += 10.8
    lib.xoa(pg, vung=[(434, 64, 771, 574), (210, 86, 432, 348), (22, 372, 434, 556)])
    lib.bieu_do(c, (486, 75, 762, 546), ms, d['Q'], dict(luoi=KE, co_truc=7.2, mau_truc=GREY, co_q=7.6, mau_q=NAVY, co_l=7.0, q_dy=4.1, l_dy=15.7, khung=GREY,
                co_tieu_h=7.8, x_tieu_h=437.7, mau_duong=BLUE, net=1.0, co_nhan=7.0, mau_nhan=NAVY, dan=13, luoi_phu=True))
    sk = f'sk{dai}.png'; w, h = lib.anh_so_do(dai, d, sk); H = 250; Wd = H * w / h
    pg.insert_image(pymupdf.Rect(321 - Wd / 2, 92, 321 + Wd / 2, 92 + H), filename=sk)
    rows = lib.gop_kich_thuoc(ms); y = 374; rh = min(12, (554 - 398) / len(rows)); xs = [24, 174, 225.6, 277.2, 328.8, 380.4, 432]
    pg.draw_rect(pymupdf.Rect(24, y, 432, y + 24), color=None, fill=NAVY)
    c(99, y + 7.7, 'MODEL', 7.8, True, WHITE, 'c'); c(303, y + 2.5, 'SIZE (mm)', 7.6, True, WHITE, 'c')
    cx = [(a + b) / 2 for a, b in zip(xs[1:], xs[2:])]
    for x, t in zip(cx, ['B1', 'B2', 'B1+B2', 'D1', 'D2']): c(x, y + 13.7, t, 7, False, WHITE, 'c')
    y += 24; y0 = y
    for i, (ten, dim) in enumerate(rows):
        if i % 2 == 0: pg.draw_rect(pymupdf.Rect(24, y, 432, y + rh), color=None, fill=ROW)
        c(32, y + (rh - 8.3) / 2, ten, 7.4, True, TXT)
        for x, v in zip(cx, dim): c(x, y + (rh - 8.3) / 2, str(v), 7.4, False, TXT, 'c')
        y += rh
    for i in range(len(rows) + 1): pg.draw_line((24, y0 + i * rh), (432, y0 + i * rh), color=KE, width=0.5)
    for x in xs: pg.draw_line((x, y0), (x, y), color=KE, width=0.5)
    # ---------- bảng hiệu năng
    doc.insert_pdf(goc, from_page=T2, to_page=T2); pg = doc[-1]; c = lib.Chu(pg, FR, FB); dau(pg, c, dai, d, 1)
    lib.xoa(pg, vung=[(22, 94, 770, 540)])
    Q = d['Q']; pg.draw_rect(pymupdf.Rect(24, 96, 768, 123), color=None, fill=NAVY)
    c(102, 99.7, 'MODEL', 7.8, True, WHITE, 'c'); c(63, 111.8, '3~ 380–415 V', 7, False, WHITE, 'c'); c(141, 111.8, '1~ 220–240 V', 7, False, WHITE, 'c')
    w = c(207.7, 99.4, 'P', 8.2, True, WHITE); c(207.7 + w, 103.6, '2', 5.6, True, WHITE); c(196, 111.8, 'kW', 7, False, WHITE, 'c'); c(228, 111.8, 'HP', 7, False, WHITE, 'c')
    c(249, 104.9, 'Q', 8.4, True, WHITE); c(280, 100.5, 'm³/h', 7, False, WHITE, 'r'); c(280, 111.8, 'l/min', 7, False, WHITE, 'r')
    cw = (768 - 284) / len(Q); qx = [284 + cw * (i + 0.5) for i in range(len(Q))]
    for x, q in zip(qx, Q): c(x, 99.7, g(q), 7.8, True, WHITE, 'c'); c(x, 111.8, lmin(q), 7, False, WHITE, 'c')
    rh = min(16.5, (536 - 123) / len(ms)); y = 123
    for i, m in enumerate(ms):
        if i % 2 == 0: pg.draw_rect(pymupdf.Rect(24, y, 244, y + rh), color=None, fill=ROW); pg.draw_rect(pymupdf.Rect(284, y, 768, y + rh), color=None, fill=ROW)
        yt = y + (rh - 8.5) / 2
        c(32, yt, m['ten'], 7.6, True, TXT); c(141, yt, '–', 7.6, False, GREY, 'c'); c(196, yt, g(m['kw']), 7.6, False, TXT, 'c'); c(228, yt, g(m['hp']), 7.6, False, TXT, 'c')
        for x, v in zip(qx, m['h']): c(x, yt, g(v), 7.6, False, TXT, 'c')
        y += rh
    c(264, (123 + y) / 2 - 4.2, 'H (m)', 7.6, True, BLUE, 'c')
    for i in range(len(ms) + 1):
        yy = 123 + i * rh; pg.draw_line((24, yy), (244, yy), color=KE, width=0.5); pg.draw_line((284, yy), (768, yy), color=KE, width=0.5)
    for x in [24, 102, 180, 212, 244, 284] + [284 + cw * (i + 1) for i in range(len(Q))]: pg.draw_line((x, 123), (x, y), color=KE, width=0.5)
# ---------- trang 1: bảng PRODUCT RANGE 13 cột + tiêu đề
p1 = doc[0]; cot, rows = lib.doc_bang_dai(p1, (22, 436, 770, 578)); cot, rows = lib.bang_dai_moi(cot, rows, D)
lib.xoa(p1, vung=[(22, 436, 770, 580)]); c = lib.Chu(p1, FR, FB); y = 438; cw = (768 - 138) / 13; xs = [138 + cw * (j + 0.5) for j in range(13)]
p1.draw_rect(pymupdf.Rect(24, y, 768, y + 15), color=None, fill=NAVY); c(30, y + 3.9, 'DESCRIPTION', 7.2, True, WHITE)
for x, t in zip(xs, cot): c(x, y + 3.7, t, 7.4, True, WHITE, 'c')
y += 15
for i, (nhan, v) in enumerate(rows):
    if i % 2 == 0: p1.draw_rect(pymupdf.Rect(24, y, 768, y + 11.2), color=None, fill=ROW)
    c(30, y + 1.6, nhan, 7.3, True, TXT)
    if len(v) == 1: c((xs[0] + xs[-1]) / 2, y + 1.6, v[0], 7.3, False, TXT, 'c')
    else:
        for x, t in zip(xs, v): c(x, y + 1.6, t, 7.3, False, TXT, 'c')
    y += 11.2; p1.draw_line((24, y), (768, y), color=KE, width=0.5)
print('đổi tiêu đề:', lib.doi_tieu_de(doc, FR, FB))
import cau_tao
cau_tao.them(doc, goc, lambda pg: lib.Chu(pg, FR, FB), 1, dict(x=24, w=236, y1=72.4, y2=334.4, bang_dy=17.6, anh=(42, 92, 242, 326), vung=(22, 64, 770, 585), trang_ma=0,
    chu=[(420, 34, 770, 46)], viet=[(768, 35.9, 'Light stainless steel vertical multi-stage centrifugal pump  |  50 Hz  |  n ≈ 2950 /min', 7.8, False, TXT, 'r')],
    hd=dict(co=8.4, mau=BLUE), bang=dict(nen_dau=NAVY, chu_dau=WHITE, cot=[4, 22, 108, 170], rh=9.6, co=7, chu=TXT, ke=KE, ghi=GREY, soc=ROW),
    ma=dict(x=278, y=72.4, w=236, d0=16.7, p=9.2, dx=26, co_k=7.6, co_t=7.3, mau_k=NAVY, mau_vd=GREY, mau_t=TXT)))
N = doc.page_count
for i, pg in enumerate(doc):
    lib.xoa(pg, chu=[(700, 591, 770, 603)]); c = lib.Chu(pg, FR, FB); c(768, 593.3, f'{i + 1:02d} / {N}', 7.4, False, GREY, 'r')
doc.subset_fonts(); doc.save(sys.argv[1], garbage=4, deflate=True); print('saved', sys.argv[1], N, 'trang')
