# Yêu cầu chỉnh mẫu: nét bảng, model đầy đủ, trục Q/H — 06/10/2026

Anh Trung trực tiếp yêu cầu:

- Đường kẻ ô đang đậm/mờ không đều gây nhầm hàng: sửa đồng bộ, dễ dò thông số.
- Không dùng riêng hậu tố -30/-28… trên đường; ghi rõ đầy đủ model. Nếu có cả1pha và3pha, đồ thị chỉ ghi model3pha; không xóa biến thể1pha hợp lệ trong bảng.
- Dòng lưu lượng m³/h vàl/min phải ngay dưới đồ thịQ–H, phía trên biểu đồ hiệu suấtη; không đặt dướiη.
- Đường đặc tính vẽ nét liền, không dùng nét đứt.
- Ghi Total head H (m) dọc trục cột áp; xóaH(m) rời cạnh tiêu đề.
- Bỏ các dòng đếm21models/18models; vẫn giữ tiêu đề dòngbơm6SP36/6SP46.
- Anh xác nhận “được rồi e sửa lại cho a đi”.

Áp vào mẫuSP6 đang xem, không suy thành đã sửa34trang. Đồng thời tuân quy tắc3kW về pha và ngưỡng5% đã công khai; giữ426sốH, côngsuất,đơnvị,đầucuối vàđiểmlàmviệc đãbiết. Ghi4ô1pha>3kW thành dấu–, giữđúng dòng3pha; không xóa model3pha hoặc tự sửa côngsuất.

## Cách làm và tránh lỗi cũ

Nét bảng phải vẽ sau TẤT CẢ nền ô, mỗi đoạnmộtlần,cùngmàu/độdày. Mẫutrước vẽnền dòngsau đè mép nét dòngtrước; chỉ đặtcùnglinewidth khôngchứng cùngđộrõ trênPDF. Bảnmới kiểm từngđường ngang/đứng vàđộđọc thật.

Nhãnfullmodel dùng bốtrítheotangent/vùngtrống, đo hộpmựcthật vớiTOÀNBỘ đường vànhãn; một sốnhãn cóthể nằm dướiđường hoặc ngoàimépvớileaderngắn đúngchủ nếu khôngđủchỗ. Không lặp suffix cùngx cốđịnh đãSTOP2; không phủ trắng/nới ngưỡng/thu fontâmthầm. Chuẩn bịJSONhìnhhọctrướcPDF, tốiđa2mẫu cho cáchmới; giữ cácmẫu cũ đểtruyvết.

Điểm6SP36-2 Q48cũ lệch5.56%: thử đườngC2 đơnđiệu đi qua426bảng (chỉkhớplại10điểm của modelnày;38đường còn giữ). Đầucuối/bảng khôngđổi; kiểm đạo hàm và điểm thực; đây là sửađường theo chuẩn mới, khôngsửa số để choqua.
