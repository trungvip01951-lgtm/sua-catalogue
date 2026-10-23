# BÁO CÁO NHÓM G07 – Aquaris FS khổ A3

Tổng: 5 việc phải sửa · ĐẠT 4 · CHƯA ĐẠT 1 · CHƯA THỂ XÁC MINH 0.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 54 | Catalog bơm nước thải Aquaris FS (bản mới).pdf | 1 | Ô m³/h trống dưới cột 800 l/min | 48 | Chép kiểu chữ ô 42, cùng cỡ 7 pt, căn giữa theo cột 800 | ĐẠT | So sanh G07.png; G07/acceptance-final.json; sai số tâm < 0,001 pt |
| 55 | Catalog bơm nước thải Aquaris FS (bản mới).pdf | 1 | industrian; movimentazionee; utllizzare; peril sollevamentodl; inseritidei; spiacevolidanni; 50 FHz; dean; nothigherthan; anda Schuko; threephase; trlphasé; IPB8 | industriali; movimentazione e; utilizzare; per il sollevamento di; inseriti dei; spiacevoli danni; 50 Hz; clean; not higher than; and a Schuko; three-phase; triphasé; IP68 | Sửa 13 cụm; dồn phần sau trong từng dòng bằng đúng phông/cỡ gốc, giữ nét đậm của đoạn Ý | ĐẠT | So sanh G07.png; G07/acceptance-final.json; đọc đủ 13 cụm; ảnh G07/review/mo-ta-sau.png |
| 56 | Catalog bơm nước thải Aquaris FS (bản mới).pdf | 1 | FESI; Imballa; CLOSEDIMPELLER; PotenZa; Kg³/m ×3 | PESI; Imballo; CLOSED IMPELLER; Potenza; kg/dm³ ×3 | Chữ thật; k từ cùng Arial gốc, ³ chép đúng mã nét có sẵn trong cùng phông | ĐẠT | So sanh G07.png; G07/acceptance-final.json; 3/3 đơn vị đọc đúng; phông nhúng giữ nguyên |
| 57 | Catalog bơm nước thải Aquaris FS (bản mới).pdf | 1 | 35 ô dùng dấu phẩy; 50HZ; 10/14/9 cỡ 8 pt | 35 ô dùng dấu chấm; 50 Hz; 10/14/9 cỡ 7 pt | Thay dấu thập phân trong bảng; chép kiểu chữ chuẩn ô bên cạnh, căn giữa | ĐẠT | So sanh G07.png; G07/acceptance-final.json; 35/35 ô đọc đúng, 3/3 số cùng cỡ 7 pt |
| 137 | Catalog bơm nước thải Aquaris FS (bản mới).pdf | 1 | FS300/80: cửa xả 50; ren G 2” | Cửa xả 50 còn giữ; ren G 3” đã sửa | Ren sửa bằng cùng phông. Cửa xả thiếu nét 8 trong phông MyriadPro-Regular (kiểu chữ thường gốc) | CHƯA ĐẠT | So sanh G07.png; G07/acceptance-final.json; G07/numeric-fonts.json; G07/source-audit.json |

Việc #136 GIỮ NGUYÊN: giữ cả hai catalogue FS khác nhau. G07 chỉ sửa file khổ A3; không ghi vào file G06.

Phần còn thiếu của #137: nét số 8 không nằm trong phông MyriadPro-Regular rút gọn của ô cửa xả. Đã kiểm cả 9 tài nguyên phông trong PDF và toàn bộ danh mục nét của phông; phông này chỉ có các chữ số 0–6. Giữ nguyên số 50 để không thay kiểu chữ. Ren G 3” đã đạt. Ø50 ở cột vật rắn giữ nguyên vì là đường kính chất rắn, khác cửa xả.

Nghiệm thu bản cuối: đọc lại trực tiếp PDF; cả 4 việc đạt đã soi ảnh từng vị trí. Khổ trang A3 ngang 1190,5 × 842 pt và 1 trang giữ nguyên. So sánh ngoài các hộp sửa ở 200 dpi (độ phân giải 200 điểm ảnh/inch) không có điểm ảnh thay đổi. 8 ảnh và 9 phông nhúng giữ nguyên từng byte; toàn bộ lệnh nét vẽ, thông tin tài liệu, liên kết và mục lục giữ nguyên. Giá trị thông tin XML/XMP giữ nguyên; mã hóa/định dạng chuỗi có thể được chuẩn hóa khi lưu.

Phương pháp chép ³/è: ký tự đã hiện thật trong nguồn và có đường nét trong bản đồ ký tự Unicode của phông Arial nhúng. Bộ kiểm phông chọn bảng mã MacRoman nên báo thiếu. Mã nguyên gốc của ký tự được chép bằng lệnh catfix, không đổi phông hay sửa bộ công cụ. Báo cáo chi tiết mã, tên nét và tọa độ nguồn nằm trong G07/build-state.json và G07/runs.json.

Đối chiếu biểu đồ nguồn:

| Model | Mốc bảng đã đo | Sai lệch cột áp lớn nhất (m) | Phần biên ngoài phạm vi đường gốc |
|---|---|---|---|
| FS75/40 | 4 | 0.215 | Không |
| FS100/40 | 4 | 0.150 | Không |
| FS150/40 | 5 | 0.377 | Không |
| FS200/50 | 6 | 0.134 | Không |
| FS300/80 | 9 | 0.394 | Không |

Tổng 28 mốc; sai lệch cột áp gần mốc lớn nhất 0,394 m, dưới ngưỡng max(1 m; 2%). Có 6 mốc sát biên nằm ngoài phạm vi đường gốc; các mốc đó dùng cột áp điểm đầu/cuối gần nhất, và ghi rõ trong G07/source-audit.json. Đây không phải xác nhận đầu/cuối đường trùng chính xác mọi mốc bảng. Không vẽ lại biểu đồ; toàn bộ lệnh vẽ nguồn giữ nguyên.

Cần anh quyết: phần cửa xả #137 còn cần nguồn nét số 8 đúng phông MyriadPro-Regular trong chính file, hoặc chỉ đạo thay đổi quy tắc phông. Phát hiện thêm không sửa: các khác biệt nhỏ ở điểm biên biểu đồ như bảng đo trên.

File kết quả: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Nước thải\Catalog bơm nước thải Aquaris FS (bản mới).pdf
Nhật ký: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\Catalog bơm nước thải Aquaris FS (bản mới).pdf.log.json
Ảnh so sánh: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\So sanh G07.png

Mã kiểm nguồn SHA256 (dấu kiểm để phát hiện file bị đổi): 4ae76b0cc2a5d1060763b332093ce952ac964902bd9aaa705f4a36b4ef9ce8fa
Mã kiểm kết quả SHA256: 5785252969ffb1f9cc78bda04f57bf573b555b26acf0a2deef68b61e96988c4e
