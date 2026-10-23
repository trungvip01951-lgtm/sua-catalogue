# Ảnh sản phẩm và nền

Anh cho đổi ảnh đại diện Perotac WC cả8 trang để khác Redpump và đồng bộ. Cách đã nghiệm thu giữ ảnh sản phẩm gốc Perotac, thay trình bày/nền sáng studio bằng lớp nền riêng; không dựng lại cơ khí sản phẩm.

## Cách đã chọn

1. Đọc ảnh XObject gốc, byte JPEG, SMask (mặt nạ), CTM (phép đặt ảnh), các vùng nền cần bỏ và khe thật. Dùng82 mốc nguồn khác nhau;230 lượt xuất hiện không phải230 chi tiết độc lập.
2. Dựng đường cắt hình học gồm20 vòng:8 viền ngoài và12 khe. Chọn quy tắc điền đúng; đường Wn và W* (hai quy tắc cắt PDF) không thay nhau mù. Giữ dây/chân/lỗ/cánh và cấu kiện thật.
3. Tạo nền rỗng bằng công cụ sinh ảnh AI nếu cần, không tạo ảnh bơm cơ khí thay cho ảnh hãng. Các phiên AI làm sai vật liệu/bộ phận đã bị loại. Không tự sửa sản phẩm bằng Python để làm đẹp.
4. Dựng mẫu trong bộ nhớ, tự nhìn đủ8 trang và từng ảnh ở150/600dpi. Kiểm đồng bộ8 trang, nền không che chữ/bảng/đường. Tác nhân độc lập xem cùng tệp thật sau lưu.
5. Ghi ứng viên CATFIX duy nhất sau khóa phương án; đọc lại bằng hai công cụ nếu cần. Giữ38 đường/372 mốc/114 khóa/174 ô đã nghiệm thu và11.070 chữ/43 hàng/108 ô trống.

## Giới hạn phải giữ

JPEG nguồn có quầng xanh lẫn kim loại/dây/chân; chưa phân biệt chắc nền/vật liệu thì không tự tẩy. Không nhận82 mốc là chứng đầy đủ mọi cấu tạo máy. Bản có nền khác Redpump không có nghĩa cơ khí bơm phải khác.

Các cách render (đọc ảnh từ PDF) có thể cho kết quả hơi khác dù byte ứng viên giữ nguyên. M1 ảnh Perotac thực đã được đọc/nhìn đủ8 và kiểm ngoài vùng bằng0. Tuy nhiên thử so RAM/tệp ở vài trang vẫn có pixel chênh tới2–4 mức màu; giữ chẩn đoán CHƯA ĐẠT cho tuyên bố mọi cách dựng trùng từng pixel, không xóa sau khi bản giao được nghiệm thu trong giới hạn nguồn.

PDFium tạo kích thước ảnh bằng làm tròn lên: ánh xạ đo vùng phải dùng kích thước bitmap thực/trang thực, không lấy mỗi dpi/72. Vấn đề ma trận đọc sai được sửa ở phép đo, không đổi PDF hoặc nới vùng/ngưỡng. Chi tiết trong hồ sơ G08 đã lưu.
