# REDPUMP 6SP30 (catalogue riêng, A4 dọc, 2 trang) — ứng viên 17A / 17B — 17/10/2026

Phiên CLAUDE_20261017T0850Z. Gốc vá: tệp anh gửi "6SP30-6 5.pdf" = deliverables/SP REDPUMP 6SP30 RIENG 20261007/REDPUMP 6SP30 - BAN 16 (hieu suat cac diem tren 65).pdf (mã kiểm ad416b37fb9b, đúng byte).
Cách làm: VÁ (QĐ 152), giữ khổ A4 dọc và trang 1 của bản 16. Mã dựng: build_6sp30_17.py.

| Ứng viên | Mã kiểm | Khác nhau |
|---|---|---|
| 17A | 5506fbe3cbab | Vật liệu 10 dòng đúng catalogue SP REDPUMP đã duyệt (tr.10, dải 6SP) |
| 17B | ba29a33c8174 | 17A + 4 dòng vật liệu lấy từ AQUARIS SP tr.21 (6SP30) + khối Applications / Operating conditions / Motor and pump / Options lấy từ REDPUMP SP tr.10 (bỏ dòng ISO 9906, QĐ 149) |

## Thay đổi
| Trang | Mục | Cũ → mới | Nguồn |
|---|---|---|---|
| 1 | Dòng cạnh tiêu đề | (không có) → "3~ 380–415 V 50 Hz / n ≈ 2850 /min / IP68 / Motor IE3" | lệnh anh 17/10 |
| 1 | Dòng điều kiện dưới bảng | (không có) → "Curves at 50 Hz, 2 poles, n ≈ 2850 /min, clean water at 20 °C, 1 mm²/s. Typical values, not guaranteed." | QĐ 149 (bắt buộc) |
| 2 | Bảng kích thước | MODEL/P/M/T + Pump/Motor/Total (kg) → MODEL/P/M/T (mm); số P/M/T giữ nguyên | QĐ 114 bỏ cân nặng |
| 2 | Ảnh sản phẩm | (không có) → KHO_ANH/Bom_gieng_SP/a1c9a2f70465.png (ảnh 6SP đang dùng ở REDPUMP SP tr.10), 245 pt cao, 203 ppi, bóng đổ dưới đế | KHO_ANH |
| 2 | Bảng vật liệu | (không có) → 10 dòng; hai dòng "Shaft" của nguồn ghi rõ "Pump shaft" (AISI 316 SS) và "Motor shaft" (AISI 304 SS-ASTM 5140) | REDPUMP SP tr.10 |
| 2 | Bảng Motor data | (không có) → 3~ 380–415 V 50 Hz; n ≈ 2850 /min; IP68; IE3; Ø 145 mm | lệnh anh + sơ đồ bản 16 |

## Kiểm tự động (tools/kiem_catalogue.py --goc bản 16 --trang 1,2 --khong-qh)
17A và 17B: ĐẠT 6 · CHƯA ĐẠT 0 · CHƯA THỂ XÁC MINH 0 · BỎ QUA 4 (Q–H không đổi; 3 hãng; DANH SACH). 17A còn vùng trống 32% trang 2 (có từ bản 16).

## Kiểm độc lập (một AI khác, 17/10)
Số P/M/T 9 model, vật liệu, trang 1 không đổi: ĐẠT. Đã sửa 2 điểm nó nêu: bóng dưới đế bị nền ảnh che (vẽ bóng sau ảnh); chữ "T" sát bảng vật liệu ở 17B (dời sơ đồ sang trái 10 pt).

## Chờ anh
1. Chọn 17A hay 17B.
2. Bản 16 không nằm trong 62 catalogue đã duyệt (QĐ 79: bản sửa riêng). Duyệt xong lưu ở đâu: theo lệnh anh.
