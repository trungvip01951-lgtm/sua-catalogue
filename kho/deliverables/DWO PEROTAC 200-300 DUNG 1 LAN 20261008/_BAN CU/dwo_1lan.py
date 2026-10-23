"""BẢN DÙNG 1 LẦN (08/10/2026): DWO PEROTAC chỉ DWO200 + DWO300, T (3 pha) và M (1 pha). Số Q–H: bảng anh gửi 08/10. Không ghi bản chính, không vào sổ."""
import sys, json, re
from pathlib import Path
K = Path.home() / 'mnt' / 'Sửa catalogue'; sys.path.insert(0, str(K / 'work/claude_bo_20261007/DWO')); sys.path.insert(0, str(K / 'work/claude_mau12_20261006/MAU_DWO'))
import dwo_bo3 as B3
from dwo_bo3 import *
from scipy.interpolate import CubicSpline, PchipInterpolator
QG = [0, 10, 20, 30, 40, 50, 60]; M1.QGRID = QG; M1.LMIN = [round(q * 1000 / 60) for q in QG]; _colx = M1.colx; M1.colx = lambda x, w, fixed, nq=None: _colx(x, w, fixed, len(QG))
ROWS = [{'model': 'DWO200T', 'model_m': 'DWO200M', 'kw': '1.5', 'kw_f': 1.5, 'hp': '2', 'i3': '3.5', 'i1': '9.0', 'H': dict(zip(QG, ['18.5', '17', '15', '12', '8', '3'])), 'label': 'DWO200T/M'},
        {'model': 'DWO300T', 'model_m': 'DWO300M', 'kw': '2.2', 'kw_f': 2.2, 'hp': '3', 'i3': '4.8', 'i1': '12.9', 'H': dict(zip(QG, ['23', '19', '18', '16', '12', '7', '1'])), 'label': 'DWO300T/M'}]
PORTS = ['Suction DNA: 2" for DWO200, 2"1/2 for DWO300', 'Delivery DNM: 2"']
SRCPDF = K / 'work/claude_bo_20261007/DWO/UNG VIEN 03 - 1 TRANG/PEROTAC - DWO.pdf'
OUTD = K / 'deliverables' / 'DWO PEROTAC 200-300 DUNG 1 LAN 20261008'; DR = Path.home() / 'claude_work' / 'DWO_1LAN'

def spline(r):
    q = np.array(list(r['H']), float); h = np.array([float(v) for v in r['H'].values()]); xs = np.linspace(q[0], q[-1], 6001); out = {}
    for name, sp in (('C2', CubicSpline(q, h, bc_type='not-a-knot')), ('PCHIP', PchipInterpolator(q, h))):
        d1 = sp(xs, 1); d2 = sp(xs, 2); s = np.sign(d2[np.abs(d2) > 1e-6]); out[name] = {'sp': sp, 'mono': bool(d1.max() < 0), 'max_slope': float(d1.max()), 'flips': int((s[1:] != s[:-1]).sum())}
    return q, h, out
def segs(q, h, sp):
    m = sp(q, 1); S_ = []
    for i in range(len(q) - 1): dq = q[i + 1] - q[i]; S_.append([(q[i], h[i]), (q[i] + dq / 3, h[i] + m[i] * dq / 3), (q[i + 1] - dq / 3, h[i + 1] - m[i + 1] * dq / 3), (q[i + 1], h[i + 1])])
    return S_

def chart2(p, S, D, x, y, w, h, left=74, right=22, bottom=40):
    px = x + left; py = y + 6; pw = w - left - right; ph = h - 6 - bottom; qs, Qax = nice(70, (5, 10, 20), 10); hs, Hax = nice(max(float(r['H'][0]) for r in D) * 1.02, (5, 10), 8)
    X = lambda q: px + q / Qax * pw; Y = lambda v: py + ph - v / Hax * ph
    for k in range(int(round(Hax / hs)) + 1): v = k * hs; p.line(px, Y(v), px + pw, Y(v), S['grid'], .55); p.text(fmt(v), px + pw + 6, Y(v) + 2.8, 7.4, 'Body', S['muted'])
    for k in range(int(round(Qax / qs)) + 1):
        q = k * qs; p.line(X(q), py, X(q), py + ph, S['grid'], .55); p.text(fmt(q), X(q), py + ph + 13, 7.8, 'Bold', S['title'], 'center'); p.text(fmt(round(q * 1000 / 60)), X(q), py + ph + 25, 7, 'Body', S['muted'], 'center')
    p.line(px, py, px, py + ph, S['muted'], .7); p.line(px, py + ph, px + pw, py + ph, S['muted'], .7)
    p.text('Q (m³/h)', px - 9, py + ph + 13, 7.4, 'Bold', S['title'], 'right'); p.text('Q (l/min)', px - 9, py + ph + 25, 7, 'Body', S['muted'], 'right'); p.text('Total head H (m)', x + 4, py + ph / 2, 7.8, 'Bold', S['title'], rotate=True)
    for r in D:
        op = [f"{rgb(S['curve'], True)} 1.15 w 1 J 1 j"]
        for i, sg in enumerate(r['segs']):
            if i == 0: op.append(f"{n(X(sg[0][0]))} {n(p.H - Y(sg[0][1]))} m")
            op.append(' '.join(f"{n(X(a))} {n(p.H - Y(b))}" for a, b in sg[1:]) + ' c')
        p.ops.append(' '.join(op) + ' S 0 J 0 j'); p.text(r['label'], px - 9, Y(float(r['H'][0])) + 2.7, 7.6, 'Bold', S['title'], 'right')
    return {'px': px, 'py': py, 'pw': pw, 'ph': ph, 'Qax': Qax, 'Hax': Hax}

def build(D):
    S = STYLE['PEROTAC']; R = M1.rng(D); p = Page(1, W, H); pd = pymupdf.open(SRCPDF); ims = {(i['width'], i['height']): i['xref'] for i in page_images(SRCPDF, 1)}; assert {(535, 198), (500, 404), (726, 564)} <= set(ims), ims
    im = {'/Logo': ('copy', str(SRCPDF), ims[(535, 198)]), '/Ph3': ('copy', str(SRCPDF), ims[(500, 404)]), '/Expl': ('copy', str(SRCPDF), ims[(726, 564)])}; I = {'logo': (535, 198)}
    head_P(p, S, I, 'PERFORMANCE & TECHNICAL DATA'); para(p, DESC, M, 84, W - 2 * M, S['ink'], 7.6, 10.4); phh = 122; phw = phh * 500 / 404; p.image('/Ph3', M + (290 - phw) / 2, 128, phw, phh)
    range_P(p, S, R, 318, 132, W - M - 318, [CODE1 + '  (T: three-phase 3~;  M: single-phase 1~)', 'Example: DWO200T, DWO200M'], 13.4)
    sec(p, S, 'Q–H curves', M, 268, 300); ax = chart2(p, S, D, M, 280, 300, 226); y = sec(p, S, 'Operating conditions', M, 530, 300); y = para(p, M1.OPER, M, y, 300, S['ink']) + 8; y = sec(p, S, 'Motor and ports', M, y + 2, 300); yl = para(p, M1.MOTOR + PORTS, M, y, 300, S['ink'])
    x = 346; w = W - M - x; sec(p, S, 'Exploded view and materials', x, 268, w); ye = M1.img(p, '/Expl', x, 282, w, (726, 564)); yr = mat_P(p, S, x, ye + 8, w, 11.4, 15, 24, 112); yt = max(yl, yr) + 40; yb = M1.ptable_P(p, S, D, M, yt, W - 2 * M); assert yb < 800, yb; foot(p, S, 'PEROTAC', 1, 1); return p, im, ax

def check(out, D, ax, S):
    d = pymupdf.open(out); pg = d[0]; res = {'sha256': sha(out), 'bytes': Path(out).stat().st_size, 'pages': len(d), 'page_size': [pg.rect.width, pg.rect.height]}
    near = lambda a, b: max(abs(u - v) for u, v in zip(a, b)) < .004; cur = [g for g in pg.get_drawings() if g.get('color') and near(g['color'], S['curve']) and abs((g.get('width') or 0) - 1.15) < .01 and any(it[0] == 'c' for it in g['items'])]; assert len(cur) == len(D), len(cur)
    Qof = lambda X_: (X_ - ax['px']) / ax['pw'] * ax['Qax']; Hof = lambda Y_: (ax['py'] + ax['ph'] - Y_) / ax['ph'] * ax['Hax']; res['curves'] = {}
    for g in cur:
        B_ = [[(Qof(pt.x), Hof(pt.y)) for pt in it[1:5]] for it in g['items'] if it[0] == 'c']; r = min(D, key=lambda r: abs(float(r['H'][0]) - B_[0][0][1])); t = np.linspace(0, 1, 401); qq = []; hh = []; errs = []
        for sg in B_: P_ = np.array(sg); c = np.stack([(1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3], 1) @ P_; qq += list(c[:-1, 0]); hh += list(c[:-1, 1])
        qq.append(B_[-1][3][0]); hh.append(B_[-1][3][1]); qq = np.array(qq); hh = np.array(hh)
        for q, v in r['H'].items(): m_ = float(np.interp(q, qq, hh)); errs.append((q, float(v), round(m_, 3), round(abs(m_ - float(v)) / float(v) * 100, 2)))
        res['curves'][r['label']] = {'segments': len(B_), 'points_table_vs_pdf': errs, 'max_err_pct': max(e[3] for e in errs), 'Q_increasing': bool((np.diff(qq) > 0).all()), 'H_decreasing': bool((np.diff(hh) < 0).all()), 'spline': r['spline'], 'curvature_sign_changes': r['flips']}
    ws = pg.get_text('words'); rows = {}
    for r in D:
        a = next(w_ for w_ in ws if w_[4] == r['model']); line = [w_[4] for w_ in sorted([w_ for w_ in ws if abs(w_[3] - a[3]) < 1.5], key=lambda w_: w_[0])]; exp = [r['model'], r['model_m'], r['kw'], r['hp'], r['i3'], r['i1']] + [r['H'].get(q, '–') for q in QG]; rows[r['model']] = {'pdf': line, 'equal_expected': line == exp}
    hd = [w_[4] for w_ in sorted([w_ for w_ in ws if abs(w_[3] - min(w2[3] for w2 in ws if w2[4] == 'm³/h' and w2[1] > 600)) < 1.5], key=lambda w_: w_[0])]; lm = [w_[4] for w_ in sorted([w_ for w_ in ws if abs(w_[3] - max(w2[3] for w2 in ws if w2[4] == 'l/min')) < 1.5], key=lambda w_: w_[0])]
    res['table_rows'] = rows; res['table_head_Q'] = hd; res['table_head_lmin'] = lm; txt = re.sub(r'\s+', ' ', pg.get_text()); sp = [(round(s_['size'], 2), s_['text']) for b in pg.get_text('dict')['blocks'] for l in b.get('lines', []) for s_ in l['spans'] if s_['text'].strip()]
    res['below_7pt'] = [s_ for s_ in sp if s_[0] < 7 and s_[1].strip() != '2']; res['other_models_found'] = sorted(set(re.findall(r'DWO(?:037|100|150|400|500|550)\w?', txt))); res['forbidden'] = [w_ for w_ in ('Ebara', 'EBARA', 'Warranty', '60 Hz', 'on request', 'Weight', 'Dimension') if w_ in txt]
    res['out_of_margin'] = [w_[4] for w_ in ws if w_[0] < 20 or w_[2] > W - M + 8 or w_[3] > 828]; L = [(pymupdf.Rect(l['bbox']), ''.join(s_['text'] for s_ in l['spans']).strip()) for b in pg.get_text('dict')['blocks'] for l in b.get('lines', []) if ''.join(s_['text'] for s_ in l['spans']).strip() and l['dir'] == (1.0, 0.0)]; ov = []
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if '2' in (L[i][1], L[j][1]): continue
            r_ = pymupdf.Rect(L[i][0].x0 + .3, L[i][0].y0 + 2.2, L[i][0].x1 - .3, L[i][0].y1 - 2.2) & pymupdf.Rect(L[j][0].x0 + .3, L[j][0].y0 + 2.2, L[j][0].x1 - .3, L[j][0].y1 - 2.2)
            if not r_.is_empty and r_.width > .2 and r_.height > .2: ov.append((L[i][1][:20], L[j][1][:20]))
    res['text_overlaps'] = ov; res['need_text_missing'] = [t for t in ['1.5–2.2 kW (2–3 HP)', '60 m³/h', '23 m', 'n ≈ 2900 /min', '50 Hz', '1~ 220–240 V / 3~ 380–415 V', 'Max. working pressure: 8 bar', 'Max. liquid temperature: 90 °C', 'max. Ø 19 mm', 'IP55'] + PORTS + [a for a, _ in PARTS] if t not in txt]
    res['images'] = [(i['width'], i['height'], round(i['width'] / (i['bbox'][2] - i['bbox'][0]) * 72)) for i in pg.get_image_info()]; return res

if __name__ == '__main__':
    S = STYLE['PEROTAC']; info = {}
    for r in ROWS:
        q, h, o = spline(r); pick = 'C2' if o['C2']['mono'] and o['C2']['flips'] <= o['PCHIP']['flips'] else 'PCHIP'; info[r['label']] = {k: {a: b for a, b in v.items() if a != 'sp'} for k, v in o.items()}; assert o[pick]['mono']
        if len(sys.argv) > 1: pick = sys.argv[1]
        r['segs'] = segs(q, h, o[pick]['sp']); r['spline'] = pick; r['flips'] = o[pick]['flips']
    print(json.dumps(info))
    p, im, ax = build(ROWS); out = DR / 'PEROTAC - DWO200-DWO300.pdf'; B0.save_multi([p], out, im, 'PEROTAC - DWO200 / DWO300'); res = check(out, ROWS, ax, S); print(json.dumps(res, ensure_ascii=False, default=float)); render_png(out, DR / 'xem.png', 110); open(DR / 'check.json', 'w', encoding='utf8').write(json.dumps(res, ensure_ascii=False, indent=1, default=float))
