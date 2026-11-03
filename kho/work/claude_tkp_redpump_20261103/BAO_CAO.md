# REDPUMP TKP600 / TKP800 — catalogue bơm tăng áp (03/11/2026, phiên CLAUDE_20261103T0100Z)
Lệnh anh (QĐ 171–172): báo giá bao_gia_TKP.png — TKP600 2 m³/h, 20 m, 0.4 kW 1 pha 220 V; TKP800 3 m³/h, 20 m, 0.6 kW 1 pha 220 V. Ảnh SWIRLS anh gửi: xoá logo thân + xoá cả tem ("ảnh đại diện thì xóa tem đi cho a cũng đc k cần thông số"), thay chữ REDPUMP.
- Ảnh: anh_tkp_redpump.png 600×600 (logo thân: inpaint OpenCV + chữ REDPUMP Liberation Sans Bold; tem: tô màu nền khung 54/49/49 + nhiễu nhẹ). Còn tem "200" trên hộp tụ — giữ (không phải thương hiệu).

## Bản 1 (03/11/2026) — QĐ 173
Tệp: REDPUMP - Bơm tăng áp TKP 1.pdf — 1 trang A4 ngang, SHA256 fee5ea6c40f4…, 398665 byte. Giao diện REDPUMP (cột tối trái, đường đỏ/xám, trục H phải, Liberation Sans).
| Model | Hmax (Q=0) | Điểm làm việc | Qmax (H=0) | P2 | HP |
|---|---|---|---|---|---|
| TKP600 | 40 m NGUỒN | 2 m³/h – 20 m NGUỒN | 3 m³/h NGUỒN | 0.4 kW NGUỒN | 0.54 SUY RA (kW/0.746) |
| TKP800 | 55 m NGUỒN | 3 m³/h – 20 m NGUỒN | 4 m³/h NGUỒN | 0.6 kW NGUỒN | 0.8 SUY RA |
- Mức Q giữa (bước 0.5) SUY RA: parabol H = Hmax − b·Q − c·Q² đi đúng 3 điểm nguồn (TKP600 b = c = 3.3333; TKP800 b 5.4167, c 2.0833) — công thức từng ô trong TKP.xlsx/QH.
- Điện "1~ 220–240 V 50 Hz" theo quy tắc ghi điện (báo giá 220 V). Khối điều kiện bỏ "2 poles (≈ 2900 min⁻¹)" (chưa có nguồn số cực/tốc độ) bằng HO_SO_TKP.json (bản sao hồ sơ chỉ đổi câu này).
- Không ghi vật liệu, kích thước, dòng điện, số cực, tốc độ, tự mồi, bảo vệ nhiệt (chưa có nguồn TKP600/800; tem trong ảnh là TKP200 của SWIRLS). Chữ APPLICATIONS viết mới (công dụng bơm tăng áp, không có số).
- Ảnh 600 px đặt 144 pt = 300 ppi.
- Kiểm: kiem_catalogue ĐẠT 8/8 (bỏ qua 2); ve_duong_cong ĐẠT (biểu đồ, bảng); xem PDF: nhãn điểm làm việc không đè. Chưa kiểm độc lập bằng AI khác.
