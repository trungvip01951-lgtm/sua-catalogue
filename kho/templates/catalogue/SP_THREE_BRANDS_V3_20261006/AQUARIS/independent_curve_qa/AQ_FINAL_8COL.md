# AQUARIS SP cuối — kiểm số và đường độc lập với bộ dựng

PDF: `deliverables/SP BA HANG THIET KE RIENG 20261006/AQUARIS SP - 31 TRANG.pdf`
SHA8170fe4d6b745c1a9e6c900b95282f7c4f8dbfe54251e2c235c76890d6774baf.

**ĐẠT phạm vi số Q/H và hình học đường.** Không thay thế kiểm hình thức, ảnh, vật liệu, kích thước/cân nặng hoặc in giấy.

| Mã | Phạm vi | Nguồn | Cách kiểm | Số lượng | Kết quả | Giới hạn | Bằng chứng |
|---|---|---|---|---|---|---|---|
|AQ-N1|Bảng actual|Own-source records; metadata agent đọc20ảnh|Đọc mọirowtext từPDF cuối, soH/kW/HP|197model/1179H/197kW/197HP|0lệch; Hkhôngđổi|Người thiết kếhàmfit cũng làm kiểm này; độc lập với writer, khôngđộc lập với thiết kếfit|AQ_FINAL_NUMERIC_SHAPE.json|
|AQ-N2|Trục actual|Ticklabels vàgridline thực|Đọc vịtrígrid/text, xác định affine Q/H; khôngnhập layoutplan/writer|20biểu đồ|Q/H tuyến tính, mỗi197curve đúngmodel|Khôngsuytrục từendpoint bảng|axis trongJSON|
|AQ-N3|Đường actual|Toántửthậpphân PDF +CTM|Lấycontrols thực, đánhgiácubic ở1179Q|197đường|Sai lệchmax4,99900000184%≤5%|Khôngápngưỡng2%cũ|checks/H_points|
|AQ-N4|Congđều/Hgiảm|Đạohàm từcontrolsactual|Kiểm cực trị giải tích dH/dQ vàd²H/dQ²; biênnhiễu dựavào sai sốcontrolsraPDF|Toànmiền197đường|Khônggợn/khônguốnngược vật lý; vùngH''=0 nằmtrongbiênroundingchứngminh|Khônggọinhiễu3,98e−11 làđổiđộcong thực|checks/shape;8SP77_2_actual_rounding_bound.json|
|AQ-N5|Khóa/C2|Endpoint và7HtableG01|Đầucurve/bảnggiữ, tablelocks nguyên;13mối nốiC2|197endpointpairs/7ô/13mối|Endpointmax3,572e−9m; C2max8,961e−10|7ôG01 làkhóa bảng, khôngphảiduty; curveđược≤5%|checks|
|AQ-N6|Nénlossless|REVIEW02SHA85c9…358|So nguyênbyte luồngcontent decoded từngtrang|31trang|31/31 giống byte|Không thaythế kiểmxobjectpixel củaROOT|FINAL_VS_REVIEW02_31_CONTENTS_EXACT.json|
|AQ-N7|Phạmvi|4SP2 loại;3SP2giữ|Đếm197modelkhôngtrùng từtableactual vàcurvesactual|20họ|Đúng197mã|KhôngmởrộngsangSA|AQ_FINAL_NUMERIC_SHAPE.json|
|AQ-N8|Tácđộng|Read-only|KhôngPDFsave/khôngclaim/khôngsổchính|0PDFghi|Đã lưu JSONscriptbằngchứng|ROOT tiếpnhận sauQA hìnhriêng|read_actual_final.py|
