Chuẩn trình bày hiện hành (ảnh, biểu đồ, bảng, chữ, tệp, định nghĩa hoàn thành): rules/CHUAN_TRINH_BAY.md; quy tắc: rules/QUY_TAC_HIEN_HANH.md — lệch thì hai tệp đó thắng. Tệp này là cách làm thời catfix (03–06/10/2026); phần "chỉ catfix ghi", 43/43, bản in chỉ áp khi sửa tại chỗ bằng catfix.

# Quy trình sửa và nghiệm thu

## 1. Chọn đúng nguồn

Đọc BƯỚC0 và43 kiểm thử theo prompt chung; giữ nguyên gói. Lấy đường dẫn qua Session/cấu hình dự án. `S.src(tên)` nhận tên gốc, không nhận chuỗi có thư mục con. `S.result(tên, sub=...)` dùng bản hiện hành đã sửa, ví dụ bản G02 hợp nhất G01. `S.dst()` chỉ là đích, không chứng tệp tồn tại/đã đạt.

Đọc prompt nhóm và mã#. Định vị chữ/số/tọa độ trên nguồn thật: `what_is_at`, `outline_dump`, `TL.dump`, `R.find`, rồi tự nhìn ảnh cắt. Chữ nhận dạng tự động bị sai, chữ ẩn hoặc bảng Excel không đủ làm chứng vị trí; phải đối chiếu với ảnh.

Ô số nghi ngờ cần ảnh có cả tên mã và đầu cột Q, tọa độ gốc và mã kiểm nguồn; không kết luận từ ô phóng lẻ. “Đã đọc đúng số nguồn” không đồng nghĩa thông tin kỹ thuật đúng. Theo lệnh anh bổ sung 03/10/2026, rà các đoạn Q tăng/H không giảm, đề xuất sửa số trung gian và đường đồng thời theo procedures/DUONG_DAC_TINH.md; extrema và điểm làm việc đã khóa vẫn giữ.

## 2. Phân loại chỗ sửa

| Loại | Hướng đã dùng |
|---|---|
| Chữ thật có chương trình phông | Chép ký tự/nét trong chính tệp, giữ phông, cỡ, màu, dòng cơ sở |
| Chữ bằng nét vẽ | Chép nhóm nét/viền đúng đối tượng; đo đầy hình và khoảng cách, không chỉ hộp diện tích |
| Ảnh quét hoặc ảnh ghép | Đọc ảnh gốc, phép đặt ảnh và vùng cắt; giữ byte ảnh/SMask (mặt nạ trong suốt); sửa đúng vùng bằng catfix |
| Toàn biểu đồ | Khóa bảng/trục/nét/chữ; mẫu trong RAM (bộ nhớ); tạo ứng viên CATFIX mới sau đủ điều kiện |
| Excel | Sửa các phần XML trong gói XLSX bằng catfix; giữ ảnh, biểu đồ, ô trống, công thức và SGV ẩn |

Không có ký tự/phông phù hợp thì ghi CHƯA THỂ. Không lấy ký tự giống hình ở phông khác hoặc OCR Tr7 (chữ ẩn) làm chứng cùng kiểu với chữ đang thấy. Không che chữ bằng hình trắng/màu.

## 3. Trước ghi

Khóa đúng catalogue, kiểm mã nguồn và bản hiện hành. Lưu tọa độ vùng cho phép, số/model/đơn vị trước và sau, phương pháp và giới hạn. Tạo mẫu trước/sau cho việc phải duyệt. Chưa có trả lời bắt buộc thì tiếp tục phần độc lập, không làm phần phụ thuộc.

Mẫu được tạo mới trong hồ sơ riêng. Giữ mọi mẫu lỗi. Mỗi cách sửa PDF tối đa2 mẫu không đạt; khi hết giới hạn dừng cách đó, chuyển việc hoặc chuẩn bị phương pháp khác có căn cứ, không chỉ đổi tên tệp.

## 4. Nghiệm thu chính tệp đã lưu

**Cửa kiểm bắt buộc trước ký:** (a) So cạnh nhau cùng loại bơm của các hãng: khác rõ màu, nền đầu trang và cách trình bày, vẫn dễ đọc. (b) Mở từng biểu đồ Q–H của từng PDF: đường cong đều, không gợn/ngoằn nghèo/gãy; kèm kiểm toàn miền, sai lệch bảng ≤5% và khóa số. Ghi riêng hai kết quả trong phiếu QA với SHA, danh sách trang/biểu đồ, ảnh bằng chứng và người kiểm. C2/khớp số không thay nhìn hình; chưa đủ bằng chứng không ký đạt. Yêu cầu trực tiếp anh Trung06/10/2026.

1. Đọc lại đường dẫn và SHA-256 (mã kiểm nội dung), tránh kiểm nhầm RAM/tệp cũ.
2. `verify.structure_check`: trang/khổ đúng. Kiểm thêm raw Info/XMP (byte thông tin tài liệu), phông/chương trình phông, ảnh/mặt nạ, CTM (ma trận đặt ảnh), tài nguyên, liên kết, mục lục, trang không sửa. Kiểm cấu trúc đơn lẻ không đủ chứng tất cả đã giữ.
3. `verify.outside_pixels` và phép so ảnh riêng. Dùng đúng vùng/độ phân giải/ngưỡng/đệm đã khóa. Prompt gốc có ngưỡng48 cho ảnh quét; nhiều mẫu đã chọn kiểm nghiêm hơn200dpi/ngưỡng0/đệm0. Không chuyển về ngưỡng lỏng sau lỗi để tuyên bố đạt.
4. Đọc lại chữ/số, bảng, đường theo dữ liệu nguồn đúng và bộ số sửa đã chốt; kiểm cả ô không sửa và ô trống. Kiểm quan hệ Q tăng/H giảm trên toàn đường và các khóa; không chỉ so vài điểm kế hoạch. Tính theo từng đoạn trục thật.
5. Người kiểm đồ họa tự mở toàn trang ở150/200dpi và vùng sửa600dpi; nhìn đủ tên/đơn vị/lòng chữ/mép cắt/giao nét. Ảnh đẹp toàn trang không chứng một chữ nhỏ đúng. Kiểm ít nhất bản trước/sau thật.
6. Tách rõ ĐẠT số, ĐẠT hình thức, bảo toàn, CHƯA ĐẠT và CHƯA THỂ. Công thức/kiểm tự động khớp không thay việc nhìn chữ. Một tệp đã tạo không có nghĩa được nghiệm thu.

Khử răng cưa ở mép cắt có thể làm thay đổi ít pixel dù byte ảnh/CTM giữ nguyên. Ghi toàn crop và nội vùng riêng; không bỏ2 pixel mép rồi gọi toàn chữ đạt. Nếu nguyên liệu nguồn thiếu, giữ giới hạn “đúng theo ảnh nguồn” và “chưa biết phông/vector gốc”.

Ví dụ SL: 0 điểm đổi ngoài vùng, byte ảnh nguyên và lõi chữ không đổi chỉ chứng phần bảo toàn đã đo; 5 cụm vẫn lẫn đường cũ nên chưa đạt hình thức. 104 mốc/26 dấu vết hình học giữ từ M1 phải ghi là kiểm kế thừa theo mã tệp, không cộng thành nghiệm thu mới hoặc toàn mực nhìn thấy đã đúng.

Ghi riêng hộp nguồn, hộp cắt và phần giao; không đổi tên hộp nới thành hộp nguồn. Nới 0,48 pt từng được thử cho 4 vạch feet và vạch 0 ghép đáy của SL, không phải quy tắc nới chung cho chữ, nhãn hoặc ảnh. Tên ảnh có “KHONG DOI” không thay phép đo trên đúng hộp.

## 5. Tiếp nhận bản chính

Người điều phối đọc QA độc lập và bằng chứng của ứng viên. Kiểm lại nguồn/current/candidate SHA ngay trước nhận. Sao lưu bản chính hiện có nguyên byte vào hồ sơ riêng, kiểm mã bản sao, rồi tiếp nhận đúng byte ứng viên CATFIX đã đạt; không in/xuất PDF lại. Đọc lại bản chính và mã; lưu biên nhận trước/sau và vùng đã nghiệm thu.

Ghi báo cáo8 cột và sổ TIEN DO.md gốc. Đếm mã# duy nhất;#132 có nhiều nhóm vẫn một việc. Các phần mở rộng mới/đường chỉ giữ nguyên/điểm thiếu bảng không cộng thành đạt toàn bộ.

## 6. Khi bị ngắt

Lưu mốc: tệp hiện hành vàSHA, ứng viên/phương pháp đang dùng, số lần thử, đã/chưa đạt, quyết định đang chờ, người ghi, khóa và bước tiếp theo. Phiên mới chạy BƯỚC0, đọc sổ và tệp thật, tra vùng sửa trước khi tiếp tục. Không chạy lại chương trình publish (tiếp nhận) đã thành công: phần lớn có `fresh()`/guard để từ chối ghi đè.
