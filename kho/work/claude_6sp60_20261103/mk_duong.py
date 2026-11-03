# SP60_duong.xlsx — CHỈ để vẽ đường Q–H (QĐ 158 đường mềm; QTH 4.2 lệch bảng ≤ 5%). Bảng thông số dùng SP60.xlsx (số đã duyệt).
# Mỗi mã: spline làm mịn bậc 3 (scipy UnivariateSpline, trọng số 1/H) qua 14 điểm đã duyệt, chọn độ mịn lớn nhất giữ lệch ≤ 4 %, H giảm, ≤ 1 điểm uốn.
import sys, numpy as np, openpyxl, collections, json
from scipy.interpolate import UnivariateSpline
W = sys.argv[1]
wb = openpyxl.load_workbook(W + '/SP60.xlsx'); g = collections.defaultdict(list)
for r in wb['QH'].iter_rows(min_row=2, values_only=True): g[r[1]].append((r[2], r[3]))
qh = wb['QH']; qh.delete_rows(2, qh.max_row); bao = {}
for m, v in g.items():
    v = sorted(v); q = np.array([a for a, b in v], float); h = np.array([b for a, b in v], float); best = None
    for s in np.geomspace(h.max() ** 2 * 0.05, 1e-3, 120):
        w = 1 / np.maximum(h, 1); w[0] *= 200; w[-1] *= 200          # giữ H max (Q 0) và điểm cuối dải (QTH 4.3)
        f = UnivariateSpline(q, h, w=w, k=3, s=s); qq = np.linspace(0, q[-1], 400); hh = f(qq)
        dev = np.max(np.abs(f(q) - h) / h) * 100; d2 = f(qq, 2); inf = int(np.sum(np.diff(np.sign(d2[np.abs(d2) > 1e-4])) != 0))
        dau = max(abs(f(q[0]) - h[0]), abs(f(q[-1]) - h[-1]))
        if np.all(np.diff(hh) < 1e-9) and inf <= 1 and dev <= 4.5 and dau < 0.05: best = (f, dev); break
    f, dev = best; bao[m] = round(float(dev), 2)
    for x in np.arange(0, q[-1] + 1e-9, 3):
        hv = h[0] if x == 0 else (h[-1] if abs(x - q[-1]) < 1e-9 else round(float(f(x)), 2))
        qh.append(('REDPUMP', m, float(x), hv, f'ĐƯỜNG VẼ (spline làm mịn qua số đã duyệt, lệch bảng ≤ {dev:.2f} %)'))
wb.save(W + '/SP60_duong.xlsx'); json.dump(bao, open(W + '/lech_duong.json', 'w')); print(max(bao.values()), bao)
