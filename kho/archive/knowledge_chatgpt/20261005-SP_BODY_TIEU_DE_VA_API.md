# SP: giữ mép tiêu đề và kiểm lệnh bộ công cụ — 05/10/2026

Hồ sơ này ghi kết quả đang làm, **không phải nghiệm thu toàn catalogue**. Nguồn SP `e1b94dc6…`, bản kết quả hiện hành `381fd9aa…` chưa đổi sau mẫu trong bộ nhớ.

## Cách đã có bằng chứng

- Bỏ toàn bộ nét cũ trong thân biểu đồ bằng vùng cắt của CATFIX, rồi dựng lưới tại vị trí đo từ nguồn. Không phủ ô màu, không biến cả trang thành ảnh.
- Mẫu thực `94e972bd…` có 25 đường, 183 phần chữ nguyên ảnh nguồn, 28 ô số và 54 vật liệu. Đường mượt, đồng nét; lưới một lớp; không còn chấm cũ ở cuối. ROOT và tác nhân độc lập mở đủ 16 ảnh. Đây mới là đạt hình thức của thân biểu đồ.
- Giữ thông số, 50 đầu/cuối, vị trí chữ và các vật liệu đã khóa. Khi chỉ sửa mép vùng cắt thì không tính lại đường hoặc ghép lại chữ.

## Lỗi và cách tránh

1. **Không suy lệnh có sẵn từ tên gọi.** `set_page_resources` không tồn tại trong CATFIX. Dùng `add_xobject_to_page`, kiểm tên trả về khớp đúng tên đã khóa. Trước mở trình sửa, đối chiếu từng lệnh với mã thư viện và đối tượng thực của đúng bộ đọc PDF. `API` là các lệnh lập trình do bộ công cụ cung cấp.
2. **Hai ô tiêu đề chưa giữ nguyên toàn mép.** Ở 600 điểm/inch, trang 7 thay 469 điểm ảnh (chênh lớn nhất 15), trang 11 thay 438 (chênh lớn nhất 4) trong phép cắt riêng. Kiểm từ toàn trang xác nhận 469 và 436 điểm ảnh; phần trong cách mép một điểm ảnh đổi 0. Bốn vùng trục/hiệu suất đổi 0. Không lấy phần trong đạt để gọi cả ô đạt, không hạ ngưỡng.
3. **Đừng mặc định lỗi là do cách cắt ảnh kiểm.** ROOT dựng lại đúng các byte của mẫu đã có, dùng CATFIX trong bộ nhớ, rồi đọc toàn trang ở 600 điểm/inch. Mẫu vẫn có chênh lệch mép thực; không lưu PDF và không nhận bản chính.
4. **Phương án sửa tiếp chỉ chừa hai điểm ảnh nguồn bên trái/dưới ô tiêu đề.** Hai vùng thân mới: trang 7 `[151,201,649,585]`, `[649,242,738,585]`; trang 11 `[1015,201,1493,581]`, `[1493,238,1575,581]`. Giữ vùng được phép sửa, đường, số, chữ, lưới và khung ngoài. Đã kiểm toán học khoảng cách đến 50 nét vẽ và hộp chữ/đường nối; chưa tạo mẫu thứ hai tại thời điểm ghi hồ sơ.
5. Hai mẫu của cùng cách sửa không đạt thì dừng cách đó. Giữ lỗi cũ và các kết quả kiểm, không đổi tên cách để thử vô hạn. Lỗi chuẩn bị mã trước khi tạo mẫu cần ghi riêng, không đếm thành mẫu đồ họa.

## Bằng chứng chính

- `_BAO CAO/G05/SP25 BODY SOURCE GRID FROZEN54 ONE CATFIX ACTUAL RAM NO PDF 20261004T202938Z-f0dce0/01 ACTUAL SP BODY FROZEN54 NATIVE2 SOURCE GRID16 NO PDF.json`: `94e972bdb2e3b3b233f896ca097e08362173094151883b64027e2ccafa20e33b`.
- `_BAO CAO/G05/SOL SP BODY132 ACTUAL54 VISUAL16 TITLES FAIL 20261005/01 DIRECT ACTUAL54 NATIVE2 BODY16 TITLE600 HARDZERO FAIL.json`: `45291fda6891ab21d411fb7cdcf2a528756f8407281e431ec242627996d3c4f8`.
- `_BAO CAO/G05/ROOT SP BODY FROZEN ACTUAL FULL600 TITLE DIAGNOSTIC 20261004T203618Z-8f62da/01 ROOT FIXED ACTUAL54 FULLPAGE600 TITLE PIXEL0 DIAGNOSTIC NO SAVE.json`: `53fe7e5a1adae18acdf9bf112e1b8a4ad48713050afc7efdd4d066183fd59f71`.
- `_BAO CAO/G05/ROOT SP BODY TITLE GUARD2 SINGLE DELTA STATIC 20261004T203931Z-42d321/01 ROOT SECOND BODY TITLE SOURCEPIXEL2 DESIGN NO RAM.json`: `2d0644dec4ebe36049e32830dcb06180d79d79cacd3793ffece0681f9e25a713`.
- `_BAO CAO/G05/SOL SP BODY TITLE GUARD2 FROZEN PAINT CLEARANCE STATIC 20261005/01 TITLE GUARD2 ALL50 CURVES FONT183 LEADER CLEAR STATIC NO RAM.json`: `c8afe94145b1cd0f71917ebc8a3fe70c8aaf9b7cad54bd8f6341b3487bbcc02f`.

Đường dẫn `_BAO CAO` tính từ thư mục kết quả trong `manifest.json`. Chữ nguồn khoảng 150 điểm/inch còn hạt khi phóng lớn; đường mới sắc nét không chứng minh toàn chữ/ảnh đã tăng chi tiết. Sổ 135/149 việc gốc chưa đổi; không lấy mẫu này thành hoàn tất SP hay dự án.
