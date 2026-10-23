# REDPUMP 300IRG800-30-110 — catalogue riêng 1 trang A4 ngang (16/10/2026, phiên CLAUDE_20261016T0826Z)
Lệnh anh 16/10/2026 15:26: "làm cho a catalogue bơm 300IRG800-30-110 lưu lượng max 880m3/h áp max 35m hmin 21m q min 600m3/h / làm cả đường đặc tính cho a nhé" + "làm redpump".
Ứng viên 03: REDPUMP - Bơm trục đứng IRG 300IRG800-30-110 (UNG VIEN 03).pdf, SHA256 e4c75ed485fc83de…, 0,54 MB, 842×595. (01, 02 bỏ: chồng số trang; tương phản nhãn.)
Cách hiểu: cặp đầu–cuối dải làm việc Qmin 600/H 35, Qmax 880/H 21; điểm định mức 800/30 theo tên model.
SỐ SUY RA: H = 36,6439 − 3,2674·(Q/880)² − 12,3764·(Q/880)^12 qua 600/35, 800/30, 880/21; điểm 0/36,6 · 200/36,5 · 400/36 · 500/35,6 · 700/33,8 · 750/32,5 · 850/25,4. 4 cực n≈1450 và 150 HP lấy theo dải IRG300 (DU_LIEU/IRG.xlsx). QĐ 149 "IRG không vẽ đường" là cho catalogue bảng IRG; lần này anh yêu cầu vẽ đường.
Chữ/vật liệu: REDPUMP - Bơm trục đứng IRG.pdf tr.1. Ảnh KHO_ANH/Bom_truc_dung_IRG/7e0835bfdec8.png; logo KHO_ANH/Bom_chim_nuoc_thai_FC_inox/eb3ac079a784.jpeg.
Kiểm: kiem_catalogue.py ĐẠT 8/8 (bỏ qua bộ 3 hãng, DANH SACH). AI khác kiểm độc lập: bảng khớp 10/10 điểm, đường lệch ≤0,02%, qua 3 điểm chốt, đơn điệu, cong không đổi chiều; điểm định mức và dải làm việc đúng; chữ cấm không có — ĐẠT.
Chưa đưa vào CATALOGUE DA DUYET / DU_LIEU — chờ anh duyệt.

## Ứng viên 04 (16/10/2026 15:39, theo lệnh anh "có q min và hmin thì đường chỉ vẽ từ qmin-qmax và hmin-hmax thôi k vẽ cả như e đang vẽ")
REDPUMP - Bơm trục đứng IRG 300IRG800-30-110 (UNG VIEN 04).pdf, SHA256 c8f5972061bb0038…; số IRG300_04.xlsx, mã build_irg300_04.py, mk_xlsx_04.py, qh04/.
Đường chỉ 600–880 m³/h (35→21 m); điểm 600/35 · 650/34,5 · 700/33,8 · 750/32,5 · 800/30 · 850/25,4 · 880/21 (650, 700, 750, 850 SUY RA, cùng công thức); bỏ dải tô. kiem_catalogue ĐẠT 8/8, lệch đường–bảng 0,0%. Ứng viên 03 bỏ.
