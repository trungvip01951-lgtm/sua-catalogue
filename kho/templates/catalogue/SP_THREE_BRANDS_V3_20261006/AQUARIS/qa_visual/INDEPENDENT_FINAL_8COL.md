# Kiểm độc lập AQUARIS SP REVIEW 02

Người kiểm: /root/sp_dimensions_assets. Chỉ đọc PDF và ghi bằng chứng riêng; không sửa PDF hoặc tiếp nhận bản chính.

Tệp thật: `deliverables/AQUARIS SP THIET KE MOI 20261006/AQUARIS SP - REVIEW 02.pdf`.

SHA256 tự tính: `85c9e28f779859e35c7a0bd2abe0cb5d2ff018fa7971c274c8ca5b45beaaa358`, 31 trang.

Kết luận: **PASS hình thức AQUARIS và cổng ĐƯỜNG CONG ĐỀU trên phạm vi đã kiểm**. Cổng so đủ ba thiết kế hãng **PENDING** đến khi có PEROTAC/REDPUMP mới. Kiểm toàn bộ 1179 ô H/độ lệch bảng và bảo toàn tài nguyên chi tiết do hồ sơ numeric của điều phối, không lấy kết luận đó thay kiểm riêng bên dưới.

| STT | Phạm vi | Yêu cầu | Bằng chứng | Kết quả | Sai lệch / chưa rõ | Giới hạn | Bước tiếp |
|---:|---|---|---|---|---|---|---|
| 1 | Toàn bộ 31 trang | Xem từng trang thật, không chỉ montage | `page-01.png` đến `page-31.png` của REVIEW01; `review02-page-26.png`, `review02-page-27.png`; `review02-independent-metrics.json` | PASS | Đã mở từng trang ở 140dpi. Hai trang 26/27 hết cắt/đẩy nội dung sau thu đều đúng khổ | 29 trang không đổi có pixel140dpi giống tuyệt đối, nên kế thừa kiểm bằng bằng chứng delta; 26/27 xem lại riêng | Giữ PDF đã kiểm |
| 2 | ĐƯỜNG CONG ĐỀU, 20 biểu đồ/197 đường | Cong đều toàn miền, không ngoằn ngoèo hoặc tăng H khi Q tăng | Actual path PDF trong `review02-independent-metrics.json`; xem toàn bộ biểu đồ trang3–13/15/17/19/21/23/25/27/29/31 | PASS | 197 đường; 0 path H tăng; 0 path đảo độ cong đáng kể; max lệch slope ở mối nối 9.07e-7 do tọa độ float | Đo từ path actual qua PyMuPDF, ngưỡng sai số tọa độ1e-5; kiểm sai lệch ≤5% so1179H nằm trong numericQA riêng | Không lấy C2 đơn lẻ thay tiêu chí thị giác; mẫu hiện tại đạt cả hai |
| 3 | Nét/nhãn/trục | Solid, đồng màu/độ dày trong mỗi chart; tên model đầy đủ; Q dưới chart, Total head H(m) bên trái | Actual path có dashes[]; các ảnh fullpage và header216 | PASS | Mỗi chart 1style; width0.95pt, riêngp27 thu đều0.922157pt. Không thấy chữ đè, thiếu nhãn hoặc đường khác độ rõ | Chưa dùng báo cáo này để xác nhận1179H hoặc mọi thông số điện; điều phối đang kiểm số | Tổng hợp với numericQA |
| 4 | Header/bảng | Khung rõ từng ô, tách kW/HP và2hàngQ; body không mất ô | `header216-p03.png`, p09/p15/p25/p29; 20 trang bảng đã xem | PASS | Chữ trắng/nền xanh đậm rõ, cộtP2 vàQ phân ranh; cộtHbody gộp rõ; không thấy ô bị xóa trắng vô ý | Bảng nhiều dòng chữ nhỏ hơn bảng ít dòng; đọc được ở crop216dpi | Giữ style |
| 5 | 20 intro, materials/modelcode | Giữ nội dung nguồn đúng hãng | `intro_readback_checks.json`, đối chiếu `assets/aquaris_nonqh_content.json` đã trích từ nguồn và ảnh | PASS | 402/402 đoạn chuẩn hóa khoảng trắng hiện diện;11small+9large,14hàngmaterials mỗi large; các mã ví dụ literal giữ nguyên | Đây là nội dung intro/materials, không thay kiểm length/weight trong20performance tables | Kết hợp metadata QA của tác nhân dữ liệu |
| 6 | Ảnh AQUARIS và dấu SUMOTO | Dấu cũ biến mất tại vùng chỉ định, giữ thân/gờ bơm | `photo600-p03-0.png`, p09/p14/p22; đầu6ảnhbìa `photo600-p01-*`; toàn20ảnhfamily xemfullpage | PASS vùng dấu nhìn thấy | Không còn dấu tại vị trí cũ; thân/gờ không thấy biến dạng; bìa dùng cùng nhómảnhđãlàm sạch | Nguồn chỉ67–116px ngang, vẫn mờ khi phóng600dpi; không tuyên bố ảnhHD. Kiểm ngoài patch bằng hash/clip do điều phối lưu riêng | Giữ giới hạn ảnh nguồn trong bàn giao |
| 7 | KHÁC GIAO DIỆN GIỮA CÁC HÃNG | Khác màu chủ đạo, nền header và trình bày giữa3hãng | AQUARIS hiện tại xanh đậm/portrait/bảngheaderđậm; PR/RP cũ landscape | PASS phần AQUARIS đã đổi; PENDING cả3hãng | AQUARIS khác rõ bản cũ và PR/RP cũ; không ký chung3hãng khi PR/RP mới chưa xuất hiện | Header nền trang AQUARIS trắng; cần đặt cạnh hai bản mới để kiểm đủ màu+nền+trình bày theo quy tắc mới | Chờ PDF PR/RP mới, kiểm đối chiếu thật |
| 8 | Phiên bản/bảo toàn delta | ĐúngSHA/31trang; chỉ26/27 đổi trong lần02 | `review02-independent-metrics.json` | PASS delta | SHA khớp;31/31khổtranggiữ;29trangpixelbằng;26/27thuđều, đọc chữ và ảnh lại đạt | Không tự ký toàn bộ preservation source-to-redesign khi chưa tích hợp kiểm metadata/font/link của điều phối | Điều phối tổng hợp, không tựadopt |
| 9 | Q số lẻ | Áp quyết định mới cho Q1chữsốthậpphân, H nguyên | `rules/QUY_TAC_CUNG_HIEN_HANH.md`, mục Nguồn hãng thiếu và lưu lượng số lẻ; bảng/trụcactual | PASS hiển thị | Rút cảnh báo Q(l/min) số lẻ sau đọc quyền mới; quy đổi như333.3/1666.7 phù hợp1decimal | Không đổi quy tắc Hnguyên | Giữ quyền mới |

## Audit ảnh PEROTAC / REDPUMP riêng — CHƯA THỂ XÁC MINH chữ SUMOTO

PR SHA `5c452fc9e01dded447622ebf302690ec2a347b6c114a97946f4f562e93fc48f8`; RP SHA `b067902b0ae5e41f19f0095db221942ddd231364694cedfd80edc7418dfc1b28`. Tệp actual13trang trong `deliverables/SP BA HANG 20261006`.

Ảnh đại diện tại p1/p5/p10/p12 (p5hai bơm) đã render mới600dpi vào `{PEROTAC,REDPUMP}-p{01,05,10,12}-head600.png`. Cáp đen giữa thân che vùng có thể mang dấu, ảnh gốc thấp nét; không đọc được chữ SUMOTO, cũng không đủ căn cứ tuyên bố vùng này chắc chắn sạch. Đây là **UNKNOWN**, không phải chứng minh cònlogo. Không tự xóa cáp/chi tiết bơm hoặc tạo vùng sửa theo phỏng đoán.

Phương án tiếp: nếu cần chỉnh, điều phối xác định vùng dấu có chứng cứ hoặc giữ UNKNOWN trong bàn giao. Không dùng oldPASS13trang để nói toàn bộ ba hãng đã đạt quy tắc thiết kế/cong đều mới.
