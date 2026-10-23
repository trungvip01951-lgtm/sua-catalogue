# Mẫu thiết kế mới SP – trang 6

Trạng thái: ĐÃ TẠO MẪU; CHƯA ĐẠT ĐỂ PHÁT HÀNH. Chỉ làm một trang theo yêu cầu anh Trung, không triển khai toàn bộ ba catalogue.

`SP TRANG 6 - MAU VE LAI.pdf` là bản xem riêng một trang. `SP DU 12 TRANG - MAU MOI O TRANG 6.pdf` giữ đủ 12 trang, mẫu mới nằm ở trang 6. Hai bản có ảnh dựng trang mẫu trùng từng điểm ở 180 dpi. Các bản chính và nguồn không đổi.

| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| PILOT-SP6-01 | SP | 6 | Chữ/bảng nền ảnh khoảng 150 ppi | Chữ Arial có thể tìm kiếm, bảng vector, bố cục hai cột xanh đậm | Dựng toàn trang bằng catfix, tệp ứng viên riêng; quyền dùng phông gần và đổi thiết kế do anh giao | ĐÃ TẠO MẪU; chưa nghiệm thu toàn trang | PDF một trang và PNG trong thư mục này |
| PILOT-SP6-02 | SP | 6 | 39 mã, 426 số H | Giữ model, kW/HP, biến thể điện; 424 H giữ, 2 H trung gian thay | 6SP46-2 tại Q12:26→25; Q18:25→24 theo yêu cầu Q tăng/H giảm; đầu/cuối giữ | ĐẠT đối chiếu dữ liệu khóa và đọc lại 426 ô PDF | KIEM TRA PDF.json; hồ sơ G05/06 ACTUAL TABLE READBACK426.json |
| PILOT-SP6-03 | SP | 6 | Đường ảnh quét | 39 đường Q–H vector cùng màu/nét 0,75 pt, hai trục vật lý đều | Dùng dữ liệu đường đã kiểm, không dùng lại ngân hàng chữ ảnh/cột nhãn phải từng thất bại | ĐẠT toán riêng; CHƯA ĐẠT nhãn -2 của 6SP46 và nhiều nhãn thấp 6SP36 vì đường sát bên đi qua | Báo cáo kiểm độc lập, ảnh phóng nhãn trong work/sp6_redesign_pilot |
| PILOT-SP6-04 | SP | 6 | Đồ thị hiệu suất η ảnh quét | Đường vector theo hình nguồn, làm mượt nhiễu ảnh | Bám nét nhìn thấy; sai lệch tối đa so điểm dò ảnh nguồn khoảng 2,78/4,12 pixel | CHƯA THỂ XÁC MINH dữ liệu hiệu suất của hãng; chỉ là tái dựng hình | 01 LOCKED DATA AND NUMERIC PREFLIGHT.json |
| PILOT-SP6-05 | SP | 6 | n≈2850 và ký hiệu P2 | Mẫu hiện ghi n=2850; tiêu đề công suất chưa có P2 | Phát hiện khi kiểm độc lập, ghi lỗi để sửa ở phương án tiếp theo | CHƯA ĐẠT bảo toàn đầy đủ chú thích kỹ thuật | Báo cáo kiểm độc lập |
| PILOT-SP6-06 | SP | 1–12 | Bản chính SHA48c8535c… | Bản chính nguyên byte, ứng viên mới SHA8f1a2edc… | Kiểm nguồn/bản chính; 11 trang khác dựng 100 dpi trùng pixel, khổ/metadata/liên kết/mục lục/ảnh/phông cũ giữ | ĐẠT trong phạm vi phép kiểm ghi rõ | KIEM TRA PDF.json |

BƯỚC 0 chạy lại 43/43 ĐẠT. Phương án mới này đã có hai bản PDF thử; bản 1 lỗi bố trí nhãn/trục, bản 2 còn lỗi nhãn -2 và nhiều nhãn thấp 6SP36. Dừng phương án bố trí nhãn hiện tại theo quy tắc hai lần. Không tạo bản 3 bằng cách đổi tên hoặc nới tiêu chí. Không nhận vào bản chính, không cộng vào 137/149 việc gốc.

Logo giữ ảnh gốc; mẫu chưa chứng minh việc làm sắc nét ảnh sản phẩm vì trang này không có ảnh máy bơm. Chưa kiểm bản in giấy. Chi phí đo riêng trong BAO CAO TOKEN CREDIT.md; Credit là chênh lệch tài khoản, không phải hóa đơn riêng trang này.
