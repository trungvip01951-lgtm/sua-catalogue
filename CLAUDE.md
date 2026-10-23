# Sửa catalogue — chạy trên đám mây (Claude Code cloud)

Quy tắc dự án: kho/CLAUDE.md và kho/AGENTS.md. Tệp này chỉ ghi phần khác khi chạy trên đám mây; lệch với skill sua-catalogue thì theo tệp này (QĐ 23/10/2026, kho/claude/QUYET_DINH_ANH_20261023.md).

- Kho gốc: GitHub riêng tư trungvip01951-lgtm/sua-catalogue, thư mục kho/. Câu trong skill "không chép catalogue lên đám mây" đã hết hiệu lực từ 23/10/2026.
- Thư mục C:\Users\H2\Desktop\Catalog Sua là bản trùng (QĐ 23/10): không cần mount; sổ TIEN DO.md ở kho/CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/.
- Môi trường tự dựng khi mở phiên (.claude/hooks/session-start.sh): tesseract, qpdf, `$HOME/mnt/Sửa catalogue` → kho/, `claude/dau_phien.sh env`. Mọi lệnh trong skill và kho/CLAUDE.md dùng đường dẫn mount đó vẫn chạy được.
- Thư viện là bản mới (Python 3.13, PyMuPDF 2.0) vì wheels offline chỉ hợp Python 3.10; anh chấp nhận, khi nghiệm thu so PDF với bản dựng trên máy anh.
- Giữ .gitattributes `* -text`: bỏ thì Git đổi CRLF và lệch niêm phong.
- Làm xong: commit và push lên nhánh đang làm; container đám mây bị thu hồi, không push là mất.
