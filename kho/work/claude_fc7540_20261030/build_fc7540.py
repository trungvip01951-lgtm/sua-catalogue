# -*- coding: utf-8 -*-
"""PEROTAC FC 75/40M + FC 75/40T — catalogue riêng 2 trang A4 ngang (30/10/2026, phiên CLAUDE_20261030T0100Z).
Lệnh anh: báo giá BG-27102026-010 (FS75/40M, 18 m³/h, 9.5 m, 0.55 kW 1 pha) + "Làm a catalogue con này cho a nhé nước thải toàn thân inox".
Số: FC75_40.xlsx (mk_xlsx.py). Chữ, bảng điện/kích thước: lấy bằng mã từ CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm chìm nước thải FC.pdf.
Ảnh: KHO_ANH/Bom_chim_nuoc_thai_FS/9c78c4b6e782.png (ảnh FC đã duyệt), 8849ae05ad42.jpeg (hình kích thước). Mẫu bố cục: build_bg27.py.
Dùng: python build_fc7540.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT = sys.argv[1:4]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
NAVY, BLUE, TXT, GREY, BAND = rgb('13334D'), rgb('1A669E'), rgb('1F3847'), rgb('5C6E78'), rgb('EDF5FA')
ROW = BAND; WHITE = (1, 1, 1); LINE = rgb('C9D6DE')
W_, H_ = 842, 595; ML = 34; MR = W_ - 34
K = R + '/KHO_ANH/'
DD = R + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm chìm nước thải FC.pdf'
d0 = pymupdf.open(DD); L1 = [s.strip() for s in d0[0].get_text().splitlines() if s.strip()]; L2 = [s.strip() for s in d0[1].get_text().splitlines() if s.strip()]
def khoi(L, a, b): i = L.index(a); return L[i + 1:L.index(b, i + 1)]
SUB = [s for s in L1 if s.startswith('AISI 304 submersible electric pumps')][0]
USES = ' '.join(khoi(L2, 'USES', 'CONSTRUCTION'))
CONS = ' '.join(khoi(L2, 'CONSTRUCTION', 'ELECTRIC MOTOR'))
MOTOR = ' '.join(khoi(L2, 'ELECTRIC MOTOR', 'ELECTRICAL DATA AND DIMENSIONS'))
assert 'Power range: 0.55 kW to 2.2 kW.' in MOTOR
MOTOR = MOTOR.replace('Power range: 0.55 kW to 2.2 kW.', 'Power: 0.55 kW.')
i = L2.index('FC 75/40 M-T'); ED = L2[i + 1:i + 15]
assert ED[:5] == ['3.6', '1.3', '16', '3x1', '4x1'] and ED[11] == 'Ø 38', ED
IMP = [s for s in L2 if s.startswith('Impeller:')][0]
AVG = ' '.join(L2[L2.index(IMP) + 1:])[:200]
AVG = [s for s in L2 if s.startswith('Table values are averages')][0]
wb = openpyxl.load_workbook(W + '/FC75_40.xlsx', data_only=True)
m = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)][0]
pts = sorted((r[2], r[3]) for r in wb['QH'].iter_rows(min_row=2, values_only=True))
assert m[1] == 'FC 75/40M' and m[2] == 'FC 75/40T' and m[3] == 0.55 and pts[0] == (0, 9.5) and pts[-1] == (18, 2)

doc = pymupdf.open(); FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def trang(sub, so):
    p = doc.new_page(width=W_, height=H_); p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
    def txt(x, y, s, size, bold=False, color=TXT, align='l'):
        w = FONT[bold].text_length(s, size)
        if align == 'r': x -= w
        elif align == 'c': x -= w / 2
        p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
    p.draw_rect(pymupdf.Rect(200, 0, W_, 64), color=None, fill=BAND)
    pix = pymupdf.Pixmap(K + 'Bom_chim_nuoc_thai_FC_inox/f05538b98e09.jpeg'); k = min(150 / pix.width, 44 / pix.height)
    p.insert_image(pymupdf.Rect(ML, 10, ML + pix.width * k, 10 + pix.height * k), filename=K + 'Bom_chim_nuoc_thai_FC_inox/f05538b98e09.jpeg')
    txt(214, 44, 'FC 75/40', 26, True, NAVY)
    txt(MR, 30, sub, 11, True, NAVY, 'r'); txt(MR, 46, SUB, 9, False, TXT, 'r')
    p.draw_line((0, 64), (W_, 64), color=BLUE, width=1); p.draw_line((ML, 562), (MR, 562), color=LINE, width=0.5)
    txt(ML, 576, 'PEROTAC  /  FC SERIES', 7.5, True, GREY); txt(MR, 576, so, 7.5, False, GREY, 'r')
    return p, txt
def wrap(t, size, width, bold=False):
    out, cur = [], ''
    for w in t.split():
        c = (cur + ' ' + w).strip()
        if FONT[bold].text_length(c, size) <= width: cur = c
        else: out.append(cur); cur = w
    return out + [cur]
PPI = {}
# ---- trang 1
p, txt = trang('FC SERIES  /  PERFORMANCE DATA', '01 / 02')
def head(x, y, s, w): txt(x, y, s, 9.5, True, BLUE); p.draw_line((x, y + 4), (x + w, y + 4), color=BLUE, width=0.6)
LW = 230; y = 86; head(ML, y, 'MAIN DATA', LW); y += 16
rows = [('Model 1~', m[1]), ('Model 3~', m[2]), ('Power P2', f'{m[3]:g} kW / {m[4]:g} HP'), ('Power supply 1~', '1~ 220–240 V 50 Hz'),
        ('Power supply 3~', '3~ 380–415 V 50 Hz'), ('Speed', 'n ≈ 2850 /min'), ('Max. flow rate', f'{pts[-1][0]:g} m³/h'), ('Max. head', f'{pts[0][1]:g} m'),
        ('Solids passage', ED[11]), ('Rated current', f'1~ {ED[0]} A  ·  3~ {ED[1]} A'), ('Capacitor (1~)', f'{ED[2]} µF'), ('Cable', f'{ED[5]} m')]
for i_, (a, b) in enumerate(rows):
    if i_ % 2 == 0: p.draw_rect(pymupdf.Rect(ML, y - 9, ML + LW, y + 3.5), color=None, fill=ROW)
    txt(ML + 4, y, a, 8.5, True); txt(ML + 96, y, b, 8.5, i_ < 2, NAVY if i_ < 2 else TXT); y += 12.5
head(ML, y + 10, 'MATERIALS', LW); y += 26
MAT = [c.strip().rstrip('.') + '.' for c in CONS.split('. ') if 'AISI 304' in c or c.startswith('Mechanical seal')]
assert len(MAT) == 2, MAT
for c_ in MAT:
    for l in wrap(c_, 9, LW): txt(ML, y, l, 9); y += 11.5
txt(ML, y + 4, IMP, 9); y += 16
# ảnh giữa
MX0, MX1 = 280, 456
pix = pymupdf.Pixmap(K + 'Bom_chim_nuoc_thai_FS/9c78c4b6e782.png'); bh = 190; bw = pix.width * bh / pix.height
rr = pymupdf.Rect((MX0 + MX1 - bw) / 2, 82, (MX0 + MX1 + bw) / 2, 82 + bh); p.insert_image(rr, filename=K + 'Bom_chim_nuoc_thai_FS/9c78c4b6e782.png'); PPI['anh'] = pix.width / rr.width * 72
y2 = 300; head(MX0, y2, 'USES', MX1 - MX0); y2 += 16
for l in wrap(USES.split('Using the pump')[0].strip(), 9, MX1 - MX0): txt(MX0, y2, l, 9); y2 += 11.5
# biểu đồ + bảng
CH = pymupdf.Rect(470, 78, MR, 78 + 338 * 380 / 330); p.show_pdf_page(CH, pymupdf.open(W + '/qh/bieu_do.pdf'), 0)
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect; TY = 556 - tr.height - 10
assert y < TY - 4 and y2 < TY - 4, (y, y2, TY)
head(ML, TY - 2, 'PERFORMANCE DATA', MR - ML); p.show_pdf_page(pymupdf.Rect(ML, TY + 8, ML + tr.width, TY + 8 + tr.height), tb, 0)
# ---- trang 2
p, txt = trang('FC SERIES  /  TECHNICAL DESCRIPTION', '02 / 02')
CW = (MR - ML - 2 * 20) / 3; xs = [ML, ML + CW + 20, ML + 2 * (CW + 20)]
for x, (t, s) in zip(xs, [('USES', USES), ('CONSTRUCTION', CONS), ('ELECTRIC MOTOR', MOTOR)]):
    head(x, 88, t, CW); yy = 104
    for l in wrap(s, 9, CW): txt(x, yy, l, 9); yy += 11.5
    YM = max(globals().get('YM', 0), yy)
YT = YM + 18
head(ML, YT, 'ELECTRICAL DATA AND DIMENSIONS', MR - ML)
hd = ['MODEL', 'I 1~ (A)', 'I 3~ (A)', 'µF', '1~ mm²', '3~ mm²', 'Cable m', 'A', 'C', 'D', 'E', 'F', 'Solids']
vals = ['FC 75/40 M-T'] + ED[:12]
wc = [86] + [36] * 12; x = ML; yy = YT + 10
p.draw_rect(pymupdf.Rect(ML, yy, ML + sum(wc), yy + 15), color=None, fill=NAVY)
for h, w in zip(hd, wc): txt(x + w / 2, yy + 10.5, h, 7.5, True, WHITE, 'c'); x += w
yy += 15; x = ML; p.draw_rect(pymupdf.Rect(ML, yy, ML + sum(wc), yy + 15), color=LINE, fill=None, width=0.5)
for v, w in zip(vals, wc): txt(x + w / 2, yy + 10.5, v, 8, v == vals[0], TXT, 'c'); p.draw_line((x, yy), (x, yy + 15), color=LINE, width=0.5); x += w
txt(ML, yy + 30, 'Dimensions in mm. ' + IMP, 9)
for i_, l in enumerate(wrap(AVG, 9, 460)): txt(ML, yy + 46 + i_ * 11.5, l, 9, False, GREY)
dpix = pymupdf.Pixmap(K + 'Bom_chim_nuoc_thai_FS/8849ae05ad42.jpeg'); dh = 552 - (yy + 22); dw = dpix.width * dh / dpix.height
if dw > MR - (ML + 472): dw = MR - (ML + 472); dh = dw * dpix.height / dpix.width
r2 = pymupdf.Rect(MR - dw, 552 - dh, MR, 552); p.insert_image(r2, filename=K + 'Bom_chim_nuoc_thai_FS/8849ae05ad42.jpeg'); PPI['kt'] = dpix.width / dw * 72
assert r2.y0 > yy + 15 and r2.x0 > ML + 460 + 6, r2
canon = {}
for pg in doc:
    for f in pg.get_fonts(full=True):
        if f[4] in ('LR', 'LB'): canon.setdefault(f[3].split('+')[-1], f[0])
for x in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: t_, v = doc.xref_get_key(x, key)
        except Exception: continue
        if t_ != 'dict': continue
        def rep(mm):
            fx = int(mm.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{mm.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x, key, nv)
doc.set_metadata({'title': 'PEROTAC - FC SERIES FC 75/40', 'author': 'PEROTAC'}); doc.subset_fonts()
for x in range(1, doc.xref_length()):
    t_, v = doc.xref_get_key(x, 'ToUnicode')
    if t_ == 'xref':
        sx = int(v.split()[0]); st = doc.xref_stream(sx); nst = st.replace(b'<2010>', b'<002D>').replace(b'<2219>', b'<00B7>')
        if nst != st: doc.update_stream(sx, nst)
doc.save(OUT, garbage=4, deflate=True)
print('saved', os.path.getsize(OUT), {k: round(v) for k, v in PPI.items()}, 'y', round(y), round(y2), 'TY', round(TY))
