# FC75_40.xlsx — PEROTAC FC 75/40M (1 pha, báo giá BG-27102026-010) + FC 75/40T (3 pha, QTH: có 1 pha phải có 3 pha).
# Số: DU_LIEU/FS_FC.xlsx (khớp báo giá: 0.55 kW, Q max 18, H max 9.5). Mức Q 3/9/15 SỐ DỰNG theo đường của chính model (QĐ 158).
import sys, openpyxl
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, sys.argv[1] + '/tools'); import ve_duong_cong as V
R, OUT = sys.argv[1], sys.argv[2]
src = openpyxl.load_workbook(R + '/DU_LIEU/FS_FC.xlsx', data_only=True)
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in src['THONG_TIN'].iter_rows(values_only=True): ws.append(r)
m = wb.create_sheet('MODEL'); hdr = True
for r in src['MODEL'].iter_rows(values_only=True):
    if hdr or (r[0] == 'PEROTAC' and r[2] == 'FC 75/40T'): m.append(r)
    hdr = False
assert m.max_row == 2
pts = sorted((r[2], r[3]) for r in src['QH'].iter_rows(min_row=2, values_only=True) if r[0] == 'PEROTAC' and r[1] == 'FC 75/40T')
assert pts == [(0, 9.5), (6, 7), (12, 5), (18, 2)], pts
f = V.kiem_duong(dict(khoa='FC 75/40T', diem=[(q, h, i) for i, (q, h) in enumerate(pts)]), True)
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
r1 = lambda x: float(Decimal(str(round(float(x), 9))).quantize(Decimal('0.1'), ROUND_HALF_UP))
for q in range(0, 19, 3):
    if q in dict(pts): qh.append(('PEROTAC', 'FC 75/40T', q, dict(pts)[q], 'NGUỒN: DU_LIEU/FS_FC.xlsx (PEROTAC - Bơm chìm nước thải FC.pdf tr.1)'))
    else: qh.append(('PEROTAC', 'FC 75/40T', q, r1(f(q)), f'SỐ DỰNG theo đường của chính model ({type(f).__name__} qua 4 điểm nguồn) = {float(f(q)):.3f}, làm tròn 0,1 m (QĐ 158)'))
wb.save(OUT)
print(type(f).__name__, [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True)])
