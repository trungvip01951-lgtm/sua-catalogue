# KHO ẢNH - catalogue đã duyệt

Kho ảnh tách từ 62 PDF trong CATALOGUE DA DUYET (AQUARIS 20, PEROTAC 21, REDPUMP 21). Tạo ngày 13/10/2026 bằng script tách ảnh. Script chỉ đọc PDF, không sửa PDF gốc.

**Cấu trúc**
- Thư mục theo nhóm sản phẩm: phần sau dấu " - " trong tên PDF, bỏ dấu, khoảng trắng đổi thành _.
- Mỗi ảnh chỉ có một tệp, tên = 12 ký tự đầu của mã sha256 + đuôi gốc. Ảnh trùng ở nhiều PDF chỉ lưu một lần.
- DANH_MUC.csv: mỗi dòng là một vị trí ảnh trên một trang. Một ảnh dùng nhiều lần thì có nhiều dòng.

**Cột DANH_MUC.csv**
- nhom, hang, tep_pdf, trang, xref: nhóm, hãng, tên PDF (thư mục hãng/tên tệp), số trang, số hiệu ảnh trong PDF.
- tep_anh: đường dẫn ảnh trong KHO_ANH.
- w_px, h_px: kích thước điểm ảnh gốc.
- rong_pt, cao_pt: kích thước ảnh khi đặt trên trang (pt; 72 pt = 1 inch).
- ppi: độ phân giải hiệu dụng = điểm ảnh chia kích thước hiển thị (inch), lấy số nhỏ hơn giữa chiều rộng và chiều cao.
- trong_suot: co = có kênh trong suốt (đã ghép thành PNG).
- so_vi_tri_tren_trang: số lần cùng ảnh xuất hiện trên trang đó.
- sha256: mã băm của dữ liệu ảnh gốc, dùng để nhận diện ảnh trùng.
- trang_thai: ĐẠT (đủ ppi); CẦN THAY KHI CÓ DỊP (ppi thấp); NỀN/TRANG TRÍ (ảnh phủ trên 60% trang); LOGO? (ảnh dưới 2% trang, sát mép trên, cần người xác nhận).
- ghi_chu: "cùng ảnh dùng ở N vị trí trên trang"; "đặt chồng" (hai vị trí trên cùng trang trùng nhau trên 80%); ghi chú lỗi xử lý ảnh nếu có.

**Ngưỡng và thứ tự xét**
- ĐẠT: ppi từ 200 trở lên. Riêng trang 1 mà ảnh chiếm trên 15% trang: từ 300 trở lên.
- Thứ tự xét: NỀN/TRANG TRÍ trước, rồi LOGO?, rồi ĐẠT hoặc CẦN THAY. Cột ppi vẫn ghi đủ để xem lại.
- Sát mép trên: mép trên ảnh cách mép trên trang không quá 10% chiều cao trang.
- Ảnh có cạnh dài dưới 64 px không đưa vào kho.

**Quy tắc**
1. Ảnh mới anh gửi và ảnh đã duyệt: lưu vào đây, mỗi ảnh một lần.
2. Catalogue sau lấy ảnh từ kho này.
3. Ảnh CẦN THAY KHI CÓ DỊP chỉ thay khi anh ra lệnh sửa đúng catalogue đó.
4. Chuẩn trình bày và ảnh: xem rules/HO_SO_HANG.json (mục "anh" trong "chung" và trong từng hãng).
