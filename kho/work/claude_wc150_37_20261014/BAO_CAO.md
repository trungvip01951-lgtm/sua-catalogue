# PEROTAC 150WC300-30-37 — catalogue riêng 2 trang A4 ngang (14/10/2026, phiên CLAUDE_20261014T0320Z)
Lệnh anh 14/10 10:11 + 10:20: "sửa catalogue perotac theo báo giá này nhé con cắt rác" (báo giá 12/10/2026) → "vẽ nguyên sản phẩm này thôi" = catalogue riêng chỉ mã này, chỉ PEROTAC (thay ứng viên 01 khổ A3 ngày 13/10).
Ứng viên 02: PEROTAC - Bơm cắt rác WC 150WC300-30-37 (UNG VIEN 02).pdf, SHA256 e030d01c8d85…, 1,25 MB, 842×595.
Tr.1 thông số + đường Q–H (tools/ve_duong_cong.py, số WC150_37.xlsx); tr.2 cấu tạo 2 cực + tính năng (chữ, ảnh lấy từ ứng viên 01 = bản đã duyệt).
Đổi so với ứng viên 01: khổ A4; trang thông số lên trước (ảnh bìa ≥300 ppi); bỏ "Curve tolerance according to ISO 9906" (QĐ 149), bỏ cột 1 pha, bỏ tính năng/hàng "Auto-cut motor protector" (chỉ bản 1 pha), bỏ phần 4 cực; thêm khối điều kiện dưới biểu đồ, "Power supply 3~ 380–415 V 50 Hz", "Rated point 300 m³/h – 30 m".
SỐ SUY RA (chờ anh): báo giá "lưu lượng 280–300 m³/h, cột áp max 25–30 m" hiểu là khoảng làm việc, khớp tên model 300 m³/h – 30 m. Đường bậc hai qua 0/53, 300/30, 540/8 (8 m = nấc 8 trong dải 150WC PEROTAC, QĐ 19): Q 0/90/180/270/360/450/540 → H 53/46.6/39.8/32.5/24.8/16.6/8. Báo giá ghi Hmax 25–30 m → nếu anh muốn đúng chữ báo giá thì vẽ lại.
Kiểm tự động kiem_catalogue.py: ĐẠT 7, CHƯA ĐẠT 1 (mục 3: công cụ coi 1 mã trong tệp là nấc 1 → đòi H tại Qmax = 1 m; giữ 8 m theo dải 150WC của bản đã duyệt), bỏ qua 2 (bộ 3 hãng, DANH SACH).
Kiểm độc lập (AI khác): số, nội dung cấm, hình thức ĐẠT; lưu ý nhỏ: câu điều kiện dưới biểu đồ xuống dòng giữa "1" và "mm²/s" (do công cụ vẽ).
Gộp phông: khối biểu đồ/bảng trỏ chung phông của trang; ảnh trang trước/sau khi gộp trùng từng điểm ảnh.
