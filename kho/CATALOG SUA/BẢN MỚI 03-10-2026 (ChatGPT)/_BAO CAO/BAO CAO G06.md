# BÁO CÁO NHÓM G06 – Aquaris FS (4 trang)

**Tổng: 3 việc cần sửa · ĐẠT 1 · CHƯA ĐẠT 2 · CHƯA THỂ XÁC MINH 0.**

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 51 | Aquaris FS_300dpi_75% (bản mới).pdf | 1 | FS 15 15 1.5 | FS-35-7-2.2 | Chép nét số/dấu nối cùng kiểu từ model thật đầu bảng; giữ từng nhóm số và lời giải thích | ĐẠT | So sanh G06.png; G06/acceptance-v2.json; G06/font-probe.json |
| 52 | Aquaris FS_300dpi_75% (bản mới).pdf | 2–3 | (KW) | Còn nguyên (KW); chưa sửa được (kW) đúng kiểu chữ | Không dùng chữ thường khác nét đậm của tiêu đề | CHƯA ĐẠT | G06/probe.json; G06/font-probe.json; So sanh G06.png |
| 53 | Aquaris FS_300dpi_75% (bản mới).pdf | 4 | Hàng 5, 13 nhỏ; 15, 18 lớn; 28 sát viền | Giữ nguyên bảng gốc; chưa đạt mục tiêu đồng cỡ | Thử hai mẫu bằng nét chữ trong bảng; mẫu chưa đúng nét nên giữ nguyên theo điều kiện prompt | CHƯA ĐẠT | G06/review/mau-sua.png; G06/review/mau-sua-2.png; G06/acceptance-v2.json |

**#136 – GIỮ NGUYÊN:** giữ cả hai catalogue FS vì là hai dòng bơm khác nhau. Không đổi/xóa/ghi file nhóm G07. Không tính #136 vào 3 việc cần sửa.

## Phần chưa đạt

#52: có chữ k thường tại Power (kW) trang 1 và socket trang 4, nhưng đều khác nét đậm của tiêu đề bảng. Chưa xác minh được mẫu k cùng kiểu đậm trong 4 trang ảnh; giữ KW, không lấy phông/chữ từ ngoài file.

#53: mẫu đầu lỗi tách nền tại đường kẻ; mẫu thứ hai sửa nền nhưng còn một số ký tự không đúng nét khi ghép. Dừng cách này sau hai mẫu. Bảng trang 4 được giữ nguyên ảnh và nội dung nguồn đúng điều kiện “không đẹp thì giữ nguyên”; chưa gọi mục tiêu đồng cỡ là hoàn thành.

Hai mẫu thử được giữ riêng trong G06/review. Không dùng bảng thử trong file cuối.

## Nghiệm thu bản cuối

- Đọc lại từng nhóm mới: 35, 7, 2.2; đọc cả ví dụ ra FS - 35 - 7 - 2.2.
- Giữ nguyên tên FS, vị trí từng nhóm, lời giải thích và đường phân cách. Số/dấu nối chép từ dòng FS-35-7-2.2 thật ở bảng trang 2, điều chỉnh về đúng chiều cao chữ sơ đồ.
- So hình số 5 giữa sơ đồ và mẫu chữ đậm trong bảng: độ trùng vùng nét 87.06%; đã soi ảnh trước/sau.
- Cấu trúc PDF đạt; không đổi ngoài vùng ví dụ ở ngưỡng kiểm ảnh quét. Trang 2, 3, 4 giống nguồn từng điểm ảnh ở 200 điểm ảnh/inch; luồng nội dung trang 4 cũng giống nguồn.
- Giữ 4 trang, khổ trang, dấu trang, liên kết và mọi giá trị thông tin XML. Byte XML có thể đổi cách ghi dấu nháy/khoảng trắng khi lưu; giá trị được kiểm độc lập.
- Ảnh trang 1 vẫn 2480 × 3508 điểm ảnh, khoảng 300 điểm ảnh/inch; giữ bảng lượng tử JPEG và cấu hình màu. Ảnh gốc các trang 2–4 giữ nguyên luồng nén.
- Kiểm ghi lại ảnh không sửa ở trang 1 và 4 đều có sai khác trung bình dưới 1 mức màu.

Nguồn: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 01-10-2026\Nước thải\Aquaris FS_300dpi_75% (bản mới).pdf

File ra: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Nước thải\Aquaris FS_300dpi_75% (bản mới).pdf

SHA256 nguồn trước/sau: a297ed5b1dec97c33b6d2327d25d30bd3f317690548b9d5895c59e1376a63b31

SHA256 file ra: 97db44101b00605e71ce8996e8d4d08d672a8475cdcfa51ae1b1d5aa9597e033

SHA256 là mã kiểm tra nội dung file; kW là kilôoát, đơn vị công suất. KW là cách viết hoa chưa chuẩn còn giữ ở #52. JPEG là định dạng nén ảnh; XML lưu dữ liệu thông tin trong PDF.

## Dữ liệu cho kiểm chéo

- G06/inspection.json: đường dẫn, mã kiểm tra nguồn, phân loại 4 trang ảnh.
- G06/probe.json: dòng đọc được, tọa độ trang và nguồn k tìm được bằng nhận dạng ảnh.
- G06/font-probe.json: 11 khối hình của model nguồn và nguồn k ở dòng socket; máy đọc số 7 thành / ở model nguồn, đã đối chiếu ảnh và gán đúng.
- G06/font-p2.png, font-p3.png, font-p4.png: ảnh phóng to dòng model và dòng socket.
- G06/geometry.json: đường kẻ bảng, từng ô và từ chữ chuẩn bằng tọa độ ảnh gốc.
- G06/build-state-2.json: dữ liệu mẫu thứ hai, vị trí từng nét mới, chiều cao và hệ số phóng số.
- G06/final-state-v2.json và acceptance-v2.json: trạng thái bản cuối và kiểm độc lập; đây là hai file dùng để chốt kết quả.
- G06/acceptance.json là lần kiểm trước đã bắt ảnh trang 4 chưa khôi phục; đã khắc phục, không dùng kết quả cũ làm nghiệm thu.

Mọi PDF được ghi bằng catfix; không cài phần mềm. Không ghi đè, đổi tên hoặc xóa bất kỳ file nguồn nào. Các mẫu không đạt và ảnh kiểm cũ được giữ để đối chiếu.

Cần anh quyết: không có câu hỏi duyệt đang chờ; người kiểm chéo có thể tìm thêm nét k đúng kiểu và phương pháp giữ nét bảng. Phần chưa đạt vẫn giữ nguyên.

Phát hiện thêm không sửa: chưa đo độ chính xác biểu đồ vì nhóm này không thay bảng cột áp/lưu lượng.

Tiến độ: G06 CHƯA XONG – 1/3 ĐẠT, #52 và #53 chưa đạt; #136 giữ nguyên.

Lập báo cáo: 2026-10-03T01:02:39.658230

## Đính chính kết luận hiện hành53 ngày05/10/2026

Các mẫu chỉnh chữ ở trên vẫn CHƯA ĐẠT. Theo điều kiện gốc, phương án giữ nguyên53 được chốt ĐẠT riêng;G06=2/3 xử lý gồm51 sửa và53 giữ,52 còn. Không nhận bảng đồngcỡ/làm nét đã xong. ROOT và kiểm độc lập mở bản thật97db,ảnh/nội dungP4 giữ và0đổi điểmảnh. Báo cáo mới: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G06\ROOT53 CONDITIONAL KEEP REAL P4 READONLY 20261005T160135Z-1d63bb\03 BAO CAO8 COT KEEP53 VA GIOI HAN.md
