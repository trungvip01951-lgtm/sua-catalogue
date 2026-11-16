# -*- coding: utf-8 -*-
"""REDPUMP: thêm dải CDLF65/85/120/150/200 vào 'REDPUMP - Bơm trục đứng CDLF.pdf' đã duyệt (mỗi dải 2 trang, nhân bản tr.12–13 CDLF42).
Dùng: python dung_redpump.py <tệp ra>"""
import sys, pymupdf, lib, so_lieu
from lib import rgb, g, lmin
GOC = lib.goc_cdlf('REDPUMP')
FR, FB = lib.KHO + '/vendor/fonts/LiberationSans-Regular.ttf', lib.KHO + '/vendor/fonts/LiberationSans-Bold.ttf'
DARK, RED, GREY, TXT, WHITE, LIGHT, BAND, LUOI = rgb('2B2E33'), rgb('A31A1F'), rgb('66666B'), rgb('262629'), (1, 1, 1), rgb('CCCCD1'), rgb('F7F2EF'), rgb('DEDBDB')
D = so_lieu.doc(); goc = pymupdf.open(GOC); doc = pymupdf.open(GOC); T1, T2 = 11, 12   # trang mẫu (chỉ số)
def trai(pg, c, dai, d):
    lib.xoa(pg, chu=[(20, 34, 205, 74), (128, 255, 190, 321), (224, 37, 420, 49)])
    c(22, 35.2, 'CDLF' + dai, 34, True, WHITE); y = 257.1
    for _, v in lib.dac_tinh(dai, d): c(186, y, v, 7.6, True, WHITE, 'r'); y += 10.8
    c(226, 38.8, f"50 Hz  |  n ≈ {d['n']} /min", 8, False, GREY)
    if dai in lib.BICH: c(22, 357, lib.BICH[dai], 7, False, LIGHT)
for dai, d in D.items():
    ms = d['models']
    # ---------- trang đường + kích thước
    doc.insert_pdf(goc, from_page=T1, to_page=T1); pg = doc[-1]; c = lib.Chu(pg, FR, FB); trai(pg, c, dai, d)
    lib.xoa(pg, vung=[(221, 58, 462, 588), (466, 84, 770, 340), (466, 360, 770, 588)])
    lib.bieu_do(c, (270, 71, 452, 558), ms, d['Q'], dict(luoi=LUOI, co_truc=7.2, mau_truc=GREY, co_q=7.6, mau_q=DARK, co_l=7.0, q_dy=4.1, l_dy=15.7, khung=rgb('5C5E66'),
                co_tieu_h=7.8, x_tieu_h=223.7, mau_duong=RED, net=1.0, co_nhan=7.0, mau_nhan=DARK, dan=12, luoi_phu=True, q_vach=8))
    sk = f'sk{dai}.png'; w, h = lib.anh_so_do(dai, d, sk); H = 246; Wd = H * w / h
    pg.insert_image(pymupdf.Rect(618 - Wd / 2, 90, 618 + Wd / 2, 90 + H), filename=sk)
    rows = lib.gop_kich_thuoc(ms); y = 362; rh = min(12.4, (584 - 384) / len(rows))
    pg.draw_rect(pymupdf.Rect(468, y, 768, y + 22), color=None, fill=DARK)
    c(474, y + 6.9, 'MODEL', 7.6, True, WHITE); c(679, y + 2.5, 'SIZE (mm)', 7.2, True, WHITE, 'c')
    cx = [605, 638, 678, 716, 750]
    for x, t in zip(cx, ['B1', 'B2', 'B1+B2', 'D1', 'D2']): c(x, y + 12.7, t, 7, False, WHITE, 'c')
    y += 22
    for ten, dim in rows:
        c(474, y + (rh - 7.8) / 2 + 0.3, ten, 7, True, TXT)
        for x, v in zip(cx, dim): c(x, y + (rh - 7.8) / 2 + 0.3, str(v), 7, False, TXT, 'c')
        y += rh; pg.draw_line((468, y), (768, y), color=LUOI, width=0.5)
    pg.draw_line((468, y), (768, y), color=DARK, width=0.8)
    # ---------- trang bảng hiệu năng
    doc.insert_pdf(goc, from_page=T2, to_page=T2); pg = doc[-1]; c = lib.Chu(pg, FR, FB); trai(pg, c, dai, d)
    lib.xoa(pg, vung=[(224, 82, 770, 588)])
    Q = d['Q']; x0, x1 = 226, 768; pg.draw_rect(pymupdf.Rect(x0, 84, x1, 109), color=None, fill=DARK)
    c(235, 86.9, 'MODEL', 7.8, True, WHITE); c(235, 98.2, '3~ 380–415 V', 7, False, LIGHT)
    w = c(384, 86.6, 'P', 8.2, True, WHITE); c(384 + w, 90.8, '2', 5.6, True, WHITE); c(373.5, 98.2, 'kW', 7, False, WHITE, 'c'); c(409.5, 98.2, 'HP', 7, False, WHITE, 'c')
    c(432.5, 91.9, 'Q', 8.4, True, WHITE); c(467.5, 87.7, 'm³/h', 7, False, WHITE, 'r'); c(467.5, 98.2, 'l/min', 7, False, LIGHT, 'r')
    cw = (x1 - 471.5) / len(Q); qx = [471.5 + cw * (i + 0.5) for i in range(len(Q))]
    for x, q in zip(qx, Q): c(x, 86.9, g(q), 7.8, True, WHITE, 'c'); c(x, 98.2, lmin(q), 7, False, LIGHT, 'c')
    nhom = {}
    for m in ms: nhom.setdefault(lib.so_tang(m), []).append(m)
    n_dong = len(ms) + len(nhom); rh = min(14.5, (548 - 109 - 11.5 * len(nhom)) / len(ms)); y = 109
    for st, mm in nhom.items():
        pg.draw_rect(pymupdf.Rect(x0, y, x1, y + 11.5), color=None, fill=BAND); pg.draw_rect(pymupdf.Rect(x0, y, x0 + 3, y + 11.5), color=None, fill=RED)
        kws = sorted({m['kw'] for m in mm}); kw = g(kws[0]) if len(kws) == 1 else f'{g(kws[0])}–{g(kws[-1])}'
        c(235, y + 1.8, f"{st} STAGE{'S' if st > 1 else ''}     {kw} kW", 7.2, True, RED); c(760, y + 1.8, '3~ 380–415 V', 7.2, True, DARK, 'r'); y += 11.5
        ytop = y
        for m in mm:
            yt = y + (rh - 8.5) / 2
            c(235, yt, m['ten'], 7.6, True, TXT); c(373.5, yt, g(m['kw']), 7.6, False, TXT, 'c'); c(409.5, yt, g(m['hp']), 7.6, False, TXT, 'c')
            for x, v in zip(qx, m['h']): c(x, yt, g(v), 7.6, False, TXT, 'c')
            y += rh; pg.draw_line((x0, y), (425, y), color=LUOI, width=0.5); pg.draw_line((471.5, y), (x1, y), color=LUOI, width=0.5)
        c(449.5, (ytop + y) / 2 - 4.2, 'H (m)', 7.6, True, RED, 'c')
        pg.draw_line((425, ytop), (425, y), color=LUOI, width=0.5); pg.draw_line((471.5, ytop), (471.5, y), color=LUOI, width=0.5)
    pg.draw_line((x0, y), (x1, y), color=DARK, width=0.8); assert y < 560, (dai, y)
# ---------- trang 1: bảng PRODUCT RANGE (2 bảng xếp chồng vì 13 cột không vừa bề ngang 542 pt ở cỡ chữ ≥ 7 pt) + tiêu đề cấu tạo
p1 = doc[0]; cot, rows = lib.doc_bang_dai(p1, (224, 408, 770, 570)); cot, rows = lib.bang_dai_moi(cot, rows, D)
lib.xoa(p1, vung=[(224, 392, 770, 572)]); c = lib.Chu(p1, FR, FB); y = 246
c(226, y - 14, 'PRODUCT RANGE', 8.6, True, RED); p1.draw_line((226, y - 2.5), (768, y - 2.5), color=RED, width=0.7)
for i0, i1 in ((0, 6), (6, 13)):
    n = i1 - i0; cw = (768 - 340) / 7; xs = [340 + cw * (j + 0.5) for j in range(n)]; x1 = 768
    p1.draw_rect(pymupdf.Rect(226, y, x1, y + 15), color=None, fill=DARK); c(232, y + 3.9, 'DESCRIPTION', 7.2, True, WHITE)
    for x, t in zip(xs, cot[i0:i1]): c(x, y + 3.7, t, 7.4, True, WHITE, 'c')
    y += 15
    for nhan, v in rows:
        c(232, y + 2.5, nhan, 7.3, True, TXT)
        if len(v) == 1: c((xs[0] + xs[-1]) / 2, y + 2.5, v[0], 7.3, False, TXT, 'c')
        else:
            for x, t in zip(xs, v[i0:i1]): c(x, y + 2.5, t, 7.3, False, TXT, 'c')
        y += 13; p1.draw_line((226, y), (x1, y), color=LUOI, width=0.5)
    p1.draw_line((226, y), (x1, y), color=DARK, width=0.9); y += 14
assert y - 14 < 588, y
print('đổi tiêu đề:', lib.doi_tieu_de(doc, FR, FB))
print('bỏ "or 2950":', lib.bo_2950(doc, FR, FB))
print('đầu bơm → inox:', lib.dau_bom_inox(doc, FR, FB), 'dòng')
import cau_tao
cau_tao.them(doc, goc, lambda pg: lib.Chu(pg, FR, FB), 2, dict(x=226, w=260, y1=74.4, y2=364.4, bang_dy=17.6, anh=(256, 94, 456, 358), vung=(224, 60, 770, 588),
    chu=[pymupdf.Rect(_s['bbox']) for _s in lib._spans(goc[2]) if _s['bbox'][0] < 200 and _s['text'].strip() == 'CDLF 32, 42'] + [(224, 39.5, 420, 47)],
    viet=[(22, [_s['bbox'][1] for _s in lib._spans(goc[2]) if _s['bbox'][0] < 200 and _s['text'].strip() == 'CDLF 32, 42'][0], 'CDLF 120, 150, 200', 7.4, False, LIGHT), (226, 38.8, '50 Hz  |  n ≈ 2900 /min', 8, False, GREY)],
    hd=dict(co=8.4, mau=RED), bang=dict(nen_dau=DARK, chu_dau=WHITE, cot=[4, 24, 124, 196], rh=9.6, co=7, chu=TXT, ke=LUOI, ghi=GREY),
    ma=dict(x=508, y=74.4, w=260, d0=16.7, p=9.2, dx=26, co_k=7.6, co_t=7.3, mau_k=RED, mau_vd=GREY, mau_t=TXT)))
# ---------- số trang
N = doc.page_count
for i, pg in enumerate(doc):
    lib.xoa(pg, chu=[(700, 591, 770, 603)]); c = lib.Chu(pg, FR, FB); c(768, 593.3, f'{i + 1:02d} / {N}', 7.4, False, GREY, 'r')
doc.subset_fonts(); doc.save(sys.argv[1], garbage=4, deflate=True); print('saved', sys.argv[1], N, 'trang')
