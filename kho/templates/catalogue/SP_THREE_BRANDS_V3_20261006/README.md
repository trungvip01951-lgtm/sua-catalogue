# Mẫu SP ba hãng V3 — đã kiểm PDF thực

Mẫu hiện hành sau phản hồi đường ngoằn nghèo/giao diện giống nhau. AQUARIS31trang xanh ngọc; PEROTAC13trang xanh lam nhạt; REDPUMP13trang đỏ trầm/than, đổi vị trí các khối. Xem manifest để lấy đúng bản cuối/SHA/bằng chứng, không dùng REVIEW hoặc mẫuV2 phát hành.

## Sửa nhanh lần sau

1. Đọc START_HERE và quy tắc cứng; kiểm bản hiện hành và khóa trước sửa.
2. Nhập yêu cầu vào PHIEU_SUA_THONG_SO.json; khóa Q/Hmin/max/duty. Dữ liệu riêng AQ trong AQUARIS/curves và tables; PR/RP dùng PEROTAC_REDPUMP/perotac_dataset_approved_v2.json + curves. Dùng layout_plan/design-plan tìm đúng trang/ô/model, không đọc lại cả bộ nếu nguồn không đổi.
3. Chỉ đổi số/model/ảnh anh giao; giữ từng cấu hình hãng. Chỉ dựng lại trang bị ảnh hưởng bằng catfix rồi ghép vào bản hiện hành qua catfix, các trang khác kiểm giữ nguyên. Không chạy nguyên mã lịch sử hoặc bypass SHA cũ.
4. Khi đổi đường phải kiểm lại cả họ liên quan: min/max/duty, giảm và cong đều toàn miền, sai lệch mỗi điểm≤5%, thứ tự công suất, nhãn đúng chủ đường. Kiểm η và clip hiển thị thật nếu đổi bố cục.
5. Xem từng trang bị sửa trên PDF thật; so các hãng cùng dòng; đủ hai cửa kiểm trước ký. Lưu delta/before-after/SHA/QA; backup rồi mới nhận bản chính.

Lưu 0 H delta ở lượt này. Không suy kích thước/cân nặng còn thiếu. Ảnh vẫn độ nét nguồn; AQ dấuSUMOTO đã xóa tại vùng nhận diện, dấu mờPR/RP chưa xác minh. In giấy chưa kiểm.
