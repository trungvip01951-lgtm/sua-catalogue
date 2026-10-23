# G09 Redpump — bàn giao staging v4

Chỉ sửa khe hở lưới H50 cạnh LH845, đồ thị 60Hz trang 7. Candidate chờ chủ việc kiểm độc lập và quyết định ghép canonical; không xác nhận hoàn thành toàn catalogue.

| File | Trang | Vị trí | Trước | Sau | Cách sửa | Kiểm chứng | Trạng thái |
|---|---|---|---|---|---|---|---|
| KTZ - LH Redpump (bản mới).pdf | 7 | 60Hz, H50 cạnh LH845 | khe nền trắng đo native 14.30326244635 pt | còn 9.30239394635 pt; giảm 5.0008685 pt (~35%) | hai clip even-odd cô lập trên hai nền trắng gốc, chỉ mở mép trống bên trái | 62 đường/style và 96 mốc bảng giữ nguyên; strict ngoài ROI 0 | STAGING — chờ root duyệt |

ROI gốc bottom-left: [401.58033150000006, 386.77239959999997, 416.6035939463506, 388.1924004]. Cutout: [401.58033150000006, 386.77239959999997, 406.9412, 388.1924004]; cách mép glyph đen 0.37 pt. Giữ nguyên lưới gốc rộng 0.7000008 pt và tất cả lệnh vẽ gốc; không thêm nét đen hay sơn trắng. Khe còn lại bao quanh chữ 845 để giữ nét chữ. Số lịch sử 14.27512168353752 pt không dùng làm chuẩn; lấy giao polygon gốc tại y=387.4824.

B0 gói nguyên bản: 43/43 PASS, log `../B0-tests-shortpath.txt`; lần đầu Tesseract lỗi đường dẫn unicode dài, đã giải quyết bằng short path Windows trong cùng staging, không cài thêm hay sửa catfix. Lưu qua catfix PdfDoc.set_stream + Job.save, backend fitz.

QA: 7 trang render/so sánh 200 và 600 dpi; xem toàn bộ trang 200 dpi, 28 quadrant 600 dpi; ROI xem 200/600/1200 dpi. Strict pixel ngoài ROI chưa nới: 0 ở mọi trang tại 200/600 dpi và region1200. Diagnostic chuẩn catfix dpi200, thr48/min2/pad2/merge4: không phát hiện ngoài ROI. Trang1–6 không đổi điểm ảnh hoặc native stream. Bảng Performance trang7 crop600dpi giống từng pixel; đủ 32 dictionary khóa/96 anchors baseline giữ nguyên bằng bảo toàn lệnh vẽ, không tuyên bố tái OCR số liệu. 62 path/style đối chiếu native độc lập PASS; cả hai glyph 845, mask đỏ region1200 và crop glyph1200 giống gốc current. Resources, non-P7 raw stream multiset, Info, XMP raw/decoded, outline và annotations giữ nguyên. Cấu trúc 7 trang, chỉ P7 stream thay đổi.

Draft không được chọn: v1 có seam và làm tròn width; v2 pikepdf đổi XMP raw/decoded; v3 ghép Q/q sai gây chênh ngoài ROI. Đã giữ hồ sơ các bản loại; v4 sửa ghép lệnh và kiểm cân bằng q/Q, qua toàn bộ QA nêu trên.

PDF SHA256: `2dcdb269de340c72e607ce18d63fa0a1f34a7f0b8f529c71a9ca17a6950c75e5`.
Source SHA256 nguyên vẹn: `396487b4b47f836601d97bfa708fb242007c462951f7a3109b24c6f446975858`.
Current SHA256 nguyên vẹn: `f20b82e880ee756e101a41fdddea87c249d2fc65e48f1532a76022ae81248ed4`.

Chứng cứ: `QA/QA-machine.json`, `QA/QA-visual.json`, `QA/COMPARE-SOURCE-CURRENT-CANDIDATE-200.png`, `-600.png`, `-1200.png`, `plan.json`, các render trang/quadrant và script `../redpump_candidate_v4.py`, `../redpump_qa.py`. Không ghi source/current/canonical, control, ledger, progress hoặc lock toàn cục. Không sửa Perotac, SP, SL6 hay mã catfix.

Còn lại: chủ việc kiểm độc lập clipping/mép glyph và chấp nhận phạm vi cải thiện này trước khi ghép canonical.
