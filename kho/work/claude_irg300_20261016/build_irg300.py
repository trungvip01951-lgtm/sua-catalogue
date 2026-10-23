# -*- coding: utf-8 -*-
"""REDPUMP - Bơm trục đứng IRG 300IRG800-30-110 — catalogue riêng 1 trang A4 ngang 842x595 (16/10/2026).
Lệnh anh 16/10/2026 15:26: "làm cho a catalogue bơm 300IRG800-30-110 lưu lượng max 880m3/h áp max 35m hmin 21m
q min 600m3/h / làm cả đường đặc tính cho a nhé" + "làm redpump".
Số: IRG300.xlsx. Biểu đồ/bảng: tools/ve_duong_cong.py (qh/bieu_do.pdf, qh/bang.pdf). Chữ: REDPUMP - Bơm trục đứng IRG.pdf tr.1.
Ảnh: KHO_ANH/Bom_truc_dung_IRG/7e0835bfdec8.png (ĐẠT trong DANH_MUC). Giao diện: hồ sơ REDPUMP (cột tối trái, nhấn đỏ).
Dùng: python build_irg300.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, json, pymupdf, openpyxl
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HS = json.load(open(R + '/rules/HO_SO_HANG.json', encoding='utf-8'))['hang']['REDPUMP']['mau']
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
DARK, RED, BG = rgb(HS['chinh']), rgb(HS['nhan']), rgb(HS['nen'])
TXT, GREY, LIGHT, WHITE = rgb('2B2E33'), rgb('5E6166'), rgb('D9DADC'), (1, 1, 1)
W_, H_, CW, X0, MR = 842, 595, 245, 268, 808

wb = openpyxl.load_workbook(W + '/IRG300.xlsx', data_only=True)
M = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)][0]
MODEL, KW, HP, DN = M[2], M[3], M[4], M[10]
PTS = sorted((r[2], r[3]) for r in wb['QH'].iter_rows(min_row=2, values_only=True) if r[1] == MODEL)
def g(v): return '%g' % v
mm = re.match(r'(\d+)IRG(\d+)-(\d+)-(\d+)', MODEL); DN_, QR, HR, KW_ = mm.groups()
assert int(DN_) == DN and float(KW_) == KW
D = dict(PTS); QMIN, QMAX = 600, PTS[-1][0]; HQMIN, HQMAX = D[QMIN], D[QMAX]
assert (QMIN, HQMIN, QMAX, HQMAX) == (600, 35, 880, 21) and D[int(QR)] == int(HR)

doc = pymupdf.open(); p = doc.new_page(width=W_, height=H_)
p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
def t(x, y, s, size, bold=False, color=TXT, align='l'):
    w = FONT[bold].text_length(s, size)
    if align == 'r': x -= w
    elif align == 'c': x -= w / 2
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
def rect(r, fill, op=1): p.draw_rect(pymupdf.Rect(r), color=None, fill=fill, fill_opacity=op)
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
t(24, 46, 'IRG SERIES', 9, True, LIGHT); t(24, 84, f'{DN_}IRG', 40, True, WHITE)
for k, ln in enumerate(['Vertical single-suction', 'centrifugal pump']): t(24, 104 + k * 13, ln, 10, False, LIGHT)
rect((24, 128, 64, 131), RED)
# ảnh nền trắng: đặt trên ô trắng bo góc để không lộ mép ảnh trên nền tối
p.draw_rect(pymupdf.Rect(24, 142, CW - 24, 318), color=None, fill=WHITE, radius=0.04)
img((30, 146, CW - 30, 314), R + '/KHO_ANH/Bom_truc_dung_IRG/7e0835bfdec8.png')
y = head(24, 342, 'MAIN DATA', True)
rows = [('Model', MODEL), ('Power P2', f'{g(KW)} kW / {g(HP)} HP'), ('Power supply', '3~ 380–415 V 50 Hz'),
        ('Speed', 'n ≈ 1450 /min (4 poles)'), ('DN', f'{DN_}×{DN_} mm'), ('Rated point', f'{QR} m³/h – {HR} m'),
        ('Flow range', f'{g(QMIN)} – {g(QMAX)} m³/h'), ('Head range', f'{g(HQMIN)} – {g(HQMAX)} m')]
for a, b in rows: t(24, y, a, 8.5, False, LIGHT); t(24 + 82, y, b, 8.5, True, WHITE); y += 13.5
y = head(24, y + 12, 'PRODUCT NOMENCLATURE', True)
cells = [(DN_, 'Outlet', '(mm)'), ('IRG', 'Series', ''), (QR, 'Rated flow', '(m³/h)'), (HR, 'Rated head', '(m)'), (KW_, 'Power', '(kW)')]
for i, (a, b, c) in enumerate(cells):
    cx = 24 + 19 + i * 40
    t(cx, y + 6, a, 12, True, WHITE, 'c'); p.draw_line((cx - 17, y + 10), (cx + 17, y + 10), color=RED, width=0.6)
    t(cx, y + 19, b, 7, False, LIGHT, 'c'); t(cx, y + 27, c, 7, False, LIGHT, 'c')
t(24, 573, 'REDPUMP  /  IRG SERIES', 7.5, True, LIGHT)
t(MR, 573, '01 / 01', 7.5, False, GREY, 'r')

# ---- phải ----
img((MR - 120, 18, MR, 64), R + '/KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg')
t(X0, 40, 'VERTICAL CENTRIFUGAL PUMP', 16, True, DARK)
t(X0, 58, f'{MODEL}  |  {g(KW)} kW  |  3~ 380–415 V  |  50 Hz  |  n ≈ 1450 /min', 9, False, GREY)
y = head(X0, 86, 'PERFORMANCE CURVE')
CH = pymupdf.Rect(X0, y - 4, X0 + 540, y - 4 + 245)
qd = pymupdf.open(W + '/qh/bieu_do.pdf')
# toạ độ trục lấy từ nhãn vạch của chính biểu đồ
sp = [(s['text'].strip(), s['bbox']) for b in qd[0].get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans']]
yq = [bb for s, bb in sp if s.startswith('Q (m³')][0][1]
row = [(s, bb) for s, bb in sp if s.isdigit() and 0 < yq - bb[3] < 8]
qx = {int(s): (bb[0] + bb[2]) / 2 for s, bb in row}
hx = max(qx.values())
hy = {int(s): (bb[1] + bb[3]) / 2 for s, bb in sp if s.isdigit() and bb[0] > hx and bb[3] < yq - 12}
q1, h1 = max(qx), max(hy)
X = lambda q: CH.x0 + qx[0] + (qx[q1] - qx[0]) * q / q1
Y = lambda h: CH.y0 + hy[0] + (hy[h1] - hy[0]) * h / h1
# dải làm việc 600–880: nền đỏ rất nhạt dưới đường (vẽ trước biểu đồ? biểu đồ có nền -> vẽ sau, mờ)
p.show_pdf_page(CH, qd, 0)
rect((X(QMIN), Y(h1), X(QMAX), Y(0)), RED, 0.07)
for q in (QMIN, QMAX): p.draw_line((X(q), Y(h1)), (X(q), Y(0)), color=RED, width=0.5, dashes='[2 2] 0')
lab = 'Operating range'; lw = FONT[True].text_length(lab, 7.5); cx = (X(QMIN) + X(QMAX)) / 2
rect((cx - lw / 2 - 3, Y(h1) + 2.5, cx + lw / 2 + 3, Y(h1) + 13), WHITE); t(cx, Y(h1) + 10.5, lab, 7.5, True, RED, 'c')
pt = pymupdf.Point(X(int(QR)), Y(int(HR)))
p.draw_circle(pt, 3, color=RED, fill=WHITE, width=1.2)
lab = f'Rated point {QR} m³/h – {HR} m'; lw = FONT[True].text_length(lab, 7.5)
rect((pt.x - 10 - lw - 3, pt.y + 7, pt.x - 10 + 3, pt.y + 18), WHITE); t(pt.x - 10, pt.y + 15.5, lab, 7.5, True, RED, 'r')
y = head(X0, CH.y1 + 20, 'PERFORMANCE TABLE')
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
TB = pymupdf.Rect(X0, y - 4, X0 + tr.width, y - 4 + tr.height); p.show_pdf_page(TB, tb, 0)

# ---- ba cột dưới (chữ theo REDPUMP - Bơm trục đứng IRG.pdf tr.1) ----
y0 = TB.y1 + 28
C1, C2, C3 = (X0, 182), (X0 + 196, 140), (X0 + 350, MR - X0 - 350)
y = head(C1[0], y0, 'FEATURES')
feats = [('Vertical design', 'Suitable for any installation.'),
         ('Anti-corrosion coating', 'On the pump casing.'),
         ('Quality bearings', 'Wear-resistant mechanical seal.'),
         ('Explosion-proof motor', 'Available on request.')]
for a, b in feats:
    rect((C1[0], y - 7, C1[0] + 2.2, y + 1), RED); t(C1[0] + 7, y, a, 8, True, DARK); y += 10.5
    for ln in wrap(b, 9, C1[1] - 7): t(C1[0] + 7, y, ln, 9); y += 11
    y += 4
y = head(C2[0], y0, 'APPLICATIONS')
for s in ['Clean water', 'Civil', 'Industry']:
    p.draw_circle((C2[0] + 3, y - 2.8), 1.3, color=None, fill=RED); t(C2[0] + 9, y, s, 8); y += 11.5
y = head(C2[0], y + 10, 'MOTOR')
for s in ['Three-phase: 380–415 V / 50 Hz', '4 poles, n ≈ 1450 /min', 'Protection IP55, class F']:
    p.draw_circle((C2[0] + 3, y - 2.8), 1.3, color=None, fill=RED); t(C2[0] + 9, y, s, 8); y += 11.5
y = head(C3[0], y0, 'MATERIALS')
mat = [('Pump casing', 'Cast iron'), ('Impeller', 'SS304 / Cast iron'), ('Shaft', 'SS304 – 45# Steel'),
       ('Mechanical seal', 'SiC / Carbon / SS304'), ('Connection', 'Cast iron'), ('Bearing', 'Ball bearing'),
       ('Water deflector', 'Rubber')]
y -= 8
for i, (a, b) in enumerate(mat):
    lines = wrap(b, 7.8, C3[1] - 92); h = 4 + 10 * len(lines)
    if i % 2 == 0: rect((C3[0], y, MR, y + h), BG)
    t(C3[0] + 4, y + 9.5, a, 7.8, True, DARK)
    for k, ln in enumerate(lines): t(C3[0] + 90, y + 9.5 + 10 * k, ln, 7.8)
    y += h
p.draw_line((C3[0], y), (MR, y), color=LIGHT, width=0.5)
assert y < 562, y

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
doc.set_metadata({'title': f'REDPUMP - IRG SERIES {MODEL}', 'author': 'REDPUMP'})
doc.subset_fonts(); doc.save(OUT, garbage=4, deflate=True)
print('saved', OUT, os.path.getsize(OUT), 'rated', round(pt.x, 1), round(pt.y, 1), 'ticks', sorted(qx), sorted(hy), 'ybot', round(y, 1))
