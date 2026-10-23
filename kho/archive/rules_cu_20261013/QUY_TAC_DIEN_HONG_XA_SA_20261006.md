# Quy tắc cứng: điện theo công suất và họng xả 4SA nhựa

Ngày chốt: 06/10/2026. Nguồn có thẩm quyền: lời anh Trung trực tiếp trong cuộc trò chuyện dự án Sửa catalogue.

> các máy công suất 3KW trở xuống mới có điện 1 pha trên 3KW chỉ có 3 pha
>
> bơm giếng SA (giếng nhựa) 4 inch dải 12 và 16 (4sa12 và 4sa16) họng xả là 2 inch, dải 4 6 8 10 là 1.5 inch

## Điện theo công suất

| Công suất kW của máy | Quy tắc áp dụng trong bộ catalogue của anh |
|---|---|
| ≤ 3 kW, bao gồm đúng 3 kW | Có thể có bản 1 pha; bản 3 pha vẫn hợp lệ. Chỉ liệt kê biến thể thực có nguồn/model, không tự tạo thêm bản 1 pha cho mọi mã. |
| > 3 kW | Chỉ có bản 3 pha. Mã/ô/cụm 1 pha ở mức này phải ghi lỗi cần sửa theo quyết định mới. |

Không nhầm 3 kW với 3 HP; đối chiếu đúng cột công suất kW, không đổi cách hiểu P1/P2 hoặc tự suy tên hậu tố từ số pha; điện áp theo ánh xạ anh chốt ở mục bổ sung bên dưới. Chưa đọc chắc công suất/model thì ghi CHƯA THỂ XÁC MINH. Đây là quy tắc danh mục sản phẩm của anh, không tuyên bố mọi động cơ trên thị trường tuân theo giới hạn này.

## Họng xả của bơm giếng nhựa SA, đường kính thân 4 inch

| Dải bơm | Họng xả |
|---|---|
| 4SA4 | 1,5 inch |
| 4SA6 | 1,5 inch |
| 4SA8 | 1,5 inch |
| 4SA10 | 1,5 inch |
| 4SA12 | 2 inch |
| 4SA16 | 2 inch |

Áp theo đúng họ/dải model, bao gồm các model thuộc dải đó sau khi nhận diện chắc chắn. Không ghép nhầm 4SA12 với 4SA120 bằng so chuỗi con. 4 inch ở đây là cỡ thân bơm; 1,5/2 inch là họng xả. Không áp sang SP/SL/SS, SA cỡ khác hoặc dải chưa được anh nêu. Không tự đổi sang DN hoặc đường kính ngoài mm khi chưa xác định chuẩn nối/ren.

## Ghi nhận và áp dụng lần sửa tiếp

Quyết định này ưu tiên số pha/họng xả mâu thuẫn trong bảng nguồn thuộc đúng phạm vi. Lưu cũ→mới và nơi cần sửa (bảng, tiêu đề, bản vẽ kích thước, danh sách model), không tự sửa Q/H/kW hoặc bỏ cả dòng bơm 3 pha chỉ để xóa biến thể 1 pha sai. Không sửa nguồn bất biến.

Lượt này chỉ lưu quy tắc và danh sách xung đột đã nhìn thấy trong dữ liệu mẫu, chưa ghi PDF/XLSX, chưa quét nghiệm thu toàn bộ catalogue. Thư viện mẫu cũ giữ nguyên phiên bản để truy vết; khi dùng lại bắt buộc áp quy tắc mới và xử lý các cờ lỗi trước phát hành. Trạng thái PASS cũ theo nguồn không thay yêu cầu mới này.

Dữ liệu dùng cho công cụ: QUY_TAC_DIEN_HONG_XA_SA_20261006.json. Phiếu sửa thông số đã có mục kiểm số pha/công suất và họng xả/đúng dải SA.


## Điện áp theo số pha — bổ sung trực tiếp 06/10/2026

Anh Trung chốt: “điện 1 pha luôn là 220 - 240V và 3 pha luôn là 380V - 415V nhé”. Áp dụng thống nhất cho mọi catalogue Redpump, Perotac và Aquaris trong dự án:

| Số pha | Điện áp phải ghi |
|---|---|
| 1 pha / 1~ | 220–240 V |
| 3 pha / 3~ | 380–415 V |

Đây là ánh xạ đã được anh chốt, thay phần chưa được phép tự suy điện áp trong quy tắc trước. Chưa rõ số pha thì ghi CHƯA THỂ XÁC MINH, không đoán. Vẫn không tự đổi tên model/hậu tố hoặc tạo biến thể mới từ điện áp. Giữ giới hạn 1 pha ≤3 kW và trên 3 kW chỉ 3 pha.

Mỗi lần sửa/bàn giao phải đối chiếu cột điện, tiêu đề bảng, chú thích và mọi thông tin điện áp liên quan; đánh dấu chỗ khác quy tắc, sửa trong phạm vi được giao và lưu cũ→mới. Không tự thay Q/H, công suất hoặc nguồn gốc bất biến. Lượt này chỉ lưu quy tắc; chưa rà/sửa toàn bộ PDF/XLSX.



## Quyết định mới thay giới hạn phạm vi cũ

Đọc CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md: họngxả4inch dải4/6/8/10=1,5inch;12/16=2inch áp bơmgiếngnóichung,thân5inch=2,5inch,6inch=3inch. Giếng6inch vàtrụcngang3M/CM khôngcó1pha dù≤3kW. Không tự ápxảcho dải4inchchưa nêu.
