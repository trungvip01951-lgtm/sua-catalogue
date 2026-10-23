# SL3SL4 và CDX — cách đã nghiệm thu và lỗi cần tránh

Phạm vi kiểm ngày 04/10/2026, kết quả là bản đã lưu thật. Đây là kiến thức bổ sung; đọc sổ chính, danh mục mới và mốc tiếp tục trước dùng. Không chạy lại các chương trình tiếp nhận một lần.

## Bản đã nhận

- SL3SL4 trang 3: ứng viên và bản giao 637c6329ebec, 7 đường/14 nét/16 đoạn cong/70 mốc/9 chỗ nối; bảng 70 số nguyên giữ. 14 giá trị đầu/cuối giữ. Sai lệch lớn nhất 1,598533 m, tỷ lệ dung sai tối đa 0,912661 theo max(1 đơn vị, 2%). Đường giảm toàn miền mở, cùng màu/nét và mượt. 178 nút/124 luồng cũ kiểm bảo toàn, chỉ thêm đúng ảnh và mặt nạ, ngoài đủ 11 trang ở 200 điểm/inch/ngưỡng 0/đệm 0 bằng 0. Khung trái 535/2591 điểm khác và 117 số định danh đổi vẫn là phép so CHƯA ĐẠT, không đổi kết quả đó. Hồ sơ G04/SL3SL4 M2 DA LUU NGHIEM THU PHAM VI BO SUNG 20261004T072439Z-ee3062; phiếu tiếp nhận04 mã927d821d95cf, đọc lại05 mã1ef5479ffd4b.
- CDX trang 4/5: bản giao5fc1a926edcc, 15 đường lệnh/112 đoạn cong/49 nét lưới; nguồn thấy 7 đường trang4 và 4 đường trang5, chữ nguồn/7 tham chiếu ảnh có sẵn. Đủ145 đối tượng phân loại, 144 nút tài nguyên/khối đóng gói kiểm quan hệ/nội dung,108 luồng thô/giải mã giữ. 4 ảnh cắt150/600 khớp mẫu hoàn toàn, ngoài đủ5 trang200/ngưỡng0/đệm0 bằng0. 22 số định danh và bảng địa chỉ/định danh tệp đổi khai báo riêng. Toàn #118 vẫn chưa xong: danh tính mã và đường thứ5 cần chứng. Hồ sơ G15/CDX M2B DO HOA NGUON DA LUU PHAM VI BO SUNG 20261004T073846Z-9838df;04 mã3a37f4d3d357,05 mãd998970b0534.

25 nguồn và24 bản giao khác giữ ở mỗi lần tiếp nhận, bản trước/sổ/danh mục/mốc được sao lưu. Cả hai nhận đúng byte CATFIX đã kiểm, không xuất lại PDF. 135/149 việc ban đầu giữ; phần bổ sung không cộng vào tỷ lệ gốc.

## Lỗi thực tế và cách xử lý đã chứng

1. Khi ghép luồng lệnh, phải có ký tự trắng/ngắt dòng giữa phần kết thúc bằng `n` và phần tiếp bằng `q`. Mẫu CDX đầu có `nq`, công cụ báo unknown keyword (từ lệnh không hợp lệ). Giữ mã/ảnh lỗi; mẫu M2B chỉ sửa ngắt dòng và đã kiểm lệnh thật/ảnh thật. Không lấy cấu trúc PDF hợp lệ làm chứng không có lỗi lệnh vẽ.
2. Danh sách đối tượng duyệt từ tài nguyên không có thứ tự ổn định qua các lần mở. Preflight131 nút CDX và lần author đầu khác thứ tự, từng nút/quan hệ/RAW/decoded/Filter vẫn nguyên. Lần lỗi chưa gọi save. So hồ sơ theo mã Ref duy nhất, vẫn so chặt mọi giá trị và báo lỗi nếu trùng mã. Đây là sửa lỗi phép kiểm, không bỏ so từ điển/nén/mặt nạ. Writer12 lưu đúng một lần; writer10/99/98 giữ.
3. Luồng ảnh có DCT hoặc Flate+DCT có thể không giải mã hết bằng `read_bytes()` tổng quát của pikepdf. Kiểm đúng Filter/DecodeParms, dữ liệu thô; với trường hợp Flate+DCT có DecodeParms[null,Quality60], đọc lớp Flate bằng zlib và ảnh RGB bằng PdfImage/Pillow. Không sửa Filter hoặc xuất lại ảnh chỉ vì reader báo không giải mã được. Phải kiểm kích thước và RGB đầy đủ của chính ảnh nguồn.
4. So ảnh phải dùng cùng điều kiện và thứ tự dựng. SL3SL4: crop trước khớp5/5; toàn trang200 trước khiến riêng cropFULL200 khác235 điểm, chênh màu tối đa1. DPI và ma trận đều cho cùng hiện tượng; trước/sau kiểm cấu trúc không ảnh hưởng. Đó là kết quả chẩn đoán thứ tự, chưa xác định chi tiết bên trong công cụ. Giữ phép khác này, không nâng ngưỡng. Reader6 dùng crop trước giống mẫu; ngoài vùng dựng toàn trang hai tệp với cùng điều kiện riêng. CDX mẫu dùng toàn trang200 trước rồi crop150/600, reader thật phải giữ đúng thứ tự đó. Chẩn đoán SL mã321776296511.
5. Duyệt Root/Info không chạm mọi đối tượng vật lý. CDX còn2 đối tượng: ObjStm là khối đóng gói (dữ liệu giữ nguyên), XRef là bảng địa chỉ (byte địa chỉ/Length/ID đổi khi lưu). Phân loại rõ, kiểm giá trị Root/Info/Size/W/Filter/DecodeParms, báo riêng thay đổi cấu trúc; không bỏ đối tượng không phân loại hoặc gọi toàn rawbytes giữ. Phiếu chẩn đoán mã16884e17fe20, reader2 mã1d1f33a3f025.
6. Phép so số định danh/điểm ảnh khung bên trong biểu đồ sửa không thay chứng bảo toàn nội dung/quan hệ/hình thức theo yêu cầu. Mọi phép kiểm thất bại giữ nguyên; không ép số định danh, không nới ngưỡng/vùng. Ngoài vùng đã khóa0/đệm0 phải bằng0.
7. Không tự yêu cầu số giữa đường cong khi làm tròn phải đúng từng số bảng nguồn nếu quy tắc chỉ yêu cầu dung sai. SL3SL4 có41/70 mốc làm tròn cùng số, nhưng70/70 đạt dung sai và bảng70 số giữ nguyên. Không dùng tiêu chí làm tròn phụ để bác hoặc nhận toàn catalogue.

## Tiếp tục

SL3SL3 đang chuẩn bị nguồn/trục/7 chữ/7 đường/91 mốc; chưa dựng mẫu. SP đang chuẩn bị đủ19 đường cùng bút,13×8 mốc và3 đuôi giữ; donor121985 đủ nhưng1258 điểm giao khác pha,349 điểm màu gần trục và6 mã chưa rõ phải kiểm riêng trên mẫu thật. DWO còn14 giá trị min (mức nhỏ nhất) thiếu và bản in thật chưa xác minh. Không biến các phần chuẩn bị thành đã nghiệm thu hoặc toàn mục tiêu hoàn tất.

Giải thích: RAW là dữ liệu thô, decoded là dữ liệu đã giải mã, Ref là mã tham chiếu đối tượng, RGB là ba thành phần màu. Preflight là kiểm đầu vào trước ghi; caller là chương trình gọi bộ sửa; writer là chương trình ghi. Các số mã rút gọn chỉ để tìm hồ sơ, phải dùng SHA-256 đủ từ biên nhận khi khóa đầu vào.
