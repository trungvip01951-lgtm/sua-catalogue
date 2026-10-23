# BÁO CÁO NHÓM G18 – Excel Perotac và DWO

| STT | File | Trang | Việc | Cũ | Mới | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| 66 | Catalogue perotac.xlsx | Sheet1 | Bảng DELIVERY – cột lưu lượng (ô N23/N22) | 34 m³/h = 566,7 l/min (các cột khác cách đều 6 m³/h) | 36 m³/h = 600 l/min | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 67 | Catalogue perotac.xlsx | Sheet1 | Options in request (ô A10) | "Other voltages or frequency 50Hz" | "…frequency 60Hz" (tiêu chuẩn đã là 50Hz) | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 68 | Catalogue perotac.xlsx | Sheet1 | Motor and Pump (A8) và tiêu đề bảng (B22) | "380 - 415V/50HZ" nhưng bảng ghi "380 - 420V" | Thống nhất 380-415V; "50Hz" | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 69 | Catalogue perotac.xlsx | Sheet1 | Motor and Pump (A8) | "It's available to equip with floating switch", "It's can work in water containing fiber" | "Available with float switch", "Can work in water containing fiber" | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 70 | Catalogue perotac.xlsx | Sheet1 | Bảng | SS-3000 bỏ trống ô model 1 pha; "Oil for food machinery." thừa dấu chấm; chữ "SS" dùng font .VnCooper (máy không có font sẽ hiển thị font khác) | Ghi "-"; bỏ dấu chấm thừa; đổi font chữ "SS" sang font Unicode cùng kiểu (Cooper Black) | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 120 | Catalogue DWO.xlsx | Sheet1 | Bảng TECHNICAL DATA – cột cuối (L14) | Tiêu đề "Max Head (m)" (trùng cột 4) nhưng số liệu là 2900 | Speed (rpm) | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 121 | Catalogue DWO.xlsx | Sheet1 | Cột HP (D16:D22 = kW/0.75, định dạng 0.0) | Hiện 2.9 (2,2 kW), 4.9 (3,7 kW), 6.7 (5 kW) | Ghi giá trị chuẩn: 2,2 kW = 3 HP… | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 122 | Catalogue DWO.xlsx | Sheet1 | Ảnh bảng linh kiện | Vật liệu cánh quạt "Noiyl" | Nylon | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 123 | Catalogue DWO.xlsx | Sheet1 | In ấn | Ảnh bảng linh kiện dài quá khổ, khi in dòng 14 "Fan cover" sang trang 2; "(kw)", "(m3/h)" | Thu nhỏ ảnh/đặt vùng in; (kW), m³/h | CHƯA THỂ XÁC MINH | G18/KIEM TRA DU LIEU.json; So sanh G18.png; đã đặt vừa 1 trang, chưa có bản in thực tế do Excel bị thông báo kích hoạt chặn |
| 142 | Catalogue perotac.xlsx | Sheet1, ô A11 | Warranty | Warranty: 1 years | Warranty: 1 year | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 143 | Catalogue perotac.xlsx | Sheet1, dòng 27 (C27, D27) | SS-450 / SSM-450F | 0.55 kW – 0.8 HP | 0.45 kW – 0.6 HP | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |
| 161 | Catalogue DWO.xlsx | Sheet1, dòng 21–22 | DWO400, DWO500 – cột kW | 3.7 kW; 5 kW | DWO400 = 3 kW (4 HP); DWO500 = 3.7 kW (5 HP) | ĐẠT | G18/KIEM TRA DU LIEU.json; So sanh G18.png |

Tổng: 12 việc, ĐẠT 11, còn lại 1.

ĐẠT 11/12 theo kiểm dữ liệu, XML và ảnh nhúng; còn #123 CHƯA THỂ XÁC MINH bản in. Ảnh So sanh G18.png gồm bảng đọc lại trước/sau và ảnh linh kiện; chưa phải ảnh bản in Excel. Excel 2013 báo Product Activation Failed (chưa kích hoạt); kết nối tự động bị RPC_E_CALL_REJECTED. Điều khiển cửa sổ báo coordinate input geometry is unavailable (không có hình học để thao tác). Giữ nguyên mọi phần khác, bao gồm trang SGV ẩn. Công thức D19 được đổi thành số 2, nên giá trị không đổi. Cập nhật 9 bộ lưu số liệu biểu đồ N23 từ 34 sang 36 cùng ô dữ liệu theo #66. Chưa nghiệm thu hình thức toàn trang. Chuyển việc khác theo quy tắc dừng cách làm sau 2 lần thất bại.
