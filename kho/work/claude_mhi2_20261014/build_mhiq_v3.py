# -*- coding: utf-8 -*-
"""Dựng catalogue MỚI PEROTAC cụm 2 bơm tăng áp biến tần MHI-Q (QĐ 155, 14/10/2026).
Số liệu: MHI-Q.xlsx (sheet MODEL, QH — một nguồn cho bảng + đường; số SUY RA từ đường MHI-403 / MHI-1604 đã duyệt).
Biểu đồ: tools/ve_duong_cong.py (chart_<model>.pdf). Hồ sơ hãng: rules/HO_SO_HANG.json (PEROTAC, A4 ngang).
Dùng: python build_mhiq.py <gốc kho> <thư mục làm (có MHI-Q.xlsx, chart_*.pdf, img/)> <tệp ra>
"""
import sys, io, json, re
import pymupdf, openpyxl
R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HS = json.load(open(R + '/rules/HO_SO_HANG.json', encoding='utf-8'))
FR, FB = R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
WHITE = (1, 1, 1)
H = HS['hang']['PEROTAC']['mau']; NAVY, BLUE, BAND = rgb(H['chinh']), rgb(H['duong']), rgb(H['nen'])
TXT, GREY, LINE = rgb('1F3847'), rgb('5C6E78'), rgb('B9C9D3')
ML, MR = 34, 808
SERIES = 'MHI-Q SERIES'

# ---------- số liệu: đọc từ MHI-Q.xlsx ----------
wb = openpyxl.load_workbook(W + '/MHI-Q.xlsx', data_only=True)
QH = {}
for r in wb['QH'].iter_rows(min_row=2, values_only=True): QH.setdefault(r[1], []).append((r[2], r[3]))
for k in QH: QH[k].sort()
MOD = {}
for r in wb['MODEL'].iter_rows(min_row=2, values_only=True):
    base = r[2].rsplit(' ', 2)[0]; MOD[base] = dict(kw=r[3], inlet=r[9], outlet=r[10])
def g(v): return '%g' % v
def pump_of(m): return m.replace('Q', '')           # MHI-403Q -> MHI-403
PSET = {'MHI-403Q': '2.4', 'MHI-1604Q': '3.0'}       # áp cài đặt theo IVT-MHI403 / IVT-MHI1604 (DU_LIEU/MHI.xlsx sheet IVT_MHI)
RATED = {'MHI-403Q': 4, 'MHI-1604Q': 16}              # Q định mức 1 bơm (DU_LIEU/MHI.xlsx)
MODELS = list(MOD)
def H_at(m, n, q):
    for Q, Hh in QH[f'{m} {n}']:
        if abs(Q - q) < 1e-9: return Hh
    return None
TECH = []
for m in MODELS:
    one, two = QH[f'{m} 1 pump'], QH[f'{m} 2 pumps']
    qr = RATED[m]; hr = H_at(m, '1 pump', qr)
    TECH.append([m, f'2 × {pump_of(m)}', g(MOD[m]['kw']), g(2 * MOD[m]['kw']), g(one[0][1]),
                 f'{g(qr)} / {g(hr)}', f'{g(2 * qr)} / {g(hr)}', g(one[-1][0]), g(two[-1][0]),
                 f"DN{MOD[m]['inlet']} / DN{MOD[m]['outlet']}", PSET[m]])

# ---------- chữ ----------
FEATURES = ['Two MHI horizontal multi-stage stainless steel pumps on a common base frame',
            'Alternating operation: one pump runs while the other stands by, the pumps take turns',
            'Parallel operation: both pumps run together at peak demand',
            'Frequency inverter control in a stainless steel control cabinet',
            'Stainless steel suction and discharge manifolds with flanged connections',
            'Isolation valves on the suction and discharge of each pump',
            'Pressure tank, pressure gauge and pressure sensor on the discharge manifold']
APPS = ['Water supply and pressure boosting', 'Apartment buildings, hotels and offices',
        'Air-conditioning and industrial circulation systems', 'Washing and sprinkler systems']
OPER = [('Approved fluids', 'Clean water'), ('Fluid temperature', '0–90 °C'), ('Max. suction lift', '8 m'),
        ('Max. pressure', '10 bar'), ('Protection class', 'IP54'), ('Power supply', '3~ 380–415 V 50 Hz'),
        ('Number of pumps', '2 (alternating or parallel)')]
MATS = [('Casing', 'AISI 304 stainless steel'), ('Impeller', 'AISI 304 stainless steel'), ('Shaft', 'AISI 304 stainless steel'),
        ('Mechanical seal', 'Silicon carbide / graphite, resistant to 120 °C'), ('Manifolds', 'Stainless steel'),
        ('Control cabinet', 'Stainless steel')]

class Pg:
    def __init__(self, doc):
        self.p = doc.new_page(width=842, height=595)
        self.p.insert_font(fontname='LR', fontfile=FR); self.p.insert_font(fontname='LB', fontfile=FB)
        self.F = {False: pymupdf.Font(fontfile=FR), True: pymupdf.Font(fontfile=FB)}
    def tl(self, s, z, b=False): return self.F[b].text_length(s, z)
    def t(self, x, y, s, z, b=False, c=TXT, al='l'):
        w = self.tl(s, z, b); x = x - w if al == 'r' else (x - w / 2 if al == 'c' else x)
        self.p.insert_text((x, y), s, fontname='LB' if b else 'LR', fontsize=z, color=c); return w
    def wrap(self, s, z, w, b=False):
        out, cur = [], ''
        for wd in s.split():
            c = (cur + ' ' + wd).strip()
            if self.tl(c, z, b) <= w or not cur: cur = c
            else: out.append(cur); cur = wd
        return out + [cur]
    def rect(self, r, fill=None, col=None, w=0.5): self.p.draw_rect(pymupdf.Rect(r), color=col, fill=fill, width=w)
    def line(self, a, b, c, w=0.5): self.p.draw_line(a, b, color=c, width=w)
    def img(self, r, data, size):
        r = pymupdf.Rect(r); s = min(r.width / size[0], r.height / size[1]); w, h = size[0] * s, size[1] * s
        rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, r.x0 + (r.width + w) / 2, r.y0 + (r.height + h) / 2)
        self.p.insert_image(rr, stream=data); return rr

def head(pg, x, y, s, w):
    pg.t(x, y, s, 9.5, True, BLUE); pg.line((x, y + 4), (x + w, y + 4), BLUE, 0.6); return y + 18
def bullets(pg, x, y, w, items, z=9):
    for it in items:
        for k, ln in enumerate(pg.wrap(it, z, w - 9)):
            if k == 0: pg.p.draw_circle((x + 2.5, y - 3), 1.3, color=None, fill=BLUE)
            pg.t(x + 9, y, ln, z); y += z * 1.32
        y += 2
    return y
def kv(pg, x, y, w, rows, c1, z=9, lead=14, hdr=None):
    if hdr:
        pg.rect((x, y, x + w, y + 14), NAVY); pg.t(x + 4, y + 10, hdr[0], 7.8, True, WHITE); pg.t(x + c1, y + 10, hdr[1], 7.8, True, WHITE); y += 14
    for i, (a, b) in enumerate(rows):
        lines = pg.wrap(b, z, w - c1 - 4); h = lead * len(lines)
        if i % 2 == 0: pg.rect((x, y, x + w, y + h), BAND)
        pg.t(x + 4, y + lead - 4, a, z, True, NAVY)
        for k, ln in enumerate(lines): pg.t(x + c1, y + lead - 4 + k * lead, ln, z)
        y += h
    pg.rect((x, y - sum(lead * len(pg.wrap(b, z, w - c1 - 4)) for _, b in rows), x + w, y), None, LINE, 0.4)
    return y
def frame(pg, doc_logo, title, sub, n, tot):
    pg.rect((200, 0, 842, 64), BAND); pg.img((ML, 10, ML + 150, 54), *doc_logo)
    pg.t(214, 44, 'MHI-Q', 26, True, NAVY)
    pg.t(MR, 30, title, 11, True, NAVY, 'r'); pg.t(MR, 46, sub, 9, False, TXT, 'r')
    pg.line((0, 64), (842, 64), BLUE, 1)
    y = 595 - 22; pg.line((ML, y - 12), (MR, y - 12), rgb('C9D6DE'), 0.5)
    pg.t(ML, y, f'PEROTAC  /  {SERIES}', 7.5, True, GREY); pg.t(MR, y, f'{n:02d} / {tot:02d}', 7.5, False, GREY, 'r')
    pg.t(421, y, 'MHI-Q  ·  twin-pump booster set', 7.5, False, GREY, 'c')

def grid_table(pg, x, y, cols, rows, head_h=26, row_h=15, z=8.5):
    """PEROTAC: kẻ đầy đủ, mảnh. cols: [(tên dòng 1, tên dòng 2, rộng, căn)]"""
    w = sum(c[2] for c in cols)
    pg.rect((x, y, x + w, y + head_h), NAVY)
    xx = x
    for a, b, cw, al in cols:
        cx = xx + cw / 2
        pg.t(cx, y + 11, a, 7.6, True, WHITE, 'c'); pg.t(cx, y + 21, b, 7, False, WHITE, 'c'); xx += cw
    y0 = y; y += head_h
    for i, row in enumerate(rows):
        if i % 2 == 1: pg.rect((x, y, x + w, y + row_h), BAND)
        xx = x
        for k, ((a, b, cw, al), v) in enumerate(zip(cols, row)):
            if al == 'l': pg.t(xx + 5, y + row_h - 4.3, v, z, k == 0, NAVY if k == 0 else TXT)
            else: pg.t(xx + cw / 2, y + row_h - 4.3, v, z, k == 0, NAVY if k == 0 else TXT, 'c')
            xx += cw
        y += row_h
    xx = x
    for c in cols[:-1]: xx += c[2]; pg.line((xx, y0 + head_h), (xx, y), LINE, 0.4)
    for yy in [y0 + head_h + row_h * i for i in range(1, len(rows))]: pg.line((x, yy), (x + w, yy), LINE, 0.4)
    pg.rect((x, y0, x + w, y), None, LINE, 0.4)
    return y

def qh_table(pg, x, y, w, m):
    one = dict(QH[f'{m} 1 pump']); two = dict(QH[f'{m} 2 pumps'])
    qs = sorted(set(two) | {max(one)})
    # H tại Q của 2 bơm lấy từ chính sheet QH; cột Qmax 1 bơm cho hàng 2 bơm: điểm có trong bảng 2 bơm hay không
    one_q = sorted(one)
    c0 = 62; cw = (w - c0) / len(qs)
    pg.rect((x, y, x + w, y + 26), NAVY)
    pg.t(x + 5, y + 11, 'Q  m³/h', 7.6, True, WHITE); pg.t(x + 5, y + 21, 'Q  l/min', 7, False, WHITE)
    for i, q in enumerate(qs):
        cx = x + c0 + cw * i + cw / 2
        pg.t(cx, y + 11, g(q), 7.6, True, WHITE, 'c'); pg.t(cx, y + 21, g(round(q * 1000 / 60)), 7, False, WHITE, 'c')
    y0 = y; y += 26
    for j, (lab, d) in enumerate([('1 pump', one), ('2 pumps', two)]):
        if j == 1: pg.rect((x, y, x + w, y + 15), BAND)
        pg.t(x + 5, y + 10.7, lab, 8.3, True, NAVY)
        for i, q in enumerate(qs):
            v = d.get(q)
            if v is None and j == 1: v = TWO_EXTRA[m].get(q)
            s = '–' if v is None else g(v)
            pg.t(x + c0 + cw * i + cw / 2, y + 10.7, s, 8.3, False, TXT, 'c')
        y += 15
    for i in range(len(qs) + 1): xx = x + c0 + cw * i if i else x + c0; pg.line((xx, y0 + 26), (xx, y), LINE, 0.4)
    pg.line((x, y0 + 41), (x + w, y0 + 41), LINE, 0.4); pg.rect((x, y0, x + w, y), None, LINE, 0.4)
    pg.t(x, y + 13, 'H (m) at Q. "–" = outside the operating range of one pump.', 9, False, GREY)
    return y + 13

# H của 2 bơm tại Qmax của 1 bơm (cột thêm) — đọc từ sheet QH_THEM
TWO_EXTRA = {m: {} for m in MODELS}
if 'QH_THEM' in wb.sheetnames:
    for r in wb['QH_THEM'].iter_rows(min_row=2, values_only=True): TWO_EXTRA[r[1].rsplit(' ', 2)[0]][r[2]] = r[3]

def main():
    src = pymupdf.open(R + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm trục ngang MHI.pdf')
    x = src[0].get_images(full=True)[0][0]; info = src.extract_image(x); LOGO = (info['image'], (info['width'], info['height']))
    ph = open(W + '/img/MHI-Q_PEROTAC.jpg', 'rb').read()
    import PIL.Image as I; PH = (ph, I.open(io.BytesIO(ph)).size)
    doc = pymupdf.open(); tot = 2
    # ---- trang 1
    pg = Pg(doc)
    frame(pg, LOGO, 'TWIN-PUMP BOOSTER SET WITH FREQUENCY INVERTER', '2 × MHI pumps  |  3~ 380–415 V  |  50 Hz', 1, tot)
    pg.img((ML, 76, 300, 342), *PH)
    pg.t(167, 356, '2 × MHI  ·  alternating / parallel operation', 9, False, GREY, 'c')
    y = head(pg, ML, 384, 'OPERATING MODES', 266)
    for t1, t2 in [('Alternating', 'One pump runs, the other stands by; the two pumps take turns.'),
                   ('Parallel', 'Both pumps run together for higher flow at peak demand.')]:
        pg.t(ML, y, t1, 9, True, NAVY)
        L = pg.wrap(t2, 9, 266 - 64)
        for k, ln in enumerate(L): pg.t(ML + 64, y + k * 12, ln, 9)
        y += 12 * len(L) + 6
    y = head(pg, 318, 86, 'FEATURES', 230); y = bullets(pg, 318, y, 230, FEATURES)
    y = head(pg, 318, y + 8, 'APPLICATION SCOPE', 230); bullets(pg, 318, y, 230, APPS)
    y = head(pg, 566, 86, 'OPERATING DATA', MR - 566); y = kv(pg, 566, y - 8, MR - 566, OPER, 100)
    y = head(pg, 566, y + 18, 'MATERIALS', MR - 566); kv(pg, 566, y - 8, MR - 566, MATS, 100, hdr=('COMPONENT', 'MATERIAL'))
    y = head(pg, ML, 468, 'TECHNICAL DATA', MR - ML)
    cols = [('MODEL', '', 74, 'l'), ('PUMPS', '', 82, 'c'), ('P2 per pump', 'kW', 60, 'c'), ('P2 total', 'kW', 52, 'c'),
            ('H max', 'm', 46, 'c'), ('Rated 1 pump', 'Q m³/h / H m', 74, 'c'), ('Rated 2 pumps', 'Q m³/h / H m', 74, 'c'),
            ('Q max 1 pump', 'm³/h', 62, 'c'), ('Q max 2 pumps', 'm³/h', 64, 'c'), ('Pump inlet / outlet', 'DN', 92, 'c'),
            ('Pressure setting', 'bar', 88, 'c')]
    grid_table(pg, ML, y - 8, cols, TECH)
    # ---- trang 2
    pg = Pg(doc)
    frame(pg, LOGO, 'PERFORMANCE CURVES', 'MHI-403Q  ·  MHI-1604Q  |  3~ 380–415 V  |  50 Hz', 2, tot)
    y = head(pg, ML, 86, 'PERFORMANCE CURVES  ·  1 PUMP AND 2 PUMPS IN PARALLEL', MR - ML) + 4
    cw = 380
    for i, m in enumerate(MODELS):
        x = ML + i * (MR - ML - cw)
        pg.t(x, y, m, 10, True, NAVY); pg.t(x + pg.tl(m, 10, True) + 6, y, f'2 × {pump_of(m)}  ·  2 × {g(MOD[m]["kw"])} kW', 9, False, GREY)
        d = pymupdf.open(W + f'/chart_{m.replace("MHI-", "")}.pdf'); ch = d[0].rect.height - 26
        d[0].add_redact_annot(pymupdf.Rect(0, ch, 380, d[0].rect.height)); d[0].apply_redactions(images=0, graphics=0)
        d = pymupdf.open('pdf', d.tobytes())
        r = pymupdf.Rect(x, y + 8, x + cw, y + 8 + ch * cw / 380)
        pg.p.show_pdf_page(r, d, 0, clip=pymupdf.Rect(0, -2, 380, ch))
        # điểm định mức (vòng tròn như bản MHI đã duyệt): quy đổi trục từ vị trí số trên trục của chính biểu đồ
        wd = d[0].get_text('words'); qrow = [w for w in wd if w[4] == '(m³/h)'][0]
        xs = [((w[0] + w[2]) / 2, float(w[4])) for w in wd if abs(w[1] - qrow[1]) < 2 and w[4].replace('.', '').isdigit()]
        ys = [((w[1] + w[3]) / 2, float(w[4])) for w in wd if w[2] < 40 and w[3] < qrow[1] - 2 and w[4].replace('.', '').isdigit()]
        import numpy as np
        ax, bx = np.polyfit([v for _, v in xs], [p for p, _ in xs], 1); ay, by = np.polyfit([v for _, v in ys], [p for p, _ in ys], 1)
        qr = RATED[m]; hr = H_at(m, '1 pump', qr)
        for q in (qr, 2 * qr):
            px, py = r.x0 + (ax * q + bx), r.y0 + 2 + (ay * hr + by)
            pg.p.draw_circle((px, py), 2.6, color=NAVY, fill=WHITE, width=1)
        rated_note = True
        yy = qh_table(pg, x, r.y1 + 8, cw, m)
    for k, ln in enumerate(pg.wrap('Curves at 50 Hz, clean water at 20 °C, kinematic viscosity 1 mm²/s. "2 pumps" = both pumps running in parallel at the same head. Circle = rated point. Typical values, not guaranteed.', 9, MR - ML)):
        pg.t(ML, yy + 22 + k * 12, ln, 9, False, GREY)
    canon = {}
    for p in doc:
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
    doc.set_metadata({'title': 'PEROTAC - MHI-Q twin-pump booster set', 'author': 'PEROTAC'})
    doc.subset_fonts(); doc.save(OUT, garbage=4, deflate=True)
main()
