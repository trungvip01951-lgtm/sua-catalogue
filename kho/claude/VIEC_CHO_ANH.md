# Việc đang chờ anh Trung — cập nhật 14/11/2026 (mục A–C cũ kiểm 13/10; mục D–E thêm 14/11)

Mỗi mục: việc gì, cần anh trả lời gì, nguồn (đã grep kiểm ngày 13/10). Anh trả lời xong thì ghi nguyên văn vào rules/QUYET_DINH_ANH.md, làm việc, rồi xoá mục ở đây (ghi "ĐÃ XONG <ngày>"). Số "QĐ" là số mới trong rules/QUYET_DINH_ANH.md.

## A. Catalogue chờ duyệt

1. **QXN40-60 (bơm chìm) — PEROTAC ứng viên 06 + AQUARIS ứng viên 03.** Số lấy theo QXN40/3-15, giữ tên QXN40-60; AQUARIS ghi 11 kW / 15 HP. Kiểm độc lập đã ĐẠT, CHƯA có trong CATALOGUE DA DUYET. Cần anh: duyệt ("ok lưu vào") hoặc báo lỗi. Tệp: deliverables/QXN40-60 PEROTAC 20261008/ (PEROTAC 0ab5ac4e9f62, AQUARIS d7e932233f0d). Nguồn: QĐ 112; TRANG_THAI cũ mục 4g (archive/claude/TRANG_THAI_CLAUDE_20261013_cu.md).
2. **PEROTAC 80WQX40-15-5.5 (bơm chìm nước thải inox, 1 trang A4) — ứng viên 03.** Cần anh: duyệt; xác nhận các số SUY RA từ tên model: điểm định mức 40 m³/h tại 15 m, họng DN80, cột áp 1 m tại Qmax 80 m³/h; gửi bảng Q–H và vật liệu nếu có. Tệp: work/claude_wqx_20261013/…(UNG VIEN 03).pdf (0c1a265f8c52). Nguồn: work/claude_wqx_20261013/BAO_CAO.md; claude/BAN_GIAO_20261013T0235Z.md.
3. **PEROTAC 150WC300-30-37 (bơm cắt rác, 37 kW) — ỨNG VIÊN 02 (14/10, A4 ngang, catalogue riêng 2 trang, QĐ 153).** Cần anh: duyệt; xác nhận cột áp — đang vẽ theo khoảng làm việc 280–300 m³/h ở 25–30 m (khớp tên model): Hmax 53 m (Q=0), 30 m tại 300 m³/h, 8 m tại Qmax 540 m³/h (số SUY RA); nếu muốn đúng chữ báo giá "cột áp max 25–30 m" thì vẽ lại. Tệp: work/claude_wc150_37_20261014/ (e030d01c8d85). Nguồn: BAO_CAO.md ở đó.

3b. **Dòng SF mới (Showfou SF áp cao) — 3 tệp AQUARIS/PEROTAC/REDPUMP "Bơm chìm nước thải SF áp cao" (QĐ 154).** Đã giao anh 14/10 để anh tự cập nhật. Muốn đưa vào CATALOGUE DA DUYET + DU_LIEU/SF.xlsx + KHO_ANH thì anh báo "duyệt SF". Tệp: work/claude_sf_20261014/ (BAO_CAO.md).

3c. **PEROTAC cụm 2 bơm MHI-Q (MHI-403Q, MHI-1604Q) — ỨNG VIÊN 07 (14/10, QĐ 155).** Cần anh: duyệt catalogue + ảnh đại diện; xác nhận các câu suy từ ảnh (van chặn từng bơm, bình áp, đồng hồ, cảm biến, tủ biến tần inox, ống góp inox, ứng dụng chung cư/khách sạn/văn phòng). Tệp: work/claude_mhi2_20261014/ (2d4209d8bf42; BAO_CAO.md).

## B. Thông số chờ anh chốt

4. **SS-450 / SSM-450F PEROTAC: tăng Qmax 18 → 24 m³/h — CHƯA LÀM.** Việc do phiên phần mềm ChatNoiBo (đã bỏ 12/10) nhận ngày 12/10, chưa ghi bản chính; thư mục làm việc đã xoá. Lời anh nguyên văn: CHƯA THỂ XÁC MINH. Cần anh: còn làm không; nếu làm thì áp cả 3 hãng SS hay chỉ PEROTAC. Nguồn: claude/khoa/da_nha/SS_PEROTAC.20261012T100028Z.json; TRANG_THAI cũ dòng 23.
5. **MHI / IVT-MHI (bản đã duyệt):** (a) MHI-805 điểm định mức đang ghi 31 m theo bảng mẫu — anh xác nhận; (b) điện áp đang ghi chung 1 pha / 3 pha, chưa ghi chú MHI-805 và MHI-1602…1604 chỉ có 3 pha — có thêm ghi chú không. Nguồn: QĐ 111.
6. **4MIX — mác inox SUS304** cho thân/cánh là em đặt; bản đã duyệt ghi SUS304, anh chưa trả lời riêng. Cần anh: xác nhận SUS304 hay mác khác. Nguồn: QĐ 80–81; DANH SACH.txt (4MIX "Toàn thân inox SUS304").
7. **Các lựa chọn điều phối tự đặt ngày 09/10 — ghi "CHỜ ANH XEM" (QĐ 136–138).** Anh đã duyệt bản cuối SA/SP/FC/CDX (QĐ 140 câu 1) nhưng chưa trả lời riêng từng điểm. Chính: SP 5 inch chỉ 3 pha; bỏ bản 1 pha 4 inch > 2,2 kW ở PEROTAC/REDPUMP (9 mã 4SPM3-39 … 4SPM14-11); 8SP120-4 tại Q 110: 50 → 53 m; SP mã thêm lệch > 5% thay bằng số nội suy theo số tầng; SA mã thêm AQUARIS khe với mã kề ≥ 1,0 m; mã thêm có đường chữ S sửa H trung gian. Cần anh: "giữ" hoặc chỉ điểm muốn đổi. Nguồn: QĐ 136, 137, 138.
8. **12 việc gốc còn tồn (mốc 137/149, thời catfix).** 06/10 anh trả lời "Làm tiếp", Claude hiểu là vẫn làm và ghi "chờ anh xác nhận cách hiểu" (QĐ 3). Sau đó cả 25 bản chính đã được dựng mới (lượt 15–16, 08/10); phương án 13/10 (bản claude/PHUONG_AN_HOAN_THIEN_20261013.md mục 3.7) đề nghị bỏ mốc này. Cần anh: xác nhận bỏ hẳn 12 việc này. Nguồn: QĐ 3; TRANG_THAI cũ mục 4.

## C. Bảng giá tối thiểu (không phải catalogue)

9. Tệp CATALOG SUA/GIA TOI THIEU 08-10-2026/Gia toi thieu - cap nhat thong so theo catalogue 09-10-2026 (ban 5).xlsx, trang "CAN ANH XEM": 12 câu của bản đầu (TRANG_THAI cũ mục 4·GIA) anh đã trả lời ngày 09/10; bản 5 còn 6 câu chưa trả lời (câu 7 đã có lời anh ở QĐ 127 và đã làm):
   1. Họng 2CDX200 (5 dòng): (1) cả 5 dòng 49-34 theo quy đổi G1½ × 1" — em đề xuất; (2) theo ảnh anh gửi 42-34, riêng 200/50 là 49-42; (3) giữ như hiện tại.
   2. CDX120/15 và CDXM120/15: (1) giữ số cũ Qmax 10,8 / Hmax 24 (380 V) và 28 (220 V); (2) thay bằng số anh chốt 09/10: Qmax 9,6 / Hmax 33 — em đề xuất.
   3. Các dòng 2CDX thêm mới: (1) Qmax/Hmax theo catalogue 2CDX đã duyệt — em đề xuất; (2) theo ảnh anh gửi (vd 2CDX120/30: ảnh 60 m – 8,4 m³/h, catalogue 59 m – 9 m³/h).
   4. 2CDX70/10, 70/12, 70/15, 70/20 (8 dòng 1 pha + 3 pha), 2CDXM120/40, 2CDXM200/40 có trong catalogue nhưng không có trong ảnh anh gửi: (1) giữ — em đề xuất; (2) xoá.
   5. Họng DWO037, DWO100 (M và T): bảng ghi 42-34 và 48-48; catalogue ghi 1¼" × 1¼" = 42-42: (1) sửa thành 42-42 — em đề xuất; (2) giữ.
   6. 3M65-160/15, 50WC10-10-0.75, 50WC12-10-1.1 không có trong catalogue đã duyệt: (1) giữ; (2) xoá — anh chọn.



## Đã chốt 14/10/2026 07:08 (QĐ 152)
- Vá hay dựng lại: VÁ đúng chỗ, giữ khổ và bố cục bản đã duyệt (anh chọn 1.1).
- Cột dòng điện A: nguồn không có A thì bỏ cột A (anh chọn 2.1).

## D. Catalogue riêng theo báo giá giao từ 15/10 đến 14/11 — chờ anh duyệt ("duyệt <tên>") hoặc báo lỗi

Tệp nằm trong work/<thư mục>/; mỗi thư mục có BAO_CAO.md ghi số nào là NGUỒN, số nào SUY RA. Anh duyệt bản nào thì báo để chép vào CATALOGUE DA DUYET (nếu anh muốn lưu ở đó).

| # | Tệp mới nhất | Thư mục work/ | Còn hỏi anh |
|---|---|---|---|
| D1 | REDPUMP - Bơm chìm nước thải SWQ 250SWQ500-5 (UNG VIEN 03).pdf | claude_swq_20261015 | — |
| D2 | REDPUMP - Bơm trục đứng IRG 300IRG800-30-110 (UNG VIEN 04).pdf | claude_irg300_20261016 | — |
| D3 | PEROTAC - Bơm cắt rác WC 200WC450-32-55 (UNG VIEN 01).pdf | claude_wc200_55_20261016 | dòng web "50–600 m³/h, 30–4 m" có dùng không; H 5 m tại Qmax |
| D4 | PEROTAC - Bơm chìm nước thải SS-150 2.pdf | claude_ss150_20261023 | — |
| D5 | AQUARIS - Bơm trục ngang CM 32-250-7.5 và CM 40-160-4 2.pdf | claude_cm2_aquaris_20261024 | — |
| D6 | PEROTAC - Bơm trục ngang CM 32-160-3 1.pdf; PEROTAC - Bơm trục đứng CDLF8-12T và CDLF16-8T 1.pdf | claude_bg27102026_20261027 | — |
| D7 | REDPUMP - Bơm trục rời đầu inox RPX 1.pdf (không có trên GitHub, QĐ 169) | claude_rpx_redpump_20261029 | thứ tự họng trong tên RPX: xả–hút (đang dùng) hay hút–xả |
| D8 | PEROTAC - Bơm chìm nước thải FC 75-40 1.pdf | claude_fc7540_20261030 | — |
| D9 | AQUARIS - Bơm trục ngang CM 1.pdf (vá 3 mã trên bản đã duyệt, QĐ 165) | claude_cm_aquaris_bg_20261030 | (a) duyệt để thay bản đã duyệt — DU_LIEU/CM.xlsx đã mang số mới; (b) CM 32-200/5.5 không có trong dải: thêm mã mới / ý anh là CM 32-250/5.5 / bỏ; (c) CM 32-160/3 số mới cắt lên trên CM 32-200/3 ở Q 24–27: giữ hay chỉnh |
| D10 | REDPUMP - Bơm giếng 6SP60 4.pdf | claude_6sp60_20261103 | báo giá 6SP60-8 cần sửa thành 64 m³/h – 56 m, 15 kW |
| D11 | REDPUMP - Bơm tăng áp TKP 1.pdf | claude_tkp_redpump_20261103 | câu công dụng viết mới; vật liệu / kích thước / dòng điện nếu anh có |
| D12 | REDPUMP - Bơm cắt rác WC 150WC-200WC 37-132kW 3.pdf + bản tiếng Việt 3 | claude_wc_redpump_20261113 | số cực / tốc độ 150WC 37–132 kW đang ghi 2 cực 2900 theo dải (suy ra) |
| D13 | REDPUMP - Bơm trục đứng đa tầng GDL 50GDL18-15x9 1.pdf | claude_gdl_redpump_20261114 | (a) ảnh máy; (b) điện áp 3 pha 380–415 V đúng không |

## E. Việc anh giao chưa làm vì chờ anh trả lời

10. **Bản chuẩn 3 hãng của sách RPX** ("Redpump là rpx perotac là prx aquaris mà aqx … thông số chuẩn hãng k sửa gì", 29/10): chờ anh trả lời 3 câu — thứ tự họng trong tên (xả–hút hay hút–xả); có giữ hậu tố "/kW" trong tên không; làm đủ mọi mã của sách mẫu hay chỉ một số cỡ.
11. **Đề xuất sau rà soát 14/11** (QĐ 184): claude/RA_SOAT_20261114.html — anh đánh số mục đồng ý / không.

