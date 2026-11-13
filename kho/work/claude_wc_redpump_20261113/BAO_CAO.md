# REDPUMP WC 150WC / 200WC 37–132 kW — catalogue riêng 14 mã, bản EN + VI (13/11/2026, phiên CLAUDE_20261113)
Lệnh anh: QĐ 174 (14 mã, thứ tự anh đưa), QĐ 175 (bản tiếng Việt).
Tệp: REDPUMP - Bơm cắt rác WC 150WC-200WC 37-132kW 1.pdf (SHA256 91d17d07f400…), … tiếng Việt 1.pdf (SHA256 a063f97e587b…); 4 trang A4 ngang, giao diện REDPUMP.
Tr.1 tổng quan + bảng 14 mã đúng thứ tự anh; tr.2 150WC (2 biểu đồ nhóm A/B + bảng); tr.3 200WC; tr.4 vật liệu, ứng dụng, điều kiện.
- NGUỒN lời anh: Qmax, Hmax, kW. Điểm định mức Q–H: tên model (quy ước mã WC).
- H tại Qmax = nấc công suất trong cỡ họng (QĐ 19), nối tiếp dải REDPUMP đã duyệt: 150WC 37→8 m … 132→14 m; 200WC 37→5 m … 132→11 m (tiền lệ 150WC300-30-37, 200WC450-32-55). kiem_catalogue đếm nấc trong riêng tệp (1…7) nên báo CHƯA ĐẠT mục QĐ 19 — giữ theo dải, chờ anh.
- SUY RA: mức Q giữa: H = Hmin + (Hmax − Hmin)(1 − (Q/Qmax)^n) qua điểm định mức; 200WC350-22-37 điểm định mức nằm dưới dây cung → parabol lồi (giống dáng bảng WC đã duyệt). HP theo DU_LIEU/IRG.xlsx (90 kW = 120 HP, 132 kW = 176 HP). 2 cực n≈2900 (150WC), 4 cực n≈1450 (200WC) theo dải.
- Số liệu anh đưa làm đường cắt nhau: 200WC350-22-37 (37 kW) cao hơn 200WC300-32-45 (45 kW) khi Q > ~560 m³/h; 150WC180-80-110 và 150WC200-90-132 hết ở 300 m³/h trong khi 37–90 kW tới 350 m³/h — trái quy tắc 06/10 "công suất lớn phải trội hơn" ở cuối dải; giữ đúng số anh, chờ anh.
- Chữ EN: REDPUMP - Bơm cắt rác WC.pdf đã duyệt tr.5 (bỏ ISO 9906 QĐ 149, bỏ dòng 1 pha). VI: dịch (bảng VI trong build_wcl.py). Ảnh 51c00456604c (150WC, 458 ppi), d78acefb2b87 (200WC, 450 ppi).
- Kiểm: ve_duong_cong ĐẠT 8 biểu đồ + 2 bảng. kiem_catalogue EN ĐẠT 7, CHƯA ĐẠT 1 (QĐ 19 như trên); VI ĐẠT 6, CHƯA ĐẠT 2 (QĐ 19 + "có chữ tiếng Việt" — anh yêu cầu bản VI). Xem PDF 4 trang mỗi bản: nhãn không đè. Chưa kiểm độc lập bằng AI khác.

## Bản 2 (13/11/2026) — QĐ 176–178
Tệp: … 37-132kW 2.pdf (SHA256 c3621cb384c0…), … tiếng Việt 2.pdf (SHA256 0d799d2cfca5…).
- Cột "Rated point" đổi thành "Duty point / Điểm làm việc" = số trong mã model; kiểm bằng mã: 14/14 mã có H đúng tại Q làm việc trong bảng.
- 200WC400-75-132: 0/105, 400/75 (điểm làm việc theo mã), 600/5 (catalogue anh) — n = 2.969; bảng 0/105, 100/104.5, 200/101.2, 300/92.2, 350/84.8, 400/75, 500/46.8, 600/5. Khác catalogue anh tại 300 (anh 80 → 92.2) và 400 (anh 60.6 → 75) vì QĐ 177.
- H tại Qmax của 200WC400-75-132 = 5 m (catalogue anh) trong khi 200WC300-65-110 = 10 m (nấc QĐ 19) — chờ anh chốt câu nấc.
- Ảnh: anh_wc_132kw.jpeg (từ catalogue anh) 328 ppi; bỏ 2 ảnh cũ.
- Kiểm: ve_duong_cong ĐẠT 8 + 2; kiem_catalogue EN ĐẠT 7 / CHƯA ĐẠT 1 (QĐ 19), VI ĐẠT 6 / CHƯA ĐẠT 2 (QĐ 19 + chữ Việt theo lệnh anh). Xem PDF tr.1, 3, 4. Chưa kiểm độc lập.

## Bản 3 (13/11/2026) — QĐ 179
Tệp: … 37-132kW 3.pdf (SHA256 f173b7fe90a2…), … tiếng Việt 3.pdf (SHA256 7a0c15cc7074…).
- H tại Qmax: 200WC 5 m, 150WC 10 m (cả 14 mã, kiểm bằng mã: 0 lệch). Điểm làm việc theo mã: 14/14 khớp. Đường giữa SUY RA cùng công thức (n mới trong WCL.xlsx).
- Kiểm: ve_duong_cong ĐẠT 8 + 2; kiem_catalogue chỉ còn mục QĐ 19 (công cụ đòi nấc 1…7 — anh đã chốt QĐ 179) và chữ Việt ở bản VI (lệnh anh QĐ 175). Xem PDF tr.2, 3. Chưa kiểm độc lập.
