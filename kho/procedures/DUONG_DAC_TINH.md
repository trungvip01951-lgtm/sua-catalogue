Chuẩn trình bày hiện hành (ảnh, biểu đồ, bảng, chữ, tệp, định nghĩa hoàn thành): rules/CHUAN_TRINH_BAY.md; quy tắc: rules/QUY_TAC_HIEN_HANH.md — lệch thì hai tệp đó thắng. Tệp này là cách làm thời catfix (03–06/10/2026); phần "chỉ catfix ghi", 43/43, bản in chỉ áp khi sửa tại chỗ bằng catfix.

# Dựng và kiểm đường đặc tính bơm

Q là lưu lượng; H là cột áp. Qmax/Qmin là lưu lượng lớn/nhỏ nhất; Hmax/Hmin là cột áp lớn/nhỏ nhất. Điểm làm việc là một cặp Q–H đã xác định. η là hiệu suất; có hình nhưng chưa có bảng η thì số η vẫn CHƯA THỂ XÁC MINH.

## Dữ liệu và trục

Đọc từng mã, hàng, cột trực tiếp từ nguồn; lưu nguyên số gốc, ô trống và số bất thường vào bằng chứng. Ảnh chứng ô nghi ngờ phải thấy tên mã và đầu cột Q, kèm tọa độ và mã kiểm nguồn. Không chỉ chụp ô số lẻ. Ghép đúng mã với đường bằng tên thật, giao nét và dữ liệu; không gán theo thứ tự bảng hoặc cao–thấp. Hai mã có cùng một điểm định mức không chứng cùng toàn đường.

Lấy tâm vạch trục từ ảnh gốc và đúng đơn vị. Ảnh quét có khoảng vạch không đều: dùng ánh xạ tuyến tính từng đoạn giữa các vạch đã đọc, không lấy một tỉ lệ chung cho cả trục. Gốc pixel (điểm ảnh) khi đo tâm là index+0,5. 600dpi phóng ảnh gốc không tạo thêm dữ liệu nhà sản xuất.

Ví dụ quy đổi đúng toán học: Q(l/min)=Q(m³/h)×1000/60. Phải kiểm trục phụ US/Imp/feet (đơn vị Mỹ/Anh và foot) bằng nhãn/vạch chính của chính nguồn, không chép hệ số/tọa độ từ thương hiệu khác. Một đường bị khung che đầu/cuối không cho phép tự ngoại suy H=0.

## Khớp đường

Anh bổ sung ngày 03/10/2026: **một mã bơm, lưu lượng tăng thì cột áp phải giảm; thông tin sai phải sửa**. Rà cả bảng và đường Q–H ở cùng điều kiện; không áp điều kiện này cho η, công suất hoặc độ ồn.

1. Sắp các cặp đã đọc chắc theo Q; đánh dấu H tăng hoặc đường quay ngược. H bằng nhau sau làm tròn cần kiểm đường thật, chưa tự coi là đường giảm đã đạt.
2. Khóa Qmax/Hmax/Qmin/Hmin đã xác định và mọi điểm làm việc anh yêu cầu giữ. Không tự gán min 0 khi thiếu nguồn hoặc dùng tỷ lệ tầng thay điểm đã khóa.
3. Đề xuất số trung gian nguyên và đường giảm trơn qua các khóa. Ghi số trước/sau, nguyên nhân và căn cứ; không lấy số nguồn sai làm đích bắt buộc hoặc nhận số nội suy là thử nghiệm nhà sản xuất.
4. Khóa mâu thuẫn khiến đường giảm không thể tồn tại thì chỉ rõ cặp khóa và chờ quyết định. Chưa định danh đường hoặc đọc chắc số thì giữ CHƯA THỂ XÁC MINH.
5. Dựng mẫu trước/sau, nghiệm thu số/đồ họa độc lập và gửi theo điều kiện duyệt. Sau lưu mở tệp thật, kiểm lại bảng, các khóa và toàn đường rồi mới tính đạt.

Ví dụ 6SL25: bảng nguồn Q0→3 tăng 1 m ở /12,/14,/16,/18,/20. Hồ sơ đọc nguồn vẫn giữ; câu cũ cho giữ đoạn tăng đã bị thay thế. Các đoạn này phải vào danh sách cần chỉnh, nhưng chưa chốt số thay khi chưa đọc đủ extrema và khóa.

Chọn đường giảm trơn, không gợn hoặc vượt khóa. PCHIP là nội suy từng đoạn giữ xu hướng; Bézier là đường dùng điểm điều khiển; C1/C2 là liên tục hướng/độ cong ở chỗ nối. Đây là công cụ toán, không tự chứng đường đẹp hoặc dữ liệu thử nghiệm. Kiểm hướng tiếp tuyến trên toàn đường, chỗ nối, điểm uốn và lệnh vẽ thật; không chỉ kiểm vài điểm rồi bỏ qua đoạn tăng ở giữa.

Với số nguồn đúng còn giữ: điểm mới lệch không quá max(1 đơn vị, 2% giá trị bảng), theo đơn vị biểu đồ. Tốt nhất đi đúng mốc; dung sai không cho dời điểm làm việc đã khóa. Với số đã xác nhận sai và được chỉnh, kiểm theo bộ số đã chốt, đồng thời lưu chênh lệch với nguồn. Chỉ có điểm định mức thì chưa đủ chứng toàn đường hoặc extrema.

Số theo tỉ lệ tầng: cùng bảng/cột Q, lấy H/tầng của các model khác, trung vị×số tầng, làm tròn nguyên. Khớp đa thức bậc2–3 để kiểm độ mượt; lệch>2% thì chọn nguyên gần đường khớp nhất; số chốt trong±2 so đề xuất. Ghi toàn số trung gian và xin quyết định nếu vượt phạm vi. Không áp cách này cho ô không được giao.

## WC đã cho đổi điểm trung gian

Khóa Qmax/Hmax/điểm làm việc và H tại Qmax đã chốt trong từng hồ sơ. Bộ38 đường mỗi thương hiệu dùng13 nhóm/ảnh nhưng tọa độ/trục có thể khác. Giữ43 hàng/108 ô trống; dữ liệu H thực được kiểm413 ô/174 ô thay. Số trung gian đã dùng quy tắc `floor(H+0.5)` (làm tròn số dương tới nguyên gần nhất), không dùng làm tròn mặc định của Python ở trường hợp đúng0,5 nếu khác quy tắc.

100WC100-15-7.5 giữ Qmax150/Hmax33/Q100H15.50WC15-25-3 giữ Q35H4 theo hồ sơ. Các114 khóa/372 mốc của bộ38 phải kiểm trên tệp thật; bảng integer (số nguyên) không tự chứng đường đi qua đúng mốc. Nếu bản sau chỉ đổi ảnh, kiểm lại bảng và toàn38 đường nguyên vẹn.

## Đồng bộ nét và chữ

Trong cùng biểu đồ, cùng bộ RGB (màu đỏ–lục–lam), bề dày theo pt (point), độ trong suốt, đầu/nối nét. Nếu có phần liền/đứt, đo nhịp/pha từ nguồn, chiều dài theo cung thật để nối liền. Không chỉ dùng độ dày dự kiến: đọc lệnh và tiết diện nét nhìn thấy trên PDF.

Vẽ toàn biểu đồ cần giữ nhãn trục/chú giải/bảng và đúng phông. Glyph (hình một ký tự) dựng từ JPEG có thể khớp diện tích/nativepixel nhưng vẫn cong/méo khi600dpi; xem lòng4/5/9, nét in, dáng chữ và khoảng cách. Toàn cụm chữ nguồn có thể giữ bằng geometric clip (đường cắt hình học), nhưng nếu đường cũ cùng ảnh chạm chữ thì giữ cụm sẽ giữ cả mẩu đường, chưa chắc đồng bộ.

Đường dẫn nhãn phải mảnh/dễ phân biệt, không tạo cảm giác là đường bơm mới và không chạm đường khác. Không cắt/di chuyển điểm kỹ thuật chỉ để né nhãn.

## Các giới hạn hiện hành

- SA ngoài p8:183 model/1827 mốc;231 mốc bổ sung là tập con. Có4 điểm chưa đạt,226 chưa thể sau kiểm mới;1596 khớp kế thừa không phải phép đo mới. Không cộng231 vào1827.
- SL 6SL25/20 tại Q27: phép đọc LAN3 của tác nhân cho H bảng 150 m, H nét 158,561393 m, bất định ±5,021414 m, sai chắc còn 3,539979 m vượt giới hạn 3 m. /16 chưa thể vì biên còn chạm ngưỡng. ROOT chưa đọc độc lập phép này; chưa tạo mẫu hoặc sửa bảng. Q33 cần đọc trục thật, không ngoại suy vạch 0…30.
- SL là bộ nguồn riêng: 17 biểu đồ/196 mã/1.931 ô; ngoài trang 8 là 16 biểu đồ/183 mã/1.827 ô. Không chép số, tên hoặc tọa độ từ SA dù tổng ngoài trang 8 giống nhau.
- SP nhãn9/bảng8 chưa phân giải; sáu đường thiếu bảng vàη giữ chưa thể. Đuôi đã chấp nhận phải giữ nguyên điểm điều khiển.
- CDX p4 không ghép đủ7 model với7 đường trong dung sai; p5 có5 dòng/4 đường, không được tự thêm đường thứ5 hoặc chọn185-B thiếu chỉ từ tên.

Chi tiết bằng chứng và mã hiện hành: knowledge/CACH_DA_NGHIEM_THU.md, state/CURRENT_CHECKPOINT.md và danh mục bên trong history/.

## Quyền mới 06/10/2026: cong đều và lệch bảng tối đa5%

Đọc mục mới nhất trong QUY_TAC_CUNG_HIEN_HANH.md. Hình dạng không được uốn gợn dù C2 và khớp bảng. Trong phạm vi được giao, ưu tiên đa thức toàn miền, kiểm H giảm và độ cong không đổi chiều liên tiếp; soi thật mọi đường. Nếu lệch H bảng quá5%, anh cho sửa H trung gian nguyên theo đường; giữ mọi extrema và điểm làm việc khóa, lưu đầy đủ cũ→mới. Ngưỡng này thay2% cũ trong phần sửa theo lệnh mới. Không tự biến đường dựng thành dữ liệu thử hãng.
