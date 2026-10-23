# Chữ nguồn và điểm trắng trong lớp che: bài học 3SL3

Mẫu M1 của 3SL3 chưa đạt hình thức: ảnh phóng lớn có vệt dọc đen tại vị trí chữ cũ của mã /31, /21, /16. Không được coi kiểm bitmap sạch hay số liệu đúng là đã đạt mẫu PDF.

Ảnh nguồn và ảnh bitmap M1 sau ghép đều sạch tại vùng này. Phiếu chẩn đoán `G04/SL3SL3 M1 SOURCE OLD FONT HALO ONLY DIAG NO M2 20261004T082245Z-942304/01 SOURCE M1 OLD7 FONT HALO PIXEL DIAG NO M2.json` có SHA256 `9a4c20ed327a8c2b6cbc0d2920293dd0177631ed30616f2ebc5f4d6b222b95b2`. Cả bảy mảnh chữ giữ nguyên điểm ảnh nguồn sau dịch lên tám điểm ảnh; không cắt lại nét hoặc tạo chữ mới.

Lớp che của M1 dùng alpha (độ phủ) 255 tại điểm ảnh có màu khác nguồn, 0 tại điểm có màu bằng nguồn. Trong toàn vùng đã gán màu và chữ có 455 điểm vẫn alpha 0. Đây không tự chứng minh lỗi: màu bằng nhau có thể là đúng. Phải đối chiếu vệt thực trong ảnh đã dựng.

Kiểm độc lập khóa bảy điểm vệt thực. Ví dụ ảnh CAPTIONS7 600 tại (43,230) có RGB 115/115/115, trùng màu chữ cũ nguồn ở (1410,237), mặc dù bitmap vá tại đó đã trắng và alpha 255; điểm trắng bên phải (1411,237) vẫn alpha 0. Mẫu tương tự có ở hai mã khác. Mẫu ranh giới này hỗ trợ thử phủ kín vùng chữ; chưa phải chứng minh đầy đủ cơ chế dựng ảnh của phần mềm.

Phương án M2 chỉ tăng độ phủ tại hộp chữ nguồn cũ cùng viền hai điểm ảnh và toàn hộp chữ mới. Nền dùng đúng hồ sơ cột/hàng trung vị của nguồn M1 rồi làm tròn giá trị nhỏ hơn; đây là màu tính toán, không phải sao nguyên từng điểm ảnh nền. Phải công bố đúng cách tính, không gọi là điểm ảnh nền nguyên bản.

Phiếu kế hoạch `G04/SL3SL3 M2 SOURCE FONT HALO2 OPAQUE ALPHA PURE PLAN NO SAMPLE 20261004T083030Z-1c4fa9/01 PROPOSED M2 SAMEFONT14 SOURCE91 HALO2 OPAQUE ALPHA NO RAM.json` có SHA256 `be712c92d30891765ec4d6891357173de62f1c8a37b2de2199039aafc090cc3b`: thêm đúng 444 điểm alpha 255, không bỏ điểm cũ; màu thay so với M1 ở 181 điểm, chênh kênh lớn nhất 7. Hộp ảnh vá [1359,184,1650,455], ma trận đặt ảnh và đường viền ngoài của ảnh vá giữ. Toàn chữ nguyên bản, 14 đoạn cong/91 số, bút và nét đứt giữ. Không tăng độ phủ tại trục lưu lượng 0, không phủ trắng hình chữ nhật.

Helper49 và caller51 chỉ được chạy một mẫu M2 sau phiếu khóa của ROOT. Helper49 bắt buộc lệnh vẽ mới bằng toàn bộ lệnh M1 SHA256 `f3e950ab9f95f559dfe85bae44b02315bee2a67e3fc7dfbc1092f34e57ca5657`; thay đổi chỉ nằm trong hai luồng ảnh và lớp che đã khóa. Thực tế M2, lưới, mép ghép và phông nhìn thấy vẫn phải được kiểm lại. Kế hoạch toán và alpha 255 đầy đủ không tự là nghiệm thu hình thức. Giữ lỗi M1 và chẩn đoán khung trái riêng; chưa nhận toàn catalogue SL hoặc nhóm G04.

Không sửa file nguồn, không tự lưu lại bản chính, không đổi sổ tiến độ hoặc danh mục tại bước chuẩn bị. Nếu thử M2 còn lỗi, không tự dựng lượt thứ ba cùng phương pháp.
