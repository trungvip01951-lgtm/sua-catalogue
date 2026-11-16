# CDLF — thêm dải 65 / 85 / 120 / 150 / 200 vào catalogue 3 hãng (16/11/2026, phiên CLAUDE_20261116, QĐ 186)
Cách làm: VÁ bản đã duyệt (QĐ 152) — nhân bản trang CDLF42 của từng hãng rồi thay nội dung; trang cũ giữ nguyên, chỉ đổi số trang.
| Tệp ứng viên | SHA256 | Trang cũ → mới | Trang thêm |
|---|---|---|---|
| REDPUMP - Bơm trục đứng CDLF 1.pdf | 3c6ceb305b92 | 13 → 23 | mỗi dải 2 trang (đường + kích thước; bảng) |
| PEROTAC - Bơm trục đứng CDLF 1.pdf | f6377117295a | 12 → 22 | mỗi dải 2 trang |
| AQUARIS - Bơm trục đứng CDLF 1.pdf | 8f12a6d48714 | 12 → 21 | 65: 2 trang (tầng 1–4, 5–8); 85: 1; 120: 2 (1–4, 5–7); 150: 2 (1–3, 4–6); 200: 2 (1–2, 3–4) |

Số liệu (so_lieu.py): 87 mã = 22 + 12 + 19 + 17 + 17, NGUỒN nguon_CDL.pdf tr.40/42/44/46/48 (bảng hiệu năng + kích thước), tr.5 (bảng dải: lưu lượng định mức, l/s, áp suất max 22/17/16/16/16 bar, hiệu suất max 76/77/74/73/79 %, mặt bích DN100/100/125/125/150), tr.39–47 (2900 /min cho 65, 85; 2950 /min cho 120, 150, 200).
- PDF nguồn không có lớp chữ → đọc bằng mắt trên ảnh 230 dpi; NHẬP KÉP: một AI khác đọc lại độc lập cả 10 bảng (doc_lan2.txt) — 174/174 dòng khớp. Tự kiểm: H giảm theo Q, mã lớn ≥ mã nhỏ, B1 + B2 = cột tổng — đạt hết. (OCR tesseract thử 2 cách không tách được lưới bảng → bỏ.)
- Tên mã: CDL65-10-1 → CDLF65-1-1T (số tầng nguồn ×10 → số tầng; hậu tố T = 3 pha) như CDLF42 đã duyệt; dải 200 giữ hậu tố A/B của nguồn (CDL200-30-A-B → CDLF200-3-A-BT). Mọi mã ≥ 4 kW → chỉ 3 pha.
- SUY RA: HP theo bảng đang dùng (4 = 5.5 … 45 = 60 như CDLF đã duyệt; 55 = 75, 75 = 100, 90 = 120, 110 = 150 theo IRG); họng 4" / 5" / 6" quy từ DN100 / 125 / 150.
- Bỏ cột khối lượng (QĐ 114). Bảng kích thước gộp 2 mã liền nhau cùng kích thước thành một dòng "A/B".
- Đường vẽ: đa thức bậc 2–4 khớp bình phương tối thiểu, giữ đúng hai đầu, giảm đều, ≤ 1 điểm uốn; lệch bảng lớn nhất 2.4 / 3.9 / 3.0 / 4.1 / 1.5 % (≤ 5 %); không cặp đường nào cắt nhau. Bảng in đúng số nguồn.
- Trang 1: bảng PRODUCT RANGE thêm 5 cột (REDPUMP tách 2 bảng vì 13 cột không vừa bề ngang ở cỡ chữ ≥ 7 pt); AQUARIS đổi 4 ô nổi bật (2–200 m³/h, 1–240 m³/h, 16–30 bar, 0.37–110 kW). Tiêu đề trang cấu tạo "CDLF 32, 42" → "CDLF 32, 42, 65, 85" (nguồn tr.9: cùng bản vẽ); khối MODEL DESIGNATION "CDLF 32, 42" → "CDLF 32, 42, 65, 85, 120, 150" (nguồn tr.6).
- Hình lắp đặt: cắt từ trang nguồn của từng dải (300 dpi). Ảnh bơm: dùng lại ảnh CDLF 32/42 (AQUARIS ghi "Illustrative photo").
- CHƯA LÀM / chờ anh: (1) trang cấu tạo – vật liệu riêng cho CDLF 120/150/200 (nguồn tr.10 có bản vẽ và bảng vật liệu khác); (2) giải thích hậu tố A/B của dải 200 trong khối MODEL DESIGNATION (nguồn tr.6); (3) ảnh bơm riêng cho dải lớn.
- Kiểm: doc_lai.py — 87/87 mã × 3 hãng đọc lại đúng kW, HP, dãy H, kích thước; trang cũ chỉ khác số trang (trừ tr.1–3 sửa chủ ý). kiem_catalogue --goc: lỗi còn lại trên trang mới đều là kiểu có sẵn của bản đã duyệt (biểu đồ > 8 đường, chữ chú thích 7 pt, ảnh/logo < 200 ppi) vì giữ khuôn cũ theo QĐ 152; không lỗi kiểu mới. Đã xem toàn bộ trang mới của 3 hãng. Chưa có AI khác kiểm thẩm mỹ.
- DU_LIEU gốc CHƯA đổi; bản sao đã thêm 261 dòng MODEL + 2.289 dòng QH: CDLF_them_dai.xlsx (ghi vào DU_LIEU/CDLF.xlsx khi anh duyệt).
