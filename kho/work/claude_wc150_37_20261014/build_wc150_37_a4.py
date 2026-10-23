# -*- coding: utf-8 -*-
"""PEROTAC - Bơm cắt rác WC 150WC300-30-37 — catalogue riêng 2 trang, A4 ngang 842x595.
Dựng mới theo rules/HO_SO_HANG (PEROTAC) + nội dung chữ lấy từ ứng viên 01 (13/10, A3) đã chép từ bản đã duyệt.
Biểu đồ + bảng: tools/ve_duong_cong.py (qh_bieu_do.pdf, qh_bang.pdf) từ WC150_37.xlsx.
Dùng: python build_wc150_37_a4.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, pymupdf
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
UV1 = R + '/work/claude_wc150_37_20261013/PEROTAC - Bơm cắt rác WC 150WC300-30-37 (UNG VIEN 01).pdf'
FR = R + '/vendor/fonts/LiberationSans-Regular.ttf'
FB = R + '/vendor/fonts/LiberationSans-Bold.ttf'

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
NAVY, BLUE, TXT, GREY, BAND = rgb('13334D'), rgb('1A669E'), rgb('1F3847'), rgb('5C6E78'), rgb('EDF5FA')
ROW = rgb('EDF5FA'); WHITE = (1, 1, 1)
W_, H_ = 842, 595; ML = 34; MR = W_ - 34

src = pymupdf.open(UV1)
def ximg(xref):
    pix = pymupdf.Pixmap(src, xref)
    if pix.alpha or pix.n > 3: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return pix.tobytes('png'), pix.width, pix.height
LOGO, CUT2, PHOTO = ximg(16), ximg(14), ximg(29)

doc = pymupdf.open()

def fonts(p):
    p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)

def txt(p, x, y, s, size, bold=False, color=TXT, align='l'):
    f = pymupdf.Font(fontfile=FB if bold else FR)
    w = f.text_length(s, size)
    if align == 'r': x -= w
    elif align == 'c': x -= w / 2
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color)
    return w

def wrap(t, size, width):
    f = pymupdf.Font(fontfile=FR); out, cur = [], ''
    for w in t.split():
        c = (cur + ' ' + w).strip()
        if f.text_length(c, size) <= width: cur = c
        else: out.append(cur); cur = w
    return out + [cur]

def heading(p, x, y, s, w):
    txt(p, x, y, s, 9.5, True, BLUE)
    p.draw_line((x, y + 4), (x + w, y + 4), color=BLUE, width=0.6)

def img(p, rect, im):
    data, iw, ih = im
    r = pymupdf.Rect(rect); s = min(r.width / iw, r.height / ih)
    w, h = iw * s, ih * s
    rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, 0, 0); rr.x1 = rr.x0 + w; rr.y1 = rr.y0 + h
    p.insert_image(rr, stream=data)
    return rr

def frame(p, big, title, sub, pg):
    p.draw_rect(pymupdf.Rect(200, 0, W_, 64), color=None, fill=BAND)
    img(p, (ML, 10, ML + 150, 54), LOGO)
    txt(p, 214, 44, big, 26, True, NAVY)
    txt(p, MR, 30, title, 11, True, NAVY, 'r')
    txt(p, MR, 46, sub, 9, False, TXT, 'r')
    p.draw_line((0, 64), (W_, 64), color=BLUE, width=1)
    p.draw_line((ML, 562), (MR, 562), color=rgb('C9D6DE'), width=0.5)
    txt(p, ML, 576, 'PEROTAC  /  WC SERIES', 7.5, True, GREY)
    txt(p, MR, 576, pg, 7.5, False, GREY, 'r')

# ---------------- Trang 1: cấu tạo + tính năng ----------------
p = doc.new_page(width=W_, height=H_); fonts(p)
frame(p, 'WC', 'WC SERIES  /  CONSTRUCTION & FEATURES', 'Submersible sewage pumps with cutter  |  50 Hz', '02 / 02')
heading(p, ML, 86, 'CONSTRUCTION  ·  150WC300-30-37 (2-POLE)', 300)
r = img(p, (ML, 96, ML + 300, 418), CUT2)
parts = ['Handle', 'Cable', 'Capacitor', 'Cap', 'Thermal protector', 'Stator', 'Rotor', 'Outlet',
         'Motor body', 'Mechanical seal', 'Screw', 'Elbow', 'Impeller', 'Pump body', 'Cutter ring', 'Base']
y0 = 432; rh = 13
for i, s in enumerate(parts):
    col, row = divmod(i, 8)
    x = ML + col * 150; y = y0 + row * rh
    if row % 2 == 0: p.draw_rect(pymupdf.Rect(x, y - 9.5, x + 146, y + 3.5), color=None, fill=ROW)
    txt(p, x + 13, y, str(i + 1), 8, True, BLUE, 'r'); txt(p, x + 20, y, s, 8)
txt(p, ML, y0 + 8 * rh + 4, 'Items 3 and 5: single-phase models only.', 9, False, GREY)

X2 = 372; WR = MR - X2
heading(p, X2, 86, 'FEATURES', WR)
feats = [('Cutter impeller with cutter ring', ['Vortex semi-open, non-clogging impeller. Solids in the wastewater are cut by the impeller and the',
          'cutter ring before being pumped out. Impeller and cutter ring are made of high-chromium stainless',
          'steel 420, hardness HRC 49–52, for good wear resistance.']),
         ('Double mechanical seal', ['Two mechanical seals arranged in series. Seal faces in silicon carbide for superior abrasion resistance',
          'and the best sealing effect.']),
         ('Epoxy-sealed cable entry', ['An epoxy resin seal at the cable base prevents moisture from entering the motor through the cable',
          'cores.']),
         ('Heavy-duty bearings', ['Heavy-duty ball bearings.']),
         ('Dry motor, 100% copper winding', ['Protection IP68, for continuous submerged operation in wastewater and sewage.'])]
y = 104
for t, lines in feats:
    p.draw_rect(pymupdf.Rect(X2, y - 8, X2 + 2.2, y + 1.5), color=None, fill=BLUE)
    txt(p, X2 + 8, y, t, 9, True, NAVY); y += 12
    for l in wrap(' '.join(lines), 9, WR - 8): txt(p, X2 + 8, y, l, 9); y += 11.5
    y += 5
heading(p, X2, y + 6, 'SPECIFICATIONS', WR); y += 16
spec = [('Liquid temperature', '0 – 40 °C'), ('Liquid', 'Wastewater, sewage'), ('Frequency', '50 Hz'),
        ('Power supply', '3~ 380–415 V 50 Hz'), ('Motor', 'Dry motor, 2-pole, n ≈ 2900 /min'), ('Protection', 'IP68'),
        ('Bearing', 'Ball type'), ('Mechanical seal', 'Double mechanical seal, silicon carbide'),
        ('Impeller', 'Vortex, non-clogging, with cutter ring')]
p.draw_rect(pymupdf.Rect(X2, y, MR, y + 14), color=None, fill=NAVY)
txt(p, X2 + 6, y + 10, 'ITEM', 7.8, True, WHITE); txt(p, X2 + 150, y + 10, '150WC300-30-37', 7.8, True, WHITE); y += 14
for i, (a, b) in enumerate(spec):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(X2, y, MR, y + 13), color=None, fill=ROW)
    txt(p, X2 + 6, y + 9.5, a, 8, True); txt(p, X2 + 150, y + 9.5, b, 8); y += 13
heading(p, X2, y + 18, 'APPLICATIONS', WR); y += 34
for s in ['Drainage of wastewater in rivers and wastewater treatment plants', 'Commercial buildings, industrial areas and amusement places',
          'Schools, hospitals, government buildings and parks', 'Chicken, cow, pig and fish farms, slaughterhouses']:
    p.draw_circle((X2 + 3, y - 3), 1.4, color=None, fill=BLUE); txt(p, X2 + 9, y, s, 9); y += 12

# ---------------- Trang 2: thông số + đường Q–H ----------------
p = doc.new_page(width=W_, height=H_); fonts(p)
frame(p, '150WC300-30-37', 'WC SERIES  /  PERFORMANCE & TECHNICAL DATA',
      'Submersible sewage pumps with cutter  |  50 Hz  |  n ≈ 2900 /min', '01 / 02')
LW = 210
heading(p, ML, 86, 'PRODUCT NOMENCLATURE', LW)
cells = [('150', 'Outlet size', '(mm)'), ('WC', 'Model', ''), ('300', 'Rated flow', '(m³/h)'), ('30', 'Rated head', '(m)'), ('37', 'Power', '(kW)')]
for i, (a, b, c) in enumerate(cells):
    cx = ML + 21 + i * 42
    txt(p, cx, 108, a, 12, True, NAVY, 'c')
    p.draw_line((cx - 17, 112), (cx + 17, 112), color=rgb('C9D6DE'), width=0.5)
    txt(p, cx, 121, b, 7, False, GREY, 'c'); txt(p, cx, 129, c, 7, False, GREY, 'c')
txt(p, ML, 141, 'WC: three-phase 3~', 7.5, False, TXT)
heading(p, ML, 160, 'MAIN DATA', LW)
rows = [('Power', '37 kW / 50 HP'), ('Power supply', '3~ 380–415 V 50 Hz'), ('Poles', '2'), ('Speed', 'n ≈ 2900 /min'),
        ('Discharge', 'DN150'), ('Rated point', '300 m³/h – 30 m'), ('Max. flow rate', '540 m³/h'), ('Max. head', '53 m')]
y = 176
for i, (a, b) in enumerate(rows):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(ML, y - 9, ML + LW, y + 3.5), color=None, fill=ROW)
    txt(p, ML + 4, y, a, 8.5, True); txt(p, ML + 92, y, b, 8.5); y += 12.5
heading(p, ML, y + 10, 'APPLICATIONS', LW); y += 26
for s in ['Sewage treatment plants', 'Industrial draining', 'Agriculture irrigation']: txt(p, ML, y, s, 9); y += 12
heading(p, ML, y + 8, 'OPERATING CONDITIONS', LW); y += 24
txt(p, ML, y, 'Maximum fluid temperature up to +40 °C', 9); y += 12
heading(p, ML, y + 8, 'MOTOR AND PUMP', LW); y += 24
for s in ['Rewindable motor', 'Three-phase: 380–415 V / 50 Hz', 'It can work in water containing fiber']: txt(p, ML, y, s, 9); y += 12

# giữa: ảnh + vật liệu
MX0, MX1 = 262, 452
img(p, (MX0 + 30, 80, MX1 - 30, 300), PHOTO)
mat = [('Diffuser', 'Cast-iron ASTM NO.30'), ('Impeller', 'AISI 420S45'), ('Motor external casing', 'Cast-iron ASTM NO.30'),
       ('Mechanical seal', 'Silicon carbide (SiC)'), ('Shaft', 'AISI 304 SS-ASTM 5140'), ('Seal lubricant oil', 'Oil for food machinery and pharmaceutical use')]
y = 316
p.draw_rect(pymupdf.Rect(MX0, y, MX1, y + 14), color=None, fill=NAVY)
txt(p, MX0 + 4, y + 10, 'COMPONENT', 7.5, True, WHITE); txt(p, MX0 + 92, y + 10, 'MATERIAL', 7.5, True, WHITE); y += 14
for i, (a, b) in enumerate(mat):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(MX0, y, MX1, y + 16), color=None, fill=ROW)
    txt(p, MX0 + 4, y + 10.5, a, 7, False);
    if pymupdf.Font(fontfile=FR).text_length(b, 7) > MX1 - MX0 - 96:
        txt(p, MX0 + 92, y + 6.8, 'Oil for food machinery and', 7); txt(p, MX0 + 92, y + 14, 'pharmaceutical use', 7)
    else: txt(p, MX0 + 92, y + 10.5, b, 7)
    y += 16

# phải: biểu đồ
CH = pymupdf.Rect(466, 78, MR, 450)
qd = pymupdf.open(W + '/qh_bieu_do.pdf')
p.show_pdf_page(CH, qd, 0)
# điểm định mức 300 m³/h – 30 m: lấy toạ độ trục từ nhãn vạch của chính biểu đồ
sp = [(sp['text'].strip(), sp['bbox']) for b in qd[0].get_text('dict')['blocks'] for l in b.get('lines', []) for sp in l['spans']]
yq = [bb for t, bb in sp if t.startswith('Q (m')][0][1]
qx = {t: (bb[0] + bb[2]) / 2 for t, bb in sp if abs(bb[1] - yq) < 2 and t.isdigit()}
xax = min(qx.values())
hy = {t: (bb[1] + bb[3]) / 2 for t, bb in sp if t.isdigit() and bb[2] < xax + 5 and bb[1] < yq - 5}
X = lambda q: CH.x0 + qx['0'] + (qx['300'] - qx['0']) * q / 300
Y = lambda h: CH.y0 + hy['0'] + (hy['30'] - hy['0']) * h / 30
pt = pymupdf.Point(X(300), Y(30))
p.draw_circle(pt, 3, color=NAVY, fill=WHITE, width=1)
txt(p, pt.x + 6, pt.y - 5, 'Rated point 300 m³/h – 30 m', 7.5, False, NAVY)
# bảng
heading(p, ML, 474, 'PERFORMANCE DATA', MR - ML)
tb = pymupdf.open(W + '/qh_bang.pdf'); tr = tb[0].rect
p.show_pdf_page(pymupdf.Rect(ML, 486, ML + tr.width, 486 + tr.height), tb, 0)

doc.move_page(1, 0)
# gộp phông: mọi tham chiếu phông cùng tên trong khối biểu đồ/bảng trỏ về một phông của trang
import re
canon = {}
for pg in doc:
    for f in pg.get_fonts(full=True):
        if f[4] in ('LR', 'LB'): canon[f[3].split('+')[-1]] = f[0]
for x in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: t, v = doc.xref_get_key(x, key)
        except Exception: continue
        if t != 'dict': continue
        def rep(m):
            fx = int(m.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{m.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x, key, nv)
doc.set_metadata({'title': 'PEROTAC - WC SERIES 150WC300-30-37', 'author': 'PEROTAC'})
doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True)
print('saved', OUT, os.path.getsize(OUT))
