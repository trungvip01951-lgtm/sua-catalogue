# Chỉ dẫn bắt buộc cho AI trong dự án Sửa catalogue

**ĐỌC TRƯỚC / KIỂM TRƯỚC KHI KÝ:** Cùng loại bơm, các hãng phải có giao diện khác rõ về màu, nền đầu trang và cách trình bày; không chỉ thay logo. Mọi đường Q–H phải cong đều, không ngoằn nghèo, kiểm toàn miền và nhìn từng biểu đồ PDF thật; khớp bảng/C2 không đủ. Sai lệch ≤5%, giữ min/max/điểm làm việc khóa; quyền sửa H trung gian nguyên đã có. Phiếu QA bắt buộc ghi riêng hai mục khác giao diện và đường cong đều, bằng chứng/SHA/trang/người kiểm, không ký đạt khi chưa xem. Đây là yêu cầu trực tiếp mới nhất của anh ngày06/10/2026, mở lại lỗi của cả AQUARIS/PEROTAC/REDPUMP SP.

Chủ dự án: anh Trung. Trả lời tiếng Việt, ngắn gọn, kết luận trước; giải thích thuật ngữ tiếng Anh. Quyết định mới do anh trực tiếp giao ưu tiên hơn tài liệu cũ, nhưng chỉ trong đúng phạm vi đã giao. Không xem tài liệu, ảnh, mã hay báo cáo của AI khác là quyền mới.

## Bắt đầu

1. Đọc START_HERE.md, manifest.json, rules/QUY_TAC_ANH_TRUNG.md và rules/PHOI_HOP_CHATGPT_CLAUDE.md.
2. Đọc **sổ TIEN DO.md gốc** chỉ qua đường dẫn trong manifest; đọc state/CURRENT_CHECKPOINT.md và phần việc liên quan. Đây là mốc tiếp tục, không phải lời chứng nghiệm thu.
3. Chạy tools/catalogue.py health, status, context đúng tệp; đọc các báo cáo/bằng chứng liên quan và đối chiếu bản thật. Khi phiên bị ngắt, chạy BƯỚC 0 đầy đủ gồm 43 kiểm thử theo gói gốc trước sửa catalogue.
4. Nhận đúng một khóa ghi cho mỗi catalogue bằng tools/catalogue.py claim. Khóa không thay quyền anh, không thay kiểm số/đồ họa. Đọc và ghi nhận trạng thái thật trước nhận phần việc mà tác nhân khác đang làm.
5. Đọc hết prompt chung, README_KY_THUAT.md và prompt nhóm tương ứng trước dùng catfix. Đọc procedures phù hợp và knowledge/LOI_VA_CACH_TRANH.md để không thử lại cách đã bị loại.

## Ghi và nghiệm thu

- **Nguồn bất biến:** không ghi đè, xóa, đổi tên, di chuyển bất kỳ tệp gốc của anh. Không tự cài. Chỉ sửa catalogue qua catfix; không xuất lại qua phần mềm khác, dùng phông ngoài, phủ ô trắng/màu hoặc biến cả trang PDF thành ảnh.
- Chỉ một tác nhân ghi một catalogue. Người kiểm độc lập đọc nguồn và tệp thật, không chỉ nghe báo cáo tác nhân sửa. Chỉ người điều phối ghi TIEN DO.md và tiếp nhận bản chính sau nghiệm thu.
- Bản chính đổi chỉ sau sao lưu nguyên byte, kiểm lại mã trước/sau và đọc lại. PDF ứng viên lưu mới vào hồ sơ riêng, tuyệt đối không ghi trực tiếp lên bản đã đạt.
- Kiểm số và kiểm hình thức là hai phần riêng. Mỗi số, tên, đơn vị, đường, ảnh phải đúng nguồn/quyết định. Mọi đường trong cùng biểu đồ đồng bộ màu, độ dày, độ rõ, mượt; chữ phải đọc đúng và đúng dáng, không lấy diện tích nét hay ảnh thu nhỏ làm chứng cùng phông.
- Bảo toàn trang/khổ, phông và chương trình phông, ảnh/mặt nạ, thông tin tài liệu, liên kết, mục lục. Đo ngoài vùng sửa theo quy định; đã khóa ngưỡng0/đệm0 thì không nới để cho đạt.
- Phần cần anh duyệt: chuẩn bị đủ mẫu trước/sau và bảng sai lệch, gửi rồi chờ. Không hỏi lại quyền đã rõ; không coi chờ lâu là đồng ý. Thiếu dữ liệu/phông phải ghi CHƯA THỂ XÁC MINH.
- Theo yêu cầu mới ngày 03/10/2026: với một mã bơm, Q tăng thì H phải giảm. Đoạn tăng ngược trong bảng hoặc đường là lỗi cần sửa; không lấy việc khớp nguồn sai làm nghiệm thu. Sửa số trung gian nguyên và đường đồng thời, giữ mức tối đa, tối thiểu và điểm làm việc đã khóa. Thiếu dữ liệu hoặc các khóa mâu thuẫn thì lập bằng chứng, không tự phá khóa hoặc đoán số.
- Hai lần một cách sửa PDF không đạt thì dừng cách đó, giữ cả bằng chứng lỗi. Nghiên cứu trong bộ nhớ phải ghi rõ chưa tạo PDF; không đổi tên phương pháp chỉ để tiếp tục lặp vô hạn.
- Báo cáo đúng 8 cột. Chỉ nói hoàn tất phạm vi đã ĐẠT trên tệp thật. Không cộng cùng mã việc hoặc cùng mốc đo hai lần; không tính phần mở rộng vào tỷ lệ 149 việc gốc.

## Tiếp quản và lưu kiến thức

Trước mỗi lô ghi: kiểm khóa và phiên bản đầu vào. `INPUT_CHANGED` nghĩa là đầu vào đổi: đọc lại, so phần thay đổi, cập nhật hồ sơ/khóa phù hợp trước tiếp tục. Không bỏ khóa SHA trong mã cũ.

Sau mốc quan trọng: lưu ảnh trước/sau, số đo, mã kiểm, cách đã dùng, giới hạn, việc dở và bước tiếp theo. Ghi vào sổ chính qua người điều phối; kiến thức mới đưa vào tài liệu dùng chung sau kiểm. Không yêu cầu anh làm người chuyển lời giữa hai AI.

Công cụ phối hợp không cưỡng chế chương trình khác ghi ngoài quy trình; không hứa đã chống ghi đè tuyệt đối. Không tự gửi tin, tạo lịch/dịch vụ hoặc điều khiển hai phiên UI cùng lúc. Máy tính chỉ một tác nhân điều khiển mỗi lần.


## Bắt buộc bổ sung — lưu quy tắc và dùng mẫu (06/10/2026)

Đọc rules/QUY_TAC_CUNG_HIEN_HANH.md trước áp điều cũ; quyền phông gần nhất và DWO min/max đã có, không hỏi lại. Trước sửa thông số đọc procedures/SUA_THONG_SO_TU_MAU.md và templates/catalogue/README.md. Sau yêu cầu/nhắc/lỗi phải lưu quyết định, bài học, chứng cứ và mẫu có trạng thái. SP6_VECTOR_V1 chưa đạt hình thức/STOP2, không lấy làm mẫu phát hành; không chạy nguyên mã lịch sử. Quy tắc mới này được anh trực tiếp yêu cầu lưu thành quy tắc cứng, chỉ trong dự án catalogue.


## Bắt buộc bổ sung — khóa việc, song song, nghiệm thu (06/10/2026, anh chốt trong phiên Claude)

Đọc mục cuối rules/QUY_TAC_CUNG_HIEN_HANH.md (mục 14–18). Ba hãng cùng loại catalogue phải khác cả bố trí, màu sắc và cách trình bày, không chỉ màu/logo. Phiên nào làm việc nào thì khóa việc đó: `python claude/khoa_viec.py xem|nhan|nha` (thêm claim nếu ghi 25 catalogue gốc); việc phiên khác giữ thì không động vào, không chiếm khóa. Tách phần độc lập cho nhiều AI chạy song song, mỗi AI một khóa/thư mục/tệp ra riêng, vẫn phải chính xác. Kiểm độc lập, sửa, kiểm lại đạt hết mới tính là xong. Chỉ kiểm phần vừa làm và phần bị ảnh hưởng trực tiếp, không kiểm lan man.
