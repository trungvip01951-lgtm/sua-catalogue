# -*- coding: utf-8 -*-
"""PEROTAC catalogue riêng theo báo giá BG-27102026-001 (27/10/2026, khách Anh Tuấn) — A4 ngang 842x595.
Lệnh anh: "Làm a catalogue 2 bộ này nhé 1 bộ 1 con 1 bộ 2 con" → bộ 1: CM 32-160/3; bộ 2: CDLF8-12T + CDLF16-8T.
Số: CM32_160_3.xlsx / CDLF_2MA.xlsx (mk_xlsx.py; mã lệch DU_LIEU theo báo giá — QĐ 159). Chữ: lấy bằng mã từ bản đã duyệt
CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm trục ngang CM.pdf tr.1 và PEROTAC - Bơm trục đứng CDLF.pdf tr.1–2.
Mẫu bố cục: work/claude_ss150_20261023/build_ss150.py. Dùng: python build_bg27.py <gốc kho> <thư mục làm> cm|cdlf <tệp ra>
"""
import sys, os, re, pymupdf, openpyxl
R, W, BO, OUT = sys.argv[1:5]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
NAVY, BLUE, TXT, GREY, BAND = rgb('13334D'), rgb('1A669E'), rgb('1F3847'), rgb('5C6E78'), rgb('EDF5FA')
ROW = BAND; WHITE = (1, 1, 1); LINE = rgb('C9D6DE')
W_, H_ = 842, 595; ML = 34; MR = W_ - 34
DD = R + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/'
def dong(f, tr): return [s.strip() for s in pymupdf.open(DD + f)[tr].get_text().splitlines() if s.strip()]
def khoi(L, a, b): i = L.index(a); return L[i + 1:L.index(b, i + 1)]
K = R + '/KHO_ANH/'

if BO == 'cm':
    L = dong('PEROTAC - Bơm trục ngang CM.pdf', 0)
    XL, QH = 'CM32_160_3.xlsx', 'qh_cm'
    BIG, SERIES = 'CM 32-160/3', 'CM SERIES'
    SUB = 'Close-coupled centrifugal pump   |   EN733   |   50 Hz   |   n ≈ 2900 /min'
    assert 'EN733   |   50 Hz   |   n ≈ 2900 /min   |   3~ 380–415 V' in L
    TS = khoi(L, 'TECHNICAL SHEET – MATERIALS', 'RANGE OVERVIEW'); TSD = dict(zip(TS[0::2], TS[1::2]))
    MAT = [(k, TSD[k]) for k in ('Casing', 'Impeller', 'Shaft', 'Shaft seal', 'Bearing')]
    MOTOR = ['3~ 380–415 V   ·   50 Hz', f"{TSD['IP']}   ·   Insulation {TSD['Class'].replace('Class', 'class')}", f"Duty {TSD['Duty']}"]
    TEXT = [('FIELDS OF USE', khoi(L, 'FIELDS OF USE', 'DESCRIPTION')), ('OPERATING LIMITS', khoi(L, 'OPERATING LIMITS', 'MODEL CODE'))]
    NOTES = ('DESCRIPTION', khoi(L, 'DESCRIPTION', 'APPLICATIONS'))
    PHOTO = K + 'Bom_truc_ngang_CM/11a1ade937e6.jpeg'; PH_BOX = (190, 126)
    def cong(m): return f'DN {m[9]} × {m[10]}'
    MODEL_CODE = [('CM', 'Pump with square motor'), ('32', 'Discharge size (mm)'), ('160', 'Nominal impeller size (mm)'), ('3', 'Rated power (kW)')]
else:
    L = dong('PEROTAC - Bơm trục đứng CDLF.pdf', 0); L2 = dong('PEROTAC - Bơm trục đứng CDLF.pdf', 1)
    XL, QH = 'CDLF_2MA.xlsx', 'qh_cdlf'
    BIG, SERIES = 'CDLF8-12T  ·  CDLF16-8T', 'CDLF SERIES'
    SUB = [s for s in L if s.startswith('Light stainless steel vertical multi-stage')][0]
    MOTOR = khoi(L, 'MOTOR', 'APPLICATIONS'); MOTOR = [s for s in MOTOR if not s.startswith('Single-phase') and not s.startswith('Above 3 kW')]
    oc = khoi(L, 'OPERATING CONDITIONS', 'MODEL DESIGNATION'); oc = [oc[0] + ' ' + oc[1]] + oc[2:]
    TEXT = [('OPERATING CONDITIONS', oc)]
    i = L2.index('MATERIALS  CDLF 8, 12, 16, 20'); seg = L2[i:L2.index('SECTION DRAWING  CDLF 32, 42')]
    mt = {}
    for k in ('Pump head', 'Impeller', 'Diffuser', 'Cylinder', 'Shaft', 'Base plate', 'Bearing'):
        j = seg.index(k); mt[k] = seg[j + 1] + (' ' + seg[j + 2] if seg[j + 2].startswith(('AISI', 'ASTM')) else '')
    MAT = list(mt.items())
    NOTES = ('PUMP', [' '.join(khoi(L, 'PUMP', 'MOTOR'))])
    PHOTO = K + 'Bom_truc_dung_CDLF/89efdf5b933e.png'; PH_BOX = (190, 150)
    def cong(m): return f'{m[9]} / {m[10]}'
    MODEL_CODE = None

wb = openpyxl.load_workbook(W + '/' + XL, data_only=True)
MD = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)]
QHp = {}
for r in wb['QH'].iter_rows(min_row=2, values_only=True): QHp.setdefault(r[1], []).append((r[2], r[3]))
for k in QHp: QHp[k].sort()

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
def heading(x, y, s, w): txt(x, y, s, 9.5, True, BLUE); p.draw_line((x, y + 4), (x + w, y + 4), color=BLUE, width=0.6)
def img(rect, path):
    pix = pymupdf.Pixmap(path)
    if pix.alpha:                      # ảnh nền trong suốt → đặt trên nền trắng (PEROTAC không bóng)
        nb = pymupdf.Pixmap(pymupdf.csRGB, pix.irect, False); nb.set_rect(nb.irect, (255, 255, 255))
        base = pymupdf.Pixmap(pymupdf.csRGB, pix); data = None
    r = pymupdf.Rect(rect); s = min(r.width / pix.width, r.height / pix.height); w, h = pix.width * s, pix.height * s
    rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, r.x0 + (r.width + w) / 2, r.y0 + (r.height + h) / 2)
    p.insert_image(rr, filename=path); return rr, pix

# ---- đầu trang
p.draw_rect(pymupdf.Rect(200, 0, W_, 64), color=None, fill=BAND)
img((ML, 10, ML + 150, 54), K + 'Bom_chim_nuoc_thai_FC_inox/f05538b98e09.jpeg')
RT = 214 + 12 + max(FONT[True].text_length(f'{SERIES}  /  PERFORMANCE & TECHNICAL DATA', 11), FONT[False].text_length(SUB, 9))
sz = 26
while FONT[True].text_length(BIG, sz) > MR - RT - 214 and sz > 16: sz -= 1
txt(214, 44, BIG, sz, True, NAVY)
txt(MR, 30, f'{SERIES}  /  PERFORMANCE & TECHNICAL DATA', 11, True, NAVY, 'r')
txt(MR, 46, SUB, 9, False, TXT, 'r')
p.draw_line((0, 64), (W_, 64), color=BLUE, width=1)
p.draw_line((ML, 562), (MR, 562), color=LINE, width=0.5)
txt(ML, 576, f'PEROTAC  /  {SERIES}', 7.5, True, GREY)

# ---- cột trái: MAIN DATA (mỗi model một cột giá trị) + chữ
LW = 230; y = 86
heading(ML, y, 'MAIN DATA', LW); y += 16
cols = [m[2] for m in MD]; cw = (LW - 92) / len(cols)
rows = [('Model', cols, True), ('Power P2', [f'{m[3]:g} kW / {m[4]:g} HP' for m in MD], False),
        ('Power supply', ['3~ 380–415 V' for m in MD], False), ('Frequency', ['50 Hz' for m in MD], False),
        ('Speed', ['n ≈ 2900 /min' for m in MD], False),
        ('Inlet / Outlet' if BO == 'cdlf' else 'Suction × Disch.', [cong(m) for m in MD], False),
        ('Flow range', [f'{QHp[m[2]][0][0]:g}–{QHp[m[2]][-1][0]:g} m³/h' for m in MD], False),
        ('Head range', [f'{QHp[m[2]][0][1]:g}–{QHp[m[2]][-1][1]:g} m' for m in MD], False)]
for i, (a, vs, b) in enumerate(rows):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(ML, y - 9, ML + LW, y + 3.5), color=None, fill=ROW)
    txt(ML + 4, y, a, 8.5, True)
    for j, v in enumerate(vs): txt(ML + 92 + j * cw, y, v, 8.5, b, NAVY if b else TXT)
    y += 12.5
if BO == 'cm':
    heading(ML, y + 10, 'MOTOR', LW); y += 26
    for s_ in MOTOR:
        for l in wrap(s_, 9, LW): txt(ML, y, l, 9); y += 11.5
else: y += 2
for t, ds in TEXT:
    heading(ML, y + 8, t, LW); y += 24
    for s_ in ds:
        for l in wrap(s_, 9, LW): txt(ML, y, l, 9); y += 11.5
t, ds = NOTES
heading(ML, y + 8, t, LW); y += 24
for s_ in ds:
    for l in wrap(s_, 9, LW): txt(ML, y, l, 9); y += 11.5
YL = y

# ---- giữa: ảnh + vật liệu + ghi chú
MX0, MX1 = 280, 456
ph, pix = img((MX0, 78, MX1, 78 + PH_BOX[1]), PHOTO); PPI = pix.width / ph.width * 72
y = 78 + PH_BOX[1] + 16
heading(MX0, y, 'MATERIALS', MX1 - MX0); y += 8
for i, (a, b) in enumerate(MAT):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(MX0, y, MX1, y + 13), color=None, fill=ROW)
    txt(MX0 + 4, y + 9.5, a, 8, True); txt(MX1 - 4, y + 9.5, b, 8, False, TXT, 'r'); y += 13
if MODEL_CODE:
    heading(MX0, y + 16, 'MODEL CODE', MX1 - MX0); y += 34
    for i, (a, b) in enumerate(MODEL_CODE):
        txt(MX0 + 4, y, a, 9, True, NAVY); txt(MX0 + 40, y, b, 8.5); y += 11.5
if BO == 'cdlf':
    heading(MX0, y + 16, 'MOTOR', MX1 - MX0); y += 32
    for s_ in MOTOR:
        for l in wrap(s_, 9, MX1 - MX0): txt(MX0, y, l, 9); y += 11.5
YM = y

# ---- phải: biểu đồ; dưới: bảng
CH = pymupdf.Rect(470, 78, MR, 78 + 338 * 318 / 330)
p.show_pdf_page(CH, pymupdf.open(W + f'/{QH}/bieu_do.pdf'), 0)
tb = pymupdf.open(W + f'/{QH}/bang.pdf'); tr = tb[0].rect
TY = 556 - tr.height - 12
assert YL < TY - 4 and YM < TY - 4, (YL, YM, TY)
heading(ML, TY - 2, 'PERFORMANCE DATA', MR - ML)
p.show_pdf_page(pymupdf.Rect(ML, TY + 8, ML + tr.width, TY + 8 + tr.height), tb, 0)

canon = {}
for f in p.get_fonts(full=True):
    if f[4] in ('LR', 'LB'): canon[f[3].split('+')[-1]] = f[0]
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
doc.set_metadata({'title': f'PEROTAC - {SERIES} {BIG}', 'author': 'PEROTAC'})
doc.subset_fonts()
for x in range(1, doc.xref_length()):
    t_, v = doc.xref_get_key(x, 'ToUnicode')
    if t_ == 'xref':
        sx = int(v.split()[0]); st = doc.xref_stream(sx)
        nst = st.replace(b'<2010>', b'<002D>').replace(b'<2219>', b'<00B7>')
        if nst != st: doc.update_stream(sx, nst)
doc.save(OUT, garbage=4, deflate=True)
print('saved', os.path.basename(OUT), os.path.getsize(OUT), 'ppi', round(PPI), 'YL', round(YL), 'YM', round(YM), 'TY', round(TY))
