# Việc đang chờ anh Trung — kiểm lại 13/10/2026

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
