# Trích thông số catalogue đã duyệt (chỉ ĐỌC, không sửa PDF)
Nguồn PDF: $HOME/mnt/Catalog Sua/CATALOGUE DA DUYET/<HÃNG>/*.pdf (KHÔNG dùng thư mục _BAN CU).
Text đã trích sẵn (pdftotext -layout): $HOME/claude_work/txt/<tên PDF>.txt
Công cụ trên máy: python3, pdftotext, pdfinfo (không có fitz). Cần vị trí chữ thì: pdftotext -bbox-layout -f N -l N.
Không ghi gì vào $HOME/mnt/. Chỉ ghi vào $HOME/claude_work/json/<NHOM>.json và script nháp trong $HOME/claude_work/<NHOM>/.
Mọi số lấy bằng script từ text, không gõ tay, không đoán. Ô "–" = không có số (null).

## Định dạng JSON (một danh sách các dòng model)
{"brand":"PEROTAC|REDPUMP|AQUARIS","family":"CM","model":"CM 32-160/1.5" (đúng chữ in trong catalogue),
 "model_alt":"mã cặp cùng dòng nếu bảng in 2 mã 1 dòng, vd DWO037M; không có thì null",
 "phase":"3~|1~|1~/3~|null", "kW":1.5, "HP":2, "dn":"50 × 32" (họng hút × xả hoặc họng xả, đúng chữ in),
 "q_unit":"m³/h", "q_points":[...], "h_points":[...] (H theo từng điểm Q của bảng; null nếu –),
 "q_min":số Q nhỏ nhất có H, "q_max":Q lớn nhất có H, "h_at_qmin":H tại q_min, "h_at_qmax":H tại q_max,
 "rated_q":Q định mức nếu catalogue ghi riêng, "rated_h":H định mức nếu ghi riêng (không có thì null),
 "extra":{các thông số khác in trong bảng: dòng điện A, áp kPa, lưu lượng m³/min, L/h, bar, cáp, tầng cánh...},
 "page":số trang PDF}
Một model in ở nhiều bảng: gộp một dòng, ưu tiên bảng thông số chính.

## Kiểm trước khi trả
- Đếm số model mỗi hãng, so với số ghi trong DANH SACH.txt ($HOME/mnt/Catalog Sua/CATALOGUE DA DUYET/DANH SACH.txt) nếu có.
- H giảm khi Q tăng; số lạ thì mở lại text dòng đó kiểm.
- So 3 hãng: model có ở hãng này mà thiếu ở hãng kia; model cùng mã mà kW/dn/Q/H khác nhau.

## Trả về (tối đa 10 dòng, tiếng Việt)
Tệp JSON đã ghi; số model mỗi hãng mỗi họ; danh sách khác nhau giữa các hãng (gọn); chỗ không đọc được / nghi ngờ.
