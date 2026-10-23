# KẾT QUẢ KIỂM THỬ BƯỚC 0

| STT | File | Trang | Việc | Cũ | Mới | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 1 | tests/run_tests.py | - | Môi trường: Mở/ghi PDF  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 2 | tests/run_tests.py | - | Môi trường: Vẽ trang để so sánh  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 3 | tests/run_tests.py | - | Môi trường: OCR (chữ nét vẽ, chữ trên ảnh)  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 4 | tests/run_tests.py | - | Môi trường: Tách chữ trên ảnh  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 5 | tests/run_tests.py | - | Đọc/ghi lại luồng nội dung không mất byte: fx_cover_cdlf_aquaris_p1.pdf (31012 lệnh, 0.29s) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 6 | tests/run_tests.py | - | Đọc/ghi lại luồng nội dung không mất byte: fx_raster_perotac_sp_p9.pdf (22 lệnh, 0.00s) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 7 | tests/run_tests.py | - | Đọc/ghi lại luồng nội dung không mất byte: fx_text_wc_p1.pdf (850 lệnh, 0.00s) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 8 | tests/run_tests.py | - | Đọc/ghi lại luồng nội dung không mất byte: fx_vector_aquaris_sp_p9_goc.pdf (18480 lệnh, 0.16s) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 9 | tests/run_tests.py | - | Chữ nét vẽ: tìm thấy đúng 1 chỗ "818" [Match('818' page=1 bbox=(515.5,509.3,528.7,515.1) objs=[155])] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 10 | tests/run_tests.py | - | Chữ nét vẽ: đọc lại thấy "815", hết "818"  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 11 | tests/run_tests.py | - | Chữ nét vẽ: vị trí chữ mới trùng bản đã kiểm duyệt (sai lệch <= 0.01pt) sai lệch 0.0027 pt |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 12 | tests/run_tests.py | - | Chữ nét vẽ: chỉ ô sửa thay đổi điểm ảnh vùng đổi={1: [(np.float64(524.6), np.float64(509.3), np.float64(529.0), np.float64(515.6))]} ngoài vùng={} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 13 | tests/run_tests.py | - | Chữ thật: tìm thấy "irrugation" và "(KW)"  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 14 | tests/run_tests.py | - | Chữ thật: đọc lại lớp chữ đúng ({'found': True, 'absent_ok': True, 'ok': True}, {'found': True, 'absent_ok': True, 'ok': True}) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 15 | tests/run_tests.py | - | Chữ thật: chỉ chỗ sửa thay đổi vùng đổi={1: [(np.float64(124.3), np.float64(345.1), np.float64(163.7), np.float64(357.1)), (np.float64(806.4), np.float64(178.1), np.float64(826.6), np.float64(186.7))]} ngoài={} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 16 | tests/run_tests.py | - | Ảnh: chọn đúng ảnh đang hiển thị (không chọn lớp ảnh chỉ hiện trong nét chữ) PageImage(X11 1732x1240 page=(0.0,0.0,831.6,595.0) ~150dpi #4) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 17 | tests/run_tests.py | - | Ảnh: OCR tìm thấy "1750" [(1330, np.int64(1039), 1357, np.int64(1051))] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 18 | tests/run_tests.py | - | Ảnh: học được mẫu chữ số 1, 5, 7  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 19 | tests/run_tests.py | - | Ảnh: OCR đọc lại "175" '175' |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 20 | tests/run_tests.py | - | Ảnh: thay đổi rõ rệt (>48 mức, >2pt) chỉ nằm ở ô sửa vùng={1: [(np.float64(639.4), np.float64(91.0), np.float64(650.9), np.float64(95.3))]} ngoài={} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 21 | tests/run_tests.py | - | Ảnh: ghi lại ảnh không sửa gì -> sai khác trung bình < 1 mức màu {'kind': 'image', 'image': 'X11', 'max_diff': 0, 'mean_diff': 0.0, 'p99': 0.0, 'rect': (np.float64(384.1), np.float64(264.9), np.float64(453.2), np.float64(334.0))} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 22 | tests/run_tests.py | - | Biểu đồ: đường cong mượt đi sát điểm bảng (đơn giản) lệch tối đa 0.272 |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 23 | tests/run_tests.py | - | Biểu đồ: hiệu chỉnh trục tuyến tính (0.000914285714259222, 0.5721240000000023) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 24 | tests/run_tests.py | - | Biểu đồ: tìm đủ 8 đường cong [308, 309, 310, 311, 312, 313, 314, 315] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 25 | tests/run_tests.py | - | Biểu đồ: đường vẽ lại khớp bảng trong dung sai [(0, 170, 170.34), (5, 157, 155.56), (10, 133, 135.45), (14, 110, 108.42), (16, 90, 89.31), (18, 65, 65.76)] {'method': 'poly3', 'max_dev': 2.488, 'tol': 3.4} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 26 | tests/run_tests.py | - | Biểu đồ: giữ nguyên màu và độ dày nét  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 27 | tests/run_tests.py | - | Ảnh bìa: xoá bơm đế gang (R25 không còn) ['R13', 'R16', 'R18', 'R20', 'R22', 'R16', 'R26'] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 28 | tests/run_tests.py | - | Ảnh bìa: bản sao bơm đặt đúng ô (sai lệch < 0.01pt) [(np.float64(238.30848), np.float64(212.0904), np.float64(376.36512), np.float64(520.6199999999999)), (np.float64(80.874565187544), np.float64(163.45199999999997), np.float64(189.607834812456), np.float64(406.4496))] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 29 | tests/run_tests.py | - | Ảnh bìa: chỉ vùng ảnh bìa thay đổi (chữ trên bìa giữ nguyên vị trí) {} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 30 | tests/run_tests.py | - | Excel: chỉ đúng các ô cần sửa thay đổi ['C15', 'C21', 'C22', 'D16', 'D17', 'D18', 'D20', 'D21', 'D22'] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 31 | tests/run_tests.py | - | Excel: ảnh/định dạng/in ấn không bị đụng tới ['xl/calcChain.xml', 'xl/sharedStrings.xml', 'xl/worksheets/sheet2.xml'] |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 32 | tests/run_tests.py | - | Excel: mở lại bằng openpyxl được, giá trị đúng  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 33 | tests/run_tests.py | - | Cấu trúc file sau sửa hợp lệ: vec_815.pdf [] 245417->245270 bytes |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 34 | tests/run_tests.py | - | Cấu trúc file sau sửa hợp lệ: text.pdf [] 185640->185659 bytes |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 35 | tests/run_tests.py | - | Cấu trúc file sau sửa hợp lệ: raster.pdf [] 174727->172313 bytes |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 36 | tests/run_tests.py | - | Cấu trúc file sau sửa hợp lệ: cover.pdf [] 760836->760890 bytes |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 37 | tests/run_tests.py | - | Đường dẫn máy anh: tìm đúng file vào, file ra cùng tên khác thư mục, đổi tên #129 Session – MÁY ANH TRUNG (code chạy thẳng trên máy anh, đọc/ghi file trong thư mục của anh) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 38 | tests/run_tests.py | - | Đường dẫn máy anh: sửa + lưu + kiểm qua S.job (nhật ký vào _BAO CAO) {}{} |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 39 | tests/run_tests.py | - | Đường dẫn máy anh: G02 lấy đúng file đã sửa của G01, ghi ra thư mục riêng, nhật ký riêng D:\TempSystem\catfix_ses_5ee5zklh\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Nước thải\G02 (gồm cả G01)\Catalog cắt rác Aquaris WC (bản mới).pdf |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 40 | tests/run_tests.py | - | Đường dẫn máy anh: ghi tiến độ được, không cho ghi đè file vào  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 41 | tests/run_tests.py | - | Đường dẫn máy chủ ChatGPT: file tải lên trong /mnt/data, ra /mnt/data/out Session – MÁY CHỦ CHATGPT (file anh tải lên trong D:\TempSystem\catfix_ses_5ee5zklh\data) |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 42 | tests/run_tests.py | - | Windows: in tiếng Việt khi đầu ra dùng bảng mã cp1252 không lỗi  |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |
| 43 | tests/run_tests.py | - | Windows: tìm được tesseract khi không có trong PATH (biến CATFIX_TESSERACT / chỗ cài mặc định) và OCR chạy C:\Users\H2\AppData\Local\Programs\Tesseract-OCR\tesseract.exe True 775 |  |  | ĐẠT | Đầu ra nguyên văn của bộ kiểm thử |

Tổng: 43 việc, ĐẠT 43, còn lại 0.