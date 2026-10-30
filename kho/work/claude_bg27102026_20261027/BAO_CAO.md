# PEROTAC — 2 catalogue riêng theo báo giá BG-27102026-001 (27/10/2026, phiên CLAUDE_20261027T0100Z)
Lệnh anh (QĐ 161): "Làm a catalogue 2 bộ này nhé 1 bộ 1 con 1 bộ 2 con" + ảnh báo giá (bao_gia_BG-27102026-001.png, khách Anh Tuấn).
Bộ 1: PEROTAC - Bơm trục ngang CM 32-160-3 1.pdf — số CM32_160_3.xlsx.
Bộ 2: PEROTAC - Bơm trục đứng CDLF8-12T và CDLF16-8T 1.pdf — số CDLF_2MA.xlsx. Mã dựng: build_bg27.py (cm|cdlf), mk_xlsx.py.
| Model | Q m³/h | H m | Loại số |
|---|---|---|---|
| CM 32-160/3 | 9 … 36 (bước 3) | 29.2, 28.8, 28.2, 27.5, 26.6, 25.6, 24.5, 23.3, 22.0, 20.5 | BÁO GIÁ 2 đầu dải (DU_LIEU 0–27, 35–15 — áp QĐ 159, anh xác nhận); mức giữa SUY RA H = 29.78 − 0.00716·Q², làm tròn 0,1 m chọn lên/xuống để đường mềm (lệch ≤ 0.06 m) |
| CDLF8-12T | 5 … 12 (bước 1) | 124 … 78 | NGUỒN DU_LIEU (khớp báo giá); SỬA 6 ô giữa để đường đều (lệch ≤ 0.7 m, < 1%): 120→120.6, 116→116.1, 111→110.6, 104→104.1, 97→96.4, 87→87.7 |
| CDLF16-8T | 6 … 24 (bước 2) + 7, 9, 11 | 106.6 … 38.3 | BÁO GIÁ 2 đầu dải (DU_LIEU 8–22, 110–70 — áp QĐ 159); SUY RA mức giữa; 7/9/11 SỐ DỰNG (cột Q chung) |
Tên 3 pha có hậu tố T (QTH 2: CDLF8-12T). Chữ: bản đã duyệt PEROTAC CM tr.1, CDLF tr.1–2 lấy bằng mã. Ảnh: CM 11a1ade937e6.jpeg (303 ppi); CDLF 89efdf5b933e.png (cùng hình 9655a7b5762b PEROTAC đã duyệt, bản nét hơn; 304 ppi).
Kiểm tự động: kiem_catalogue ĐẠT 8/8 cả 2 bản. Chưa đưa vào CATALOGUE DA DUYET — chờ anh duyệt.
Kiểm độc lập (AI khác): CDLF ĐẠT (số, đường mềm 0 lần đổi chiều, chữ, ảnh); CM số/chữ/ảnh ĐẠT nhưng đường gợn (làm tròn 0,1 m) → đã chọn lại 3 ô (12: 28.7→28.8, 24: 25.7→25.6, 27: 24.6→24.5), đường spline, đo trên PDF 0 lần đổi chiều độ cong; kiem_catalogue ĐẠT 8/8.
SHA256: CM 5c99a75dfaae…, CDLF c1dd393dcceb….
