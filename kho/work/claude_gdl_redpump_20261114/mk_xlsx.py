# GDL.xlsx — REDPUMP 50GDL18-15×9 (báo giá BaoGia_REDPUMP_50GDL18-15x9_14112026.pdf, QĐ 180). Không có dòng GDL trong DU_LIEU.
# NGUỒN báo giá: 11 kW; Q 0 ~ 22,56 m³/h ứng H 172,29 ~ 112,12 m; điểm làm việc 18 m³/h – 135 m; hút/xả 50/50 mm; 2930 vòng/phút.
# SUY RA: H = 172.29 − k·Q^n qua đúng 3 điểm nguồn; HP 15 (11 kW theo DU_LIEU); 2 cực (2930 /min ở 50 Hz).
import sys, math, openpyxl
OUT = sys.argv[1]; H0, Q1, H1, QD, HD = 172.29, 22.56, 112.12, 18.0, 135.0
n = math.log((H0 - H1) / (H0 - HD)) / math.log(Q1 / QD); k = (H0 - HD) / QD ** n
f = lambda q: H0 - k * q ** n
assert abs(f(QD) - HD) < 1e-9 and abs(f(Q1) - H1) < 1e-9 and n > 1
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in [('khoa', 'gia_tri', 'nguon'), ('nhom', 'GDL (bơm ly tâm đa tầng trục đứng)', 'báo giá 14/11/2026'),
          ('so_cuc', 2, 'SUY RA: 2930 /min ở 50 Hz'), ('toc_do_vg_ph', 2930, 'NGUỒN báo giá')]: ws.append(r)
m = wb.create_sheet('MODEL'); m.append(('hang', 'model_1pha', 'model_3pha', 'p2_kw', 'p2_hp', 'dong_A_1pha', 'dong_A_3pha', 'dien_ap_1pha', 'dien_ap_3pha', 'hong_hut', 'hong_xa', 'thong_so_khac', 'nguon', 'nghi_ngo'))
m.append(('REDPUMP', None, '50GDL18-15×9', 11, 15, None, None, None, '380–415 V', 'DN50', 'DN50',
          f'Q 0–{Q1} m³/h; H {H0}–{H1} m; điểm làm việc {QD:g} m³/h – {HD:g} m; 9 tầng; n_mu {n:.4f}', 'báo giá 14/11/2026', None))
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for q in [0, 3, 6, 9, 12, 15, 18, 21, Q1]:
    if q == 0: h, s = H0, 'NGUỒN báo giá'
    elif q == QD: h, s = HD, 'NGUỒN báo giá (điểm làm việc)'
    elif q == Q1: h, s = H1, 'NGUỒN báo giá'
    else: h, s = round(f(q), 1), f'SUY RA: H = {H0} − {k:.5f}·Q^{n:.4f} = {f(q):.3f}'
    qh.append(('REDPUMP', '50GDL18-15×9', q, h, s))
wb.save(OUT); print(round(n, 4), [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True)])
