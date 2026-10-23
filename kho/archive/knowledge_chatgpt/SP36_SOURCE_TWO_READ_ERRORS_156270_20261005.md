# Nguồn6SP36 — giữ hai lỗi chép số đã bị kiểm độc lập bắt

Ngày05/10/2026 21:40, G03 đọc trực tiếp bảng nguồn và ảnh dựng PDF hiện hành, phát hiện hai lỗi chép trong phiếu Luna `c673891f…` và ROOT chuẩn bị `ca827613…/56a57ba6…`:

- 6SP36-15, Q30 m³/h: nguồn/current156m; đã chép nhầm157.
- 6SP36-26 hàng đầu, Q30 m³/h: nguồn/current270m; đã chép nhầm271.

ROOT mở lại cả hai ảnh nguồn phóng theo điểm ảnh, xác nhận156/270. Không sửa catalogue: hai ô in trong nguồn/current đúng. Giữ phiếu cũ/đường chuẩn bị cũ nguyên vẹn nhưng CHƯA ĐẠT, không được dùng để xuất PDF. Không tính hai số này thành hai ô sửa mới.

Phiếu crop đúng: `_BAO CAO/G05/INDEPENDENT6SP36 SOURCE210 TABLE RULE READONLY/01 VERIFIED Q30 CELLS SOURCE BOUNDS.json`. Hộp nguồn: hàng15 `[625,1026,664,1043]`, hàng26 đầu `[625,1120,664,1136]`. Chỉ các ảnh có tên VERIFIED là hai hộp hàng đúng; hai ảnh thăm dò15Q30/26Q30 đầu đã chọn sai hàng, không dùng làm chứng. Phóng theo điểm ảnh để đọc không phải làm nét nguồn hay vật liệu chèn catalogue.

Chuẩn bị mới `_BAO CAO/G05/ROOT6SP36 SOURCE210 CORRECT156270 PURE21 NO PDF 20261005T144000Z-283c9b/`: phiếu nguồn sửa cách đọc3726c6e61d324fb6c7b8332cad0a551d283bd6a8f6787aa851ba6ad688538443, đường thuần739c4cbc505dc5131fd65dec4c51d9bcd0d8f7bc281ce61e83d45d54e042cdf3.210H/42 đầu-cuối/24 mã điện giữ,0 sửa catalogue.39 đoạn/18 nối; còn chờ kiểm độc lập, chữ/bố cục/PDF chưa nghiệm thu.

Không xem hai lần tác nhân đọc giống nhau là đã xác minh chắc số nhỏ trong ảnh nén. Người kiểm phải tự mở ảnh nguồn, khóa đúng hàng/cột theo tiêu đề và số liền kề; khi số đáng ngờ, lập crop nguyên RGB có hộp nguồn, kiểm nguồn/current thật và giữ phiếu sai. Tỷ lệ đạt149 việc gốc không đổi.


## Mốc chuẩn bị54 đường và DWO 20261005T154304Z-dcf0a3

54 đường đã đạt kiểm toán số riêng, chưa ghi catalogue. 6SP36 đọc đúng156/270; hai số này vốn đúng trong PDF. 9 ô đề xuất thuộc6SP46/8SP77 chưa áp dụng; giữ108 đầu-cuối bảng. Phép ánh xạ trục6SP36 và giao lõi xám/đen6SP46 không đạt; không ép/làm rộng ngưỡng. Hai cụm nhãn2/28 nguồn6SP36 vẫn sát/chạm nét cũ, chưa dùng làm chữ sạch. Bản phác226 đã có nhãn trục đầy đủ và các vùng cần giữ, chưa chọn cách vẽ thật. Office đã đóng thông báo, nhưng DWO chưa mở và hai lần chụp giao diện tiếp tục lỗi; bản in vẫn CHƯA THỂ XÁC MINH. Fan cover (nắp quạt) là dòng14 của ảnh linh kiện. Nguồn có7 ô công thức, không phải2; phiếu03 DWO đính chính phiếu01. Bản đồSL17 biểu đồ dùng cùngphiếu04 sửađếm: P6=18+17,P11=11+11,P3=7 gồm6 cậpnhật và1 giữ. ROOT mở3 trang thật,không suy P3=13 hoặc nhận tổng195 làchứngđếm đúng;đây chỉlàmapphạmvi,chưađạt toànhìnhthức. Quyết định chữ và14 số tối thiểu DWO còn chờ.135/149 việc gốc giữ.

Bằng chứng: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT PREP54 AXES LIMITS DWO UI 20261005T151935Z-8afafd\01 ROOT PREPARED54 SCOPED READBACK.json; C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G18\INDEPENDENT DWO PRINT XML59 MEDIA3 READONLY\04 FINAL DWO XML PRINT 8COL WITH FORMULA CORRECTION.md
