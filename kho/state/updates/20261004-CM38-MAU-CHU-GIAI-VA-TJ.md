# CM38 — mẫu chú giải và bài học dịch chữ gốc

Mẫu 03/04 được ROOT tự dựng, đọc và soi ảnh ngày 04/10/2026; chưa tạo PDF hoặc tiếp nhận bản giao. Các bảng và đường của RAM21 đã có bằng chứng riêng, không đọc lại 431 số chỉ vì đổi nhãn.

- Công thức mới gỡ đúng 504 lớp của 36 nhãn A/B/C, bốn lớp số1/2 cũ và hai chú giải cũ. Có 38 số ngắn, 38 dòng chú giải, hai dòng tách tốc độ, ba đường chỉ mảnh. Dùng chính phông Aquaris Ref28 Univers-CondensedLight, cỡ 8.0000064 điểm PDF; không làm tròn cỡ thành8.0 hoặc thay phông ngoài.
- ROOT đọc đủ78 chuỗi thật và bốn ghi chú nguồn sau dịch. Mã ký tự, phông, cỡ, ma trận tuyến tính và khoảng cách từng glyph của bốn ghi chú giữ; sai số dịch lớn nhất3.83125e-11pt. Trang1–3 giữ nguyên nội dung RAM21; tài nguyên/metadata giữ. Biên bản `_BAO CAO/G13/ROOT KIEM ACTUAL RAM38 ID VA CHU GIAI NGUON 04-10-2026/ROOT DOC78 CHU VA4 NOTE GIU TJ.json`, SHA256 `c291e78bccfe48801b2e6b6d07a677fea945a6a600b0c02f7ac36b7fd85e1bbd`.
- ROOT mở đủ bốn ảnh trước/sau toàn trang150, chú giải600, đồ thị300. Hình thức CHƯA ĐẠT: hai dòng tốc độ baseline506 chồng số trục l/min; nhiều khoảng lưới đứt của nhãn cũ lộ ra sau gỡ nhãn. Báo cáo8 cột `BAO CAO8 COT ROOT MAU38 NHAN VA HAI LOI HINH THUC.md` trong cùng thư mục, SHA256 `787572a0e076b5719094df58b5126b7ab38663da924f5cbe0cc0fce4ad6b860d`.
- Source lưới gồm203 đối tượng nét thẳng bị cắt sẵn. Không có ô trắng trong biểu đồ; hình tô trắng duy nhất là chữN header, sourceoi655. Khôi phục khoảng thiếu do nhãn cũ bằng các đoạn nối cùng bút nguồn, đặt dưới đường cong, nối endpoint thật theo cùng vạch. Không nối qua ô xanhN, không thay hệ tọa độ hoặc geometry38. Màu nguồn RGB(0.102051,0.0900879,0.110107), độ dày khoảng0.2830008pt; vài vạch hơi nghiêng. HeaderN#110 và giải thích#155 còn riêng, không tự dùng phông mới để chốt.

## Bài học dịch ghi chú PDF

Bốn ghi chú `Hm = Prevalenza`, `Hm = Head`, `Q = Capacità`, `Q = Capacity` cùng chung một Tm đầu, các dòng sau dùng Td. Giá trị `TextRun.Tm` tại một Tj không nhất thiết bằng Tm gần nhất trong lệnh trang: phải diễn giải các Td và lệnh chữ trước đó. Nới epsilon để ép hai ma trận bằng nhau sẽ che lỗi chọn điểm dịch.

Phương án đã kiểm dùng Td dịch trước lệnh hiển thị đầu mỗi ghi chú và Td nghịch sau lệnh cuối, giữ toàn bộ Tf/Tj/TJ và Td nội bộ. Chỉ an toàn khi ghi chú bắt đầu ở dòng đã khóa và lệnh tiếp theo định vị lại chữ hoặc kết thúc ET; nếu còn chữ dùng vị trí Tm đang tiến thì phải chứng minh phục hồi trạng thái tương ứng. Không gõ lại ghi chú theo độ rộng danh nghĩa vì có thể mất khoảng cách chữ gốc. Bốn ghi chú có hai kiểu phông nguồn /R34 và /R36; không ép chúng thành kiểu Ref28 dùng cho chú giải mới.

Recipe03 SHA256 `fd1ae64e0ccf55a9a415c36254bf50c84eafc0c23f720306b5bf3461932a93a3`; helper04 SHA256 `abb99ec1fa466fbb38f9ce8e623eaede06fcb643ac03a75a4125023cae05e5ad`. Hai tệp đã khóa tại app `catalogue-kiem-do-hoa-dong-bo/outputs/g13-ram21-numbered38-independent`; tác giả phải dùng tên mới nếu sửa. G18 kiểm độc lập mapping/phông/khoảng cách và ngoài vùng; mẫu03/04 không được ghi thành hình thức đạt. Chưa xác nhận Claude đã đọc/áp dụng tài liệu này.

Glyph là hình ký tự; baseline là đường chân chữ; metadata là thông tin kèm tài liệu; source là nguồn; recipe là công thức dựng; helper là hàm hỗ trợ; RAM là bản dựng bộ nhớ. Tm là ma trận định vị chữ; Td là lệnh dịch dòng chữ; Tf chọn phông/cỡ; Tj/TJ hiển thị chữ và khoảng cách; ET kết thúc khối chữ. RGB là ba thành phần màu; pt là điểm trên trang; dpi là mật độ điểm ảnh; SHA256 là mã kiểm nội dung.
