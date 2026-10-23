# WC200_55.xlsx — PEROTAC 200WC450-32-55 (lệnh anh 16/10/2026 15:45 + ảnh web)
import sys, numpy as np, openpyxl
R = sys.argv[1]
irg = openpyxl.load_workbook(R + '/DU_LIEU/IRG.xlsx', data_only=True)['MODEL']
HP = [r[4] for r in irg.iter_rows(min_row=2, values_only=True) if r[0] == 'REDPUMP' and r[2] == 'IRG300-315/55-4'][0]
LENH = 'Lệnh anh 16/10/2026 15:45 "vẽ catalogue con này cho a nhé" + "perotac"; ảnh trang web: 200WC450-32-55, 55 Kw, lưu lượng max 760 m³/h, cột áp max 44 m, DN200, 3 pha/380V/50Hz, IP68, cách điện F'
# H = 44 − a·Q² − b·Q³ qua 0/44 (Hmax), 450/32 (tên model), 760/5 (Qmax; H 5 m = nấc 5 dải 200WC theo QĐ 19)
A = np.array([[450 ** 2, 450 ** 3], [760 ** 2, 760 ** 3]]); a, b = np.linalg.solve(A, [44 - 32, 44 - 5])
f = lambda q: 44 - a * q * q - b * q ** 3
CT = f'H = 44 − {a:.4e}·Q² − {b:.4e}·Q³'
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'; ws.append(('khoa', 'gia_tri', 'nguon'))
for r in [('nhom', 'WC (bơm cắt rác chìm) — catalogue riêng 1 model', LENH),
          ('ten_dong_EN', 'WC SERIES - Submersible sewage pumps with cutter', 'PEROTAC - Bơm cắt rác WC.pdf tr.1'),
          ('hang_co', 'PEROTAC (1 model 3 pha)', 'lệnh anh "perotac"'), ('tan_so', '50 Hz', 'ảnh web 3 pha/380V/50Hz'),
          ('so_cuc', '4', 'PEROTAC - Bơm cắt rác WC.pdf: 200WC–300WC 4 cực (THONG_TIN DU_LIEU/WC.xlsx)'),
          ('toc_do_vg_ph', '1450', 'như so_cuc'), ('dien_ap', '3 pha 380–415 V / 50 Hz', 'rules: >3 kW chỉ 3 pha')]: ws.append(r)
m = wb.create_sheet('MODEL')
m.append(('hang', 'model_1pha', 'model_3pha', 'p2_kw', 'p2_hp', 'dong_A_1pha', 'dong_A_3pha', 'dien_ap_1pha', 'dien_ap_3pha', 'hong_hut', 'hong_xa', 'thong_so_khac', 'nguon', 'nghi_ngo'))
m.append(('PEROTAC', None, '200WC450-32-55', 55, HP, None, None, None, '380–415 V', None, 200, 'số cực=4; n=1450 vg/ph',
          LENH + f'; HP {HP} quy đổi theo 55 kW trong DU_LIEU/IRG.xlsx',
          'Dòng web "Lưu lượng 50–600 m³/h, Cột áp 30–4 m" trùng dải của 200WC250-22-30 và mâu thuẫn tên model (450 m³/h – 32 m) → KHÔNG dùng, hỏi anh; H tại Qmax SUY RA'))
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
goc = {0: 'WEB: cột áp max 44 m', 450: 'TÊN MODEL: 450 m³/h – 32 m'}
for q in [0, 100, 200, 300, 400, 450, 500, 600, 700, 760]:
    h = {0: 44, 450: 32, 760: 5}.get(q, round(float(f(q)), 1))
    qh.append(('PEROTAC', '200WC450-32-55', q, h, goc.get(q, 'WEB: lưu lượng max 760 m³/h; H 5 m SUY RA (QĐ 19 nấc 5)' if q == 760 else f'SUY RA: {CT} qua 0/44, 450/32, 760/5; làm tròn 0,1 m')))
wb.save('WC200_55.xlsx'); print('ok HP', HP, CT, [round(float(f(q)), 1) for q in (100, 200, 300, 400, 500, 600, 700)])
