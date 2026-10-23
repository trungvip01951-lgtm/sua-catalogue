# Chuẩn trình bày catalogue — ảnh, biểu đồ, bảng, chữ, tệp, mẫu lệnh, mẫu trả lời, định nghĩa hoàn thành

Nguồn: phương án anh Trung duyệt 13/10/2026 (rules/QUYET_DINH_ANH.md mục 147–149; claude/PHUONG_AN_DA_DUYET_20261013.md). Giá trị số máy đọc: rules/HO_SO_HANG.json. Quy tắc nội dung (mã, điện, số liệu): rules/QUY_TAC_HIEN_HANH.md.
Áp cho bản DỰNG MỚI hoặc trang được sửa. 62 PDF đã duyệt giữ nguyên, không làm lại.

Thuật ngữ: **pt** = point, 1/72 inch (đơn vị cỡ chữ, nét). **ppi** = số điểm ảnh trên mỗi inch khi ảnh nằm đúng cỡ trên trang. **RGB** = hệ màu màn hình. **PCHIP** = cách nội suy (nối điểm) giữ đúng chiều tăng/giảm, không tạo gợn. **Q** = lưu lượng (m³/h), **H** = cột áp (m). **Điểm làm việc** = cặp Q–H định mức theo tên model.

## 1. Ảnh sản phẩm

1. Nền trắng RGB 255 (#FFFFFF) hoặc trong suốt. Cấm nền trang trí: nước bắn, phông xám, đế trưng bày, hộp, túi, cuộn cáp, vật thừa.
2. Độ nét: ≥ 200 ppi tại kích thước đặt trên trang; ảnh lớn ở bìa ≥ 300 ppi; ảnh gốc cạnh dài ≥ 1000 px. Bản vẽ cấu tạo/bản vẽ nổ: dạng vector (nét vẽ, phóng không vỡ) hoặc ≥ 200 ppi. Không phóng ảnh nhỏ rồi gọi là nét hơn.
3. Bố cục: sản phẩm chiếm 80–85% cạnh dài ô ảnh, căn giữa; đủ nguyên thân bơm — không cắt/lẹm nắp, bulong, tai móc, cáp, mặt bích, chân đế.
4. Đồng bộ trong một catalogue: cùng góc nhìn, cùng hướng sáng (trên-trái), cùng tông màu, cùng kiểu bóng theo hãng (AQUARIS bóng tiếp xúc mờ; PEROTAC không bóng; REDPUMP bóng đổ dưới đế). Bóng tiếp xúc độ đục 15–25%.
5. Mỗi cỡ/model một ảnh riêng; dùng chung một ảnh cho nhiều cỡ chỉ khi anh cho phép.
6. Xoá sạch logo, chữ, tem của hãng gốc in trên ảnh.
7. Soi viền: đặt ảnh lên 3 nền trắng, xám #808080, đen; phóng 300%: không quầng sáng, không răng cưa, không sót nền trong khe, không cắt cụt.
8. Ảnh anh gửi là ảnh mẫu → tách nền, làm sạch, căn đẹp. Được vẽ lại một phần hoặc tự tạo ảnh mới dựa trên ảnh mẫu (giữ đúng cấu tạo), NHƯNG phải gửi anh duyệt trước khi dùng. Một AI khác so ảnh gốc với ảnh làm, phóng từng vùng, xác nhận không lẹm.
9. Kho ảnh: KHO_ANH/<nhóm>/<model>_<hãng>.png; mỗi ảnh ghi trạng thái ĐẠT hoặc CẦN THAY KHI CÓ DỊP. Catalogue sau lấy ảnh từ kho, không cắt lại.

## 2. Biểu đồ Q–H

1. Đường và bảng sinh từ MỘT tệp số liệu DU_LIEU/<nhóm>.xlsx (không gõ số hai nơi).
2. Nối điểm bằng PCHIP đi qua đúng điểm dữ liệu; Q tăng thì H giảm; lệch đường so với bảng ≤ 5% tại từng điểm; không móc đầu/cuối, không gợn; giữ Qmin, Qmax, Hmin, Hmax, điểm làm việc; đường chạy hết dải Q của bảng.
3. Trục: Q m³/h là trục chính, l/min là trục phụ (l/min = m³/h × 16,667); H tính bằng m. Bỏ gpm (đơn vị Mỹ).
4. ≤ 8 đường mỗi biểu đồ; nhiều hơn thì tách biểu đồ.
5. Nét đường ≥ 1.5 pt; lưới chính 0.5 pt; nét so với nền tương phản ≥ 3 : 1.
6. Nhãn đường sát đường, cùng màu đường, không bị đè, không chồng nhãn khác. Kiểu nhãn theo hãng (AQUARIS số khoanh tròn + chú giải; PEROTAC tên model đầu trái đường; REDPUMP tên model trong ô màu cuối phải đường).
7. Nét đứt vùng khuyến nghị chỉ vẽ khi nguồn có. Không tự nội suy hiệu suất η hoặc NPSH khi nguồn không có.
8. Dưới biểu đồ luôn có khối điều kiện: "Curves at 50 Hz, 2 poles (≈ 2900 min⁻¹), clean water at 20 °C, kinematic viscosity 1 mm²/s. Typical values, not guaranteed." (số cực và tốc độ theo nguồn). Chỉ ghi "ISO 9906:2012 Grade 3B" khi nhà cung cấp xác nhận.
9. Mọi nhóm có biểu đồ, TRỪ IRG (chỉ bảng). Thiết bị không phải bơm ly tâm (GB, Root RL, máy khuấy, định lượng, đĩa phân phối khí): lấy bản đã duyệt làm mẫu.

## 3. Bảng thông số

1. Cột (bảng mỗi model một dòng — PEROTAC, REDPUMP): Model 1 pha | Model 3 pha | P2 kW | P2 HP | A | các cột Q. Hàng đầu các cột Q ghi m³/h, hàng dưới ghi l/min; ô là H (m). AQUARIS xoay bảng (mỗi model một cột) nhưng giữ đủ các trường trên.
2. Dấu "–" chỉ ở cột model 1 pha (model không có bản 1 pha) hoặc ngoài dải chạy của bơm; không bao giờ ở giữa dãy H.
3. Điện ghi "1~ 220–240 V 50 Hz" và "3~ 380–415 V 50 Hz". HP theo nguồn. Dấu chấm thập phân. Số căn phải.
4. Cùng dải: model lớn hơn cho Q hoặc H lớn hơn tại cùng điểm (thứ tự công suất).
5. Số model trong bảng = số nhãn đường trên biểu đồ (trừ IRG).
6. Kẻ bảng theo hãng (AQUARIS kẻ ngang mảnh; PEROTAC kẻ đầy đủ mảnh; REDPUMP đầu bảng nền tối chữ trắng, sọc xám xen kẽ). Nét kẻ vẽ sau toàn bộ nền ô, cùng màu, cùng độ dày.

## 4. Chữ và bố cục

1. Tiêu đề trang ≥ 16 pt; chữ thân ≥ 9 pt, giãn dòng ≥ 120%; số trong bảng, nhãn trục, nhãn đường ≥ 7 pt (nên 8). Không đủ chỗ thì tách trang, không thu nhỏ chữ.
2. Tương phản chữ/nền ≥ 4.5 : 1 (chữ lớn ≥ 3 : 1).
3. ≤ 2 phông mỗi tệp (AQUARIS Lato; PEROTAC, REDPUMP Liberation Sans).
4. Lề 12–15 mm; lưới 12 cột; vùng trống liền ≤ 10% chiều cao trang.
5. Chỉ khổ A4: AQUARIS dọc 595×842 pt; PEROTAC, REDPUMP ngang 842×595 pt.
6. "50 Hz" có ở trang đầu mọi sản phẩm có động cơ.
7. Cấm: bảo hành, cân nặng/khối lượng, 60 Hz, tiếng Việt, ô "*". GIỮ bảng kích thước và họng hút/xả (QĐ 114 mục (6): "bỏ cân nặng (kg) ở MỌI catalogue, giữ kích thước"; quy tắc bỏ kích thước D×R×C chỉ áp cho trang sản phẩm/bài viết web).

## 5. Tệp PDF

1. ≤ 5 MB mỗi tệp (tối đa 10 MB); hệ màu RGB.
2. Phông nhúng một lần, dạng rút gọn (chỉ các ký tự dùng); gộp ảnh trùng; lưu với garbage=4 + deflate (nén, bỏ phần thừa); ảnh JPEG chất lượng 80–85% (PNG nếu cần trong suốt).
3. Tên tệp: "HÃNG - Tên dòng.pdf" (vd "PEROTAC - Bơm trục ngang CM.pdf").
4. Mã dựng đạt lưu ở templates/<nhóm>/ để lần sau sửa nhanh.

## 6. Mẫu lệnh 6 ô (người phụ trách dự án giao việc cho AI)

| Ô | Điền gì | Ví dụ |
|---|---|---|
| 1. Việc | Tạo mới / Sửa / Đổi ảnh | Sửa |
| 2. Dòng bơm | tên dòng | CM |
| 3. Hãng | PEROTAC / REDPUMP / AQUARIS / Cả 3 | PEROTAC |
| 4. Sửa gì | model — thông số — cũ → mới; hoặc số trang | CM 32-160/2.2 — H tại Q 12 — 32 → 34 |
| 5. Tệp đính kèm | nguồn, ảnh | ảnh bơm mới |
| 6. Ghi chú | điều đặc biệt | áp cả 3 hãng |

Lệnh ngắn vẫn được: "Sửa CM PEROTAC: CM 32-160/2.2 H tại Q 12: 32 → 34", "Tạo catalogue <dòng> cho <hãng>. Nguồn: <tệp>", "Đổi ảnh <model> trong catalogue <dòng> hãng <…>", "Duyệt <tên>", "Trả lại <tên>: <lỗi>". Thiếu ô nào thì AI hỏi đúng ô đó MỘT lần, lựa chọn đánh số.

## 7. Mẫu trả lời của AI sau mỗi việc

1. Kết luận một dòng: ĐẠT / CHƯA ĐẠT / CHỜ ANH.
2. Ảnh xem trước các trang đổi, 3 hãng đặt cạnh nhau.
3. Bảng thay đổi: model | thông số | cũ → mới | loại số (nguồn / suy ra / dựng) | trang.
4. Phiếu kiểm tự động (tools/kiem_catalogue.py, 10 mục) + kết quả kiểm mắt.
5. Câu hỏi gom một lần, mỗi câu có dẫn chứng cụ thể (model, trang, số) và lựa chọn đánh số 1, 2, 3; câu cũ chưa trả lời gộp vào. Thuật ngữ tiếng Anh phải dịch.
6. Đường dẫn tệp ứng viên và mã kiểm SHA-256 (12 ký tự đầu).

## 8. Định nghĩa hoàn thành (chỉ khi đủ cả 8 điều)

1. Mọi số khớp tệp số liệu gốc; số nghi ngờ thì liệt kê, không tự sửa.
2. tools/kiem_catalogue.py đạt đủ 10 mục: (1) chữ cấm + có 50 Hz; (2) điện/pha; (3) bảng: Q tăng H giảm, dấu "–" đúng chỗ, thứ tự công suất, số model = số nhãn; (4) đường: lệch ≤ 5%, không điểm uốn, không móc, ≤ 8 đường; (5) chữ không chồng, đủ cỡ; (6) ảnh: ppi, không tràn mép, không đặt chồng 2 lần, không một ảnh cho nhiều cỡ; (7) tương phản; (8) tệp: A4, dung lượng, phông không lặp, RGB, vùng trống; (9) 3 hãng khác giao diện; (10) mã kiểm khớp DANH SACH.txt.
3. Trang có đường cong có khối điều kiện.
4. Ảnh đạt mục 1, đã soi 3 nền; ảnh tự tạo/vẽ lại đã được anh duyệt.
5. 3 bản cùng dòng khác ≥ 5/6 trục; số giống nhau từng ký tự.
6. Một AI khác kiểm thẩm mỹ độc lập trên PDF thật.
7. Phiếu QA có hai mục riêng **KHÁC GIAO DIỆN GIỮA CÁC HÃNG** và **ĐƯỜNG CONG ĐỀU**; mỗi yêu cầu ghi ĐẠT / CHƯA ĐẠT / CHƯA THỂ XÁC MINH, kèm tệp, mã kiểm, trang đã xem, người kiểm.
8. Thiếu dữ liệu thì không đoán, không điền 0 — ghi CHƯA THỂ XÁC MINH và hỏi anh.
