# Bộ kiểm phông gần nhất ngày 06/10/2026

Quyền trực tiếp của anh đã được ghi tại QUYET_DINH_MOI_PHONG_GAN_NHAT_DWO_MINMAX_20261006.md. Không hỏi lại quyền này hoặc 14 số min DWO.

Bộ kiểm tại `D:/ChatGPT/Sửa catalogue/deliverables/BAN GIAO KIEM 25 CATALOGUE 20261006T012858Z`; ZIP có đúng 25 catalogue, 7 PDF sửa chữ và DWO mới, 17 bản chính nguyên byte. Chưa tiếp nhận bản chính, 137/149 gốc giữ đến nhận; bản bàn giao mới `BAN_GIAO_BO_KIEM_20261006T013010Z.md`.

Các chữ đạt kiểm nội bộ có thể dùng nét gần từ tệp (Ó ghép O+dấu sắc, W chỉnh ma trận) hoặc Arial hiện có cho SA; không cài phông. Kết luận cần cả từ, toàn trang và kiểm tài nguyên/ngoài vùng, không lấy diện tích nét hoặc ảnh nhỏ chứng cùng phông. W nghiêng CM mẫu1 quá mảnh; mẫu2 mới được chọn sau kiểm ảnh 600dpi và toàn trang, giữ giới hạn hạt ảnh nguồn.

FS nhỏ G06: vá cục bộ đã dùng 2/2, mẫu cuối 627766ec còn nền/viền/hạt và 24 điểm ảnh ngoài vùng. DỪNG cách đó, giữ bản chính 97db4410; không mẫu3 hoặc nới vùng/đệm/ngưỡng. Thay toàn ảnh Flate trước đó thất bại và bỏ. Các cách trước/sau phải được phân biệt bằng thay đổi thực chất, không bằng tên.

CDLF Aquaris: ánh xạ lịch sử đã đảo tên 2/4, chỉ phát hiện khi xoay ảnh chữ đúng hướng. Mẫu2 có cấu trúc/ngoài vùng đạt vẫn sai nội dung, không nhận. Hai mẫu đã dùng, DỪNG; giữ 119b2618. CDLF Perotac còn mép1pixel ngoài vùng và nét/số donor lệch sau mẫu2, DỪNG; giữ 72f45237. Không dùng các ứng viên đó vào bộ25, không tái dùng phiếu ánh xạ cũ như nguồn số đúng.

Catfix pikepdf save có thể chuẩn hóa XML thông tin XMP. Cách bảo toàn đã có trong g13_publish_precise.py: catfix.vector.Editor(ứngviên, backend='fitz'), doc.set_stream(Ref((xref,0)), bytes XML đã đọc gốc), E.save(tệp mới), E.close. Không gọi backend.save ngoài catfix hoặc sửa công cụ. Phải kiểm mọi pixel vùng rỗng và tài nguyên sau nhánh bảo toàn. XML decoded nguyên byte không có nghĩa RAW encoded/mã hóa luồng XMP giữ; CMRedpump đổi none sang Flate, ghi riêng. Ảnh/mặt nạ/chương trình phông gốc được kiểm RAW riêng.

DWO ứng viên1 0d375ba9: bảy đường tham khảo/455điểm đúng min/max và Q tăng H giảm; công thức/caches và các phần giữ qua kiểm độc lập. Helpers U:AH **không ẩn**: nhận định plotVisOnly=1 làm trống biểu đồ là giả định đã đính chính, không tạo mẫu2 vì nhận định đó. Không tự ẩn helpers rồi quên đổi plotVisOnly cho phép ô ẩn. Bản in/hình Excel chưa nghiệm thu; PNG từ bộ đọc bỏ nhãnseries/3ảnh, không dùng làm chứng bản in.

Nguồn/bản chính 25 tệp giữ. CM38 và hai mã bổ sung đã đạt trước phiên, giữ; không thêm trùng. Các STOP2 SP/SL trước phiên không được mở lại chỉ vì anh cho đổi chữ gần nhất.
