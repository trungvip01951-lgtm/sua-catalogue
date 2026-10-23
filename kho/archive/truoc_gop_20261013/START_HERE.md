# Bắt đầu tại đây

## ĐỌC TRƯỚC — hai cửa kiểm bắt buộc anh Trung nhắc ngày 06/10/2026

SP đã sửa theo yêu cầu này và nhận bản mới ở [mẫu V3](templates/catalogue/SP_THREE_BRANDS_V3_20261006/README.md). Đọc [bàn giao mới](BAN_GIAO_SP_THIET_KE_RIENG_20261006T093634Z.md); các PASS V2 dưới đây là lịch sử bị trả lại về hình thức.

1. **Cùng loại bơm, khác hãng phải khác giao diện rõ ràng.** PEROTAC, REDPUMP và AQUARIS phải khác màu chủ đạo, nền đầu trang và cách trình bày; không chỉ thay logo/tên trên cùng một mẫu. Vẫn đơn giản, rõ số, dễ đọc. Được dùng chung dữ liệu đã kiểm nếu đúng nguồn được anh cho phép.
2. **Đường Q–H phải cong đều, không ngoằn nghèo.** Kiểm toàn miền đường giảm, không gợn/đổi độ cong liên tiếp; rồi nhìn từng biểu đồ trên PDF thật. Khớp bảng/C2 không thay kiểm hình. Sai lệch từng điểm bảng ≤5%; anh cho sửa H trung gian nguyên nếu cần, nhưng giữ min/max và điểm làm việc đã khóa. Xem quy tắc cứng để xử lý khóa mâu thuẫn.
3. Phiếu nghiệm thu phải có hai mục riêng **KHÁC GIAO DIỆN GIỮA CÁC HÃNG** và **ĐƯỜNG CONG ĐỀU**, kèm PDF/SHA, trang/biểu đồ đã xem, bằng chứng và người kiểm. Chưa kiểm hoặc còn lỗi thì CHƯA ĐẠT, không ký hoàn tất. Anh đã trả lại phần này của cả ba SP; PASS cũ không chứng yêu cầu mới đạt.

Dự án **Sửa catalogue**, phiên bản dữ liệu **1.0**, được anh Trung yêu cầu tạo ngày03/10/2026 để ChatGPT và Claude dùng lại cách làm đã kiểm, không phải kể lại nhiều.

## 1. Đọc trạng thái trước làm

Đọc AGENTS.md, manifest.json, hai tệp trong rules/, knowledge/THAY_DOI_QUY_TAC_20261003.md, rồi sổ TIEN DO.md tại đường dẫn gốc trong manifest. Đọc state/CURRENT_CHECKPOINT.md để tìm phần đang dở, nhưng ưu tiên sổ và tệp thật mới nhất. Quy tắc mới yêu cầu Q tăng/H giảm; bảng nguồn tăng nhẹ không còn là điều kiện chấp nhận, phải rà/sửa trong phạm vi khóa.

Mở PowerShell trong thư mục này. Các lệnh đọc dùng Python đang có, không cài thêm:

```powershell
& 'C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\.catfix-venv\Scripts\python.exe' -B -X utf8 tools/catalogue.py health
& 'C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\.catfix-venv\Scripts\python.exe' -B -X utf8 tools/catalogue.py status
& 'C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\.catfix-venv\Scripts\python.exe' -B -X utf8 tools/catalogue.py context --file 'Trục ngang/Catalogue DWO (bản mới).xlsx'
```

`health` là kiểm cấu trúc kho và quy tắc, **không phải** 43 kiểm thử catfix, kiểm số, hình thức hoặc bản in. `context` là gói đường dẫn/mã phiên bản của một catalogue. `status` đọc trực tiếp sổ gốc và các khóa hiện có.

Nguồn/bản sửa khác ảnh chụp trạng thái: đọc lại hồ sơ và bản thật, xác định thay đổi có thẩm quyền, rồi người điều phối cập nhật state bằng tools/refresh_index.py. Không lấy thời gian sửa mới hơn làm chứng bản nào đúng.

## 2. Chuẩn bị công cụ khi phiên bị ngắt

Đọc hết bản prompt chung và README_KY_THUAT trong vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT/. Chạy BƯỚC 0 nguyên văn và 43 bài kiểm:

```powershell
& 'C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\.catfix-venv\Scripts\python.exe' -B -X utf8 tools/bootstrap_legacy.py --tests
```

Phải có4 mục môi trường **ĐƯỢC** và dòng **TỔNG KẾT: 43/43 ĐẠT** thật của lần chạy. Thiếu công cụ thì báo, không tự cài. `catwork.start()` chỉ khởi động/kiểm môi trường, không thay 43 bài kiểm.

## 3. Nhận việc và khóa ghi

Đọc prompt nhóm từ gói gốc. Thứ tự gốc: **G18,G08,G01,G02,G03,G04,G05,G06,G07,G09,G10,G11,G12,G13,G14,G15,G16,G17**. Anh đã cho song song theo catalogue; một bên ghi/tệp, người điều phối chốt nhóm. G01/G02 cùng Aquaris SP và G04/G05 có việc#132 giao nhau phải phối hợp, không tính/làm trùng.

Ví dụ, thay mã phiên và phạm vi bằng phiên thật:

```powershell
& 'C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\.catfix-venv\Scripts\python.exe' -B -X utf8 tools/catalogue.py claim --file 'Trục ngang/Catalogue DWO (bản mới).xlsx' --actor Claude --session 'phien-thuc-te-cua-ban' --purpose 'Chuẩn bị biểu đồ DWO theo số anh chốt' --ttl 1800
```

Lưu token (mã khóa) trả về. Trước ghi dùng `check`; trong lô dài dùng `heartbeat` để gia hạn; sau đọc lại/bàn giao dùng `release --note 'đường dẫn báo cáo, phần đã/chưa nghiệm thu và bước tiếp theo'`. Thêm `--actor`, `--session`, `--token` đúng khóa cho các lệnh này.

Khóa hết hạn vẫn giữ hồ sơ; không tự chiếm. Chủ cũ đọc lại rồi nhả khóa, hoặc người điều phối xác minh đầu vào/ý định dở và lập tiếp quản có bằng chứng. Công cụ không thay quyền anh hoặc điều kiện chờ số min của DWO.

## 4. Làm, kiểm, bàn giao

Chọn procedures đúng loại. Lưu ứng viên mới qua catfix, mở chính tệp đã lưu để nghiệm thu số và đồ họa độc lập. Người điều phối sao lưu bản chính rồi tiếp nhận đúng byte ứng viên đã đạt. Báo cáo8 cột, ảnh trước/sau, số đo và giới hạn phải có trước tính xong.

Sau khi **chính mình** đọc đủ nguồn chung, ghi receipt (xác nhận đọc) với đúng phạm vi và bước tiếp theo. Không ghi thay cho AI khác. Mã đã dùng nằm trong archive/code/ nhưng cách được chọn và giới hạn nằm trong knowledge/; không chạy một tệp chỉ vì tên có FINAL hoặc đã tồn tại.

## 5. Với catalogue mới sau này

Anh đưa đường dẫn tệp/phiên bản và việc mới. AI tự áp dụng tiêu chuẩn chung; chỉ hỏi dữ liệu/quyết định thực sự thiếu. Giữ bản gốc, tạo thư mục đầu ra riêng. Người điều phối bổ sung manifest/danh mục và phiếu việc từ templates, khóa mã nguồn mới. Gói sửa năm2026 có tên thư mục ngày cố định trong Session; **không đổi hằng số catfix âm thầm** để áp cho bộ khác. Lập cấu hình/adapter đường dẫn riêng, kiểm an toàn rồi mới chạy theo cấu hình đã giao. Mã các phiên cũ có số/tọa độ/SHA riêng không phải chương trình sửa mọi catalogue tự động.


## Bắt buộc bổ sung — lưu quy tắc và dùng mẫu (06/10/2026)

Đọc rules/QUY_TAC_CUNG_HIEN_HANH.md trước áp điều cũ; quyền phông gần nhất và DWO min/max đã có, không hỏi lại. Trước sửa thông số đọc procedures/SUA_THONG_SO_TU_MAU.md và templates/catalogue/README.md. Sau yêu cầu/nhắc/lỗi phải lưu quyết định, bài học, chứng cứ và mẫu có trạng thái. SP6_VECTOR_V1 chưa đạt hình thức/STOP2, không lấy làm mẫu phát hành; không chạy nguyên mã lịch sử. Quy tắc mới này được anh trực tiếp yêu cầu lưu thành quy tắc cứng, chỉ trong dự án catalogue.
