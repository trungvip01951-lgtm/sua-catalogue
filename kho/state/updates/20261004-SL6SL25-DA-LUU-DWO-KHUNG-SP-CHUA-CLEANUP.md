Mốc tiếp tục ngày 04/10/2026, sau nhận SL6SL25 lúc 11:46 giờ Việt Nam.

Đối chiếu TIEN DO.md gốc và state/catalogues.json trước làm. Đây là mốc chuyển tiếp, không thay nghiệm thu hoặc quyền anh. 135/149 việc gốc đã sửa đạt; 13 chưa xong, 1 giữ nguyên theo điều kiện #53. Các phần mở rộng không cộng vào tỷ lệ này.

| Phạm vi | Kết quả thực | Bước tiếp theo |
|---|---|---|
| Redpump SL6SL25 trang 10 | Đã nhận đúng PDF CATFIX ddb0bc676409; 10 đường/120 mốc đạt; 26 ô sửa+94 giữ; 10 nhãn và đầu/thân/khung đạt đồ họa | Bản trước b7c1febb sao lưu trong G04/SL6SL25 C2 DA LUU NGHIEM THU PHAM VI BO SUNG 04-10-2026/BAN TRUOC. Không chạy lại chương trình tiếp nhận hoặc ghi PDF. SL khác/G04 chưa xong |
| Tài nguyên SL | Kiểm đủ 128 đối tượng cũ/75 luồng và 50 đối tượng mới; 74 luồng cũ nguyên, 1 luồng trang 10 thay; 10 trang khác nguyên, đủ 11 trang ngoài vùng ở 200 điểm/inch, ngưỡng0/đệm0 bằng0 | 31 số định danh, 7 số mục lục, định danh tệp thứ hai và số đối tượng trong tổng kết tệp đổi đã khai báo. Kiểm số định danh nguyên vẫn CHƯA ĐẠT |
| Điểm ảnh khung SL | Hình thức và ảnh nguồn/ma trận giữ; lõi khung toàn trang23/44/0 tại150/200/600, chênh màu lớn nhất1/8/0; ảnh cắt4/9/0, chênh1/1/0 | Kiểm điểm ảnh khung nguyên vẫn CHƯA ĐẠT150/200. Không nới vùng/ngưỡng/bỏ mép. Các điểm khác giao vùng biểu đồ đã khóa. Nguyên nhân nội bộ dựng ảnh chưa đo riêng |
| DWO Excel | Ứng viên khung cd2f978e đã CATFIX lưu; 20 phần gói khớp RAM, 59 ô/3 ảnh và vị trí/trang SGV giữ; khung B38:S67 chưa có dãy hoặc điểm. Chưa nhận bản chính | Qmin/Hmin của 7 mã thiếu, không đặt0. Hai vùng in cấu trúc A1:S37 và B38:S67 chưa chứng hai trang thực; Excel/bản in chưa nghiệm thu. Nguồn bd2187/bản hiện hành e56968 giữ |
| SP Perotac | SP134 có13 đường cong bậc3 đơn/104 số, giảm toàn miền và sai số bảng đạt;13 đuôi khóa. Chỉ phương án toán, chưa mẫu/PDF mới | Dọn13 nét trái nguồn và mẩu mực ở-24/-30 chưa đạt;19 nhãn cần bảo vệ. Không làm lại hai phương pháp lỗi hoặc tự gán mã6SP30-8/-9. Còn15 cặp bằng ngoài phạm vi cần đọc đường thật |
| 3M,CDLF,CM,WC | Các phần đã nghiệm thu và lưu xem mốc TIEN DO00:41/05:08/07:32/09:59 ngày04/10 | Không làm lại phần đạt. Chữ/đơn vị và đường phụ thiếu dữ liệu chưa xong |

Cách được chọn cho SL:

1. Khóa bảng/trục riêng của SL. 10 đường cong bậc3 gồm40 đoạn,30 chỗ nối mượt;120 mốc theo dung sai max(1,2%). Giữ mức lớn/nhỏ nhất và đầu/cuối bảng; không suy cực đại vật lý của hãng.
2. Dọn mực cũ theo nền/lưới chính ảnh nguồn, thêm797 điểm mực đầu ở u1354..1370; giữ ảnh/trục nguồn và ma trận. Không thay phông hoặc phủ ô trắng.
3. CATFIX build() không nhả hàng đợi sửa đã áp dụng. Lần ghép lại đã áp dụng trùng472 thao tác cũ; hàm queuefix chỉ loại hàng đợi trang9 đã áp dụng, kiểm lại lệnh vẽ đúng từng byte. Không sửa mã CATFIX. Giữ bằng chứng hỏng d40ba661.
4. Giữ dữ liệu thô và mặt nạ39/40 đã khóa; đưa36 ảnh/mặt nạ từ mẫu đã kiểm vào bản hiện hành bằng CATFIX, thay luồng trang hiện có. Job.save chỉ1 lần. Số định danh đối tượng có thể đổi khi lưu. Kiểm độc lập đủ128 đối tượng qua ánh xạ hai chiều, quan hệ dùng chung, kiểu từ điển, thuộc tính nén, dữ liệu thô và toàn bộ dữ liệu giải mã. Không bỏ thuộc tính dạng mảng hay tùy ý chuẩn hóa hồ sơ màu.
5. Mở PDF thực: lệnh vẽ7184d01f,4 ảnh thực khớp mẫu,120 mốc/bảng và11 trang ngoài vùng0. Kiểm số/hình thức/bảo toàn riêng. Giữ lỗi phép so số định danh nguyên; không chạy ghi PDF lần2 để thay báo cáo.
6. ROOT chốt yêu cầu gốc và quyền mới của anh, nhận đúng byte ứng viên sau sao lưu/kiểm khóa. Chẩn đoán số định danh và điểm ảnh trong vùng biểu đồ chưa đạt vẫn giữ. Chỉ nhận phạm vi đã đạt điều kiện nội dung/thông tin/chức năng và hình thức được giao; không nhận toàn SL/G04.

Hồ sơ nghiệm thu: _BAO CAO/G04/SL6SL25 C2 DA LUU NGHIEM THU PHAM VI BO SUNG 04-10-2026; cổng01 SHA7ddcbfae, biên nhận04 SHA0ccfa7f5. Bốn phiếu thực: ef6f2369 tài nguyên, d229b0d4 số/bảng, a28a2c37 đồ họa, 3bd4cc9a ngoài vùng. Danh mục ba655ad0, sổ f0d9a2a9, mã khóa luật437f067c.

Mã phương pháp chép nguyên byte vào archive/code/SL6SL25_C2_DA_TIEP_NHAN_20261004 kèm danh mục MANIFEST. Đây là mã đã chạy; mỗi tệp có tọa độ/mã kiểm riêng và nhiều tệp chạy ngay khi nhập. Chỉ đọc, không chạy lại hoặc bỏ điều kiện khóa đầu vào. Tạo chương trình gọi mới sau đọc mã/nguồn/phiên bản nếu nhiệm vụ khác. CATFIX là bộ công cụ sửa; RAM là bộ nhớ; raw là dữ liệu thô; native là lệnh vẽ; ID là số định danh; RGB là thành phần màu; ICC là hồ sơ màu; SHA-256 là mã kiểm nội dung.
