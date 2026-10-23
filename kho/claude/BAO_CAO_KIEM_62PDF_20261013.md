Báo cáo tham khảo — anh đã chốt 13/10/2026 không làm lại catalogue cũ; chỉ dùng làm bài học và khi anh ra lệnh sửa catalogue đó

# Kiểm tự động 62 PDF đã duyệt (CATALOG SUA/CATALOGUE DA DUYET) — 13/10/2026

- Công cụ: `tools/kiem_catalogue.py` (bản 13/10/2026); mọi ngưỡng đọc từ `rules/HO_SO_HANG.json` phiên bản 2026.10.13.
- Lệnh: `python -B -X utf8 tools/kiem_catalogue.py "CATALOG SUA/CATALOGUE DA DUYET" --tu-ghep-bo3 --json <tệp>` (chạy 13/10/2026 16:01 UTC; 62 tệp ≈ 50 giây, chậm nhất 5.0 giây/tệp). Chỉ đọc PDF, không sửa gì.
- Ký hiệu: Đ = ĐẠT · ✗ = CHƯA ĐẠT · ? = CHƯA THỂ XÁC MINH (máy không đo được, không đoán) · – = BỎ QUA.
- Chuẩn 13/10 (chữ thân ≥9 pt, bảng ≥7 pt, ảnh ≥200 ppi/bìa ≥300, ≤8 đường/biểu đồ, A4, ≤10 MB, vùng trống ≤10%) là chuẩn cho bản MỚI; 62 bản cũ làm trước chuẩn nên nhiều ✗ là dự kiến.
- Mục 9 dùng ngưỡng giống 0,6 (HO_SO_HANG.json chung.nguong_giong_giao_dien) là ngưỡng ĐỀ XUẤT, chưa được anh duyệt. Mục 9 chỉ chạy cho nhóm đủ 3 hãng (FS AQUARIS ghép với FC PEROTAC/REDPUMP theo bảng "Phạm vi hãng").

## Tổng theo mục

| Mục | ĐẠT | CHƯA ĐẠT | CHƯA THỂ XÁC MINH | BỎ QUA |
|---|---|---|---|---|
| 1. Chữ cấm + 50 Hz | 56 | 6 | 0 | 0 |
| 2. Điện/pha | 29 | 16 | 17 | 0 |
| 3. Bảng | 39 | 0 | 9 | 14 |
| 4. Đường | 12 | 27 | 9 | 14 |
| 5. Chữ | 1 | 61 | 0 | 0 |
| 6. Ảnh | 19 | 43 | 0 | 0 |
| 7. Tương phản | 42 | 20 | 0 | 0 |
| 8. Tệp | 18 | 44 | 0 | 0 |
| 9. Khác 3 hãng | 15 | 42 | 0 | 5 |
| 10. Mã kiểm | 62 | 0 | 0 | 0 |

## Bảng tổng: tệp × 10 mục

| Tệp | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| AQUARIS - Bơm chìm nước thải FS inox | ✗ | Đ | Đ | Đ | ✗ | Đ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm chìm nước thải FS | Đ | ✗ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm chìm nước thải KTZ-LH | Đ | ✗ | ? | ✗ | ✗ | ✗ | ✗ | ✗ | Đ | Đ |
| AQUARIS - Bơm chìm nước thải SS | Đ | Đ | Đ | ✗ | ✗ | Đ | ✗ | Đ | ✗ | Đ |
| AQUARIS - Bơm cắt rác WC | Đ | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm giếng SA | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm giếng SP | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục ngang 2CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục ngang 3M | Đ | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục ngang CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục ngang CM | Đ | ✗ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục ngang DWO (bản 1 trang) | Đ | ✗ | Đ | ✗ | ✗ | Đ | ✗ | Đ | ✗ | Đ |
| AQUARIS - Bơm trục ngang DWO (bản 2 trang) | Đ | ✗ | Đ | ✗ | ✗ | ✗ | ✗ | Đ | ✗ | Đ |
| AQUARIS - Bơm trục ngang MHI | Đ | ? | ? | ? | ✗ | ✗ | ✗ | ✗ | Đ | Đ |
| AQUARIS - Bơm trục đứng CDLF | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| AQUARIS - Bơm trục đứng IRG | Đ | ? | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| AQUARIS - Bơm định lượng JLM-JBB | ✗ | ? | – | – | ✗ | ✗ | Đ | ✗ | – | Đ |
| AQUARIS - Máy khuấy chìm 4MIX | Đ | ? | – | – | ✗ | Đ | Đ | Đ | Đ | Đ |
| AQUARIS - Máy khuấy chìm MIX | Đ | ? | – | – | ✗ | Đ | Đ | Đ | Đ | Đ |
| AQUARIS - Máy thổi khí con sò GB | Đ | ✗ | – | – | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm chìm nước thải FC inox | ✗ | Đ | Đ | Đ | ✗ | Đ | Đ | Đ | ✗ | Đ |
| PEROTAC - Bơm chìm nước thải FC | Đ | ✗ | Đ | Đ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm chìm nước thải KTZ-LH | Đ | ✗ | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| PEROTAC - Bơm chìm nước thải SS | Đ | Đ | Đ | ✗ | ✗ | Đ | Đ | Đ | ✗ | Đ |
| PEROTAC - Bơm cắt rác WC | Đ | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| PEROTAC - Bơm giếng SA | Đ | Đ | Đ | ✗ | ✗ | Đ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm giếng SP | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục ngang 2CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục ngang 3M | Đ | Đ | Đ | Đ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục ngang CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục ngang CM | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục ngang DWO (bản 1 trang) | Đ | ✗ | Đ | ✗ | ✗ | ✗ | Đ | Đ | ✗ | Đ |
| PEROTAC - Bơm trục ngang DWO (bản 2 trang) | Đ | ✗ | Đ | ✗ | ✗ | ✗ | Đ | Đ | ✗ | Đ |
| PEROTAC - Bơm trục ngang MHI | Đ | ? | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| PEROTAC - Bơm trục đứng CDLF | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Bơm trục đứng IRG | Đ | ? | ? | ? | ✗ | ✗ | ✗ | ✗ | Đ | Đ |
| PEROTAC - Máy khuấy chìm 4MIX | Đ | ? | – | – | ✗ | Đ | Đ | Đ | Đ | Đ |
| PEROTAC - Máy khuấy chìm MIX | Đ | ? | – | – | ✗ | Đ | Đ | Đ | Đ | Đ |
| PEROTAC - Máy thổi khí Root RL | ✗ | ? | – | – | ✗ | ✗ | ✗ | ✗ | – | Đ |
| PEROTAC - Máy thổi khí con sò GB | Đ | ✗ | – | – | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| PEROTAC - Đĩa phân phối khí DN270-DN128 | Đ | ? | – | – | ✗ | Đ | Đ | Đ | – | Đ |
| REDPUMP - Bơm chìm nước thải FC inox | ✗ | Đ | Đ | Đ | ✗ | Đ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm chìm nước thải FC | Đ | ✗ | Đ | Đ | ✗ | Đ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm chìm nước thải KTZ-LH | Đ | ✗ | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| REDPUMP - Bơm chìm nước thải SS | Đ | Đ | Đ | ✗ | ✗ | Đ | Đ | Đ | ✗ | Đ |
| REDPUMP - Bơm cắt rác WC | Đ | Đ | Đ | Đ | ✗ | ✗ | ✗ | ✗ | ✗ | Đ |
| REDPUMP - Bơm giếng SA | Đ | Đ | Đ | ✗ | ✗ | Đ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm giếng SP | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm trục ngang 2CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | Đ | ✗ | Đ |
| REDPUMP - Bơm trục ngang 3M | Đ | Đ | Đ | Đ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm trục ngang CDX | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm trục ngang CM | Đ | Đ | Đ | ✗ | ✗ | Đ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm trục ngang DWO (bản 1 trang) | Đ | ✗ | Đ | ✗ | ✗ | ✗ | Đ | Đ | ✗ | Đ |
| REDPUMP - Bơm trục ngang DWO (bản 2 trang) | Đ | ✗ | Đ | ? | ✗ | ✗ | Đ | Đ | ✗ | Đ |
| REDPUMP - Bơm trục ngang MHI | Đ | ? | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| REDPUMP - Bơm trục đứng CDLF | Đ | Đ | Đ | ✗ | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Bơm trục đứng IRG | Đ | ? | ? | ? | ✗ | ✗ | Đ | ✗ | Đ | Đ |
| REDPUMP - Máy khuấy chìm 4MIX | Đ | ? | – | – | ✗ | Đ | Đ | Đ | Đ | Đ |
| REDPUMP - Máy khuấy chìm MIX | Đ | ? | – | – | Đ | Đ | Đ | Đ | Đ | Đ |
| REDPUMP - Máy thổi khí Root RL | ✗ | ? | – | – | ✗ | ✗ | ✗ | ✗ | – | Đ |
| REDPUMP - Máy thổi khí con sò GB | Đ | ✗ | – | – | ✗ | ✗ | Đ | ✗ | ✗ | Đ |
| REDPUMP - Đĩa phân phối khí DN270-DN128 | Đ | ? | – | – | ✗ | Đ | Đ | ✗ | – | Đ |

## Đối chiếu với lỗi đã biết

| Lỗi đã biết | Tệp | Công cụ | Số đo |
|---|---|---|---|
| 1 SP >14MB | AQUARIS SP | BẮT | dung lượng 14.7 MB > tối đa 10 MB |
| 1 SP >14MB | REDPUMP SP | BẮT | dung lượng 14.2 MB > tối đa 10 MB |
| 2 chữ<6pt | PEROTAC SP | BẮT | 23 trang có chữ <7pt, nhỏ nhất 4.5 pt |
| 2 chữ<6pt | REDPUMP SP | BẮT | 21 trang có chữ <7pt, nhỏ nhất 4.5 pt |
| 2 chữ<6pt | PEROTAC RL | BẮT | 20 trang có chữ <7pt, nhỏ nhất 4.8 pt |
| 2 chữ<6pt | REDPUMP RL | BẮT | 21 trang có chữ <7pt, nhỏ nhất 4.7 pt |
| 3 ảnh<150ppi | AQUARIS GB | BẮT | 26 ảnh dưới ngưỡng, thấp nhất 83 ppi |
| 3 ảnh<150ppi | PEROTAC GB | BẮT | 35 ảnh dưới ngưỡng, thấp nhất 84 ppi |
| 3 ảnh<150ppi | REDPUMP GB | BẮT | 22 ảnh dưới ngưỡng, thấp nhất 89 ppi |
| 3 ảnh<150ppi | PEROTAC CDLF | BẮT | 23 ảnh dưới ngưỡng, thấp nhất 92 ppi |
| 3 ảnh<150ppi | PEROTAC RL tr.1 | BẮT | 2 ảnh dưới ngưỡng, thấp nhất 85 ppi |
| 3 ảnh<150ppi | REDPUMP RL tr.1 | BẮT | 2 ảnh dưới ngưỡng, thấp nhất 91 ppi |
| 3 ảnh<150ppi | AQUARIS CDX tr.1 | BẮT | 2 ảnh dưới ngưỡng, thấp nhất 97 ppi |
| 3 ảnh<150ppi | PEROTAC CDX tr.1 | BẮT | 2 ảnh dưới ngưỡng, thấp nhất 124 ppi |
| 3 ảnh<150ppi | REDPUMP CDX tr.1 | BẮT | 2 ảnh dưới ngưỡng, thấp nhất 122 ppi |
| 4 thiếu 50Hz | AQUARIS FS inox | BẮT | tr.1: thiếu "50 Hz" (sản phẩm có động cơ) |
| 4 thiếu 50Hz | PEROTAC FC inox | BẮT | tr.1: thiếu "50 Hz" (sản phẩm có động cơ) |
| 4 thiếu 50Hz | REDPUMP FC inox | BẮT | tr.1: thiếu "50 Hz" (sản phẩm có động cơ) |
| 4 thiếu 50Hz | PEROTAC RL | BẮT | tr.1: thiếu "50 Hz" (sản phẩm có động cơ) |
| 4 thiếu 50Hz | REDPUMP RL | BẮT | tr.1: thiếu "50 Hz" (sản phẩm có động cơ) |
| 5 Weight RL | PEROTAC RL | BẮT | 30 chỗ "weight" |
| 5 Weight RL | REDPUMP RL | BẮT | 36 chỗ "weight" |
| 6 ảnh chồng 2 lần | REDPUMP SP | BẮT | trang [1, 10, 16, 19] |
| 7 móc đường ② | AQUARIS CDX tr.2 | BẮT | cuối đường 2 chạm đầu đường 8 tại (337,336) [Q≈4.8, H≈20.5], lệch hướng 32° → nhìn như một đường gãy (móc) |
| 8 WC đúng QĐ 19 (H tại Qmax = nấc công suất) | AQUARIS WC | ĐÚNG QĐ 19 | 45 mã đúng, 0 mã sai, 8 cỡ họng |
| 8 WC đúng QĐ 19 (H tại Qmax = nấc công suất) | PEROTAC WC | ĐÚNG QĐ 19 | 45 mã đúng, 0 mã sai, 8 cỡ họng |
| 8 WC đúng QĐ 19 (H tại Qmax = nấc công suất) | REDPUMP WC | ĐÚNG QĐ 19 | 50 mã đúng, 0 mã sai, 8 cỡ họng |

Kết luận đối chiếu: bắt được cả 7 nhóm lỗi đã biết (24/24 dòng). Dòng 8: catalogue WC cả 3 hãng ĐÚNG Quy định 19 (rules/QUYET_DINH_ANH.md mục 19, QTH 4.9: trong cùng cỡ họng, H tại Qmax của model công suất bé nhất = 1 m, mỗi nấc công suất +1 m) — AQUARIS 45 mã, PEROTAC 45 mã, REDPUMP 50 mã (gồm mã 1 pha), 0 mã sai.

Các lần sửa công cụ trong lúc đối chiếu: (1) "móc đường ②" CDX AQUARIS tr.2 thật ra là cuối đường ② (CDX70/07, Q 4,8 m³/h, H 20,5 m) chạm đúng đầu đường ⑧ (CDX200/12) nên mắt thấy một đường gãy — thêm phép "đầu/cuối hai đường chạm nhau" (cùng lỗi ở CDX PEROTAC và REDPUMP); (2) "SP REDPUMP ảnh chồng 2 lần tr.1/10/16/19" là ảnh cỡ cả trang 831×595 pt đặt lệch, 53–60% nằm ngoài trang; (3) bỏ phép "nhãn che đuôi đường" vì báo nhầm; (4) thêm phép QĐ 19 chỉ cho WC; (5) chỉ áp phép Q–H (≤8 đường, H giảm khi Q tăng, cong đều) cho biểu đồ trục Q (m³/h) – H (m); thiết bị không có Q–H (máy thổi khí, máy khuấy, định lượng, đĩa) BỎ QUA mục 3–4; (6) đọc được bảng/biểu đồ do tools/ve_duong_cong.py vẽ (bảng hàng P/R, bảng xoay AQUARIS, trục phụ l/min). Kiểm chéo: PEROTAC CM đã duyệt so DU_LIEU/CM.xlsx: 87/87 model lệch ≤5% (lớn nhất 3,1% ở CM 125-200/45).

## Lỗi theo tệp / trang

(Mỗi mục gom gọn; ✗ = lỗi làm CHƯA ĐẠT, ? = chưa thể xác minh. Cảnh báo không ghi ở đây.)

### AQUARIS - Bơm chìm nước thải FS inox.pdf  (3 trang)
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ✗ M5 Chữ: 2 ký tự < 7 pt ở tr. 1–2 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 11 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.6 pt "• Double-channel impeller with high flow…")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 1 cụm chữ, tr.1 (vd "FS-100-7-5.5")
  - ✗ M8 Tệp: tr.2: vùng trống liền 10.8% chiều cao trang (y 714–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.39 (tương quan 0.03); trang biểu đồ tr.1/tr.1 SSIM 0.39; vùng biểu đồ trùng nét 0.85; màu chủ đạo #AAC8C5 / #13334C (cách 244) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.34; vùng biểu đồ trùng nét 0.90; màu chủ đạo #AAC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan -0.02); trang biểu đồ tr.1/tr.1 SSIM 0.32; vùng biểu đồ trùng nét 0.93; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm chìm nước thải FS.pdf  (1 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "230 V" tr. 1; "400 V" tr. 1
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 22 dòng chữ thân < 9 pt ở tr. 1 (vd 8.4 pt "FS SERIES   ·   AISI 304 SUBMERSIBLE ELE…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 195 ppi); vd tr.1: ảnh 594×814 px đặt 219×300 pt tại (96,118) = 195 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 1 cụm chữ, tr.1 (vd "FS 200/50")
  - ✗ M8 Tệp: 1 trang không phải A4 (±2 pt): tr.1 1190.6×842.0 pt (420×297 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.37 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.93; màu chủ đạo #B5B9BA / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.29 (tương quan 0.13); trang biểu đồ tr.1/tr.1 SSIM 0.29; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B5B9BA / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm chìm nước thải KTZ-LH.pdf  (6 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 2
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ✗ M4 Đường: 2 biểu đồ quá 8 đường: tr.2 (9), tr.5 (10)
  - ✗ M5 Chữ: 2 ký tự < 7 pt ở tr. 2, 5 (nhỏ nhất 5.2 pt)
  - ✗ M5 Chữ: 23 dòng chữ thân < 9 pt ở tr. 1–6 (vd 7.6 pt "SUBMERSIBLE DRAINAGE PUMP   ·   OVERVIEW…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 181 ppi); vd tr.1: ảnh 157×341 px đặt 62×136 pt tại (38,174) = 181 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 2 cụm chữ, tr.2,5 (vd "6")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 2 cụm chữ, tr.2,5 (vd "4")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.83 < 4.5 — 2 cụm chữ, tr.2,5 (vd "9")
  - ✗ M7 Tương phản: chữ #C99700 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 2.65 < 4.5 — 2 cụm chữ, tr.2,5 (vd "12")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.80 < 4.5 — 2 cụm chữ, tr.2,5 (vd "10")
  - ✗ M8 Tệp: tr.1: vùng trống liền 11.8% chiều cao trang (y 701–801 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 10.3% chiều cao trang (y 714–801 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 11.5% chiều cao trang (y 704–801 pt) > 10%

### AQUARIS - Bơm chìm nước thải SS.pdf  (1 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (10)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.4 pt)
  - ✗ M5 Chữ: 2 dòng chữ thân < 9 pt ở tr. 1 (vd 7.6 pt "SUBMERSIBLE SEWAGE PUMP   ·   50 Hz   · …")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.80 < 4.5 — 1 cụm chữ, tr.1 (vd "SS-3000")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.83 < 4.5 — 1 cụm chữ, tr.1 (vd "SS-2200")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 1 cụm chữ, tr.1 (vd "SS-750")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 1 cụm chữ, tr.1 (vd "SS-370")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #13334C (cách 245) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.05); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.27 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.27; vùng biểu đồ trùng nét 0.98; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm cắt rác WC.pdf  (8 trang)
  - ✗ M5 Chữ: 613 ký tự < 7 pt ở tr. 1–8 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 40 dòng chữ thân < 9 pt ở tr. 1–8 (vd 8.4 pt "WC SERIES   ·   SUBMERSIBLE SEWAGE PUMPS…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 246 ppi); vd tr.1: ảnh 1024×1024 px đặt 294×300 pt tại (67,122) = 246 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #FFFFFF trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 1.00 < 4.5 — 16 cụm chữ, tr.1,2,3,4,5,6,7,8 (vd "COMPONENT")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 7 cụm chữ, tr.1,2,3,4,5,6,8 (vd "50WC20-25-4")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 5 cụm chữ, tr.1,2,3,4,5 (vd "50WC15-40-7.5")
  - ✗ M8 Tệp: 8 trang không phải A4 (±2 pt): tr.1 1208.2×825.6 pt (426×291 mm); tr.2 1208.2×825.6 pt (426×291 mm); tr.3 1208.2×825.6 pt (426×291 mm); tr.4 1208.2×825.6 pt (426×291 mm); tr.5 1208.2×825.6 pt (426×291 mm); tr.6 1208.2×825.6 pt (426×291 mm)
  - ✗ M8 Tệp: tr.6: vùng trống liền 14.6% chiều cao trang (y 673–794 pt) > 10%
  - ✗ M8 Tệp: tr.7: vùng trống liền 17.2% chiều cao trang (y 652–794 pt) > 10%
  - ✗ M8 Tệp: tr.8: vùng trống liền 12.0% chiều cao trang (y 695–794 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.07); trang biểu đồ tr.1/tr.2 SSIM 0.44; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #C5C7C8 (cách 54) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.04); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #2B2D33 (cách 210) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.04); trang biểu đồ tr.2/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.96; màu chủ đạo #C5C7C8 / #2B2D33 (cách 264) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm giếng SA.pdf  (17 trang)
  - ✗ M4 Đường: 10 biểu đồ quá 8 đường: tr.7 (13), tr.8 (13), tr.9 (15), tr.10 (11), tr.11 (13), tr.12 (12), tr.13 (11), tr.15 (9), tr.16 (9), tr.17 (9)
  - ✗ M5 Chữ: 16 ký tự < 7 pt ở tr. 2–17 (nhỏ nhất 5.7 pt)
  - ✗ M5 Chữ: 36 dòng chữ thân < 9 pt ở tr. 1–17 (vd 7.8 pt "SUBMERSIBLE PUMPS   ·   2 in TO 6 in WEL…")
  - ✗ M6 Ảnh: 8 lượt ảnh dưới ngưỡng ppi ở tr. 1, 7–13 (thấp nhất 136 ppi); vd tr.1: ảnh 163×651 px đặt 86×344 pt tại (63,108) = 136 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 15 cụm chữ, tr.3,4,5,6,7,8,9,10… (vd "2.5SA1.5/31")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 14 cụm chữ, tr.4,5,6,7,8,9,10,11… (vd "3SA2/33")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.83 < 4.5 — 10 cụm chữ, tr.7,8,9,10,11,12,13,15… (vd "4SA3/35")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.80 < 4.5 — 7 cụm chữ, tr.7,8,9,10,11,12,13 (vd "4SA3/40")
  - ✗ M7 Tương phản: chữ #C99700 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 2.65 < 4.5 — 5 cụm chữ, tr.7,8,9,11,12 (vd "4SA3/50")
  - ✗ M8 Tệp: 17 trang không phải A4 (±2 pt): tr.1 612.0×858.0 pt (216×303 mm); tr.2 612.0×858.0 pt (216×303 mm); tr.3 612.0×858.0 pt (216×303 mm); tr.4 612.0×858.0 pt (216×303 mm); tr.5 612.0×858.0 pt (216×303 mm); tr.6 612.0×858.0 pt (216×303 mm)
  - ✗ M8 Tệp: tr.1: vùng trống liền 16.8% chiều cao trang (y 682–826 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.40 (tương quan 0.05); trang biểu đồ tr.2/tr.2 SSIM 0.39; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B4B9BB / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.11); trang biểu đồ tr.2/tr.2 SSIM 0.33; vùng biểu đồ trùng nét 0.81; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.28; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm giếng SP.pdf  (42 trang)
  - ✗ M4 Đường: 24 biểu đồ quá 8 đường: tr.3 (13), tr.4 (15), tr.5 (19), tr.7 (12), tr.8 (15), tr.9 (10), tr.10 (9), tr.11 (9), tr.12 (10), tr.15 (20), tr.17 (11), tr.18 (10) …
  - ✗ M5 Chữ: 156 ký tự < 7 pt ở tr. 3–4, 6–13, 15, 17–18, 20, 22–23, 25–26, 28, 30, 32, 34, 36, 38, 40, 42 (nhỏ nhất 6.0 pt)
  - ✗ M5 Chữ: 108 dòng chữ thân < 9 pt ở tr. 2–5, 7–14, 16, 19, 21, 24, 27, 29, 31, 33, 35, 37, 39, 41 (vd 8.8 pt "STAINLESS STEEL SUBMERSIBLE PUMPS  /  50…")
  - ✗ M6 Ảnh: 11 lượt ảnh dưới ngưỡng ppi ở tr. 1, 3–5, 7–13 (thấp nhất 93 ppi); vd tr.1: ảnh 493×169 px đặt 155×53 pt tại (30,30) = 229 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 26 cụm chữ, tr.3,4,5,7,8,9,10,11… (vd "4SP3-22")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 26 cụm chữ, tr.3,4,5,7,8,9,10,11… (vd "4SP3-15")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.83 < 4.5 — 24 cụm chữ, tr.3,4,5,7,8,9,10,11… (vd "4SP3-32")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.80 < 4.5 — 20 cụm chữ, tr.3,4,5,7,8,9,12,15… (vd "4SP3-39")
  - ✗ M7 Tương phản: chữ #C99700 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 2.65 < 4.5 — 13 cụm chữ, tr.3,4,5,7,8,15,20,22… (vd "4SP3-52")
  - ✗ M7 Tương phản: chữ #4C8C1A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.14 < 4.5 — 2 cụm chữ, tr.5,15 (vd "4SP8-44")
  - ✗ M8 Tệp: 42 trang không phải A4 (±2 pt): tr.1 598.0×853.0 pt (211×301 mm); tr.2 598.0×853.0 pt (211×301 mm); tr.3 598.0×853.0 pt (211×301 mm); tr.4 598.0×853.0 pt (211×301 mm); tr.5 598.0×853.0 pt (211×301 mm); tr.6 598.0×853.0 pt (211×301 mm)
  - ✗ M8 Tệp: dung lượng 14.7 MB > tối đa 10 MB
  - ✗ M8 Tệp: phông nhúng lặp: Arial-BoldMT ×25, ArialMT ×25
  - ✗ M8 Tệp: tr.6: vùng trống liền 43.2% chiều cao trang (y 452–820 pt) > 10%
  - ✗ M8 Tệp: tr.42: vùng trống liền 11.6% chiều cao trang (y 160–259 pt) > 10%
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.36; vùng biểu đồ trùng nét 0.98; màu chủ đạo #E2F2FC / #631015 (cách 347) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang 2CDX.pdf  (2 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (11)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 7 dòng chữ thân < 9 pt ở tr. 1–2 (vd 7.2 pt "STAINLESS STEEL HORIZONTAL TWIN-IMPELLER…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 202 ppi); vd tr.1: ảnh 398×330 px đặt 142×118 pt tại (30,112) = 202 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (ô nền): tỉ lệ 3.13 < 4.5 — 2 cụm chữ, tr.1 (vd "4")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (ô nền): tỉ lệ 4.31 < 4.5 — 2 cụm chữ, tr.1 (vd "6")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (ô nền): tỉ lệ 3.83 < 4.5 — 2 cụm chữ, tr.1 (vd "9")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (ô nền): tỉ lệ 3.80 < 4.5 — 2 cụm chữ, tr.1 (vd "10")
  - ✗ M8 Tệp: tr.2: vùng trống liền 12.8% chiều cao trang (y 697–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5BABC / #13334C (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.06); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.84; màu chủ đạo #B5BABC / #2B2D33 (cách 240) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.87; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang 3M.pdf  (7 trang)
  - ✗ M5 Chữ: 5 ký tự < 7 pt ở tr. 2–6 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 63 dòng chữ thân < 9 pt ở tr. 1–7 (vd 8.4 pt "3M SERIES   ·   PRODUCT OVERVIEW & CONST…")
  - ✗ M6 Ảnh: 9 lượt ảnh dưới ngưỡng ppi ở tr. 1–7 (thấp nhất 162 ppi); vd tr.1: ảnh 473×162 px đặt 170×58 pt tại (1015,20) = 200 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 5 cụm chữ, tr.2,3,4,5,6 (vd "3M 32-200/5.5")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 5 cụm chữ, tr.2,3,4,5,6 (vd "3M 32-200/3.0")
  - ✗ M8 Tệp: 7 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm); tr.4 1225.0×842.0 pt (432×297 mm); tr.5 1225.0×842.0 pt (432×297 mm); tr.6 1225.0×842.0 pt (432×297 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.30); trang biểu đồ tr.2/tr.2 SSIM 0.46; vùng biểu đồ trùng nét 0.96; màu chủ đạo #D5E2EA / #13334C (cách 305) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.38 (tương quan -0.08); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.91; màu chủ đạo #D5E2EA / #2B2D33 (cách 308) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan -0.13); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.90; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang CDX.pdf  (3 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.2 (11)
  - ✗ M4 Đường: tr.2 biểu đồ (234,174)–(555,506): cuối đường 2 chạm đầu đường 8 tại (337,336) [Q≈4.8, H≈20.5], lệch hướng 32° → nhìn như một đường gãy (móc)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 2 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 16 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.2 pt "STAINLESS STEEL HORIZONTAL SINGLE-STAGE …")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 97 ppi); vd tr.1: ảnh 469×389 px đặt 190×158 pt tại (30,114) = 178 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (ô nền): tỉ lệ 3.13 < 4.5 — 2 cụm chữ, tr.2 (vd "4")
  - ✗ M7 Tương phản: chữ #C99700 trên #FFFFFF (ô nền): tỉ lệ 2.65 < 4.5 — 2 cụm chữ, tr.2 (vd "6")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (ô nền): tỉ lệ 4.31 < 4.5 — 2 cụm chữ, tr.2 (vd "7")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (ô nền): tỉ lệ 3.83 < 4.5 — 2 cụm chữ, tr.2 (vd "11")
  - ✗ M8 Tệp: tr.1: vùng trống liền 11.6% chiều cao trang (y 707–805 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 12.8% chiều cao trang (y 697–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.44 (tương quan 0.03); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #A3C2D8 (cách 37) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.37 (tương quan 0.06); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.10); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.87; màu chủ đạo #A3C2D8 / #2B2D33 (cách 253) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang CM.pdf  (12 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 2–11
  - ✗ M4 Đường: 4 biểu đồ quá 8 đường: tr.3 (11), tr.4 (9), tr.5 (9), tr.10 (9)
  - ✗ M5 Chữ: 10 ký tự < 7 pt ở tr. 2–11 (nhỏ nhất 5.4 pt)
  - ✗ M5 Chữ: 170 dòng chữ thân < 9 pt ở tr. 1–12 (vd 7.0 pt "CLOSE-COUPLED PUMPS   ·   ELETTROPOMPE M…")
  - ✗ M6 Ảnh: 11 lượt ảnh dưới ngưỡng ppi ở tr. 1–11 (thấp nhất 191 ppi); vd tr.1: ảnh 477×391 px đặt 170×139 pt tại (28,96) = 202 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 27 cụm chữ, tr.2,3,4,5,6,7,9,10… (vd "4")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 24 cụm chữ, tr.2,3,4,5,7,9,10,11 (vd "6")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.83 < 4.5 — 12 cụm chữ, tr.3,4,5,10 (vd "9")
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.80 < 4.5 — 3 cụm chữ, tr.3 (vd "10")
  - ✗ M8 Tệp: tr.8: vùng trống liền 12.0% chiều cao trang (y 720–820 pt) > 10%
  - ✗ M8 Tệp: tr.12: vùng trống liền 11.1% chiều cao trang (y 727–820 pt) > 10%
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.38 (tương quan 0.13); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.89; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang DWO (bản 1 trang).pdf  (1 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ✗ M4 Đường: tr.1 biểu đồ (290,335)–(545,445) đường 1 (293,379) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 38° trong 5% chiều dài ở 0% đường (dốc -37° → -76°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M4 Đường: tr.1 biểu đồ (290,335)–(545,445) đường 2 (293,379) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 32° trong 5% chiều dài ở 0% đường (dốc -6° → -38°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 10 dòng chữ thân < 9 pt ở tr. 1 (vd 7.6 pt "STAINLESS STEEL CENTRIFUGAL PUMP   ·   5…")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 1 cụm chữ, tr.1 (vd "DWO200T/M")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 1 cụm chữ, tr.1 (vd "DWO400T/M")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.28 (tương quan 0.02); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B4BABB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.24 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.24; vùng biểu đồ trùng nét 0.92; màu chủ đạo #B4BABB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.21 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.21; vùng biểu đồ trùng nét 0.92; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang DWO (bản 2 trang).pdf  (2 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ✗ M4 Đường: tr.2 biểu đồ (122,134)–(525,608) đường 1 (127,324) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 38° trong 5% chiều dài ở 0% đường (dốc -37° → -76°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M4 Đường: tr.2 biểu đồ (122,134)–(525,608) đường 2 (127,324) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 32° trong 5% chiều dài ở 0% đường (dốc -6° → -38°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 9 dòng chữ thân < 9 pt ở tr. 1–2 (vd 7.6 pt "STAINLESS STEEL CENTRIFUGAL PUMP   ·   5…")
  - ✗ M6 Ảnh: 4 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 177 ppi); vd tr.1: ảnh 436×348 px đặt 113×90 pt tại (75,213) = 277 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.13 < 4.5 — 1 cụm chữ, tr.2 (vd "DWO200T/M")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 4.31 < 4.5 — 1 cụm chữ, tr.2 (vd "DWO400T/M")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.34 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.58; vùng biểu đồ trùng nét 0.97; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục ngang MHI.pdf  (3 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 9 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.4 pt "Silicon carbide and US Morgan graphite, …")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1, 3 (thấp nhất 132 ppi); vd tr.1: ảnh 810×418 px đặt 236×122 pt tại (30,120) = 247 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (ô nền): tỉ lệ 3.13 < 4.5 — 3 cụm chữ, tr.2 (vd "205")
  - ✗ M8 Tệp: tr.1: vùng trống liền 20.0% chiều cao trang (y 636–805 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 11.8% chiều cao trang (y 705–805 pt) > 10%

### AQUARIS - Bơm trục đứng CDLF.pdf  (12 trang)
  - ✗ M4 Đường: 10 biểu đồ quá 8 đường: tr.3 (13), tr.4 (13), tr.5 (12), tr.6 (13), tr.7 (11), tr.8 (12), tr.9 (16), tr.10 (16), tr.11 (12), tr.12 (13)
  - ✗ M5 Chữ: 10 ký tự < 7 pt ở tr. 3–12 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 52 dòng chữ thân < 9 pt ở tr. 1–12 (vd 8.4 pt "CDLF SERIES   ·   LIGHT STAINLESS STEEL …")
  - ✗ M6 Ảnh: 9 lượt ảnh dưới ngưỡng ppi ở tr. 1, 3–8 (thấp nhất 158 ppi); vd tr.1: ảnh 182×547 px đặt 65×195 pt tại (54,175) = 202 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #7A8B14 trên #FFFFFF (ô nền): tỉ lệ 3.80 < 4.5 — 10 cụm chữ, tr.3,4,5,6,7,8,9,10… (vd "CDLF2-15T")
  - ✗ M7 Tương phản: chữ #0E8FA3 trên #FFFFFF (ô nền): tỉ lệ 3.83 < 4.5 — 10 cụm chữ, tr.3,4,5,6,7,8,9,10… (vd "CDLF2-13T")
  - ✗ M7 Tương phản: chữ #2E8B3A trên #FFFFFF (ô nền): tỉ lệ 4.31 < 4.5 — 10 cụm chữ, tr.3,4,5,6,7,8,9,10… (vd "CDLF2-7T")
  - ✗ M7 Tương phản: chữ #D9791A trên #FFFFFF (ô nền): tỉ lệ 3.13 < 4.5 — 10 cụm chữ, tr.3,4,5,6,7,8,9,10… (vd "CDLF2-5T")
  - ✗ M7 Tương phản: chữ #C99700 trên #FFFFFF (ô nền): tỉ lệ 2.65 < 4.5 — 9 cụm chữ, tr.3,4,5,6,8,9,10,11… (vd "CDLF2-22T")
  - ✗ M8 Tệp: 12 trang không phải A4 (±2 pt): tr.1 1207.0×824.0 pt (426×291 mm); tr.2 1207.0×824.0 pt (426×291 mm); tr.3 1207.0×824.0 pt (426×291 mm); tr.4 1207.0×824.0 pt (426×291 mm); tr.5 1207.0×824.0 pt (426×291 mm); tr.6 1207.0×824.0 pt (426×291 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.08); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.04); trang biểu đồ tr.3/tr.4 SSIM 0.30; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B5B9BB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.07); trang biểu đồ tr.3/tr.4 SSIM 0.25; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### AQUARIS - Bơm trục đứng IRG.pdf  (5 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 20 ký tự < 7 pt ở tr. 2–5 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 8 dòng chữ thân < 9 pt ở tr. 1–5 (vd 8.4 pt "Complete range with a full series of cen…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 206 ppi); vd tr.1: ảnh 880×880 px đặt 307×307 pt tại (46,91) = 206 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 5 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm); tr.4 1225.0×842.0 pt (432×297 mm); tr.5 1225.0×842.0 pt (432×297 mm)
  - ✗ M8 Tệp: tr.2: vùng trống liền 12.8% chiều cao trang (y 685–793 pt) > 10%
  - ✗ M8 Tệp: tr.4: vùng trống liền 20.7% chiều cao trang (y 619–793 pt) > 10%
  - ✗ M8 Tệp: tr.5: vùng trống liền 12.6% chiều cao trang (y 687–793 pt) > 10%

### AQUARIS - Bơm định lượng JLM-JBB.pdf  (4 trang)
  - ✗ M1 Chữ cấm + 50 Hz: chữ cấm: "weight" ×1 ở tr. 2
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 4 dòng chữ thân < 9 pt ở tr. 1–4 (vd 8.6 pt "TRUSTWORTHY PUMP  ·  MADE BY AQUARIS…")
  - ✗ M6 Ảnh: 6 lượt ảnh dưới ngưỡng ppi ở tr. 1–2 (thấp nhất 162 ppi); vd tr.1: ảnh 462×178 px đặt 190×73 pt tại (40,46) = 175 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: ảnh xref 14 (462×178 px) hệ màu CMYK

### AQUARIS - Máy khuấy chìm 4MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 3 dòng chữ thân < 9 pt ở tr. 1 (vd 8.2 pt "SUBMERSIBLE MIXER   ·   ALL STAINLESS ST…")

### AQUARIS - Máy khuấy chìm MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 3 dòng chữ thân < 9 pt ở tr. 1 (vd 8.2 pt "SUBMERSIBLE MIXER   ·   TECHNICAL DATA  …")

### AQUARIS - Máy thổi khí con sò GB.pdf  (17 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "220 V" tr. 3–6, 11–13; "380 V" tr. 4–16
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 116 dòng chữ thân < 9 pt ở tr. 1–17 (vd 7.6 pt "VORTEX AIR PUMP   ·   BLOWER PUMP   ·   …")
  - ✗ M6 Ảnh: 26 lượt ảnh dưới ngưỡng ppi ở tr. 1–17 (thấp nhất 83 ppi); vd tr.1: ảnh 244×233 px đặt 115×110 pt tại (68,246) = 153 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 17 trang không phải A4 (±2 pt): tr.1 816.4×612.3 pt (288×216 mm); tr.2 816.4×612.3 pt (288×216 mm); tr.3 816.4×612.3 pt (288×216 mm); tr.4 816.4×612.3 pt (288×216 mm); tr.5 816.4×612.3 pt (288×216 mm); tr.6 816.4×612.3 pt (288×216 mm)
  - ✗ M8 Tệp: tr.6: vùng trống liền 12.9% chiều cao trang (y 503–582 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.41 (tương quan -0.00); trang biểu đồ tr.3/tr.3 SSIM 0.40; vùng biểu đồ trùng nét 0.87; màu chủ đạo #B4B9BB / #ABB4B9 (cách 10) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.17); trang biểu đồ tr.3/tr.3 SSIM 0.35; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.18); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.74; màu chủ đạo #ABB4B9 / #2B2D33 (cách 229) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm chìm nước thải FC inox.pdf  (3 trang)
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ✗ M5 Chữ: 2 ký tự < 7 pt ở tr. 1–2 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 15 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.6 pt "• Double-channel impeller with high flow…")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.39 (tương quan 0.03); trang biểu đồ tr.1/tr.1 SSIM 0.39; vùng biểu đồ trùng nét 0.85; màu chủ đạo #AAC8C5 / #13334C (cách 244) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.34; vùng biểu đồ trùng nét 0.90; màu chủ đạo #AAC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan -0.02); trang biểu đồ tr.1/tr.1 SSIM 0.32; vùng biểu đồ trùng nét 0.93; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm chìm nước thải FC.pdf  (2 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "230 V" tr. 2; "400 V" tr. 2
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 28 dòng chữ thân < 9 pt ở tr. 1–2 (vd 8.2 pt "AISI 304 submersible electric pumps  |  …")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1–2 (thấp nhất 188 ppi); vd tr.1: ảnh 594×814 px đặt 162×222 pt tại (352,96) = 264 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.2: vùng trống liền 13.8% chiều cao trang (y 671–787 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.37 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.93; màu chủ đạo #B5B9BA / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.29 (tương quan 0.13); trang biểu đồ tr.1/tr.1 SSIM 0.29; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B5B9BA / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm chìm nước thải KTZ-LH.pdf  (6 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 2
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 2 ký tự < 7 pt ở tr. 2, 5 (nhỏ nhất 5.2 pt)
  - ✗ M5 Chữ: 22 dòng chữ thân < 9 pt ở tr. 1–6 (vd 8.4 pt "Submersible drainage pump  |  50 Hz  |  …")
  - ✗ M6 Ảnh: 4 lượt ảnh dưới ngưỡng ppi ở tr. 1–2 (thấp nhất 158 ppi); vd tr.1: ảnh 157×341 px đặt 72×155 pt tại (41,105) = 158 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: vùng trống liền 13.3% chiều cao trang (y 688–801 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 10.4% chiều cao trang (y 713–801 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 11.1% chiều cao trang (y 707–801 pt) > 10%

### PEROTAC - Bơm chìm nước thải SS.pdf  (1 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (10)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.4 pt)
  - ✗ M5 Chữ: 3 dòng chữ thân < 9 pt ở tr. 1 (vd 8.2 pt "Submersible sewage pump  |  50 Hz  |  n …")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #13334C (cách 245) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.05); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.27 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.27; vùng biểu đồ trùng nét 0.98; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm cắt rác WC.pdf  (9 trang)
  - ✗ M5 Chữ: 2947 ký tự < 7 pt ở tr. 2–9 (nhỏ nhất 5.5 pt)
  - ✗ M5 Chữ: 54 dòng chữ thân < 9 pt ở tr. 1–9 (vd 7.4 pt "Items 3 and 5: single-phase models.…")
  - ✗ M5 Chữ: 66 chỗ chữ chồng nhau, vd tr.2: chữ chồng nhau tại (161,265): "DN50" ⟂ "Power                    " (đè 58% ký tự) ; tr.2: chữ chồng nhau tại (161,279): "50 m³/h" ⟂ "Power                    " (đè 37% ký tự)
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 155 ppi); vd tr.1: ảnh 730×940 px đặt 339×436 pt tại (41,142) = 155 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #5C6E78 trên #C7E8FA (ô nền): tỉ lệ 4.15 < 4.5 — 15 cụm chữ, tr.3,6 (vd "0")
  - ✗ M7 Tương phản: chữ #4DB8DA trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 2.28 < 4.5 — 5 cụm chữ, tr.2,3,4,5,6 (vd "50WC15-15-1.5")
  - ✗ M7 Tương phản: chữ #E27F86 trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 2.76 < 4.5 — 5 cụm chữ, tr.2,3,4,5,6 (vd "50WC15-25-3")
  - ✗ M7 Tương phản: chữ #DA629F trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.37 < 4.5 — 4 cụm chữ, tr.2,3,5,6 (vd "50WC9-22-2.2")
  - ✗ M7 Tương phản: chữ #B8772E trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 3.67 < 4.5 — 4 cụm chữ, tr.2,4,5,6 (vd "50WC20-25-4")
  - ✗ M8 Tệp: 9 trang không phải A4 (±2 pt): tr.1 1208.2×825.6 pt (426×291 mm); tr.2 1208.2×825.6 pt (426×291 mm); tr.3 1208.2×825.6 pt (426×291 mm); tr.4 1208.2×825.6 pt (426×291 mm); tr.5 1208.2×825.6 pt (426×291 mm); tr.6 1208.2×825.6 pt (426×291 mm)
  - ✗ M8 Tệp: tr.7: vùng trống liền 13.1% chiều cao trang (y 686–794 pt) > 10%
  - ✗ M8 Tệp: tr.8: vùng trống liền 14.6% chiều cao trang (y 673–794 pt) > 10%
  - ✗ M8 Tệp: tr.9: vùng trống liền 11.0% chiều cao trang (y 703–794 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.07); trang biểu đồ tr.1/tr.2 SSIM 0.44; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #C5C7C8 (cách 54) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.04); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #2B2D33 (cách 210) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.04); trang biểu đồ tr.2/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.96; màu chủ đạo #C5C7C8 / #2B2D33 (cách 264) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm giếng SA.pdf  (19 trang)
  - ✗ M4 Đường: 10 biểu đồ quá 8 đường: tr.7 (15), tr.8 (15), tr.9 (15), tr.10 (14), tr.11 (13), tr.12 (13), tr.13 (11), tr.15 (9), tr.16 (9), tr.17 (9)
  - ✗ M5 Chữ: 16 ký tự < 7 pt ở tr. 2–17 (nhỏ nhất 5.4 pt)
  - ✗ M5 Chữ: 126 dòng chữ thân < 9 pt ở tr. 1–19 (vd 7.4 pt "For water supply from wells or reservoir…")
  - ✗ M8 Tệp: 19 trang không phải A4 (±2 pt): tr.1 841.9×598.8 pt (297×211 mm); tr.2 841.9×598.8 pt (297×211 mm); tr.3 841.9×598.8 pt (297×211 mm); tr.4 841.9×598.8 pt (297×211 mm); tr.5 841.9×598.8 pt (297×211 mm); tr.6 841.9×598.8 pt (297×211 mm)
  - ✗ M8 Tệp: tr.4: vùng trống liền 10.8% chiều cao trang (y 514–579 pt) > 10%
  - ✗ M8 Tệp: tr.5: vùng trống liền 13.0% chiều cao trang (y 501–579 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 13.0% chiều cao trang (y 501–579 pt) > 10%
  - ✗ M8 Tệp: tr.14: vùng trống liền 10.8% chiều cao trang (y 514–579 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.40 (tương quan 0.05); trang biểu đồ tr.2/tr.2 SSIM 0.39; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B4B9BB / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.11); trang biểu đồ tr.2/tr.2 SSIM 0.33; vùng biểu đồ trùng nét 0.81; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.28; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm giếng SP.pdf  (23 trang)
  - ✗ M4 Đường: 21 biểu đồ quá 8 đường: tr.1 (13), tr.2 (15), tr.3 (19), tr.4 (12), tr.5 (15), tr.6 (10), tr.7 (9), tr.8 (9), tr.9 (10), tr.11 (20), tr.12 (21), tr.13 (13) …
  - ✗ M5 Chữ: 44719 ký tự < 7 pt ở tr. 1–23 (nhỏ nhất 4.5 pt)
  - ✗ M5 Chữ: 41 dòng chữ thân < 9 pt ở tr. 1–23 (vd 7.0 pt "Stainless steel submersible pumps  |  50…")
  - ✗ M6 Ảnh: 26 lượt ảnh dưới ngưỡng ppi ở tr. 1–2, 4, 6–12, 15–23 (thấp nhất 124 ppi); vd tr.1: ảnh 99×728 px đặt 47×346 pt tại (335,98) = 152 ppi < 300 (trang bìa)
  - ✗ M6 Ảnh: tr.2: ảnh (-69,98,-22,443) tràn ra ngoài trang 832×595, 100% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: tr.4: ảnh (-69,98,-22,443) tràn ra ngoài trang 832×595, 100% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: tr.12: ảnh (-102,97,8,427) tràn ra ngoài trang 832×595, 93% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: tr.15: ảnh (-102,97,8,427) tràn ra ngoài trang 832×595, 93% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: tr.17: ảnh (-102,97,8,427) tràn ra ngoài trang 832×595, 93% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: tr.19: ảnh (-69,98,-24,444) tràn ra ngoài trang 832×595, 100% diện tích ảnh nằm ngoài
  - ✗ M6 Ảnh: … còn 1 dòng cùng mục
  - ✗ M8 Tệp: 23 trang không phải A4 (±2 pt): tr.1 831.6×595.0 pt (293×210 mm); tr.2 831.6×595.0 pt (293×210 mm); tr.3 831.6×595.0 pt (293×210 mm); tr.4 831.6×595.0 pt (293×210 mm); tr.5 831.6×595.0 pt (293×210 mm); tr.6 831.6×595.0 pt (293×210 mm)
  - ✗ M8 Tệp: tr.1: vùng trống liền 10.1% chiều cao trang (y 519–579 pt) > 10%
  - ✗ M8 Tệp: tr.4: vùng trống liền 10.1% chiều cao trang (y 519–579 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 13.5% chiều cao trang (y 499–579 pt) > 10%
  - ✗ M8 Tệp: tr.7: vùng trống liền 13.5% chiều cao trang (y 499–579 pt) > 10%
  - ✗ M8 Tệp: tr.8: vùng trống liền 13.5% chiều cao trang (y 499–579 pt) > 10%
  - ✗ M8 Tệp: … còn 6 dòng cùng mục
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.36; vùng biểu đồ trùng nét 0.98; màu chủ đạo #E2F2FC / #631015 (cách 347) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang 2CDX.pdf  (2 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (11)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 11 dòng chữ thân < 9 pt ở tr. 1–2 (vd 8.0 pt "Stainless steel horizontal twin-impeller…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 171 ppi); vd tr.1: ảnh 486×314 px đặt 205×132 pt tại (30,92) = 171 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.2: vùng trống liền 20.5% chiều cao trang (y 632–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5BABC / #13334C (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.06); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.84; màu chủ đạo #B5BABC / #2B2D33 (cách 240) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.87; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang 3M.pdf  (7 trang)
  - ✗ M5 Chữ: 5 ký tự < 7 pt ở tr. 2–6 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 49 dòng chữ thân < 9 pt ở tr. 1–7 (vd 8.4 pt "Stainless steel 304 standard pump design…")
  - ✗ M6 Ảnh: 9 lượt ảnh dưới ngưỡng ppi ở tr. 1–7 (thấp nhất 150 ppi); vd tr.1: ảnh 502×172 px đặt 170×58 pt tại (40,18) = 213 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 7 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm); tr.4 1225.0×842.0 pt (432×297 mm); tr.5 1225.0×842.0 pt (432×297 mm); tr.6 1225.0×842.0 pt (432×297 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.30); trang biểu đồ tr.2/tr.2 SSIM 0.46; vùng biểu đồ trùng nét 0.96; màu chủ đạo #D5E2EA / #13334C (cách 305) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.38 (tương quan -0.08); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.91; màu chủ đạo #D5E2EA / #2B2D33 (cách 308) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan -0.13); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.90; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang CDX.pdf  (3 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.2 (11)
  - ✗ M4 Đường: tr.2 biểu đồ (290,110)–(555,424): cuối đường 2 chạm đầu đường 8 tại (375,263) [Q≈4.8, H≈20.5], lệch hướng 34° → nhìn như một đường gãy (móc)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 2 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 22 dòng chữ thân < 9 pt ở tr. 1–3 (vd 8.0 pt "Stainless steel horizontal single-stage …")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 124 ppi); vd tr.1: ảnh 924×363 px đặt 535×210 pt tại (30,92) = 124 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: vùng trống liền 10.4% chiều cao trang (y 717–805 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 19.1% chiều cao trang (y 643–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.44 (tương quan 0.03); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #A3C2D8 (cách 37) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.37 (tương quan 0.06); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.10); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.87; màu chủ đạo #A3C2D8 / #2B2D33 (cách 253) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang CM.pdf  (13 trang)
  - ✗ M4 Đường: 6 biểu đồ quá 8 đường: tr.2 (12), tr.3 (11), tr.4 (11), tr.5 (12), tr.8 (9), tr.10 (9)
  - ✗ M5 Chữ: 10 ký tự < 7 pt ở tr. 2–11 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 122 dòng chữ thân < 9 pt ở tr. 1–11, 13 (vd 8.6 pt "Clean water  ·  Civil  ·  Industrial  · …")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 133 ppi); vd tr.1: ảnh 629×531 px đặt 340×287 pt tại (40,116) = 133 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 13 trang không phải A4 (±2 pt): tr.1 1224.0×792.0 pt (432×279 mm); tr.2 1224.0×792.0 pt (432×279 mm); tr.3 1224.0×792.0 pt (432×279 mm); tr.4 1224.0×792.0 pt (432×279 mm); tr.5 1224.0×792.0 pt (432×279 mm); tr.6 1224.0×792.0 pt (432×279 mm)
  - ✗ M8 Tệp: tr.6: vùng trống liền 16.2% chiều cao trang (y 645–773 pt) > 10%
  - ✗ M8 Tệp: tr.7: vùng trống liền 10.2% chiều cao trang (y 693–773 pt) > 10%
  - ✗ M8 Tệp: tr.9: vùng trống liền 12.2% chiều cao trang (y 677–773 pt) > 10%
  - ✗ M8 Tệp: tr.11: vùng trống liền 12.2% chiều cao trang (y 677–773 pt) > 10%
  - ✗ M8 Tệp: tr.13: vùng trống liền 11.3% chiều cao trang (y 684–773 pt) > 10%
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.38 (tương quan 0.13); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.89; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang DWO (bản 1 trang).pdf  (1 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ✗ M4 Đường: tr.1 biểu đồ (102,282)–(306,420) đường 1 (105,337) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 38° trong 5% chiều dài ở 0% đường (dốc -37° → -76°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M4 Đường: tr.1 biểu đồ (102,282)–(306,420) đường 2 (105,337) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 32° trong 5% chiều dài ở 0% đường (dốc -6° → -38°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 10 dòng chữ thân < 9 pt ở tr. 1 (vd 8.0 pt "Stainless steel centrifugal pump  |  50 …")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 237 ppi); vd tr.1: ảnh 726×564 px đặt 221×172 pt tại (346,278) = 237 ppi < 300 (trang bìa)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.28 (tương quan 0.02); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B4BABB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.24 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.24; vùng biểu đồ trùng nét 0.92; màu chủ đạo #B4BABB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.21 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.21; vùng biểu đồ trùng nét 0.92; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang DWO (bản 2 trang).pdf  (2 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ✗ M4 Đường: tr.2 biểu đồ (122,116)–(525,570) đường 1 (127,298) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 38° trong 5% chiều dài ở 0% đường (dốc -37° → -76°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M4 Đường: tr.2 biểu đồ (122,116)–(525,570) đường 2 (127,298) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 32° trong 5% chiều dài ở 0% đường (dốc -6° → -38°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 11 dòng chữ thân < 9 pt ở tr. 1–2 (vd 8.0 pt "Stainless steel centrifugal pump  |  50 …")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 165 ppi); vd tr.1: ảnh 726×564 px đặt 316×245 pt tại (28,312) = 165 ppi < 300 (trang bìa)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.34 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.58; vùng biểu đồ trùng nét 0.97; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục ngang MHI.pdf  (3 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 10 dòng chữ thân < 9 pt ở tr. 1–3 (vd 8.6 pt "MHI · IVT-MHI   /   PRODUCT OVERVIEW…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1, 3 (thấp nhất 132 ppi); vd tr.1: ảnh 810×418 px đặt 262×135 pt tại (30,104) = 223 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: vùng trống liền 30.3% chiều cao trang (y 550–805 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 16.8% chiều cao trang (y 663–805 pt) > 10%

### PEROTAC - Bơm trục đứng CDLF.pdf  (12 trang)
  - ✗ M4 Đường: 8 biểu đồ quá 8 đường: tr.3 (13), tr.4 (13), tr.5 (12), tr.6 (13), tr.7 (11), tr.8 (12), tr.9 (32), tr.11 (25)
  - ✗ M5 Chữ: 8 ký tự < 7 pt ở tr. 3–8, 10, 12 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 50 dòng chữ thân < 9 pt ở tr. 1–12 (vd 7.8 pt "Light stainless steel vertical multi-sta…")
  - ✗ M6 Ảnh: 23 lượt ảnh dưới ngưỡng ppi ở tr. 1–12 (thấp nhất 92 ppi); vd tr.1: ảnh 257×88 px đặt 123×42 pt tại (24,10) = 151 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 12 trang không phải A4 (±2 pt): tr.1 792.0×612.0 pt (279×216 mm); tr.2 792.0×612.0 pt (279×216 mm); tr.3 792.0×612.0 pt (279×216 mm); tr.4 792.0×612.0 pt (279×216 mm); tr.5 792.0×612.0 pt (279×216 mm); tr.6 792.0×612.0 pt (279×216 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.08); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.04); trang biểu đồ tr.3/tr.4 SSIM 0.30; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B5B9BB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.07); trang biểu đồ tr.3/tr.4 SSIM 0.25; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Bơm trục đứng IRG.pdf  (3 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 6 ký tự < 7 pt ở tr. 2–3 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 6 dòng chữ thân < 9 pt ở tr. 1–3 (vd 8.4 pt "Clean water   ·   Home   ·   Civil   ·  …")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 205 ppi); vd tr.1: ảnh 583×200 px đặt 181×62 pt tại (40,15) = 232 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #5C6E78 trên #D6E0E5 (ô nền): tỉ lệ 3.99 < 4.5 — 3 cụm chữ, tr.2,3 (vd "(continued)")
  - ✗ M8 Tệp: 3 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm)

### PEROTAC - Máy khuấy chìm 4MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 2 dòng chữ thân < 9 pt ở tr. 1 (vd 8.6 pt "Artificial water flow for amusement faci…")

### PEROTAC - Máy khuấy chìm MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 2 dòng chữ thân < 9 pt ở tr. 1 (vd 8.6 pt "Artificial water flow for amusement faci…")

### PEROTAC - Máy thổi khí Root RL.pdf  (20 trang)
  - ✗ M1 Chữ cấm + 50 Hz: chữ cấm: "weight" ×10 ở tr. 4–13; "kg" ×34 ở tr. 4–13, 16–19
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 18850 ký tự < 7 pt ở tr. 1–20 (nhỏ nhất 4.8 pt)
  - ✗ M5 Chữ: 122 dòng chữ thân < 9 pt ở tr. 1–14, 16–20 (vd 8.4 pt "Pressure and vacuum operation  |  bore 4…")
  - ✗ M6 Ảnh: 12 lượt ảnh dưới ngưỡng ppi ở tr. 1, 4–13 (thấp nhất 85 ppi); vd tr.1: ảnh 316×248 px đặt 268×210 pt tại (254,84) = 85 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #CC6B1F trên #FFFFFF (ô nền): tỉ lệ 3.69 < 4.5 — 59 cụm chữ, tr.4,5,6,7,8,9,10,11… (vd "0.75 kW")
  - ✗ M8 Tệp: 20 trang không phải A4 (±2 pt): tr.1 816.4×612.3 pt (288×216 mm); tr.2 816.4×612.3 pt (288×216 mm); tr.3 816.4×612.3 pt (288×216 mm); tr.4 816.4×612.3 pt (288×216 mm); tr.5 816.4×612.3 pt (288×216 mm); tr.6 816.4×612.3 pt (288×216 mm)
  - ✗ M8 Tệp: tr.2: vùng trống liền 11.7% chiều cao trang (y 510–582 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 18.8% chiều cao trang (y 467–582 pt) > 10%
  - ✗ M8 Tệp: tr.14: vùng trống liền 27.7% chiều cao trang (y 412–582 pt) > 10%

### PEROTAC - Máy thổi khí con sò GB.pdf  (17 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "220 V" tr. 3–6, 11–13; "380 V" tr. 4–16
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 85 dòng chữ thân < 9 pt ở tr. 1–16 (vd 8.4 pt "Single-stage and double-stage  |  50 Hz…")
  - ✗ M6 Ảnh: 35 lượt ảnh dưới ngưỡng ppi ở tr. 1–17 (thấp nhất 84 ppi); vd tr.1: ảnh 921×666 px đặt 286×207 pt tại (240,90) = 232 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 17 trang không phải A4 (±2 pt): tr.1 816.4×612.3 pt (288×216 mm); tr.2 816.4×612.3 pt (288×216 mm); tr.3 816.4×612.3 pt (288×216 mm); tr.4 816.4×612.3 pt (288×216 mm); tr.5 816.4×612.3 pt (288×216 mm); tr.6 816.4×612.3 pt (288×216 mm)
  - ✗ M8 Tệp: tr.2: vùng trống liền 20.0% chiều cao trang (y 460–582 pt) > 10%
  - ✗ M8 Tệp: tr.17: vùng trống liền 10.1% chiều cao trang (y 520–582 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.41 (tương quan -0.00); trang biểu đồ tr.3/tr.3 SSIM 0.40; vùng biểu đồ trùng nét 0.87; màu chủ đạo #B4B9BB / #ABB4B9 (cách 10) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.17); trang biểu đồ tr.3/tr.3 SSIM 0.35; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.18); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.74; màu chủ đạo #ABB4B9 / #2B2D33 (cách 229) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### PEROTAC - Đĩa phân phối khí DN270-DN128.pdf  (2 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 28 dòng chữ thân < 9 pt ở tr. 1–2 (vd 8.6 pt "FINE BUBBLE   |   MODEL DN270   |   10 I…")

### REDPUMP - Bơm chìm nước thải FC inox.pdf  (3 trang)
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ✗ M5 Chữ: 2 ký tự < 7 pt ở tr. 1–2 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 15 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.4 pt "Liquid temperature: 0 to +50 °C…")
  - ✗ M8 Tệp: tr.2: vùng trống liền 13.7% chiều cao trang (y 694–809 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.39 (tương quan 0.03); trang biểu đồ tr.1/tr.1 SSIM 0.39; vùng biểu đồ trùng nét 0.85; màu chủ đạo #AAC8C5 / #13334C (cách 244) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.34; vùng biểu đồ trùng nét 0.90; màu chủ đạo #AAC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan -0.02); trang biểu đồ tr.1/tr.1 SSIM 0.32; vùng biểu đồ trùng nét 0.93; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm chìm nước thải FC.pdf  (2 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "230 V" tr. 2; "400 V" tr. 2
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 19 dòng chữ thân < 9 pt ở tr. 1–2 (vd 7.6 pt "The components are carefully selected fo…")
  - ✗ M8 Tệp: tr.1: vùng trống liền 16.4% chiều cao trang (y 671–809 pt) > 10%
  - ✗ M8 Tệp: tr.2: vùng trống liền 13.8% chiều cao trang (y 662–779 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.37 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.93; màu chủ đạo #B5B9BA / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.29 (tương quan 0.13); trang biểu đồ tr.1/tr.1 SSIM 0.29; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B5B9BA / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm chìm nước thải KTZ-LH.pdf  (6 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 2
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 4 ký tự < 7 pt ở tr. 2, 5 (nhỏ nhất 5.2 pt)
  - ✗ M5 Chữ: 13 dòng chữ thân < 9 pt ở tr. 1, 4 (vd 8.0 pt "The motor and pump bodies are made of ri…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 253 ppi); vd tr.1: ảnh 157×341 px đặt 45×97 pt tại (18,149) = 253 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: vùng trống liền 12.5% chiều cao trang (y 711–816 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 18.1% chiều cao trang (y 664–816 pt) > 10%
  - ✗ M8 Tệp: tr.4: vùng trống liền 12.0% chiều cao trang (y 716–816 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 19.1% chiều cao trang (y 655–816 pt) > 10%

### REDPUMP - Bơm chìm nước thải SS.pdf  (1 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (10)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.4 pt)
  - ✗ M5 Chữ: 2 dòng chữ thân < 9 pt ở tr. 1 (vd 7.4 pt "Curve tolerance according to ISO 9906…")
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #13334C (cách 245) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.05); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.94; màu chủ đạo #ABC8C5 / #2B2D33 (cách 248) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.27 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.27; vùng biểu đồ trùng nét 0.98; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm cắt rác WC.pdf  (8 trang)
  - ✗ M5 Chữ: 440 ký tự < 7 pt ở tr. 1–8 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 40 dòng chữ thân < 9 pt ở tr. 1–8 (vd 7.4 pt "WC: three-phase 3~     WCD: single-phase…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 242 ppi); vd tr.1: ảnh 738×1071 px đặt 219×318 pt tại (42,148) = 242 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #FFFFFF trên #FFFFFF (nền trắng (không có ô nền)): tỉ lệ 1.00 < 4.5 — 16 cụm chữ, tr.1,2,3,4,5,6,7,8 (vd "COMPONENT")
  - ✗ M8 Tệp: 8 trang không phải A4 (±2 pt): tr.1 1208.2×825.6 pt (426×291 mm); tr.2 1208.2×825.6 pt (426×291 mm); tr.3 1208.2×825.6 pt (426×291 mm); tr.4 1208.2×825.6 pt (426×291 mm); tr.5 1208.2×825.6 pt (426×291 mm); tr.6 1208.2×825.6 pt (426×291 mm)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.07); trang biểu đồ tr.1/tr.2 SSIM 0.44; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #C5C7C8 (cách 54) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.35 (tương quan 0.04); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.97; màu chủ đạo #A7A6AA / #2B2D33 (cách 210) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.04); trang biểu đồ tr.2/tr.1 SSIM 0.37; vùng biểu đồ trùng nét 0.96; màu chủ đạo #C5C7C8 / #2B2D33 (cách 264) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm giếng SA.pdf  (19 trang)
  - ✗ M4 Đường: 10 biểu đồ quá 8 đường: tr.7 (15), tr.8 (15), tr.9 (15), tr.10 (14), tr.11 (13), tr.12 (13), tr.13 (11), tr.15 (9), tr.16 (9), tr.17 (9)
  - ✗ M5 Chữ: 16 ký tự < 7 pt ở tr. 2–17 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 112 dòng chữ thân < 9 pt ở tr. 1–19 (vd 7.2 pt "For water supply from wells or reservoir…")
  - ✗ M8 Tệp: 19 trang không phải A4 (±2 pt): tr.1 834.0×593.0 pt (294×209 mm); tr.2 834.0×593.0 pt (294×209 mm); tr.3 834.0×593.0 pt (294×209 mm); tr.4 834.0×593.0 pt (294×209 mm); tr.5 834.0×593.0 pt (294×209 mm); tr.6 834.0×593.0 pt (294×209 mm)
  - ✗ M8 Tệp: tr.14: vùng trống liền 13.8% chiều cao trang (y 498–580 pt) > 10%
  - ✗ M8 Tệp: tr.15: vùng trống liền 12.4% chiều cao trang (y 507–580 pt) > 10%
  - ✗ M8 Tệp: tr.16: vùng trống liền 12.4% chiều cao trang (y 507–580 pt) > 10%
  - ✗ M8 Tệp: tr.17: vùng trống liền 12.4% chiều cao trang (y 507–580 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.40 (tương quan 0.05); trang biểu đồ tr.2/tr.2 SSIM 0.39; vùng biểu đồ trùng nét 0.90; màu chủ đạo #B4B9BB / #13334C (cách 237) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.11); trang biểu đồ tr.2/tr.2 SSIM 0.33; vùng biểu đồ trùng nét 0.81; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.28; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm giếng SP.pdf  (21 trang)
  - ✗ M4 Đường: 21 biểu đồ quá 8 đường: tr.1 (13), tr.2 (19), tr.2 (15), tr.3 (15), tr.3 (12), tr.6 (10), tr.7 (9), tr.7 (9), tr.8 (10), tr.10 (20), tr.11 (21), tr.11 (13) …
  - ✗ M5 Chữ: 30273 ký tự < 7 pt ở tr. 1–21 (nhỏ nhất 4.5 pt)
  - ✗ M5 Chữ: 40 dòng chữ thân < 9 pt ở tr. 1–21 (vd 7.0 pt "Stainless steel submersible pumps  |  50…")
  - ✗ M6 Ảnh: 4 lượt ảnh dưới ngưỡng ppi ở tr. 1, 10, 16, 19 (thấp nhất 150 ppi); vd tr.1: ảnh 1732×1240 px đặt 832×595 pt tại (432,7) = 150 ppi < 300 (trang bìa)
  - ✗ M6 Ảnh: tr.1: ảnh (432,7,1264,602) tràn ra ngoài trang 832×595, 53% diện tích ảnh nằm ngoài — ảnh cỡ cả trang đặt lệch (nghi ảnh dán chồng lên trang)
  - ✗ M6 Ảnh: tr.10: ảnh (477,-7,1309,588) tràn ra ngoài trang 832×595, 58% diện tích ảnh nằm ngoài — ảnh cỡ cả trang đặt lệch (nghi ảnh dán chồng lên trang)
  - ✗ M6 Ảnh: tr.16: ảnh (491,5,1323,600) tràn ra ngoài trang 832×595, 59% diện tích ảnh nằm ngoài — ảnh cỡ cả trang đặt lệch (nghi ảnh dán chồng lên trang)
  - ✗ M6 Ảnh: tr.19: ảnh (498,8,1330,603) tràn ra ngoài trang 832×595, 60% diện tích ảnh nằm ngoài — ảnh cỡ cả trang đặt lệch (nghi ảnh dán chồng lên trang)
  - ✗ M8 Tệp: 21 trang không phải A4 (±2 pt): tr.1 831.6×595.0 pt (293×210 mm); tr.2 831.6×595.0 pt (293×210 mm); tr.3 831.6×595.0 pt (293×210 mm); tr.4 831.6×595.0 pt (293×210 mm); tr.5 831.6×595.0 pt (293×210 mm); tr.6 831.6×595.0 pt (293×210 mm)
  - ✗ M8 Tệp: dung lượng 14.2 MB > tối đa 10 MB
  - ✗ M8 Tệp: phông nhúng lặp: Arial-BoldMT ×6, ArialMT ×6, Calibri-Bold ×5
  - ✗ M8 Tệp: tr.4: vùng trống liền 15.7% chiều cao trang (y 480–573 pt) > 10%
  - ✗ M8 Tệp: tr.5: vùng trống liền 15.7% chiều cao trang (y 480–573 pt) > 10%
  - ✗ M8 Tệp: tr.6: vùng trống liền 13.5% chiều cao trang (y 499–579 pt) > 10%
  - ✗ M8 Tệp: … còn 7 dòng cùng mục
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.36 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.36; vùng biểu đồ trùng nét 0.98; màu chủ đạo #E2F2FC / #631015 (cách 347) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang 2CDX.pdf  (2 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.1 (11)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 5 dòng chữ thân < 9 pt ở tr. 1–2 (vd 7.4 pt "Bracket and motor casing in aluminium…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 207 ppi); vd tr.1: ảnh 398×330 px đặt 138×115 pt tại (22,148) = 207 ppi < 300 (trang bìa)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.14); trang biểu đồ tr.1/tr.1 SSIM 0.35; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5BABC / #13334C (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.06); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.84; màu chủ đạo #B5BABC / #2B2D33 (cách 240) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.28 (tương quan 0.09); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.87; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang 3M.pdf  (7 trang)
  - ✗ M5 Chữ: 5 ký tự < 7 pt ở tr. 2–6 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 55 dòng chữ thân < 9 pt ở tr. 1–7 (vd 8.8 pt "Stainless steel 304 standard pump design…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1, 7 (thấp nhất 195 ppi); vd tr.1: ảnh 735×500 px đặt 238×162 pt tại (32,150) = 222 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 7 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm); tr.4 1225.0×842.0 pt (432×297 mm); tr.5 1225.0×842.0 pt (432×297 mm); tr.6 1225.0×842.0 pt (432×297 mm)
  - ✗ M8 Tệp: tr.1: vùng trống liền 13.8% chiều cao trang (y 688–805 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.43 (tương quan 0.30); trang biểu đồ tr.2/tr.2 SSIM 0.46; vùng biểu đồ trùng nét 0.96; màu chủ đạo #D5E2EA / #13334C (cách 305) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.38 (tương quan -0.08); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.91; màu chủ đạo #D5E2EA / #2B2D33 (cách 308) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.35 (tương quan -0.13); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.90; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang CDX.pdf  (3 trang)
  - ✗ M4 Đường: 1 biểu đồ quá 8 đường: tr.2 (11)
  - ✗ M4 Đường: tr.2 biểu đồ (238,84)–(559,376): cuối đường 2 chạm đầu đường 8 tại (341,226) [Q≈4.8, H≈20.5], lệch hướng 30° → nhìn như một đường gãy (móc)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 2 (nhỏ nhất 5.3 pt)
  - ✗ M5 Chữ: 13 dòng chữ thân < 9 pt ở tr. 1–3 (vd 7.8 pt "Single-impeller centrifugal pumps with h…")
  - ✗ M6 Ảnh: 2 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 122 ppi); vd tr.1: ảnh 465×386 px đặt 138×115 pt tại (22,148) = 243 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: tr.1: vùng trống liền 21.2% chiều cao trang (y 643–822 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.44 (tương quan 0.03); trang biểu đồ tr.2/tr.2 SSIM 0.36; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #A3C2D8 (cách 37) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.37 (tương quan 0.06); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B6B9B9 / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.10); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.87; màu chủ đạo #A3C2D8 / #2B2D33 (cách 253) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang CM.pdf  (11 trang)
  - ✗ M4 Đường: 6 biểu đồ quá 8 đường: tr.2 (12), tr.3 (11), tr.4 (11), tr.5 (12), tr.8 (9), tr.10 (9)
  - ✗ M5 Chữ: 10 ký tự < 7 pt ở tr. 2–11 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 122 dòng chữ thân < 9 pt ở tr. 1–11 (vd 8.6 pt "Clean water  ·  Civil  ·  Industrial  · …")
  - ✗ M8 Tệp: 11 trang không phải A4 (±2 pt): tr.1 1164.5×789.1 pt (411×278 mm); tr.2 1164.5×789.1 pt (411×278 mm); tr.3 1164.5×789.1 pt (411×278 mm); tr.4 1164.5×789.1 pt (411×278 mm); tr.5 1164.5×789.1 pt (411×278 mm); tr.6 1164.5×789.1 pt (411×278 mm)
  - ✗ M8 Tệp: tr.1: vùng trống liền 20.1% chiều cao trang (y 611–769 pt) > 10%
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.38 (tương quan 0.13); trang biểu đồ tr.2/tr.2 SSIM 0.27; vùng biểu đồ trùng nét 0.89; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang DWO (bản 1 trang).pdf  (1 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ✗ M4 Đường: tr.1 biểu đồ (284,110)–(545,228) đường 1 (287,157) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 38° trong 5% chiều dài ở 0% đường (dốc -37° → -76°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M4 Đường: tr.1 biểu đồ (284,110)–(545,228) đường 2 (287,157) [đầu đường Q≈1, H≈12]: đường không cong đều: đổi hướng 32° trong 5% chiều dài ở 0% đường (dốc -6° → -38°, đoạn phẳng rồi dốc gắt / gãy)
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 11 dòng chữ thân < 9 pt ở tr. 1 (vd 7.4 pt "   hydraulic parts made of AISI 304 stai…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 297 ppi); vd tr.1: ảnh 726×564 px đặt 176×137 pt tại (210,661) = 297 ppi < 300 (trang bìa)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.28 (tương quan 0.02); trang biểu đồ tr.1/tr.1 SSIM 0.28; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B4BABB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.24 (tương quan 0.01); trang biểu đồ tr.1/tr.1 SSIM 0.24; vùng biểu đồ trùng nét 0.92; màu chủ đạo #B4BABB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.21 (tương quan -0.01); trang biểu đồ tr.1/tr.1 SSIM 0.21; vùng biểu đồ trùng nét 0.92; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang DWO (bản 2 trang).pdf  (2 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "400 V" tr. 1; "230 V" tr. 1
  - ? M4 Đường: có biểu đồ nhưng không biểu đồ nào có trục Q (m³/h) – H (m) → chưa kiểm phép Q–H
  - ✗ M5 Chữ: 1 ký tự < 7 pt ở tr. 1 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 10 dòng chữ thân < 9 pt ở tr. 1–2 (vd 7.4 pt "   hydraulic parts made of AISI 304 stai…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 169 ppi); vd tr.1: ảnh 726×564 px đặt 310×241 pt tại (234,391) = 169 ppi < 300 (trang bìa)
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.34 (tương quan 0.02); trang biểu đồ tr.2/tr.2 SSIM 0.58; vùng biểu đồ trùng nét 0.97; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục ngang MHI.pdf  (3 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 4 dòng chữ thân < 9 pt ở tr. 1 (vd 7.6 pt "Hot water circulation and heating system…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 3 (thấp nhất 140 ppi); vd tr.3: ảnh 682×405 px đặt 351×209 pt tại (208,84) = 140 ppi < 200
  - ✗ M8 Tệp: tr.1: vùng trống liền 25.5% chiều cao trang (y 607–822 pt) > 10%
  - ✗ M8 Tệp: tr.2: vùng trống liền 10.9% chiều cao trang (y 730–822 pt) > 10%
  - ✗ M8 Tệp: tr.3: vùng trống liền 24.6% chiều cao trang (y 615–822 pt) > 10%

### REDPUMP - Bơm trục đứng CDLF.pdf  (13 trang)
  - ✗ M4 Đường: 8 biểu đồ quá 8 đường: tr.4 (13), tr.5 (13), tr.6 (12), tr.7 (13), tr.8 (11), tr.9 (12), tr.10 (32), tr.12 (25)
  - ✗ M5 Chữ: 8 ký tự < 7 pt ở tr. 4–9, 11, 13 (nhỏ nhất 5.6 pt)
  - ✗ M5 Chữ: 36 dòng chữ thân < 9 pt ở tr. 1, 3–10, 12 (vd 7.0 pt "CDLF is a vertical, non-self-priming mul…")
  - ✗ M6 Ảnh: 10 lượt ảnh dưới ngưỡng ppi ở tr. 1–2, 4–9 (thấp nhất 169 ppi); vd tr.1: ảnh 89×268 px đặt 33×100 pt tại (36,141) = 193 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 13 trang không phải A4 (±2 pt): tr.1 792.0×612.0 pt (279×216 mm); tr.2 792.0×612.0 pt (279×216 mm); tr.3 792.0×612.0 pt (279×216 mm); tr.4 792.0×612.0 pt (279×216 mm); tr.5 792.0×612.0 pt (279×216 mm); tr.6 792.0×612.0 pt (279×216 mm)
  - ✗ M8 Tệp: tr.4: vùng trống liền 10.1% chiều cao trang (y 533–595 pt) > 10%
  - ✗ M8 Tệp: tr.8: vùng trống liền 11.5% chiều cao trang (y 524–595 pt) > 10%
  - ✗ M8 Tệp: tr.13: vùng trống liền 10.4% chiều cao trang (y 531–595 pt) > 10%
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.35 (tương quan 0.08); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.85; màu chủ đạo #B5B9BB / #13334C (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.32 (tương quan 0.04); trang biểu đồ tr.3/tr.4 SSIM 0.30; vùng biểu đồ trùng nét 0.89; màu chủ đạo #B5B9BB / #2B2D33 (cách 239) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.33 (tương quan 0.07); trang biểu đồ tr.3/tr.4 SSIM 0.25; vùng biểu đồ trùng nét 0.91; màu chủ đạo #13334C / #2B2D33 (cách 35) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Bơm trục đứng IRG.pdf  (5 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ? M3 Bảng: không nhận được bảng Q–H (dạng hàng "m³/h" + các mức Q, hoặc dạng xoay "Model" theo cột) → chưa kiểm được bảng
  - ? M4 Đường: không nhận được biểu đồ có lưới/trục nào → chưa kiểm được đường
  - ✗ M5 Chữ: 8 ký tự < 7 pt ở tr. 2–5 (nhỏ nhất 5.8 pt)
  - ✗ M5 Chữ: 3 dòng chữ thân < 9 pt ở tr. 1 (vd 8.4 pt "Complete range with a full series of cen…")
  - ✗ M6 Ảnh: 1 lượt ảnh dưới ngưỡng ppi ở tr. 1 (thấp nhất 218 ppi); vd tr.1: ảnh 880×880 px đặt 290×290 pt tại (1,130) = 218 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 5 trang không phải A4 (±2 pt): tr.1 1225.0×842.0 pt (432×297 mm); tr.2 1225.0×842.0 pt (432×297 mm); tr.3 1225.0×842.0 pt (432×297 mm); tr.4 1225.0×842.0 pt (432×297 mm); tr.5 1225.0×842.0 pt (432×297 mm)
  - ✗ M8 Tệp: tr.1: vùng trống liền 10.3% chiều cao trang (y 723–809 pt) > 10%

### REDPUMP - Máy khuấy chìm 4MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 1 dòng chữ thân < 9 pt ở tr. 1 (vd 8.6 pt "ALL STAINLESS STEEL   |   50 Hz…")

### REDPUMP - Máy khuấy chìm MIX.pdf  (1 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha

### REDPUMP - Máy thổi khí Root RL.pdf  (21 trang)
  - ✗ M1 Chữ cấm + 50 Hz: chữ cấm: "weight" ×14 ở tr. 4–13, 16–17; "kg" ×38 ở tr. 4–13, 16–20
  - ✗ M1 Chữ cấm + 50 Hz: tr.1: thiếu "50 Hz" (sản phẩm có động cơ)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 19162 ký tự < 7 pt ở tr. 1–21 (nhỏ nhất 4.7 pt)
  - ✗ M5 Chữ: 130 dòng chữ thân < 9 pt ở tr. 1–14, 16–21 (vd 8.4 pt "Pressure and vacuum operation  |  bore 4…")
  - ✗ M6 Ảnh: 15 lượt ảnh dưới ngưỡng ppi ở tr. 1, 3–13 (thấp nhất 91 ppi); vd tr.1: ảnh 316×248 px đặt 250×196 pt tại (255,74) = 91 ppi < 300 (trang bìa)
  - ✗ M7 Tương phản: chữ #A31A1F trên #2B2E33 (ô nền): tỉ lệ 1.77 < 4.5 — 6 cụm chữ, tr.2 (vd "1")
  - ✗ M8 Tệp: 21 trang không phải A4 (±2 pt): tr.1 816.4×612.3 pt (288×216 mm); tr.2 816.4×612.3 pt (288×216 mm); tr.3 816.4×612.3 pt (288×216 mm); tr.4 816.4×612.3 pt (288×216 mm); tr.5 816.4×612.3 pt (288×216 mm); tr.6 816.4×612.3 pt (288×216 mm)
  - ✗ M8 Tệp: tr.2: vùng trống liền 12.9% chiều cao trang (y 513–592 pt) > 10%
  - ✗ M8 Tệp: tr.14: vùng trống liền 17.4% chiều cao trang (y 486–592 pt) > 10%
  - ✗ M8 Tệp: tr.20: vùng trống liền 14.1% chiều cao trang (y 506–592 pt) > 10%
  - ✗ M8 Tệp: tr.21: vùng trống liền 11.0% chiều cao trang (y 525–592 pt) > 10%

### REDPUMP - Máy thổi khí con sò GB.pdf  (17 trang)
  - ✗ M2 Điện/pha: chuỗi điện áp khác chuẩn 220–240 V / 380–415 V: "220 V" tr. 3–6, 11–13; "380 V" tr. 4–16
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 86 dòng chữ thân < 9 pt ở tr. 1–16 (vd 8.0 pt "Vortex air pump / blower pump / ring blo…")
  - ✗ M6 Ảnh: 22 lượt ảnh dưới ngưỡng ppi ở tr. 1–15, 17 (thấp nhất 89 ppi); vd tr.1: ảnh 244×233 px đặt 155×148 pt tại (616,422) = 113 ppi < 300 (trang bìa)
  - ✗ M8 Tệp: 17 trang không phải A4 (±2 pt): tr.1 816.4×612.3 pt (288×216 mm); tr.2 816.4×612.3 pt (288×216 mm); tr.3 816.4×612.3 pt (288×216 mm); tr.4 816.4×612.3 pt (288×216 mm); tr.5 816.4×612.3 pt (288×216 mm); tr.6 816.4×612.3 pt (288×216 mm)
  - ✗ M8 Tệp: tr.3: vùng trống liền 13.8% chiều cao trang (y 507–592 pt) > 10%
  - ✗ M8 Tệp: tr.7: vùng trống liền 13.8% chiều cao trang (y 507–592 pt) > 10%
  - ✗ M8 Tệp: tr.8: vùng trống liền 13.8% chiều cao trang (y 507–592 pt) > 10%
  - ✗ M8 Tệp: tr.9: vùng trống liền 13.8% chiều cao trang (y 507–592 pt) > 10%
  - ✗ M8 Tệp: tr.10: vùng trống liền 13.8% chiều cao trang (y 507–592 pt) > 10%
  - ✗ M8 Tệp: … còn 4 dòng cùng mục
  - ✗ M9 Khác 3 hãng: AQUARIS–PEROTAC: trang 1 SSIM 0.41 (tương quan -0.00); trang biểu đồ tr.3/tr.3 SSIM 0.40; vùng biểu đồ trùng nét 0.87; màu chủ đạo #B4B9BB / #ABB4B9 (cách 10) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: AQUARIS–REDPUMP: trang 1 SSIM 0.34 (tương quan 0.17); trang biểu đồ tr.3/tr.3 SSIM 0.35; vùng biểu đồ trùng nét 0.83; màu chủ đạo #B4B9BB / #2B2D33 (cách 238) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)
  - ✗ M9 Khác 3 hãng: PEROTAC–REDPUMP: trang 1 SSIM 0.34 (tương quan -0.18); trang biểu đồ tr.3/tr.3 SSIM 0.33; vùng biểu đồ trùng nét 0.74; màu chủ đạo #ABB4B9 / #2B2D33 (cách 229) → vượt 0.6 (HO_SO_HANG.json chung.nguong_giong_giao_dien — đề xuất, chưa anh duyệt)

### REDPUMP - Đĩa phân phối khí DN270-DN128.pdf  (2 trang)
  - ? M2 Điện/pha: không đọc được bảng model nào → chưa kiểm được công suất / bản 3 pha của mã 1 pha
  - ✗ M5 Chữ: 21 dòng chữ thân < 9 pt ở tr. 1–2 (vd 8.2 pt "TECHNICAL DATA   |   FINE BUBBLE DISC DI…")
  - ✗ M8 Tệp: tr.2: vùng trống liền 13.5% chiều cao trang (y 695–809 pt) > 10%

## Giới hạn còn lại của công cụ

- Mục 3 có phép QĐ 19 chỉ cho mã …WC… (H tại Qmax = nấc công suất trong cùng cỡ họng); mã không đọc được kW thì CHƯA THỂ XÁC MINH.
- Mục 4: đường Q–H phải cong đều — quá 1 điểm uốn hoặc đổi hướng >25° trong 5% chiều dài (đoạn phẳng rồi dốc gắt) là CHƯA ĐẠT; đường vẽ bằng ít đoạn thẳng (gấp khúc) cũng bị bắt.
- Có chế độ --goc <bản gốc> [--trang …]: chỉ tính lỗi MỚI so với bản gốc (dùng khi vá một phần catalogue đã duyệt).
- Bảng: đọc bảng dạng hàng (tiêu đề "m³/h" + các mức Q) và bảng xoay "Model 3~/1~" theo cột (kiểu ve_duong_cong AQUARIS). Bảng thông số định mức (MHI, KTZ-LH) và IRG → mục 3 CHƯA THỂ XÁC MINH.
- Biểu đồ: nhận theo khung lưới + nhãn số trục (khung cắt theo đường lưới đứng, bỏ trục phụ l/min); biểu đồ không lưới hoặc là ảnh → không kiểm được đường. Phép Q–H chỉ áp cho biểu đồ có trục Q (m³/h) – H (m) (cờ --khong-qh ép bỏ).
- So đường với số liệu ≤5% chỉ chạy khi có --du-lieu (DU_LIEU/<nhóm>.xlsx, sheet QH như ve_duong_cong.py); ghép model ↔ đường theo đường gần nhất, không theo nhãn.
- Chữ chồng nhau tính theo khung chữ; chữ bị ô trắng che (vẫn còn trong PDF) chỉ tách được khi ô che vẽ trực tiếp trên trang. PEROTAC WC tr.2–6 có 66 chỗ chồng khung — cần mắt xem.
- Chữ thân < 9 pt nhận theo mẫu dòng (≥6 từ, ≥70% chữ cái, rộng ≥100 pt) nên có thể sót/nhầm vài dòng.
- Tương phản: chữ nằm trên ảnh hoặc nền chuyển màu không đo (chỉ đếm); không tìm thấy nền thì coi nền trắng (chữ trắng không có nền = không nhìn thấy, vẫn ghi ✗).
- Mục 9: so ảnh xám 72 dpi (SSIM) trang 1, trang biểu đồ đầu và độ trùng nét vùng biểu đồ; ngưỡng 0,6 là đề xuất. Không chấm 6 trục (màu, phông, bìa, bảng, biểu đồ, đồ họa phụ) riêng lẻ.
- Mục 2: mã 1 pha nhận theo cột "1~", dấu "1~"/"3~" trên hàng hoặc cặp tên CDX/CDXM; ngưỡng 1 pha 3 kW đọc từ HO_SO_HANG.json chung.dien.mot_pha_kw_toi_da (khoá đề xuất 13/10, chưa anh duyệt). Chưa thấy mã 1 pha > 3 kW trong 62 tệp.
- Vùng trống: dựng ảnh 50 dpi, tính dải hàng không có nét ngang; khoảng trắng chủ ý (lề, ô trống thiết kế) cũng bị đếm.
