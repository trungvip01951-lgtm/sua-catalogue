# PEROTAC SS-150 / SSM-150F — catalogue riêng 1 trang A4 ngang (23/10/2026, phiên CLAUDE_20261023T0430Z)
Lệnh anh 23/10/2026: "làm a catalogue con perotac ss-150 lưu lượng max 6m3/h áp max 7m nhé". Số này ngược QĐ 48 (Q max 7, H max 6, đã có trong PEROTAC - Bơm chìm nước thải SS.pdf b617cdf9d4e7) → hỏi; anh trả lời "1. 1  2. 1" = giữ số đã chốt, làm catalogue riêng 1 trang.
Ứng viên 01: PEROTAC - Bơm chìm nước thải SS-150 1.pdf, SHA256 9bec10e100ba…, 260869 byte, 842×595, 1 trang.
Số: DU_LIEU/SS.xlsx (PEROTAC SS-150: 0/6, 6/1.6, 7/0; 0.15 kW / 0.2 HP), không đổi số nào. Chữ: lấy bằng mã từ bản đã duyệt SS PEROTAC (không gõ lại).
SỐ SUY RA: "2 poles" trong khối điều kiện — nguồn chỉ ghi n ≈ 2850 /min; 2850 ở 50 Hz = 2 cực. Biểu đồ vẽ từ SS_ss150.xlsx (bản sao chỉ sửa THONG_TIN.so_cuc = 2; MODEL/QH đã kiểm giống hệt DU_LIEU).
LỖI CÔNG CỤ (chưa sửa, tools/ niêm phong): tools/ve_duong_cong.py đọc ô so_cuc dạng chữ "PDF không ghi số cực (chỉ ghi n ≈ 2850 /min)" thành "2850 poles". Ai vẽ SS từ DU_LIEU/SS.xlsx sẽ dính.
Ảnh: anh.jpg từ ảnh anh gửi 08/10 "SS - PEROTAC - SS-150 den SS-370 (co phao).png" (1145×1374) qua lam_anh.py: nền nối mép → 255, bỏ bóng dưới đế, khung 82%; 951×1395, đặt 130×190 pt = 529 ppi (ảnh trong kho a2daccc46bfe chỉ 345×450 → 202 ppi, không đạt 300 ppi trang 1). Chỉ làm sạch nền, không vẽ lại. Chưa đưa vào KHO_ANH — chờ anh duyệt.
Kiểm: tools/kiem_catalogue.py (--du-lieu kiem_ss150.xlsx = chỉ hàng PEROTAC SS-150) ĐẠT 8, CHƯA ĐẠT 0, bỏ qua mục 9 (1 hãng) và 10 (chưa duyệt). AI khác kiểm độc lập: số, đường (qua đúng 3 điểm; gấp nhẹ tại Q 6 là số đã duyệt), chữ, ảnh (không lẹm, không méo), thẩm mỹ — ĐẠT; 3 góp ý (thiếu tiêu đề MATERIALS, 2 cụm chữ mới, khoảng trống cột giữa) đã sửa trong bản này, kiểm tự động lại ĐẠT 8.
Xem: claude/_xem/xem_4.png. Chưa đưa vào CATALOGUE DA DUYET — chờ anh duyệt.

## Ứng viên 02 (23/10/2026) — theo QĐ 158
Lời anh: "em phải có bảng thông số lưu lượng bao nhiêu cột áp bao nhiêu chia nhiều mức như catalogue khác cho a, đường đặc tính vẽ công mềm mại cho a. lưu 2 quy tắc cho a và sửa lại".
Tệp: PEROTAC - Bơm chìm nước thải SS-150 2.pdf, SHA256 cab8c194f695…, 261255 byte. Số liệu: SS150.xlsx (mk_xlsx.py) — bảng và đường cùng tệp.
| Q m³/h | H m | Loại số |
|---|---|---|
| 0 | 6 | NGUỒN (QĐ 48) |
| 1 | 5.9 | SUY RA H = 6·(1 − (Q/7)²) = 5.878 |
| 2 | 5.5 | SUY RA = 5.510 |
| 3 | 4.9 | SUY RA = 4.898 |
| 4 | 4.0 | SUY RA = 4.041 |
| 5 | 2.9 | SUY RA = 2.939 |
| 6 | 1.6 | NGUỒN (công thức 1.592, giữ số nguồn) |
| 7 | 0 | NGUỒN (Q max) |
Đường: tools/ve_duong_cong.py nối spline bậc 3 (đầu dốc 0) — chỉ nhận khi không tăng, không vượt điểm, không thêm điểm uốn, lệch PCHIP ≤ 2%; 3243 bộ điểm trong DU_LIEU: số bộ lỗi dữ liệu không đổi so với công cụ cũ; 6SP46-8, 6SP60-4, CM 100-200/30 vẫn PCHIP.
Kiểm: kiem_catalogue ĐẠT 8/8 (bỏ qua 9, 10); test_ve_duong_cong 13/13. Kiểm độc lập lần 2: bảng, đường ĐẠT; góp ý công cụ đổi dáng đường catalogue khác + câu quy tắc + báo cáo này — đã sửa.
Chưa đưa vào CATALOGUE DA DUYET — chờ anh duyệt. Ứng viên 01 giữ lại, không dùng.
