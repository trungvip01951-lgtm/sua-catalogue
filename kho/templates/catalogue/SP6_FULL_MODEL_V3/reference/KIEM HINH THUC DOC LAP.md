# Kiểm độc lập SP trang 6 — 06/10/2026

Kết luận: **PASS hình thức trong phạm vi một trang mẫu SP6**. Đã mở ảnh toàn trang, hai ảnh đồ thị phóng lớn và cả hai bảng; đồng thời đọc trực tiếp chữ và đường vector từ PDF ứng viên. Không tham gia bố trí hoặc sửa PDF.

PDF: `deliverables/SP6 FULL MODEL NET LIEN 20261006/SP DU 12 TRANG - FULL MODEL NET LIEN.pdf`.
SHA-256 đã đọc lại: `f6701fbd513b8860fe8dc8d735c4c448bb45f5c642bfeaa36b2009abea51d7f1`.

| STT | Phạm vi | Yêu cầu | Chứng cứ thật | Kết quả | Sai lệch | Giới hạn | Bước tiếp |
|---|---|---|---|---|---|---|---|
| 1 | Nhãn 39 đường | Model đầy đủ 3 pha | PDF có đủ 39/39 model theo data_current; 21 trái và 18 phải; quan sát hai crop | PASS | Không thiếu nhãn, không còn dạng chỉ hậu tố | Kiểm trên màn hình | Không sửa |
| 2 | Q–H | Toàn bộ nét liền, cùng màu/độ dày | 39 đường Bezier thật: màu RGB 0.15/0.37/0.46; rộng 0.75 pt; dash [] 0 | PASS | 0 kiểu nét khác | Kiểm hình thức; độ khớp số do điều phối kiểm riêng | Ghép với kiểm số |
| 3 | Nhãn/đường/lưới | Chữ không bị đường xuyên | Đọc toàn bộ 39 nhãn trên hai crop; 6SP46-3A ở ngoài trái bằng nét dẫn, 6SP46-2 dưới đường; các nhãn khác trên đường và không bị xuyên | PASS | Không thấy chạm/xuyên nét chữ | Không thay phép đo khoảng cách của điều phối | Không sửa |
| 4 | Trục và đơn vị | m³/h và l/min dưới Q–H trên η; Total head H(m) dọc trục; bỏ số đếm | Cả hai đồ thị có đúng vị trí đơn vị; PDF có hai Total head H (m) xoay dọc; không có 21/18 models | PASS | 0 lỗi nhìn thấy | H(m) trong ô bảng được giữ đúng ngữ cảnh | Không sửa |
| 5 | Bảng trái/phải | Nét tất cả ô đều, nền không phủ đường | Quan sát hai bảng; PDF có 120 đoạn kẻ đồng RGB 0.32/0.48/0.56 và 0.6 pt | PASS | Không thiếu nét ở các ô dữ liệu; ô H(m) gộp có viền bao đúng | Một nét 0.4 pt phía chân trang không thuộc bảng | Không sửa |
| 6 | Điện 1 pha | Bỏ bốn model trên 3 kW | Base có sáu model 1 pha; ứng viên chỉ còn 6SPM36-2 và 6SPM46-2; bốn ô còn lại nhìn thấy dấu - | PASS | Đúng bốn model 36-3/36-4/46-3A/46-3 được bỏ khỏi cột 1 pha | Không suy sang các catalogue khác | Không sửa |
| 7 | Logo | Perotac nền trắng đồng trang | Đọc ảnh toàn trang: logo đỏ/xanh trên nền trắng, không có ô nền khác màu nhìn thấy | PASS | Không thấy ô nền | Không nhận nguồn logo là vector hoặc chất lượng in giấy | Không sửa |
| 8 | 426 H và đường 6SP36-2 | Giữ số; khớp ≤5% và C2 | data_current có 39 dòng/426 H; dòng 6SP36-2 có 10 điểm và 9 đoạn; hình đường đã đọc | CHƯA THỂ XÁC MINH toàn bộ số trong lượt kiểm hình | Chưa có kết luận sai số độc lập ở báo cáo này | Điều phối đang kiểm đủ 426 ô, sai số/C2 trên PDF thật | Chỉ nhận toàn phạm vi khi kiểm số đạt |

Giới hạn: báo cáo chỉ nghiệm thu hình thức trang 6 trên màn hình; không nghiệm thu 11 trang còn lại, toàn bộ 34 trang, bản chính hoặc bản in giấy. Cần kết quả kiểm số và bảo toàn độc lập của điều phối trước tuyên bố mẫu hoàn tất. Dữ kiện đọc PDF lưu tại `work/sp6_fullmodel/independent_pdf_facts.json`.
