# Tiếp tục SP95 — đã kiểm nguồn, chưa lấy mẫu mới

Lượt trước có tiến triển thật: SL4SL12 đã lưu và tiếp nhận bản `a04dbd5a9b035fd260a66027f246e4cb98740c6b088bff5e61376ea994427ac7`. Nghiệm thu độc lập và hậu kiểm bản chính đạt; 15 đường/15 nhãn mới, 150 số giữ nguyên. Toàn SL còn việc. Số việc gốc giữ 135/149.

Đường dẫn điện thoại SL: https://at.adobe.com/m8a1ENCIBE57uBMf. Đã tải lại đủ 3.778.013 byte, SHA trùng bản chính. Phiếu điện thoại `_BAO CAO/G04/SL4SL12 DUONG15 GIU150 GUI DIEN THOAI EXACT 20261004T215310Z-4b0675/01 PHONE LINK EXACT CANONICAL_SL_A04DB VERIFIED.json`, SHA `0727d6ee6a0ce97e8ccf7c0a3dca2d15c0c348630ceab4e92cada246446ca38b`.

SP hiện hành vẫn `8a104308703154d437102a328a42ebf81c0b95cff97a26b6b2022de8112fae28`; nguồn `e1b94dc6f23c35d18d61cee71d9d88c844b1070d14ff662bbabe2256cdd690c9`. Trạng thái tệp điều phối sau SL: danh mục `5f1a3be1cba85d54c746149d32690b73a8799cfae5d34afdf83ec7386167d03c`, tiến độ `a319cb4e39e196df1027441ba234932452a488d6744ce1941f2d81769355b5e2`, mốc tiếp tục `c7b57c32f41c307fb08e4e51f7475f62c4fb271fc45dba641b77c3f702ebae61`. Không sửa các tệp này trong bước chuẩn bị SP95.

SP95 đã kiểm độc lập nguồn 132 số/12 nhãn/24 điểm đối chiếu, trục chính; toàn 120 cặp giảm, không sửa bảng. Nguồn đọc mới `15110112...`, QA nguồn `bde6e3e9...`. ROOT đã xem bảy ảnh nguồn và đọc trực tiếp nguồn/bản hiện hành: 225 đối tượng, P10 Contents167 là riêng, ảnh X13 nguồn và hiện hành cùng byte. Phiếu ROOT basis92 trong `_BAO CAO/G05/ROOT SP95 SOURCE132 CURRENT225 P10 BASIS READONLY 20261004T214634Z-846774`, SHA `57b95b6a8b4cd7b2e53847b072a6d6a761085b07305c443a2a7297023e163ac2`.

Toán tĩnh12 đường: 47 đoạn nối C2, 132 mốc trong dung sai, 24 đầu-cuối giữ, toàn đoạn lưu lượng tăng/cột áp giảm. Không gọi mọi mốc nằm chính xác trên đường. Phiếu `9942b427...`, QA toán/chữ `724a25de...`; 11 mã có đổi dấu độ cong được giữ chẩn đoán, hình thức phải xem mẫu thật.

Bộ chữ12 nhãn/77 phần nguyên RGB nguồn `2196c816...`; ROOT/Sol đã xem đủ atlas12. Giữ giới hạn ảnh JPEG và số4 hơi xám. Tái dùng12 ảnh chữ đã có trong225 đối tượng: token8→152,SP→131,9→183,5→110,-→149,1→151,0→142,2→150,3→111,4→153,6→120,7→154; tất cả thế hệ0. Có40 ảnh trùng toàn tệp được ghi rõ, các Ref chọn thuộc alias SP25 thật. Phiếu tái dùng `6ce979a9...`, QA mapping `d5763485...`. Không cần thêm ảnh/luồng chữ.

Vị trí144 `fb4a5462...`: 12 nhãn x148, cao12 pixel nguồn, 144 phép nhãn–nhánh và66 cặp nhãn không giao. BODY giữ `[130,197,630,581]` và `[630,240,745,581]`. ROOT đã đọc mã144 và bốn ảnh lưới/tiêu đề/đầu đường. Trước mẫu mới, chốt5 vùng giữ0: tiêu đề, chữ trụcH, hiệu suất+trụcQ, bảng132, kích thước bên phải. Bốn vùng khung là số chẩn đoán vì chứa đầu các đường đang sửa; không coi toàn khung đổi0 là điều kiện mới. Phải ghi đủ số và xem trực quan, không giấu lỗi.

Đường mới hiển thị đủ Q0→Q120, clip chart riêng bắt đầu x125, BODY không mở. ROI `[125,191,750,587]` khóa trước mẫu. Sau mẫu phải xem12 đầu đường600 và toàn trang200 để phát hiện vệt nguồn còn ở2 pixel gần trục. ROOT đã đọc toàn helper145 hiện có, nhưng chưa nhận SHA cuối/caller/combinedplan nên chưa cấp mẫu.

Tác nhân next_work_scope chuẩn bị combinedhelper/caller; cdlf_saved_visual chuẩn bị mã lưu225/no-newstream, chưa chạy; qa_sol_vua kiểm tĩnh độc lập. ROOT phải đọc toàn mã/plan cuối, thực hiện dấu PDF trước mẫu đúng một lần cho scopeSP95, cấp một mẫu; nghiệm thu mẫu rồi mới một lần lưu ứng viên, kiểm file lưu độc lập, tiếp nhận byte chính xác và ghi sổ. Chưa có marker/mẫu/Save SP95; không tái làm P5/P7/P11/P12 đã đạt.

Excel: đã tìm lại cửa sổ Book1/Product Activation Failed, lỗi `window capture timed out: timed out waiting on channel`; tìm lại cửa sổ và phục hồi một lần lỗi `failed to activate captured window`. Không dùng nút Close20 cũ, không gõ/lưu tài liệu/cài phần mềm/kill tiến trình. DWO bản xem trước in vẫn NOT RUN. Phiếu G18 `e97aefe9...`; không suy hộp Office đã đóng từ danh sách cửa sổ.

Toàn mục tiêu còn, giữ ACTIVE. Đây là tiếp tục tự động cùng phiên, không phải ngắt môi trường; không chạy lại BƯỚC0 hoặc mẫu đã đạt chỉ vì chuyển lượt.
