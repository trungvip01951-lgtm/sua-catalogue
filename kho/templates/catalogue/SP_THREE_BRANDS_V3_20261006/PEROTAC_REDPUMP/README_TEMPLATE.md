# Mẫu thiết kế riêng PEROTAC và REDPUMP SP

## Trạng thái và nơi dùng

Hai bộ plan đã được ROOT dùng để tạo REVIEW 02. Trạng thái nhận bản chính do ROOT ghi riêng. Không chạy lại toàn catalogue chỉ vì một thông số thay đổi; dùng JSON và mẫu trang liên quan để làm delta, kiểm đầu vào và khóa trước ghi.

Nguồn số đóng băng: `work/sp_three_brands/audit/perotac_dataset_approved_v2.json`. Curve Q/H mới: `curves/PR_RP_CONCAVE_220.json`, 220 model, 2218 H không đổi, 167 đường được chỉnh hình dạng, 53 đường giữ controls.

## Bộ thiết kế dùng lại

- `design/PEROTAC-design-plan.json`, `design/REDPUMP-design-plan.json`: toàn bộ chữ, bảng, controls tọa độ trang, ảnh, PDF ops đã chuẩn bị.
- `design/resource_map_ready.json`: SHA input/plan, ánh xạ `/SPBody`, `/SPBold`, CID đã kiểm, XObject và target từng trang.
- `geometry/new_concave_label_plan.json`: 220 nhãn theo bộ curve mới. Tọa độ PEROTAC; REDPUMP dịch nguyên khối ±404 pt.
- `geometry/leader_ownership.json`: 9 leader nối đúng đầu/cuối đường riêng, không chạm đường khác/chữ/leader khác.
- `design_preview.py`: chỉ sinh SVG/PNG/JSON, không có save PDF. `--save` bị khóa. ROOT ghi PDF qua catfix sau kiểm khóa và SHA.
- `review01evidence`: snapshot trước sửa header/clip, giữ để tránh lặp lỗi.

## Quyết định thiết kế

PEROTAC: đầu trang bên trái trắng rộng 136 pt, vùng còn lại xanh lam nhạt, chữ navy, bảng xanh sáng. REDPUMP: đầu trang đỏ trầm, vùng logo trắng bên phải, bảng tiêu đề charcoal/chữ trắng. REDPUMP đảo vị trí nguyên khối trái/phải; trang kích thước 4SP chuyển hình đo sang phải.

Toàn bộ trang vẫn 13, khổ 831.56 × 595 pt. Giữ nguồn ảnh và dữ liệu đã đạt. Các đường Q/H cùng hãng cùng màu, nét liền 0.75 pt; η 0.65 pt. Các leader 0.45 pt là nét chỉ model, không phải đường đặc tính.

## Lỗi và cách tránh

1. Không dùng nhãn cũ sau khi đổi controls: phải kiểm chữ thật với toàn bộ đường và kiểm nhận diện model. Các lần nhét nhãn vào cùng khe nhìn như chung đường đã đóng; không tiếp tục lặp chỉ vì phép đo giao nhau đạt.
2. 6SP30-4, 6SP36-6/-7 dùng leader ngắn tại cuối đường. Không trả về cách để hai tên nối tiếp trong một khe. Nhãn ≥5.4 pt.
3. Khi dịch panel, phải dịch cả clip η. `clipx = px + p.dx`; path, trục và clip phải cùng hệ tọa độ. Bản02 đã đo đủ15viewport mỗi hãng trên PDF thật.
4. Không tạo ô trắng nhỏ bao logo trên nền màu. Thiết kế vùng logo trắng thành một vùng đầu trang hoàn chỉnh.
5. Không lấy snapshot12trang làm nền ghi mới. ROOT mở PDF accepted13trang hiện hành; snapshot12 chỉ truy ảnh gốc đúng hash. Giữ resources/document info/page boxes và không chèn thêm trang.
6. Sau sửa bộ curve, gắn đúng SHA trong geometry; nếu controls thay, geometry cũ không tự còn hiệu lực.

## Kiểm sau xuất

`independent_numbers/BAO_CAO_8_COT_REVIEW02.md` và các JSON kiểm đủ số trên tệp thật. `check_actual_eta.py` đọc raw cubic cùng active clipping để chứng minh đường hiệu suất hiện trong viewport. Q/H curve fit và hình thức 26 trang có báo cáo độc lập của tác nhân khác do ROOT tiếp nhận; không thay bằng trạng thái của plan.
