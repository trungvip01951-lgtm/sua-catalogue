# Vá AQUARIS - Bơm trục ngang CM.pdf: thay số 3 mã theo báo giá anh gửi 30/10/2026 (QĐ 165) — vá đúng chỗ (QTH 4b).
# Mỗi mã: thay đường (1 Bezier bậc 3 cùng màu/nét), dời số nhãn đường, thay ô bảng (chữ cùng phông, căn giữa ô cũ). Không ghi đè bản đã duyệt.
import sys, re, json, numpy as np, pymupdf, openpyxl
from decimal import Decimal, ROUND_HALF_UP
R, OUT, CFG = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3], encoding='utf-8'))
SRC = R + '/CATALOG SUA/CATALOGUE DA DUYET/AQUARIS/AQUARIS - Bơm trục ngang CM.pdf'
doc = pymupdf.open(SRC); HP = doc[0].rect.height
cu = {}
for r in openpyxl.load_workbook(R + '/DU_LIEU/CM.xlsx', data_only=True)['QH'].iter_rows(min_row=2, values_only=True):
    if r[0] == 'AQUARIS': cu.setdefault(r[1], []).append((r[2], r[3]))
for k in cu: cu[k].sort()
hx = lambda t: ''.join('%04x' % ord(c) for c in t)
un = lambda h: ''.join(chr(int(h[i:i+4], 16)) for i in range(0, len(h), 4))
NUM = r'-?[\d.]+'
TOP = re.compile(r'BT /(\S+) ([\d.]+) Tf (\S+) Tc ([\d. ]+?) rg 1 0 0 1 (' + NUM + r') (' + NUM + r') Tm <([0-9a-fA-F]+)> Tj (\S+) Tc ET')
PATH = re.compile(r'([\d.]+ [\d.]+ [\d.]+) RG ([\d.]+) w 1 J 1 j (' + NUM + r') (' + NUM + r') m (' + NUM + r') (' + NUM + r') (' + NUM + r') (' + NUM + r') (' + NUM + r') (' + NUM + r') c S')
bao = []
for pg, models in CFG.items():
    p = doc[int(pg) - 1]; xr = p.get_contents(); assert len(xr) == 1; s = doc.xref_stream(xr[0]).decode('latin1')
    texts = [dict(m=m, font=m.group(1), size=float(m.group(2)), col=m.group(4), x=float(m.group(5)), y=float(m.group(6)), t=un(m.group(7))) for m in TOP.finditer(s)]
    paths = list(PATH.finditer(s))
    # màu đường theo mã: vạch màu trước tên mã trong bảng
    def mau(md):
        tm = [t for t in texts if t['t'] == md and t['y'] < 300]; assert len(tm) == 1, (md, tm)
        y = tm[0]['y']; c = [mm for mm in re.finditer(r'([\d.]+ [\d.]+ [\d.]+) rg (' + NUM + r') (' + NUM + r') 8 3 re f', s) if abs(float(mm.group(3)) - (y + 1.3)) < 1.5]
        assert len(c) == 1, (md, len(c)); return c[0].group(1), tm[0]
    # hệ trục: khớp tuyến tính từ điểm đầu/cuối các đường cũ ↔ số cũ
    X, Y = [], []
    for md in [t['t'] for t in texts if t['t'].startswith('CM ') and t['y'] < 300 and t['t'] in cu]:
        c, _ = mau(md); pp = [q for q in paths if q.group(1) == c]
        if len(pp) != 1: continue
        g = [float(v) for v in pp[0].groups()[2:]]
        X += [(cu[md][0][0], g[0]), (cu[md][-1][0], g[6])]; Y += [(cu[md][0][1], g[1]), (cu[md][-1][1], g[7])]
    ax = np.polyfit([a for a, b in X], [b for a, b in X], 1); ay = np.polyfit([a for a, b in Y], [b for a, b in Y], 1)
    rx = max(abs(np.polyval(ax, a) - b) for a, b in X); ry = max(abs(np.polyval(ay, a) - b) for a, b in Y)
    assert rx < 0.3 and ry < 0.3, ('truc', pg, rx, ry)
    fx = lambda q: float(np.polyval(ax, q)); fy = lambda h: float(np.polyval(ay, h))
    for md, cf in models.items():
        (qa, ha), (qb, hb) = cf['dau'], cf['cuoi']; b = (ha - hb) / (qb * qb - qa * qa); a = ha + b * qa * qa
        H = lambda q: a - b * q * q
        c, trow = mau(md)
        pp = [q for q in paths if q.group(1) == c]; assert len(pp) == 1, (md, len(pp)); old = pp[0]; g = [float(v) for v in old.groups()[2:]]
        # Bezier khớp: P0, P3 cố định; P1, P2 bình phương tối thiểu
        t = np.linspace(0, 1, 60); qq = qa + (qb - qa) * t
        P = np.column_stack([[fx(q) for q in qq], [fy(H(q)) for q in qq]])
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; u = d / d[-1]
        P0, P3 = P[0], P[-1]; B1 = 3 * u * (1 - u) ** 2; B2 = 3 * u * u * (1 - u)
        rhs = P - np.outer((1 - u) ** 3, P0) - np.outer(u ** 3, P3)
        A = np.column_stack([B1, B2]); sol = np.linalg.lstsq(A, rhs, rcond=None)[0]; P1, P2 = sol
        bez = lambda uu: np.outer((1 - uu) ** 3, P0) + np.outer(3 * uu * (1 - uu) ** 2, P1) + np.outer(3 * uu * uu * (1 - uu), P2) + np.outer(uu ** 3, P3)
        ss = bez(np.linspace(0, 1, 400)); err = 0
        for q in qq: x = fx(q); k = np.argmin(abs(ss[:, 0] - x)); err = max(err, abs(ss[k, 1] - fy(H(q))))
        assert err < 0.6, (md, 'bezier lech pt', err)
        new = f'{c} RG {old.group(2)} w 1 J 1 j {P0[0]:.3f} {P0[1]:.3f} m {P1[0]:.3f} {P1[1]:.3f} {P2[0]:.3f} {P2[1]:.3f} {P3[0]:.3f} {P3[1]:.3f} c S'
        s = s.replace(old.group(0), new, 1)
        # nhãn số đường: chữ cùng màu gần điểm đầu cũ
        lb = [t for t in texts if t['col'] == c and abs(t['x'] - g[0]) < 25 and abs(t['y'] - g[1]) < 12]
        assert len(lb) == 1, (md, 'nhan', len(lb)); lb = lb[0]; dx, dy = lb['x'] - g[0], lb['y'] - g[1]
        nx, ny = P0[0] + dx, P0[1] + dy
        s = s.replace(lb['m'].group(0), lb['m'].group(0).replace(f"1 0 0 1 {lb['m'].group(5)} {lb['m'].group(6)} Tm", f'1 0 0 1 {nx:.3f} {ny:.3f} Tm'), 1)
        wr = re.search(r'1 1 1 rg (' + NUM + r') (' + NUM + r') ([\d.]+) ([\d.]+) re f\nBT /\S+ [\d.]+ Tf \S+ Tc ' + re.escape(c) + r' rg 1 0 0 1 ' + re.escape(f'{nx:.3f} {ny:.3f}'), s)
        oldw = re.search(r'1 1 1 rg (' + NUM + r') (' + NUM + r') ([\d.]+) ([\d.]+) re f\n(?=BT /\S+ [\d.]+ Tf \S+ Tc ' + re.escape(c) + r' rg 1 0 0 1 ' + re.escape(f'{nx:.3f} {ny:.3f}') + ')', s)
        if oldw:
            s = s.replace(oldw.group(0), f'1 1 1 rg {float(oldw.group(1)) + nx - lb["x"]:.3f} {float(oldw.group(2)) + ny - lb["y"]:.3f} {oldw.group(3)} {oldw.group(4)} re f\n', 1)
        # ô bảng: hàng tiêu đề Q = hàng có nhiều chữ số khớp cột nhất
        ry_ = trow['y']; cols = cf['cot']
        hdrs = {}
        for t in texts:
            if t['y'] > ry_ and t['y'] < 330 and t['t'] in [('%g' % q) for q in cols]: hdrs.setdefault(round(t['y'], 1), {})[float(t['t'])] = t
        hy = max(hdrs, key=lambda k: len(hdrs[k])); hd = hdrs[hy]; assert len(hd) == len(cols), (md, len(hd), len(cols))
        fnt = None; cells = [t for t in texts if abs(t['y'] - ry_) < 0.3 and t['font'] != trow['font'] or (abs(t['y'] - ry_) < 0.3 and t['t'] not in (md,))]
        cells = [t for t in texts if abs(t['y'] - ry_) < 0.3 and t['x'] > min(h['x'] for h in hd.values()) - 15]
        moi = {q: v for q, v in cf['bang']}
        xref_f = [f for f in p.get_fonts(full=True) if f[4] == cells[0]['font']][0][0]
        F = pymupdf.Font(fontbuffer=doc.extract_font(xref_f)[3])
        for q in cols:
            hc = hd[q]; hcx = hc['x'] + F.text_length(hc['t'], hc['size']) / 2 if False else None
            cand = [t for t in cells if abs((t['x'] + F.text_length(t['t'], t['size']) / 2) - (hd[q]['x'] + F.text_length(hd[q]['t'], hd[q]['size']) / 2)) < 9]
            assert len(cand) == 1, (md, q, [(t['t'], t['x']) for t in cand])
            ce = cand[0]; v = moi.get(q); nt = '–' if v is None else ('%g' % v)
            cx = ce['x'] + F.text_length(ce['t'], ce['size']) / 2; nx2 = cx - F.text_length(nt, ce['size']) / 2
            o = ce['m'].group(0); n = o.replace(f"1 0 0 1 {ce['m'].group(5)} {ce['m'].group(6)} Tm <{ce['m'].group(7)}>", f"1 0 0 1 {nx2:.3f} {ce['m'].group(6)} Tm <{hx(nt)}>")
            assert s.count(o) >= 1; s = s.replace(o, n, 1); bao.append((pg, md, q, ce['t'], nt))
    doc.update_stream(xr[0], s.encode('latin1'))
doc.save(OUT, garbage=3, deflate=True)
for b_ in bao: print(*b_)
