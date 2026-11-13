# -*- coding: utf-8 -*-
"""REDPUMP 150WC / 200WC 37–132 kW — catalogue riêng 14 mã, A4 ngang 4 trang, bản EN và VI (13/11/2026, QĐ 174).
Số: WCL.xlsx (mk_xlsx.py). Chữ EN: REDPUMP - Bơm cắt rác WC.pdf đã duyệt tr.5 (bỏ "Curve tolerance … ISO 9906" QĐ 149, bỏ dòng 1 pha).
VI: dịch từ chữ EN (bảng VI dưới). Ảnh: KHO_ANH/Bom_cat_rac_WC/51c00456604c.jpeg (150WC), d78acefb2b87.jpeg (200WC) — ảnh trang 150WC/200WC của bản đã duyệt.
Dùng: python build_wcl.py <gốc kho> <thư mục làm> <tệp ra> <en|vi>"""
import sys, os, re, pymupdf, openpyxl
R, W, OUT, LANG = sys.argv[1:5]
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
DARK, RED, GREY, TXT, WHITE, LINE = rgb('2B2E33'), rgb('A31A1F'), rgb('6B6F75'), rgb('222428'), (1, 1, 1), rgb('D9D4D1')
STRIPE, LIGHT, PINK = rgb('F1EEEC'), rgb('C9CDD2'), rgb('E8767B')
K = R + '/KHO_ANH/'; LOGO = K + 'Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg'
ANH = {'150': K + 'Bom_cat_rac_WC/51c00456604c.jpeg', '200': K + 'Bom_cat_rac_WC/d78acefb2b87.jpeg'}
W_, H_ = 842, 595; COL = 238; CX0, CX1 = COL + 26, W_ - 34

# ---- chữ EN từ bản đã duyệt
D0 = pymupdf.open(R + '/CATALOG SUA/CATALOGUE DA DUYET/REDPUMP/REDPUMP - Bơm cắt rác WC.pdf')
L = [s.strip() for s in D0[4].get_text().splitlines() if s.strip()]
def khoi(a, b): i = L.index(a); return L[i + 1:L.index(b, i + 1)]
SUB = L[2]; APP = khoi('APPLICATIONS', 'OPERATING CONDITIONS / MOTOR AND PUMP')
OPC = [s for s in khoi('OPERATING CONDITIONS / MOTOR AND PUMP', 'MATERIALS') if 'ISO 9906' not in s and not s.startswith('Single-phase')]
ML = khoi('MATERIAL', [s for s in L if re.fullmatch(r'\d\d / \d\d', s)][0]); MAT = list(zip(ML[0::2], ML[1::2]))
assert SUB == 'Submersible sewage pumps with cutter' and len(APP) == 3 and len(OPC) == 4 and len(MAT) == 6, (APP, OPC, MAT)
VI = {'Submersible sewage pumps with cutter': 'Bơm chìm nước thải có dao cắt rác',
      'Sewage treatment plants': 'Trạm xử lý nước thải', 'Industrial draining': 'Thoát nước công nghiệp', 'Agriculture irrigation': 'Tưới tiêu nông nghiệp',
      'Maximum fluid temperature up to +40 °C': 'Nhiệt độ chất lỏng tối đa +40 °C', 'Rewindable motor': 'Động cơ quấn lại được',
      'Three-phase: 380–415 V / 50 Hz': 'Ba pha: 380–415 V / 50 Hz', 'It can work in water containing fiber': 'Làm việc được trong nước có lẫn sợi',
      'Diffuser': 'Buồng bơm', 'Impeller': 'Cánh bơm', 'Motor external casing': 'Vỏ ngoài động cơ', 'Mechanical seal': 'Phớt cơ khí', 'Shaft': 'Trục',
      'Seal lubricant oil': 'Dầu bôi trơn phớt', 'Cast-iron ASTM NO.30': 'Gang ASTM NO.30', 'Oil for food machinery and pharmaceutical use': 'Dầu dùng cho máy thực phẩm và dược phẩm'}
T = {  # khóa: (EN, VI)
 'series': ('WC SERIES  ·  SUBMERSIBLE SEWAGE PUMPS WITH CUTTER', 'DÒNG WC  ·  BƠM CHÌM NƯỚC THẢI CẮT RÁC'),
 'range': ('RANGE CHARACTERISTICS', 'ĐẶC TÍNH DẢI'), 'power': ('Power P2', 'Công suất P2'), 'disch': ('Discharge', 'Cửa xả'),
 'qmax': ('Max. flow rate', 'Lưu lượng max'), 'hmax': ('Max. head', 'Cột áp max'), 'speed': ('Speed', 'Tốc độ'), 'supply': ('Power supply', 'Nguồn điện'),
 'nom': ('PRODUCT NOMENCLATURE', 'CÁCH ĐỌC MÃ'), 'n1': ('Outlet size (mm)', 'Cỡ cửa xả (mm)'), 'n2': ('Series', 'Dòng'), 'n3': ('Rated flow (m³/h)', 'Lưu lượng định mức (m³/h)'),
 'n4': ('Rated head (m)', 'Cột áp định mức (m)'), 'n5': ('Power (kW)', 'Công suất (kW)'), 'p1t': ('Model overview', 'Tổng quan model'),
 'p1s': ('14 models, 37–132 kW, three-phase 3~ 380–415 V 50 Hz.', '14 model, 37–132 kW, ba pha 3~ 380–415 V 50 Hz.'),
 'main': ('MAIN DATA', 'THÔNG SỐ CHÍNH'), 'h_no': ('No.', 'TT'), 'h_md': ('Model', 'Model'), 'h_rated': ('Rated point', 'Điểm định mức'),
 'h_qmax': ('Max. flow', 'Q max'), 'h_hmax': ('Max. head', 'H max'), 'h_dn': ('Discharge', 'Cửa xả'), 'h_sp': ('Speed', 'Tốc độ'),
 'rpm': ('/min', 'v/ph'), 'poles2': ('2 poles · n ≈ 2900 /min', '2 cực · n ≈ 2900 vòng/phút'), 'poles4': ('4 poles · n ≈ 1450 /min', '4 cực · n ≈ 1450 vòng/phút'),
 'note1': ('Rated point: rated flow and head given in the model code. Max. flow at H = 0; max. head at Q = 0.',
           'Điểm định mức: lưu lượng và cột áp định mức ghi trong mã model. Lưu lượng max tại H = 0; cột áp max tại Q = 0.'),
 'curves': ('Performance curves', 'Đường đặc tính'), 'perf': ('PERFORMANCE DATA', 'BẢNG THÔNG SỐ'), 'ga': ('GROUP A', 'NHÓM A'), 'gb': ('GROUP B', 'NHÓM B'),
 'p4t': ('Applications, operating conditions and materials', 'Ứng dụng, điều kiện làm việc và vật liệu'),
 'app': ('APPLICATIONS', 'ỨNG DỤNG'), 'opc': ('OPERATING CONDITIONS / MOTOR AND PUMP', 'ĐIỀU KIỆN LÀM VIỆC / ĐỘNG CƠ VÀ BƠM'),
 'mat': ('MATERIALS', 'VẬT LIỆU'), 'comp': ('Component', 'Bộ phận'), 'matl': ('Material', 'Vật liệu'),
 'tnote': ('Head values between max. head, rated point and max. flow are read on the performance curve. “–” = outside the operating range.',
           'Cột áp giữa các điểm cột áp max, điểm định mức và lưu lượng max đọc trên đường đặc tính. “–” = ngoài dải làm việc.'),
}
tr = lambda k: T[k][0 if LANG == 'en' else 1]
vt = lambda s: s if LANG == 'en' else VI[s]
assert LANG in ('en', 'vi') and (LANG == 'en' or all(x in VI for x in [SUB] + APP + OPC + [c for ab in MAT for c in ab if not c.startswith(('AISI', 'Graphite'))]))

wb = openpyxl.load_workbook(W + '/WCL.xlsx', data_only=True)
MD = sorted([r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True)], key=lambda r: r[14])
INFO = {r[2]: dict(qmax=float(re.search(r'Qmax ([\d.]+)', r[11]).group(1)), hmax=float(re.search(r'Hmax ([\d.]+)', r[11]).group(1)),
                   rated=re.search(r'định mức ([\d.]+) m³/h – ([\d.]+) m', r[11]).groups()) for r in MD}
assert len(MD) == 14 and MD[0][2] == '150WC200-35-37' and MD[-1][2] == '200WC400-75-132'
NHOM = {'150': (['150WC200-35-37', '150WC180-50-55', '150WC200-60-75', '150WC200-70-90'], ['150WC200-40-45', '150WC180-80-110', '150WC200-90-132']),
        '200': (['200WC350-22-37', '200WC300-32-45', '200WC300-40-55', '200WC300-60-90'], ['200WC350-45-75', '200WC300-65-110', '200WC400-75-132'])}
assert sorted(sum(map(list, NHOM['150'] + NHOM['200']), [])) == sorted(INFO)

doc = pymupdf.open(); FONT = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}; NP = 4; PPI = {}
class Pg:
    def __init__(s, so, ten, tom=None):
        s.p = p = doc.new_page(width=W_, height=H_); p.insert_font(fontname='LR', fontfile=FR); p.insert_font(fontname='LB', fontfile=FB)
        p.draw_rect(pymupdf.Rect(0, 0, COL, H_), color=None, fill=DARK); p.draw_rect(pymupdf.Rect(COL - 5, 0, COL, H_), color=None, fill=RED)
        for i, l in enumerate(s.wrap(tr('series'), 9, COL - 56, True)): s.txt(28, 52 + i * 12, l, 9, True, LIGHT)
        if so: s.txt(28, 112, so, 30, True, PINK)
        y = 140
        for l in s.wrap(ten, 17, COL - 56, True): s.txt(28, y, l, 17, True, WHITE); y += 21
        if tom:
            y += 6
            for l in s.wrap(tom, 9, COL - 56): s.txt(28, y, l, 9, False, LIGHT); y += 12
        s.yc = y
        pix = pymupdf.Pixmap(LOGO); k = min(104 / pix.width, 46 / pix.height)
        p.insert_image(pymupdf.Rect(CX1 - pix.width * k, 18, CX1, 18 + pix.height * k), filename=LOGO)
        p.draw_line((CX0, 566), (CX1, 566), color=LINE, width=0.5)
        s.txt(CX0, 580, 'REDPUMP  /  WC SERIES', 7.5, True, GREY); s.txt(CX1, 580, f'{doc.page_count:02d} / {NP:02d}' if LANG == 'en' else f'Trang {doc.page_count}/{NP}', 7.5, True, GREY, 'r')
    def txt(s, x, y, st, size, bold=False, color=TXT, align='l'):
        w = FONT[bold].text_length(st, size); x = x - w if align == 'r' else x - w / 2 if align == 'c' else x
        s.p.insert_text((x, y), st, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
    def wrap(s, st, size, width, bold=False):
        out, cur = [], ''
        for w in st.split():
            c = (cur + ' ' + w).strip()
            if FONT[bold].text_length(c, size) <= width: cur = c
            else: out.append(cur); cur = w
        return out + [cur]
    def head(s, x, y, st, w, color=DARK):
        sz = 10
        while FONT[True].text_length(st, sz) > w and sz > 9: sz -= 0.25
        assert FONT[True].text_length(st, sz) <= w, st
        s.txt(x, y, st, sz, True, color); s.p.draw_line((x, y + 5), (x + w, y + 5), color=RED, width=1.2); return y + 19
    def lst(s, x, y, ds, w, size=9, color=TXT):
        for d in ds:
            for i, l in enumerate(s.wrap(d, size, w - 9)):
                if i == 0: s.p.draw_circle((x + 2.5, y - 3), 1.3, color=None, fill=RED)
                s.txt(x + 9, y, l, size, False, color); y += size * 1.3
        return y
    def table(s, x, y, hdr, rows, widths, size=8, rh=13.5, al=None):
        tw = sum(widths); p = s.p; p.draw_rect(pymupdf.Rect(x, y, x + tw, y + rh + 2), color=None, fill=DARK); cx = x
        for h, w in zip(hdr, widths): s.txt(cx + w / 2, y + rh - 2.5, h, size, True, WHITE, 'c'); cx += w
        y += rh + 2
        for i, row in enumerate(rows):
            if i % 2: p.draw_rect(pymupdf.Rect(x, y, x + tw, y + rh), color=None, fill=STRIPE)
            cx = x
            for j, (v, w) in enumerate(zip(row, widths)):
                a = (al or ['l'] + ['c'] * (len(row) - 1))[j]
                s.txt(cx + 5 if a == 'l' else cx + w / 2, y + rh - 4, str(v), size, j == (al or ['l']).index('l') if al else j == 0, TXT, 'l' if a == 'l' else 'c'); cx += w
            y += rh
        p.draw_line((x, y), (x + tw, y), color=DARK, width=0.8); return y
    def img(s, rect, path):
        pix = pymupdf.Pixmap(path); r = pymupdf.Rect(rect); k = min(r.width / pix.width, r.height / pix.height); w, h = pix.width * k, pix.height * k
        rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, r.x0 + (r.width + w) / 2, r.y0 + (r.height + h) / 2)
        s.p.insert_image(rr, filename=path); PPI[os.path.basename(path)] = pix.height / h * 72; return rr

# ===== Trang 1: tổng quan
pg = Pg(None, '150WC · 200WC', tr('p1s')); t = pg.txt; y = pg.yc + 20
t(28, y, tr('range'), 10, True, WHITE); pg.p.draw_line((28, y + 5), (COL - 28, y + 5), color=RED, width=1.2); y += 22
for a, b in [(tr('power'), '37 – 132 kW'), (tr('disch'), 'DN150 · DN200'), (tr('qmax'), '350 · 780 m³/h'), (tr('hmax'), '120 · 105 m'),
             (tr('supply'), '3~ 380–415 V 50 Hz')]:
    t(28, y, a, 8, True, LIGHT); t(112, y, b, 9.5, True, WHITE); y += 16
for k in ('poles2', 'poles4'): t(28, y, ('150WC: ' if k == 'poles2' else '200WC: ') + tr(k), 8.5, False, LIGHT); y += 13
y += 18; t(28, y, tr('nom'), 10, True, WHITE); pg.p.draw_line((28, y + 5), (COL - 28, y + 5), color=RED, width=1.2); y += 24
for c, d in [('150', tr('n1')), ('WC', tr('n2')), ('200', tr('n3')), ('35', tr('n4')), ('37', tr('n5'))]:
    t(28, y, c, 11, True, PINK); t(64, y, d, 9, False, WHITE); y += 15
t(28, y + 2, ('Example: ' if LANG == 'en' else 'Ví dụ: ') + '150WC200-35-37', 8.5, False, LIGHT); assert y < 556, y
t(CX0, 44, 'WC  150WC · 200WC', 18, True, DARK); t(CX0, 62, vt(SUB).upper() + '  ·  37–132 kW', 9.5, True, RED)
for i, (dn, x0) in enumerate((('150', CX0), ('200', CX0 + 140))):
    rr = pg.img((x0, 76, x0 + 120, 226), ANH[dn]); t((rr.x0 + rr.x1) / 2, 238, dn + 'WC', 9, True, DARK, 'c')
x2 = CX0 + 290; yy = pg.head(x2, 90, tr('app'), CX1 - x2); yy = pg.lst(x2, yy, [vt(a) for a in APP], CX1 - x2)
yy = pg.head(x2, yy + 8, tr('opc'), CX1 - x2); yy = pg.lst(x2, yy, [vt(a) for a in OPC], CX1 - x2); assert yy < 250, yy
y = pg.head(CX0, 262, tr('main'), CX1 - CX0)
rows = []
for i, r in enumerate(MD, 1):
    m = r[2]; f = INFO[m]; dn = m[:3]
    rows.append((i, m, f'{r[3]:g} kW / {r[4]} HP', f"{f['rated'][0]} m³/h – {f['rated'][1]} m", f"{f['qmax']:g} m³/h", f"{f['hmax']:g} m", 'DN' + dn,
                 ('2900 ' if dn == '150' else '1450 ') + tr('rpm')))
y = pg.table(CX0, y - 6, [tr('h_no'), tr('h_md'), 'P2', tr('h_rated'), tr('h_qmax'), tr('h_hmax'), tr('h_dn'), tr('h_sp')], rows,
             [26, 104, 86, 104, 62, 50, 50, 62], size=8, rh=14, al=['c', 'l', 'c', 'c', 'c', 'c', 'c', 'c'])
for l in pg.wrap(tr('note1'), 9, CX1 - CX0): t(CX0, y + 14, l, 9, False, GREY); y += 12
assert y < 556, y

# ===== Trang 2–3: đường + bảng
for so, dn in (('2', '150'), ('3', '200')):
    pg = Pg(dn + 'WC', tr('curves'), tr('poles2' if dn == '150' else 'poles4') + ' · 50 Hz')
    rr = pg.img((28, pg.yc + 20, COL - 28, pg.yc + 20 + 200), ANH[dn])
    y2 = rr.y1 + 26; pg.txt(28, y2, tr('range'), 10, True, WHITE); pg.p.draw_line((28, y2 + 5), (COL - 28, y2 + 5), color=RED, width=1.2); y2 += 22
    ms = [m for m in INFO if m.startswith(dn)]
    for a, b in [(tr('power'), f"{min(int(m.split('-')[-1]) for m in ms)} – {max(int(m.split('-')[-1]) for m in ms)} kW"), (tr('disch'), 'DN' + dn),
                 (tr('qmax'), f"{max(INFO[m]['qmax'] for m in ms):g} m³/h"), (tr('hmax'), f"{max(INFO[m]['hmax'] for m in ms):g} m")]:
        pg.txt(28, y2, a, 8, True, LIGHT); pg.txt(112, y2, b, 9.5, True, WHITE); y2 += 16
    assert y2 < 556, y2
    cw = 266; x = CX0; CHH = float(os.environ.get('CHH', 262))
    for g, (lab, f) in enumerate(((tr('ga'), 'a'), (tr('gb'), 'b'))):
        pg.head(x, 92, lab, cw); pg.p.show_pdf_page(pymupdf.Rect(x, 104, x + cw, 104 + CHH), pymupdf.open(f'{W}/qh/{LANG}_bd{dn}{f}.pdf'), 0); x += cw + 12
    y = pg.head(CX0, 104 + CHH + 14, tr('perf'), CX1 - CX0)
    tb = pymupdf.open(f'{W}/qh/bang{dn}.pdf'); trc = tb[0].rect
    pg.p.show_pdf_page(pymupdf.Rect(CX0, y - 6, CX0 + trc.width, y - 6 + trc.height), tb, 0); y += trc.height - 4
    for l in pg.wrap(tr('tnote'), 9, CX1 - CX0): pg.txt(CX0, y + 6, l, 9, False, GREY); y += 11
    assert y < 562, y

# ===== Trang 4: vật liệu
pg = Pg(None, tr('p4t')); y = pg.head(CX0, 100, tr('mat'), 302)
pg.table(CX0, y - 6, [tr('comp'), tr('matl')], [(vt(a), vt(b) if not b.startswith(('AISI', 'Graphite')) else b) for a, b in MAT], [112, 190], size=9, rh=16)
x2 = CX0 + 322; yy = pg.head(x2, 100, tr('app'), CX1 - x2); yy = pg.lst(x2, yy, [vt(a) for a in APP], CX1 - x2)
yy = pg.head(x2, yy + 10, tr('opc'), CX1 - x2); yy = pg.lst(x2, yy, [vt(a) for a in OPC], CX1 - x2)
for dn, x0 in (('150', CX0 + 40), ('200', CX0 + 300)):
    rr = pg.img((x0, 280, x0 + 180, 520), ANH[dn]); pg.txt((rr.x0 + rr.x1) / 2, 536, dn + 'WC', 9, True, DARK, 'c')
assert doc.page_count == NP

canon = {}
for p in doc:
    for f in p.get_fonts(full=True):
        if f[4] in ('LR', 'LB'): canon.setdefault(f[3].split('+')[-1], f[0])
for x in range(1, doc.xref_length()):
    for key in ('Resources/Font', 'Font'):
        try: ty, v = doc.xref_get_key(x, key)
        except Exception: continue
        if ty != 'dict': continue
        def rep(mm):
            fx = int(mm.group(2)); base = doc.xref_get_key(fx, 'BaseFont')[1].lstrip('/').split('+')[-1]
            return f'/{mm.group(1)} {canon.get(base, fx)} 0 R'
        nv = re.sub(r'/([\w.-]+)\s+(\d+)\s+0\s+R', rep, v)
        if nv != v: doc.xref_set_key(x, key, nv)
doc.set_metadata({'title': 'REDPUMP - WC 150WC/200WC 37-132 kW', 'author': 'REDPUMP'}); doc.subset_fonts()
doc.save(OUT, garbage=4, deflate=True); print('saved', OUT, os.path.getsize(OUT), {k: round(v) for k, v in PPI.items()})
