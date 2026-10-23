# Bài học mẫu SP6 — đã kiểm độc lập 06/10/2026

Ứng viên2 SHA8f1a2edc65aad20ab5f0d41b1c4980e85cd7617193a868ac2e98ad05cac7c583. Nguồn e1b94dc6…, bản chính48c8535c… giữ. Quyền dùng nearfont/thiết kế mới có; nghiệm thu hình thức vẫn FAIL. Hai mẫu đã dùng hết; không chạy bản3cùngcách.

| Lỗi thật | Nguyên nhân/căn cứ | Cách tránh bắt buộc | Trạng thái |
|---|---|---|---|
| Nhãn -2 của6SP46 bị đường -3A xuyên; nhiều nhãn thấp6SP36 (-11/-9/-8/-7/-6/-4) cũng vậy | Bố trí đầu đường chỉ xét vị trí tương đối một đường, không chặn toàn bộ đường lân cận | Lập đầy đủ hộp chữ và nét có bề dày, kiểm giao với tất cả đường/lưới/nhãn; xem cụm dày ở cỡ thật và phóng lớn trước lưu | FAIL; không tái dùng bố trí hiện tại |
| H(m) chồng Impgpm ở bản1 | Hai lớp chữ dùng chung vùng trên trục | Phân khu trục trước dựng, kiểm toàn cặp hộp chữ | Đã sửa ởbản2, giữ bằng chứngbản1 |
| η gợn do dò nét ảnh nén | Nhiễu JPEG đi vào điểm dò; bản2 làm mượt hình | Đối chiếu nguồn, ghi sai lệch; không dựng hiệu suất thử nghiệm từ ảnh | Hình bản2 tốt hơn; dữ liệuη hãng CHƯA THỂ XÁC MINH |
| n≈2850 bị đổi n=2850; P2 mất | Bảng kê nội dung không khóa cả ký hiệu ngữ nghĩa | Lưu chuỗi đúng nguồn/kýhiệuP2; kiểm toàn văn/ký hiệu và điều kiện vận hành riêng với số | CHƯA SỬA ởmẫu |
| Gọi426điểmđạt như khớp tuyệt đối | Ngưỡng dữ liệu mẫu là max(1m,2%H); độc lập thấy sai lệch lớn nhất≈4,49998m | Báo ngưỡng và số đo, không nói đi chính xác mọi điểm; không áp ngưỡng này chung cho catalogue khác | 426ô đọc lại đúng; đường chỉđạt ngưỡng hồsơ |
| Session.result(NAME,sub='Giếng') thànhGiếng/Giếng | Hàm đã suy thư mục từbasename | ĐọcAPIhiệncó, truyềnbasename,kiểmđườngdẫn tồn tại trước ghi | Sửa tiền kiểm;0PDF từlỗi |
| catalogue.py check có --file không được hỗ trợ | Nhầm tham sốclaim/context vớicheck | Đọc --help; check dùngactor/session/token | Sửa tiền kiểm;0PDF từlỗi |
| Tiến trình con lỗiUnicode tiếngViệt | Thiếu -Xutf8 khi chạyPythoncon | DùngPython -Xutf8;đọcghiUTF8;khôngđổi tên nguồn | Sửa tiền kiểm |
| Đọc /Metadata trực tiếp bịAttributeError | PDF cóthể không cóXMP | So cùng trường thiếu=null, không tự tạo metadata | Sửa phép kiểm, không sửaPDF |
| Script kế thừa chứaSHA/khóa/đườngdẫn cứng | Mã theo mộtlần chạy, không bộ dựng tổngquát | Lưu .py.txt để tham khảo; yêu cầu hồ sơđầu vào/phiên/khóa mới; không nhập/runmãlịch sử | Chặn chạy nguyên trạng |
| Gán803,47Credit cho mộttrang | Số dư toàn tài khoản cóphiênSEOWEB đồng thời | Giữ cửa sổ đo, báo phạmvi tài khoản, không nói chi phí riêng | Đã công bốgiới hạn |

Phần tái dùng được: bảng dữ liệu39mã/426H và metadata đãkiểm, đường vật lý đãkiểm theo ngưỡng riêng, nguyên lýfontnhúng/vector/table, phép đọc426ô trênPDFthật, phép bảo toàn11trang và tài nguyên. Hai H của6SP46-2 Q12:26→25 vàQ18:25→24 chỉ ở ứngviên; chưa nhập bảnchính. Đầu/cuối giữ. Không áp2ô này sang modelkhác.

Bằng chứng: [báo cáo độc lập](../deliverables/SP%20TRANG%206%20MAU%20VE%20LAI%2020261006/KIEM%20DOC%20LAP.md), [mẫu và hồsơ](../templates/catalogue/SP6_VECTOR_V1/README.md), work/sp6_redesign_pilot và _BAO CAO/G05/SP6 THIET KE MOI VECTOR PILOT20261006 (tên thực có dấu cách PILOT 20261006).

Hướng nghiên cứu tiếp (CHƯA THỬ, không là mẫuđạt): tính vùngtrống cho toàncụm, tách nhãnkhỏinét bằngbốtrícó chứng từngchủđường, hoặc xin quyếtđịnh về bố cục rộng hơn nếu thật sự khôngđủchỗ. Không chỉ dịch nhãn3A để lỗi chuyển sang-2; không gọi việc đổi vài tọađộ thànhphươngán mới.
