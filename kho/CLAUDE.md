# Claude — dự án Sửa catalogue

@AGENTS.md

Đọc và áp dụng đúng AGENTS.md ở trên (chung cho mọi AI). Thứ tự đọc đầu phiên: rules/QUY_TAC_HIEN_HANH.md → rules/HO_SO_HANG.md → rules/CHUAN_TRINH_BAY.md → claude/TRANG_THAI_CLAUDE.md.

Riêng Claude:
- Claude là người điều phối (QĐ 1): được ghi sổ TIEN DO.md và nhận bản chính sau nghiệm thu, theo đúng quy trình sao lưu và đọc lại mã kiểm.
- Kho trên máy anh truy cập qua máy ảo Linux: `$HOME/mnt/Sửa catalogue`. Môi trường: `bash claude/dau_phien.sh env` (cài offline từ vendor/wheels); `bash claude/dau_phien.sh test` (43/43) chỉ cần khi dùng catfix.
- Lệnh dự án: `$HOME/cfenv/bin/python -B -X utf8 claude/cat.py health|status|context|claim|check|heartbeat|release|receipt` (lớp dịch đường dẫn Windows → thư mục mount; công cụ gốc tools/catalogue.py không sửa).
- Mỗi lệnh shell ≤ 170 giây; tiến trình chạy nền bị dừng khi lệnh kết thúc; trong kho không xoá được bằng rm. Nháp để ngoài kho ($HOME/claude_work/<việc>).
- Cuối phiên: ghi đè mục 4 của claude/TRANG_THAI_CLAUDE.md và ghi bàn giao ngắn claude/BAN_GIAO_<UTC>.md (≤ 2 KB).
