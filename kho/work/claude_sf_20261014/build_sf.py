# -*- coding: utf-8 -*-
"""Dựng catalogue MỚI dòng SF (nguồn: Catalog bơm nước thải Showfou SF áp cao.pdf, anh gửi 14/10/2026) cho 3 hãng.
Số liệu: SF.xlsx (một nguồn cho bảng + đường + bảng tổng quan). Biểu đồ/bảng: tools/ve_duong_cong.py (thư mục qh/).
Hồ sơ hãng: rules/HO_SO_HANG.json. Khổ: AQUARIS A4 dọc; PEROTAC, REDPUMP A4 ngang.
Dùng: python build_sf.py <gốc kho> <thư mục làm> <thư mục ra>
"""
import sys, os, re, io, json
import pymupdf, openpyxl
from PIL import Image, ImageFilter, ImageDraw

R, W, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
HS = json.load(open(R + '/rules/HO_SO_HANG.json', encoding='utf-8'))
FONTS = {'Liberation Sans': (R + '/vendor/fonts/LiberationSans-Regular.ttf', R + '/vendor/fonts/LiberationSans-Bold.ttf'),
         'Lato': (R + '/vendor/fonts/Lato-Regular.ttf', R + '/vendor/fonts/Lato-Bold.ttf')}
TEN_TEP = 'Bơm chìm nước thải SF áp cao'

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
WHITE = (1, 1, 1)

# ---------- số liệu (đọc từ SF.xlsx, không gõ lại) ----------
wb = openpyxl.load_workbook(W + '/SF.xlsx', data_only=True)
MODELS = [r for r in wb['MODEL'].iter_rows(min_row=2, values_only=True) if r[2]]
QH = {}
for r in wb['QH'].iter_rows(min_row=2, values_only=True):
    QH.setdefault(r[1], []).append((r[2], r[3]))
def fmt(v): return ('%g' % v)
OVERVIEW = []  # (m1, m3, kW, HP, Qmax, Hmax)
for m in MODELS:
    pts = sorted(QH[m[2]])
    OVERVIEW.append((m[1] or '–', m[2], fmt(m[3]), fmt(m[4]), fmt(pts[-1][0]), fmt(pts[0][1])))
KW = [m[3] for m in MODELS]; QMAX = max(p[-1][0] for p in (sorted(v) for v in QH.values())); HMAX = max(v[0][1] for v in (sorted(x) for x in QH.values()))
RANGE = [('Power P2', f'{fmt(min(KW))} – {fmt(max(KW))} kW'), ('Max. flow rate', f'{fmt(QMAX)} m³/h ({fmt(QMAX * 1000 / 60)} l/min)'),
         ('Max. head', f'{fmt(HMAX)} m'), ('Speed', 'n ≈ 2850 /min (2 poles)'), ('Frequency', '50 Hz'),
         ('Single-phase', '1~ 220–240 V 50 Hz'), ('Three-phase', '3~ 380–415 V 50 Hz'), ('Models', f'{len(MODELS)} (three-phase), {sum(1 for m in MODELS if m[1])} (single-phase)')]

# ---------- chữ (từ nguồn Showfou SF; bỏ bảo hành, 60 Hz, ISO 9906; sửa chính tả) ----------
SECTIONS = [('APPLICATIONS', ['For water supply from wells or reservoirs.', 'For domestic use, for civil and industrial applications.',
                              'For garden use and irrigation.']),
            ('OPERATING CONDITIONS', ['Maximum fluid temperature up to +40 °C', 'Maximum sand content: 0.1 %']),
            ('MOTOR AND PUMP', ['Rewindable motor', 'Single-phase: 1~ 220–240 V 50 Hz', 'Three-phase: 3~ 380–415 V 50 Hz',
                                'Can be equipped with a floating switch (single-phase models, suffix F)']),
            ('OPTIONS ON REQUEST', ['Special mechanical seal', 'Other voltages'])]
MATERIALS = [('Impeller', 'Cast aluminium'), ('Strainer', 'AISI 304 stainless steel'), ('Motor external casing', 'AISI 304 stainless steel'),
             ('Top cover', 'AISI 304 stainless steel'), ('Mechanical seal', 'Graphite / ceramic'),
             ('Seal lubricant oil', 'Oil for food machinery and pharmaceutical use')]
NOMEN = [('SF', 'Model'), ('m', 'Single-phase'), ('6', 'Capacity (m³/h)'), ('22', 'Head (m)'), ('0.75', 'Power (kW)'), ('F', 'Floating switch')]
NOMEN_NOTE = 'Example: SFm6-22-0.75F  ·  three-phase models without "m"'
SERIES = 'SF SERIES'
SUB = 'Stainless steel submersible pumps – high head'
GROUPS = {'PEROTAC': [('0.37 – 1.1 kW', 'PE_c1', 'PE_b1'), ('1.5 – 3 kW', 'PE_c2', 'PE_b2'), ('4 – 9.2 kW', 'PE_c3', 'PE_b3')],
          'REDPUMP': [('0.37 – 1.1 kW', 'RE_c1', 'RE_b1'), ('1.5 – 3 kW', 'RE_c2', 'RE_b2'), ('4 – 9.2 kW', 'RE_c3', 'RE_b3')],
          'AQUARIS': [('0.37 – 1.9 kW', 'AQ_c1', 'AQ_b1'), ('2.2 – 9.2 kW', 'AQ_c2', 'AQ_b2')]}

# ---------- ảnh ----------
PHOTO = Image.open(W + '/img/sf_cut.png').convert('RGBA')
def logo_bytes(h):
    b = io.BytesIO(); Image.open(W + f'/img/logo_{h}.png').convert('RGB').save(b, 'PNG'); return b.getvalue(), Image.open(W + f'/img/logo_{h}.png').size

def photo_with_shadow(kind):
    """kind: none | contact (AQUARIS, tiếp xúc mờ) | drop (REDPUMP, bóng đổ dưới đế). Trả PNG RGBA."""
    p = PHOTO
    if kind == 'none':
        b = io.BytesIO(); p.save(b, 'PNG'); return b.getvalue(), p.size
    pad = 40
    W_, H_ = p.width + 2 * pad, p.height + pad
    base = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    sh = Image.new('L', (W_, H_), 0); d = ImageDraw.Draw(sh)
    cx = pad + p.width * 0.52; y = p.height - 6
    if kind == 'contact':
        d.ellipse((cx - p.width * 0.36, y - 8, cx + p.width * 0.36, y + 14), fill=int(255 * 0.22)); sh = sh.filter(ImageFilter.GaussianBlur(7))
    else:
        d.ellipse((cx - p.width * 0.30 + 18, y - 4, cx + p.width * 0.42 + 18, y + 26), fill=int(255 * 0.25)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    shadow = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); shadow.putalpha(sh)
    base.alpha_composite(shadow); base.alpha_composite(p, (pad, 0))
    b = io.BytesIO(); base.save(b, 'PNG'); return b.getvalue(), base.size

# ---------- trợ giúp vẽ ----------
class Pg:
    def __init__(self, doc, w, h, fam):
        self.p = doc.new_page(width=w, height=h); self.w, self.h = w, h
        self.fr, self.fb = FONTS[fam]
        self.p.insert_font(fontname='LR', fontfile=self.fr); self.p.insert_font(fontname='LB', fontfile=self.fb)
        self.F = {False: pymupdf.Font(fontfile=self.fr), True: pymupdf.Font(fontfile=self.fb)}
    def tl(self, s, size, bold=False): return self.F[bold].text_length(s, size)
    def t(self, x, y, s, size, bold=False, color=(0, 0, 0), align='l'):
        w = self.tl(s, size, bold)
        if align == 'r': x -= w
        elif align == 'c': x -= w / 2
        self.p.insert_text((x, y), s, fontname='LB' if bold else 'LR', fontsize=size, color=color); return w
    def wrap(self, s, size, width, bold=False):
        out, cur = [], ''
        for wd in s.split():
            c = (cur + ' ' + wd).strip()
            if self.tl(c, size, bold) <= width or not cur: cur = c
            else: out.append(cur); cur = wd
        return out + [cur]
    def rect(self, r, fill, color=None, width=0.5): self.p.draw_rect(pymupdf.Rect(r), color=color, fill=fill, width=width)
    def line(self, a, b, color, width=0.5): self.p.draw_line(a, b, color=color, width=width)
    def img(self, rect, data, size):
        r = pymupdf.Rect(rect); s = min(r.width / size[0], r.height / size[1]); w, h = size[0] * s, size[1] * s
        rr = pymupdf.Rect(r.x0 + (r.width - w) / 2, r.y0 + (r.height - h) / 2, 0, 0); rr.x1 = rr.x0 + w; rr.y1 = rr.y0 + h
        self.p.insert_image(rr, stream=data); return rr
    def block(self, name, rect):
        d = pymupdf.open(W + f'/qh/{name}.pdf'); r = d[0].rect
        tgt = pymupdf.Rect(rect[0], rect[1], rect[0] + r.width, rect[1] + r.height)
        self.p.show_pdf_page(tgt, d, 0); return tgt

def sections(pg, x, y, w, head, body, hcol, tcol, size=9, gap=7):
    for title, lines in SECTIONS:
        y = head(pg, x, y, title, w)
        for l in lines:
            for k, ln in enumerate(pg.wrap(l, size, w - 8)):
                if k == 0: pg.p.draw_circle((x + 2.5, y - 3), 1.3, color=None, fill=hcol)
                pg.t(x + 8, y, ln, size, False, tcol); y += size * 1.3
        y += gap
    return y

def kv_table(pg, x, y, w, rows, c1, size, fill_a, fill_b, tcol, kcol, lead=13, wrapw=None):
    for i, (a, b) in enumerate(rows):
        lines = pg.wrap(b, size, wrapw) if wrapw else [b]
        hgt = lead * len(lines)
        f = fill_a if i % 2 == 0 else fill_b
        if f: pg.rect((x, y, x + w, y + hgt), f)
        pg.t(x + 4, y + lead - 3.8, a, size, True, kcol)
        for k, ln in enumerate(lines): pg.t(x + c1, y + lead - 3.8 + k * lead, ln, size, False, tcol)
        y += hgt
    return y

def overview_table(pg, x, y, w, size, head_fill, head_col, fill_a, fill_b, tcol, line_col=None, bold_col=None):
    cols = [('MODEL|1~', 0.25, 'l'), ('MODEL|3~', 0.23, 'l'), ('P2|kW', 0.11, 'r'), ('P2|HP', 0.11, 'r'),
            ('Q max|m³/h', 0.15, 'r'), ('H max|m', 0.15, 'r')]
    xs = [x]; [xs.append(xs[-1] + w * c[1]) for c in cols]
    pg.rect((x, y, x + w, y + 23), head_fill)
    for (n, _, al), x0, x1 in zip(cols, xs, xs[1:]):
        a, b = n.split('|')
        pg.t(x0 + 4 if al == 'l' else x1 - 4, y + 10, a, 7.5, True, head_col, al)
        pg.t(x0 + 4 if al == 'l' else x1 - 4, y + 19, b, 7, False, head_col, al)
    y += 23
    for i, row in enumerate(OVERVIEW):
        f = fill_a if i % 2 == 0 else fill_b
        if f: pg.rect((x, y, x + w, y + 13), f)
        for k, ((n, _, al), x0, x1) in enumerate(zip(cols, xs, xs[1:])):
            pg.t(x0 + 4 if al == 'l' else x1 - 4, y + 9.4, row[k], size, k == 1, (bold_col if k == 1 and bold_col else tcol), al)
        if line_col: pg.line((x, y + 13), (x + w, y + 13), line_col, 0.4)
        y += 13
    return y

def nomen(pg, x, y, w, big_col, lab_col, line_col, size_big=13):
    n = len(NOMEN); cw = w / n
    for i, (a, b) in enumerate(NOMEN):
        cx = x + cw * i + cw / 2
        pg.t(cx, y + 12, a, size_big, True, big_col, 'c')
        pg.line((cx - cw / 2 + 3, y + 17), (cx + cw / 2 - 3, y + 17), line_col, 0.6)
        lines = pg.wrap(b, 7, cw - 2)
        for k, ln in enumerate(lines): pg.t(cx, y + 26 + k * 8.5, ln, 7, False, lab_col, 'c')
    yy = y + 52
    for ln in pg.wrap(NOMEN_NOTE, 9, w): pg.t(x, yy, ln, 9, False, lab_col); yy += 11.5
    return yy - 4

def footer(pg, brand, n, tot, col, line_col, y=None):
    y = y or pg.h - 22
    pg.line((34, y - 12), (pg.w - 34, y - 12), line_col, 0.5)
    pg.t(34, y, f'{brand}  /  {SERIES}', 7.5, True, col); pg.t(pg.w - 34, y, f'{n:02d} / {tot:02d}', 7.5, False, col, 'r')

# ====================== PEROTAC ======================
def build_perotac(doc):
    H = HS['hang']['PEROTAC']['mau']; NAVY, BLUE, BAND = rgb(H['chinh']), rgb(H['duong']), rgb(H['nen'])
    TXT, GREY = rgb('1F3847'), rgb('5C6E78'); LG = logo_bytes('PEROTAC'); ML, MR = 34, 808
    def head(pg, x, y, s, w):
        pg.t(x, y, s, 9.5, True, BLUE); pg.line((x, y + 4), (x + w, y + 4), BLUE, 0.6); return y + 18
    def frame(pg, title, sub, n):
        pg.rect((200, 0, 842, 64), BAND); pg.img((ML, 10, ML + 150, 54), *LG)
        pg.t(214, 44, SERIES, 26, True, NAVY)
        pg.t(MR, 30, title, 11, True, NAVY, 'r'); pg.t(MR, 46, sub, 9, False, TXT, 'r')
        pg.line((0, 64), (842, 64), BLUE, 1); footer(pg, 'PEROTAC', n, len(GROUPS['PEROTAC']) + 1, GREY, rgb('C9D6DE'))
    # trang 1
    pg = Pg(doc, 842, 595, 'Liberation Sans')
    frame(pg, 'STAINLESS STEEL SUBMERSIBLE PUMP – HIGH HEAD', '1~ 220–240 V  |  3~ 380–415 V  |  50 Hz  |  n ≈ 2850 /min', 1)
    # ảnh đại diện PEROTAC: 2 ảnh anh gửi 14/10 16:35 (không phao = 3 pha, có phao = 1 pha), nền trắng, không bóng
    for k, (f, cap) in enumerate((('khong_phao', ['Three-phase', 'SF…']), ('co_phao', ['Single-phase, floating switch', 'SFm…F']))):
        im = Image.open(W + f'/img/sf_pe_{f}.png'); bb = io.BytesIO(); im.save(bb, 'PNG')
        x0 = ML + k * 120
        r = pg.img((x0, 84, x0 + 116, 256), bb.getvalue(), im.size)
        for j, c in enumerate(cap): pg.t(x0 + 58, r.y1 + 14 + j * 10, c, 7.5, j == 1, NAVY if j else TXT, 'c')
    y = head(pg, ML, 312, 'RANGE CHARACTERISTICS', 236)
    kv_table(pg, ML, y - 10, 236, RANGE, 82, 8.3, BAND, None, TXT, NAVY, 13.5, wrapw=150)
    sections(pg, 292, 88, 250, head, None, BLUE, TXT)
    y = head(pg, 560, 88, 'MODEL CODE', 248); y = nomen(pg, 560, y - 8, 248, NAVY, GREY, rgb('C9D6DE'))
    y = head(pg, 560, y + 10, 'MATERIALS', 248)
    pg.rect((560, y - 8, MR, y + 6), NAVY); pg.t(564, y + 2, 'COMPONENT', 7.8, True, WHITE); pg.t(560 + 104, y + 2, 'MATERIAL', 7.8, True, WHITE)
    kv_table(pg, 560, y + 6, 248, MATERIALS, 104, 9, BAND, None, TXT, NAVY, 13.5, wrapw=140)
    y = head(pg, 292, 362, 'RANGE OVERVIEW', MR - 292)
    overview_table(pg, 292, y - 8, MR - 292, 8, NAVY, WHITE, BAND, None, TXT, rgb('C9D6DE'), NAVY)
    # trang 2, 3
    for i, (grp, c, b) in enumerate(GROUPS['PEROTAC']):
        pg = Pg(doc, 842, 595, 'Liberation Sans')
        frame(pg, 'PERFORMANCE & TECHNICAL DATA', f'Models {grp}  |  50 Hz  |  n ≈ 2850 /min', i + 2)
        y = head(pg, ML, 84, f'PERFORMANCE CURVES  ·  {grp}', MR - ML)
        cr = pg.block(c, (ML, y - 6))
        y = head(pg, ML, cr.y1 + 16, 'PERFORMANCE DATA', MR - ML)
        pg.block(b, (ML, y - 6))

# ====================== REDPUMP ======================
def build_redpump(doc):
    H = HS['hang']['REDPUMP']['mau']; DARK, RED, BG = rgb(H['chinh']), rgb(H['nhan']), rgb(H['nen'])
    TXT, GREY, LIGHT = rgb('2B2E33'), rgb('5E6166'), rgb('D9DADC'); LG = logo_bytes('REDPUMP'); CW = 245; X0, MR = 268, 808
    def head(pg, x, y, s, w, dark=False):
        pg.rect((x, y - 8.5, x + 3, y + 1.5), RED); pg.t(x + 8, y, s, 9.5, True, WHITE if dark else DARK); return y + 16
    def head_main(pg, x, y, s, w): return head(pg, x, y, s, w)
    def column(pg, n):
        pg.rect((0, 0, CW, 595), DARK)
        pg.t(24, 46, 'SF SERIES', 9, True, LIGHT); pg.t(24, 84, 'SF', 40, True, WHITE)
        for k, ln in enumerate(['Stainless steel submersible pumps', 'High head']): pg.t(24, 104 + k * 13, ln, 10, False, LIGHT)
        pg.rect((24, 128, 64, 131), RED)
        footer_y = 573; pg.t(24, footer_y, f'REDPUMP  /  {SERIES}', 7.5, True, LIGHT)
        pg.t(MR, footer_y, f'{n:02d} / {len(GROUPS["REDPUMP"]) + 1:02d}', 7.5, False, GREY, 'r')
    def logo(pg): pg.img((MR - 120, 18, MR, 64), *LG)
    # trang 1
    pg = Pg(doc, 842, 595, 'Liberation Sans'); column(pg, 1)
    y = head(pg, 24, 160, 'RANGE CHARACTERISTICS', CW - 48, True)
    for a, b in RANGE:
        lines = pg.wrap(b, 8.5, CW - 48 - 82)
        pg.t(24, y, a, 8.5, False, LIGHT)
        for k, ln in enumerate(lines): pg.t(24 + 82, y + k * 11.5, ln, 8.5, True, WHITE)
        y += 11.5 * len(lines) + 3
    y = head(pg, 24, y + 14, 'MODEL CODE', CW - 48, True)
    pg.t(24, y + 8, 'SFm6-22-0.75F', 14, True, WHITE); y += 26
    for a, b in NOMEN:
        pg.t(24, y, a, 9, True, rgb('E8A3A5')); pg.t(64, y, b, 8.5, False, LIGHT); y += 13
    pg.t(24, y + 4, 'Three-phase models without "m".', 8.5, False, LIGHT)
    logo(pg)
    pg.t(X0, 40, 'STAINLESS STEEL SUBMERSIBLE PUMP', 16, True, DARK)
    pg.t(X0, 58, 'High head  |  1~ 220–240 V  |  3~ 380–415 V  |  50 Hz  |  n ≈ 2850 /min', 9, False, GREY)
    sections(pg, X0, 88, 300, head_main, None, RED, TXT)
    pg.rect((590, 82, MR, 312), WHITE); ph = photo_with_shadow('drop'); pg.img((600, 84, MR, 296), *ph)
    y = head(pg, X0, 336, 'TECHNICAL SHEET – MATERIALS', MR - X0)
    yy = kv_table(pg, X0, y - 8, 236, MATERIALS, 104, 9, BG, None, TXT, DARK, 13.5, wrapw=128)
    y2 = head(pg, 520, 336, 'RANGE OVERVIEW', MR - 520)
    overview_table(pg, 520, y2 - 8, MR - 520, 7.5, DARK, WHITE, None, rgb('EFEFEF'), TXT, None, RED)
    # trang 2, 3
    for i, (grp, c, b) in enumerate(GROUPS['REDPUMP']):
        pg = Pg(doc, 842, 595, 'Liberation Sans'); column(pg, i + 2)
        y = head(pg, 24, 160, 'PERFORMANCE DATA', CW - 48, True)
        for a, bb in [('Models', grp)] + ([('Single-phase', '1~ 220–240 V 50 Hz')] if i < 2 else []) + [('Three-phase', '3~ 380–415 V 50 Hz'), ('Speed', 'n ≈ 2850 /min'), ('Poles', '2')]:
            pg.t(24, y, a, 8.5, False, LIGHT); pg.t(24 + 82, y, bb, 8.5, True, WHITE); y += 14.5
        ph = photo_with_shadow('none'); pg.img((40, y + 20, CW - 40, y + 20 + 200), *ph)
        logo(pg)
        pg.t(X0, 40, f'PERFORMANCE & TECHNICAL DATA', 16, True, DARK); pg.t(X0, 58, f'SF SERIES  ·  {grp}', 9, False, GREY)
        cr = pg.block(c, (X0, 74))
        y = head(pg, X0, cr.y1 + 20, 'PERFORMANCE TABLE', MR - X0)
        pg.block(b, (X0, y - 4))

# ====================== AQUARIS ======================
def build_aquaris(doc):
    H = HS['hang']['AQUARIS']['mau']; GREEN, BG = rgb(H['chinh']), rgb(H['nen']); FLAG = [rgb(c) for c in H['co_y']]
    TXT, GREY = rgb('1E2B2A'), rgb('5B6B69'); LG = logo_bytes('AQUARIS'); ML, MR = 34, 561
    def head(pg, x, y, s, w):
        pg.t(x, y, s, 9.5, True, GREEN); pg.line((x, y + 4), (x + w, y + 4), GREEN, 0.5); return y + 17
    def frame(pg, title, sub, n):
        for k, c in enumerate(FLAG): pg.rect((ML + k * 60, 0, ML + 60 + k * 60, 5), c, rgb('DDDDDD') if c == WHITE else None, 0.3)
        pg.t(ML, 50, title, 24, True, GREEN); pg.t(ML, 66, sub, 9, False, GREY)
        pg.img((MR - 120, 18, MR, 62), *LG)
        footer(pg, 'AQUARIS', n, 3, GREY, rgb('C9D9D6'), 822)
    pg = Pg(doc, 595, 842, 'Lato')
    frame(pg, SERIES, SUB.upper().replace('–', '·'), 1)
    ph = photo_with_shadow('contact'); pg.img((ML, 84, 230, 300), *ph)
    kpi = [(f'{fmt(min(KW))}–{fmt(max(KW))} kW', 'POWER P2'), (f'{fmt(QMAX)} m³/h', 'MAX. FLOW RATE'), (f'{fmt(HMAX)} m', 'MAX. HEAD'),
           ('50 Hz', 'FREQUENCY'), ('1~ / 3~', '220–240 V / 380–415 V'), ('2850 /min', 'SPEED · 2 POLES')]
    bx, by, bw, bh = 248, 92, 151, 62
    for k, (v, l) in enumerate(kpi):
        cx = bx + (k % 2) * (bw + 11); cy = by + (k // 2) * (bh + 10)
        pg.rect((cx, cy, cx + bw, cy + bh), BG); pg.line((cx, cy), (cx + bw, cy), GREEN, 1.2)
        pg.t(cx + bw / 2, cy + 30, v, 15, True, GREEN, 'c'); pg.t(cx + bw / 2, cy + 47, l, 7.5, False, GREY, 'c')
    y1 = sections(pg, ML, 330, 255, head, None, GREEN, TXT)
    y = head(pg, 306, 330, 'MODEL CODE', 255); y = nomen(pg, 306, y - 8, 255, GREEN, GREY, rgb('C9D9D6'))
    y = head(pg, 306, y + 12, 'MATERIALS', 255)
    y2 = kv_table(pg, 306, y - 8, 255, MATERIALS, 108, 9, BG, None, TXT, GREEN, 13.5, wrapw=144)
    y = head(pg, ML, max(y1, y2) + 18, 'RANGE OVERVIEW', MR - ML)
    overview_table(pg, ML, y - 8, MR - ML, 8, GREEN, WHITE, None, None, TXT, rgb('C9D9D6'), GREEN)
    for i, (grp, c, b) in enumerate(GROUPS['AQUARIS']):
        pg = Pg(doc, 595, 842, 'Lato')
        frame(pg, 'SF  ' + grp, 'PERFORMANCE & TECHNICAL DATA  ·  50 Hz  ·  n ≈ 2850 /min', i + 2)
        y = head(pg, ML, 96, 'PERFORMANCE CURVES', MR - ML)
        cr = pg.block(c, (ML, y - 4))
        y = head(pg, ML, cr.y1 + 18, 'PERFORMANCE DATA', MR - ML)
        pg.block(b, (ML, y - 4))

def finish(doc, path, brand):
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
    doc.set_metadata({'title': f'{brand} - {SERIES}', 'author': brand})
    doc.subset_fonts()
    # Lato: glyph gạch nối được ToUnicode ghi U+2010 → đổi về U+002D để tìm chữ / chép mã đúng
    for x in range(1, doc.xref_length()):
        if doc.xref_get_key(x, 'Type')[1] == '/Font' and doc.xref_get_key(x, 'ToUnicode')[0] == 'xref':
            tu = int(doc.xref_get_key(x, 'ToUnicode')[1].split()[0]); st = doc.xref_stream(tu)
            if b'<2010>' in st: doc.update_stream(tu, st.replace(b'<2010>', b'<002D>'))
    doc.save(path, garbage=4, deflate=True)
    print('saved', path, os.path.getsize(path))

os.makedirs(OUT, exist_ok=True)
for brand, fn in (('AQUARIS', build_aquaris), ('PEROTAC', build_perotac), ('REDPUMP', build_redpump)):
    d = pymupdf.open(); fn(d); finish(d, f'{OUT}/{brand} - {TEN_TEP}.pdf', brand)
