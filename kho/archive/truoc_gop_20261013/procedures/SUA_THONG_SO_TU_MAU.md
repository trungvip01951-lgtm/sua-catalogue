# Dùng mẫu để sửa thông số catalogue nhanh và đúng

1. Anh nêu catalogue/model/thông số mới. AI tự tra manifest, mẫu, quyếtđịnh và bản chính; điền PHIEU_DOI_THONG_SO.json. Anh không phải điềnJSON. Chỉ hỏi thông tin thật sự thiếu hoặc mâu thuẫn, không hỏi lại quyền đã chốt.
2. Khóa phiên bản nguồn/bản chính/mẫu; đọc trạng thái mẫu. Nếu mẫu cònFAIL, dùng dữ liệu đã kiểm để chuẩn bị, không dùng bố trí lỗi hoặc tự nhận mẫuđạt. Không chạy chương trình lịch sử chứa mãkhóa cũ.
3. Lập bảng cũ→mới cho đúng model/điện/đơn vị/trang. Tách chỉsửa chữ khỏi sửa dữ liệu kỹthuật. Khi Q/H/kW/điện/kíchthước đổi, dò tất cả nơi xuất hiện và quan hệ bảng/đường/tiêuđề; chỉ làm ảnh hưởng có thật. Không tự đổi kết cấu bơm hoặc suy công suất/hiệu suất từ ít điểm.
4. Ghi nguồn/quyền cho từng thayđổi;giữ các khóa cònlại. Dữliệu mới phải ở bảncopy riêng, không sửa gói dữliệuđãkhóa. Chạy kiểmthiếu/đơnvị/monotonic/đầucuối/điểmlàmviệc trướcvẽ. Bảng/đường phải cùng nguồn dữliệu và đúngtỉlệ.
5. Với mẫu đãđạt và còn phùhợp, chỉ sinh trang/vùng chịu tácđộng bằngcatfix;vớimẫu đangnghiêncứu phải giải quyết lỗi của nó trước nhânrộng. Kiểm toànnhãn với đường/lưới, kýhiệu≈/P2, độđọc vàtínhđầyđủ. Không giảmphôngâmthầm vìbảngthêmcột.
6. Lưu ứngviên mới,đọclại sốtừPDFthật, rendertrangđổi,kiểmbảotoànngoàiphạmvi,tácnhânđộclậpkiểmnguồnvàtệp. Ghi từngPASS/FAIL/CHƯATHỂ;chỉnhậnđúngbytebảnđạt saubackup. Giữtệpnguồn/mẫu/lỗi.
7. Bàn giao PDF, ảnhxem,8cột và phiênbản dữliệu/cấuhình/mãkiểm. Cậpnhật sổ/thuviện/kiếnthức cho lần sau. Không mở rộng yêu cầu sửa1thôngsố thành làm lại34trang.

Mẫu yêu cầu có model + biến thể điện + trường + giá trị cũ/mới + đơn vị + nguồn/quyền + trang ảnhhưởng + khóa cần giữ + trạngthái. Các trường chưa biết đểnull;null không phải0. Ngưỡng kỹthuật lấy hồsơ riêng, không hard-code một ngưỡng cho mọi bơm.

Phương án34trang: một bộdữliệu/mộtbộdựng, bốn dạngtrang, ba cấu hìnhSP/SL/SA. Đây là thiết kế nghiêncứu lưu ở deliverables/NGHIEN CUU VE LAI SP SL SA 20261006; mới thửSP6 và chưađạt toànhình. Không có cam kết sốtoken/trang hoặc bộxuất hàngloạt đãhoạtđộng.


## Kiểm đủ thương hiệu trước làm và trước bàn giao

Đọc rules/QUY_TAC_BA_THUONG_HIEU_20261006.md; kiểm Redpump/Perotac/Aquaris và điền brand_coverage trong phiếu. Thiếu hoặc yêu cầu chưa đủ phải nhắc, hỏi lại anh để chốt; chưa có tệp thật thì không đánh dấu đã đủ.


## Chọn phương án theo khả năng đọc và tra cứu

Áp mục “Thiết kế dễ nhìn, dễ đọc, dễ hiểu và đơn giản” trong rules/QUY_TAC_CUNG_HIEN_HANH.md. Ưu tiên thông tin, bố cục đơn giản, chữ rõ, màu tiết chế; không trang trí gây rối hoặc bỏ thông số cần thiết. Trước bàn giao, điền qa.simple_readable_information_first sau khi xem tệp thật ở cỡ sử dụng bình thường; chưa kiểm giữ NOT_RUN.


## Kiểm điện áp theo số pha

1 pha luôn ghi 220–240 V; 3 pha luôn ghi 380–415 V theo anh chốt. Đối chiếu bảng, tiêu đề và chú thích; điền qa.voltage_vs_phase sau kiểm tệp thật. Giữ quy tắc công suất/pha và không tự đổi model.


## Dùng lại nguồn khác hãng khi thiếu

Redpump/Aquaris không có nguồn riêng: dùngPerotac theo quyềnanhchốt, lưu nguồnSHA vàtậpdữliệu đãkiểm. Nếu cónguồnriêng thì dùngnguồnriêng. Qcho phép1sốthậpphân đúngnguồn; không épQnguyên làmtrùng/sai cột. Chỉsửa vùngảnhhưởng vàkiểmphụthuộc.
