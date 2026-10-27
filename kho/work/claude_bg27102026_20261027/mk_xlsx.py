# Số liệu 2 catalogue riêng PEROTAC theo báo giá BG-27102026-001 (27/10/2026, khách Anh Tuấn).
# Anh đã chốt "theo báo giá" (QĐ 159) — mã lệch DU_LIEU dùng số báo giá; mức giữa SUY RA H = a − b·Q² qua 2 đầu dải (QĐ 158).
import sys, openpyxl
from decimal import Decimal, ROUND_HALF_UP
R, W = sys.argv[1], sys.argv[2]
BG = 'Báo giá BG-27102026-001 (27/10/2026) anh gửi'
r1 = lambda x: float(Decimal(str(round(x, 9))).quantize(Decimal('0.1'), ROUND_HALF_UP))
def bo(nhom, out, models, toc):
    src = openpyxl.load_workbook(f'{R}/DU_LIEU/{nhom}.xlsx', data_only=True)
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'THONG_TIN'
    for r in src['THONG_TIN'].iter_rows(values_only=True):
        if r[0] == 'toc_do_vg_ph': r = ('toc_do_vg_ph', toc, r[2])
        if r[0] == 'so_cuc': r = ('so_cuc', 2, r[2] if r[1] else 'SUY RA: n ≈ 2900 /min ở 50 Hz = 2 cực')
        ws.append(r)
    m = wb.create_sheet('MODEL'); hdr = True
    for r in src['MODEL'].iter_rows(values_only=True):
        if hdr or (r[0] == 'PEROTAC' and r[2] in models): m.append(r)
        hdr = False
    assert m.max_row == len(models) + 1
    qh = wb.create_sheet('QH'); qh.append(('hang', 'model', 'q_m3h', 'h_m', 'nguon'))
    for md, cfg in models.items():
        if cfg is None or isinstance(cfg, dict):
            sua = cfg or {}
            for r in src['QH'].iter_rows(min_row=2, values_only=True):
                if r[0] == 'PEROTAC' and r[1] == md:
                    if r[2] in sua:
                        r = (r[0], r[1], r[2], sua[r[2]], f'SỬA cũ {r[3]} → mới {sua[r[2]]} để đường cong đều/mềm (QĐ 158, QTH 4.2): đường bậc 2 qua 5/124 và 12/78; ' + str(r[4]))
                    qh.append(r)
            continue
        (q0, h0), (q1, h1), buoc = cfg[:3]; them = cfg[3] if len(cfg) > 3 else []; tron = cfg[4] if len(cfg) > 4 else {}
        b = (h0 - h1) / (q1 ** 2 - q0 ** 2); a = h0 + b * q0 ** 2
        qs = []; q = q0
        while q <= q1 + 1e-9: qs.append(q); q += buoc
        for q in sorted(set(qs) | set(them)):
            if q == q0: h, n = h0, f'BÁO GIÁ: {q0}–{q1} m³/h, {h0}–{h1} m (đầu dải)'
            elif q == q1: h, n = h1, f'BÁO GIÁ: {q0}–{q1} m³/h, {h0}–{h1} m (cuối dải)'
            else: h, n = r1(a - b * q * q), ('SỐ DỰNG (cột Q chung với model khác, QTH 4.7): ' if q in them else 'SUY RA: ') + f'H = {a:.4f} − {b:.6f}·Q² = {a - b * q * q:.3f}, làm tròn 0,1 m'
            if q in tron: n += f' → chọn {tron[q]} (làm tròn lên/xuống 0,1 m để đường mềm, lệch công thức ≤ 0,06 m)'; h = tron[q]
            qh.append(('PEROTAC', md, q, h, n + '; ' + BG))
    wb.save(out)
    for md in models: print(md, [(r[2], r[3]) for r in qh.iter_rows(min_row=2, values_only=True) if r[1] == md])
bo('CM', W + '/CM32_160_3.xlsx', {'CM 32-160/3': ((9, 29.2), (36, 20.5), 3, [], {12: 28.8, 24: 25.6, 27: 24.5})}, 2900)
bo('CDLF', W + '/CDLF_2MA.xlsx', {'CDLF8-12T': {6: 120.6, 7: 116.1, 8: 110.6, 9: 104.1, 10: 96.4, 11: 87.7}, 'CDLF16-8T': ((6, 106.6), (24, 38.3), 2, [7, 9, 11])}, 2900)
