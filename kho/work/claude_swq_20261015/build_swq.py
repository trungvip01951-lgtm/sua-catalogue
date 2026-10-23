# -*- coding: utf-8 -*-
"""REDPUMP - Bơm chìm nước thải SWQ 250SWQ500-5 — catalogue riêng 1 trang A4 ngang 842x595 (15/10/2026).
Lệnh anh 15/10/2026: catalogue con 250SWQ500-5 (báo giá BG-15102026-005), không cắt rác, Qmax 600 m³/h, Hmax 25 m,
ảnh đại diện = ảnh con cắt rác WC 30 kW (KHO_ANH/Bom_cat_rac_WC/d78acefb2b87.jpeg); chỉ REDPUMP.
Số: SWQ.xlsx (SUY RA theo QĐ anh 16:14). Biểu đồ/bảng: tools/ve_duong_cong.py (qh/bieu_do.pdf, qh/bang.pdf).
Giao diện: hồ sơ REDPUMP (cột tối trái, nhấn đỏ) như REDPUMP SF/WC.
Dùng: python build_swq.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, json, io, pymupdf, openpyxl
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HS = json.load(open(R + '/rules/HO_SO_HANG.json', encoding='utf-8'))['hang']['REDPUMP']['mau']
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
DARK, RED, BG = rgb(HS['chinh']), rgb(HS['nhan']), rgb(HS['nen'])
TXT, GREY, LIGHT, WHITE, PINK = rgb('2B2E33'), rgb('5E6166'), rgb('D9DADC'), (1, 1, 1), rgb('E8A3A5')
W_, H_, CW, X0, MR = 842, 595, 245, 268, 808

# ---- số liệu: đọc SWQ.xlsx, không gõ lại ----
wb = openpyxl.load_workbook(W + '/SWQ.xlsx', data_only=True)
M = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)][0]
MODEL, KW, HP, DN = M[2], M[3], M[4], M[10]
PTS = sorted((r[2], r[3]) for r in wb['QH'].iter_rows(min_row=2, values_only=True) if r[1] == MODEL)
def g(v): return '%g' % v
QMAX, HMAX = PTS[-1][0], PTS[0][1]
mm = re.match(r'(\d+)SWQ(\d+)-(\d+)', MODEL); DN_, QR, HR = mm.groups()
assert int(DN_) == DN

doc = pymupdf.open(); p = doc.new_page(width=W_, height=H_)
p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
def t(x, y, s, size, bold=False, color=TXT, align='l'):
    w = FONT[bold].text_length(s, size)
    if align == 'r': x -= w
    elif align == 'c': x -= w / 2
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
def rect(r, fill): p.draw_rect(pymupdf.Rect(r), color=None, fill=fill)
def wrap(s, size, width, bold=False):
    out, cur = [], ''
    for w in s.split():
        c = (cur + ' ' + w).strip()
        if FONT[bold].text_length(c, size) <= width: cur = c
        else: out.append(cur); cur = w
    return out + [cur]
def img(r, path):
    pix = pymupdf.Pixmap(path); r = pymupdf.Rect(r); s = min(r.width / pix.width, r.height / pix.height)
    w, h = pix.width * s, pix.height * s; x0, y0 = r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2
    rr = pymupdf.Rect(x0, y0, x0 + w, y0 + h); p.insert_image(rr, filename=path); return rr
def head(x, y, s, dark=False):
    rect((x, y - 8.5, x + 3, y + 1.5), RED); t(x + 8, y, s, 9.5, True, WHITE if dark else DARK); return y + 16

# ---- cột tối trái ----
rect((0, 0, CW, H_), DARK)
t(24, 46, 'SWQ SERIES', 9, True, LIGHT); t(24, 84, f'{DN_}SWQ', 40, True, WHITE)
for k, ln in enumerate(['Submersible sewage pump', 'Without cutter  ·  Large flow']): t(24, 104 + k * 13, ln, 10, False, LIGHT)
rect((24, 128, 64, 131), RED)
img((24, 142, CW - 24, 318), R + '/KHO_ANH/Bom_cat_rac_WC/d78acefb2b87.jpeg')
y = head(24, 342, 'MAIN DATA', True)
rows = [('Model', MODEL), ('Power P2', f'{g(KW)} kW / {g(HP)} HP'), ('Power supply', '3~ 380–415 V 50 Hz'),
        ('Speed', 'n ≈ 1450 /min (4 poles)'), ('Discharge', f'DN{DN}'), ('Rated point', f'{QR} m³/h – {HR} m'),
        ('Max. flow rate', f'{g(QMAX)} m³/h'), ('Max. head', f'{g(HMAX)} m')]
for a, b in rows: t(24, y, a, 8.5, False, LIGHT); t(24 + 82, y, b, 8.5, True, WHITE); y += 13.5
y = head(24, y + 12, 'PRODUCT NOMENCLATURE', True)
cells = [(DN_, 'Outlet size', '(mm)'), ('SWQ', 'Model', ''), (QR, 'Rated flow', '(m³/h)'), (HR, 'Rated head', '(m)')]
for i, (a, b, c) in enumerate(cells):
    cx = 24 + 24 + i * 50
    t(cx, y + 6, a, 13, True, WHITE, 'c'); p.draw_line((cx - 20, y + 10), (cx + 20, y + 10), color=RED, width=0.6)
    t(cx, y + 19, b, 7, False, LIGHT, 'c'); t(cx, y + 27, c, 7, False, LIGHT, 'c')
t(24, 573, 'REDPUMP  /  SWQ SERIES', 7.5, True, LIGHT)
t(MR, 573, '01 / 01', 7.5, False, GREY, 'r')

# ---- phải ----
img((MR - 120, 18, MR, 64), R + '/KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg')
t(X0, 40, 'SUBMERSIBLE SEWAGE PUMP', 16, True, DARK)
t(X0, 58, f'{MODEL}  |  {g(KW)} kW  |  3~ 380–415 V  |  50 Hz  |  n ≈ 1450 /min', 9, False, GREY)
y = head(X0, 86, 'PERFORMANCE CURVE')
CH = pymupdf.Rect(X0, y - 4, X0 + 540, y - 4 + 245)
qd = pymupdf.open(W + '/qh/bieu_do.pdf'); p.show_pdf_page(CH, qd, 0)
# điểm làm việc: toạ độ trục lấy từ nhãn vạch của chính biểu đồ
sp = [(s['text'].strip(), s['bbox']) for b in qd[0].get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']]
yq = [bb for s, bb in sp if s.startswith('Q (m³')][0][1]
row = [(s, bb) for s, bb in sp if s.isdigit() and 0 < yq - bb[3] < 8]
qx = {s: (bb[0] + bb[2]) / 2 for s, bb in row}
hx = max(qx.values())
hy = {s: (bb[1] + bb[3]) / 2 for s, bb in sp if s.isdigit() and bb[0] > hx and bb[3] < yq - 12}
X = lambda q: CH.x0 + qx['0'] + (qx['500'] - qx['0']) * q / 500
Y = lambda h: CH.y0 + hy['0'] + (hy['25'] - hy['0']) * h / 25
pt = pymupdf.Point(X(int(QR)), Y(int(HR)))
p.draw_line((pt.x, Y(0)), (pt.x, pt.y), color=GREY, width=0.5, dashes='[2 2] 0')
p.draw_circle(pt, 3, color=RED, fill=WHITE, width=1.2)
lab = f'Rated point {QR} m³/h – {HR} m'; lw = FONT[True].text_length(lab, 7.5)
rect((pt.x - 10 - lw - 3, pt.y + 7, pt.x - 10 + 3, pt.y + 18), WHITE); t(pt.x - 10, pt.y + 15.5, lab, 7.5, True, RED, 'r')
y = head(X0, CH.y1 + 20, 'PERFORMANCE TABLE')
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
TB = pymupdf.Rect(X0, y - 4, X0 + tr.width, y - 4 + tr.height); p.show_pdf_page(TB, tb, 0)

# ---- ba cột dưới ----
y0 = TB.y1 + 26
C1, C2, C3 = (X0, 182), (X0 + 196, 140), (X0 + 350, MR - X0 - 350)
y = head(C1[0], y0, 'FEATURES')
feats = [('Non-clogging impeller', 'Open channel, without cutter.'),
         ('Double mechanical seal', 'Silicon carbide seal faces.'),
         ('Epoxy-sealed cable entry', 'Keeps moisture out of the motor.'),
         ('Dry motor, 100% copper winding', 'IP68, heavy-duty ball bearings.')]
for a, b in feats:
    rect((C1[0], y - 7, C1[0] + 2.2, y + 1), RED); t(C1[0] + 7, y, a, 8, True, DARK); y += 10.5
    for ln in wrap(b, 9, C1[1] - 7): t(C1[0] + 7, y, ln, 9); y += 11
    y += 4
y = head(C2[0], y0, 'APPLICATIONS')
for s in ['Sewage treatment plants', 'Industrial draining', 'Large-flow drainage, flood control', 'Agriculture irrigation']:
    p.draw_circle((C2[0] + 3, y - 2.8), 1.3, color=None, fill=RED); t(C2[0] + 9, y, s, 8); y += 11.5
y = head(C2[0], y + 10, 'OPERATING CONDITIONS')
for s in ['Max. fluid temperature +40 °C', 'Rewindable motor', 'Three-phase: 380–415 V / 50 Hz']:
    p.draw_circle((C2[0] + 3, y - 2.8), 1.3, color=None, fill=RED); t(C2[0] + 9, y, s, 8); y += 11.5
y = head(C3[0], y0, 'MATERIALS')
mat = [('Pump casing', 'Cast-iron ASTM NO.30'), ('Impeller', 'Cast-iron ASTM NO.30'), ('Motor casing', 'Cast-iron ASTM NO.30'),
       ('Mechanical seal', 'Silicon carbide (SiC)'), ('Shaft', 'AISI 304 SS-ASTM 5140'),
       ('Seal lubricant oil', 'Oil for food machinery and pharmaceutical use')]
y -= 8
for i, (a, b) in enumerate(mat):
    lines = wrap(b, 7.8, C3[1] - 92); h = 6 + 10 * len(lines)
    if i % 2 == 0: rect((C3[0], y, MR, y + h), BG)
    t(C3[0] + 4, y + 10, a, 7.8, True, DARK)
    for k, ln in enumerate(lines): t(C3[0] + 90, y + 10 + 10 * k, ln, 7.8)
    y += h
p.draw_line((C3[0], y), (MR, y), color=LIGHT, width=0.5)

# ---- gộp phông khối chèn về phông trang ----
canon = {}
for f in p.get_fonts(full=True):
    if f[4] in ('LR', 'LB'): canon[f[3].split('+')[-1]] = f[0]
for x in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: tt, v = doc.xref_get_key(x, key)
        except Exception: continue
        if tt != 'dict': continue
        def rep(m):
            fx = int(m.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{m.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x, key, nv)
doc.set_metadata({'title': f'REDPUMP - SWQ SERIES {MODEL}', 'author': 'REDPUMP'})
doc.subset_fonts(); doc.save(OUT, garbage=4, deflate=True)
print('saved', OUT, os.path.getsize(OUT), 'rated', round(pt.x, 1), round(pt.y, 1))
