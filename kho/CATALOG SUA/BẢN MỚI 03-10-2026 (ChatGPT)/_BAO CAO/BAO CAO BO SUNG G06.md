# BÁO CÁO BỔ SUNG G06 – nghiệm thu lại bảng trang 4

**Kết quả hiện tại: 1/3 ĐẠT; #52 và #53 CHƯA ĐẠT. File ra vẫn là bản đã nghiệm thu #51 trước đó.**

| Việc | Trang | Nội dung | Kết quả | Bằng chứng |
|---|---|---|---|---|
| #51 | 1 | Ví dụ model FS-35-7-2.2 đã đạt; giữ nguyên | ĐẠT | G06/acceptance-v2.json; mã file hiện tại khớp |
| #52 | 2–3 | (KW) chưa đổi được thành (kW) đúng nét đậm | CHƯA ĐẠT | Không có phông nhúng; chưa có k cùng kiểu |
| #53 | 4 | Chỉnh năm dòng bằng nguyên từ nguồn; mẫu cuối còn mực C sát lưới nên không dùng | CHƯA ĐẠT | Ảnh mép ô 1200 điểm ảnh/inch và dữ liệu nguồn mực |

**#136 giữ nguyên:** hai catalogue FS là hai dòng bơm khác nhau; không ghi file G07.

## Các phương pháp và giới hạn

Cách ghép từng ký tự đã thất bại hai mẫu trước lượt bổ sung và đã dừng. Lượt này thử hai phương pháp khác, mỗi phương pháp tối đa hai mẫu:

1. Chép nguyên từ nhưng xoá theo vùng ảnh dựng: bố cục gọn, nền sạch nhưng mặt nạ chạm mép mờ của đường ngang. Hai mẫu word-copy-mau-1/2.pdf không dùng.
2. Chép nguyên từ theo tọa độ ảnh gốc, chỉ xoá mực/quầng của từng từ: mẫu đầu bảo vệ lưới quá rộng nên giữ mẩu C/d; mẫu hai thu vùng bảo vệ theo nét ngang/dọc thật. Lưới, số thứ tự và 29 từ mới đạt phép kiểm, nhưng cạnh C cũ ở dòng 5 vẫn còn. Hai mẫu native-word-mau-1/2.pdf không dùng.

Không tạo mẫu thứ ba bằng cùng cách và không ghi các mẫu thử vào bản đích.

## Đối chứng mực C còn sót

Các điểm chưa sạch dòng 5 ở ảnh 600 điểm ảnh/inch nằm x=311,34 điểm, y≈623,82–624,42 điểm. Chúng ánh xạ vào cột 1297, hàng 906–908 của ảnh gốc; nằm trong miếng từ Cruss dùng làm nguồn chép, ngoài mặt nạ lưới gốc. Mực có độ che 0,184–0,431; mức xám nguồn 208–145. Vùng bảo vệ vách đã giữ nguyên các điểm đó. Ảnh phóng 1200 cho thấy đoạn xám ngắn đúng cao độ C cũ. Chưa đủ căn cứ gọi toàn bộ đoạn này là mép lưới, nên không nghiệm thu đạt.

Các điểm dòng 13 và điểm góc dòng 18 chủ yếu nằm sát mép lưới; kết quả thô được giữ để người kiểm đối chiếu. Không bỏ điểm nghi ngờ chỉ theo màu hoặc chỉ vì nằm gần lưới.

## Phần đo được của bản thử cuối

- Lưới cả hai bảng, kể cả mép khử răng cưa, và số thứ tự giống bản trước từng điểm ảnh ở 400/500/600 điểm ảnh/inch.
- Đọc lại 29 từ từ luồng ảnh và mặt nạ trong PDF đã lưu: mọi giá trị mực khớp nét nguồn sau phép co/phóng đồng tỷ lệ. Có tọa độ và mã kiểm tra từng miếng nguồn. Không ghép từng ký tự, không dùng phông ngoài.
- Mẫu chữ M ở dòng Motor có chiều cao 23 điểm ảnh ở độ phân giải ảnh gốc. Các hệ số dòng 5/13/15/18/28 lần lượt: 1,27778; 1,15; 0,95833; 1; 1,04545. Dòng 18 giữ chiều cao vốn đã 23 điểm ảnh, chỉ ngắt dòng/căn lại trong mẫu.
- Dòng 5/13 ngắt sau head; dòng 15/18 ngắt sau head; dòng 28 một dòng và căn trong ô. Giữ nguyên mọi cách viết của nguồn, kể cả Cruss và assemblie.
- Sai khác ngoài năm ô ở 200 điểm ảnh/inch bằng rỗng, ngưỡng màu 0, không bỏ điểm ảnh nhỏ. Ảnh gốc không nén lại; chỉ thêm năm miếng nhỏ với mặt nạ trong suốt. Những điều đạt riêng này không làm #53 trở thành ĐẠT khi còn mực chữ cũ.

## Bản đích hiện tại

- Nguồn: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 01-10-2026\Nước thải\Aquaris FS_300dpi_75% (bản mới).pdf
- File ra: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Nước thải\Aquaris FS_300dpi_75% (bản mới).pdf
- Mã SHA256 nguồn: a297ed5b1dec97c33b6d2327d25d30bd3f317690548b9d5895c59e1376a63b31
- Mã SHA256 file ra: 97db44101b00605e71ce8996e8d4d08d672a8475cdcfa51ae1b1d5aa9597e033
- Mã file ra khớp bản final-state-v2.json đã đạt #51. Trang 2–4 giữ nguyên luồng nội dung nguồn; cấu trúc PDF đạt. Không cập nhật PDF, không xóa/đổi tên/ghi đè file nguồn.

## Hồ sơ kiểm chéo

- G06/review/word-copy-build-1/2.json và word-copy-grid-diagnostic.json: cách dùng vùng dựng ảnh và lỗi mép lưới.
- G06/review/native-word-build-1/2.json: cách ảnh gốc, tọa độ 29 từ và mặt nạ.
- G06/review/native-word-acceptance-stage-2.json: kiểm thô lưới, số thứ tự, ảnh, thông tin, liên kết, đọc chữ và nền; kết quả tổng chưa đạt.
- G06/review/native-word-verification-stage-2.json: đọc lại mực từng từ từ PDF; kết quả tổng chưa đạt, không dùng phép loại mép để chốt.
- G06/review/native-word-edge-point-coordinates.json và native-word-edge-original-ink.json: tọa độ điểm nghi ngờ, đối chiếu đúng ảnh và mực nguồn.
- G06/review/native-word-edge-row5/row13/row28-1200dpi.png: trước/sau tại mép ô; các ảnh marked đánh dấu điểm nghi ngờ.
- G06/review/native-word-mau-2-400dpi/500dpi/600dpi.png, native-word-toan-bang-2.png, native-word-nguyen-tu-chung-cu-2.png: ảnh mẫu và đối chứng nguyên từ.
- So sanh bo sung G06.png: nguồn và bản đích hiện tại; bảng cuối giữ nguyên.

SHA256 là mã kiểm tra nội dung file; PDF là định dạng tài liệu; kW là kilôoát, đơn vị công suất; điểm là đơn vị bố cục bằng 1/72 inch; độ che mực 0 là trong suốt, 1 là đen kín. Motor nghĩa là động cơ, head nghĩa là đầu. Các từ nguyên gốc còn lại trong hình được giữ theo yêu cầu #53.

Tiến độ: G06 CHƯA XONG – 1/3 ĐẠT. Phần thử bổ sung #53 đã dừng theo quy tắc hai mẫu; cần phương pháp khác có thể xóa mực sát lưới mà chứng minh giữ lưới trước khi coi hoàn thành.

Lập: 2026-10-03T05:23:22.316184

## Đính chính kết luận hiện hành53 ngày05/10/2026

Các mẫu chỉnh chữ ở trên vẫn CHƯA ĐẠT. Theo điều kiện gốc, phương án giữ nguyên53 được chốt ĐẠT riêng;G06=2/3 xử lý gồm51 sửa và53 giữ,52 còn. Không nhận bảng đồngcỡ/làm nét đã xong. ROOT và kiểm độc lập mở bản thật97db,ảnh/nội dungP4 giữ và0đổi điểmảnh. Báo cáo mới: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G06\ROOT53 CONDITIONAL KEEP REAL P4 READONLY 20261005T160135Z-1d63bb\03 BAO CAO8 COT KEEP53 VA GIOI HAN.md
