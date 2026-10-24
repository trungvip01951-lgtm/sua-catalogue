# -*- coding: utf-8 -*-
"""AQUARIS CM 32-250/7.5 + CM 40-160/4 — catalogue riêng 1 trang A4 dọc 595x842 (24/10/2026, phiên CLAUDE_20261024T0100Z).
Lệnh anh: "Làm cho a catalogue aquaris cm 2 mã này nhé" (ảnh báo giá) + "Theo báo giá" + "Làm catalogue cho 2 mã này thôi song gửi a".
Số: CM2.xlsx (mk_xlsx.py). Bảng ngang (QĐ 160): qh/bang.pdf vẽ với --ho-so HO_SO_HANG_bang_ngang.json (AQUARIS bang.huong = model_theo_dong). Chữ: lấy bằng mã từ CATALOG SUA/CATALOGUE DA DUYET/AQUARIS/AQUARIS - Bơm trục ngang CM.pdf tr.3;
cánh bơm "Cast iron" theo báo giá ("Cánh quạt: Gang"). Ảnh KHO_ANH/Bom_truc_ngang_CM/29357a5db185.jpeg, logo 01e988048331.jpeg.
Dùng: python build_cm2.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FR, FB = R + '/vendor/fonts/Lato-Regular.ttf', R + '/vendor/fonts/Lato-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
GREEN, BG, TXT, MUTE, LINE = rgb('0D6159'), rgb('F0F7F5'), rgb('22302E'), rgb('5B6B68'), rgb('C8D8D4')
FL = [rgb('009246'), (1, 1, 1), rgb('CE2B37')]
W_, H_ = 595, 842; ML = 28; MR = W_ - 28

# ---- chữ từ bản đã duyệt
D = pymupdf.open(R + '/CATALOG SUA/CATALOGUE DA DUYET/AQUARIS/AQUARIS - Bơm trục ngang CM.pdf')
L = [s.strip() for s in D[2].get_text().splitlines() if s.strip()]
def khoi(a, b): i = L.index(a); return L[i + 1:L.index(b, i + 1)]
SCOPE = ' '.join(khoi('SCOPE OF APPLICATION', 'PUMP'))
PUMP = ' '.join(khoi('PUMP', 'MOTOR'))
MOTOR = khoi('MOTOR', 'STANDARD')
STD = khoi('STANDARD', L[L.index('STANDARD') + 3])[:2]
SUB = [s for s in L if s.startswith('CM SERIES   ·')][0]
ML_ = khoi('MATERIALS', 'PERFORMANCE DATA'); MAT = list(zip(ML_[0::2], ML_[1::2]))
SUCT = [s for s in L if s.startswith('Max. suction lift')][0]
AVG = [s for s in L if s.startswith('The figures in the tables')][0]
assert 'cast iron, AISI 304 or brass impeller' in PUMP and MAT[1] == ('Impeller', 'Cast iron / AISI 304 / Brass') and len(MAT) == 6
PUMP = PUMP.replace('cast iron, AISI 304 or brass impeller', 'cast iron impeller')   # báo giá: cánh gang
MAT[1] = ('Impeller', 'Cast iron')
MOTOR_T = ' '.join(MOTOR[:-1]); VOLT = MOTOR[-1]

# ---- số
wb = openpyxl.load_workbook(W + '/CM2.xlsx', data_only=True)
MD = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)]
assert [r[2] for r in MD] == ['CM 32-250/7.5', 'CM 40-160/4']
DN = '  /  '.join(f'{r[9]} × {r[10]}' for r in MD)
P2 = f'{min(r[3] for r in MD):g}–{max(r[3] for r in MD):g} kW'

doc = pymupdf.open(); p = doc.new_page(width=W_, height=H_)
p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def txt(x, y, s, size, bold=False, color=TXT, align='l'):
    w = FONT[bold].text_length(s, size)
    if align == 'r': x -= w
    elif align == 'c': x -= w / 2
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
def wrap(t, size, width, bold=False):
    out, cur = [], ''
    for w in t.split():
        c = (cur + ' ' + w).strip()
        if FONT[bold].text_length(c, size) <= width: cur = c
        else: out.append(cur); cur = w
    return out + [cur]
def heading(x, y, s, w):
    txt(x, y, s, 9.5, True, GREEN); p.draw_line((x, y + 4), (x + w, y + 4), color=GREEN, width=0.6)
def para(x, y, t, w, size=9):
    for l in wrap(t, size, w): txt(x, y, l, size); y += size * 1.3
    return y
def img(rect, path):
    pix = pymupdf.Pixmap(path); r = pymupdf.Rect(rect); s = min(r.width / pix.width, r.height / pix.height)
    rr = pymupdf.Rect(r.x0, r.y0, r.x0 + pix.width * s, r.y0 + pix.height * s); p.insert_image(rr, filename=path); return rr, pix

# ---- đầu trang: dải cờ Ý, tên dòng, logo
for i, c in enumerate(FL): p.draw_rect(pymupdf.Rect(i * W_ / 3, 0, (i + 1) * W_ / 3, 5), color=None, fill=c)
txt(ML, 50, 'CM', 30, True, GREEN)
txt(ML + FONT[True].text_length('CM', 30) + 10, 50, '32-250/7.5   ·   40-160/4', 15, False, GREEN)
txt(ML, 69, SUB, 9, True, MUTE)
img((MR - 116, 20, MR, 60), R + '/KHO_ANH/Bom_truc_ngang_CM/01e988048331.jpeg')
p.draw_line((ML, 78), (MR, 78), color=LINE, width=0.5)

# ---- hàng 2: ảnh (300 ppi) + ô số liệu + vật liệu
ph, pix = img((ML, 90, ML + 114, 184), R + '/KHO_ANH/Bom_truc_ngang_CM/29357a5db185.jpeg')
PPI = pix.width / ph.width * 72
X0 = 160; bw = (MR - X0 - 3 * 6) / 4
for i, (a, b) in enumerate([(DN, 'DN (MM)'), (P2, 'POWER P2'), ('3~ 380–415 V', 'VOLTAGE'), ('50 Hz', 'FREQUENCY')]):
    x = X0 + i * (bw + 6); p.draw_rect(pymupdf.Rect(x, 90, x + bw, 126), color=None, fill=BG)
    sz = 11 if FONT[True].text_length(a, 11) < bw - 8 else 9.5
    txt(x + bw / 2, 108, a, sz, True, GREEN, 'c'); txt(x + bw / 2, 120, b, 7, True, MUTE, 'c')
heading(X0, 142, 'MATERIALS', MR - X0)
cw = (MR - X0) / 2
for i, (a, b) in enumerate(MAT):
    col, row = divmod(i, 3); x = X0 + col * cw; y = 158 + row * 12.5
    txt(x, y, a, 8); txt(x + cw - 8, y, b, 8, True, align='r')
    p.draw_line((x, y + 3.5), (x + cw - 8, y + 3.5), color=LINE, width=0.4)

# ---- chữ 2 cột: trái SCOPE + STANDARD, phải PUMP + MOTOR
LW = 262; RX = MR - LW; y = 206
heading(ML, y, 'SCOPE OF APPLICATION', LW); y = para(ML, y + 17, SCOPE, LW)
heading(ML, y + 8, 'STANDARD', LW); y += 25
for s_ in STD: txt(ML, y, s_, 9); y += 11.7
yr = 206
heading(RX, yr, 'PUMP', LW); yr = para(RX, yr + 17, PUMP, LW)
heading(RX, yr + 8, 'MOTOR', LW); yr = para(RX, yr + 25, MOTOR_T, LW); txt(RX, yr, VOLT, 9); yr += 11.7
y = max(y, yr); assert y < 372, y

# ---- biểu đồ rộng hết khổ
HC = y + 16
heading(ML, HC, 'PERFORMANCE CURVES', MR - ML)
p.show_pdf_page(pymupdf.Rect(ML, HC + 10, MR, 664), pymupdf.open(W + '/qh/bieu_do.pdf'), 0)

# ---- bảng ngang (mỗi model một dòng, QĐ 160)
heading(ML, 684, 'PERFORMANCE DATA', MR - ML)
txt(MR, 684, 'Three-phase 3~ 380–415 V   ·   50 Hz', 8, False, MUTE, 'r')
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
p.show_pdf_page(pymupdf.Rect(ML, 694, ML + tr.width, 694 + tr.height), tb, 0)
y = 694 + tr.height + 14
txt(ML, y, SUCT, 9, False, MUTE)
for l in wrap(AVG, 9, (MR - ML) * 0.62): y += 11.7; txt(ML, y, l, 9, False, MUTE)
assert y < 804, y
p.draw_line((ML, 812), (MR, 812), color=LINE, width=0.5)
txt(ML, 825, 'AQUARIS  /  CM SERIES', 7.5, True, MUTE)

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
doc.set_metadata({'title': 'AQUARIS - CM SERIES CM 32-250/7.5, CM 40-160/4', 'author': 'AQUARIS'})
doc.subset_fonts()
# phông Lato chèn lên trang ánh xạ '-' → U+2010, '·' → U+2219 trong ToUnicode: đưa về mã gốc để tìm/chép chữ đúng
for x in range(1, doc.xref_length()):
    t, v = doc.xref_get_key(x, 'ToUnicode')
    if t == 'xref':
        sx = int(v.split()[0]); st = doc.xref_stream(sx)
        nst = st.replace(b'<2010>', b'<002D>').replace(b'<2219>', b'<00B7>')
        if nst != st: doc.update_stream(sx, nst)
doc.save(OUT, garbage=4, deflate=True)
print('saved', OUT, os.path.getsize(OUT), 'anh ppi', round(PPI), 'y cot trai', round(y))
