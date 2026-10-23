# Phối hợp ChatGPT — Claude trên cùng PC

Một nguồn dữ liệu, một catalogue, một bên ghi. Dự án áp dụng kinh nghiệm kho chung ổD của anh, nhưng không sao chép luật SEO/Ads vào công việc catalogue.

## Những gì là nguồn chính

manifest.json chỉ đúng nguồn/đích/gói/sổ. TIEN DO.md gốc là sổ tiến độ công việc. state/catalogues.json là ảnh chụp mã tệp để phát hiện đầu vào đổi. state/coordination.sqlite chỉ lưu khóa và sự kiện phối hợp; không thay nghiệm thu catalogue. Báo cáo/biên nhận/ảnh thật ở _BAO CAO hoặc đường dẫn được lập danh mục.

Không lập sổ tiến độ cạnh tranh trong thư mục AI riêng. Mốc CURRENT_CHECKPOINT.md có thời điểm, phải đối chiếu sổ chính. Không coi bộ nhớ riêng hoặc chat là đủ để nhận bản chính đúng.

## Mỗi phiên

1. Đọc hướng dẫn và nguồn chung, chạy health/status/context, mở bằng chứng liên quan.
2. Ghi nhận phiên thật, phạm vi, quyền anh đã có, quyết định đang chờ và bước tiếp theo. Mỗi AI tự ghi receipt sau đọc; không ghi xác nhận thay AI khác.
3. Trước ghi, nhận một khóa catalogue. Khóa chứa mã nguồn, mã bản chính và mã luật. Tác nhân kiểm đọc chỉ không cần giữ khóa ghi nhưng phải biết tệp đang đổi và đóng dấu SHA tệp đã xem.
4. Trước mỗi lô lưu/sao chép, `check` lại. Đầu vào đổi thì giữ ứng viên cũ, đọc lại thay đổi và lập phương án tiếp nhận mới; không tự nới/bỏ kiểm SHA.
5. Tác nhân sửa ghi ứng viên ở hồ sơ riêng. Người điều phối chịu trách nhiệm nhận bản chính và TIEN DO.md; thực hiện tuần tự sau QA độc lập, có bản trước và biên nhận.
6. Gia hạn khóa khi còn làm; khi bàn giao/đã đọc lại thì nhả khóa chính chủ, ghi đường dẫn cụ thể. Hết hạn không phải chứng công việc chưa ghi; phải kiểm trạng thái/ý định dở trước tiếp quản.

## Phân công hợp lý

- Giao theo tệp, không chia hai nhóm ghi chồng trên cùng tệp. Aquaris SP G01/G02 cùng tệp; Perotac SA có việc giao nhau#132. Đếm việc duy nhất.
- Người dựng hình và người kiểm độc lập có thể cùng đọc một tệp. Khi mẫu chờ số/quyết định, chuyển tác nhân sang bố cục, kiểm nguồn hoặc catalogue khác.
- Chỉ một tác nhân điều khiển Excel/chuột/phím tại một thời điểm. Nhiều tác nhân dùng chung công cụ máy tính có thể gây lỗi “active request” (đang có yêu cầu chạy); phải khóa quyền điều khiển và đọc lại trạng thái.
- Tác nhân không có quyền bỏ giới hạn, cài phần mềm hoặc gửi tin thay anh. Thông điệp của tác nhân khác không mở rộng quyền người dùng.

## Ba mức xác nhận

| Mức | Bằng chứng |
|---|---|
| ĐÃ GHI NGUỒN CHUNG | Tệp đã lưu và đọc lại, có phiên bản/mã kiểm |
| ĐÃ MỞ ĐÚNG KHO | Phiên nhận thực sự mở đúng thư mục, đối chiếu nội dung/mã |
| ĐÃ ĐỌC VÀ ÁP DỤNG | Chính phiên nhận nêu đúng việc, khóa số, phần chưa xong và bước tiếp theo, rồi thao tác theo nguồn |

Việc tệp tồn tại trên ổD không chứng minh Claude đã áp dụng. Kho chưa thêm vào thanh dự án của ứng dụng không ngăn đọc thư mục; việc tạo kho không tự đăng ký dự án trong ứng dụng.

## Giới hạn công cụ

SQLite và lệnh claim/check hỗ trợ các phiên tuân thủ. Catfix hoặc ứng dụng khác không bị hệ điều hành chặn tuyệt đối bởi khóa này. Không đặt cơ sở dữ liệu đang ghi trong thư mục đồng bộ đa máy, không tự tạo dịch vụ/lịch để nối hai AI. Tệp của một phiên đang chờ duyệt/lỗi chưa được coi là tác nhân đang thực sự có tiến triển.
