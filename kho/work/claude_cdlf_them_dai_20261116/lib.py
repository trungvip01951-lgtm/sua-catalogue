# -*- coding: utf-8 -*-
"""Hàm chung dựng trang dải CDLF mới bằng cách nhân bản trang CDLF42 đã duyệt (vá, giữ khổ và bố cục — QĐ 152)."""
import math, re, pymupdf, numpy as np
from scipy.interpolate import PchipInterpolator
KHO = '/home/user/sua-catalogue/kho'
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
LMIN = 1000 / 60
def lmin(q): return f'{math.floor(q * LMIN + 0.5):d}'
def g(v): return f'{v:g}'
class Chu:
    """Viết chữ bằng phông tệp (Regular/Bold); toạ độ y là ĐỈNH hộp chữ như bbox của trang mẫu."""
    def __init__(s, page, reg, bold, asc=0.905):
        s.p = page; s.f = {False: pymupdf.Font(fontfile=reg), True: pymupdf.Font(fontfile=bold)}; s.asc = asc
        s.reg, s.bold = reg, bold; s.dam_bao()
    def dam_bao(s):
        co = {f[4] for f in s.p.get_fonts()}      # apply_redactions viết lại tài nguyên trang → phải gắn lại phông
        if 'NR' not in co: s.p.insert_font(fontname='NR', fontfile=s.reg)
        if 'NB' not in co: s.p.insert_font(fontname='NB', fontfile=s.bold)
    def w(s, t, size, bold=False): return s.f[bold].text_length(t, size)
    def __call__(s, x, ytop, t, size, bold=False, color=(0, 0, 0), align='l', rotate=0, gian=0):
        w = s.w(t, size, bold) + gian * (len(t) - 1); s.dam_bao()
        if gian:
            x = x - w if align == 'r' else x - w / 2 if align == 'c' else x
            for ch in t:
                s.p.insert_text((x, ytop + size * s.asc), ch, fontname='NB' if bold else 'NR', fontsize=size, color=color); x += s.w(ch, size, bold) + gian
            return w
        if rotate == 90:
            s.p.insert_text((x + size * s.asc, ytop), t, fontname='NB' if bold else 'NR', fontsize=size, color=color, rotate=90); return w
        x = x - w if align == 'r' else x - w / 2 if align == 'c' else x
        s.p.insert_text((x, ytop + size * s.asc), t, fontname='NB' if bold else 'NR', fontsize=size, color=color); return w
def xoa(page, chu=(), vung=()):
    """chu: các ô chỉ xoá chữ (giữ nét, ảnh); vung: các ô xoá cả chữ, nét nằm trọn trong ô, ảnh chạm ô."""
    if chu:
        for r in chu: page.add_redact_annot(pymupdf.Rect(r))
        page.apply_redactions(images=0, graphics=0)
    if vung:
        for r in vung: page.add_redact_annot(pymupdf.Rect(r))
        page.apply_redactions(images=1, graphics=1)
def buoc_dep(vmax, toi_da, ds=(1, 2, 2.5, 4, 5)):
    e = 10 ** math.floor(math.log10(vmax))
    for k in (0.1, 1, 10):
        for m in ds:
            b = m * e * k
            if b * toi_da >= vmax: return b
def truc_q(Q, toi_da=12):
    b = buoc_dep(Q[-1], toi_da, (1, 2, 3, 4, 5)); return b, math.ceil(Q[-1] / b - 1e-9) * b
LECH = {}
def duong_min(Q, H, qq):
    """Đường vẽ cong đều (QTH 4.2): đa thức bậc 2→4 khớp bình phương tối thiểu, hai đầu giữ đúng số bảng; nhận bậc thấp nhất
    mà đường giảm đều, không đổi chiều cong và lệch bảng ≤ 4,5 % tại mọi điểm; không đạt thì PCHIP qua đúng điểm."""
    Q = np.array(Q, float); H = np.array(H, float); w = np.ones(len(Q)); w[0] = w[-1] = 300
    for uon_toi_da in (0, 1):          # ưu tiên không điểm uốn; không được thì cho 1 điểm uốn (QTH 4.2: tối đa 1)
        for bac in (2, 3, 4):
            if bac >= len(Q): break
            p = np.poly1d(np.polyfit(Q, H, bac, w=w)); hh = p(qq); lech = float(np.max(np.abs(p(Q) - H) / H))
            d1 = np.diff(hh); d2 = np.diff(hh, 2); dau = np.sign(d2[np.abs(d2) > 1e-6]); uon = int(np.sum(dau[1:] != dau[:-1]))
            if lech <= 0.045 and np.all(d1 <= 1e-9) and uon <= uon_toi_da: return hh, lech
    f = PchipInterpolator(Q, H); return f(qq), 0.0
def bieu_do(c, R, models, Q, st):
    """Vẽ biểu đồ Q–H trong ô R (x0,y0,x1,y1 = vùng lưới). st: dict kiểu hãng. Nhãn model bên trái đầu đường, có nét dẫn."""
    p = c.p; x0, y0, x1, y1 = R
    bq, qmax = truc_q(Q, st.get('q_vach', 12)); hmax_dl = max(m['h'][0] for m in models)
    lo = min(m['h'][-1] for m in models); bh = buoc_dep(hmax_dl * 1.02, st.get('h_vach', 8), (1, 2, 2.5, 4, 5)); hmin = 0
    if st.get('cat_day') and lo > 0.25 * hmax_dl:      # trang nhóm tầng cao: trục H không bắt đầu từ 0 (như tr.12 AQUARIS CDLF42)
        bh = buoc_dep((hmax_dl * 1.02 - lo * 0.9), st.get('h_vach', 8), (1, 2, 2.5, 4, 5)); hmin = math.floor(lo * 0.97 / bh) * bh
    hmax = math.ceil(hmax_dl * 1.02 / bh - 1e-9) * bh
    X = lambda q: x0 + (x1 - x0) * q / qmax; Y = lambda h: y1 - (y1 - y0) * (h - hmin) / (hmax - hmin)
    n_h = int(round((hmax - hmin) / bh))
    for i in range(n_h + 1):
        h = hmin + i * bh; p.draw_line((x0, Y(h)), (x1, Y(h)), color=st['luoi'], width=st.get('luoi_w', 0.5))
        c(x0 - 4, Y(h) - st['co_truc'] * 0.55, g(h), st['co_truc'], False, st['mau_truc'], 'r')
        if i < n_h and st.get('luoi_phu'): p.draw_line((x0, Y(h + bh / 2)), (x1, Y(h + bh / 2)), color=st['luoi'], width=0.3)
    nq = int(round(qmax / bq))
    for i in range(nq + 1):
        q = i * bq; p.draw_line((X(q), y0), (X(q), y1), color=st['luoi'], width=st.get('luoi_w', 0.5))
        c(X(q), y1 + st['q_dy'], g(q), st['co_q'], True, st['mau_q'], 'c'); c(X(q), y1 + st['l_dy'], lmin(q), st['co_l'], False, st['mau_truc'], 'c')
    p.draw_line((x0, y0), (x0, y1), color=st['khung'], width=0.5); p.draw_line((x0, y1), (x1, y1), color=st['khung'], width=0.5)
    c(x0 - 7, y1 + st['q_dy'] + 0.4, 'Q (m³/h)', st['co_truc'], True, st['mau_q'], 'r'); c(x0 - 7, y1 + st['l_dy'], 'Q (l/min)', st['co_l'], False, st['mau_truc'], 'r')
    tw = c.w('Total head H (m)', st['co_tieu_h'], True); c(st['x_tieu_h'], (y0 + y1) / 2 + tw / 2, 'Total head H (m)', st['co_tieu_h'], True, st['mau_q'], rotate=90)
    # đường
    ds = []
    for k, m in enumerate(models):
        qq = np.linspace(Q[0], Q[-1], 60); hh, lech = duong_min(Q, m['h'], qq); LECH[m['ten']] = lech
        mau = st['mau_duong'](k) if callable(st['mau_duong']) else st['mau_duong']
        p.draw_polyline([pymupdf.Point(X(q), Y(h)) for q, h in zip(qq, hh)], color=mau, width=st.get('net', 1.0), closePath=False)
        ds.append(dict(m=m, y=Y(m['h'][0]), mau=mau))
    # nhãn: tránh đè nhau theo chiều dọc
    kc = st.get('kc_nhan', st['co_nhan'] + 2.2); ds.sort(key=lambda d: d['y'])
    ys = [d['y'] for d in ds]
    for _ in range(200):
        doi = False
        for i in range(len(ys) - 1):
            if ys[i + 1] - ys[i] < kc:
                tb = (ys[i] + ys[i + 1]) / 2; ys[i], ys[i + 1] = tb - kc / 2, tb + kc / 2; doi = True
        if not doi: break
    lo, hi = y0 + 2, y1 - 2
    if ys and ys[0] < lo: ys = [y + (lo - ys[0]) for y in ys]
    assert not ys or ys[-1] <= hi + kc, 'nhãn không vừa chiều cao biểu đồ'
    xr = X(Q[0]) - st.get('dan', 12)
    for d, y in zip(ds, ys):
        mc = d['mau'] if st.get('nhan_mau_duong') else st['mau_nhan']
        w = c(xr, y - st['co_nhan'] * 0.55, d['m']['ten'], st['co_nhan'], True, mc, 'r')
        p.draw_line((xr + 2, y), (X(Q[0]) - 4, y), color=d['mau'], width=0.4); p.draw_line((X(Q[0]) - 4, y), (X(Q[0]), d['y']), color=d['mau'], width=0.4)
        assert xr - w > x0 + 1, ('nhãn tràn trục', d['m']['ten'])
    return X, Y, qmax, hmax
def gop_kich_thuoc(models, toi_da=2):
    """Gộp các model liền nhau cùng bộ kích thước thành một dòng 'A/B' (như bảng CDLF42 đã duyệt), tối đa 2 tên/dòng."""
    out = []
    for m in models:
        if out and out[-1][1] == m['dim'] and len(out[-1][0]) < toi_da: out[-1][0].append(m['ten'])
        else: out.append([[m['ten']], m['dim']])
    return [('/'.join(t), d) for t, d in out]
def so_tang(m): return int(re.match(r'CDLF\d+-(\d)', m['ten']).group(1))
INCH = {100: '4"', 125: '5"', 150: '6"'}
PR = {'65': dict(ls='18', fr='30–80', frl='8.3–22.2', bar='22', eff='76'), '85': dict(ls='24', fr='50–110', frl='13.8–30.5', bar='17', eff='77'),
      '120': dict(ls='33', fr='60–150', frl='16.7–41.7', bar='16', eff='74'), '150': dict(ls='41.6', fr='80–180', frl='22–50', bar='16', eff='73'),
      '200': dict(ls='55.6', fr='100–240', frl='27.8–66.7', bar='16', eff='79')}   # bảng 产品范围 tr.5 của nguồn
def dac_tinh(dai, d):
    ms = d['models']
    return [('Rated flow', f'{dai} m³/h'), ('Flow range', f"{d['Q'][0]}–{d['Q'][-1]} m³/h"), ('Max. pressure', f"{PR[dai]['bar']} bar"),
            ('Motor power', f"{g(ms[0]['kw'])}–{g(ms[-1]['kw'])} kW"), ('Inlet / Outlet', f"{INCH[d['dn']]} / {INCH[d['dn']]}"), ('Speed', f"n ≈ {d['n']} /min")]
def anh_so_do(dai, d, out):
    """Cắt hình lắp đặt từ trang nguồn (300 dpi, xám)."""
    src = pymupdf.open('nguon_CDL.pdf'); pg = src[d['trang'] - 1]
    pm = pg.get_pixmap(dpi=300, clip=pymupdf.Rect(66, 442, 272, 744), colorspace=pymupdf.csGRAY); pm.save(out); return pm.width, pm.height

# ---------------------------------------------------------------- trang đầu: bảng PRODUCT RANGE + tiêu đề cấu tạo
def _spans(p, clip=None):
    return [s for b in p.get_text('dict', clip=clip)['blocks'] for l in b.get('lines', []) for s in l['spans'] if s['text'].strip()]
def doc_bang_dai(p, vung):
    """Đọc bảng PRODUCT RANGE có sẵn trên trang 1 (không gõ lại): trả (tên cột, [(nhãn, [giá trị])])."""
    ss = _spans(p, pymupdf.Rect(vung)); hang = {}
    for s in ss: hang.setdefault(round(s['bbox'][1] / 3), []).append(s)
    rows = [sorted(v, key=lambda s: s['bbox'][0]) for _, v in sorted(hang.items())]
    assert rows[0][0]['text'].strip() == 'DESCRIPTION', rows[0][0]['text']
    cot = [s['text'].strip() for s in rows[0][1:]]; out = [(r[0]['text'].strip(), [s['text'].strip() for s in r[1:]]) for r in rows[1:]]
    assert cot == ['CDLF2', 'CDLF4', 'CDLF8', 'CDLF12', 'CDLF16', 'CDLF20', 'CDLF32', 'CDLF42'] and len(out) == 11, (cot, len(out))
    return cot, out
def bang_dai_moi(cot, rows, D):
    """Nối 5 dải mới (số từ bảng 产品范围 tr.5 của nguồn + bảng hiệu năng)."""
    them = {'Rated flow (m³/h)': lambda k, d: k, 'Rated flow (l/s)': lambda k, d: PR[k]['ls'], 'Flow range (m³/h)': lambda k, d: PR[k]['fr'],
            'Flow range (l/s)': lambda k, d: PR[k]['frl'], 'Max. pressure (bar)': lambda k, d: PR[k]['bar'],
            'Motor power (kW)': lambda k, d: f"{g(d['models'][0]['kw'])}–{g(d['models'][-1]['kw'])}", 'Max. efficiency (%)': lambda k, d: PR[k]['eff'],
            'DIN flange': lambda k, d: f"DN{d['dn']}", 'Cutting ferrule joint': lambda k, d: '–', 'Pipe thread': lambda k, d: '–'}
    out = []
    for nhan, v in rows:
        if nhan == 'Temperature range (°C)': assert v == ['-15 ~ +120']; out.append((nhan, v)); continue
        assert len(v) == 8 and nhan in them, (nhan, v); out.append((nhan, v + [them[nhan](k, d) for k, d in D.items()]))
    for k, d in D.items(): assert PR[k]['fr'] == f"{d['Q'][0]}–{d['Q'][-1]}", k
    return cot + ['CDLF' + k for k in D], out
def doi_tieu_de(doc, FR, FB):
    """'CDLF 32, 42' ở trang cấu tạo → thêm 65, 85 (nguồn tr.9: cùng bản vẽ và vật liệu); ở khối MODEL DESIGNATION → thêm 65, 85, 120, 150 (nguồn tr.6)."""
    n = 0
    for pg in list(doc)[:4]:
        ss = _spans(pg); viec = []
        for k, s in enumerate(ss):
            t = s['text']; sau = ss[k + 1]['text'] if k + 1 < len(ss) else ''
            if t.strip() == 'CDLF 32, 42' and sau.startswith('Example'): moi = 'CDLF 32, 42, 65, 85, 120, 150'
            elif t.rstrip().endswith('CDLF 32, 42') and 'Photo' not in t: moi = t.rstrip() + ', 65, 85'
            else: continue
            viec.append((s, moi))
        if not viec: continue
        xoa(pg, chu=[pymupdf.Rect(s['bbox']) + (-0.5, 0.5, 0.5, -0.5) for s, _ in viec]); c = Chu(pg, FR, FB)
        for s, moi in viec:
            col = s['color']; c(s['bbox'][0], s['bbox'][1] + (s['bbox'][3] - s['bbox'][1] - s['size'] * 1.117) / 2, moi, s['size'], 'Bold' in s['font'], ((col >> 16) / 255, (col >> 8 & 255) / 255, (col & 255) / 255)); n += 1
    return n
