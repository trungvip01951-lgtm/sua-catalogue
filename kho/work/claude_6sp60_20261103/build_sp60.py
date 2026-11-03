# -*- coding: utf-8 -*-
"""REDPUMP 6SP60 — catalogue riêng dải 6SP60 (17 mã), A4 ngang, 5 trang (03/11/2026, phiên CLAUDE_20261103T0100Z, QĐ 166).
Lệnh anh: báo giá (bơm chìm hỏa tiễn 50 m³/h–50 m và 60 m³/h–50 m, hiệu suất ≥ 70 %) + "làm catalogue REDPUMP 6SP dải 60 cho a có đầy đủ
thông số kỹ thuật nhé. hiêu ssuất trên 70% tại điểm làm việc cho a nhé."
Số: SP60.xlsx (bảng, kích thước, η) — mk_xlsx.py; SP60_duong.xlsx (chỉ để vẽ đường mềm, lệch bảng ≤ 4.02 %) — mk_duong.py.
Chữ/vật liệu: REDPUMP - Bơm giếng SP.pdf tr.10 (mục 6SP), bỏ dòng ISO 9906 (QĐ 149). η: đường η tr.14 đã duyệt (số hoá).
Ảnh: KHO_ANH/Bom_gieng_SP/f5c472824f21.png (ĐẠT). Mẫu khung trang: work/claude_rpx_redpump_20261029/build_rpx.py.
Dùng: python build_sp60.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, json, pymupdf, openpyxl, numpy as np
R, W, OUT = sys.argv[1:4]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
DARK, RED, GREY, TXT, WHITE, LINE, PLOT = rgb('2B2E33'), rgb('A31A1F'), rgb('6B6F75'), rgb('222428'), (1, 1, 1), rgb('D9D4D1'), rgb('F4F4F4')
STRIPE, LIGHT = rgb('F1EEEC'), rgb('C9CDD2')
W_, H_ = 842, 595; COL = 238; CX0, CX1 = COL + 26, W_ - 34
LOGO = R + '/KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg'; ANH = R + '/KHO_ANH/Bom_gieng_SP/f5c472824f21.png'

# ---- dữ liệu
wb = openpyxl.load_workbook(W + '/SP60.xlsx', data_only=True)
MD = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)]
QH = {}
for r in wb['QH'].iter_rows(min_row=2, values_only=True): QH.setdefault(r[1], {})[r[2]] = r[3]
KT = [r for r in wb['KICH_THUOC'].iter_rows(min_row=2, values_only=True)]
ETA = [(r[0], r[1]) for r in wb['ETA'].iter_rows(min_row=2, values_only=True) if r[0] != 'dinh']
DINH = [r for r in wb['ETA'].iter_rows(min_row=2, values_only=True) if r[0] == 'dinh'][0]
DQH = {}
for r in openpyxl.load_workbook(W + '/SP60_duong.xlsx', data_only=True)['QH'].iter_rows(min_row=2, values_only=True): DQH.setdefault(r[1], {})[r[2]] = r[3]
LECH = json.load(open(W + '/lech_duong.json'))
from scipy.interpolate import PchipInterpolator as _P
eta_at = lambda q: float(_P([a for a, b in ETA], [b for a, b in ETA])(q))
def h_duong(m, q):
    k = sorted(DQH[m]); from scipy.interpolate import CubicSpline
    return float(CubicSpline(k, [DQH[m][x] for x in k])(q))
NHOM = [['6SP60-2', '6SP60-6', '6SP60-10', '6SP60-13', '6SP60-16'], ['6SP60-3', '6SP60-8', '6SP60-11', '6SP60-14', '6SP60-18'], ['6SP60-4', '6SP60-9', '6SP60-12', '6SP60-15', '6SP60-20']]
DUTY = [('54 m³/h – 53 m', '6SP60-6', 54), ('64 m³/h – 56 m', '6SP60-8', 64)]   # QĐ 168 + QĐ 170: 6SP60-8 dời về 64 m³/h (η ≥ 70 %)
DP = [(lab, m, q, QH[m].get(q, round(h_duong(m, q))), round(eta_at(q), 1), [r for r in MD if r[2] == m][0]) for lab, m, q in DUTY]   # H = số bảng đã duyệt tại Q đó
print('DP', [(d[1], d[2], d[3], d[4], round(h_duong(d[1], d[2]), 2)) for d in DP]); assert [d[3] for d in DP] == [53, 56] and all(d[4] > 70 for d in DP) and all(abs(h_duong(d[1], d[2]) - d[3]) / d[3] < 0.05 for d in DP), DP
D0 = pymupdf.open(R + '/CATALOG SUA/CATALOGUE DA DUYET/REDPUMP/REDPUMP - Bơm giếng SP.pdf')
L = [s.strip() for s in D0[9].get_text().splitlines() if s.strip()]; i0 = L.index('6SP')
def khoi(a, b): i = L.index(a, i0); return L[i + 1:L.index(b, i + 1)]
APP = khoi('Applications', 'Operating conditions'); OPC = khoi('Operating conditions', 'Motor and pump')
MOT = [s for s in khoi('Motor and pump', 'Options on request') if 'ISO 9906' not in s]
OPT = khoi('Options on request', 'COMPONENT'); ML_ = khoi('MATERIAL', 'Shaft')
ml = L[L.index('MATERIAL', i0) + 1:L.index('MATERIAL', i0) + 21]; MAT = list(zip(ml[0::2], ml[1::2]))
sh = [i for i, (a, b) in enumerate(MAT) if a == 'Shaft']; assert len(sh) == 2
MAT[sh[0]] = ('Pump shaft', MAT[sh[0]][1]); MAT[sh[1]] = ('Motor shaft', MAT[sh[1]][1])
assert MAT[0] == ('Delivery casing', 'AISI 304 SS') and len(MAT) == 10, MAT

doc = pymupdf.open(); FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
class Pg:
    def __init__(s, so, ten, tom=None):
        s.p = p = doc.new_page(width=W_, height=H_); p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
        p.draw_rect(pymupdf.Rect(0, 0, COL, H_), color=None, fill=DARK); p.draw_rect(pymupdf.Rect(COL - 5, 0, COL, H_), color=None, fill=RED)
        s.txt(28, 60, 'SP SERIES  ·  6-INCH WELL PUMPS', 9, True, LIGHT)
        if so: s.txt(28, 112, so, 30, True, rgb('E8767B'))
        y = 140
        for l in s.wrap(ten, 17, COL - 56, True): s.txt(28, y, l, 17, True, WHITE); y += 21
        if tom:
            y += 8
            for l in s.wrap(tom, 9, COL - 56): s.txt(28, y, l, 9, False, LIGHT); y += 12
        s.yc = y
        pix = pymupdf.Pixmap(LOGO); k = min(104 / pix.width, 46 / pix.height)
        p.insert_image(pymupdf.Rect(CX1 - pix.width * k, 18, CX1, 18 + pix.height * k), filename=LOGO)
        p.draw_line((CX0, 566), (CX1, 566), color=LINE, width=0.5)
        s.txt(CX0, 580, 'REDPUMP  /  6SP60', 7.5, True, GREY); s.txt(CX1, 580, f'{doc.page_count:02d} / 05', 7.5, True, GREY, 'r')
    def txt(s, x, y, st, size, bold=False, color=TXT, align='l'):
        w = FONT[bold].text_length(st, size)
        if align == 'r': x -= w
        elif align == 'c': x -= w / 2
        s.p.insert_text((x, y), st, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
    def wrap(s, st, size, width, bold=False):
        out, cur = [], ''
        for w in st.split():
            c = (cur + ' ' + w).strip()
            if FONT[bold].text_length(c, size) <= width: cur = c
            else: out.append(cur); cur = w
        return out + [cur]
    def head(s, x, y, st, w):
        s.txt(x, y, st, 10, True, DARK); s.p.draw_line((x, y + 5), (x + w, y + 5), color=RED, width=1.2); return y + 19
    def lst(s, x, y, ds, w, size=9):
        for d in ds:
            for i, l in enumerate(s.wrap(d, size, w - 9)):
                if i == 0: s.p.draw_circle((x + 2.5, y - 3), 1.3, color=None, fill=RED)
                s.txt(x + 9, y, l, size); y += size * 1.3
        return y
    def table(s, x, y, hdr, rows, widths, size=8, rh=13.5, al=None):
        tw = sum(widths); p = s.p; p.draw_rect(pymupdf.Rect(x, y, x + tw, y + rh + 2), color=None, fill=DARK)
        cx = x
        for h, w in zip(hdr, widths): s.txt(cx + w / 2, y + rh - 2.5, h, size, True, WHITE, 'c'); cx += w
        y += rh + 2
        for i, row in enumerate(rows):
            if i % 2: p.draw_rect(pymupdf.Rect(x, y, x + tw, y + rh), color=None, fill=STRIPE)
            cx = x
            for j, (v, w) in enumerate(zip(row, widths)):
                a = (al or ['l'] + ['c'] * (len(row) - 1))[j]
                s.txt(cx + 5 if a == 'l' else cx + w / 2, y + rh - 4, str(v), size, j == 0, TXT, 'l' if a == 'l' else 'c'); cx += w
            y += rh
        p.draw_line((x, y), (x + tw, y), color=DARK, width=0.8); return y
    def chart(s, rect, pdf):
        bd = pymupdf.open(pdf); s.p.show_pdf_page(rect, bd, 0); bp = bd[0]; sc = rect.width / bp.rect.width
        nen = max([d['rect'] for d in bp.get_drawings() if d.get('fill') and all(abs(c - 0xF4 / 255) < 0.01 for c in d['fill'][:3])], key=lambda r: r.width * r.height)
        sp = [(x['text'].strip(), pymupdf.Rect(x['bbox'])) for b in bp.get_text('dict')['blocks'] for l in b.get('lines', []) for x in l['spans']]
        num = lambda t: re.fullmatch(r'\d+(\.\d+)?', t)
        q1 = max(float(t) for t, r in sp if num(t) and nen.y1 < r.y0 < nen.y1 + 14); h1 = max(float(t) for t, r in sp if num(t) and r.x0 > nen.x1)
        return (lambda q: rect.x0 + (nen.x0 + nen.width * q / q1) * sc), (lambda h: rect.y0 + (nen.y1 - nen.height * h / h1) * sc)
    def duty(s, X, Y, q, h, lab):
        pt = pymupdf.Point(X(q), Y(h)); p = s.p
        p.draw_line((X(q), Y(0)), pt, color=RED, width=0.6, dashes='[2 2] 0'); p.draw_circle(pt, 3.2, color=DARK, fill=WHITE, width=1.1)
        w = FONT[True].text_length(lab, 7.5); bx = pymupdf.Rect(pt.x - w - 10, pt.y - 15, pt.x - 4, pt.y - 5)
        p.draw_rect(bx, color=DARK, fill=WHITE, width=0.5); s.txt(bx.x0 + 3, bx.y1 - 2.5, lab, 7.5, True, DARK)

PPI = {}
# ================= Trang 1 =================
pg = Pg(None, '6SP60 stainless steel submersible well pumps', f'Rated flow 60 m³/h · 6-inch wells · {len(MD)} models, 2 to 20 impellers.')
y = pg.yc + 24; t = pg.txt
for a, b in [('Power P2', f'{min(r[3] for r in MD):g}–{max(r[3] for r in MD):g} kW'), ('Flow rate', f'up to {max(max(v) for v in QH.values()):g} m³/h'),
             ('Head', f'up to {max(max(v.values()) for v in QH.values()):g} m'), ('Pump efficiency', f'up to {DINH[1]:g} %'),
             ('Outlet', '3 in'), ('Power supply', '3~ 380–415 V 50 Hz'), ('Speed', 'n ≈ 2850 /min'), ('Min. well diameter', '6 in')]:
    t(28, y, a, 8, True, LIGHT); t(118, y, b, 9.5, True, WHITE); y += 16
t(CX0, 104, '6SP60', 30, True, DARK); t(CX0, 128, 'STAINLESS STEEL SUBMERSIBLE PUMPS  ·  50 Hz  ·  n ≈ 2850 /min', 10, True, RED)
pix = pymupdf.Pixmap(ANH); bh = 400; bw = pix.width * bh / pix.height
rr = pymupdf.Rect(CX0 + 8, 150, CX0 + 8 + bw, 150 + bh); pg.p.draw_oval(pymupdf.Rect(rr.x0 - 6, rr.y1 - 4, rr.x1 + 6, rr.y1 + 6), color=None, fill=rgb('E3DFDC'))
pg.p.insert_image(rr, filename=ANH); PPI['anh'] = pix.height / bh * 72
x1 = CX0 + 110; w1 = 200; y = 156
y = pg.head(x1, y, 'APPLICATIONS', w1); y = pg.lst(x1, y, APP, w1)
y = pg.head(x1, y + 8, 'OPERATING CONDITIONS', w1); y = pg.lst(x1, y, OPC, w1)
y = pg.head(x1, y + 8, 'MOTOR AND PUMP', w1); y = pg.lst(x1, y, MOT, w1)
y = pg.head(x1, y + 8, 'OPTIONS ON REQUEST', w1); y = pg.lst(x1, y, OPT, w1); assert y < 556, y
x2 = x1 + w1 + 22; w2 = CX1 - x2
yy = pg.head(x2, 156, 'MATERIALS', w2); yy = pg.table(x2, yy - 6, ['Component', 'Material'], MAT, [96, w2 - 96], size=7.8, rh=13)
yy = pg.head(x2, yy + 22, 'MODEL CODE', w2)
for c, d in [('6', 'Well diameter (in)'), ('SP', 'Series'), ('60', 'Rated flow (m³/h)'), ('8', 'Number of impellers')]:
    t(x2, yy, c, 11, True, RED); t(x2 + 30, yy, d, 9); yy += 14
t(x2, yy + 4, 'Example: 6SP60-8', 9, False, GREY); assert yy < 556

# ================= Trang 2: biểu đồ A, B =================
pg = Pg('1', 'Performance curves', 'Group A and group B. Curves at 50 Hz, n ≈ 2850 /min. Data table: page 4.')
cw = 266; chh = 328
for i, f in enumerate(('bd1', 'bd2')):
    x = CX0 + i * (cw + 14); pg.head(x, 92, ['GROUP A', 'GROUP B'][i], cw)
    X, Y = pg.chart(pymupdf.Rect(x, 104, x + cw, 104 + chh), W + f'/qh/{f}.pdf')
    for d in DP:
        if d[1] in NHOM[i]: pg.duty(X, Y, d[2], d[3], f'Duty point {d[0]}')
# ================= Trang 3: biểu đồ C + η =================
pg = Pg('2', 'Curves, efficiency and duty points', 'Group C, pump efficiency curve of the 6SP60 range and the two duty points.')
x = CX0; pg.head(x, 92, 'GROUP C', cw); X, Y = pg.chart(pymupdf.Rect(x, 104, x + cw, 104 + chh), W + '/qh/bd3.pdf')
for d in DP:
    if d[1] in NHOM[2]: pg.duty(X, Y, d[2], d[3], f'Duty point {d[0]}')
x = CX0 + cw + 14; pg.head(x, 92, 'PUMP EFFICIENCY η', cw)
E = pymupdf.Rect(x + 30, 112, x + cw - 6, 112 + 190); p = pg.p
p.draw_rect(E, color=None, fill=PLOT)
qmax, emax = 80, 80
EX = lambda q: E.x0 + E.width * q / qmax; EY = lambda e: E.y1 - E.height * e / emax
for e in range(0, 81, 20):
    p.draw_line((E.x0, EY(e)), (E.x1, EY(e)), color=LINE, width=0.4); pg.txt(E.x0 - 4, EY(e) + 3, str(e), 7.5, False, GREY, 'r')
for q in range(0, 81, 20):
    p.draw_line((EX(q), E.y0), (EX(q), E.y1), color=LINE, width=0.4); pg.txt(EX(q), E.y1 + 11, str(q), 7.5, False, GREY, 'c')
pg.txt(E.x0 + E.width / 2, E.y1 + 23, 'Q (m³/h)', 8, True, DARK, 'c'); pg.txt(x, E.y0 - 4, 'η (%)', 8, True, DARK)
from scipy.interpolate import PchipInterpolator
fe = PchipInterpolator([a for a, b in ETA], [b for a, b in ETA]); qd = np.linspace(0, ETA[-1][0], 200)
pts = [pymupdf.Point(EX(a), EY(float(fe(a)))) for a in qd]
p.draw_polyline(pts, color=RED, width=1.6)
for lab, m, q, h, e, r in DP:
    pt = pymupdf.Point(EX(q), EY(e)); p.draw_line((EX(q), EY(0)), pt, color=DARK, width=0.6, dashes='[2 2] 0')
    p.draw_circle(pt, 3, color=DARK, fill=WHITE, width=1.1)
pg.txt(E.x0 + 6, E.y0 + 12, f'Peak {DINH[1]:g} % at Q ≈ {float(DINH[2].split()[-2]):.0f} m³/h', 7.5, True, DARK)
y = pg.head(x, E.y1 + 46, 'DUTY POINTS', cw)
rows = [(m, f'{q} m³/h', f'{h:g} m', f'{e:g} %', f'{r[3]:g} kW / {r[4]:g} HP') for lab, m, q, h, e, r in DP]
y = pg.table(x, y - 6, ['Model', 'Q', 'H', 'η pump', 'P2'], rows, [64, 46, 40, 44, cw - 194], size=8)
for l in pg.wrap('H from the performance data table (6SP60-8 at 64 m³/h: read on the performance curve); η read on the pump efficiency curve of the 6SP60 range (pump only, without motor). '
                 'Curves at 50 Hz, 2 poles, n ≈ 2850 /min, clean water at 20 °C, kinematic viscosity 1 mm²/s. Typical values, not guaranteed.', 9, cw):
    y += 11.5; pg.txt(x, y + 2, l, 9, False, GREY)
assert y < 556, y

# ================= Trang 4: bảng thông số =================
pg = Pg('3', 'Performance data', 'Three-phase 3~ 380–415 V 50 Hz. Q in m³/h and l/min, H in m.')
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
y = pg.head(CX0, 92, 'PERFORMANCE DATA  ·  6SP60', CX1 - CX0)
pg.p.show_pdf_page(pymupdf.Rect(CX0, y - 4, CX0 + tr.width, y - 4 + tr.height), tb, 0)
yy = y - 4 + tr.height + 16
for l in pg.wrap('Curves on pages 2–3 are drawn as smooth curves through the table values (deviation ≤ ' + f'{max(LECH.values()):.1f}' +
                 ' %); maximum head (Q = 0) and the last point of each curve are kept exactly.', 9, CX1 - CX0):
    pg.txt(CX0, yy, l, 9, False, GREY); yy += 11.5
assert yy < 556, yy

# ================= Trang 5: kích thước =================
pg = Pg('4', 'Dimensions and motor data', 'Outlet 3 in. Dimensions in mm: P pump, M motor, T total length.')
y = pg.head(CX0, 92, 'DIMENSIONS  ·  6SP60  ·  OUTLET 3 in', 300)
y = pg.table(CX0, y - 6, ['Model', 'kW', 'HP', 'P (mm)', 'M (mm)', 'T (mm)'],
             [(k[0], f'{[r for r in MD if r[2] == k[0]][0][3]:g}', f'{[r for r in MD if r[2] == k[0]][0][4]:g}', k[1], k[2], k[3]) for k in KT], [70, 40, 40, 50, 50, 50], size=8, rh=13.5)
assert y < 556, y
x = CX0 + 330; w = CX1 - x
yy = pg.head(x, 92, 'MOTOR DATA', w)
yy = pg.table(x, yy - 6, ['Item', 'Value'], [('Power supply', '3~ 380–415 V 50 Hz'), ('Speed', 'n ≈ 2850 /min'), ('Start', 'Direct or star-delta'),
                                            ('Motor', 'Rewindable'), ('Outlet', '3 in'), ('Min. well diameter', '6 in')], [80, w - 80], size=8)
yy = pg.head(x, yy + 22, 'WORKING LIMITS', w); yy = pg.lst(x, yy, OPC, w)

canon = {}
for pg_ in doc:
    for f in pg_.get_fonts(full=True):
        if f[4] in ('LR', 'LB'): canon.setdefault(f[3].split('+')[-1], f[0])
for x_ in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: t_, v = doc.xref_get_key(x_, key)
        except Exception: continue
        if t_ != 'dict': continue
        def rep(mm):
            fx = int(mm.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{mm.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x_, key, nv)
doc.set_metadata({'title': 'REDPUMP - 6SP60 stainless steel submersible pumps', 'author': 'REDPUMP'}); doc.subset_fonts()
for x_ in range(1, doc.xref_length()):
    t_, v = doc.xref_get_key(x_, 'ToUnicode')
    if t_ == 'xref':
        sx = int(v.split()[0]); st = doc.xref_stream(sx); nst = st.replace(b'<2010>', b'<002D>').replace(b'<2219>', b'<00B7>')
        if nst != st: doc.update_stream(sx, nst)
doc.save(OUT, garbage=4, deflate=True)
print('saved', doc.page_count, os.path.getsize(OUT), {k: round(v) for k, v in PPI.items()}, DP)
