# Claude — dự án Sửa catalogue

**Đọc trước khi làm và trước khi ký QA:** anh Trung yêu cầu cùng loại bơm nhưng khác hãng phải khác rõ giao diện (màu, nền đầu trang, cách trình bày). Mọi đường Q–H phải cong đều, không ngoằn nghèo; phải kiểm số toàn miền và nhìn từng biểu đồ PDF thật, không chỉ C2/khớp bảng. Sai lệch bảng≤5%, giữ min/max/duty khóa. Phiếu QA bắt buộc có hai mục KHÁC GIAO DIỆN GIỮA CÁC HÃNG / ĐƯỜNG CONG ĐỀU và bằng chứng trước ký. SP hiện hành là mẫuV3 sau phản hồi06/10/2026; đọc START_HERE và sổ mới, không phát hành lạiV2.

@AGENTS.md

Đọc và áp dụng cùng bộ quy tắc của ChatGPT tại đây. Đây là nguồn chung trên máy anh Trung, không cần anh dán lại lịch sử cuộc trò chuyện.

Đọc START_HERE.md → manifest.json → rules/QUY_TAC_ANH_TRUNG.md → rules/PHOI_HOP_CHATGPT_CLAUDE.md → sổ TIEN DO.md **gốc** → state/CURRENT_CHECKPOINT.md → prompt nhóm và procedures đúng việc. Chạy lệnh health/status/context. Tự mở nguồn và bằng chứng thật.

Trước ghi, đối chiếu phân công hiện hành và nhận khóa chính chủ. Không chỉnh chung catalogue với tác nhân ChatGPT đang giữ; có thể kiểm độc lập hoặc nhận tệp khác. Không sửa catfix để qua kiểm thử, không đổi giấy phép Office hoặc tự cài.

Mỗi phiên tự ghi xác nhận đã đọc bằng lệnh receipt, nêu đúng phạm vi, số đã khóa, việc chưa xong và bước tiếp theo. Xác nhận này chỉ đại diện phiên Claude đã đọc; không xác nhận cho phiên ChatGPT hoặc cho mọi phiên tương lai.

Mã trong archive là lịch sử được bảo toàn, có cả cách thất bại. Chỉ dùng phiên được chọn trong bảng bài học/biên nhận hiện hành sau đối chiếu SHA; chạy mã ghi cũ phải giữ nguyên cơ chế chặn sai đầu vào và không ghi đè.


## Bắt buộc bổ sung — lưu quy tắc và dùng mẫu (06/10/2026)

Đọc rules/QUY_TAC_CUNG_HIEN_HANH.md trước áp điều cũ; quyền phông gần nhất và DWO min/max đã có, không hỏi lại. Trước sửa thông số đọc procedures/SUA_THONG_SO_TU_MAU.md và templates/catalogue/README.md. Sau yêu cầu/nhắc/lỗi phải lưu quyết định, bài học, chứng cứ và mẫu có trạng thái. SP6_VECTOR_V1 chưa đạt hình thức/STOP2, không lấy làm mẫu phát hành; không chạy nguyên mã lịch sử. Quy tắc mới này được anh trực tiếp yêu cầu lưu thành quy tắc cứng, chỉ trong dự án catalogue.
