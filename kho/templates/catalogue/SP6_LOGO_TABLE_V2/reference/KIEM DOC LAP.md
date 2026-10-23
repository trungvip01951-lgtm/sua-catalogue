# Kiểm độc lập LOGO và BẢNG SP6

Kết luận: **PASS phạm vi mới logo, bảng, ký hiệu n≈2850. Toàn trang vẫn FAIL cũ tại nhãn đồ thị; không nghiệm thu toàn trang.**

Thời điểm 2026-10-06T10:09:35. Tệp đã mở: D:\ChatGPT\Sửa catalogue\deliverables\SP6 LOGO BANG RO QH 20261006\SP DU 12 TRANG - LOGO VA BANG MOI.pdf
SHA-256: 7b20403444ef5b97ae1f4da15a39e3affa64cb14206063da05e6114ad0208d05.
Bản nền: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\SP6 THIET KE MOI VECTOR PILOT 20261006\UNG VIEN 2\Perotac bơm giếng SP_compressed (bản mới).pdf, SHA 8f1a2edc65aad20ab5f0d41b1c4980e85cd7617193a868ac2e98ad05cac7c583.
Chỉ đọc; không sửa PDF, không UI; không kiểm lại lỗi đồ thị cũ.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| LOGO-01 | SP6 mới | 6 | Logo nền xanh trong bản2 | Logo Perotac nền trắng, rõ, không mép nền khác màu | Kiểm độc lập PDF và LOGO.png | ĐẠT / PASS | Raster1041×356 so RGB với xref200 PDF WC nguồn: [True]; nhìn logo và chữ MADE IN TAIWAN đủ, không bị cắt |
| TABLE-01 | SP6 mới | 6 | Header bảng gọn, thiếu P2 | MODEL/P₂/DELIVERY, điện1~/3~, kW/HP, Qm³/h và l/min tách hai hàng; H(m) rõ | Mở BANG TRAI.png/BANG PHAI.png và đọc chữ thật PDF | ĐẠT / PASS | Ô tách rõ, không thấy chồng chữ/đường trong bảng;39 dòng giữ đủ |
| NUM-01 | SP6 mới | 6 | Bộ khóa39 dòng426H | 426H và model/kW/HP đúng từng ô | Đọc vị trí chữ trong PDF, đối chiếu bộ khóa nguyên | ĐẠT / PASS | Số ô H:426; lỗi đối chiếu:0 |
| HEADER-01 | SP6 mới | 6 | n=2850 | n≈2850;50Hz giữ | Đọc PDF thật và nhìn header | ĐẠT / PASS | Chuỗi n ≈ 2850 có trong PDF; P₂ hiện rõ ở hai bảng |
| HOLD-01 | SP6 mới | 6 và ngoài6 | Plot bản2 đang FAIL nhãn | Plot giữ nguyên | Render so byte RGB200dpi vùng(0,47,831.56,354);11trang khác so72dpi | ĐẠT bảo toàn phạm vi / PASS | Plot bằng byte:True;11trang khác bằng byte:True; không sửa số/công suất/thứ tự |

Giới hạn: chỉ nghiệm thu thay đổi mới. Lỗi nhãn đồ thị từ bản2 giữ FAIL/STOP2, chưa xử lý. Bản in giấy chưa kiểm. Nhận xét công suất bất thường dành lượt riêng, không sửa số từ suy đoán. Quy tắc đường khớp ≥95% và giữ điểm làm việc/max cần định nghĩa phép đo ở lượt kỹ thuật riêng; lần này đường không đổi, không nhận đã giải quyết toàn bộ.

Agent session 01a10f1c-5cf7-7942-8a3d-71edcbca5572; log C:\Users\H2\.codex\sessions\2026\10\06\rollout-2026-10-06T09-47-59-01a10f1c-5cf7-7942-8a3d-71edcbca5572.jsonl.
