# -*- coding: utf-8 -*-
"""REDPUMP TKP600 / TKP800 — catalogue bơm tăng áp 1 trang A4 ngang (03/11/2026, phiên CLAUDE_20261103T0100Z, QĐ 172–173).
Số: TKP.xlsx (mk_xlsx.py) — Hmax, Qmax, điểm làm việc theo lời anh/báo giá; mức giữa SUY RA (parabol qua 3 điểm).
Ảnh: anh_tkp_redpump.png (ảnh anh gửi, đã xoá tem + logo SWIRLS, chữ REDPUMP). Giao diện REDPUMP như 6SP60.
Không ghi số cực, tốc độ, vật liệu, kích thước, dòng điện (chưa có nguồn).
Dùng: python build_tkp.py <gốc kho> <thư mục làm> <tệp ra>"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT = sys.argv[1:4]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
DARK, RED, GREY, TXT, WHITE, LINE = rgb('2B2E33'), rgb('A31A1F'), rgb('6B6F75'), rgb('222428'), (1, 1, 1), rgb('D9D4D1')
STRIPE, LIGHT = rgb('F1EEEC'), rgb('C9CDD2')
LOGO = R + '/KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg'; ANH = W + '/anh_tkp_redpump.png'
W_, H_ = 842, 595; COL = 238; CX0, CX1 = COL + 26, W_ - 34
wb = openpyxl.load_workbook(W + '/TKP.xlsx', data_only=True)
MD = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)]
QH = {}
for r in wb['QH'].iter_rows(min_row=2, values_only=True): QH.setdefault(r[1], {})[r[2]] = r[3]
INFO = {r[1]: dict(re.findall(r'(Hmax|Qmax) ([\d.]+)', r[11]), duty=re.search(r'điểm làm việc ([\d.]+) m³/h – ([\d.]+) m', r[11]).groups()) for r in MD}
assert [r[1] for r in MD] == ['TKP600', 'TKP800'] and INFO['TKP600']['duty'] == ('2', '20') and INFO['TKP800']['duty'] == ('3', '20')
assert all(QH[m][float(d[0])] == float(d[1]) for m, d in ((m, INFO[m]['duty']) for m in QH))

doc = pymupdf.open(); p = doc.new_page(width=W_, height=H_)
p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def txt(x, y, s, size, bold=False, color=TXT, align='l'):
    w = FONT[bold].text_length(s, size); x = x - w if align == 'r' else x - w / 2 if align == 'c' else x
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
def wrap(s, size, width, bold=False):
    out, cur = [], ''
    for w in s.split():
        c = (cur + ' ' + w).strip()
        if FONT[bold].text_length(c, size) <= width: cur = c
        else: out.append(cur); cur = w
    return out + [cur]
def head(x, y, s, w, color=DARK):
    txt(x, y, s, 10, True, color); p.draw_line((x, y + 5), (x + w, y + 5), color=RED, width=1.2); return y + 19

# ---- cột tối trái
p.draw_rect(pymupdf.Rect(0, 0, COL, H_), color=None, fill=DARK); p.draw_rect(pymupdf.Rect(COL - 5, 0, COL, H_), color=None, fill=RED)
txt(28, 60, 'TKP SERIES  ·  PRESSURE BOOSTER PUMPS', 9, True, LIGHT)
txt(28, 104, 'TKP600', 30, True, rgb('E8767B')); txt(28, 138, 'TKP800', 30, True, WHITE)
y = 166
for l in wrap('Single-phase pressure booster pumps for domestic water supply.', 9.5, COL - 56): txt(28, y, l, 9.5, False, LIGHT); y += 13
y += 16
for a, b in [('Power P2', '0.4 / 0.6 kW'), ('Max. head', f"{INFO['TKP600']['Hmax']} / {INFO['TKP800']['Hmax']} m"),
             ('Max. flow', f"{INFO['TKP600']['Qmax']} / {INFO['TKP800']['Qmax']} m³/h"), ('Power supply', '1~ 220–240 V 50 Hz')]:
    txt(28, y, a, 8, True, LIGHT); txt(108, y, b, 9.5, True, WHITE); y += 17
y += 22; txt(28, y, 'APPLICATIONS', 10, True, WHITE); p.draw_line((28, y + 5), (COL - 28, y + 5), color=RED, width=1.2); y += 21
for s in ['Boosting tap pressure in houses and apartments', 'Supplying showers, water heaters and washing machines',
          'Raising pressure from roof tanks and mains supply', 'Garden watering']:
    for i, l in enumerate(wrap(s, 9, COL - 65)):
        if i == 0: p.draw_circle((30.5, y - 3), 1.3, color=None, fill=RED)
        txt(37, y, l, 9, False, WHITE); y += 12
    y += 3
assert y < 560, y

# ---- đầu trang phải: logo + tên
pix = pymupdf.Pixmap(LOGO); k = min(104 / pix.width, 46 / pix.height)
p.insert_image(pymupdf.Rect(CX1 - pix.width * k, 18, CX1, 18 + pix.height * k), filename=LOGO)
txt(CX0, 44, 'PRESSURE BOOSTER PUMPS', 16, True, DARK); txt(CX0, 62, 'TKP600  ·  TKP800  ·  1~ 220–240 V 50 Hz', 9.5, True, RED)

# ---- ảnh (≥ 300 ppi: 600 px → 144 pt)
pi = pymupdf.Pixmap(ANH); S = 144; rr = pymupdf.Rect(CX0 + 4, 92, CX0 + 4 + S, 92 + S)
p.insert_image(rr, filename=ANH); PPI = pi.width / S * 72

# ---- bảng thông số chính dưới ảnh
y = head(CX0, 262, 'MAIN DATA', 186)
rows = [(m, f'{r[3]:g} kW', f"{INFO[m]['duty'][0]} m³/h – {INFO[m]['duty'][1]} m") for m, r in ((r[1], r) for r in MD)]
wd = [56, 50, 80]; x = CX0
p.draw_rect(pymupdf.Rect(x, y - 6, x + sum(wd), y + 9), color=None, fill=DARK)
for h_, w in zip(['Model', 'P2', 'Duty point'], wd): txt(x + w / 2, y + 5, h_, 7.8, True, WHITE, 'c'); x += w
y += 9
for i, row in enumerate(rows):
    if i % 2: p.draw_rect(pymupdf.Rect(CX0, y, CX0 + sum(wd), y + 14), color=None, fill=STRIPE)
    x = CX0
    for j, (v, w) in enumerate(zip(row, wd)): txt(x + w / 2, y + 10, v, 8, j == 0, TXT, 'c'); x += w
    y += 14
p.draw_line((CX0, y), (CX0 + sum(wd), y), color=DARK, width=0.8)
y += 14
for l in wrap('Duty point: operating point stated in the quotation. Max. head at Q = 0; max. flow at H = 0.', 9, 186): txt(CX0, y, l, 9, False, GREY); y += 12
assert y < 400, y

# ---- biểu đồ phải + điểm làm việc
CR = pymupdf.Rect(CX1 - 330, 84, CX1, 84 + 280)
head(CR.x0, 84, 'PERFORMANCE CURVES', 330)
CR = pymupdf.Rect(CX1 - 330, 98, CX1, 98 + 280)
bd = pymupdf.open(W + '/qh/bd.pdf'); p.show_pdf_page(CR, bd, 0); bp = bd[0]; sc = CR.width / bp.rect.width
nen = max([d['rect'] for d in bp.get_drawings() if d.get('fill') and all(abs(c - 0xF4 / 255) < 0.01 for c in d['fill'][:3])], key=lambda r: r.width * r.height)
sp = [(s['text'].strip(), pymupdf.Rect(s['bbox'])) for b in bp.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']]
num = lambda t: re.fullmatch(r'\d+(\.\d+)?', t)
q1 = max(float(t) for t, r in sp if num(t) and nen.y1 < r.y0 < nen.y1 + 14); h1 = max(float(t) for t, r in sp if num(t) and r.x0 > nen.x1)
X = lambda q: CR.x0 + (nen.x0 + nen.width * q / q1) * sc; Y = lambda h: CR.y0 + (nen.y1 - nen.height * h / h1) * sc
for m in ('TKP600', 'TKP800'):
    q, h = map(float, INFO[m]['duty']); pt = pymupdf.Point(X(q), Y(h)); lab = f'{m}: {q:g} m³/h – {h:g} m'
    p.draw_line((X(q), Y(0)), pt, color=RED, width=0.6, dashes='[2 2] 0'); p.draw_circle(pt, 3.2, color=DARK, fill=WHITE, width=1.1)
    w = FONT[True].text_length(lab, 7.5)
    bx = pymupdf.Rect(pt.x - w - 10, pt.y + 5, pt.x - 4, pt.y + 15) if m == 'TKP600' else pymupdf.Rect(pt.x + 4, pt.y - 15, pt.x + w + 10, pt.y - 5)
    p.draw_rect(bx, color=DARK, fill=WHITE, width=0.5); txt(bx.x0 + 3, bx.y1 - 2.5, lab, 7.5, True, DARK)

# ---- bảng hiệu năng dưới
y = head(CX0, 410, 'PERFORMANCE DATA', CX1 - CX0)
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
p.show_pdf_page(pymupdf.Rect(CX0, y - 4, CX0 + tr.width, y - 4 + tr.height), tb, 0); y += tr.height + 8
for l in wrap('Head values between max. head, duty point and max. flow are read on the performance curve.', 9, CX1 - CX0): txt(CX0, y, l, 9, False, GREY); y += 12
assert y < 556, y
p.draw_line((CX0, 566), (CX1, 566), color=LINE, width=0.5); txt(CX0, 580, 'REDPUMP  /  TKP SERIES', 7.5, True, GREY)

canon = {}
for f in p.get_fonts(full=True):
    if f[4] in ('LR', 'LB'): canon[f[3].split('+')[-1]] = f[0]
for x in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: t, v = doc.xref_get_key(x, key)
        except Exception: continue
        if t != 'dict': continue
        def rep(mm):
            fx = int(mm.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{mm.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x, key, nv)
doc.set_metadata({'title': 'REDPUMP - TKP pressure booster pumps', 'author': 'REDPUMP'}); doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True); print('saved', OUT, os.path.getsize(OUT), 'ppi', round(PPI))
