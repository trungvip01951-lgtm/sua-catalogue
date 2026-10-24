# CM2.xlsx — AQUARIS catalogue riêng 2 mã: CM 32-250/7.5 + CM 40-160/4 (lệnh anh 24/10/2026, ảnh bảng báo giá).
# CM 40-160/4: số DU_LIEU/CM.xlsx (khớp báo giá 9–39 m³/h, 35.5–25 m).
# CM 32-250/7.5: anh chốt "theo báo giá" (Q 6–36 m³/h, H 73–38 m) — khác DU_LIEU (0–24, 69.5–53).
#   Mức Q 9…33 SUY RA theo H = 74 − Q²/36 (qua 6/73 và 36/38), làm tròn 0,1 m (QĐ 158).
import sys, openpyxl
from decimal import Decimal, ROUND_HALF_UP
R, OUT = sys.argv[1], sys.argv[2]
LENH = 'Lệnh anh 24/10/2026: "Làm cho a catalogue aquaris cm 2 mã này nhé" (ảnh báo giá: CM32-250/7.5 6–36 m3/h, 73–38 m; CM40-160/4.0 9–39 m3/h, 35.5–25 m) + "Theo báo giá"'
src = openpyxl.load_workbook(R + '/DU_LIEU/CM.xlsx', data_only=True)
MD = ['CM 32-250/7.5', 'CM 40-160/4']
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in src['THONG_TIN'].iter_rows(values_only=True):
    if r[0] == 'toc_do_vg_ph': r = ('toc_do_vg_ph', 2850, 'AQUARIS - Bơm trục ngang CM.pdf tr.2, tr.3: CM 32-250/7.5 và CM 40-160/4 n ≈ 2850 /min')
    ws.append(r)
m = wb.create_sheet('MODEL'); first = True
for r in src['MODEL'].iter_rows(values_only=True):
    if first or (r[0] == 'AQUARIS' and r[2] in MD): m.append(r)
    first = False
assert m.max_row == 3
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for r in src['QH'].iter_rows(min_row=2, values_only=True):
    if r[0] == 'AQUARIS' and r[1] == 'CM 40-160/4': qh.append(r)
r1 = lambda x: float(Decimal(str(x)).quantize(Decimal('0.1'), ROUND_HALF_UP))
for q in range(6, 37, 3):
    if q == 6: h, n = 73, 'BÁO GIÁ: cột áp max 73 m tại Q min 6 m³/h'
    elif q == 36: h, n = 38, 'BÁO GIÁ: Q max 36 m³/h, cột áp 38 m'
    else: h, n = r1(74 - q * q / 36), f'SUY RA: H = 74 − Q²/36 = {74 - q * q / 36:.3f} (qua 6/73, 36/38), làm tròn 0,1 m'
    qh.append(('AQUARIS', 'CM 32-250/7.5', q, h, n + '; ' + LENH))
wb.save(OUT)
for k in MD: print(k, [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True) if r[1] == k])
print([(r[2], r[3], r[4], r[6], r[9], r[10]) for r in m.iter_rows(min_row=2, values_only=True)])
