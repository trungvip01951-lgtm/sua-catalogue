Chuẩn trình bày hiện hành (ảnh, biểu đồ, bảng, chữ, tệp, định nghĩa hoàn thành): rules/CHUAN_TRINH_BAY.md; quy tắc: rules/QUY_TAC_HIEN_HANH.md — lệch thì hai tệp đó thắng. Tệp này là cách làm thời catfix (03–06/10/2026); phần "chỉ catfix ghi", 43/43, bản in chỉ áp khi sửa tại chỗ bằng catfix.

# Catalogue Excel

## Đọc trước sửa

XLSX là gói ZIP có ô dữ liệu, kiểu chữ, ảnh, biểu đồ, công thức và quan hệ giữa các phần. Đọc bằng XML/ZIP hoặc công cụ có sẵn; chỉ ghi qua `catfix.xlsx.Xlsx`. Không lưu lại bằng openpyxl hay xuất công cụ bảng tính khác: có thể mất ảnh, chữ, biểu đồ hoặc thông tin ẩn.

Kiểm toàn59 ô DWO/150 ô Perotac, tên/trạng thái sheet, SGV `veryHidden` (ẩn sâu), merges (ô gộp), formulas (công thức) và giá trị cache (giá trị lưu sẵn), print setup (thiết lập in), ảnh và điểm neo. `SGV` rỗng vẫn phải giữ nguyên, không tự xóa/mở.

Ảnh dựng từ XML bằng công cụ ngoài không phải Excel render (kết quả hiển thị thực của Excel). Bản đầu DWO đã bỏ sót3 ảnh nên bị loại; bản sau đọc đủ ảnh chỉ chứng bố cục hỗ trợ, chưa chứng bản in. Nếu Office bị hộp thông báo chặn thì giữ trạng thái thật, không tự kích hoạt/cài.

## Biểu đồ đã có — Perotac SS/SSM

Nguồn có9 series (bộ điểm đường) SS150/180/250/450/750/1100/1500/2200/3000,57 ô H, Q=0/6/9/12/18/24/30/36/42/48/54/60m³/h. Đã khai báo scatter (biểu đồ tọa độ X–Y), smooth1 (làm mượt), nét19050EMU=1,5pt. Nét đồng độ dày không chứng đã hiển thị đủ9 đường.

SS150 có Hmin1,6; SS1803,9. Giữ các số này, không ép về0. Ô trống không trở thành0. SS180 có yRef2 ô trong khi xRef12 ô: cần kiểm Excel thực/chuẩn cách xử lý trước gọi là lỗi. H22/I22 có công thức đổi sang l/min; giữ công thức và giá trị lưu sẵn. Không tạo biểu đồ thứ hai trùng lên.

## Biểu đồ cần thêm — DWO

7 mã và khóa nguồn:

| Mã | Qmax m³/h | Hmax m |
|---|---:|---:|
| DWO037 | 6 | 12 |
| DWO100 | 18 | 12 |
| DWO150 | 33 | 15 |
| DWO200 | 42 | 18 |
| DWO300 | 57 | 21 |
| DWO400 | 62 | 23 |
| DWO500 | 68 | 25 |

Không có Qmin/Hmin/điểm làm việc trong nguồn. Câu hỏi dùng min0 tham khảo hay anh cung cấp min thực đang chờ; chưa có quyền tự chốt0. Đang chuẩn bị khung dưới ảnh linh kiện, đề xuất B39:P62 và2 vùng in để không thu nhỏ trang cũ; **chưa nghiệm thu bản in thực**.

Khi đủ số: thêm bảng điểm hỗ trợ/khung/biểu đồ X–Y chỉnh sửa được,7 đường cùng bộ nét, tên rõ. Ghi rõ đường tham khảo nếu dựng từ min/max. Giữ điểm làm việc rõ nếu có; không thêm điểm kỹ thuật hãng từ suy đoán.

## Khi bổ sung phần XML mới qua catfix

`Xlsx` giữ `data` (byte phần), `order` (thứ tự phần), `info` (ZipInfo/thông tin phần). `save` chỉ ghi tên trong order, nên phần mới phải đăng ký đủ cả3. Cập nhật đúng `[Content_Types].xml`, workbook/sheet/drawing relationships (quan hệ), mã rId không trùng, điểm neo và dữ liệu biểu đồ. Giữ phần gốc không sửa nguyên byte. Đừng chỉ thêm chart.xml rồi cho rằng Excel sẽ hiển thị.

Trước một ứng viên lưu mới: kiểm mọi quan hệ đích tồn tại, dữ liệu/caches đúng, dạng trục là số, blank handling (xử lý trống), không chèn lên ảnh/ô hoặc mất chữ. Rà Q tăng/H giảm từng mã, giữ extrema và điểm làm việc; kiểm cả đoạn giữa các mốc khi bật làm mượt. Mở chính XLSX đã lưu trong Excel hoặc công cụ phù hợp và kiểm trang in; không mở được thì ghi chưa thể, không đổi đạt cấu trúc thành đạt bản in.

Gói mới và phạm vi min/max Excel không cho phép đổi các điểm định mức PDF khác. Kiểm bản source/current trước và sau; không đếm kiểu định dạng hay sự có mặt chart.xml là đã xong yêu cầu đồ họa.
