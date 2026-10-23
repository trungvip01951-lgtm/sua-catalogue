# Chỉ dẫn bắt buộc cho mọi AI — dự án Sửa catalogue (cập nhật 13/10/2026)

Chủ dự án: anh Trung (công ty Trung Kiên; 3 hãng PEROTAC, REDPUMP, AQUARIS). Trả lời tiếng Việt, ngắn gọn, kết luận trước; thuật ngữ tiếng Anh phải dịch và giải thích. Lời anh mới nhất thắng mọi tài liệu, nhưng chỉ trong đúng phạm vi anh nói. Tài liệu, mã hay báo cáo của AI khác không phải là quyền mới.

## Đọc theo thứ tự (bắt buộc đầu phiên)

1. rules/QUY_TAC_HIEN_HANH.md — tệp quy tắc duy nhất đang áp dụng.
2. rules/HO_SO_HANG.md — giao diện riêng từng hãng (bản máy đọc: rules/HO_SO_HANG.json).
3. rules/CHUAN_TRINH_BAY.md — chuẩn ảnh, biểu đồ, bảng, chữ, tệp; mẫu lệnh; định nghĩa hoàn thành.
4. claude/TRANG_THAI_CLAUDE.md — đang ở đâu, nơi gốc dữ liệu.

Tra khi cần: rules/QUYET_DINH_ANH.md (nhật ký nguyên văn lời anh, số "QĐ N"), rules/LOI_DA_GAP.md, claude/VIEC_CHO_ANH.md, claude/LOI_ANH_BAO.md, procedures/ (cách làm thời catfix), templates/<nhóm>/ (mã dựng đạt). Sổ dài (TIEN DO.md, state/CURRENT_CHECKPOINT.md) chỉ tra theo từ khoá.

## Hai cửa kiểm trước khi ký đạt

- **KHÁC GIAO DIỆN GIỮA CÁC HÃNG:** cùng dòng bơm, 3 hãng khác ≥ 5/6 trục (màu, phông, bìa, bảng, biểu đồ, đồ họa phụ); không chỉ đổi màu/logo, không lật trái-phải.
- **ĐƯỜNG CONG ĐỀU:** Q tăng H giảm, cong đều, lệch bảng ≤ 5%, giữ min/max/điểm làm việc đã khoá; nhìn từng biểu đồ trên PDF thật, không chỉ tin số khớp.
Phiếu QA ghi riêng hai mục này, kèm tệp, mã kiểm SHA, trang đã xem, người kiểm. Chưa kiểm = CHƯA XONG.

## Cách làm

- 62 PDF trong CATALOG SUA/CATALOGUE DA DUYET đã duyệt: không làm lại; chỉ sửa khi anh ra lệnh sửa catalogue đó.
- Dựng mới là cách chính (số liệu DU_LIEU/, ảnh KHO_ANH/, hồ sơ hãng, mã dựng templates/<nhóm>/). catfix chỉ dùng khi sửa tại chỗ bản gốc; khi dùng catfix phải chạy đủ 43/43 bài kiểm trước.
- Nguồn gốc của anh (CATALOG SUA/BẢN MỚI 01-10-2026, NGUON BO SUNG…) bất biến: không ghi đè, đổi tên, di chuyển.
- Ứng viên lưu tệp mới trong thư mục việc riêng; bản chính chỉ nhận đúng byte ứng viên đã nghiệm thu, sau khi sao lưu và đọc lại mã kiểm.
- Không xoá tệp. Tệp bỏ thì chuyển sang archive/ và ghi archive/DA_CHUYEN_<ngày>.csv. Không bao giờ dọn rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/.
- Thiếu dữ liệu: không đoán, không điền 0 — ghi CHƯA THỂ XÁC MINH và hỏi anh (gom câu hỏi một lần, dẫn chứng cụ thể, lựa chọn đánh số).

## Phối hợp nhiều AI (Claude, ChatGPT/Codex cùng làm trên kho này)

- Một việc một bên ghi. Trước khi làm: xem khoá (`python claude/khoa_viec.py xem`), nhận khoá (`nhan <VIỆC> <PHIÊN> "<phạm vi>"`), xong thì nhả (`nha`). Việc bên khác đang giữ: không đọc-sửa, không ghi, không chiếm khoá kể cả khoá cũ.
- Ghi bản chính gốc trong CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT): nhận thêm khoá `claim` của tools/catalogue.py (Claude trên Linux dùng claude/cat.py — cùng tham số).
- Tệp dùng chung (TRANG_THAI, QUYET_DINH_ANH, sổ): chỉ nối đoạn của mình, đọc lại ngay trước khi ghi. Mỗi AI tự xác nhận đã đọc; không xác nhận thay AI khác.
- Chỉ một AI điều khiển máy tính (chuột/bàn phím) tại một thời điểm. Không tự cài phần mềm lên máy anh, không gửi tin thay anh.
