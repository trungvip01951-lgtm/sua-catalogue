"""Thêm 200WC350-22-37 vào trang 200WC của catalogue WC đã duyệt (vá tại chỗ, giữ khuôn trang).
Dùng: python them_ma.py <HÃNG> <pdf gốc> <pdf ra>"""
import sys, math, pymupdf
sys.path.insert(0, '/home/user/sua-catalogue/kho/work/claude_cdlf_them_dai_20261116'); import lib
KHO = lib.KHO; FR, FB, LB = KHO + '/vendor/fonts/LiberationSans-Regular.ttf', KHO + '/vendor/fonts/LiberationSans-Bold.ttf', KHO + '/vendor/fonts/Lato-Bold.ttf'
MA, KW, HP, QMAX, HMAX, QLV, HLV, HQMAX = '200WC350-22-37', '37', '50', 780, 40, 350, 22, 5   # lời anh 16/11 + mã (QĐ 177) + nấc 5 dải 200WC (QĐ 19)
# H = HMAX + b·Q + c·Q² qua (0, HMAX), (QLV, HLV), (QMAX, HQMAX)
c2 = ((HQMAX - HMAX) / QMAX - (HLV - HMAX) / QLV) / (QMAX - QLV); b1 = (HLV - HMAX) / QLV - c2 * QLV
def Hf(q): return HMAX + b1 * q + c2 * q * q
QCOT = list(range(0, 751, 50)) + [QMAX]; HCOT = [math.floor(Hf(q) + 0.5) for q in QCOT]
assert HCOT[0] == HMAX and HCOT[QCOT.index(QLV)] == HLV and HCOT[-1] == HQMAX and all(a > b for a, b in zip(HCOT, HCOT[1:])), HCOT
QM_CU, HM_CU, QM, HM = 600, 35, 800, 45
P = {'PEROTAC': dict(trang=6, plot=(738, 134, 1138, 514), tab=(40, 592, 686.8), xq=358, rp=15.2),
     'REDPUMP': dict(trang=5, plot=(432, 114, 1138.2, 390), tab=(334, 474, 576.6), xq=570, rp=14.4),
     'AQUARIS': dict(trang=5, plot=(530, 202, 858, 468), tab=(432, 552, 672), xq=700, rp=21.5, mau_moi=lib.rgb('6b3fa0'))}
XR = 1168.2
def spans(pg): return [s for b in pg.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'] if s['text'].strip()]
def mau(i): return ((i >> 16) / 255, (i >> 8 & 255) / 255, (i & 255) / 255)
def gan(a, b, e=0.35): return abs(a - b) < e
def ve(pg, d, items=None, color='=', fill='='):
    col = d.get('color') if color == '=' else color; fi = d.get('fill') if fill == '=' else fill
    for it in items or d['items']:
        if it[0] == 'l': pg.draw_line(it[1], it[2], color=col, width=d.get('width') or 0.5)
        elif it[0] == 're': pg.draw_rect(it[1], color=None if d['type'] == 'f' else col, fill=fi, width=0 if d['type'] == 'f' else d['width'])
        elif it[0] == 'c': pg.draw_bezier(it[1], it[2], it[3], it[4], color=col, width=d['width'])
def chay(hang, vao, ra):
    p = P[hang]; doc = pymupdf.open(vao); pg = doc[p['trang']]; x0, y0, x1, y1 = p['plot']; tx, ty, tb = p['tab']; xq, rp = p['xq'], p['rp']
    S = spans(pg); D = pg.get_drawings()
    # ---------- thu thập
    Rp = pymupdf.Rect(x0 - 7, y0 - 2, x1 + 2, y1 + 2); Rt = pymupdf.Rect(tx - 1, ty - 1, XR + 1.5, tb + 1)
    Dp = [d for d in D if Rp.contains(d['rect'])]; Dt = [d for d in D if Rt.contains(d['rect'])]
    St = [s for s in S if Rt.contains(pymupdf.Rect(s['bbox']))]
    cy = lambda s: (s['bbox'][1] + s['bbox'][3]) / 2; cx = lambda s: (s['bbox'][0] + s['bbox'][2]) / 2
    so = lambda s: s['text'].strip().isdigit()
    nhan = [s for s in S if s['text'].startswith('200WC') and y0 - 6 < cy(s) < y1 and s['bbox'][2] < x0]
    trucH = [s for s in S if so(s) and x1 < s['bbox'][0] < x1 + 14 and y0 - 6 < cy(s) < y1 + 6]
    trucQ = [s for s in S if so(s) and y1 + 2 < s['bbox'][1] < y1 + 26 and x0 - 12 < cx(s) < x1 + 12]
    tk = {'11 – 30 kW': '11 – 37 kW', '600 m³/h': f'{QMAX} m³/h', '32 m': f'{HMAX} m'}; Stk = [s for s in S if s['text'].strip() in tk and s not in St]
    assert len(nhan) == 4 and len(trucH) == 8 and len(trucQ) == 14 and len(Stk) == 3, (len(nhan), len(trucH), len(trucQ), len(Stk))
    # ---------- xoá
    lib.xoa(pg, chu=[pymupdf.Rect(s['bbox']) + (-0.5, 0.5, 0.5, -0.5) for s in nhan + trucH + trucQ + Stk], vung=[Rp, Rt]); c = lib.Chu(pg, FR, FB)
    def viet(s, t=None, x=None, y=None, align='l', col=None):
        t = s['text'].strip() if t is None else t; lech = (s['bbox'][3] - s['bbox'][1] - s['size'] * 1.117) / 2
        xx = {'l': s['bbox'][0], 'c': cx(s), 'r': s['bbox'][2]}[align] if x is None else x
        if 'Lato' in s['font']:
            f = pymupdf.Font(fontfile=LB); w = f.text_length(t, s['size'])
            if 'LTB' not in {q[4] for q in pg.get_fonts()}: pg.insert_font(fontname='LTB', fontfile=LB)
            xx = xx - w / 2 if align == 'c' else xx      # viết từng từ: dấu cách của Lato bị đọc ra thành U+00A0
            for tu in t.split(' '):
                pg.insert_text((xx, s['origin'][1]), tu, fontname='LTB', fontsize=s['size'], color=mau(s['color'])); xx += f.text_length(tu + ' ', s['size'])
            return
        dam = 'Bold' in s['font']; gian = 0
        if t == s['text'].strip() == s['text'] and len(t) > 3:      # chữ gốc có giãn khoảng cách ký tự → giữ đúng bề rộng
            du = s['bbox'][2] - s['bbox'][0] - c.w(t, s['size'], dam); gian = du / (len(t) - 1) if abs(du) > 0.6 else 0
        c(xx, (s['bbox'][1] if y is None else y) + lech, t, s['size'], dam, mau(s['color']) if col is None else col, align, gian=gian)
    # ---------- ô tóm tắt
    for s in Stk: viet(s, tk[s['text'].strip()], align='c' if hang == 'AQUARIS' else 'l')
    # ---------- biểu đồ
    X = lambda q: x0 + (x1 - x0) * q / QM; Y = lambda h: y1 - (y1 - y0) * h / HM
    fx = lambda x: x0 + (x - x0) * QM_CU / QM; fy = lambda y: y1 - (y1 - y) * HM_CU / HM; fp = lambda q: pymupdf.Point(fx(q.x), fy(q.y))
    luoi = next(d for d in Dp if gan(d.get('width') or 0, 0.55, 0.01)); truc = [d for d in Dp if gan(d.get('width') or 0, 0.7, 0.01)]
    for h in range(0, HM + 1, 5): pg.draw_line((x0, Y(h)), (x1, Y(h)), color=luoi['color'], width=0.55)
    for q in range(0, QM + 1, 100): pg.draw_line((X(q), y0), (X(q), y1), color=luoi['color'], width=0.55)
    for d in truc: ve(pg, d)
    cong = [d for d in Dp if d['items'][0][0] == 'c']; vach = [d for d in Dp if gan(d.get('width') or 0, 0.4, 0.01)]
    assert len(cong) == 4 and len(vach) == 4 and len(luoi['items']) == 1
    for d in cong: ve(pg, d, [('c',) + tuple(fp(q) for q in it[1:]) for it in d['items']])
    for d in vach: ve(pg, d, [('l', pymupdf.Point(it[1].x, fy(it[1].y)), pymupdf.Point(it[2].x, fy(it[2].y))) for it in d['items']])
    mm = p.get('mau_moi') or cong[0]['color']; yc = HMAX + b1 * QMAX / 2      # điểm điều khiển của parabol
    A, B, C = pymupdf.Point(X(0), Y(HMAX)), pymupdf.Point(X(QMAX / 2), Y(yc)), pymupdf.Point(X(QMAX), Y(HQMAX))
    pg.draw_bezier(A, A + (B - A) * (2 / 3), C + (B - C) * (2 / 3), C, color=mm, width=1.15)
    pg.draw_line((x0 - 6, Y(HMAX)), (x0, Y(HMAX)), color=mm, width=0.4)
    for s in nhan: viet(s, y=fy(cy(s)) - (s['bbox'][3] - s['bbox'][1]) / 2, align='r')
    s = nhan[0]; viet(s, MA, y=Y(HMAX) - (s['bbox'][3] - s['bbox'][1]) / 2, align='r', col=p.get('mau_moi'))
    s = trucH[0]
    for h in range(0, HM + 1, 5): viet(s, str(h), y=Y(h) - (s['bbox'][3] - s['bbox'][1]) / 2)
    sb = next(s for s in trucQ if 'Bold' in s['font']); sr = next(s for s in trucQ if 'Bold' not in s['font'])
    for q in range(0, QM + 1, 100): viet(sb, str(q), x=X(q), align='c'); viet(sr, lib.lmin(q), x=X(q), align='c')
    # ---------- bảng
    pc = (XR - xq) / 13; pm = (XR - xq) / len(QCOT)
    def mx(x):
        if x <= xq + 0.3: return x
        j = (x - xq) / pc; assert gan(j, round(j), 0.03), x; j = round(j); return XR if j == 13 else xq + j * pm
    for d in Dt:
        r = d['rect']; day = gan(r.y1, tb)
        if d['type'] == 'f':
            rr = pymupdf.Rect(r)
            if day and r.height > 2 * rp: rr.y1 += rp
            pg.draw_rect(rr, color=None, fill=d['fill'], width=0)
            if r.width > 500 and gan(r.y0, tb - 2 * rp) and gan(r.y1, tb - rp): pg.draw_rect(rr + (0, 2 * rp, 0, 2 * rp), color=None, fill=d['fill'], width=0)
            if r.width < 5 and r.y0 > tb - rp: pg.draw_rect(rr + (0, rp, 0, rp), color=None, fill=p.get('mau_moi') or d['fill'], width=0)
        elif r.width < 0.3:      # nét dọc
            ya, yb = r.y0, r.y1 + (rp if day else 0); pg.draw_line((mx(r.x0), ya), (mx(r.x0), yb), color=d['color'], width=d['width'])
            if r.x0 > xq + 1 and round((r.x0 - xq) / pc) == 12:
                for j in range(13, len(QCOT)): pg.draw_line((xq + j * pm, ya), (xq + j * pm, yb), color=d['color'], width=d['width'])
        else:                    # nét ngang
            ngan = any(e is not d and e['type'] == 's' and gan(e['rect'].y0, r.y0 - rp) and gan(e['rect'].x0, r.x0) and gan(e['rect'].x1, r.x1) and gan(e['width'], d['width'], 0.01) for e in Dt)
            if not day or ngan: pg.draw_line((mx(r.x0), r.y0), (mx(r.x1), r.y0), color=d['color'], width=d['width'])
    for d in Dt:                 # nét đáy vẽ sau cùng để đè đúng thứ tự
        r = d['rect']
        if d['type'] == 's' and r.width > 0.3 and gan(r.y1, tb): pg.draw_line((mx(r.x0), r.y0 + rp), (mx(r.x1), r.y0 + rp), color=d['color'], width=d['width'])
    ycuoi = max(s['bbox'][1] for s in St if s['text'].startswith('200WC'))
    cot = lambda s: round((cx(s) - xq - pc / 2) / pc); xc = lambda k: xq + (k + 0.5) * pm
    lmn = {**{q: lib.lmin(q) for q in QCOT}}
    for s in St:
        t = s['text'].strip(); cuoi = abs(s['bbox'][1] - ycuoi) < 2.5
        if cx(s) > xq:
            k = cot(s); viet(s, x=xc(k), align='c')
            if k == 12 and s['bbox'][1] < ty + 34 and so(s):      # tiêu đề cột mới
                for j in range(13, len(QCOT)): viet(s, str(QCOT[j]) if 'Bold' in s['font'] else lmn[QCOT[j]], x=xc(j), align='c')
            if cuoi: viet(s, str(HCOT[k]), x=xc(k), y=s['bbox'][1] + rp, align='c')
            if cuoi and k == 12:
                for j in range(13, len(QCOT)): viet(s, str(HCOT[j]), x=xc(j), y=s['bbox'][1] + rp, align='c')
        else:
            viet(s, y=s['bbox'][1] + (rp / 2 if t == 'H (m)' else 0))
            if cuoi: viet(s, {'200WC250-22-30': MA, '30': KW, '40': HP}.get(t, t), y=s['bbox'][1] + rp, align='l' if t.startswith('200WC') else 'c')
    doc.subset_fonts(); doc.save(ra, garbage=3, deflate=True); print(hang, 'ĐÃ LƯU', ra, len(doc), 'trang | H bảng', HCOT, '| b, c =', round(b1, 6), f'{c2:.4e}')
if __name__ == '__main__': chay(*sys.argv[1:4])
