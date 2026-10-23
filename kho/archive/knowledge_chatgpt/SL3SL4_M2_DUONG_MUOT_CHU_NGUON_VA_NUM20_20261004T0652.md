# SL3SL4: đường mượt, chữ nguồn và kiểm số sau khi lưu

Phạm vi ghi chú: Redpump SL, riêng biểu đồ **3SL4 trang 3**, 7 mẫu bơm và 70 cặp lưu lượng/cột áp. Bảng số giữ nguyên. Tại thời điểm ghi, mẫu PDF M2 đã lưu trong báo cáo và đang chờ nghiệm thu độc lập sau lưu; **chưa đưa vào bản chính, chưa hoàn thành toàn catalogue SL**.

## Cách dùng lại

1. Đọc BƯỚC 0, hướng dẫn chung, sổ tiến độ và trạng thái thật. Kiểm mã SHA-256, tức mã kiểm nội dung, của nguồn/bản hiện hành. Giữ khóa đúng catalogue, dùng bản hiện hành đã được giao làm nền; không lấy toàn tệp mẫu cũ thay cho nền hiện hành.
2. Khóa từng mã bơm với đúng nhánh từ nhãn/đường nguồn. Không gán theo thứ tự hoặc cột áp cao thấp. Hậu tố /6 của 3SL4 mờ: nhánh được xác định bằng hai điểm nguồn Q=3 và Q=4,8 m³/h rồi loại sáu hàng khác; hình dạng chữ mờ được ghi riêng. ROOT chốt danh tính tại phiếu `448b2ecc…`, không coi việc này là nghiệm thu toàn đường.
3. Giữ đầu và cuối đường theo bảng. Kiểm toàn miền lưu lượng tăng thì cột áp giảm, cùng đủ các mốc bảng theo mục 6(b): sai số tối đa `max(1 m; 2% cột áp bảng)`. Đây là dung sai biểu đồ đã có trong hướng dẫn. Không tự thêm điều kiện mọi giá trị đường phải làm tròn ra đúng số nguyên cũ; không biến số nguyên bằng nhau thành lỗi tự động.
4. Ưu tiên đường Bézier bậc ba đơn, là đường cong liên tục điều khiển bằng bốn điểm, khi đủ mốc trong dung sai. Nếu cần nhiều đoạn, chọn nối C2, tức vị trí, độ dốc và độ cong đều liên tục. M2 dùng sáu đường bậc ba đơn; /24 dùng ba đoạn C2. Sau chia nét đứt/liền tại Q=1,2 m³/h: 14 nét, 16 đoạn cong. Phân số chính xác giữ đầu/cuối và đủ 70 mốc; đạo hàm không dương và không có đoạn phẳng.
5. Kết quả không đạt trong một lớp điểm điều khiển đơn điệu chưa chứng minh mọi đường bậc ba đều bất khả thi. Ghi riêng giới hạn lớp đã thử. Phương án cuối phải được chứng bằng phân số; kết quả tối ưu gần đúng chỉ giúp chọn phương án.
6. Với chữ nằm trong ảnh JPEG, tức ảnh nén, giữ nguyên vùng chữ nguồn đủ cả nét và lỗ chữ, không đổi kích thước. /6 mới chỉ thay ký tự cuối bằng số 6 sạch từ /16 **trong cùng biểu đồ**: ảnh nguyên 8×12 điểm ảnh, dịch vị trí; giữ nguyên phần đầu và dấu gạch chéo.
7. Dọn nét ảnh cũ bằng dấu vết màu/xám nguồn thực và dữ liệu nền/lưới từ chính biểu đồ. M1 chỉ dọn quầng hai điểm ảnh nên còn dải mực JPEG cũ. M2 khóa 61.577 điểm ảnh riêng theo bảy nhánh đã đọc, có vùng loại trừ chữ, tiêu đề và trục. Bán kính vùng tìm quầng 16 điểm ảnh là lựa chọn xử lý ảnh, **không phải ngưỡng nghiệm thu của anh**. Mặt nạ chuẩn bị chưa chứng minh đã sạch; phải xem ảnh mẫu thực. Giữ bút 0,95 điểm in, không tăng độ dày để che nét cũ.
8. Chữ và nền màu dùng đúng không gian màu của ảnh nguồn, kể cả ICC, tức hồ sơ quản lý màu. Không tự thay thành màu RGB mặc định. Giữ nguyên ảnh lớn gốc, dữ liệu nén, lệnh đặt ảnh và ma trận đặt ảnh. Chỉ thêm ảnh RGB nhỏ với SMask, tức mặt nạ độ trong suốt, tại đúng vị trí nguồn.
9. Lệnh vẽ số dùng Num20, tức số tọa độ ghi 20 chữ số thập phân, rồi **đọc lại lệnh thực**. Tại một nút chung, làm tròn cực nhỏ có thể đưa Q sang đoạn kề bên. Reader22 chọn đoạn theo kế hoạch nên thất bại tại nút; giữ lỗi đó. Reader23 chọn miền từ các lệnh thật và giải tọa độ x bằng 80 lần chia đôi phân số, kiểm đủ 70 mốc; không sửa lại mẫu để làm chương trình kiểm qua.
10. Chỉ sau nghiệm thu mẫu mới lưu đúng một PDF qua CATFIX. M2 dùng bản hiện hành `ddb0bc…`, cập nhật **Contents Ref 57 đang có**, tức đối tượng chứa lệnh trang 3, bằng `set_stream`; thêm mặt nạ trước ảnh RGB từ bốn luồng dữ liệu thực đã khóa. Không vẽ lại lần nữa khi lưu. Giữ mọi tài nguyên cũ trong bộ nhớ và kiểm lại sau lưu. CATFIX dùng pikepdf có thể đổi số đối tượng; nếu xảy ra phải giữ kiểm nghiêm ngặt không đạt và chứng ánh xạ một-một, nội dung, bộ lọc nén và các tham chiếu dùng chung. Không tự tuyên bố số đối tượng giữ nguyên.

## Bằng chứng và chương trình

- Toán M2: `G04/SL3SL4 M2 SIXSINGLE ONEC2 FRACTION70 PURE NO RAM 20261004T062151Z-7e342f`, phiếu `615cda962c…`.
- Kế hoạch M2: `G04/SL3SL4 M2 SIXCUBIC ONEC2 SOURCEHALO PREPARED 20261004T063347Z-d8dcf3`, phiếu `bfe98fdcad…`.
- Mẫu trong bộ nhớ thực: `G04/SL3SL4 ONE CATFIX RAM M2 NO PDF 20261004T063815Z-196c0f`, phiếu `319feb5846…`, lệnh trang 3 `5929f9fdef…`.
- Nghiệm thu độc lập mẫu: `G04/G03 SL3SL4 M2 INDEPENDENT14 CUBIC16 SOURCE70 DIRECT5 20261004T064506Z-80fa98`, phiếu `6a60edc353…`: 14 nét, 16 đoạn, 70 mốc và 5 ảnh đạt riêng.
- PDF mẫu đã lưu: `G04/SL3SL4 M2 ONE CATFIX SAVED CANDIDATE 20261004T065005Z-518418/Redpump gieng SL_compressed (bản mới).pdf`, SHA-256 `637c6329ebec45a1b7c7271d3789678d1f711ff911099c9eea7c033eb1b5824c`; phiếu tự đọc sau lưu `bab0265893…`, chưa thay cho nghiệm thu độc lập.
- Mã tại thư mục làm việc `C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a`: `next_work_sl3sl4_M2_cubic6_C2one_fraction_math18.py`, `next_work_sl3sl4_M2_source_RGB_halo19.py`, `next_work_sl3sl4_catfix_M2_ram_builder20.py`, `next_work_sl3sl4_one_CATFIX_M2_RAM_caller21.py`, `next_work_sl3sl4_M2_actual_literal70_read23_actual_xroot.py`, `next_work_sl3sl4_M2_existing_Content_CATFIX_candidate24.py`.

Các đường dẫn G04 ở trên thuộc `C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\`.

Giữ riêng các kiểm chưa đạt: M1 bị vai gãy /9 và quầng nét cũ; kiểm tuyệt đối độ tương phản 20 và điều kiện màu /16 là phương pháp cũ không đạt. M2 trục trái có 535/2.591 điểm ảnh khác nguồn ở độ phân giải 200/600 điểm/in, mức khác lớn nhất 115/120; ảnh trực tiếp trục vẫn liền. Không nâng kiểm điểm ảnh khung thành đạt và không tự áp nó thành điều kiện mới ngoài yêu cầu anh. Bảng 70 số, hình hiệu suất, tiêu đề và ngoài toàn biểu đồ giữ nguyên; 10 trang khác giữ lệnh nguyên.

Mẫu này không phải số liệu thử bơm của nhà sản xuất, không bổ sung điểm làm việc chưa có dữ liệu và không nghiệm thu toàn SL/G04. Mọi lần làm tiếp phải kiểm trạng thái mới và khóa lại phạm vi trước khi chạy chương trình.
