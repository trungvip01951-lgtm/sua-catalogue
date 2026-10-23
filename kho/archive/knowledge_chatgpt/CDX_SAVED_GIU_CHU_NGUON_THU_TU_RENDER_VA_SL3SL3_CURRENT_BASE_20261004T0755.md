# Chữ nguồn CDX, thứ tự kết xuất ảnh và nền bản hiện hành SL

Ghi riêng từ chứng cứ ngày04-10-2026. Không thay sổ tiến độ hoặc hồ sơ nghiệm thu. Mã kiểm SHA256 là chuỗi kiểm chứng byte tệp.

CDX đã được ROOT tiếp nhận đúng tệp `5fc1a926edcc175dd00f01592f4535d7387570b7458ad72c951cfc58b7899efd`, trong phạm vi đồ họa. Việc118 vẫn chưa hoàn tất: chưa chứng minh toàn bộ tên model và đường thứ5 ở trang5. Số1–7 trên hình chỉ là chỉ số nguồn, chưa phải danh tính kỹ thuật bơm.

## Những thao tác đã có chứng thật

- Giữ nguyên ảnh nguồn trong PDF, rồi đặt bí danh tài nguyên trỏ tới chính ảnh đó. Cắt đúng vùng chữ và chỉ tịnh tiến ma trận, giữ kích thước và viền chống răng cưa nguồn. Không vẽ lại chữ đen từ đường bao hoặc ép chữ theo một phông khác.
- CDX thật có15 nét đỏ/112 đoạn Bézier (đường cong toán học), gồm7nét/81đoạn trang4 và8phầnnét/31đoạn trang5. Không ép thành117 theo một hồ sơ lịch sử.
- Bí danh7 chữ số cùng trỏ tới tài nguyên donor hiện hành đã có. Đối chiếu trực tiếp với chính PDF nguồn: toàn byte ảnh nén, mảng bộ giải mã, tham số giải mã, RGB toàn ảnh và RGB nguyên vùng chữ đều giữ. Đổi số tham chiếu sau lưu không được gọi là số tham chiếu nguồn giữ nguyên; ROOT kiểm phép ánh xạ tài nguyên riêng.
- Đọc độc lập5luồng lệnh trang của PDF đã lưu, đối chiếu byte với2native đã nghiệm thu và3trang hiện hành còn lại. Không dựa vào báo cáo tác giả để kết luận luồng lệnh thật.
- Kết xuất ảnh phải dùng cùng thứ tự với mẫu đã khóa. Với CDX M2B: tài liệu mới mở, lần lượt trang1–5; ở mỗi trang kết xuất toàn trang200điểm/inch trước; trang4/5 sau đó cắt cùng vùng ở150và600điểm/inch. Cả4ảnh PDF lưu khớp mẫu tuyệt đối0điểm ảnh khác/độ lệch lớn nhất0; PNG cũng cùng mã kiểm. Không nới ngưỡng để bỏ chênh lệch.

Phiếu độc lập CDX:

`_BAO CAO\G15\NEXT CDX SAVED ACTUAL5 NATIVE7 SOURCEALIASES4 RGB INDEPENDENT 20261004T073229Z-751943\01 INDEPENDENT CDX SAVED5 NATIVE7 ALIAS4 RGB ACTUAL NO FULL118.json`

SHA256 `70f992bfebce2a4727995e865d220862dd82144e472a1ab5016e9834b122565d`.

Phiếu mở trực tiếp4ảnh cùng thư mục: `02 DIRECT4 SAVED CDX SOURCEFONT GRID RED PASS FULL118 UNKNOWN.json`, SHA256 `c92b2572e9336fc5a163c594bf876949ed422590558b693dc4a13f06ac64c01b`.

## Lỗi công cụ cần tránh lặp

1. `pikepdf.read_bytes(generalized)` có thể báo luồng không giải mã được khi còn JPEG/DCT. Lỗi này không tự chứng ảnh đã sai hoặc bị nén lại. CDX có mảng `/Filter [/FlateDecode /DCTDecode]` và `/DecodeParms [null << /Quality60 >>]`. Reader29 giữ kiểm mảng/tham số thật, gỡ đúng lớpFlate bằngzlib vì tham số lớp đó lànull, rồi đọc RGB đầy đủ bằngPdfImage. Không chỉnh bộ giải mã trong PDF. Giữ script28 và phiếu99lỗi cũ.
2. Đừng so tài nguyên ảnh bằng thứ tự duyệt danh sách. Dùng ánh xạ duy nhất `(trang,tên)`→mã byte ảnh, kiểm mọi khóa và giá trị; khóa trùng phải dừng. CallerSL3SL3 phiên37 đã sửa đúng điểm này; giữ phiên36.
3. Thứ tự toàn trang/cắt ảnh có thể làm1mức RGB sai khác do bộ kết xuất, dù tài liệu không đổi. SL3SL4 đã có chẩn đoán: cắt trước khớp5/5; toàntrang trước làmFULL200 khác235pixel, tối đa1; bốn ảnh khác vẫnkhớp. Giữ chẩn đoán, dùng đúng điều kiện riêng của mẫu; không sửaPDF hoặc tăngdung sai. Ngoài toàn vùng dùng một phép so riêng với điều kiện giống nhau cho nguồn/current/saved.

## SL3SL3 đang chuẩn bị, chưa có mẫu RAM

Bản SL hiện hành đã có3SL4 và6SL25: SHA256 `637c6329ebec45a1b7c7271d3789678d1f711ff911099c9eea7c033eb1b5824c`. Trang2 hiện hành cóluồng lệnh `1454b16c...`, khác nguồn `4edcbbe8...` do trạng thái/sửa cósẵn; ảnh X2 gốc, RGB và ma trận của3SL3 vẫn giữ. So QH7và bảng91 ở200điểm/inch giữa nguồn/current cho0pixel khác. Vì vậy dùng bản hiện hành làm nền và nối thêm, giữ mọi lệnh cũ; không đòi toàn trang hiện hành bằng nguồn hoặc dùng nguồn làm nền rồi bỏ sửa cũ.

Plan nguồn có7đường cubic đơn,91mốc,14đoạn sau khi chia nét đứt/liền ởQ0,6. Giữ đầu/cuối bảng, giảm toàn miền mở, không đổi91số. 7nhãn nguyên RGBnguồn dự kiến dịch lên8pixel ảnh gốc, giữ cỡ/x; mới là sàng bố trí, chưa nghiệm thu hình. Các số nguyên bằng nhau trong bảng không tự là lỗi: đường giảm mượt vẫn có thể nằm đúng dung sai6(b), giữ số hiển thị nguyên. Không thêm điều kiện phải làm tròn đúng ô cũ nếu hướng dẫn chỉ yêu cầu6(b).

Nền dọn nét là **màu tính toán**, không phải byte donor nguyên: lấy trung vị theo cột/hàng của pixel trung tính trong chính JPEG nguồn, chọn tối thiểu hai trung vị rồi làm trònRGB. Chỉ nguyên vùng chữ là RGBnguồn được sao chép đúng byte. Vùng dọn32588pixel từ7dấu vết nguồn và quầngJPEG, loại chữ/trục/tiêu đề; chưa thể gọi lưới hoặc quầng đã đạt trước mẫu thật.

Plan mới trướcRAM: `_BAO CAO\G04\SL3SL3 CURRENT637C SOURCE7 CUBIC91 FONT7 RAM PREPARED 20261004T074850Z-4adbef\01 CURRENT637C EXACT7 CUBIC91 FONT7 ONE RAM PREPARED.json`, SHA256 `f2016531fe6249086e77fc206b74e0b8e4bcee3ccbb90ba5b4710114da7805df`.

Helper34 `next_work_SL3SL3_CATFIX_source7_RAM_builder34.py`, SHA256 `172f7fb8c818f5e9c18770b5223ca686204a70279747521d74f43a5b8165a00f`. Caller37 `next_work_SL3SL3_current637c_preflight_one_RAM_caller37_assetmap.py`, SHA256 `1c117b1c08acd3ad6cad7356507404f530bb2959e0c8c221386d4919c77d1862`.

Chỉ sau ROOT/kiểm độc lập mới dựng đúngmột mẫuCATFIX trongbộ nhớ. Trước đó kiểm nguồn/current/khóa phiên sống, sau đó giữ10trang khác (đặc biệt3/10), bảng/η/tiêu đề và ngoài toàn đồ thị; đo mọi chênh khung riêng. Chưa có quyền nhận toànSL/G04 từ plan này; chưa lưuPDF3SL3.
