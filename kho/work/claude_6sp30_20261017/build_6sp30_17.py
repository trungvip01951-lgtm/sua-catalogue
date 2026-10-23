# REDPUMP 6SP30 (catalogue riêng, A4 dọc) — bản 17: vá trên bản 16 (ad416b37fb9b)
# Trang 1: giữ nguyên, thêm dòng thông số cạnh tiêu đề + khối điều kiện dưới bảng.
# Trang 2: dựng lại: bảng kích thước P/M/T (bỏ cột khối lượng, QĐ 114), sơ đồ kích thước,
#          ảnh sản phẩm (KHO_ANH a1c9a2f70465.png, ảnh 6SP đang dùng ở REDPUMP SP tr.10),
#          bảng vật liệu (theo REDPUMP - Bơm giếng SP.pdf tr.10, dải 6SP), bảng thông số kỹ thuật.
# Dùng: python build_6sp30_17.py <ban16.pdf> <anh.png> <thu_muc_phong> <ra.pdf> [A|B]
import sys, pymupdf as f
SRC, IMG, FD, OUT = sys.argv[1:5]
FULL = len(sys.argv) > 5 and sys.argv[5] == "B"   # B: thêm 4 dòng vật liệu AQUARIS 6SP30 + khối Applications / Operating conditions
DARK = (0.16, 0.17, 0.19); HDR = (0.235, 0.245, 0.26); STRIPE = (0.985, 0.971, 0.967)
LINE = (0.59, 0.55, 0.54); TITLE = (0.47, 0.094, 0.122); WHITE = (1, 1, 1)
d = f.open(SRC)
logo = d.extract_image(87)["image"]

def fonts(p):
    p.insert_font(fontname="LS", fontfile=FD + "/LiberationSans-Regular.ttf")
    p.insert_font(fontname="LSB", fontfile=FD + "/LiberationSans-Bold.ttf")

def txt(p, x, y, s, size, bold=False, color=DARK, align=0, width=None):
    fn = "LSB" if bold else "LS"
    w = f.get_text_length(s, fontname="helv") if False else None
    font = f.Font(fontfile=FD + ("/LiberationSans-Bold.ttf" if bold else "/LiberationSans-Regular.ttf"))
    tw = font.text_length(s, size)
    if align == 1: x = x - tw / 2
    elif align == 2: x = x - tw
    p.insert_text((x, y), s, fontname=fn, fontsize=size, color=color)
    return tw

def table(p, x, y, cols, head, rows, rh=12.0, hh=15.0, size=7.5, aligns=None):
    w = sum(cols); aligns = aligns or [1] * len(cols)
    sh = p.new_shape()
    sh.draw_rect(f.Rect(x, y, x + w, y + hh)); sh.finish(fill=HDR, color=None)
    for i in range(len(rows)):
        if i % 2 == 1:
            sh.draw_rect(f.Rect(x, y + hh + i * rh, x + w, y + hh + (i + 1) * rh)); sh.finish(fill=STRIPE, color=None)
    yb = y + hh + len(rows) * rh
    for k in range(len(rows) + 2):
        yy = y if k == 0 else y + hh + (k - 1) * rh
        sh.draw_line((x, yy), (x + w, yy))
    xx = x
    for c in [0] + cols:
        xx += c; sh.draw_line((xx, y), (xx, yb))
    sh.finish(color=LINE, width=0.6); sh.commit()
    def cell(i, j, s, yy, bold, color, sz):
        x0 = x + sum(cols[:j]); a = aligns[j]
        tx = x0 + 6 if a == 0 else (x0 + cols[j] / 2 if a == 1 else x0 + cols[j] - 6)
        txt(p, tx, yy, s, sz, bold, color, align=a)
    for j, s in enumerate(head): cell(-1, j, s, y + hh / 2 + size * 0.36, True, WHITE, size)
    for i, r in enumerate(rows):
        for j, s in enumerate(r): cell(i, j, s, y + hh + i * rh + rh / 2 + size * 0.36, j == 0 and len(cols) > 2 and False, DARK, size)
    return yb

# ---------- trang 1 ----------
p1 = d[0]; fonts(p1)
txt(p1, 507, 32.0, "3~ 380–415 V 50 Hz   |   n ≈ 2850 /min   |   IP68   |   Motor IE3", 9, True, DARK, align=2)
txt(p1, 297.6, 780.5, "Curves at 50 Hz, 2 poles, n ≈ 2850 /min, clean water at 20 °C, 1 mm²/s. Typical values, not guaranteed.",
    9, False, DARK, align=1)

# ---------- trang 2 (dựng lại) ----------
old = d[1]
dims = []
spans = [s for b in old.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]
rowsy = sorted({round(s["bbox"][1], 1) for s in spans if s["text"].startswith("6SP30-")})
for y in rowsy:
    r = sorted([s for s in spans if round(s["bbox"][1], 1) == y], key=lambda s: s["bbox"][0])
    dims.append([s["text"] for s in r][:4])          # MODEL, P, M, T — bỏ Pump/Motor/Total (kg)
assert len(dims) == 9 and all(len(r) == 4 for r in dims), dims
d.delete_page(1)
p2 = d.new_page(-1, width=595.28, height=841.89); fonts(p2)
txt(p2, 69.6, 33.6, "6SP30  |  Outlet 3 in", 12, True, TITLE)
yb = table(p2, 69.6, 46, [114, 114, 114, 114], ["MODEL", "P (mm)", "M (mm)", "T (mm)"], dims, rh=14, hh=18, size=8.5)
txt(p2, 69.6, yb + 14, "Dimensions: mm   |   3~ 380–415 V 50 Hz", 9)

# khối dưới: ảnh | sơ đồ kích thước | vật liệu + thông số
Y0 = yb + 52
# ảnh sản phẩm (ppi >= 200: 692 px / 245 pt * 72 = 203)
ih = 245.0; iw = ih * 230 / 692; ix = 60.0
p2.insert_image(f.Rect(ix, Y0, ix + iw, Y0 + ih), filename=IMG)
# bóng đổ dưới đế: vẽ SAU ảnh (ảnh nền trắng đặc sẽ che bóng nếu vẽ trước)
sh = p2.new_shape()
for k, (rx, ry, op) in enumerate([(48, 5.5, 0.05), (40, 4.3, 0.07), (32, 3.2, 0.09), (24, 2.2, 0.11)]):
    cx, cy = ix + iw / 2, Y0 + ih - 1.0
    sh.draw_oval(f.Rect(cx - rx, cy - ry, cx + rx, cy + ry)); sh.finish(fill=(0, 0, 0), color=None, fill_opacity=op)
sh.commit()
txt(p2, ix + iw / 2, Y0 + ih + 22, "6SP30", 9, True, TITLE, align=1)
# sơ đồ kích thước (vẽ lại sơ đồ bản 16, phóng 1,6 lần)
S = 1.6; ox, oy = 156.0, Y0 + 30
X = lambda x: ox + (x - 264.0) * S; Yy = lambda y: oy + (y - 204.0) * S
sh = p2.new_shape()
for (a, b, c_, e) in [(279.6, 204, 306, 204), (279.6, 204, 279.6, 283.3), (306, 204, 306, 283.3), (279.6, 283.3, 306, 283.3), (279.6, 251.6, 306, 251.6)]:
    sh.draw_line((X(a), Yy(b)), (X(c_), Yy(e)))
sh.finish(color=DARK, width=0.8)
for (a, b, c_, e) in [(284.4, 220.8, 301.2, 220.8), (284.4, 235.2, 301.2, 235.2)]:
    sh.draw_line((X(a), Yy(b)), (X(c_), Yy(e)))
sh.finish(color=(0.80, 0.78, 0.77), width=0.5)
for (a, b, c_, e) in [(267.6, 204, 267.6, 251.6), (264, 204, 271.2, 204), (264, 251.6, 271.2, 251.6), (267.6, 251.6, 267.6, 283.3),
                      (264, 283.3, 271.2, 283.3), (320.4, 204, 320.4, 283.3), (316.8, 204, 324, 204), (316.8, 283.3, 324, 283.3)]:
    sh.draw_line((X(a), Yy(b)), (X(c_), Yy(e)))
sh.finish(color=DARK, width=0.7); sh.commit()
txt(p2, X(292.8), Yy(199), "DN", 9, True, align=1)
txt(p2, X(259.5), Yy(229.5), "P", 9, True, align=1)
txt(p2, X(259.5), Yy(269.5), "M", 9, True, align=1)
txt(p2, X(328.5), Yy(245.5), "T", 9, True, align=1)
txt(p2, X(292.8), Yy(296), "Ø 145 mm", 9, align=1)
txt(p2, X(292.8), Yy(306), "Motor Ø 145 mm", 9, align=1)

# vật liệu (REDPUMP - Bơm giếng SP.pdf tr.10, dải 6SP)
TX = 320.6; cols = [95, 110]
txt(p2, TX, Y0 - 6, "COMPONENTS AND MATERIALS", 9, True, TITLE)
MAT = [("Delivery casing", "AISI 304 SS"), ("Suction lantern", "AISI 304 SS"), ("Diffuser", "AISI 304 SS"),
       ("Impeller", "AISI 304 SS"), ("Pump shaft", "AISI 316 SS"), ("Shaft coupling", "AISI 316 SS"),
       ("Wear ring", "Rubber"), ("Motor external casing", "AISI 304 SS"), ("Seal", "NBR Graphite-SIC/TC"),
       ("Motor shaft", "AISI 304 SS-ASTM 5140")]
if FULL:   # 4 dòng REDPUMP không có, lấy từ AQUARIS - Bơm giếng SP.pdf tr.21 (6SP30)
    MAT.insert(1, ("Check valve", "AISI 304 / AISI 316 SS"))
    MAT.insert(9, ("Top cover", "Cast iron G20 UNI5007 / AISI 304 SS"))
    MAT += [("Thrust bearing", "Ceramic/Carbon"), ("Radial bearing", "Ceramic/TC")]
cols = [100, 110] if not FULL else [96, 152]; MS = 8.5 if not FULL else 8.0; TX = 525.6 - sum(cols)
yb2 = table(p2, TX, Y0, cols, ["COMPONENT", "MATERIAL"], [list(m) for m in MAT], rh=14, hh=18, size=MS, aligns=[0, 0])
Y2 = yb2 + 30
txt(p2, TX, Y2 - 6, "MOTOR DATA", 9, True, TITLE)
TEC = [("Power supply", "3~ 380–415 V 50 Hz"), ("Speed", "n ≈ 2850 /min"), ("Protection grade", "IP68"),
       ("Efficiency class", "IE3"), ("Motor diameter", "Ø 145 mm")]
yb3 = table(p2, TX, Y2, cols, ["ITEM", "VALUE"], [list(t) for t in TEC], rh=14, hh=18, size=MS, aligns=[0, 0])
if FULL:   # chữ lấy từ REDPUMP - Bơm giếng SP.pdf tr.10 (6SP); bỏ dòng ISO 9906 (QĐ 149)
    def block(x, y, items):
        for head, lines in items:
            txt(p2, x, y, head, 9, True, TITLE); y += 13
            for l in lines: txt(p2, x, y, l, 9); y += 12
            y += 8
        return y
    block(69.6, Y0 + ih + 52, [("APPLICATIONS", ["For water supply from wells or reservoirs", "For domestic use, for civil and",
                                                   "industrial applications",
                                                   "For garden use and irrigation"]),
                                 ("OPERATING CONDITIONS", ["Maximum fluid temperature: 50 °C", "Maximum sand content: 0.25%", "Minimum well diameter: 6 in"])])
    block(TX, yb3 + 30, [("MOTOR AND PUMP", ["Rewindable motor", "1. Direct start (1 cable)", "2. Star-delta start (2 cables)",
                                             "Equipped with start control box or", "digital auto-control box", "NEMA dimension standards"]),
                         ("OPTIONS ON REQUEST", ["Special mechanical seal"])])
p2.insert_image(f.Rect(259.3, 786.3, 336.0, 820.3), stream=logo)
d.set_metadata({**d.metadata, "title": "REDPUMP 6SP30", "author": "", "creator": "", "producer": ""})
d.save(OUT, garbage=4, deflate=True)
print("OK", OUT, dims[0], dims[-1])
