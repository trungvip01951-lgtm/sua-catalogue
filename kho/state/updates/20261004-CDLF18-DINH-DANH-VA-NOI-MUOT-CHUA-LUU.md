# CDLF: 18 đoạn đã định danh, bản sửa chưa lưu

Ghi ngày 04/10/2026, sau khi ROOT tiếp nhận bản CM38 thật. Đây là dữ liệu bàn giao chung đã ghi trên máy; chưa có xác nhận Claude đã đọc hoặc áp dụng. Không dùng phiếu toán thay nghiệm thu catalogue.

## Trạng thái đã xác minh

- WC ba hãng đã lưu đúng thứ tự 11 → 15 → 22 → 30 kW ở bảng và chú thích. Giữ các tệp đã nghiệm thu; không dựng hoặc sửa lại vì ghi chú này.
- Bản CM38 đã lưu và nghiệm thu riêng đường đặc tính, bảng, chữ và tài nguyên. Toàn G13 chưa hoàn tất: #110 và sơ đồ trang 1 của #154/#155 còn thiếu tài nguyên đúng kiểu. Ba mô tả ở trang 1 đã đúng; không báo chúng là thiếu hoặc làm lại.
- CDLF hiện chưa lưu bản sửa các đầu rời. Đã định danh chính xác 16 đầu trái và hai đoạn giữa tăng cột áp, dùng nhãn, nét nguồn và thân đúng model; không gán theo thứ hạng cột áp. 18 lỗi này vẫn CHƯA ĐẠT ở tệp hiện hành.
- 16 đầu trái có phương án toán: 14 nối trùng tiếp tuyến và độ cong; hai CDLF32-13-2 nối trùng tiếp tuyến. Hai CDLF32-1-1 có phương án toán cho đoạn giữa, chưa đủ dữ liệu đầu trái/chữ để nhận toàn miền.
- Bốn nhãn 10/12 mới có vị trí dịch đề xuất. Sáu nhãn 2/3/8/11/13/14 mỗi hãng cần né đường mới. Nhãn −9−2 bị đường đỏ cắt trên hình hiện hành, chưa đối chiếu nguồn để gọi lỗi mới. Đầu rời còn mảnh hơn thân.

## Cách tiếp tục

1. Tác giả cung cấp dữ liệu nhỏ đúng hai −1−1: đầu trái, lệnh và ma trận nguyên, đỉnh quan sát, cụm chữ và hộp chữ. G01 tính tiền tố toàn miền giảm, giữ thân từ Q16; không nạp lại toàn 344 đường hoặc 400 ô ảnh.
2. Một tác giả ráp 18 đoạn, đồng bộ 24 bút đầu rời và dời nguyên cụm chữ. Giữ 14 luồng trang đã nghiệm thu và các đường chỉ dẫn; không tạo thêm các bộ mẫu lặp.
3. Đọc lại lệnh thật sau dựng để kiểm hướng, điểm nối, độ rộng bút, thân/bảng và nét ngoài phạm vi. Kiểm ảnh thật để chốt độ mượt, nhãn đúng nhánh và khoảng hở.
4. ROOT mới mở bước lưu một PDF thật mỗi hãng bằng CATFIX, kiểm lại tệp đã lưu, rồi sao lưu chính xác bản trước và tiếp nhận bản giao. Mã lưu đã chuẩn bị nhưng chưa chạy.

## Bài học cần giữ

- Nghiệm thu thân đường không chứng minh các đoạn đầu rời hoặc đoạn giữa cùng model đã đạt. Mỗi mảnh phải có chủ sở hữu và hướng được kiểm.
- Lưu lượng tăng thì cột áp giảm trên cả miền. Một tiếp tuyến ngang tại điểm cô lập không phải đoạn lưu lượng tăng mà cột áp giữ nguyên.
- C0 là trùng vị trí nối; C1 là trùng độ dốc; C2 là trùng độ cong. C2 không phải điều kiện chung bắt buộc của catalogue. Giữ thân có tiếp tuyến ngang và độ cong âm có thể làm tiền tố giảm nối C2 bất khả. Dùng C1 có chứng minh và kiểm ảnh, không nhận hình thức đẹp chỉ từ công thức.
- Đỉnh và đầu nét quan sát không tự trở thành giới hạn hoặc điểm định mức do nhà máy công bố. Giữ đỉnh quan sát khi dựng lại và giữ số đã chốt; thiếu dữ liệu thì ghi CHƯA THỂ XÁC MINH.
- Chuyển tọa độ thành số thập phân phải đọc lại đúng sai số do số chữ số đã dùng. Không gọi điểm nối sau chuyển đổi là chính xác tuyệt đối khi chỉ mới có phương án phân số.
- Chữ đủ ký tự nhưng khác kiểu không được dùng để thay phông. Bỏ một chữ B không đồng nghĩa sơ đồ giải thích công suất đã hoàn tất.
- Bản dựng trong bộ nhớ và PDF đã lưu là hai mốc riêng. Chỉ tăng tiến độ sau nghiệm thu tệp thật và ghi bằng chứng.

## Mã kiểm và bằng chứng

Sổ TIEN DO.md: c43b2fa4e640309384660fc2abe7fe0ab4fde80e10f191850f13583c42753498.
Danh mục state/catalogues.json: bca14d094f2f227a5e50dcd44b05d06d36782185222f191dbd957d70f7b88d9b.
Tệp niêm phong điều khiển giữ nguyên: 437f067cfb4c220cb460dac9cecbc8862c170e4bf1b3f9ae53b6155b7ec4ed82.

- [g01_10 MANIFEST FINAL18 OWNER VA4 PHUONG AN TOAN CHUA AP.json](<C:/Users/H2/Desktop/Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/G16/G01 DINH DANH18 DOAN TANG VA PHUONG AN4 DAU 04-10-2026/g01_10 MANIFEST FINAL18 OWNER VA4 PHUONG AN TOAN CHUA AP.json>): 5ebb4a1084859182f323a564ee44b0ed08253ee8247c1992bc5f9d6e7b243a0f.
- [01 TOAN12 DAU10C2 VA2 XUNG DOT13 GIU THANQ8.json](<C:/Users/H2/Desktop/Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/G16/G18 TOAN12 DAU CDLF32 GIU JETQ8 CHI DU LIEU GON 04-10-2026/01 TOAN12 DAU10C2 VA2 XUNG DOT13 GIU THANQ8.json>): 90ee86644a73d661c2180ef2fb6c02aa0a298978d45f7bf3eebde7b2a91ff5c3.
- [g01_01 HAI DOAN GIUA1-1 XUNG DOT C2 VA C1 DIEU KIEN.json](<C:/Users/H2/Desktop/Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/G16/G01 HAI DOAN GIUA1-1 GIU THAN Q16 CHI TOAN 04-10-2026/g01_01 HAI DOAN GIUA1-1 XUNG DOT C2 VA C1 DIEU KIEN.json>): 8ba024273d1db26ccef3b24037979c5c94ff6765b77836146db8a41c76c535e3.
- [G03 CDLF186 DO HOA CHI DOC PROPOSAL CHUA AP DUNG.json](<C:/Users/H2/Desktop/Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/G16/G03 DO HOA DAU ROI VA4 NHAN DE XUAT186/G03 CDLF186 DO HOA CHI DOC PROPOSAL CHUA AP DUNG.json>): e22273ab55aa52bbba61823851e5fc01098cdfb0899b3b0b582c4edfbea59483.
- [G03 CM187 PHIEU8 COT CHU NGUON VA PHAN CHUA DU.md](<C:/Users/H2/Desktop/Catalog Sua/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/G13/G03 RA SOAT TAI NGUYEN CHU3 VIEC187/G03 CM187 PHIEU8 COT CHU NGUON VA PHAN CHUA DU.md>): ad20178eb94f02445cb765a24768f9aefd6f82a56bfe205d07d018fd83891658.
