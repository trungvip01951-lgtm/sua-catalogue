# SP60.xlsx — REDPUMP dải 6SP60 (17 mã) cho catalogue riêng (03/11/2026, QĐ 166).
# Q–H, kW/HP: DU_LIEU/SP.xlsx (REDPUMP - Bơm giếng SP.pdf tr.14). Kích thước P/M/T: tr.15. η: số hoá đường "η (%)" tr.14 (đường chung cả dải).
import sys, numpy as np, pymupdf, openpyxl
R, OUT = sys.argv[1], sys.argv[2]
src = openpyxl.load_workbook(R + '/DU_LIEU/SP.xlsx', data_only=True)
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in src['THONG_TIN'].iter_rows(values_only=True): ws.append(r)
m = wb.create_sheet('MODEL'); hdr = True; md = []
for r in src['MODEL'].iter_rows(values_only=True):
    if hdr or (r[0] == 'REDPUMP' and str(r[2]).startswith('6SP60-')): m.append(r); md += [] if hdr else [r[2]]
    hdr = False
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for r in src['QH'].iter_rows(min_row=2, values_only=True):
    if r[0] == 'REDPUMP' and r[1] in md: qh.append(r)
D = pymupdf.open(R + '/CATALOG SUA/CATALOGUE DA DUYET/REDPUMP/REDPUMP - Bơm giếng SP.pdf')
L = [s.strip() for s in D[14].get_text().splitlines() if s.strip()]; i = L.index('6SP60  |  Outlet 3 in'); j = i + 5; kt = []
while j < len(L) and L[j].startswith('6SP60-'): kt.append(L[j:j + 4]); j += 4
assert [k[0] for k in kt] == md, (len(kt), len(md))
k = wb.create_sheet('KICH_THUOC'); k.append(('model', 'P_mm', 'M_mm', 'T_mm', 'nguon'))
for r in kt: k.append((r[0], int(r[1]), int(r[2]), int(r[3]), 'REDPUMP - Bơm giếng SP.pdf tr.15 (6SP60 | Outlet 3 in)'))
p = D[13]; c = [x for x in p.get_drawings() if x.get('color') and abs(x['color'][0] - 0.49) < 0.01 and x['rect'].y0 > 320 and x['rect'].y1 < 349]
assert len(c) == 1; pts = []
for it in c[0]['items']:
    P0, P1, P2, P3 = it[1:5]
    for t in np.linspace(0, 1, 60):
        pts.append(((1 - t) ** 3 * P0.x + 3 * t * (1 - t) ** 2 * P1.x + 3 * t * t * (1 - t) * P2.x + t ** 3 * P3.x,
                    (1 - t) ** 3 * P0.y + 3 * t * (1 - t) ** 2 * P1.y + 3 * t * t * (1 - t) * P2.y + t ** 3 * P3.y))
pts = np.array(sorted(pts)); q = (pts[:, 0] - 457.0) / (783.0 - 457.0) * 90; e = (348.0 - pts[:, 1]) / (348.0 - 322.222) * 80
eta = wb.create_sheet('ETA'); eta.append(('q_m3h', 'eta_pct', 'nguon'))
for qq in range(0, 79, 3):
    if qq <= q.max() + 1e-6: eta.append((qq, round(float(np.interp(qq, q, e)), 1), 'số hoá đường η (%) REDPUMP - Bơm giếng SP.pdf tr.14 (trục 0–80 %, Q 0–90 m³/h), đường chung dải 6SP60'))
eta.append(('dinh', round(float(e.max()), 1), f'đỉnh tại Q {q[e.argmax()]:.1f} m³/h'))
wb.save(OUT); print(len(md), 'model; eta', [(r[0], r[1]) for r in eta.iter_rows(min_row=2, values_only=True)][::3])
