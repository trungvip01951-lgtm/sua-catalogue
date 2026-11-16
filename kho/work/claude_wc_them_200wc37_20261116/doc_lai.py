"""Đọc lại PDF sau khi thêm mã: trang khác không đổi chữ; trang 200WC: chữ cũ giữ nguyên vị trí (ngoài vùng Q), bảng đủ 5 dòng × 17 cột."""
import sys, pymupdf
T = {'PEROTAC': 6, 'REDPUMP': 5, 'AQUARIS': 5}; XQ = {'PEROTAC': 358, 'REDPUMP': 570, 'AQUARIS': 700}
MOI = [40, 37, 34, 32, 29, 27, 24, 22, 20, 18, 15, 13, 11, 10, 8, 6, 5]; QC = [str(q) for q in list(range(0, 751, 50)) + [780]]
def sp(pg): return [s for b in pg.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'] if s['text'].strip()]
for H in T:
    a, b = pymupdf.open(f'goc_{H}.pdf'), pymupdf.open(f'{H}.pdf'); t = T[H]
    khac = [i + 1 for i in range(len(a)) if i != t and (a[i].get_text() != b[i].get_text() or len(a[i].get_drawings()) != len(b[i].get_drawings()))]
    A, B = sp(a[t]), sp(b[t]); lech = []
    for s in A:
        if (s['bbox'][0] + s['bbox'][2]) / 2 > XQ[H] and s['bbox'][1] > 400 or s['text'].strip().isdigit() or s['text'].strip() in ('11 – 30 kW', '600 m³/h', '32 m', 'H (m)') or s['text'].startswith('200WC'): continue
        if not any(q['text'].strip() == s['text'].strip() and max(abs(x - y) for x, y in zip(q['bbox'], s['bbox'])) < 0.6 and abs(q['size'] - s['size']) < 0.01 and q['color'] == s['color'] for q in B): lech.append(s['text'])
    def bang(S):
        rows = {}
        for s in S:
            if s['text'].startswith('200WC') and s['bbox'][1] > 440: rows[s['text']] = round(s['bbox'][1], 1)
        out = {}
        for m, y in rows.items():
            out[m] = [q['text'].strip() for q in sorted(S, key=lambda q: q['bbox'][0]) if abs(q['bbox'][1] - y) < 2.5 and q['text'].strip().isdigit()]
        return out
    ba, bb = bang(A), bang(B); cu = all(bb[m] == ba[m] for m in ba); moi = bb.get('200WC350-22-37')
    ok_moi = moi == ['37', '50'] + [str(v) for v in MOI]
    yq = min(s['bbox'][1] for s in B if s['text'].strip() == '780' and 'Bold' in s['font']); hd = [s['text'].strip() for s in sorted(B, key=lambda q: q['bbox'][0]) if abs(s['bbox'][1] - yq) < 1 and s['text'].strip().isdigit() and 'Bold' in s['font']]
    # cột: mỗi ô H của dòng mới thẳng cột với tiêu đề Q
    cxs = lambda S, y: [(q['bbox'][0] + q['bbox'][2]) / 2 for q in sorted(S, key=lambda q: q['bbox'][0]) if abs(q['bbox'][1] - y) < 1 and q['text'].strip().isdigit() and (q['bbox'][0] + q['bbox'][2]) / 2 > XQ[H]]
    ym = next(s['bbox'][1] for s in B if s['text'] == '200WC350-22-37' and s['bbox'][1] > 440); thang = max(abs(x - y) for x, y in zip(cxs(B, yq), cxs(B, ym)))
    tk = [x in b[t].get_text() for x in ('11 – 37 kW', '780 m³/h', '40 m')]
    print(H, '| trang khác đổi:', khac, '| chữ cũ lệch:', lech, '| 4 dòng cũ nguyên:', cu, '| dòng mới đúng:', ok_moi, '| tiêu đề Q đúng:', hd == QC, '| lệch cột tối đa %.2f' % thang, '| ô tóm tắt:', tk, '| số trang', len(a), len(b))
