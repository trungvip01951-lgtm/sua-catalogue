# CM/CDLF: kiểm nhãn và tái dùng nghiệm thu theo phần thay đổi

Ghi chú ngày 04/10/2026 từ ROOT. Chưa tiếp nhận PDF CM/CDLF mới, chưa thay sổ tiến độ hay quy tắc niêm phong. Không xác nhận Claude đã đọc/áp dụng.

## CDLF — bản ráp cuối đã kiểm toàn vẹn, bốn nhãn chưa đạt

Recipe khóa: wc_sample_graphics_G16_full_merge_RAM_plus_P8_recipe.json, SHA256 aa5a01476b8ea35a9137e4af5300603c9a28b9bf9e373ab26498b96f3f845e51. Helper thuần SHA256 23ea88a57c80f5e6d5be23a1fff0d10adc6af870d3562675c43fb0fff35ee194. Manifest 16 luồng lệnh vẽ SHA256 f7d571d02ec9eaf78e987eca74cdfb448a71081d1006ea954f1468bfed3ce21e. Nằm tại outputs của catalogue-wc-kiem-mau-perotac-redpump.

ROOT tự dựng đúng 16 luồng lệnh đã khóa; mọi nét/chữ ngoài danh sách sửa giữ nguyên. Đối chiếu ảnh 16 trang ở 200 điểm ảnh mỗi inch: ngoài vùng sửa, ngưỡng sai biệt 0, không thêm đệm, số điểm ảnh khác =0. Ảnh/mặt nạ/phông/khổ trang/liên kết/mục lục/Info/XMP giữ; bốn trang đầu mỗi tệp giữ nguyên nội dung. Hồ sơ: _BAO CAO\G16\ROOT KIEM RAM RAP CUOI344 VA16 QH PHU 04-10-2026\ROOT ACTUAL16 STREAM VA NGOAI16 TRANG.json, SHA256 41b1689f091f820f3c374fc5916aabd255a3c255c5be695c12e171537163514a. Đây chỉ là chứng bảo toàn trong bộ nhớ, không nghiệm thu hình thức hay PDF đã lưu.

G03 tự dựng khớp 16 luồng, 344 mã bơm/16 QH phụ có độ dày thống nhất theo hãng. Nhưng cả bốn nhãn -7-2/-4-2 trang11 dính nhãn -6/-3: mắt đọc thành '-7-2-6'/'-4-2-3'; lưới cắt lõi chữ. ROOT mở hai ảnh thực và xác nhận lỗi. JSON166 SHA256 b02245ac74e81bc5407ee2d372514952d807c2765b64446a909c27fcafe99768. Tác giả đang sửa riêng bốn nhãn bằng bản mới; file đã khóa giữ bất biến.

Bài học: số điểm ảnh giao giữa lõi chữ và đường bơm bằng0 chưa đủ. Phải kiểm khoảng hở với chữ hàng xóm, khả năng đọc cả cụm, vị trí theo đúng nhánh, vạch lưới qua lõi chữ và ảnh toàn biểu đồ. Chứng hình học của 324 neo giữ riêng; 230 neo đổi độ dày bút nhưng đường/ma trận không đổi, không vì thế đo lại bảng hay neo. Chỉ cần nghiệm thu kiểu bút mới. 400 ô số trong ảnh là một phần của tổng2106, không cộng lần nữa. Bốn QH phụ raster và sáu header thiếu /h vẫn chưa thể; không đổi trạng thái đó thành đạt khi 344 đường chính đạt.

## CM — chữ đã chứng, mẫu cũ lỗi lưới và dòng tốc độ

Recipe03/helper04 bất biến. ROOT/G18 đã đọc đủ78 cụm mới, bốn ghi chú giữ mã chữ/phông/khoảng cách nguồn, 38 ID đủ khoảng hở thật với đường. Với ID3/30, hộp bao bảo thủ nhỏ hơn0,4pt nhưng contour ký tự thật đạt0,69967/0,51806pt; không kết luận glyph chạm đường chỉ từ hộp bao.

Hai lỗi mẫu03: dòng tốc độ đè trục l/min và lưới bị cắt sẵn tại caption cũ. Ngoài vùng cũ còn1239 điểm ảnh chưa được chứng chủ sở hữu; giữ CHƯA ĐẠT, đã dừng truy nguyên mẫu lỗi. Không nới hộp để ép0. Bản mới đang hạ dòng tốc độ, nối67 khoảng bằng đúng đầu đoạn nguồn dưới đường bơm, giữ màu/nét0,2830008pt/độ nghiêng nguồn và nền tiêu đề N. Một số ID đổi vị trí để tránh lưới nối; cần đọc lại khoảng hở/vị trí phát xạ thực cho ID đổi, giữ chứng431 số/38 đường và chương trình phông khi literal không đổi.

Khi lập mặt nạ kiểm ảnh, dùng nét/contour và trạng thái phông/clip của chính lệnh nguồn–đích, kể cả phủ mực thực của bộ hiển thị, không thêm hộp tùy ý. Mẫu lỗi trong bộ nhớ chưa phải một PDF ứng viên đã lưu.

## G12 — không tự thêm yêu cầu mọi ô khớp tuyệt đối

RAM02 của hai3M (SHA256620b3c4d10bb2be1e914ad671778c7b51e315e219bf3b40b7d3fac858df17b30) sửa17 đoạn đầu/tệp, giữ đoạn đuôi quan sát; các ô thường dùng đúng dung sai6(d) đã đọc. Sáu cặp cuối nguồn nằm hơi sau Q cuối bảng và cao hơn số bảng khoảng0,0018–0,262m. Yêu cầu đồng thời mọi ô exact và mực đuôi exact sẽ mâu thuẫn, nhưng đó không tự tạo lỗi vượt dung sai gốc1đơn vị/2%. Không tự cắt đuôi, suy cực trị vật lý hoặc thêm số định mức. G12 chưa có nghiệm thu đồ họa/PDF mới; tác giả nhận phần kiểm chuẩn bị rồi quay lại ưu tiên bốn nhãn G16 bị lỗi.

RAM = bản dựng trong bộ nhớ; stream = luồng lệnh vẽ; contour = biên thật của ký tự; glyph = hình nét của ký tự; delta = phần thay đổi mới; raster = ảnh bằng điểm ảnh; SHA256 = mã kiểm nội dung. Chỉ ROOT tiếp nhận bản chính sau nghiệm thu tệp thật, nguồn giữ nguyên và có bản sao trước.
