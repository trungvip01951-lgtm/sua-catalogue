# BÁO CÁO G14 BỔ SUNG – đơn vị công suất đứng

**G14 vẫn CHƯA XONG: 7/8 việc ĐẠT.** Đã sửa thêm đủ 4 `kw` đứng ở hai đầu bảng trang 2 thành `kW` (kilowatt, đơn vị công suất). Bốn `(kw)` kiểu nghiêng tại trang 1 vẫn CHƯA THỂ do thiếu W đúng kiểu trong chính tệp.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 128 bổ sung | Perotac + Redpump | 2, hai đầu bảng mỗi tệp | kw | kW | Chép W đứng thật từ kW trong chính tệp, chỉnh đều kích cỡ theo mẫu k tại đầu bảng bằng catfix | ĐẠT 4/4 vị trí | G14/KW BO SUNG/* SO SANH.png; G14/NGHIEM THU BO SUNG KW.json |

Nghiệm thu bổ sung: 4/4 vị trí đọc đúng kW và đúng chữ hoa. Kiểm ngoài vùng ở 150 điểm ảnh/inch, ngưỡng màu 12/255, cỡ nhỏ nhất 1 điểm in, biên 0,4 điểm in: rỗng. Ảnh nguồn, mặt nạ, toàn bộ các mảnh sửa trước, siêu dữ liệu, liên kết và dấu trang đều giữ nguyên byte/nội dung/vị trí. Bản cuối hiển thị trùng mẫu mới từng điểm ảnh; nguồn không đổi.

Bản trước do phiên này tạo đã giữ tại G14/PHIEN TRUOC KW sau kiểm đường dẫn và SHA-256 (mã kiểm nội dung). Báo cáo cũ giữ nguyên làm lịch sử; bản mới nhất là các tệp dưới đây.

Tệp hiện hành:

- C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Trục ngang\bơm trục ngang perotac model CM (bản mới).pdf; SHA-256: 8c39f96488f7a1e4524605080b6b4511b57dd29f44d3269babf3528fdd335a8c
- C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Trục ngang\bơm trục ngang redpump model CM_300dpi_75% (bản mới).pdf; SHA-256: e968a794b348b5924dd7300ac873ba1aff73c0527d64a233d6b2ee217a1b2bdc

Giữ các kết quả nghiệm thu 7/8 việc và #162 từ báo cáo G14 trước. Hai tệp không có biểu đồ đường đặc tính trong 2 trang được giao.
Cần anh quyết: chưa có quyết định mới; chỗ thiếu W nghiêng đang CHƯA THỂ.
Phát hiện thêm: 4 kw đứng đã xử lý trong lượt bổ sung này.

Giải thích kỹ thuật: catfix là bộ công cụ sửa được giao; copy_box là chép vùng ảnh; XML là định dạng đánh dấu dùng lưu thông tin tệp; OCR là nhận chữ từ ảnh; Rated power là công suất danh định; CM also available nghĩa là “CM cũng có...” (câu bị bỏ dở).
