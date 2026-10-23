# Dữ liệu dự án sửa catalogue — bổ sung ngày 04/10/2026

Tài liệu này để ChatGPT/Codex và Claude dùng chung cho lần sửa tiếp theo. Đây là kinh nghiệm đã kiểm từ các mẫu WC, không thay quy tắc gốc, sổ tiến độ hoặc quyền phê duyệt của anh Trung. File nằm trong thư mục chung; chưa xác nhận Claude đã đọc hoặc áp dụng.

## Trạng thái đã giao

Ba catalogue WC Aquaris, Perotac và Redpump đã được lưu và nghiệm thu: trang 6 sắp bảng và chú giải theo 11 → 15 → 22 → 30 kW; thêm hai mã mới và sửa cột áp tối đa của mã 30 kW theo anh Trung. Chỉ phần này đã xong; không suy thành toàn dự án đã hoàn tất.

Nguồn giữ nguyên tại `C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 01-10-2026`. Bản giao tại `C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Nước thải`.

| File giao | Mã kiểm nội dung SHA256 sau lưu |
|---|---|
| Catalog cắt rác Aquaris WC (bản mới).pdf | 6d2ae0251ee8e45445bc4f025b168c86967d38f5adaf8b1842f5cb095500a4b3 |
| Catalog cắt rác perotac (bản mới).pdf | 4366d54e6e66f58c5c7e1aa4d6aa96a5b73235bc1a3839c1ef37289f4d364034 |
| Catalog cắt rác redpump (bản mới).pdf | b5c94ffffbcf14177636ba3912675f5b71fd3cc52098d25d19769d4fe800bdf6 |

Bằng chứng giao chính thức và bản sao trước sửa: `_BAO CAO\G08\DA LUU WC11 15 22 30 VA32 NGHIEM THU 04-10-2026`. Báo cáo `BAO CAO8 COT WC11 15 22 30 VA32 DA LUU.md`; biên bản `ROOT BA WC DA LUU VA NGHIEM THU.json`, mã kiểm `a86268985ad93cc57d2df765921e9d5f22776e21cd5709ff8960aa11fb50b9d0`.

Mỗi hãng 40 đường, 435 ô số, 9 điểm chốt. Tổng 120 đường, 1.305 ô số và 27 điểm chốt. Số đếm này là phạm vi WC, không cộng thêm các lượt dựng thử hoặc lượt kiểm lại.

## Thông số đã chốt và thông số còn chờ

- 200WC200-9-11: lưu lượng tối đa 500 m³/h, cột áp tối đa 20 m, điểm làm việc 200 m³/h tại 9 m, điểm cuối 500 m³/h tại 1 m.
- 200WC220-12-15: lưu lượng tối đa 500 m³/h, cột áp tối đa 25 m, điểm làm việc 220 m³/h tại 12 m, điểm cuối 500 m³/h tại 1 m.
- 200WC250-22-30: cột áp tối đa 32 m, giữ lưu lượng tối đa 600 m³/h, điểm làm việc 250 m³/h tại 22 m và điểm cuối 600 m³/h tại 1 m.
- Hai mã mới không có số ở lưu lượng 550 và 600 m³/h; để trống, không ghi 0 hoặc kéo dài đường quá giới hạn.
- Ba đề xuất cột áp 41/25/26 m cho 150WC200-20-18.5, 250WC600-12-37 và 250WC600-15-45 vẫn chưa được anh chốt. Không dùng tài liệu này làm phê duyệt.
- Công suất lớn hơn không tự chứng minh cột áp lớn hơn khi chỉ cùng đường kính họng. Cần đối chiếu cùng họ bơm, lưu lượng, tốc độ và cấu hình cánh; không suy thông số thử máy từ công suất.

## Cách sửa chữ tránh mất khoảng cách nguồn

CATFIX là bộ công cụ sửa tài liệu đã được kiểm thử. Khi di chuyển chữ cũ, giữ phông nhúng, cỡ chữ, màu, ma trận biến đổi và vị trí tương đối từng ký tự nguồn. Không thay bằng phông gần giống.

Ở mẫu WC thử M2, dựng lại cả từ bằng `insert_like` làm mất khoảng cách điều chỉnh giữa các ký tự trong lệnh PDF `TJ`: một ký tự lệch khoảng 0,5919 điểm in. Mẫu M3 sửa bằng cách chuyển từng glyph nguồn (hình ký tự) cùng độ dịch chuyển; đọc lại vị trí từng ký tự và khoảng cách trong cụm. Không chỉ kiểm văn bản đọc ra hoặc tổng chiều rộng của từ.

Với ô đơn vị gộp, căn giữa bằng khung nét chữ thật của phông nhúng và ma trận trang. Không dùng riêng tọa độ dòng chữ hoặc khung gần đúng. Ghi rõ sai số số học còn lại; mẫu H(m) sau lưu còn khoảng 0,0001 điểm in, không gọi là tuyệt đối bằng 0.

Giữ đủ các lớp nét chữ nguồn, gồm lớp tô và lớp viền. Nếu dịch hoặc xoay một cụm nhãn, biến đổi toàn cụm cùng nhau để giữ khoảng cách nội bộ; tránh làm thiếu lớp viền hoặc tạo quầng trắng mới.

## Cách kiểm đường đặc tính

Q là lưu lượng; H là cột áp. Với từng đường Q–H đã sửa, kiểm Q tăng thì H giảm trên toàn đoạn, không chỉ lấy vài điểm mẫu. Kiểm cả đầu, thân, đuôi và chỗ nối; đường giảm vẫn có thể bị gợn hoặc gãy tiếp tuyến.

Điểm chốt do anh cung cấp phải giữ. Điểm số in trong bảng, cực trị thấy trên nét và thông số vật lý tối đa của máy là ba nguồn bằng chứng khác nhau; không tự coi chúng là một. Đường không có hàng bảng riêng không được mượn thông số từ model bên cạnh.

Kiểm riêng bề dày, màu, mối nối và khoảng hở với nhãn. Giữ nét đồng đều trong mỗi catalogue. Không cho nhãn che hoặc cắt đường để làm hình trông đạt. Nhãn Q–H ở biểu đồ phụ vẫn thuộc phạm vi kiểm; không nhầm với η (hiệu suất), P2 (công suất trục) hoặc NPSH (yêu cầu chống xâm thực).

## Cách kiểm ảnh và đọc lại PDF thực tế

PDF là định dạng tài liệu; RAM là bản dựng trong bộ nhớ. Chỉ RAM đạt chưa đủ: phải mở đúng PDF đã lưu, đọc lại chữ, số, nét, tài nguyên ảnh/phông và xem ảnh xuất từ tệp đó.

Mẫu WC cho thấy ảnh toàn trang có thể khác giữa hai trình tự đọc dù dữ liệu ảnh nguồn giữ nguyên. Nguyên nhân chưa được xác định; không kết luận lỗi thư viện hoặc sửa lại ảnh để ép khớp ảnh tham chiếu.

Quy trình so sánh đã dùng thành công: trong tiến trình mới, mở bản trước và mẫu sau; xuất đủ 8 trang của cả hai ở 200 điểm ảnh mỗi inch, rồi xuất trang 6 toàn trang ở 150 và vùng bảng/biểu đồ ở 600. Dùng cùng trình tự, màu và điều kiện cho cả trước/sau. Kiểm chữ và tài nguyên nguyên gốc trong tiến trình riêng. Giữ các lần so sánh không khớp làm hồ sơ lỗi; không xóa bằng chứng.

Không so sánh chỉ số thứ tự khối ảnh như thể đó là dữ liệu ảnh. Không đòi chuỗi từ điển PDF phải giống nguyên văn nếu lúc lưu chỉ đổi thứ tự khóa: đối chiếu toàn bộ khóa, giá trị, tham chiếu, dữ liệu ảnh nén/giải mã và chương trình phông. Mẫu WC giữ các dữ liệu này; một số từ điển phông/ảnh đổi thứ tự khóa.

Vùng kiểm thay đổi phải bao gồm đúng khung nét nguồn và nét đích. Nếu còn điểm ảnh ngoài vùng, xác định nét nào sở hữu điểm ảnh đó; không tăng đệm hoặc che nền để biến lỗi thành đạt. Trường hợp CM có 21 điểm ảnh ở chân chữ C cũ được xác định từng nét; chỉ hợp nhất đúng khung ký tự nguồn/đích.

## Bộ ảnh Perotac WC đã nghiệm thu

Cả 8 trang dùng nền studio riêng đã duyệt và giữ ảnh thân bơm thực tế nguồn. Nền khác Redpump. Giữ ảnh JPEG, mặt nạ trong suốt và vị trí/biến đổi của thân bơm; không lấy mẫu lại ảnh nguồn.

Nền studio là ảnh không có bơm; lệnh vẽ thân bơm được thực hiện sau nền. Xóa lệnh vẽ ảnh thân bơm sẽ làm mất sản phẩm, không phải chỉ bỏ ảnh cũ. Không vẽ thêm chi tiết cơ khí không có nguồn.

Biên bản cuối đủ 8 trang: `_BAO CAO\G08\G18 DOC ANH PDF FRESH DU8 TRANG\DOI CHIEU V2 DUNG PHAM VI PHOTO\04 KET LUAN ANH WC ACTUAL DA SOI DU8 TRANG.json`, mã kiểm `50194e2b99d04b90705c30491e9c2e5a4166edb1d83b96a6e7fffa4de5ff3242`.

## Giao việc và tiếp tục sau gián đoạn

Một tác nhân làm một catalogue hoặc một phần việc tách biệt; người sửa và người nghiệm thu độc lập không dùng báo cáo tác giả làm kết luận cuối. Tác nhân không tự ghi bản giao hoặc sổ tiến độ. ROOT kiểm bản thực, giữ bản sao trước sửa, ghi biên bản và cập nhật chỉ mục sau khi tiếp nhận.

Khi tiếp tục, chạy BƯỚC 0 theo hướng dẫn chung, đọc `TIEN DO.md`, lấy trạng thái hiện hành và mã kiểm mới. Không chạy lại bộ xuất WC M3 đã tiếp nhận; các mã bản giao cũ đã hết hiệu lực. Không làm lại phần đã đạt nếu đầu vào và phạm vi không đổi. Giữ riêng ĐẠT, KHÔNG ĐẠT, CHƯA THỂ XÁC MINH và CHƯA CHẠY.

Không cài phần mềm, không sửa/xóa/đổi tên file nguồn. Không dùng thao tác giao diện thay thế khi công cụ điều khiển máy được hỗ trợ đang lỗi. Không gọi file đặt trong thư mục chung là bằng chứng Claude đã áp dụng.
