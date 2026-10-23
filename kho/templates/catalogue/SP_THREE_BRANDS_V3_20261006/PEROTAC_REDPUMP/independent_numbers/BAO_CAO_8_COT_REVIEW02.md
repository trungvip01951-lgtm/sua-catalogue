# PEROTAC / REDPUMP SP — kiểm số độc lập trên PDF REVIEW 02

**ĐẠT phạm vi số bảng, pha, kích thước, tiêu đề và đường hiệu suất η.** Không thay cho báo cáo Q/H curve fit hoặc nghiệm thu hình thức toàn trang của người kiểm khác.

- PEROTAC: `07c0ca71af6a323b4fb142bc77d3e11685f521d79eed5a95c29bdf4c5e1da98a`.
- REDPUMP: `2face7a1b50125c174b361877ea27e6dd01d4b4cf956faaeccb1b76b0f461ca6`.
- Thư mục PDF: `deliverables/SP BA HANG THIET KE RIENG 20261006`.

| STT | Phạm vi | Nguồn kỳ vọng | Kiểm trên PDF thật | Kết quả | Sai lệch | Bằng chứng | Giới hạn/bước tiếp |
|---|---|---|---|---|---|---|---|
| 1 | Model, kW, HP | perotac_dataset_approved_v2.json; bản 13 trang đã nhận | 220 dòng mỗi hãng, đọc từng ô và model pha | ĐẠT cả hai | 0 | PEROTAC/review02/actual_numbers.json; REDPUMP/review02/actual_numbers.json | Không dùng writer import hoặc plan làm kỳ vọng |
| 2 | Cột áp H | Bảng đã chốt; gồm 4SP14-4 H24/23 và #133 H103/72 | 2218 ô mỗi hãng | ĐẠT cả hai | 0 | performance_rows | Kiểm số bảng; đường cong do source-audit kiểm riêng |
| 3 | Q và đơn vị | Q nguồn, quy đổi l/min đã dùng trong bản nhận | 153 Q m³/h và 153 l/min mỗi hãng | ĐẠT cả hai | 0 | headers | Giữ phần lẻ Q được phép, H nguyên |
| 4 | Điện, tên model | Bản đã chốt có 9 bổ sung model 3 pha; quy tắc 6 inch chỉ 3 pha | Các ô model pha và điện áp; mọi chữ hiển thị 13/13 trang | ĐẠT cả hai | 0 | performance_rows + actual_baseline_readback | Không tự thêm chiều dài/cân nặng cho 9 model chưa có số nguồn |
| 5 | Kích thước và cân nặng | Dimensions 4inch/6inch/8_10inch của nguồn đã kiểm | 219 dòng mỗi hãng, đủ P/M/T/DN và các cột kg có nguồn | ĐẠT cả hai | 0 | dimension_rows | 4SP2 đã loại; không tạo hàng 6SP36-28 thiếu nguồn |
| 6 | Nội dung và tiêu đề | Đọc trực tiếp PDF 13 trang đã nhận, không lấy bản dựng làm chuẩn | Tập hợp mọi chuỗi chữ từng trang sau đổi vị trí/màu | ĐẠT 13/13 trang mỗi hãng | 0 | actual_baseline_readback | Màu/bố cục do người kiểm hình thức nghiệm thu |
| 7 | Đường η và clip | Đường η thật trong PDF cũ đã nhận | Đọc raw cubic và trạng thái clip của đủ 15 đường mỗi hãng | ĐẠT 30/30 | Sai lệch controls sau bù dịch ngang = 0; đủ điểm nằm trong viewport | actual_eta_review02.json | Không suy đây là dữ liệu thử máy độc lập |
| 8 | Delta 02 | Số liệu và hình học Q/H giữ nguyên từ 01; sửa header PR và clip RP | Readback02 khớp nguồn, SHA xác nhận như trên | ĐẠT phạm vi này | 0 | review02_delta_proof.json; các báo cáo trên | Chỉ ROOT nhận bản chính sau toàn bộ QA khác đạt |

Lỗi đã phát hiện và sửa trước bản02: vùng clip η của REDPUMP chưa dịch cùng đường; PEROTAC có mảng trắng logo nhỏ trên nền xanh. Bản02 dùng vùng trắng toàn đầu trang bên trái đến x=136 pt và nền xanh phần còn lại; REDPUMP giữ vùng logo trắng bên phải. Lỗi η được xác minh bằng trạng thái đồ họa PDF, không chỉ dựa việc có path trong tài liệu.

Không ghi hoặc sửa PDF trong công việc kiểm này. Người kiểm đã từng chuẩn hóa dữ liệu nguồn và chuẩn bị SVG; ROOT là tác nhân xuất PDF. Giá trị kỳ vọng là dữ liệu đã đóng băng và bản PDF đã nhận; không import writer hoặc dùng plan để tạo số kỳ vọng.
