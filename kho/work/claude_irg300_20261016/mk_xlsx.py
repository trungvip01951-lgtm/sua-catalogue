# Tạo IRG300.xlsx — số liệu 300IRG800-30-110 (lệnh anh 16/10/2026 15:26)
import sys, numpy as np, openpyxl
R = sys.argv[1]
src = openpyxl.load_workbook(R + '/DU_LIEU/IRG.xlsx', data_only=True)['MODEL']
ref = [r for r in src.iter_rows(min_row=2, values_only=True) if r[0] == 'REDPUMP' and r[2] == 'IRG300-400/110-4'][0]
KW, HP = ref[3], ref[4]
LENH = 'Lệnh anh 16/10/2026 15:26: "300IRG800-30-110 lưu lượng max 880m3/h áp max 35m hmin 21m q min 600m3/h" + "làm redpump"'
P = [(600, 35), (800, 30), (880, 21)]; p = 12
A = np.array([[1, -(q / 880) ** 2, -(q / 880) ** p] for q, h in P]); H0, c1, c2 = np.linalg.solve(A, [h for q, h in P])
f = lambda q: H0 - c1 * (q / 880) ** 2 - c2 * (q / 880) ** p
CT = f'H = {H0:.4f} − {c1:.4f}·(Q/880)² − {c2:.4f}·(Q/880)^12'
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
ws.append(('khoa', 'gia_tri', 'nguon'))
for r in [('nhom', 'IRG300 (bơm trục đứng ly tâm 1 tầng, catalogue riêng 1 model)', LENH),
          ('ten_dong_EN', 'IRG SERIES - Single-suction centrifugal pump', 'REDPUMP - Bơm trục đứng IRG.pdf tr.1'),
          ('hang_co', 'REDPUMP (1 model 3 pha)', 'lệnh anh "làm redpump"'),
          ('tan_so', '50 Hz', 'REDPUMP - Bơm trục đứng IRG.pdf tr.1'),
          ('so_cuc', '4', 'SUY RA: mọi IRG300 trong DU_LIEU/IRG.xlsx là 4 cực (REDPUMP - Bơm trục đứng IRG.pdf tr.5)'),
          ('toc_do_vg_ph', '1450', 'như so_cuc'),
          ('dien_ap', '3 pha 380–415 V / 50 Hz', 'rules: >3 kW chỉ 3 pha')]: ws.append(r)
m = wb.create_sheet('MODEL')
m.append(('hang', 'model_1pha', 'model_3pha', 'p2_kw', 'p2_hp', 'dong_A_1pha', 'dong_A_3pha', 'dien_ap_1pha', 'dien_ap_3pha', 'hong_hut', 'hong_xa', 'thong_so_khac', 'nguon', 'nghi_ngo'))
m.append(('REDPUMP', None, '300IRG800-30-110', KW, HP, None, None, None, '380–415 V', 300, 300, 'số cực=4; n=1450 vg/ph',
          LENH + f'; kW theo tên model; HP {HP} lấy theo IRG300-400/110-4 (DU_LIEU/IRG.xlsx); DN300×300 theo tên model và dải IRG300',
          'Qmin 600/Hmax 35, Qmax 880/Hmin 21 theo lệnh anh (hiểu là cặp đầu–cuối dải làm việc); 800/30 theo tên model; điểm khác SUY RA'))
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for q in [0, 200, 400, 500, 600, 700, 750, 800, 850, 880]:
    goc = {600: 'ANH: Qmin 600 – Hmax 35', 800: 'TÊN MODEL: 800 m³/h – 30 m', 880: 'ANH: Qmax 880 – Hmin 21'}
    h = dict(P).get(q, round(float(f(q)), 1))
    qh.append(('REDPUMP', '300IRG800-30-110', q, h, goc.get(q, f'SUY RA: {CT} qua 600/35, 800/30, 880/21; làm tròn 0,1 m')))
wb.save('IRG300.xlsx'); print('ok', KW, HP, round(H0, 2))
