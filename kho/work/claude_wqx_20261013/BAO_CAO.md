# PEROTAC 80WQX40-15-5.5 — catalogue riêng 1 trang (13/10/2026, phiên CLAUDE_WQX_20261013)
Nguồn: báo giá BG-13102026-004 (12/10/2026) + ảnh anh gửi 13/10 (ANH GOC ...png). Mã dựng: build_wqx.py (pymupdf, Liberation Sans 2, logo lấy nguyên từ PEROTAC FC inox đã duyệt).
Ứng viên: UNG VIEN 01b — SHA 876fabcbc7ee48d13ad84656d6bf831706e06b66e0c2cc249935cff72a8c4ae7. (UNG VIEN 01 bỏ: dấu gạch trong mã model trích ra thành gạch mềm, tìm chữ không thấy.)
Số trên trang = báo giá: Qmax 80 m³/h, Hmax 25 m, 5,5 kW, 3 pha 50 Hz, Đài Loan. Ghi theo quy tắc: 380–415 V (báo giá ghi 380 V).
SUY RA từ tên model (chờ anh xác nhận): DN80, điểm định mức 40 m³/h @ 15 m. 7,5 HP = cách quy đổi giống FC inox.
CHƯA CÓ: bảng Q–H (không vẽ đường cong), vật liệu inox 304/316, cỡ hạt rác, tốc độ, dài cáp, nhiệt độ chất lỏng, độ sâu ngập.
Kiểm: số trên trang khớp báo giá (script đếm chữ: ĐẠT); hình thức nhìn PNG 110/250 dpi: ĐẠT; đường cong: CHƯA THỂ XÁC MINH (không có); bản in: chưa kiểm; kiểm độc lập AI khác: chưa (việc 1 trang, rủi ro thấp).
Trạng thái: chờ anh duyệt + dữ liệu. Chưa chép vào CATALOGUE DA DUYET.

## UNG VIEN 02 — 13/10/2026 09:40 (theo quy tắc mới anh chốt 09:26: mặc định có đường đặc tính + ảnh tách nền)
SHA b98d9982d9c87b85…; mã build_wqx_02.py. Ảnh đại diện: ANH DAI DIEN 80WQX40-15-5.5 (tach nen).png — tách nền tự động (rembg isnet) + mặt nạ tay bỏ túi giấy tờ, cuộn cáp, mép thùng gỗ; giữ mặt bích nối kèm theo (bỏ sẽ thủng chân bơm). Không sinh thêm chi tiết.
Đường Q–H: qua 3 điểm khóa (0;25) (40;15) (80;1), đa thức bậc 3 cong đều (độ dốc −0,232→−0,431, không đổi chiều cong, Q tăng H giảm). Bảng 0/20/40/60/80 → 25/20/15/9/1; lệch đo lại trên PDF: 0 / 1,3% / 0 / 2,9% / 0 (≤5%: ĐẠT).
SUY RA cần anh xác nhận: H=1 m tại Qmax 80 (theo quy ước FC inox Perotac: lưu lượng tối đa ở cuối đường, cột áp ~1 m); 40/15 và DN80 theo tên model.

## UNG VIEN 03 — 13/10/2026 ~10:05 (ảnh đại diện v2 theo quyết định 09:38)
SHA 0c1a265f8c522d8a…; mã build_wqx_03.py; ảnh: ANH DAI DIEN ... (v2 nen trong suot).png / (v2 nen trang).jpg; mã ảnh hero.py + final.py (ngoài kho, phiên đám mây).
Cách làm: tách nền AI (rembg isnet) + mặt nạ tay; VẼ LẠI dây cáp nguồn phía trên (cùng đường đi) vì cáp thật lẫn với túi giấy tờ; giữ bulong/tai móc từ ảnh thật; tẩy ánh xanh của túi bằng chuyển xám (không cắt); giữ mặt bích rời (vật thật trong ảnh mẫu); bóng mềm dưới chân.
Kiểm độc lập (AI Sonnet so ảnh gốc–ảnh cắt): không lẹm — ĐẠT; 6 lỗi nhỏ đã sửa, xem lại vùng phóng to: hết.
Ảnh trong PDF nằm gọn (75,101)-(257,399) trong ô (40,96)-(292,404): không bị cắt.
