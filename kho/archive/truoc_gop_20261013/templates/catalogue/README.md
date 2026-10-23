# Thư viện mẫu catalogue dùng lại

Đọc rules/QUY_TAC_CUNG_HIEN_HANH.md và procedures/SUA_THONG_SO_TU_MAU.md trước dùng. Mục tiêu: anh chỉ nêu số cần đổi, AI tìm đúng mẫu/dữ liệu và phạm vi để sửa nhanh.

| Mẫu | Dữ liệu | Trạng thái thiết kế | Cách dùng |
|---|---|---|---|
| [SP6_VECTOR_V1](SP6_VECTOR_V1/README.md) |39mã/426H/39đường,metadata model-kW-HP-điện | CHƯA ĐẠT; bốtrínhãnSTOP2 | Tái dùng dữliệu/phépkiểm đã đạt, không dùng bốtrílỗi đểpháthành |
| PHIEU_DOI_THONG_SO.json | Khungghi yêu cầu sửa | Formchung,chưa chứasố thực | Copyvào work/tácvụmới, AIđiền theo lờianh |
| Phương ánSP/SL/SA |34trang/4dạng/3cấuhình | Nghiêncứu;chưa cóbộmẫuđạtcho34trang | Xem bảnnghiêncứu gốc đãsao lưu trongSP6_VECTOR_V1/reference |

Mẫu đãđạtở các hồsơ cũ được tra qua knowledge/CACH_DA_NGHIEM_THU.md và archive/EVIDENCE_INDEX.json theo đúngcatalogue/SHA, không lấy chữFINAL làm chứng.
Mỗi lần chốt mẫu mới lưu phiênbảnmới, giữmanifestmãkiểm/trạngthái/phạmvi/bằngchứng; không ghiđè bảnlịch sử.


## Yêu cầu logo/bảng và kiểm công suất 06/10/2026

Đọc rules/BO_SUNG_LOGO_BANG_QH_CONG_SUAT_20261006.md: logo không có ô nền khác màu; bảng rõ khung MODEL/P₂/Q(m³/h,l/min)/H(m); giữ điểm làm việc,Qmax,Hmax; công khai cách đo độ khớp≥95%; ghi bất thường thứ tự công suất trong cùng dòng/điều kiện để sửa sau. Không tự đổi426H hoặc lặp cách đặt nhãn đãSTOP2.


## Mẫu logo/bảng mới

[SP6_LOGO_TABLE_V2](SP6_LOGO_TABLE_V2/README.md): logo và bảng Q/H/P₂ rõ khung đã kiểm độc lập đạt;39mã/426H giữ. Toàn trang chưađạt do nhãncũ và1điểmvượt5%. Ưu tiên táidùng phầnlogo/bảngV2, không dùngheaderV1. Dữliệu/ô/logo/code/bằngchứng/SHA được lưu riêng.


## Kiểm điện và họng xả bắt buộc khi dùng lại mẫu

Đọc rules/QUY_TAC_DIEN_HONG_XA_SA_20261006.md/.json. Mẫu SP6 cũ có4biến thể1pha trên3kW cần sửa theo lệnh mới; dữ liệu lưu giữ lịch sử, không được nhân rộng nguyên trạng. Danh sách tại knowledge/XUNG_DOT_DIEN_SP6_20261006.json. MẫuSA phải áp ánh xạ họng xả đúng6dải4SA; chưa kiểm mẫuSA không được nhận đạt.


## Mẫu hiện hành: SP6_FULL_MODEL_V3

[SP6_FULL_MODEL_V3](SP6_FULL_MODEL_V3/README.md) đã ĐẠT kiểm số và hình thức độc lập cho một trang mẫu số. Ưu tiên V3 thay bố trí V1/V2; 426 H giữ, 39 nhãn đầy đủ, nét liền, trục và bảng đúng yêu cầu. Bốn ô 1 pha >3 kW đã sửa ở V3; lịch sử V1/V2 và cờ cũ không đổi. Chưa nhận bản chính, chưa kiểm in giấy/chưa duyệt nhân rộng.


## Tiêu chí bắt buộc cho mọi mẫu

Thiết kế đơn giản, dễ nhìn, dễ đọc, dễ hiểu; ưu tiên thông tin người dùng cần. Màu tiết chế, tương phản rõ, tránh lòe loẹt hoặc trang trí gây rối; giữ đủ thông số/đơn vị. Đọc quy tắc cứng mục thiết kế ngày 06/10/2026 trước dùng hoặc đề xuất mẫu.


## SP ba hãng — mốc mới nhất

[SP_THREE_BRANDS_20261006](SP_THREE_BRANDS_20261006/README.md): AQUARIS 31 trang đã đạt kiểm số/hình thức độc lập và nhận bản chính; PEROTAC/REDPUMP mới có dữ liệu/bố cục có điều kiện, chưa PDF mới. Bỏ 4SP2 cả ba, giữ 3SP2. Dùng đúng SHA/trạng thái trong manifest, chỉ sửa phần cần sửa.


## SP ba hãng V2 — lịch sử, đã được V3 thay thế

[SP_THREE_BRANDS_V2_20261006](SP_THREE_BRANDS_V2_20261006/README.md): PEROTAC13trang, REDPUMP13trang, AQUARIS31trang đã kiểm số/hình thức trên PDF thật và nhận bản chính. Dữ liệu được đóng băng cùng sơ đồ ô/trang để sửa cục bộ; chỉ sửa phần cần sửa. Quy tắc có1pha phải cómodel3pha đã áp dụng. Đọc giới hạn nguồn trong manifest.

**Không phát hành lạiV2:** anh trả lại đường cong gợn và giao diện các hãng quá giống. Mốc PASS phía trên chỉ ghi lịch sử tại lúc giao.

## Mẫu hiện hành SP ba hãng V3 — thiết kế riêng, cong đều

[SP_THREE_BRANDS_V3_20261006](SP_THREE_BRANDS_V3_20261006/README.md) đã kiểm thực và nhận31/13/13trang. AQUARIS xanh ngọc; PEROTAC xanh lam nhạt; REDPUMP đỏ trầm/than và bố cục riêng. 197/220/220đường,1179/2218/2218H giữ, sai lệch tối đa4.999000019%. Có mẫu số, bảng metadata, cấu hình hãng, sơ đồ trang/ô, ảnh dấu đã sửa, bằng chứngQA/SHA và phiếu sửa cục bộ. Luôn kiểm hai cửa khác giao diện/cong đều trước ký; η phải nhìn thấy trên PDF thật khi đổi panel. Chỉ sửa phần liên quan yêu cầu mới; nguồn ảnh/dim thiếu/in giấy giữ giới hạn trong manifest.
