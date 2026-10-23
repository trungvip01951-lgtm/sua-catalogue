# Mẫu SP ba hãng — dùng lại theo phạm vi

Đọc manifest.json và state/CURRENT_CHECKPOINT.md trước sửa. Không chạy lại mã lịch sử chứa token/SHA cũ.

- **AQUARIS: ĐẠT kiểm số/hình thức độc lập, đã nhận bản chính.** Dùng đúng PDF SHA 9b2ca1ba4c429fc098f0f354884b0ce2eeb1f20c4b4994dd9e4f0aefd8ba214e, 31 trang, 197 model, 1.179 điểm H. Sau này chỉ sửa phần cần sửa; không chạy lại phương pháp thay panel theo vùng đã STOP2. Ảnh sản phẩm vẫn giới hạn độ phân giải nguồn. Chưa kiểm in giấy.
- **PEROTAC/REDPUMP: CHƯA TẠO PDF mới.** Đủ dữ liệu 220 dòng/2.218 H, 219 dòng kích thước đã kiểm độc lập, bố cục vector/nhãn/ảnh xem trước. Phương án 13 trang và 4SP14-4 là CÓ ĐIỀU KIỆN, chờ anh chốt; không coi là bản đã nghiệm thu.
- Quyết định bỏ 4SP2 áp cả ba hãng, giữ 3SP2. Redpump dùng bộ Perotac. Aquaris giữ nguồn riêng.
- Phải nhận khóa mới, cập nhật perotac_writer/active_lock.json đúng actor/session/token, kiểm đầu vào trước lưu PDF. Phương pháp mới chỉ sửa đường/table/nhãn bị ảnh hưởng. Không hạ ngưỡng/đệm0 hoặc tự mở lại cách STOP2.
- Dữ liệu/mã/nhãn/bằng chứng được giữ trong work/sp_three_brands và khóa SHA tại manifest thư viện. Mã dựng dùng catfix; SVG/PNG chỉ là mẫu xem trước, không thay PDF thật/QA sau lưu.


Mốc trên là lịch sử. Mẫu hiện hành đã đạt cả ba hãng: [SP_THREE_BRANDS_V2_20261006](../SP_THREE_BRANDS_V2_20261006/README.md). Ba quyết định đã được anh chốt, không hỏi lại.
