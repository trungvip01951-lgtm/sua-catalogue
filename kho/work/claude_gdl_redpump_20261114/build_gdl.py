# -*- coding: utf-8 -*-
"""REDPUMP 50GDL18-15×9 — catalogue riêng 1 trang A4 ngang (14/11/2026, phiên CLAUDE_20261114, QĐ 180).
Số: GDL.xlsx (mk_xlsx.py) theo báo giá; mức giữa SUY RA. Giao diện REDPUMP (như 6SP60/TKP). Chưa có ảnh GDL trong kho — trang không có ảnh.
Không ghi vật liệu, kích thước, dòng điện, NPSH, hiệu suất (chưa có nguồn). Dùng: python build_gdl.py <gốc kho> <thư mục làm> <tệp ra>"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT = sys.argv[1:4]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
DARK, RED, GREY, TXT, WHITE, LINE = rgb('2B2E33'), rgb('A31A1F'), rgb('6B6F75'), rgb('222428'), (1, 1, 1), rgb('D9D4D1')
LIGHT, PINK = rgb('C9CDD2'), rgb('E8767B')
LOGO = R + '/KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg'
W_, H_ = 842, 595; COL = 238; CX0, CX1 = COL + 26, W_ - 34
wb = openpyxl.load_workbook(W + '/GDL.xlsx', data_only=True)
md = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)][0]
QH = {r[2]: r[3] for r in wb['QH'].iter_rows(min_row=2, values_only=True)}
MOD = md[2]; QD, HD = map(float, re.search(r'điểm làm việc ([\d.]+) m³/h – ([\d.]+) m', md[11]).groups())
Q1 = max(QH); H0, H1 = QH[0], QH[Q1]
assert MOD == '50GDL18-15×9' and (QD, HD) == (18, 135) and QH[QD] == HD and (H0, Q1, H1) == (172.29, 22.56, 112.12)
fs = lambda v: f'{v:g}'.replace('.', '.')
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
def head(x, y, s, w, color=DARK, line=RED):
    txt(x, y, s, 10, True, color); p.draw_line((x, y + 5), (x + w, y + 5), color=line, width=1.2); return y + 19

# ---- cột tối
p.draw_rect(pymupdf.Rect(0, 0, COL, H_), color=None, fill=DARK); p.draw_rect(pymupdf.Rect(COL - 5, 0, COL, H_), color=None, fill=RED)
txt(28, 56, 'GDL SERIES  ·  VERTICAL MULTISTAGE PUMP', 9, True, LIGHT)
txt(28, 100, MOD, 24, True, PINK)
y = 124
for l in wrap('Vertical multistage centrifugal pump, 9 stages, in-line suction and discharge.', 9.5, COL - 56): txt(28, y, l, 9.5, False, LIGHT); y += 13
y += 18; y = head(28, y, 'MAIN DATA', COL - 56, WHITE) + 2
for a, b in [('Power P2', f'{md[3]:g} kW / {md[4]} HP'), ('Duty point', f'{QD:g} m³/h – {HD:g} m'), ('Flow range', f'0 – {Q1:g} m³/h'),
             ('Head range', f'{H0:g} – {H1:g} m'), ('Suction / discharge', 'DN50 / DN50'), ('Speed', 'n ≈ 2930 /min (2 poles)'),
             ('Stages', '9'), ('Power supply', '3~ 380–415 V 50 Hz')]:
    txt(28, y, a, 8, True, LIGHT); txt(116, y, b, 9, True, WHITE); y += 16
y += 16; y = head(28, y, 'MODEL CODE', COL - 56, WHITE) + 4
for c, d in [('50', 'Suction / discharge size (mm)'), ('GDL', 'Series'), ('18', 'Rated flow (m³/h)'), ('15', 'Head per stage (m)'), ('×9', 'Number of stages')]:
    txt(28, y, c, 11, True, PINK); txt(68, y, d, 9, False, WHITE); y += 15
assert y < 560, y

# ---- phải
pix = pymupdf.Pixmap(LOGO); k = min(104 / pix.width, 46 / pix.height)
p.insert_image(pymupdf.Rect(CX1 - pix.width * k, 18, CX1, 18 + pix.height * k), filename=LOGO)
txt(CX0, 44, 'VERTICAL MULTISTAGE CENTRIFUGAL PUMP', 16, True, DARK)
txt(CX0, 62, f'{MOD}  ·  11 kW  ·  3~ 380–415 V 50 Hz  ·  n ≈ 2930 /min', 9.5, True, RED)
head(CX0, 88, 'PERFORMANCE CURVE', CX1 - CX0)
CR = pymupdf.Rect(CX0, 102, CX1, 102 + 250)
bd = pymupdf.open(W + '/qh/bd.pdf'); p.show_pdf_page(CR, bd, 0); bp = bd[0]; sc = CR.width / bp.rect.width
nen = max([d['rect'] for d in bp.get_drawings() if d.get('fill') and all(abs(c - 0xF4 / 255) < 0.01 for c in d['fill'][:3])], key=lambda r: r.width * r.height)
sp = [(s['text'].strip(), pymupdf.Rect(s['bbox'])) for b in bp.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']]
num = lambda t: re.fullmatch(r'\d+(\.\d+)?', t)
q1 = max(float(t) for t, r in sp if num(t) and nen.y1 < r.y0 < nen.y1 + 14); h1 = max(float(t) for t, r in sp if num(t) and r.x0 > nen.x1)
X = lambda q: CR.x0 + (nen.x0 + nen.width * q / q1) * sc; Y = lambda h: CR.y0 + (nen.y1 - nen.height * h / h1) * sc
pt = pymupdf.Point(X(QD), Y(HD)); lab = f'Duty point {QD:g} m³/h – {HD:g} m'
p.draw_line((X(QD), Y(0)), pt, color=RED, width=0.6, dashes='[2 2] 0'); p.draw_line((X(0), Y(HD)), pt, color=RED, width=0.6, dashes='[2 2] 0')
p.draw_circle(pt, 3.4, color=DARK, fill=WHITE, width=1.1)
w = FONT[True].text_length(lab, 8); bx = pymupdf.Rect(pt.x - w - 12, pt.y + 7, pt.x - 4, pt.y + 19)
p.draw_rect(bx, color=DARK, fill=WHITE, width=0.5); txt(bx.x0 + 4, bx.y1 - 3, lab, 8, True, DARK)
y = head(CX0, 372, 'PERFORMANCE DATA', CX1 - CX0)
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
p.show_pdf_page(pymupdf.Rect(CX0, y - 6, CX0 + tr.width, y - 6 + tr.height), tb, 0); y += tr.height + 8
for l in wrap(f'Flow range 0 – {Q1:g} m³/h and duty point {QD:g} m³/h – {HD:g} m as stated in the quotation; other head values are read on the performance curve.', 9, CX1 - CX0):
    txt(CX0, y, l, 9, False, GREY); y += 12
y += 14; xa, wa = CX0, 250; ya = head(xa, y, 'APPLICATIONS', wa)
for s in ['Water supply and pressure boosting for high-rise buildings', 'Industrial water transfer and circulation', 'Irrigation and water distribution systems']:
    p.draw_circle((xa + 2.5, ya - 3), 1.3, color=None, fill=RED); txt(xa + 9, ya, s, 9); ya += 12
xb = CX0 + 280; yb = head(xb, y, 'DESIGN', CX1 - xb)
for s in ['Vertical multistage design, 9 stages', 'Suction and discharge on the same axis (in-line)', 'Two-pole motor, n ≈ 2930 /min']:
    p.draw_circle((xb + 2.5, yb - 3), 1.3, color=None, fill=RED); txt(xb + 9, yb, s, 9); yb += 12
assert max(ya, yb) < 560, (ya, yb)
p.draw_line((CX0, 566), (CX1, 566), color=LINE, width=0.5); txt(CX0, 580, 'REDPUMP  /  GDL SERIES', 7.5, True, GREY); txt(CX1, 580, '01 / 01', 7.5, True, GREY, 'r')
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
doc.set_metadata({'title': 'REDPUMP - 50GDL18-15x9 vertical multistage pump', 'author': 'REDPUMP'}); doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True); print('saved', OUT, os.path.getsize(OUT))
