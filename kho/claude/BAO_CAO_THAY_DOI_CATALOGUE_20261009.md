# BÁO CÁO THAY ĐỔI CATALOGUE — ngày 09/10/2026

Người lập: Claude (điều phối, phiên Sửa catalogue). Dành cho: dự án SEO web, người cập nhật trang sản phẩm.
Nhân viên phụ trách cập nhật web: [CHƯA CÓ TÊN trong dữ liệu — anh Trung điền]

Tệp đi kèm: `claude/THAY_DOI_MA_20261009.csv` (UTF-8 có BOM, mỗi dòng một mã, 590 dòng). Cột: hang, catalogue, ma, loai_thay_doi (thêm / xoá / đổi), loai_ma (3 pha / 1 pha / chung 1~ và 3~), kw, hp, pha_dien_ap, q_max_m3h, h_max_m, so_suy_ra, thay_doi_cu_moi, nguon_so, tep_pdf, trang_pdf, tep_pdf_ban_cu, trang_pdf_ban_cu, ma_kiem_12, ma_kiem_12_ban_cu, ma_cap_doi, ghi_chu.

Cách đếm: mỗi dòng là một chuỗi mã. Tên 1 pha có chữ M (4SPM5-4, 4SAM6/26, CDXM120/15, FC ...M) tính là một dòng riêng. SA và WC của AQUARIS dùng một mã chung cho 1~ và 3~, tính một dòng. Qmax, Hmax: Qmax = lưu lượng ở ô cuối có số trong bảng hiệu suất; Hmax = cột áp tại lưu lượng nhỏ nhất có số. Số đọc bằng script từ chính PDF mới (và PDF cũ để so).

## 1. Bảng tóm tắt số lượng (thêm / xoá / đổi theo hãng × catalogue)

| Hãng | Catalogue | Thêm | Xoá | Đổi | Tổng dòng |
|---|---|---:|---:|---:|---:|
| PEROTAC | Bơm cắt rác WC | 1 | 0 | 1 | 2 |
| PEROTAC | Bơm trục ngang CDX | 4 (gồm 2 tên 1 pha) | 0 | 2 (gồm 1 tên 1 pha) | 6 |
| PEROTAC | Bơm giếng SA | 2 (gồm 2 tên 1 pha) | 26 (gồm 11 tên 1 pha) | 0 | 28 |
| PEROTAC | Bơm giếng SP | 114 (gồm 6 tên 1 pha) | 12 (gồm 10 tên 1 pha) | 0 | 126 |
| PEROTAC | Bơm chìm nước thải FC | 10 (gồm 5 tên 1 pha) | 0 | 0 | 10 |
| PEROTAC | Bơm chìm nước thải FC inox | 7 | 0 | 0 | 7 |
| REDPUMP | Bơm cắt rác WC | 1 | 0 | 1 | 2 |
| REDPUMP | Bơm trục ngang CDX | 4 (gồm 2 tên 1 pha) | 0 | 2 (gồm 1 tên 1 pha) | 6 |
| REDPUMP | Bơm giếng SA | 2 (gồm 2 tên 1 pha) | 26 (gồm 11 tên 1 pha) | 0 | 28 |
| REDPUMP | Bơm giếng SP | 114 (gồm 6 tên 1 pha) | 12 (gồm 10 tên 1 pha) | 0 | 126 |
| REDPUMP | Bơm chìm nước thải FC | 10 (gồm 5 tên 1 pha) | 0 | 0 | 10 |
| REDPUMP | Bơm chìm nước thải FC inox | 7 | 0 | 0 | 7 |
| AQUARIS | Bơm định lượng JLM-JBB | 0 | 0 | 2 | 2 |
| AQUARIS | Bơm cắt rác WC | 1 | 0 | 1 | 2 |
| AQUARIS | Bơm trục ngang CDX | 4 (gồm 2 tên 1 pha) | 0 | 2 (gồm 1 tên 1 pha) | 6 |
| AQUARIS | Bơm giếng SA | 28 | 8 | 0 | 36 |
| AQUARIS | Bơm giếng SP | 174 (gồm 34 tên 1 pha) | 12 | 0 | 186 |
| **Tổng** | | **483** | **96** | **11** | **590** |

Khớp CSV: thêm 483, xoá 96, đổi 11, cộng 590 dòng (đếm lại trực tiếp từ tệp CSV khi lập báo cáo).

## 2. Hướng dẫn ngắn cho người sửa web

- Đọc tệp CSV theo cột `loai_thay_doi`: **thêm** = tạo mới dòng/trang sản phẩm; **xoá** = gỡ hoặc ẩn dòng sản phẩm đang có trên web; **đổi** = chỉ sửa số, xem cột `thay_doi_cu_moi` (ví dụ `kW 0.37→0.25`).
- Số ở các cột kW, HP, Qmax, Hmax, pha/điện áp là số in trong PDF mới. Cột `so_suy_ra` ghi rõ ô nào do chúng tôi suy ra hoặc chỉnh (không phải số nhà sản xuất in sẵn); nếu web có mục "thông số chính hãng" thì không dán các số này vào đó. Chữ "không suy ra" nghĩa là số lấy nguyên từ nguồn.
- Tên có chữ M là bản 1 pha (4SPM5-4, 4SAM6/26, CDXM120/15, FC 75/40M); chữ T trong FC là 3 pha. SA và WC của AQUARIS dùng một mã chung cho 1 pha và 3 pha (cột `loai_ma`).
- PDF catalogue đã được thay bằng tệp mới (mục 3, kèm mã kiểm 12 ký tự). Nếu web gắn liên kết tải catalogue thì đổi sang tệp mới. Số trang của SA, SP đã dịch chuyển (SA mất 1 trang, SP thêm trang), nên dùng cột `trang_pdf` của bản mới, không dùng số trang cũ.
- Cả 3 hãng không còn dải 3SP; cả 3 hãng không còn dải 4SA2. SP PEROTAC và REDPUMP: bỏ 9 tên 1 pha công suất trên 2,2 kW và 4SPM8-13 (đi theo 4SP8-13), cộng 10 dòng xoá 1 pha; thêm 6 tên 1 pha mới. SP AQUARIS: thêm 34 tên 1 pha (22 tên cho mã 3 pha đã có, 12 tên cho mã 3 pha mới thêm).
- JBB chỉ đổi công suất 2 mã AQUARIS. Catalogue JBB in lưu lượng theo L/h và áp suất theo bar, không in HP và không in cột áp theo m (cột `h_max_m` để trống).
- FC (bơm chìm nước thải) là catalogue mới của PEROTAC và REDPUMP: toàn bộ số lấy từ AQUARIS FS, chỉ đổi tên mã FS thành FC.
- Mã nào được anh yêu cầu xoá mà bản cũ của hãng đó không có thì không cần thao tác trên web (mục 4.5).

## 3. PDF mới trong CATALOGUE DA DUYET

Thư mục: `Catalog Sua/CATALOGUE DA DUYET/<HÃNG>/`. Mã kiểm = 12 ký tự đầu của `sha256sum` đọc lại từ tệp lúc lập báo cáo. Bản cũ nằm ở `<HÃNG>/_BAN CU/<tên> (<mã kiểm cũ>).pdf`.

| Hãng | Tệp mới | Mã kiểm 12 ký tự | Số trang | Mã kiểm bản cũ | Số trang cũ |
|---|---|---|---:|---|---:|
| AQUARIS | AQUARIS - Bơm định lượng JLM-JBB.pdf | 4f1ebc262e3a | 4 | 96abafa05240 | 4 |
| PEROTAC | PEROTAC - Bơm cắt rác WC.pdf | 50032fe5237a | 9 | 781609d51ecb | 9 |
| REDPUMP | REDPUMP - Bơm cắt rác WC.pdf | d25e5a9a99ac | 8 | c4ad5d386def | 8 |
| AQUARIS | AQUARIS - Bơm cắt rác WC.pdf | 627874543daf | 8 | 850af5704bdd | 8 |
| PEROTAC | PEROTAC - Bơm trục ngang CDX.pdf | de4c5e6aff60 | 3 | 00e3426c2147 | 3 |
| REDPUMP | REDPUMP - Bơm trục ngang CDX.pdf | 11b2b3d9a724 | 3 | 7b400d88d171 | 3 |
| AQUARIS | AQUARIS - Bơm trục ngang CDX.pdf | 61fd76110067 | 3 | e68f140ef5f1 | 3 |
| PEROTAC | PEROTAC - Bơm giếng SA.pdf | e91bedd73896 | 19 | 1c6a7a62c27f | 20 |
| REDPUMP | REDPUMP - Bơm giếng SA.pdf | dc58fb98a435 | 19 | b59c62e751b6 | 20 |
| AQUARIS | AQUARIS - Bơm giếng SA.pdf | 427a70820ce0 | 17 | 962ad7e5a369 | 18 |
| PEROTAC | PEROTAC - Bơm giếng SP.pdf | 00debe7acb61 | 23 | 6409c7f721d9 | 13 |
| REDPUMP | REDPUMP - Bơm giếng SP.pdf | 4d452705a0b4 | 21 | adb8e5da02f6 | 13 |
| AQUARIS | AQUARIS - Bơm giếng SP.pdf | cfe9b2636314 | 42 | 7c0c9fa03401 | 31 |
| PEROTAC | PEROTAC - Bơm chìm nước thải FC.pdf | bfdebd99876b | 2 | tệp mới, chưa có bản cũ | - |
| PEROTAC | PEROTAC - Bơm chìm nước thải FC inox.pdf | b3e1bb621dda | 3 | tệp mới, chưa có bản cũ | - |
| REDPUMP | REDPUMP - Bơm chìm nước thải FC.pdf | 50c62091820f | 2 | tệp mới, chưa có bản cũ | - |
| REDPUMP | REDPUMP - Bơm chìm nước thải FC inox.pdf | 65a7a53537a4 | 3 | tệp mới, chưa có bản cũ | - |
| AQUARIS | AQUARIS - Bơm trục ngang CM.pdf (việc khác trong ngày) | 24ef59e17cb7 | 12 | - | - |
| PEROTAC | PEROTAC - Máy thổi khí Root RL.pdf (việc khác trong ngày) | 4b23aae2b7b3 | 20 | - | - |
| REDPUMP | REDPUMP - Máy thổi khí Root RL.pdf (việc khác trong ngày) | 42eebb8e3e88 | 21 | - | - |

Đối chiếu `CATALOGUE DA DUYET/DANH SACH.txt`: 20/20 mã kiểm có trong danh sách.

## 4. Chi tiết theo catalogue

Số trang trong bảng là trang của PDF mới (mã bị xoá: trang của PDF cũ). Số mã 3 pha ở mỗi PDF đọc bằng script từ bảng hiệu suất (không tính tên M).

Đối chiếu số mã 3 pha: số mã bản cũ + thêm − xoá phải bằng số mã đọc từ PDF mới.

| Hãng | Catalogue | Mã cũ (PDF cũ) | + thêm | − xoá | = tính | Mã mới (PDF mới) | Khớp |
|---|---|---:|---:|---:|---:|---:|---|
| PEROTAC | Bơm cắt rác WC | 44 | 1 | 0 | 45 | 45 | khớp |
| PEROTAC | Bơm trục ngang CDX | 9 | 2 | 0 | 11 | 11 | khớp |
| PEROTAC | Bơm giếng SA | 175 | 0 | 15 | 160 | 160 | khớp |
| PEROTAC | Bơm giếng SP | 220 | 108 | 2 | 326 | 326 | khớp |
| REDPUMP | Bơm cắt rác WC | 44 | 1 | 0 | 45 | 45 | khớp |
| REDPUMP | Bơm trục ngang CDX | 9 | 2 | 0 | 11 | 11 | khớp |
| REDPUMP | Bơm giếng SA | 175 | 0 | 15 | 160 | 160 | khớp |
| REDPUMP | Bơm giếng SP | 220 | 108 | 2 | 326 | 326 | khớp |
| AQUARIS | Bơm cắt rác WC | 44 | 1 | 0 | 45 | 45 | khớp |
| AQUARIS | Bơm trục ngang CDX | 9 | 2 | 0 | 11 | 11 | khớp |
| AQUARIS | Bơm giếng SA | 132 | 28 | 8 | 152 | 152 | khớp |
| AQUARIS | Bơm giếng SP | 197 | 140 | 12 | 325 | 325 | khớp |

Kết quả: 12/12 dòng khớp.

### 4.1 Bơm định lượng JLM-JBB (chỉ AQUARIS)

Đổi công suất JBB201/7 và JBB321/6 từ 0,37 kW xuống 0,25 kW. Ô công suất ở bảng 1 của PDF: cũ [0.25, 0.37] kW, mới [0.25] kW. Ô tóm tắt "0.25–0.37 kW" giữ nguyên vì JBB421/6 và JBB521/5 vẫn 0,37 kW. Catalogue in lưu lượng theo L/h và áp suất theo bar; không in HP, không in cột áp (m).

| Hãng | Mã | Loại | kW | HP | Pha / điện áp | Qmax (m³/h) | Hmax (m) | Thay đổi cũ → mới | Số suy ra (không phải số in sẵn của hãng) | Tệp PDF, trang |
|---|---|---|---:|---:|---|---:|---:|---|---|---|
| AQUARIS | JBB201/7 | đổi | 0.25 | không in | 3~ 380–415 V (JBB201–JBB521 theo chữ in p.4) | 0.201 | không in | kW 0.37→0.25 | không suy ra; lưu lượng 0,201/0,321 m³/h là đổi đơn vị từ L/h (catalogue in L/h) | A tr.4 |
| AQUARIS | JBB321/6 | đổi | 0.25 | không in | 3~ 380–415 V (JBB201–JBB521 theo chữ in p.4) | 0.321 | không in | kW 0.37→0.25 | không suy ra; lưu lượng 0,201/0,321 m³/h là đổi đơn vị từ L/h (catalogue in L/h) | A tr.4 |

### 4.2 Bơm cắt rác WC (3 hãng)

Thêm 100WC100-40-18.5 (18,5 kW, 25 HP, Q tới 240 m³/h, H tới 52 m). Đổi 100WC100-50-22: chỉ ô H tại Q=240 từ 7 thành 8 m, các ô khác giữ nguyên. Ô tóm tắt "Max. head 65" không đổi. Nguồn: QUYET_DINH mục 110 câu 2; `V2_WC/BAO_CAO.md`.

| Hãng | Mã | Loại | kW | HP | Pha / điện áp | Qmax (m³/h) | Hmax (m) | Thay đổi cũ → mới | Số suy ra (không phải số in sẵn của hãng) | Tệp PDF, trang |
|---|---|---|---:|---:|---|---:|---:|---|---|---|
| PEROTAC, REDPUMP, AQUARIS | 100WC100-40-18.5 | thêm | 18.5 | 25 | 3~ 380–415 V | 240 | 52 | - | HP 25 (lấy theo 150WC200-20-18.5 cùng 18,5 kW); H tại Q=30,60,90,120,150,180,210 = 49,46,41,35,29,22,15 suy ra từ 2 đường 15 kW và 22 kW; H tại Q=240 = 7 suy ra theo quy tắc nấc công suất | P tr.5; R tr.4; A tr.4 |
| PEROTAC, REDPUMP, AQUARIS | 100WC100-50-22 | đổi | 22 | 30 | 3~ 380–415 V | 240 | 65 | H(Q=240): 7→8 | không | P tr.5; R tr.4; A tr.4 |

### 4.3 Bơm trục ngang CDX (3 hãng)

Thêm CDX120/15, CDX200/15, CDXM120/15, CDXM200/15 (1,1 kW). Đổi CDX200/25 và CDXM200/25 từ 1,8 kW lên 2,2 kW (dòng điện giữ 4,8 A bản 3 pha, 11,8 A bản 1 pha). CDX200/15: H in 24,1 m ở Q=4,8 và 16 m ở Q=15 (đã chỉnh nằm giữa CDX200/12 và CDX200/20 theo anh duyệt mục 110 câu 4), là số suy ra. Catalogue CDX không in HP.

| Hãng | Mã | Loại | kW | HP | Pha / điện áp | Qmax (m³/h) | Hmax (m) | Thay đổi cũ → mới | Số suy ra (không phải số in sẵn của hãng) | Tệp PDF, trang |
|---|---|---|---:|---:|---|---:|---:|---|---|---|
| PEROTAC, REDPUMP, AQUARIS | CDX120/15 | thêm | 1.1 | không in | 3~ 380–415 V | 9.6 | 33 | - | H tại Q=4.8,5.4,6.6,7.8 = 30.3,29.3,27.3,25.3 suy ra (giữa CDX120/12 và /20); dòng điện suy ra theo công thức hồi quy; kích thước lấy theo CDX120/12 (anh chọn) | P tr.2; R tr.2; A tr.2 |
| PEROTAC, REDPUMP, AQUARIS | CDX200/15 | thêm | 1.1 | không in | 3~ 380–415 V | 15 | 24.1 | - | toàn bộ H suy ra (24.1,23.7,22.9,22.0,20.6,19.6,18.1,16.0) theo nội suy công suất giữa CDX200/12 (0,9 kW) và CDX200/20 (1,5 kW) (anh chọn "đổi cho phù hợp"); anh nói "áp 25–35" nhưng số in là 24,1→16; dòng điện suy ra; kích thước lấy theo CDX200/12 | P tr.2; R tr.2; A tr.2 |
| PEROTAC, REDPUMP, AQUARIS | CDXM120/15 | thêm | 1.1 | không in | 1~ 220–240 V | 9.6 | 33 | - | H tại Q=4.8,5.4,6.6,7.8 = 30.3,29.3,27.3,25.3 suy ra (giữa CDX120/12 và /20); dòng điện suy ra theo công thức hồi quy; kích thước lấy theo CDX120/12 (anh chọn) | P tr.2; R tr.2; A tr.2 |
| PEROTAC, REDPUMP, AQUARIS | CDXM200/15 | thêm | 1.1 | không in | 1~ 220–240 V | 15 | 24.1 | - | toàn bộ H suy ra (24.1,23.7,22.9,22.0,20.6,19.6,18.1,16.0) theo nội suy công suất giữa CDX200/12 (0,9 kW) và CDX200/20 (1,5 kW) (anh chọn "đổi cho phù hợp"); anh nói "áp 25–35" nhưng số in là 24,1→16; dòng điện suy ra; kích thước lấy theo CDX200/12 | P tr.2; R tr.2; A tr.2 |
| PEROTAC, REDPUMP, AQUARIS | CDX200/25 | đổi | 2.2 | không in | 3~ 380–415 V | 15 | 38 | kW 1.8→2.2 | không đổi số khác; dòng điện giữ 3~ 4,8 A / 1~ 11,8 A (số cũ ứng 1,8 kW; 11,8 A vốn là số suy ra) | P tr.2; R tr.2; A tr.2 |
| PEROTAC, REDPUMP, AQUARIS | CDXM200/25 | đổi | 2.2 | không in | 1~ 220–240 V | 15 | 38 | kW 1.8→2.2 | không đổi số khác; dòng điện giữ 3~ 4,8 A / 1~ 11,8 A (số cũ ứng 1,8 kW; 11,8 A vốn là số suy ra) | P tr.2; R tr.2; A tr.2 |

### 4.4 Bơm giếng SA

- Xoá dải 4SA2 cả 3 hãng. PEROTAC và REDPUMP: 26 dòng xoá (15 mã 3 pha + 11 tên 1 pha 4SAM2). AQUARIS: 8 dòng xoá (AQUARIS chỉ có 8 mã 4SA2, mã chung 1~/3~).
- PEROTAC, REDPUMP không thêm mã 3 pha; chỉ thêm 2 tên 1 pha 4SAM6/26 và 4SAM10/17 (cùng 3 kW, số giữ nguyên theo bản 3 pha).
- AQUARIS thêm 28 mã số PEROTAC (kW mới trong dải AQUARIS cùng cỡ). Không thêm 4SA8/5, 4SA12/5. Các ô H chỉnh để giữ thứ tự công suất và khe >= 1,0 m được ghi trong cột `so_suy_ra`.
- Số trang: PEROTAC và REDPUMP 20 thành 19 trang; AQUARIS 18 thành 17 trang (do bỏ dải 4SA2). Các mã còn lại có thể đã đổi trang, dùng cột `trang_pdf`.
- Mã xoá PEROTAC: 4SA2/7, 9, 12, 15, 18, 21, 24, 28, 32, 37, 42, 47, 52, 58, 64; 4SAM2/7, 9, 12, 15, 18, 21, 24, 28, 32, 37, 42.
- Mã xoá REDPUMP: 4SA2/7, 9, 12, 15, 18, 21, 24, 28, 32, 37, 42, 47, 52, 58, 64; 4SAM2/7, 9, 12, 15, 18, 21, 24, 28, 32, 37, 42.
- Mã xoá AQUARIS: 4SA2/8, 11, 14, 19, 25, 38, 52, 65.

Mã thêm (đầy đủ số):

| Hãng | Mã | Loại | kW | HP | Pha / điện áp | Qmax (m³/h) | Hmax (m) | Có số suy ra | Trang PDF |
|---|---|---|---:|---:|---|---:|---:|---|---|
| PEROTAC | 4SAM6/26 | thêm | 3 | 4 | 1~ 220–240 V | 8.4 | 182 | không | 9 |
| PEROTAC | 4SAM10/17 | thêm | 3 | 4 | 1~ 220–240 V | 13.8 | 115 | không | 11 |
| REDPUMP | 4SAM6/26 | thêm | 3 | 4 | 1~ 220–240 V | 8.4 | 182 | không | 9 |
| REDPUMP | 4SAM10/17 | thêm | 3 | 4 | 1~ 220–240 V | 13.8 | 115 | không | 11 |
| AQUARIS | 4SA3/5 | thêm | 0.25 | 0.33 | 1~ 220–240 V / 3~ 380–415 V | 5.4 | 36 | có | 7 |
| AQUARIS | 4SA3/26 | thêm | 1.8 | 2.5 | 1~ 220–240 V / 3~ 380–415 V | 5.4 | 186 | có | 7 |
| AQUARIS | 4SA3/35 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 5.4 | 251 | có | 7 |
| AQUARIS | 4SA3/45 | thêm | 3.7 | 5 | 3~ 380–415 V | 5.4 | 323 | có | 7 |
| AQUARIS | 4SA4/6 | thêm | 0.37 | 0.5 | 1~ 220–240 V / 3~ 380–415 V | 6 | 44 | không | 8 |
| AQUARIS | 4SA4/21 | thêm | 1.8 | 2.5 | 1~ 220–240 V / 3~ 380–415 V | 6 | 143 | có | 8 |
| AQUARIS | 4SA4/28 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 6 | 203 | không | 8 |
| AQUARIS | 4SA4/36 | thêm | 3.7 | 5 | 3~ 380–415 V | 6 | 261 | không | 8 |
| AQUARIS | 4SA6/5 | thêm | 0.37 | 0.5 | 1~ 220–240 V / 3~ 380–415 V | 9.6 | 35 | có | 9 |
| AQUARIS | 4SA6/9 | thêm | 0.92 | 1.25 | 1~ 220–240 V / 3~ 380–415 V | 9.6 | 63 | có | 9 |
| AQUARIS | 4SA6/13 | thêm | 1.3 | 1.75 | 1~ 220–240 V / 3~ 380–415 V | 9.6 | 84 | có | 9 |
| AQUARIS | 4SA6/17 | thêm | 1.8 | 2.5 | 1~ 220–240 V / 3~ 380–415 V | 9.6 | 119 | có | 9 |
| AQUARIS | 4SA6/23 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 9.6 | 161 | có | 9 |
| AQUARIS | 4SA6/30 | thêm | 3.7 | 5 | 3~ 380–415 V | 9.6 | 210 | có | 9 |
| AQUARIS | 4SA8/10 | thêm | 1.3 | 1.75 | 1~ 220–240 V / 3~ 380–415 V | 10.8 | 60 | có | 10 |
| AQUARIS | 4SA8/14 | thêm | 1.8 | 2.5 | 1~ 220–240 V / 3~ 380–415 V | 10.8 | 82 | có | 10 |
| AQUARIS | 4SA8/26 | thêm | 3.7 | 5 | 3~ 380–415 V | 10.8 | 153 | có | 10 |
| AQUARIS | 4SA10/6 | thêm | 0.92 | 1.25 | 1~ 220–240 V / 3~ 380–415 V | 14.4 | 38 | có | 11 |
| AQUARIS | 4SA10/8 | thêm | 1.3 | 1.75 | 1~ 220–240 V / 3~ 380–415 V | 14.4 | 51 | có | 11 |
| AQUARIS | 4SA10/11 | thêm | 1.8 | 2.5 | 1~ 220–240 V / 3~ 380–415 V | 14.4 | 74 | có | 11 |
| AQUARIS | 4SA10/15 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 14.4 | 101 | có | 11 |
| AQUARIS | 4SA10/19 | thêm | 3.7 | 5 | 3~ 380–415 V | 14.4 | 128 | có | 11 |
| AQUARIS | 4SA12/7 | thêm | 1.3 | 1.75 | 1~ 220–240 V / 3~ 380–415 V | 16 | 43 | có | 12 |
| AQUARIS | 4SA12/14 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 16 | 86 | có | 12 |
| AQUARIS | 4SA12/18 | thêm | 3.7 | 5 | 3~ 380–415 V | 16 | 110 | có | 12 |
| AQUARIS | 4SA16/5 | thêm | 1.3 | 1.75 | 1~ 220–240 V / 3~ 380–415 V | 22 | 30 | có | 13 |
| AQUARIS | 4SA16/11 | thêm | 2.6 | 3.5 | 1~ 220–240 V / 3~ 380–415 V | 22 | 63 | có | 13 |
| AQUARIS | 4SA16/14 | thêm | 3.7 | 5 | 3~ 380–415 V | 22 | 83 | có | 13 |

### 4.5 Bơm giếng SP

- PEROTAC: thêm 114 (gồm 6 tên 1 pha), xoá 12 (gồm 10 tên 1 pha); số dòng thêm có ô H suy ra / chỉnh (không tính kích thước): 48/114.
- REDPUMP: thêm 114 (gồm 6 tên 1 pha), xoá 12 (gồm 10 tên 1 pha); số dòng thêm có ô H suy ra / chỉnh (không tính kích thước): 48/114.
- AQUARIS: thêm 174 (gồm 34 tên 1 pha), xoá 12; số dòng thêm có ô H suy ra / chỉnh (không tính kích thước): 63/174.
- Cả 3 hãng không còn 3SP. AQUARIS xoá 10 mã 3SP (3SP1, 3SP2); PEROTAC và REDPUMP không có 3SP ở bản cũ và không thêm.
- Số trang: PEROTAC 13 thành 23 trang, REDPUMP 13 thành 21 trang, AQUARIS 31 thành 42 trang; mọi mã đều có thể đổi trang, dùng cột `trang_pdf` của CSV.

Mã xoá (có dòng trong CSV):

- PEROTAC: 4SP8-13; 4SPM3-39, 45; 4SPM5-29, 33; 4SPM8-13, 18, 21; 4SPM10-13, 15; 4SPM14-11; 10SP135-9.
- REDPUMP: 4SP8-13; 4SPM3-39, 45; 4SPM5-29, 33; 4SPM8-13, 18, 21; 4SPM10-13, 15; 4SPM14-11; 10SP135-9.
- AQUARIS: 3SP1-10, 15, 22, 30, 40; 3SP2-8, 11, 17, 24, 32; 8SP120-9; 10SP125-9.

Mã thêm tính theo dải (đầy đủ từng mã, kW, HP, Q, H nằm trong CSV):

PEROTAC và REDPUMP: cùng danh sách mã và cùng khoảng giá trị.

| Dải | Số dòng | kW (nhỏ–lớn) | Qmax (m³/h) | Hmax (m) | Dòng có ô H suy ra / chỉnh |
|---|---:|---|---|---|---:|
| 4SP5 | 1 | 4–4 | 6.6–6.6 | 246–246 | 1 |
| 4SP8 | 13 | 1.1–7.5 | 10.8–10.8 | 42–278 | 13 |
| 4SP14 | 7 | 1.5–7.5 | 18–18 | 32–160 | 7 |
| 5SP10 | 10 | 1.5–15 | 20–20 | 33–330 | 0 |
| 5SP15 | 9 | 2.2–15 | 25–25 | 33–275 | 0 |
| 5SP20 | 9 | 2.2–15 | 30–30 | 32–231 | 0 |
| 5SP25 | 10 | 1.5–15 | 35–35 | 22–220 | 0 |
| 5SP30 | 8 | 3–15 | 40–40 | 33–176 | 0 |
| 6SP20 | 13 | 1.5–26 | 30–30 | 22–418 | 0 |
| 6SP30 | 7 | 9.2–26 | 42–42 | 102–318 | 7 |
| 6SP60 | 4 | 18.5–26 | 78–78 | 126–210 | 4 |
| 8SP77 | 3 | 5.5–63 | 96–96 | 20–342 | 3 |
| 8SP95 | 3 | 5.5–93 | 120–120 | 21–408 | 3 |
| 8SP120 | 9 | 7.5–63 | 150–150 | 22–220 | 9 |
| 10SP125 | 8 | 11–93 | 160–160 | 30–235 | 1 |

AQUARIS:

| Dải | Số dòng | kW (nhỏ–lớn) | Qmax (m³/h) | Hmax (m) | Dòng có ô H suy ra / chỉnh |
|---|---:|---|---|---|---:|
| 4SP3 | 11 | 0.37–4 | 4–4 | 38–378 | 3 |
| 4SP5 | 11 | 0.37–5.5 | 6–6 | 25–357 | 4 |
| 4SP8 | 15 | 0.75–5.5 | 10–10 | 33–227 | 10 |
| 4SP10 | 16 | 1.1–7.5 | 14.4–14.4 | 30–198 | 0 |
| 4SP14 | 12 | 1.1–7.5 | 18–18 | 27–177 | 10 |
| 6SP10 | 20 | 2.2–22 | 18–18 | 61–590 | 0 |
| 6SP18 | 21 | 2.2–30 | 24–24 | 33–638 | 0 |
| 6SP30 | 17 | 2.2–37 | 40–40 | 26–550 | 17 |
| 6SP36 | 21 | 3–37 | 54–54 | 27–405 | 0 |
| 6SP46 | 7 | 3–37 | 55–55 | 26–317 | 7 |
| 6SP60 | 5 | 4–37 | 65–65 | 28–280 | 5 |
| 8SP77 | 5 | 37–75 | 90–90 | 178–437 | 5 |
| 8SP95 | 2 | 37–92 | 110–110 | 149–383 | 2 |
| 10SP135 | 11 | 11–110 | 180–180 | 31–313 | 0 |

Tình trạng các mã anh yêu cầu xoá hoặc không thêm (tra từ PDF cũ và PDF mới):

| Hãng | Mã | Có trong PDF cũ | Có trong PDF mới | Cách xử lý trên web |
|---|---|---|---|---|
| PEROTAC | 4SP8-13 | có | không | có dòng "xoá" trong CSV |
| PEROTAC | 8SP120-9 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| PEROTAC | 10SP125-9 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| PEROTAC | 10SP135-9 | có | không | có dòng "xoá" trong CSV |
| PEROTAC | 4SP3-32 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| PEROTAC | 4SP3-44 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| PEROTAC | 4SP5-17 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| PEROTAC | 4SP5-22 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 4SP8-13 | có | không | có dòng "xoá" trong CSV |
| REDPUMP | 8SP120-9 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 10SP125-9 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 10SP135-9 | có | không | có dòng "xoá" trong CSV |
| REDPUMP | 4SP3-32 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 4SP3-44 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 4SP5-17 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| REDPUMP | 4SP5-22 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 4SP8-13 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 8SP120-9 | có | không | có dòng "xoá" trong CSV |
| AQUARIS | 10SP125-9 | có | không | có dòng "xoá" trong CSV |
| AQUARIS | 10SP135-9 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 4SP3-33 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 4SP3-45 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 4SP5-18 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 4SP5-21 | không | không | không cần thao tác (hãng này không có mã, không thêm) |
| AQUARIS | 6SP46-3A | không | không | không cần thao tác (hãng này không có mã, không thêm) |

Có 19 cặp (hãng, mã) thuộc nhóm không cần thao tác. Bảng lấy bằng script từ PDF cũ và PDF mới.

### 4.6 Bơm chìm nước thải FC và FC inox (PEROTAC, REDPUMP — catalogue mới)

Hai hãng, mỗi hãng 2 PDF mới: FC (2 trang, 5 kiểu máy, mỗi kiểu có bản T = 3 pha và M = 1 pha, tổng 10 mã) và FC inox (3 trang, 7 mã 3 pha). Toàn bộ số bằng AQUARIS FS, chỉ đổi tên mã FS thành FC; đối chiếu bằng script: PEROTAC FC 10/10 mã; PEROTAC FCI 7/7 mã; REDPUMP FC 10/10 mã; REDPUMP FCI 7/7 mã. PEROTAC và REDPUMP có cùng danh sách mã và số liệu; trang PDF theo từng hãng (P, R).

| Hãng | Mã | Loại | kW | HP | Pha / điện áp | Qmax (m³/h) | Hmax (m) | Thay đổi cũ → mới | Số suy ra (không phải số in sẵn của hãng) | Tệp PDF, trang |
|---|---|---|---:|---:|---|---:|---:|---|---|---|
| PEROTAC, REDPUMP | FC 75/40M | thêm | 0.55 | 0.75 | 1~ 220–240 V | 18 | 9.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 75/40T | thêm | 0.55 | 0.75 | 3~ 380–415 V | 18 | 9.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 100/40M | thêm | 0.75 | 1 | 1~ 220–240 V | 18 | 10 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 100/40T | thêm | 0.75 | 1 | 3~ 380–415 V | 18 | 10 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 150/40M | thêm | 1.1 | 1.5 | 1~ 220–240 V | 24 | 12.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 150/40T | thêm | 1.1 | 1.5 | 3~ 380–415 V | 24 | 12.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 200/50M | thêm | 1.5 | 2 | 1~ 220–240 V | 30 | 14 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 200/50T | thêm | 1.5 | 2 | 3~ 380–415 V | 30 | 14 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 300/80M | thêm | 2.2 | 3 | 1~ 220–240 V | 48 | 15.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC 300/80T | thêm | 2.2 | 3 | 3~ 380–415 V | 48 | 15.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-35-7-2.2 | thêm | 2.2 | 3 | 3~ 380–415 V | 40 | 17 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-50-7-3.0 | thêm | 3 | 4 | 3~ 380–415 V | 60 | 17 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-50-10-4.0 | thêm | 4 | 5.5 | 3~ 380–415 V | 80 | 20 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-100-7-5.5 | thêm | 5.5 | 7.5 | 3~ 380–415 V | 120 | 21.5 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-100-10-7.5 | thêm | 7.5 | 10 | 3~ 380–415 V | 120 | 24 | - | không suy ra | P tr.1; R tr.1 |
| PEROTAC, REDPUMP | FC-150-15-11 | thêm | 11 | 15 | 3~ 380–415 V | 200 | 26 | - | không suy ra | P tr.2; R tr.2 |
| PEROTAC, REDPUMP | FC-150-20-15 | thêm | 15 | 20 | 3~ 380–415 V | 250 | 30 | - | không suy ra | P tr.2; R tr.2 |

## 5. Thay đổi cùng ngày từ các phiên khác (chỉ tóm tắt, không có trong CSV)

Nguồn: sổ `Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/TIEN DO.md`, dòng 309–313. Các mục này đã xong trước 5 việc hôm nay. Riêng SA AQUARIS: bản cũ của việc SA hôm nay (962ad7e5a369) đã có 64 model này, nên CSV không liệt kê lại.

- **SA AQUARIS thêm dải 2 / 2,5 / 3 / 6 inch** (lượt 19 và 19b, 09/10 02:28Z và 02:46Z): 9 thành 18 trang, thêm 9 dải, 64 model lấy số PEROTAC (64/64 khớp PEROTAC, 1.130 ô); bỏ tem đỏ trên ảnh. Mã kiểm 68cc5b052dbd, rồi 2ca42825d673, rồi 962ad7e5a369 (là bản cũ của việc SA hôm nay). Đếm lại bằng script trong PDF SA AQUARIS mới: 64 mã bắt đầu 2SA, 2.5SA, 3SA, 6SA. Ledger ghi "chờ anh xem ảnh" cho lượt 19.
- **CM AQUARIS thêm 6 mã** (lượt 20, 09/10 02:48Z): 11 thành 12 trang, 66 thành 72 model; thêm CM32-160/3, CM32-250/9.2, CM40-250/9.2, CM40-250/18.5, CM80-250/37, CM80-250/45 (đọc lại trong PDF mới: 6/6 mã có mặt); dải CM 40-250 đổi sang số PEROTAC. Mã kiểm 96efa0b2bb2d thành 24ef59e17cb7. Kiểm độc lập 5/5 đạt (theo sổ).
- **Máy thổi khí Root RL PEROTAC và REDPUMP** (09/10 03:59Z xem thử, 04:14Z anh duyệt): catalogue mới vào CATALOGUE DA DUYET. PEROTAC 20 trang, mã kiểm 4b23aae2b7b3; REDPUMP 21 trang, mã kiểm 42eebb8e3e88. 7 ô bảng hiệu suất sửa theo đề xuất, còn lại giữ số nguồn (theo sổ).

## 6. Điểm chưa rõ

- Chưa có tên nhân viên phụ trách cập nhật web trong dữ liệu dự án; đã để chỗ trống ở đầu báo cáo, anh Trung điền.
- CDX200/15: ban đầu anh nhắn "áp 25 - 35" (GIAO_VIEC_20261009_5_VIEC.md, dòng 11, hiểu 35 m tại Q=4,8 và 25 m tại Q=15). Sau đó anh trả lời "đổi cho phù hợp dựa vào con lớn hơn và bé hơn liền kề" (QUYET_DINH mục 110 câu 4), nên PDF in 24,1 m rồi 16 m (số suy ra). Web dùng số trong PDF; nếu anh muốn đúng 35 / 25 thì phải sửa lại PDF.
- CDX, JBB: catalogue không in HP (ô HP để trống). JBB chỉ in lưu lượng L/h và áp suất bar, nên Hmax (m) để trống; Qmax JBB là đổi từ L/h sang m³/h (201 L/h = 0,201 m³/h).
- Số suy ra không phải số nhà sản xuất in: ô nào suy ra được ghi trong cột `so_suy_ra`. SP, số dòng thêm có ô H suy ra hoặc chỉnh: PEROTAC 48/114; REDPUMP 48/114; AQUARIS 63/174; các dòng còn lại lấy nguyên số H in của hãng nguồn (một số kèm kích thước suy ra). Nếu web có mục thông số chính hãng thì không đưa số suy ra vào đó.
- SP: sổ ghi "XONG; bản in CHƯA KIỂM" (chưa kiểm bản in thật). Các tệp SP vẫn là bản đã nhận vào CATALOGUE DA DUYET.
- Một số mã anh yêu cầu xoá không có ở bản cũ của hãng đó (xem bảng mục 4.5) nên không có dòng xoá; không cần làm gì trên web.
- Các thay đổi cùng ngày ở mục 5 (SA AQUARIS thêm 64 model dải 2 / 2,5 / 3 / 6 inch; CM AQUARIS thêm 6 mã; Root RL) chỉ tóm tắt theo yêu cầu, chưa có từng mã trong CSV; nếu web cần danh sách đầy đủ phải lập thêm.
- Tệp THAY_DOI_MA_20261009.csv cũ cùng tên (bản nháp 524 dòng, SP ở bản UV03) đã bị ghi đè bằng bản này.

## 7. Nguồn và cách kiểm

- PDF mới: `Catalog Sua/CATALOGUE DA DUYET/<HÃNG>/`; PDF cũ: `<HÃNG>/_BAN CU/`, chọn đúng bản cũ bằng `before_sha256` trong `history/5viec-*-accepted-*/BIEN_NHAN.json`.
- Thêm / xoá: lấy hiệu hai tập mã đọc từ bảng hiệu suất của PDF cũ và PDF mới (pymupdf). Đổi: ô kW, HP, pha, dòng điện hoặc H khác nhau giữa hai bản.
- Cờ "suy ra": dữ liệu `V2_WC/BAO_CAO.md`, `V2_CDX/data.json`, `V3_SA/THEM_AQ_UV03.json`, `V4_SP_PEROTAC/DATA_FULL_PR_RP_v6.json`, `V4_SP_AQUARIS/DATA_FULL_v6.json` (trong `work/claude_5viec_20261009/`). FC: không suy ra, số bằng AQUARIS FS.
- Đối chiếu dữ liệu với PDF mới: SA AQUARIS dữ liệu UV03 khớp PDF 168/168; SP PEROTAC dữ liệu v6 khớp PDF 891/891; SP REDPUMP dữ liệu v6 khớp PDF 891/891; SP AQUARIS dữ liệu v6 khớp PDF 1287/1287.
- Mã kiểm 12 ký tự: `sha256sum` đọc lại từ tệp lúc lập báo cáo, trùng `DANH SACH.txt`.
- Quyết định của anh: `claude/QUYET_DINH_ANH_20261006_PHIEN_CLAUDE.md` mục 107–123; giao việc: `claude/GIAO_VIEC_20261009_5_VIEC.md`; sổ tiến độ `TIEN DO.md` dòng 309–317.
- Không sửa catalogue nào khi lập báo cáo; chỉ ghi hai tệp: báo cáo này và CSV.
