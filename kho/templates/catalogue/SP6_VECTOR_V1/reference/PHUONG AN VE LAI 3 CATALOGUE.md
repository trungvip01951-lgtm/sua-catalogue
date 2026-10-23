# Phương án nghiên cứu dựng lại SP / SL / SA

Ngày 06/10/2026. Phạm vi: nghiên cứu phương án cho đúng ba PDF anh vừa chỉ định; cho phép đề xuất bố cục khác nhẹ, hình đẹp và rõ. Chưa tạo PDF catalogue mới, chưa thay bản chính. Quyết định bố cục mới trong ba tệp này được xét theo lời giao mới; không mở rộng sang 22 tệp khác.

## Kết luận đề xuất

Dựng một bộ dữ liệu có nguồn cho từng catalogue, một bộ dựng trang chung, bốn dạng trang và ba cấu hình trình bày. Chữ, bảng, khung, trục, đồ thị và bản vẽ kích thước dựng bằng vector; ảnh sản phẩm dùng tài sản rõ đúng model. Làm ba trang thử trước, sau đó chạy hàng loạt và kiểm toàn bộ 34 trang. Phương án này được đánh giá phù hợp nhất để giảm số lượt AI xử lý lặp; chưa có đo thời gian/token của một bản dựng hoàn chỉnh để cam kết phần trăm tiết kiệm.

## Đã đọc từ tệp thật

| Bộ | Số trang | Dung lượng hiện tại | Nhận xét |
|---|---:|---:|---|
| Perotac SP | 12 | 4,36 MB | Ảnh nền trang khoảng 150 ppi, có các đường vector và vùng sửa cục bộ; chỉ 17 ký tự trích xuất được |
| Redpump SL | 11 | 3,79 MB | Ảnh nền trang khoảng 150 ppi, nhiều phần đã sửa; không trích được văn bản bằng lớp chữ PDF |
| Perotac SA | 11 | 7,52 MB | Ảnh trang khoảng 150 ppi; không trích được văn bản bằng lớp chữ PDF |

Tổng 34 trang, 15,67 MB (đơn vị MB thập phân, số làm tròn). Cả ba bản đính kèm trùng byte với bản chính hiện hành. Không suy từ dung lượng rằng tệp lớn nét hơn. Một số vùng của SP/SL có mật độ điểm ảnh 600 ppi nhưng có thể là vùng dựng/phóng từ nguồn cũ; đó không phải bằng chứng chi tiết sản phẩm tăng. Đã xem tổng quan đủ 34 trang và mở riêng các trang đầu. Đây là kiểm cấu trúc/hình thức để nghiên cứu, chưa kiểm lại toàn bộ ô số của 34 trang.

SL ở tệp thực tế mang logo Redpump. SA có cả các dải 2SS/2.5SS/3SS bên cạnh SA. Phải giữ đúng thương hiệu và từng tên model nhìn thấy; không đổi tất cả thành SA/Perotac dựa vào tên thư mục hay báo cáo lịch sử.

## So sánh cách làm

| Cách | Công ban đầu | Công lặp và token | Chất lượng phù hợp |
|---|---|---|---|
| Vá tiếp từng chữ trên nền ảnh cũ | Ít nếu chỉ một lỗi | Cao với nhiều lỗi, dễ phải xem đi xem lại | Không giải quyết hết độ mờ của toàn bộ 34 trang |
| Cho AI sinh ảnh toàn trang | Có mẫu nhanh | Phải kiểm và sửa lại chữ/số nhiều lượt | Không chọn làm bản kỹ thuật cuối |
| Dựng dữ liệu + mẫu vector dùng chung | Cần thiết lập dữ liệu và mẫu | Các trang sau chủ yếu do mã dựng, AI tập trung chỗ khó | Đề xuất chọn |

## Thiết kế khác nhau nhẹ

Giữ khổ ngang và số trang 12/11/11 làm mục tiêu ban đầu. Nếu nội dung thật không vừa ở cỡ đọc rõ thì báo trang đó trước khi đổi số trang; không âm thầm thu nhỏ chữ hoặc bỏ cột.

- SP: xanh navy, nền trắng, xám bạc; tiêu đề dạng dải ngang mảnh, ảnh bơm ở cột riêng, ưu tiên diện tích biểu đồ.
- SL: xanh đậm đi cùng điểm nhấn đỏ tương hợp logo Redpump; tiêu đề ở cạnh trái, đầu bảng gọn, chia khối thông tin rõ.
- SA: xanh lam sáng và trắng, khoảng trống nhẹ hơn; tiêu đề theo khối, bảng có dòng xen kẽ rất nhạt để dò số.

Giữ logo chuẩn và các nội dung xuất xứ/điều kiện hiện có theo hồ sơ; không tự thêm chứng nhận, xuất xứ hoặc tính năng. Các tông màu trên là đề xuất, không phải quy chuẩn thương hiệu đã có. Một họ phông dễ đọc, hai độ đậm, bộ ký tự đủ đơn vị và ngôn ngữ đang dùng. Quyền dùng phông giống/gần nhất đã có; không cài phông mới. Tên họ phông và cách nhúng/đổi thành nét phải kiểm bằng trang thử trước khi nhân rộng.

Bốn dạng trang rút từ tổng quan: (1) giới thiệu sản phẩm kèm biểu đồ/bảng, (2) hai cụm biểu đồ và bảng, (3) bản vẽ kích thước và bảng, (4) biểu đồ kết hợp kích thước. Phân loại sơ bộ: SP 4/3/2/3 trang; SL 4/3/1/3; SA 4/3/1/3. Có biến thể số khung trong một trang, không ép mọi trang vào hình giống hệt.

## Dựng ảnh cho rõ

1. Chữ, bảng, ký hiệu, đồ thị, sơ đồ kích thước: dựng vector từ dữ liệu đã xác minh. Không lấy ảnh cả trang rồi tăng độ phân giải.
2. Ảnh máy bơm: tìm ảnh gốc chưa nén đúng model trong nguồn công ty/nhà cung cấp. Tệp compressed đang có chưa chứng đủ ảnh sắc nét. Lượt này kiểm các thư mục gốc liên quan, chưa tìm thấy bộ ảnh sản phẩm rời chất lượng cao; chưa dò toàn ổ đĩa hoặc web.
3. Mục tiêu ảnh in khoảng 300 ppi tại đúng kích thước đặt. Ví dụ hình cao 120 mm cần khoảng 1.418 pixel chiều cao; ảnh 150 ppi đặt cùng cỡ chỉ khoảng 709 pixel. Phóng 709 thành 1.418 pixel không tự phục hồi chi tiết thật.
4. Có thể thiết kế nền sáng, khoảng trống và bóng nhẹ. Nếu dùng AI, chỉ cân nhắc nền/ý tưởng trình bày; mọi chỉnh ảnh sản phẩm phải xem lại cấu tạo thật. Không dùng máy bơm AI tự sáng tác làm ảnh chứng sản phẩm.
5. Khi chưa có ảnh rõ: dùng ảnh thật ở kích thước nhỏ phù hợp trong mẫu, ghi hạng mục ảnh chưa đủ chuẩn in; không nhận đã hết mờ.

## Dữ liệu và đường đặc tính

- Nạp lại các bảng/số/điểm điều khiển đã được nghiệm thu từ hồ sơ đúng SHA, giữ nguồn riêng SP/SL/SA. Tái dùng mẫu bố cục giữa SA và SL không có nghĩa chép số giữa hai bộ.
- Mỗi model có mã, điện áp, kW/HP, cỡ ống, các điểm Q-H, các khóa, số trang và căn cứ; ô trống giữ trống. Bảng và đường cùng sinh từ một bản ghi.
- Dữ liệu nguồn, số đã chốt và số đang đề xuất là ba trạng thái khác nhau. Bản đề xuất chưa được nhận không tự trở thành số để xuất bản.
- Q tăng thì H giảm; giữ min/max và điểm làm việc đã khóa; sửa trung gian nguyên trong phạm vi đã cho. Dựng trục mới đều và đúng đơn vị từ tọa độ vật lý, không chép méo của ảnh quét. Đường đã đạt dùng lại hình học vật lý/điểm điều khiển, không khớp lại tùy ý.
- Mỗi đường gắn đúng model và điện áp. Quy tắc giảm không áp cho đường hiệu suất η. Thiếu bảng η hoặc thiếu chủ đường không tự suy ra từ hình đẹp.
- SP vẫn có nhánh 6SP30 chưa xác minh chủ đường; các mẫu trang 6 bị loại giữ trạng thái bị loại. SL trang 11 có bộ 22 đường/220 số và kiểm riêng đã lưu để tận dụng, nhưng cần đúng hồ sơ ROOT nhận, không dùng nhãn PASS của bản chuẩn bị thay nghiệm thu.
- Nhận dạng chữ chỉ hỗ trợ vùng chưa có dữ liệu; phải đối chiếu với nguồn nhìn thấy. Phần khó là xác minh và ráp số đúng model, không phải thời gian máy vẽ 34 trang.

## Thực hiện nhanh và ít token

1. Một người điều phối nghiên cứu/dựng. Lưu bảng dữ liệu, quyết định, danh sách chưa rõ trên đĩa; các lượt sau chỉ nạp phần thay đổi.
2. AI giải quyết bố cục, đọc những ô chưa chắc, kiểm ảnh và ngoại lệ. Chương trình xử lý hàng loạt việc lặp: đường/bảng/đổi đơn vị/kiểm khóa/kiểm thiếu model/vẽ trang.
3. Dựng ba trang thử: SP trang 6 (đồ thị dày), SL trang 11 (biểu đồ và kích thước), SA trang 1 (ảnh, chữ và bảng). Đây là lựa chọn nghiên cứu, chưa tạo PDF. Kiểm lại trang bảng thuần đầu tiên khi sinh loại trang thứ ba.
4. Sau khi ba mẫu đạt, sinh 31 trang còn lại bằng mẫu đã chốt. AI vẫn xem đủ 34 trang cuối; chỉ phóng lớn vùng nguy cơ và vùng đổi. Kiểm dữ liệu tự động phải chạy toàn bộ.
5. Một lượt kiểm độc lập nhận dữ liệu khóa và tệp đã lưu. Không cho nhiều AI cùng đọc lại toàn lịch sử hoặc cùng viết một catalogue; không dùng mô hình suy luận cao cho các phép đo/lặp đã có chương trình.
6. Mỗi kiểu dựng tối đa hai mẫu PDF lỗi, giữ hồ sơ. Bố cục mới phải là thay đổi thực chất, không đổi tên phương pháp cũ để mở lại STOP2. Các lần render để nghiên cứu không được gọi là PDF ứng viên.

Chưa đủ căn cứ đưa số token/giờ cố định. Phải đo ba trang thử rồi mới dự báo: T tổng = T dữ liệu và xử lý thiếu + T làm mẫu + 31 × T sinh/kiểm trung bình + T xử lý ngoại lệ. Token tổng = token thiết kế/dữ liệu chưa rõ + token kiểm mẫu/toàn trang + token sửa ngoại lệ. Việc vẽ bằng chương trình không cần một lượt AI riêng cho từng trang, nhưng kiểm nhận vẫn cần công. Không hứa giảm một tỷ lệ token cụ thể trước đo.

## Công cụ, bảo toàn và nghiệm thu

Theo quy định hiện tại, chỉ catfix ghi PDF catalogue. Đã kiểm mã Editor hỗ trợ thay/chèn lệnh nội dung và lưu ứng viên; chưa kiểm khả thi đầy đủ của một bộ dựng trang mới và bộ phông trên PDF thật. Khâu này phải được chứng ở mẫu đầu, không đổi sang chương trình xuất PDF khác âm thầm. Không cài thêm hoặc sửa catfix. Trước tác vụ sửa sau gián đoạn phải chạy lại BƯỚC 0 gồm 43 kiểm thử và nhận đúng khóa ghi.

Mẫu thiết kế mới lưu thành phiên bản riêng. Các vùng bố cục được thiết kế lại sẽ đổi vị trí/màu có chủ đích; nghiệm thu bằng bảng kê nội dung và thông số, hình thức mới, bảo toàn tài nguyên và các phần ngoài phạm vi. Không gọi việc đổi toàn bố cục là đạt kiểm nguyên pixel toàn trang; không nới ngưỡng cũ để sửa một ứng viên cũ cho đạt. Khổ, số trang, ảnh/phông gốc và metadata/liên kết/mục lục được giữ theo phạm vi kỹ thuật có thể kiểm; mọi khác biệt phải được ghi, quyền đổi bố cục không tự cho xóa thông tin hay đổi số.

Tiêu chí mẫu: số và model đúng 100% trong phạm vi đã xác minh; không sót nội dung; Q-H đúng khóa; đường mượt, đồng bộ nét/màu; chữ không chồng; ảnh đúng sản phẩm và đủ độ rõ ở cỡ in; kiểm PDF đã lưu tại kích thước đọc bình thường và phóng lớn. Chỉ nhận bản chính sau đúng quy trình sao lưu, kiểm độc lập và đọc lại. Hồ sơ đủ tám cột.

## Nguồn kỹ thuật tham khảo

- Adobe, độ phân giải ảnh in và quan hệ kích thước/pixel: https://helpx.adobe.com/photoshop/desktop/crop-resize-transform/resize-adjust-resolution/change-print-dimensions-and-resolution.html
- OpenAI, giới hạn vị trí/chất lượng chữ và bố cục của mô hình sinh ảnh: https://developers.openai.com/api/docs/guides/image-generation

Tệp bằng chứng: 01 FILE AUDIT READONLY.json; 02 VERIFIED SUMMARY.json; các ảnh tổng quan là bản render để nghiên cứu. Bản xem hướng bố cục HTML dùng khối minh họa, không có đồ thị/số kỹ thuật giả và không được dùng để chọn bơm.
