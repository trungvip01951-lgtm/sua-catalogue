# PHƯƠNG ÁN ĐÃ DUYỆT 13/10/2026 — cập nhật quy tắc, công cụ, dữ liệu, skill (KHÔNG làm lại catalogue)

Anh Trung 13/10/2026 21:06: "a k cần làm lại các catalogue cũ a đã duyệt bây giờ chỉ cần cập nhật dữ liệu dự án hay skill hay hướng dẫn để về sau làm sẽ tốt hơn tối ưu hơn ... nói cho a những thứ e sẽ thay đổi trước a duyệt mới cập nhật nhé"
Anh Trung 13/10/2026 21:18: "ok cập nhật cho a nhé". Anh Trung 13/10/2026 21:22 trả lời theo số: "1. 1 / 2. 1 / 3. 3.2 / 4. 4.1 / 5. 5.1 / 6. 6.1 / 7. 7.1".
Tài liệu: https://claude.ai/code/artifact/df40d71e-7d3e-46e1-aee0-3440e3b0b0b1 (bản cũ hơn: claude/PHUONG_AN_HOAN_THIEN_20261013.md — tệp NÀY thắng khi lệch).

## Quyết định
- 62 PDF trong CATALOG SUA/CATALOGUE DA DUYET giữ nguyên, không làm lại; lỗi thấy trên bản cũ chỉ là bài học, chỉ sửa khi anh ra lệnh sửa catalogue đó. Không xoá tệp nào; tệp cũ bị thay chuyển sang archive/.
- 1.1 Làm đợt A→D. 2.1 Áp đúng cột "Đề xuất" bảng mâu thuẫn (dưới). 3.2 IRG KHÔNG vẽ đường cong (giữ QĐ 71). 4.1 Dưới biểu đồ ghi khối điều kiện + "Typical values, not guaranteed"; chỉ ghi "ISO 9906:2012 Grade 3B" khi nhà cung cấp xác nhận. 5.1 Bản mới chỉ khổ A4: AQUARIS dọc 595×842, PEROTAC và REDPUMP ngang 842×595. 6.1 Chữ thân ≥9 pt, số bảng/nhãn trục/nhãn đường ≥7 pt (nên 8). 7.1 Ảnh tự tạo/vẽ lại được làm nhưng phải gửi anh duyệt trước khi dùng.

## Mâu thuẫn — áp dụng
| Điểm | Áp dụng |
|---|---|
| Bảo hành | Không ghi mọi catalogue (QĐ 32) |
| Dòng điện A | Giữ cột A; mã thiếu thì tự suy từ mã công suất lớn hơn (QĐ 70) |
| Cột áp H | H có số lẻ theo nguồn thì giữ (QĐ 25) |
| Phạm vi hãng | FS/FC cả 3 hãng (FS=AQUARIS, FC=PEROTAC/REDPUMP, cả bản inox); Root RL PEROTAC+REDPUMP; KTZ-LH cả 3; định lượng JLM-JBB chỉ AQUARIS; đĩa phân phối khí PEROTAC+REDPUMP; SL không làm; còn lại cả 3 |
| Đường IRG | Không vẽ đường (QĐ 71, anh chọn 3.2 ngày 13/10); mọi nhóm khác mặc định có đường |
| Ảnh | Được vẽ lại/tự tạo, gửi anh duyệt trước (QĐ 13/10 + 7.1) |
| DWO | Số theo Ebara (QĐ 44), bỏ DWO500 (QĐ 55) |
| Cách làm PDF | Dựng mới là cách chính; catfix chỉ cho sửa tại chỗ bản gốc; 43/43 chỉ bắt buộc khi dùng catfix |
| Kiểm bản in | Bỏ; PDF chỉ đăng web và gửi Zalo (QĐ 2) |
| Cân nặng | Không ghi cân nặng (QĐ 102(6)); GIỮ bảng kích thước và họng hút/xả (đính chính 13/10: bản đầu ghi nhầm "không ghi D×R×C" — đó là quy tắc web) |

## Hồ sơ hãng (giữ màu đã đo trên bản duyệt)
| Trục | AQUARIS | PEROTAC | REDPUMP |
|---|---|---|---|
| Khổ | A4 dọc 595×842 | A4 ngang 842×595 | A4 ngang 842×595 |
| Màu | xanh rêu #0D6159, nền #F0F7F5 | xanh than #13334D, đường #1A669E, nền #EDF5FA | than #2B2E33, đỏ đô #A31A1F, nền #F7F2F0 |
| Đồ họa phụ | dải cờ Ý #009246/#FFFFFF/#CE2B37 | băng đầu trang xanh nhạt | cột tối trái 28–30% bề ngang |
| Phông | Lato | Liberation Sans | Liberation Sans |
| Bìa | ảnh trên trái, ô số liệu nổi bật, nhiều khoảng trắng | logo trái, chia 3 cột | cột tối trái chứa tên dòng + dải hiệu năng, ảnh bên phải |
| Biểu đồ | mỗi model một màu (Okabe–Ito bỏ vàng), số khoanh tròn + chú giải | 1 tông xanh, tên model đầu trái đường, trục H trái | đỏ/xám, tên model trong ô màu cuối phải đường, trục H phải, nền biểu đồ xám rất nhạt |
| Bảng | mỗi model một cột, kẻ ngang mảnh | mỗi model một dòng, kẻ đầy đủ mảnh | mỗi model một dòng, đầu bảng nền tối chữ trắng, sọc xám xen kẽ |
| Ảnh | nền trắng, bóng tiếp xúc mờ | nền trắng, không bóng | nền trắng, bóng đổ dưới đế |
3 bản cùng dòng khác ≥5/6 trục (màu, phông, bìa, bảng, biểu đồ, đồ họa phụ); P–R cùng phông nên 5 trục kia bắt buộc khác. Cấm chung khuôn biểu đồ/bảng rồi chỉ đổi màu, lật trái-phải, đảo khối. Mẫu nhìn theo: CM và MIX. Không chép logo/màu/bố cục hãng thật.

## Chuẩn ảnh
Nền RGB 255 hoặc trong suốt, cấm nền trang trí; ≥200 ppi tại kích thước đặt (bìa ≥300), ảnh gốc cạnh dài ≥1000 px; bản vẽ cấu tạo vector hoặc ≥200 ppi; sản phẩm 80–85% cạnh dài ô, căn giữa; cùng góc, cùng hướng sáng trên-trái, cùng tông, cùng kiểu bóng theo hãng; bóng tiếp xúc độ đục 15–25%; mỗi cỡ một ảnh (trừ khi anh cho phép); xoá sạch logo/chữ hãng gốc; soi viền trên 3 nền trắng/xám #808080/đen, phóng 300%: không quầng, răng cưa, sót nền trong khe, cắt cụt. Kho ảnh KHO_ANH/<nhóm>/<model>_<hãng>.png có trạng thái ĐẠT / CẦN THAY KHI CÓ DỊP.

## Chuẩn biểu đồ và bảng
Đường và bảng sinh từ một tệp số liệu DU_LIEU/<nhóm>.xlsx; nội suy PCHIP qua đúng điểm; Q tăng H giảm; lệch ≤5%; không móc đầu/cuối; giữ Qmin/Qmax/Hmin/Hmax/điểm làm việc; chạy hết dải Q. Trục Q m³/h chính + l/min phụ (×16,667), H m; bỏ gpm. ≤8 đường/biểu đồ, nhiều hơn thì tách. Nét đường ≥1,5 pt, lưới chính 0,5 pt, nét tương phản ≥3:1. Nhãn sát đường, cùng màu, không bị đè. Nét đứt vùng khuyến nghị chỉ khi nguồn có; không tự nội suy η/NPSH khi nguồn không có. Khối điều kiện dưới biểu đồ: "Curves at 50 Hz, 2 poles (≈ 2900 min⁻¹), clean water at 20 °C, kinematic viscosity 1 mm²/s. Typical values, not guaranteed." (số cực/tốc độ theo nguồn).
Bảng: Model 1 pha | Model 3 pha | P2 kW | P2 HP | A | các cột Q (hàng m³/h trên, l/min dưới), ô là H (m); "–" chỉ ở cột 1 pha, không giữa dãy H; điện "1~ 220–240 V 50 Hz", "3~ 380–415 V 50 Hz"; HP theo nguồn; dấu chấm thập phân; số căn phải; cùng dải thì model lớn hơn cho Q hoặc H lớn hơn tại cùng điểm. Thiết bị không phải bơm ly tâm (GB, RL, máy khuấy, định lượng, đĩa phân phối khí): lấy bản đã duyệt làm mẫu.

## Chuẩn chữ, tệp
Tiêu đề trang ≥16 pt; thân ≥9 pt, dòng ≥120%; bảng/nhãn ≥7 pt (không đủ chỗ thì tách trang, không thu chữ); tương phản chữ ≥4,5:1 (lớn ≥3:1); ≤2 phông/tệp; lề 12–15 mm, lưới 12 cột; vùng trống liền ≤10% chiều cao trang; chỉ A4; "50 Hz" ở trang đầu mọi sản phẩm có động cơ. Tệp ≤5 MB (tối đa 10), RGB, phông nhúng một lần dạng rút gọn, gộp ảnh trùng, lưu garbage=4 + deflate, ảnh JPEG 80–85% (PNG nếu trong suốt); tên "HÃNG - Tên dòng.pdf". Cấm: bảo hành, cân nặng, 60 Hz, tiếng Việt, ô "*" (giữ bảng kích thước).

## Mẫu lệnh 6 ô
1 Việc: Tạo mới | Sửa | Đổi ảnh · 2 Dòng bơm · 3 Hãng: PEROTAC | REDPUMP | AQUARIS | Cả 3 · 4 Sửa gì (model — thông số — cũ → mới; hoặc trang) · 5 Tệp đính kèm · 6 Ghi chú. Lệnh ngắn vẫn được ("Sửa CM PEROTAC: … 32 → 34", "Duyệt …", "Trả lại …: …"). Thiếu ô nào hỏi ô đó một lần, lựa chọn đánh số. AI gửi lại theo mẫu: ảnh xem trước trang đổi 3 hãng cạnh nhau; bảng cũ → mới; phiếu kiểm tự động; câu hỏi gom một lần.

## Định nghĩa hoàn thành
Số khớp tệp số liệu gốc (nghi ngờ thì liệt kê, không tự sửa); kiem_catalogue.py đạt 10 mục; trang đường cong có khối điều kiện; ảnh đạt chuẩn, đã soi 3 nền, ảnh tự tạo đã được duyệt; 3 bản khác ≥5/6 trục, số giống từng ký tự; AI khác kiểm thẩm mỹ độc lập; phiếu QA có KHÁC GIAO DIỆN GIỮA CÁC HÃNG và ĐƯỜNG CONG ĐỀU, mỗi yêu cầu ĐẠT / CHƯA ĐẠT / CHƯA THỂ XÁC MINH; thiếu dữ liệu không đoán, không điền 0.

## Công cụ (tools/)
kiem_catalogue.py (10 mục: chữ cấm + 50 Hz; điện/pha; bảng Q↑H↓, "–", thứ tự công suất, số model = số nhãn; đường ≤5%, điểm uốn, móc, ≤8 đường; chữ chồng, cỡ chữ; ảnh ppi, tràn mép, chồng 2 lần, 1 ảnh nhiều cỡ; tương phản; tệp A4/dung lượng/phông lặp/RGB/khoảng trống; khác giao diện 3 hãng; mã kiểm khớp DANH SACH) · ve_duong_cong.py (vẽ Q–H + bảng từ DU_LIEU theo hồ sơ hãng) · nhan_ban_chinh.py (sao lưu history/, chép vào DA DUYET, đọc lại mã kiểm, cập nhật DANH SACH, TIEN DO, TRANG_THAI) · dong_bo_drive.py (chép phần đổi sang gói "Sửa catalogue - DRIVE NV", đóng skill NV, ghi số phiên bản).

## Cách cập nhật về sau
Nơi gốc: rules/ (quy tắc, hồ sơ hãng, chuẩn), DU_LIEU/, KHO_ANH/, templates/<nhóm>/ (mã dựng đạt), CATALOG SUA/CATALOGUE DA DUYET/. Quyết định mới: ghi nguyên văn vào rules/QUYET_DINH_ANH.md + sửa tệp hiện hành cùng lượt + (nếu là lỗi) thêm phép kiểm + tăng số phiên bản + dong_bo_drive.py + báo anh 1 dòng. Không bao giờ xoá rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/; nháp để ngoài kho.
