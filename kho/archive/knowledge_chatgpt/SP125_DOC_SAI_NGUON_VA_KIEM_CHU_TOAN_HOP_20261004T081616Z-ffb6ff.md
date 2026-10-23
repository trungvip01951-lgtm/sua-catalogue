# SP: đọc đúng nguồn125 và nghiệm thu mẫu thật

Nguồn6SP30-13 tại18 m³/h là125 m; JSON cũ ghi126 là lỗi đọc dữ liệu, không phải lỗi bảng catalogue. Bản chính hiện hành đã giữ125, không sửa bảng thành126. Nguồn6SP30-42 tại0 m³/h là478 m.

Đã đối chiếu raw/giải mãRGB của nguồn và bản chính, nhìn trực tiếp ô nguồn và tệp thực. Tác nhân đọc lại đủ104 ô của13 hàng trên14 ảnh gốc trước so JSON:104 khớp dữ liệu mới,0 ô mờ; chỉ một ô JSON cũ sai.

Cubic cũ cho đường13 ởQ18 ra127.605226176291 m: so126 có thể qua nhưng so đúng125 vượt dung sai2.5 m. Chỉ tính lại đường13 với8 neo nguồn đúng125;12 đường/96 phép kiểm khác giữ literal. Kế hoạch mới ởQ18 cho127.095226176291 m, lỗi2.095226176291≤2.5; đầu148 và cuối46 giữ. Tổng vẫn104, không cộng8 neo mới lần nữa. Phép toán mới không tự chứng mẫu hoặc PDF thật đã đạt.

MẫuSP19 đầu tiên có38 nét vẽ vì19 nhánh được clip riêng đứt/liền; đây vẫn19 model. Mẫu này CHƯA ĐẠT: hai cặp nhãn30/26 và24/20 giao quầng chữ; vùng nhãn cũ còn dấu chấm/quầng. Giữ tất cả ảnh/bins và0PDF. Ngoài vùng0 hoặc phép toán qua không thay nghiệm thu chữ/lưới sạch.

Khi thay phần chữ nguồn từ crop nhỏ sang crop đủ viền, phải tính lại kích thước hộp chữ thực và kiểm mọi cặp hộp chữ, không chỉ khoảng cách chữ với đường cong. Giữ cỡ/phông/RGB nguyên, đặt lại vị trí cho đủ khoảng hở. Nền dọn phải bao cả viềnJPEG chữ cũ mà không đụng trục/khung; phân biệt halo bitmap nguồn và cácDo bản hiện hành. Không tự mở rộng maskQ0/khung hoặc xóa tài nguyên trước khi có phương án rõ.

SL3SL3 cũng mới có một mẫu7 đường/91 mốc; vẫn chờ kiểm số native và phân loại viền ở vị trí nhãn cũ. NềnSL dùng profile trung vị và phépmin có tính toán; không gọi là chép nguyên điểmRGB nguồn.

Bằng chứng nguồn: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT SP13 Q18 SOURCE125 CURRENT125 LOCK READONLY 20261004T074935Z-31bda3\01 ROOT SOURCE CURRENT125 MAX478 RAW RGB ACTUAL600.json
SHA256: 176b11860456624966ed134a913cd26e182da2b0afb24dad12fa67dd537f0676

Đối chiếu104: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\SP SOURCE104 ALL13 DIRECT NATIVE ROW READONLY 20261004T075845Z-b71769\03 DIRECT104 SOURCE COMPARISON NEW135 ALL104 MATCH OLDONE WRONG.json
SHA256: e648d2347febfb496ec42f150bc8a5119baaf3bace1c535d471fdf6726ce5470

Mẫu thực và đánh giáROOT: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT SP125 SOURCE104 ACTUAL SAMPLE GRAPHICSFAIL PROGRESS 20261004T081616Z-ffb6ff\01 ROOT DIRECT ACTUAL SP FAIL SL PENDING NO PDF.json
SHA256: ed616a9c89ddef8018fcf63824955d6293cd8f3ff102b17c47b2d3237307dc87

Việc gốc giữ135/149; toàn bộ yêu cầu mở rộng và mục tiêu dự án chưa hoàn tất.
