# TKP.xlsx — REDPUMP TKP600 / TKP800 (QĐ 172–173). Không có dòng TKP trong DU_LIEU.
# NGUỒN lời anh 03/11/2026: TKP600 Hmax 40 (Q=0), Qmax 3 (H=0), điểm làm việc 2 m³/h – 20 m, 0.4 kW 1 pha 220 V;
# TKP800 Hmax 55, Qmax 4, điểm làm việc 3 m³/h – 20 m, 0.6 kW 1 pha 220 V.
# p2_hp SUY RA = kW / 0.746.
# Mức Q còn lại SUY RA: parabol H = Hmax − b·Q − c·Q² đi đúng 3 điểm nguồn (QĐ 158 — cách SS-150).
import sys, openpyxl
OUT = sys.argv[1]
NG = {'TKP600': (40, 3, 2, 20, 0.4), 'TKP800': (55, 4, 3, 20, 0.6)}
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
ws.append(('khoa', 'gia_tri', 'nguon'))
ws.append(('nhom', 'TKP (bơm tăng áp)', 'báo giá anh 03/11/2026'))
ws.append(('so_cuc', None, 'CHƯA CÓ NGUỒN'))
ws.append(('toc_do_vg_ph', None, 'CHƯA CÓ NGUỒN'))
m = wb.create_sheet('MODEL')
m.append(('hang', 'model_1pha', 'model_3pha', 'p2_kw', 'p2_hp', 'dong_A_1pha', 'dong_A_3pha', 'dien_ap_1pha', 'dien_ap_3pha', 'hong_hut', 'hong_xa', 'thong_so_khac', 'nguon', 'nghi_ngo'))
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for md, (h0, qm, qd, hd, kw) in NG.items():
    m.append(('REDPUMP', md, None, kw, round(kw / 0.746, 2), None, None, '220–240 V', None, None, None,
              f'Hmax {h0} m; Qmax {qm} m³/h; điểm làm việc {qd} m³/h – {hd} m', 'báo giá + lời anh 03/11/2026', None))
    c = (h0 - hd - (h0 * qd / qm)) / (qd * qd - qd * qm); b = h0 / qm - c * qm   # H(qd)=hd, H(qm)=0
    f = lambda q: h0 - b * q - c * q * q
    assert abs(f(qd) - hd) < 1e-9 and abs(f(qm)) < 1e-9 and b > 0 and c > 0
    for i in range(int(qm * 2) + 1):
        q = i / 2
        if q in (0, qd, qm): h, n = {0: h0, qd: hd, qm: 0}[q], 'NGUỒN: lời anh / báo giá 03/11/2026'
        else: h, n = round(f(q), 1), f'SUY RA: H = {h0} − {b:.4f}·Q − {c:.4f}·Q² = {f(q):.3f}'
        qh.append(('REDPUMP', md, q, h, n))
    print(md, [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True) if r[1] == md])
wb.save(OUT)
