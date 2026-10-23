# 6SP10 và SL trang1 — chuẩn bị đã kiểm, chưa tạo mẫu

Bản chính SP hiện b24aaf99f80556bbbd956ad87af43a28b0b66d2d555602af75636bb2e90b62b3; SL a04dbd5a9b035fd260a66027f246e4cb98740c6b088bff5e61376ea994427ac7. SP95 trang10 đã lưu/nhận ở đợt trước, các trang5/7/11/12 giữ. Không làm lại phần đã đạt. Việc gốc135/149 không đổi; toàn dự án chưa xong.

## Phần chuẩn bị mới

6SP10 trang4: đọc nguồn20 mã/180 cột áp nguyên,40 đầu-cuối,160 cặp giảm; ROOT mở bảng/trục/20nhãn, kiểm67 crop RGB nguồn; Sol replay nhánh/40neo. Trục chính l/phút, cuối bảng300l/phút=18m³/h; biên320l/phút không phải cực đại máy. Giữ công suất/điện và mọi số. Toán20 đường38đoạn cong nối C2, giảm toàn đoạn; kiểm lại tọa độ hữu hạn20 số thập phân, cả180mốc đạt dung sai gốc max(1m,2%). Cùng bút SP98/108/110,0,7773689114693686điểm.

Bộ20nhãn:138 phần RGB nguồn,11vật liệu đã có trên B24, không đổi màu/co chữ/phông hệ thống. ROOT và Sol kiểm bộ tĩnh; chữ4/5 có pha xám và hạt nguồn được giữ, chưa nhận toàn chữ đã làm nét. Hình chữ6 ở nhãn nguồn thấp còn bất định JPEG; owner6 từ hai neo là kết luận riêng. Phương án bố trí được ROOT chốt: quay cả từ theo tiếp tuyến để giữ cỡ và tránh va đường; ưu tiên đoạn đầu ít dốc. Tính toán hiện có18 nhãn đủ khe và cần2 đường chỉ nhãn ngắn cho26/28 trong khung; chưa có layout cuối hoặc mẫu thật được nhận.

SL trang1:63 số/7mã/14đầu-cuối; ROOT mở hai bảng/hai đồ thị/hai trục/bảy nhãn, đọc PDF nguồn và replay764 cột mực,11 trục,14neo; Sol kiểm riêng. Nhãn /24 lặp thấp là lỗi trong nguồn, hai điểmQ1,5/H28,3604 vàQ2,1/H15,7047 khớp duy nhất hàng/17 (bảng29/16). Giữ nhãn sai trong bằng chứng; nhãn mới17 là đề xuất sửa. Toán7 đã qua ROOT/Sol,10 đoạn C2 toàn đường,17 đoạn sau chia đứt/liền,63mốc hữu hạn đạt dung sai. Dùng bút SL132/151/151,0,95điểm, không bút SP. Chữ7 đang kiểm; mẫu tĩnh đầu thiếu dấu/ ở17 giữ CHƯA ĐẠT, điều chỉnh prefix nguồn/12 + nguyên vật liệu17 hiện hành đã có riêng, chưa ROOT/Sol nhận font7 trên trang.

## Kinh nghiệm cần giữ

- Không ép native hiện tại bằng native nguồn: trang4 SP có ba CfxPatch cũ hợp lệ. Kiểm riêng ảnh nguồn/CTM và toàn quan hệ của bản chính đã nhận, rồi giữ các paint ngoài vùng được sửa.
- Số tham chiếu PDF có thể đổi sau lưu. Trên B24, Contents trang4 là28/0, ảnhX5 là33/0 từ nguồn38/0; token9 là168/0, không183 cũ. Phải dùng mapping thật, không đoán theo số cũ.
- Hệ số bậc3 của tọa độ chiếu lên trục chữ không chứng minh dấu đạo hàm. Kiểm cực tiểu đạo hàm trên hai đầu và điểm dừng trước dùng tìm khoảng. ROOT đã phát hiện/chỉnh trước mẫu.
- Một thư mục bằng chứng lồng quá dài trên Windows gây FileNotFoundError ở bước ghi bản đọc. Chỉ rút ngắn/nới cấp thư mục bằng chứng; không đổi phép so sánh. Lần đọc sửa lại đã đạt, không có Editor/Save.
- Bộ chữ tĩnh đúng chưa chứng minh đẹp trên trang. Cần kiểm polygon đầy đủ RGB, khoảng nét bút, trục/hiệu suất/tiêu đề/bảng, rồi xem mẫu thật và file đã lưu. Không dùng lõi chữ hoặc xóa viền theo ngưỡng để cho qua.

## Làm tiếp

ROOT giữ quyền nhận bản chính và ghi ba tệp điều phối. Một tác nhân làm SP layout/helper/caller; một tác nhân làm SL chữ/layout; Sol kiểm độc lập. Chưa chạy Editor/RAM/Save mới trong các phạm vi trên. Trước mỗi mẫu phải đọc mã cuối, kiểm dữ liệu còn đúng, chạy cổng rõ phạm vi; không dùng phiếu tĩnh làm quyền lưu. Chỉ chuyển sang ghi tiến độ ĐẠT sau mở file đã lưu và kiểm độc lập. Trạng thái mutable/index/ledger/checkpoint không được thay trong bản ghi này.

## Bằng chứng ROOT

- G05 nguồn180/nềnB24: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT6SP10B24 20261004T230844Z-219f46\01 ROOT SOURCE180 MANUAL20 CURRENT B24 DIRECT BASIS NO RAM GATE.json; SHA256 42168e5fa870df71f721c9af2612b73a80b9b6fa6753fce74fb4789f1670b85d
- G05 toán20: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT6SP10MATH 20261004T231037Z-6c6f8e\01 ROOT PURE20 SOURCE180 ANALYTIC FINITE38 SCOPED PASS NO RAM.json; SHA256 a783e81dc0fc300166891051db77299ed81ab533a7bc9fedcefe3a10bac56779
- G05 chữ20 tĩnh: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05\ROOT6SP10FONT 20261004T231803Z-41320e\01 ROOT WORD20 SOURCE138 RGB EXISTING B24 STATIC REVIEW NO RAM.json; SHA256 c880cfebbace8b936a5c85b3d053de5a38523808b7c54383a466b6e9379cab89
- G04 nguồn63: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\ROOT SL P1 SOURCE63 20261004T231349Z-7f970e\01 ROOT SOURCE63 LABEL7 AXIS11 OWNER7 ANCHORS14 READONLY PASS.json; SHA256 427ad2fa9bd91714e77d08840b94e2b16a497b01c80014dd311840b269fc9933
- G04 toán7: C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\ROOTSLP1MATH 20261004T232248Z-646653\01 ROOT SL7 SOURCE63 ANALYTIC C2 FINITE20 SCOPED PASS NO RAM.json; SHA256 8eddc9e8815897559ed80c8ddd6ce873528d50fc1213f418cf12964e4195d390
