# WCL.xlsx — REDPUMP 150WC / 200WC 37–132 kW, 14 mã (lời anh 13/11/2026, QĐ 174). Không có trong DU_LIEU/WC.xlsx.
# NGUỒN lời anh: Qmax (H = 0), Hmax (Q = 0), P2. Điểm định mức Q–H: tên model (quy ước mã NNWCQ-H-P, DU_LIEU/WC.xlsx THONG_TIN).
# H tại Qmax = nấc công suất trong cỡ họng (QĐ 19), nối tiếp dải REDPUMP đã duyệt: 150WC có 7 mã 5.5–22 kW (nấc 1–7) → 37 kW = nấc 8 … 132 kW = 14;
#   200WC có 4 mã 11–30 kW (nấc 1–4) → 37 kW = nấc 5 … 132 kW = 11.
# SUY RA: H = Hmin + (Hmax − Hmin)·(1 − (Q/Qmax)^n), n chọn để qua đúng điểm định mức; nếu n < 1 (điểm định mức nằm dưới dây cung)
#   dùng parabol lồi H = Hmax − b·Q − c·Q² (c < 0, như dáng bảng WC đã duyệt) — đều đơn điệu, không điểm uốn; HP theo DU_LIEU/IRG.xlsx;
# số cực / tốc độ theo dải (150WC 2 cực n ≈ 2900; 200WC 4 cực n ≈ 1450 — DU_LIEU/WC.xlsx THONG_TIN).
import sys, math, openpyxl
OUT = sys.argv[1]
L = """150WC200-35-37 350 45 37
200WC350-22-37 780 40 37
150WC200-40-45 350 55 45
200WC300-32-45 700 45 45
150WC180-50-55 350 70 55
200WC300-40-55 600 60 55
150WC200-60-75 350 80 75
200WC350-45-75 600 65 75
150WC200-70-90 350 90 90
200WC300-60-90 600 75 90
150WC180-80-110 300 105 110
200WC300-65-110 600 85 110
150WC200-90-132 300 120 132
200WC400-75-132 600 105 132"""
HP = {37: 50, 45: 60, 55: 75, 75: 100, 90: 120, 110: 150, 132: 176}
NAC0 = {'150': 7, '200': 4}; KWS = [37, 45, 55, 75, 90, 110, 132]
GRID = {'150': [0, 50, 100, 150, 180, 200, 250, 300, 350], '200': [0, 100, 200, 300, 350, 400, 500, 600, 700, 780]}
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
for r in [('khoa', 'gia_tri', 'nguon'), ('nhom', 'WC (bơm cắt rác chìm) 150WC/200WC 37–132 kW', 'lời anh 13/11/2026'),
          ('so_cuc', 'REDPUMP: 2 (150WC); 4 (200WC)', 'SUY RA theo dải DU_LIEU/WC.xlsx'), ('toc_do_vg_ph', 'REDPUMP: 2900 (150WC); 1450 (200WC)', 'SUY RA theo dải')]: ws.append(r)
m = wb.create_sheet('MODEL'); m.append(('hang', 'model_1pha', 'model_3pha', 'p2_kw', 'p2_hp', 'dong_A_1pha', 'dong_A_3pha', 'dien_ap_1pha', 'dien_ap_3pha', 'hong_hut', 'hong_xa', 'thong_so_khac', 'nguon', 'nghi_ngo', 'thu_tu'))
qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
for i, l in enumerate(L.splitlines(), 1):
    md, qm, hm, kw = l.split(); qm, hm, kw = float(qm), float(hm), int(kw)
    dn, rest = md.split('WC'); qr, hr, k2 = map(float, rest.split('-')); assert k2 == kw
    hmin = NAC0[dn] + KWS.index(kw) + 1
    n = math.log(1 - (hr - hmin) / (hm - hmin)) / math.log(qr / qm)
    if n >= 1: f = lambda q: hmin + (hm - hmin) * (1 - (q / qm) ** n); cong = f'Hmin + (Hmax − Hmin)·(1 − (Q/Qmax)^{n:.4f})'
    else:
        c = ((hm - hmin) * qr - (hm - hr) * qm) / (qr * qm * (qm - qr)); b = (hm - hr - c * qr * qr) / qr
        f = lambda q: hm - b * q - c * q * q; cong = f'{hm:g} − {b:.5f}·Q − ({c:.4e})·Q²'
        assert b > 0 and b + 2 * c * qm > 0, md
    assert abs(f(qr) - hr) < 1e-9 and abs(f(qm) - hmin) < 1e-9 and n < 5, (md, n)
    m.append(('REDPUMP', None, md, kw, HP[kw], None, None, None, '380–415 V', None, f'DN{dn}',
              f'Qmax {qm:g} m³/h; Hmax {hm:g} m; Hmin {hmin} m (nấc QĐ 19); định mức {qr:g} m³/h – {hr:g} m; n_mu {n:.4f}; {"2 cực n≈2900" if dn == "150" else "4 cực n≈1450"}', 'lời anh 13/11/2026', None, i))
    for q in GRID[dn] + ([qr] if qr not in GRID[dn] else []):
        if q > qm: continue
        if q == 0: h, s = hm, 'NGUỒN: Hmax lời anh'
        elif q == qm: h, s = hmin, f'NGUỒN: Qmax lời anh; H = nấc {hmin} (QĐ 19)'
        elif q == qr: h, s = hr, 'NGUỒN: định mức theo tên model'
        else: h, s = round(f(q), 1), f'SUY RA: H = {cong} = {f(q):.3f}'
        qh.append(('REDPUMP', md, q, h, s))
    print(md, round(n, 3), [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True) if r[1] == md])
wb.save(OUT)
