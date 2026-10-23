# SS150.xlsx — PEROTAC SS-150 / SSM-150F catalogue riêng (QĐ 158: bảng nhiều mức Q, đường cong mềm).
# Số khoá từ DU_LIEU/SS.xlsx (QĐ 48): 0/6, 6/1.6, 7/0. Mức Q 1–5 SUY RA theo H = 6·(1 − (Q/7)²) qua Hmax 6 và Qmax 7
# (tại Q 6 công thức cho 1.59 → giữ số nguồn 1.6, lệch 0.6%).
import sys, openpyxl
R, OUT = sys.argv[1], sys.argv[2]
src = openpyxl.load_workbook(R + '/DU_LIEU/SS.xlsx')
pts = {r[2]: r[3] for r in src['QH'].iter_rows(min_row=2, values_only=True) if r[0] == 'PEROTAC' and r[1] == 'SS-150'}
assert pts == {0: 6, 6: 1.6, 7: 0}, pts
f = lambda q: 6 * (1 - (q / 7) ** 2)
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in src['THONG_TIN'].iter_rows(values_only=True):
    if r[0] == 'so_cuc': r = ('so_cuc', 2, 'SUY RA: n ≈ 2850 /min ở 50 Hz = 2 cực (nguồn PDF không ghi số cực)')
    if r[0] == 'toc_do_vg_ph': r = ('toc_do_vg_ph', 2850, r[2])
    ws.append(r)
m = wb.create_sheet('MODEL'); hdr = None
for r in src['MODEL'].iter_rows(values_only=True):
    if hdr is None: hdr = r; m.append(r)
    elif r[0] == 'PEROTAC' and r[2] == 'SS-150': m.append(r)
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for q in range(8):
    if q in pts: h, n = pts[q], 'NGUỒN: DU_LIEU/SS.xlsx (QĐ 48)'
    else: h, n = round(f(q), 1), f"SUY RA: H = 6·(1 − (Q/7)²) = {f(q):.3f}, làm tròn 0,1 m (QĐ 158)"
    qh.append(('PEROTAC', 'SS-150', q, h, n))
wb.save(OUT)
print([(q, r[3]) for q, r in enumerate(qh.iter_rows(min_row=2, values_only=True))], 'f(6)=%.3f' % f(6))
