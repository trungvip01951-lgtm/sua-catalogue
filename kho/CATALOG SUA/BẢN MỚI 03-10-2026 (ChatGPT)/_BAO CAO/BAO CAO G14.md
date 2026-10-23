# BÁO CÁO NHÓM G14 – CM Perotac và Redpump

**CHƯA XONG: 7/8 việc ĐẠT.** #128 đã sửa các phần có mẫu chữ, còn 4 chỗ `(kw)` kiểu nghiêng trong 2 tệp vì thiếu chữ W đúng kiểu trong chính tệp. Không thay bằng phông khác.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 124 | Perotac + Redpump | 1 | 3 dòng nhận thiết kế Aquaris | Bỏ đủ 3 dòng mỗi tệp | catfix tẩy nét chữ, trả nền liên tục | ĐẠT | G14/NGHIEM THU/* TUNG VI TRI.png |
| 125 | Perotac + Redpump | 2 | Hai dòng lặp CM32-250/5.5 (79.5 m), /7.5 (95 m) | Bỏ 2 dòng, dồn 34 dòng phía dưới lên | catfix copy_box; giữ nguyên điểm ảnh DN/công suất/cột áp và cột cuối | ĐẠT | G14/MAU 2/* SO SANH.png; G14/NGHIEM THU CUOI.json |
| 126 | Perotac + Redpump | 2 | CM 100-160/220 | CM 100-160/22 | catfix tẩy riêng số 0 thừa; giữ các giá trị 220 khác | ĐẠT | G14/NGHIEM THU/* CM 100-160-22.png |
| 127 | Perotac + Redpump | 2 | Tham chiếu đường đặc tính trang 111–129, 130–141 | Bỏ đủ hai dòng mỗi tệp | catfix tẩy nét chữ, đọc ảnh lưu lại | ĐẠT | G14/NGHIEM THU/* TUNG VI TRI.png |
| 128 | Perotac + Redpump | 1–2 | Câu bỏ dở CM also available; Rated power(kw); disenadas | ĐẠT: bỏ hai câu chân trang; Rated power(kW); diseñadas. CHƯA THỂ: hai (kw) nghiêng mỗi tệp | Mẫu W đứng/ñ nghiêng thật cùng tệp. Không có W nghiêng cùng kiểu; giữ chỗ thiếu | CHƯA THỂ XÁC MINH | G14/NGHIEM THU/* MAU CHU.png |
| 129 | Perotac + Redpump | Tên tệp | ngnag | ngang tại bản ra | S.dst(..., rename=...), không đổi tên nguồn | ĐẠT | G14/NGHIEM THU CUOI.json |
| 157 | Perotac + Redpump | 2 | 9 tên mã bơm kết thúc .0 mỗi tệp | Bỏ .0 ở đủ 18 tên, giữ chữ/số khác | catfix tẩy riêng .0, giữ đúng nét nguồn | ĐẠT | G14/NGHIEM THU/* 9 TEN MODEL DUNG VI TRI.png |
| 158 | Redpump | Cả tệp | Tệp Redpump cung cấp | Bản đã sửa lưu riêng, tên đúng | Sửa từ đúng tệp 300dpi_75% anh chỉ định | ĐẠT | G14/NGUON.json; G14/NGHIEM THU CUOI.json |

Tổng: 8 việc · ĐẠT 7 · CHƯA ĐẠT 0 · CHƯA THỂ XÁC MINH 1.

Cần anh quyết: không xin duyệt lại; đã dùng quyền sửa anh cấp. Việc còn lại cần mẫu W nghiêng đúng kiểu trong chính tệp.

Giữ nguyên #162: logo Redpump “Italy Standard” (chuẩn Ý). Toàn bộ ảnh/lớp mặt nạ nguồn giữ nguyên byte và vị trí; hình bơm/logo không đổi.

Nghiệm thu:

- Đã mở và đọc lại cả hai trang của từng bản sửa; cấu trúc, số trang, khổ trang, siêu dữ liệu, nội dung XML, liên kết và dấu trang đều giữ nguyên. Nguồn không đổi mã kiểm SHA-256.
- Kiểm ngoài vùng sửa ở 150 điểm ảnh/inch, ngưỡng sai màu 12/255, kích thước nhỏ nhất 1 điểm in: rỗng ở cả hai tệp. Bản cuối giống mẫu 2 từng điểm ảnh và từng luồng nội dung.
- Dồn bảng: 34 dòng phía dưới được chép; mọi điểm ảnh trong DN (đường kính ống danh nghĩa), công suất kW (kilowatt), hp (mã lực), H (cột áp) đến cột cuối trùng nguồn. Bảng còn 46 dòng bên trái và 41 dòng bên phải, mỗi tệp.
- Đọc độc lập đủ 18 tên bỏ .0 và hai CM 100-160/22 đều đúng. Các dòng xóa không còn chữ. Bộ OCR (nhận chữ từ ảnh) tiếng Anh đọc sai ñ; đã soi trực tiếp hình mẫu nguồn và hình sau sửa để xác minh diseñadas.
- Hai tệp chỉ có mô tả và bảng thông số; không có biểu đồ đường đặc tính. Không có các trang 111–141 được tham chiếu trước đây, nên không thể nghiệm thu đường nằm ngoài tệp được giao.
- Mẫu 1 chưa đạt vì lớp trong suốt để lộ chữ cũ và phần ảnh chèn mở rộng chạm dòng kề. Mẫu 2 dùng các mảnh ảnh không mất dữ liệu đúng hộp sửa; đã hết chữ cũ và không đổi vùng ngoài. Giữ cả hai mẫu trong G14/MAU 1 và G14/MAU 2.

Phát hiện thêm (chưa sửa): đơn vị kw đứng ở hai đầu bảng trang 2 chưa nằm trong yêu cầu riêng “(kw)” ở mô tả mã bơm; ghi nhận để tránh tự bỏ qua.

Tệp đã sửa (bản chưa chốt trọn nhóm):

- C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Trục ngang\bơm trục ngang perotac model CM (bản mới).pdf; SHA-256: 64ef858f01db9c2e92ad03cf46f5cd5babf632030533aad26764557c253daba7
- C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Trục ngang\bơm trục ngang redpump model CM_300dpi_75% (bản mới).pdf; SHA-256: 1b49fa419a93905ab17701c59e84d9b708cce42f2af6c56e9950d882f1fc5019

Hồ sơ: G14/NGHIEM THU CUOI.json; ảnh toàn trang và từng vị trí tại G14/NGHIEM THU; hai mẫu tại G14/MAU 1 và G14/MAU 2.
