# Hướng dẫn anh Trung — đưa lên Google Drive và cài cho nhân viên (bộ quy tắc 2026.10.13)

## A. Tải lên Drive (làm 1 lần)
1. Mở drive.google.com bằng Gmail của anh.
2. Bánh răng (góc trên phải) → Cài đặt → mục "Chuyển đổi tệp tải lên": BẬT "Chuyển tệp đã tải lên sang định dạng trình chỉnh sửa Google Tài liệu" → Xong. (Để các tệp .docx hướng dẫn thành Google Tài liệu, Claude đọc tốt nhất.)
3. Nút "+ Mới" → "Tải thư mục lên" → chọn `D:\ChatGPT\Sửa catalogue - DRIVE NV` → chờ tải xong (xem dung lượng thật ở PHIEN_BAN.txt).
4. Lấy đường dẫn thư mục: chuột phải thư mục vừa tải → Chia sẻ → "Sao chép đường liên kết". Giữ đường dẫn này cho bước C5.

## B. Chia sẻ cho nhân viên
1. Chuột phải thư mục "Sửa catalogue - DRIVE NV" → Chia sẻ → nhập Gmail nhân viên → quyền **Người xem** → Gửi.
2. Mở thư mục, chuột phải thư mục `NV_LAM` → Chia sẻ → cùng Gmail đó → quyền **Người chỉnh sửa** → Gửi.

## C. Trên tài khoản Claude của từng nhân viên (claude.ai)
1. Đăng nhập claude.ai bằng tài khoản Claude của nhân viên.
2. Bật kết nối Google Drive: trong ô chat bấm dấu **+** → **Connectors** (trình kết nối) → bật **Google Drive** → đăng nhập đúng Gmail đã được chia sẻ ở bước B → Cho phép. (Gói Team/Enterprise: chủ tổ chức phải bật connector trước.)
3. Bật chạy mã: bấm tên/chữ cái đầu tên ở góc dưới trái → **Settings** (Cài đặt) → **Capabilities** (Tính năng) → bật **Code execution and file creation** (chạy mã và tạo tệp) → bật **Allow network egress** (cho phép kết nối mạng, để Claude cài thư viện Python). Gói Free/Pro/Max thường đã bật sẵn; gói Team/Enterprise thì chủ tổ chức bật ở **Organization settings → Capabilities**, chọn ít nhất "Allow network egress to package managers only".
4. Thanh bên trái → **Projects** (dự án) → tạo dự án mới tên "Sửa catalogue".
5. Ô **Instructions** (hướng dẫn) của dự án: dán đoạn ở mục D, thay `<DUONG_DAN_THU_MUC>` bằng đường dẫn lấy ở bước A4, thay `<TEN_NV>` bằng tên nhân viên.
6. Mục **Files** (tệp) của dự án → **+** → **Drive** → tìm `00_CLAUDE_DOC_TRUOC` → chọn. (Claude luôn có sẵn hướng dẫn này.)
7. Cài skill: tải tệp `sua-catalogue.zip` (ở gốc thư mục Drive) về máy → claude.ai → **Customize** (Tuỳ chỉnh) → **Skills** → **+** → **+ Create skill** → **Upload a skill** → chọn tệp zip → bật công tắc skill **sua-catalogue**. Skill đã có sẵn quy tắc, hồ sơ hãng và 2 công cụ (kiểm catalogue, vẽ đường cong).
8. Thử: mở cuộc trò chuyện trong dự án, nhắn "Đọc hướng dẫn dự án và cho tôi biết catalogue SS của Perotac đang ở thư mục nào". Claude trả lời đúng là xong.

## D. Đoạn dán vào ô Instructions của dự án
```
Dự án Sửa catalogue bơm công ty Trung Kiên (PEROTAC, REDPUMP, AQUARIS).
Dữ liệu ở Google Drive, thư mục "Sửa catalogue - DRIVE NV": <DUONG_DAN_THU_MUC>
Tôi là nhân viên: <TEN_NV>.
Mọi việc catalogue: dùng skill sua-catalogue và làm đúng theo. Đầu mỗi cuộc trò chuyện đọc tệp 00_CLAUDE_DOC_TRUOC trong thư mục Drive trên. Tự tìm tệp bằng kết nối Google Drive, không bắt tôi dán đường dẫn.
Tôi ra lệnh theo mẫu 6 ô (Việc, Dòng bơm, Hãng, Sửa gì, Tệp đính kèm, Ghi chú); thiếu ô nào thì hỏi ô đó một lần, đưa lựa chọn đánh số.
Chỉ được ghi vào NV_LAM/<TEN_NV>/ và một dòng trong NV_LAM/KHOA_VIEC. Không sửa quy tắc, công cụ, bản chính, thư mục đã duyệt.
Trả lời tiếng Việt, ngắn gọn; thuật ngữ tiếng Anh phải dịch. Không đoán số liệu; thiếu thì hỏi.
```

## E. Nhận bài, cập nhật
- Nhân viên nộp ở `NV_LAM/<tên>/`. Anh bảo Claude điều phối trên máy: "nghiệm thu bài NV_LAM/<tên>/<việc> và đưa vào bản chính".
- Bản chính hoặc quy tắc trên máy đổi: bảo Claude "cập nhật gói Drive NV". Claude chạy công cụ đồng bộ và báo anh tệp nào cần tải lại lên Drive (cách dễ nhất: cài "Google Drive cho máy tính" và để thư mục `D:\ChatGPT\Sửa catalogue - DRIVE NV` tự đồng bộ).
- Khi Claude báo skill có bản mới: tải lại `sua-catalogue.zip` lên tài khoản từng nhân viên (Customize → Skills → mở skill → thay bằng tệp mới, hoặc xoá skill cũ rồi tải lên lại).
- Mẫu lệnh cho nhân viên (dán vào cuộc trò chuyện):
```
1. Việc: Tạo mới | Sửa | Đổi ảnh
2. Dòng bơm:
3. Hãng: PEROTAC | REDPUMP | AQUARIS | Cả 3
4. Sửa gì: (model — thông số — cũ → mới)
5. Tệp đính kèm:
6. Ghi chú:
```
