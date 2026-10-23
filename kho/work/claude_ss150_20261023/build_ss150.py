# -*- coding: utf-8 -*-
"""PEROTAC SS-150 / SSM-150F — catalogue riêng 1 trang, A4 ngang 842x595 (23/10/2026, phiên CLAUDE_20261023T0430Z).
Lệnh anh 23/10/2026: "làm a catalogue con perotac ss-150 lưu lượng max 6m3/h áp max 7m nhé" + trả lời "1. 1  2. 1"; ứng viên 02 theo QĐ 158
(giữ số đã chốt QĐ 48: Q max 7 m³/h, H max 6 m; catalogue riêng 1 trang).
Mẫu dựng: work/claude_wc200_55_20261016/build_wc200_55.py (PEROTAC catalogue riêng A4 ngang).
Số liệu: SS150.xlsx (mk_xlsx.py): 3 điểm khoá DU_LIEU/SS.xlsx + mức Q 1–5 SUY RA (QĐ 158); bảng và biểu đồ cùng tệp.
Chữ: lấy bằng mã từ bản đã duyệt CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm chìm nước thải SS.pdf (b617cdf9d4e7).
Ảnh: anh.jpg = ảnh anh gửi 08/10 'SS - PEROTAC - SS-150 den SS-370 (co phao).png' (QĐ 116) qua lam_anh.py (nền 255, bỏ bóng, khung 82%); logo Bom_chim_nuoc_thai_FC_inox/f05538b98e09.jpeg.
Dùng: python build_ss150.py <gốc kho> <thư mục làm> <tệp ra>
"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FR = R + '/vendor/fonts/LiberationSans-Regular.ttf'
FB = R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
NAVY, BLUE, TXT, GREY, BAND = rgb('13334D'), rgb('1A669E'), rgb('1F3847'), rgb('5C6E78'), rgb('EDF5FA')
ROW = rgb('EDF5FA'); WHITE = (1, 1, 1); LINE = rgb('C9D6DE')
W_, H_ = 842, 595; ML = 34; MR = W_ - 34

# ---- chữ từ bản đã duyệt (không gõ lại)
DUYET = R + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm chìm nước thải SS.pdf'
L = [s.strip() for s in pymupdf.open(DUYET)[0].get_text().splitlines() if s.strip()]
def khoi(a, b): i = L.index(a); j = L.index(b, i + 1); return L[i + 1:j]
APP = khoi('APPLICATIONS', 'OPERATING CONDITIONS')
OPC = khoi('OPERATING CONDITIONS', 'MOTOR AND PUMP')
MOT = khoi('MOTOR AND PUMP', 'Impeller type:')
IMP = L[L.index('Impeller type:') + 1]
MATL = khoi('MATERIAL', 'MODEL CODE'); MAT = list(zip(MATL[0::2], MATL[1::2]))
SUB = [s for s in L if s.startswith('Submersible sewage pump')][0]
SEAL = [s for s in MOT if s.startswith('Special mechanical seal')][0]
MOT = [s for s in MOT if s != SEAL]
QMAXNOTE = [s for s in L if s.startswith('Q max =')][0]
assert len(APP) == 3 and len(OPC) == 1 and len(MAT) == 4 and IMP == 'open' and '2850' in SUB

# ---- số từ DU_LIEU/SS.xlsx
wb = openpyxl.load_workbook(R + '/DU_LIEU/SS.xlsx', data_only=True)
m = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True) if r[0] == 'PEROTAC' and r[2] == 'SS-150'][0]
pts = sorted((r[2], r[3]) for r in wb['QH'].iter_rows(min_row=2, values_only=True) if r[0] == 'PEROTAC' and r[1] == 'SS-150')
QMAX, HMAX = pts[-1][0], pts[0][1]
assert m[1] == 'SSM-150F' and (QMAX, HMAX) == (7, 6) and pts[-1][1] == 0 and pts[0][0] == 0

def ximg(path):
    pix = pymupdf.Pixmap(path)
    if pix.alpha or pix.n > 3: pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return path, pix.width, pix.height
K = R + '/KHO_ANH/'
LOGO, PHOTO = ximg(K + 'Bom_chim_nuoc_thai_FC_inox/f05538b98e09.jpeg'), ximg(W + '/anh.jpg')

doc = pymupdf.open()
p = doc.new_page(width=W_, height=H_)
p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
def txt(x, y, s, size, bold=False, color=TXT, align='l'):
    w = FONT[bold].text_length(s, size)
    if align == 'r': x -= w
    elif align == 'c': x -= w / 2
    p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
def heading(x, y, s, w):
    txt(x, y, s, 9.5, True, BLUE); p.draw_line((x, y + 4), (x + w, y + 4), color=BLUE, width=0.6)
def img(rect, im):
    path, iw, ih = im; r = pymupdf.Rect(rect); s = min(r.width / iw, r.height / ih); w, h = iw * s, ih * s
    rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, r.x0 + (r.width + w) / 2, r.y0 + (r.height + h) / 2)
    p.insert_image(rr, filename=path); return rr

# ---- đầu trang (băng xanh nhạt, logo trái) + chân trang
p.draw_rect(pymupdf.Rect(200, 0, W_, 64), color=None, fill=BAND)
img((ML, 10, ML + 150, 54), LOGO)
txt(214, 44, 'SS-150', 26, True, NAVY)
txt(MR, 30, 'SS SERIES  /  PERFORMANCE & TECHNICAL DATA', 11, True, NAVY, 'r')
txt(MR, 46, SUB, 9, False, TXT, 'r')
p.draw_line((0, 64), (W_, 64), color=BLUE, width=1)
p.draw_line((ML, 562), (MR, 562), color=LINE, width=0.5)
txt(ML, 576, 'PEROTAC  /  SS SERIES', 7.5, True, GREY)

# ---- cột trái
LW = 210
heading(ML, 86, 'MODEL CODE', LW)
for i, (a, b) in enumerate([(m[2], 'three-phase 3~'), (m[1], 'single-phase 1~')]):
    y = 104 + i * 15; txt(ML, y, a, 10, True, NAVY); txt(ML + 70, y, b, 8.5)
heading(ML, 150, 'MAIN DATA', LW)
rows = [('Power P2', f'{m[3]} kW / {m[4]} HP'), ('Power supply 1~', '1~ 220–240 V 50 Hz'), ('Power supply 3~', '3~ 380–415 V 50 Hz'),
        ('Speed', 'n ≈ 2850 /min'), ('Max. flow rate', f'{QMAX:g} m³/h (H = 0)'), ('Max. head', f'{HMAX:g} m (Q = 0)'), ('Impeller type', IMP)]
y = 166
for i, (a, b) in enumerate(rows):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(ML, y - 9, ML + LW, y + 3.5), color=None, fill=ROW)
    txt(ML + 4, y, a, 8.5, True); txt(ML + 92, y, b, 8.5); y += 12.5
for t, ds in [('APPLICATIONS', APP), ('OPERATING CONDITIONS', OPC), ('MOTOR AND PUMP', MOT)]:
    heading(ML, y + 10, t, LW); y += 26
    for s in ds: txt(ML, y, s, 9); y += 12
assert y < 455, y

# ---- giữa: ảnh + vật liệu
MX0, MX1 = 262, 452
ph = img((MX0, 80, MX1, 270), PHOTO)
heading(MX0, 292, 'MATERIALS', MX1 - MX0)
y = 302
p.draw_rect(pymupdf.Rect(MX0, y, MX1, y + 14), color=None, fill=NAVY)
txt(MX0 + 4, y + 10, 'COMPONENT', 7.5, True, WHITE); txt(MX0 + 92, y + 10, 'MATERIAL', 7.5, True, WHITE); y += 14
for i, (a, b) in enumerate(MAT):
    if i % 2 == 0: p.draw_rect(pymupdf.Rect(MX0, y, MX1, y + 15), color=None, fill=ROW)
    txt(MX0 + 4, y + 10.5, a, 7.5); txt(MX0 + 92, y + 10.5, b, 7.5); y += 15
y += 22
heading(MX0, y, 'NOTES', MX1 - MX0); y += 17
for s in [SEAL]:
    p.draw_circle((MX0 + 3, y - 3), 1.4, color=None, fill=BLUE); txt(MX0 + 9, y, s, 9); y += 12
assert y < 470, y

# ---- phải: biểu đồ
CH = pymupdf.Rect(466, 78, MR, 78 + 342 * 318 / 330)
p.show_pdf_page(CH, pymupdf.open(W + '/qh/bieu_do.pdf'), 0)

# ---- dưới: bảng
heading(ML, 466, 'PERFORMANCE DATA', MR - ML)
tb = pymupdf.open(W + '/qh/bang.pdf'); tr = tb[0].rect
p.show_pdf_page(pymupdf.Rect(ML, 478, ML + tr.width, 478 + tr.height), tb, 0)
txt(ML + tr.width + 16, 506, QMAXNOTE, 9, False, GREY)

# gộp phông trùng tên giữa trang và các khối chèn
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
doc.set_metadata({'title': 'PEROTAC - SS SERIES SS-150', 'author': 'PEROTAC'})
doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True)
print('saved', OUT, os.path.getsize(OUT), 'anh', round(ph.width), 'x', round(ph.height), 'pt; ppi', round(PHOTO[2] / ph.height * 72))
