# Yêu cầu trực tiếp: logo, bảng Q/H và quy tắc thông số — 06/10/2026

Anh Trung yêu cầu sửa logo Perotac xấu/sai và bỏ ô nền to; bảng thông số phải trực quan như ảnh, ghi rõ Q/H, chia khung từng ô, nhất là hai dòng đầu.

Anh chốt: giữ điểm làm việc nếu biết, lưu lượng tối đa và cột áp tối đa; đường đặc tính không cần khớp bảng100% nhưng phải khoảng95% trở lên. Anh yêu cầu công suất lớn hơn thì cùng dải lưu lượng phải có cột áp lớn hơn, và cùng dải cột áp phải có lưu lượng lớn hơn; các trường hợp bất thường anh đã thấy để sửa sau.

## Áp dụng hiện hành

- Logo: ưu tiên logo Perotac đúng thương hiệu từ tài sản gốc rõ, giữ tỷ lệ và nét; không đặt mảng nền khác màu thành ô vuông quanh logo. Nếu dùng lại logo gốc nền trắng, đặt trên vùng trắng đồng nhất. Không tự vẽ kiểu chữ gần giống thành logo chuẩn.
- Bảng: có nhóm MODEL, P₂ đúng nguồn; tách biến thể điện/pha, kW/HP; Q đặt ngay cạnh hai dòng đơn vị m³/h và l/min; H(m) nằm riêng ở thân bảng. Vẽ rõ đường biên các ô đầu bảng và thân, không chỉ đổi màu. Giữ đủ mọi model/ô số/đơn vị.
- Khóa điểm làm việc đã biết, Qmax/Hmax. Những min/đầu cuối đã khóa trước vẫn giữ nếu anh chưa yêu cầu đổi; câu mới không ngầm xóa khóa cũ.
- Cách đo95% do AI diễn giải để kiểm: tại từng Q trong bảng cóH>0, độ lệch tuyệt đối |Hđường−Hbảng|/Hbảng ≤5%. Không hiểu là chỉ95% ô đúng, không lấy sai số trung bình che một điểm lệch. H=0 không chia phần trăm; dùng khóa/độ chính xác và ngưỡng riêng được xác minh, không tự đặt dung sai. Chưa có dữ liệu thì ghi CHƯA THỂ XÁC MINH. Đây là cách đo công khai, không trích nguyên văn anh đã nói công thức. Phương án đã có ngưỡng chặt hơn vẫn giữ, không nới ngưỡng để hợp thức hóa mẫu thất bại.
- Kiểm thứ tự công suất giữa các model trong cùng dòng/cấu hình và cùng điều kiện vận hành (Hz, tốc độ, chất lỏng, kiểu công suấtP1/P2). So tại Q chung và miềnH chung. Ghi đầy đủ cặp mã, công suất, Q/H và nguồn. Không áp như định luật tuyệt đối giữa hai loại bơm khác nhau; khác cấu tạo/điều kiện phải tách hoặc hỏi khi có quyết định cần thiết.
- Các bất thường về thứ tự công suất hiện chỉ lập danh sách cho lần sửa sau theo lời anh; không đổi số bảng, model hoặc đường để ép thứ tự ở lượt sửa logo/bảng này. Không đồng nhất kW danh định motor với công suất trục đo nếu nguồn chưa chứng.

## Phạm vi thực hiện lượt này

Sửa logo và trình bày bảng của mẫuSP6 trong tệp mới; giữ 39đường/426H của mẫu2 và các số đã kiểm. Khôi phục ký hiệu≈ của tốc độ, P₂ theo nguồn. Các nhãn biểu đồ đangFAIL/STOP2 không được thử lần3 bằng cách sửa vài tọa độ; phạm vi logo/bảng độc lập với cách đặt nhãn bị đóng. Không nhận toàn trang hoặc bản chính nếu nhãn còn lỗi. Lưu mẫu mới vào thư viện kèm trạng thái từng phần, giữ nguyên mẫuV1 lỗi.

Ảnh anh gửi được lưu nguyên byte trong work/sp6_logo_table_v2/user_references. Quy tắc này bổ sung rules/QUY_TAC_CUNG_HIEN_HANH.md; yêu cầu mới trực tiếp ưu tiên trong đúng phạm vi.
