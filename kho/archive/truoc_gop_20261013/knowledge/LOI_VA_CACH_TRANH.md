# Lỗi thật và cách tránh

Đây là kiến thức, không phải danh sách chương trình được chạy lại. Tra chứng cứ trong archive/EVIDENCE_INDEX.json và sổ gốc. Giữ mẫu lỗi và phạm vi chưa kiểm; không sửa báo cáo cũ thành đạt.

| Lỗi/ngộ nhận | Cách xử lý cho phiên sau |
|---|---|
| S.src nhận chuỗi có thư mục nên không thấy tệp | Truyền basename, tức chỉ tên tệp; danh mục giữ thư mục và danh tính riêng |
| catwork.start đổi thư mục/sys.path khiến không nhập được helper | Giữ HERE là thư mục chương trình; phục hồi đường dẫn nhập hàm phụ, không sửa catfix |
| Khởi động môi trường được gọi là 43 kiểm | Chạy tests/run_tests.py thật. Nếu chỉ 41/43 thì chưa đạt; 4/4 môi trường không thay 43/43. Chưa tìm được báo cáo lịch sử 41/43 thì không dựng lại hai lỗi |
| Bản G01 cũ ghi lùi G02 | Dùng G02 (gồm cả G01) trong manifest và khóa mã bản hợp nhất |
| Gán mọi việc trong nhóm cho mọi tệp của nhóm | Đối chiếu trường files của từng việc. SA không nhận #162 logo Redpump; DWO không nhận #66 của Excel Perotac. Đã sửa danh mục, kiểm bốn tình huống nguồn riêng; không coi mã nhóm là quyền sửa mọi tệp |
| Chạy lại chương trình tiếp nhận đã xong | fresh/mã trước từ chối là đúng; không bỏ điều kiện chặn hoặc ghi lại chỉ để có báo cáo mới |
| Thiếu k/W/8/Ó đúng phông | Tìm cùng kiểu trong chính tệp. Không thu nhỏ K, đổi phông hoặc ghép chữ để đoán; ghi chưa thể |
| Chữ OCR ẩn bị coi là chữ đang thấy | Kiểm lớp/chương trình phông/nhiều chữ chung/độ rộng. Tr7 nghĩa là chữ không được vẽ ra |
| Hình chữ từ JPEG khớp diện tích nhưng trông viết tay | Xem toàn ký tự/cụm 600 dpi. Số 4 cong như 3, 5 u cục, 9 sai lòng/đáy đều không đạt; SP v24 chưa được xuất PDF |
| Lặp dựng chữ SL 5/2/9 nhiều phiên | V7 có 9 tốt hơn, 5/2 chưa đạt; V8–V10 bị loại. Không đổi tên để thử cùng cách vô hạn |
| Giữ cụm nguồn được coi mặc định sạch | SL /23,/11,/8,/5,/4 giữ cả nét đường chạm chữ; 13 đảo đã dừng, 8 cụm khác chưa chốt, chưa PDF 2 |
| Bỏ 2 điểm ảnh mép rồi gọi toàn chữ không đổi | Báo toàn mép và nội vùng riêng. SA còn quầng Hfeet200/US10/US30; phải xem đủ cụm |
| Chỉ kiểm nét S, bỏ hình tô f* | S vẽ viền, f* tô theo quy tắc chẵn/lẻ; kiểm cả hai. Hộp Eta/60 giao nhau không tự chứng biên chữ giao; dáng 60 vẫn có lỗi riêng |
| Hai hộp W* chồng nhau tạo lỗ | W* cắt theo chẵn/lẻ; hợp nhất hình học hoặc gộp thành một đảo đúng miền. Giữ byte ảnh/ma trận, kiểm ảnh thật |
| Nhầm PageImage.key và PageImage.index | key định danh trang, index là chỉ số lệnh Do. SL LAN2 có tài nguyên mà chữ không hiện; LAN2B sửa index mới thấy đủ 13 cụm |
| Nới hộp riêng thành quy tắc chung | Phân biệt hộp nguồn/hộp cắt. 0,48 pt của 4 vạch feet + đáy 0 SL không áp cho chữ hoặc catalogue khác |
| Tên ảnh KHONG DOI được dùng thay phép đo | Hộp tiêu đề SL nguồn có 0 điểm đổi, hộp đã nới có thay đổi ở lề. Ghi đúng hộp/đơn vị/mã và phép đo |
| Chỉ dùng độ dày/màu kế hoạch | Đọc lệnh thật và tiết diện mực; kiểm trong suốt, đầu/nối/nét đứt. GB M1 quá nhạt, M2 mới đạt |
| Đường η có quá nhiều đoạn/điểm uốn | Kiểm đạo hàm và hình. SL M1 có 117 đoạn/99 điểm uốn, chưa nhận bản chính |
| Khớp ảnh nguồn được nhận là dữ liệu hãng | Đầu nét quan sát và 6 đường SP thiếu bảng chỉ là chứng hình, không tự xác nhận Qmax/Hmax hãng |
| Gán mã theo thứ tự dòng hoặc cột áp gần nhất | CDX trang 4/5 chưa định danh đủ; 5 dòng/4 đường không tự thành 5 đường hoặc mã 185-B |
| Một hệ số cho cả trục ảnh quét | Đọc tâm vạch và đơn vị từng đoạn của chính biểu đồ; không chép từ hãng khác |
| Khớp bảng tăng ngược rồi gọi kỹ thuật đúng | Lệnh mới 03/10 yêu cầu Q tăng/H giảm từng mã. Sửa số trung gian nguyên + đường, giữ extrema/điểm làm việc. Hướng cũ giữ tăng nhẹ 6SL25 đã bị thay thế |
| H bằng nhau được tự động coi giảm | Kiểm đường thật và làm tròn. Không tự cho đạt hoặc phá giá trị max/min đã khóa |
| Đọc ô lẻ sai dòng/đảo y | Ảnh chứng phải có tên mã, đầu cột và tọa độ. ROOT đọc 4SL3/15 tại Q3 là 76, không phải 78; giữ ảnh sai làm cảnh báo |
| Biên sai số chạm ngưỡng bị gọi lỗi chắc | Ghi danh nghĩa và bất định; SL /16 chưa thể, /20 là phép đọc tác nhân còn chờ ROOT độc lập |
| Cộng mốc đo lại thành tiến độ mới | SA 231 là tập con 1.827; 82 mốc ảnh khác 230 lượt đặt; #132 G04/G05 chỉ đếm một việc |
| RAM và tệp thật khác vài điểm bị che đi | Giữ chẩn đoán lỗi Perotac WC trang 6–8; kiểm tệp thật/bảo toàn/hình thức riêng |
| PDFium làm tròn bitmap nhưng gắn vùng bằng dpi/72 | Dùng kích thước bitmap và khổ trang thực. Sửa phép đo, không nới vùng hoặc sửa PDF để cho qua |
| Parser trả record rỗng cuối | So toàn byte và lệnh có nghĩa; CDX trang 3 có 237 lệnh/238 record, không tự kết luận mất lệnh |
| Chứng cỡ ±2% khi chữ nguồn bị lưới che | 14 chữ CDX trang 3 chưa đủ nguồn để chứng toàn cỡ; 170 chữ sạch không thay giới hạn |
| AI tạo sai cấu tạo bơm | Dùng ảnh sản phẩm gốc + nền AI rỗng + đường cắt hình học; không tạo thêm bộ phận hoặc tẩy màu vật liệu chưa rõ |
| Dựng XLSX ngoài làm mất 3 ảnh | Đọc drawing/media/anchor. Ảnh bố cục từ XML không thay bản Excel/bản in thật |
| chart.xml có 9 series được coi hiển thị 9 đường | Đọc dữ liệu/bộ nhớ đệm/ô trống/quan hệ rồi xem thật; SS180 có x12/y2 chưa tự gọi lỗi |
| Min thiếu được ngầm đặt 0 | DWO còn chờ anh chốt min 0 tham khảo hoặc min thực. Phê duyệt cũ không trả lời câu hỏi mới |
| Office chặn, lặp Close/Raise/Enter không hiệu quả | Quyền anh đã đủ; công cụ/cửa sổ là giới hạn thật. Ngừng lặp, một AI điều khiển; bản in chưa thể |
| Hai AI cùng điều khiển desktop | Active request là công cụ đang bận, không chứng nút đã bấm. Điều phối tuần tự |
| With sqlite3.connect không đóng kết nối | Kiểm phối hợp đầu có 7 lỗi dọn kho tạm trên Windows. ClosingConnection đóng ở __exit__; chạy lại 8/8 đạt. Đây không phải kiểm catfix |
| FINAL hoặc báo cáo AI được coi đã nghiệm thu | Đúng mã tệp thật + người kiểm độc lập + số/đồ họa/bảo toàn/phạm vi. Tên tệp không có quyền ưu tiên |

Thông báo thật: FileExistsError là tệp đã tồn tại; INPUT_CHANGED là đầu vào đổi; Computer Use helper already has an active request là công cụ đang bận; failed to activate captured window là chưa đưa được cửa sổ lên. Không diễn giải thành thao tác thành công.

Thuật ngữ: RAM là bộ nhớ; glyph là hình ký tự; ROI là vùng kiểm/sửa; CTM là ma trận đặt ảnh; dpi là điểm ảnh mỗi inch; SHA-256 là mã kiểm nội dung; helper là hàm phụ; sourcefit là khớp ảnh nguồn; renderer là công cụ dựng ảnh từ tài liệu; series là một dãy dữ liệu biểu đồ; extrema là giá trị lớn/nhỏ nhất.

Không dùng ngưỡng lỏng/hộp lớn/bỏ mép để làm kết quả xanh. Hai mẫu PDF cùng cách không đạt thì dừng; giữ chứng cứ và lý do. Mã trong archive phải đọc trước nhập, vì có chương trình ghi ngay khi nhập mô-đun.


## Bổ sung hiện hành 06/10/2026

Các hàng thiếufont/DWOmin ở trên giữ làm lịch sử. Quyềnphông gần vàDWOmin1/max đãđược anh chốt; xem rules/QUY_TAC_CUNG_HIEN_HANH.md. Lỗi SP6 thực tế, Unicode/API/metadata và chi phí được ghi đầy đủ tại [BAI_HOC_SP6_VE_LAI_20261006.md](BAI_HOC_SP6_VE_LAI_20261006.md). Bắt buộc kiểm nhãn với TẤT CẢ đường lân cận, giữ n≈2850/P2; hai mẫu thất bại không được nhân rộng. Hồsơ mẫu có trạngthái tại templates/catalogue/SP6_VECTOR_V1.


## Yêu cầu logo/bảng và kiểm công suất 06/10/2026

Đọc rules/BO_SUNG_LOGO_BANG_QH_CONG_SUAT_20261006.md: logo không có ô nền khác màu; bảng rõ khung MODEL/P₂/Q(m³/h,l/min)/H(m); giữ điểm làm việc,Qmax,Hmax; công khai cách đo độ khớp≥95%; ghi bất thường thứ tự công suất trong cùng dòng/điều kiện để sửa sau. Không tự đổi426H hoặc lặp cách đặt nhãn đãSTOP2.


## Logo/bảng theo ảnh anh nhắc

Không đặtlogoảnhnềnxanh thànhôvuông trênnềnkhác. Dùng nguyênlogoPerotac rõ từnguồnWC1041×356 trênnềntrắng: đãkiểmđộc lập. Bảng phải hiệnMODEL/P₂/Qhaiđơnvị/H(m), khungđầu bảngtáchrõ. Arial hiệncó thiếuU+2082: dựngP và2chỉsốdưới bằnghaiđoạnchữcófontthật, không tựđoánký tự. Lỗi này chỉtiềnkiểm,0PDFtạo khi lỗi. Ngưỡngcũcho1mkhôngchứngđạt5%:6SP36-2 Q48,H14/13.2222 lệch5.56%,đãghiCHƯAĐẠT mới. NhãncũSTOP2giữ.


## Tránh dùng dữ liệu cũ trái quyết định mới về điện/họng xả

Từ lời anh06/10: >3kW không được liệt kê1pha; ≤3kW không có nghĩa tự có đủ cả hai biến thể. 4inch là thân bơmSA nhựa, không là họng xả; đúngdải4/6/8/10 xả1,5inch,12/16 xả2inch. Không so tên bằng chuỗi con hoặc áp sangSP/SL/SS. DữliệuSP6 có4cờ1pha>3kW tại knowledge/XUNG_DOT_DIEN_SP6_20261006.json; chưa sửaPDF vàkhôngnhận đãràtoànbộ.


## Model đầy đủ, nét bảng, trục Q/H — 06/10/2026

Đọc rules/BO_SUNG_FULL_MODEL_NET_BANG_TRUC_20261006.md: fullmodel3pha trênđường khi cócảhai; nétliền; Q ngaydướiQH/trênη; Total head H(m) dọctrục, bỏH(m)rời vàsốđếmmodel. Kẻbảngsaucùngtoànbộnềnô,cùngmàunét. Không chạy lại cách nhãn suffixđãSTOP2. Anhđãxácnhậnsửa mẫu.


## SP6 V3 đã giải quyết — 20261006T034834Z

Bảng đậm/nhạt do nền dòng sau che một phần nét dòng trước: vẽ toàn bộ lưới sau tất cả nền, cùng 0,6 pt/màu, không đè lặp. Nhãn đầy đủ phải kiểm bao nét chữ với mọi đường/lưới/nhãn, có thể bố trí theo tiếp tuyến; hai nhãn thấp cần vị trí riêng, không dùng quy tắc chỉ đặt phía trên. Xóa phần lưới sau chữ bằng đoạn vector, không che ô trắng hoặc cắt đường Q–H. V3 một ứng viên đạt kiểm hình độc lập, 426 H giữ, sai lệch max4,9201%; 6SP36-2 chỉnh đường C2, không đổi số. Bốn biến thể 1 pha>3kW đã bỏ trong mẫu V3, không suy bản chính đã sửa. Thư viện templates/catalogue/SP6_FULL_MODEL_V3; các phương án STOP2 cũ giữ đóng.


## SP ba hãng 06/10/2026 — bài học đã kiểm

- Không đoán Aquaris 32 trang có SA: đã đọc thực tế tất cả là SP inox; chỉ bỏ 4SP2 sau lệnh trực tiếp.
- Không lấy bộ Perotac đè Aquaris có nguồn riêng. Redpump không có nguồn riêng được anh chốt dùng Perotac.
- Metadata cũ có thể đọc sai: 4SP5-29 tại Q2.4 là H153 trong cả nguồn và bản chính, hồ sơ cũ ghi163 sai. Kiểm ảnh thật trước hỏi sửa số.
- Phải phân biệt nguồn ban đầu và bản chính đã sửa: 6SP46-7 T1767 ở nguồn ban đầu, T1827 ở bản chính, người chép1827 không sai. Giữ thay đổi đã chốt.
- Aquaris thay panel/xóa chữ theo vùng thất bại hai mẫu do nhãn xoay nằm lệch ra ngoài: STOP2, không chạy lại bằng cách nới vùng. Phương pháp khác đã kiểm: đối chiếu hình từng glyph nguồn, khóa SHA và đúng4objectID rồi xóa chính xác, kiểm ngoài vùng0; tiếp đó bổ sung đúng20vạch header riêng, không dựng lại panel.
- Phải kiểm hai hàng đầu bảng riêng: giữ nguyên ảnh thân bảng không chứng header kW/HP rõ khung. 20 separator thiếu đã bổ sung, kiểm độc lập cả20 crop.
- Không thu nhỏ chữ nhãn để nhồi4plot. Giải pháp hai plot/trang có mẫu xem trước; chờ chốt số trang, không tự coi quyền vẽ lại là đã duyệt tăng trang.
- 6SP36-28 nguồn thiếu dòng kích thước: giữ CHƯA CÓ DỮ LIỆU, không suy kích thước/cân nặng. Ảnh bơm gốc thấp phân giải không thể nhận là ảnh mới nét cao.



## SP ba hãng REVIEW02 — bài học đã kiểm 06/10/2026

- Không chọn ảnh PDF chỉ theo diện tích pixel lớn nhất: nguồn10SP có patch biểu đồ lớn; phải xác minh xref/bbox/ảnh thực. REVIEW01 thiếu ảnh, REVIEW02 dùng đúng184 và kiểm pixel nguồn.
- Preview SVG không chứng PDF lưu đúng. Đọc lại đủ trang của tệp cuối; kiểm ảnh, đường kính thân/motor, các ô và nhãn từ chính PDF.
- Clearance không đủ chứng nhãn thuộc đường nào: cặp6SP18-5/-7,6SP30-5/-6 phải có leader riêng rõ. Không đổi tên phương pháp để lặp STOP2.
- Dataset hoặc báo cáo RAM không cao hơn quyết định anh: việc133 đã chốt6SP60-20=103/72, dataset sơ bộ110/80 là lùi số. Dùng data_approved.json và so task gốc/canonical trước áp nguồn cũ.
- Không sửa nhầm số từ ảnh nhỏ: 4SP10-33 từng bị đọc nhầm32; crop nét cao và chữ thật xác nhận33.
- Kiểm điện bằng chuỗi đơn vị đầy đủ, không tìm riêng220 vì có thể là H220m.
- Một pha phải có tên ba pha: thêm đúngmodel ở QH/dimensions/nhãn; không suy số kích thước/cân nặng/dòng điện thiếu.
- REDPUMP dùng Perotac đã đạt; body13/13trang giống pixel/chữ/vector, chỉ đổi header/logo/footer. Không tính lại cùng mốc vào149việc gốc.

Bằng chứng: templates/catalogue/SP_THREE_BRANDS_V2_20261006/manifest.json và work/sp_three_brands/perotac_redpump_accepted.json. REVIEW01 giữ FAIL; REVIEW02 đạt số/hình trên tệp thật. Ảnh nguồn, thiếu dimensions và in giấy giữ giới hạn riêng.

## SP V3 — bài học bắt buộc sau anh trả lại ngày06/10/2026

- **C2/khớp số không chứng đường cong đều:** đường qua từng điểm bằng spline có thể gợn. Dùng đa thức toàn miền hoặc splineC2 có độ cong cùng chiều; kiểm đạo hàm/độ cong toàn miền và nhìn từng chart. Phải kiểm lại dữ liệu5%,min/max,duty và thứ tự công suất. LượtV3 giữ toàn bộH; không áp bộ thử đổi30H AQ đã bỏ.
- **Khóa ô bảng khác khóa điểm làm việc:** bảy ô G01 và các ô G05/4SP14 đã duyệt phải giữ giá trị, đường có thể lệch≤5% nếu không được chốt làduty. Không tự suy duty từ tên model.
- **Khổ trang không đồng nhất:** AQp26/27 nhỏ hơn29trang còn lại. REVIEW01 dùng chiều cao chung gây lệch25pt; phải đọc từng CropBox/MediaBox và fit nội dung đúng khổ, giữbox. REVIEW02 sửa đạt. Không kết luận previewSVG chứng PDF đúng.
- **Float renderer gây dấu cong giả:** đọcrawdecimaloperators+CTM và tính biên sai số từ làm tròn khi H''≈0. 8SP77-2 nhiễuH''3.983e−11, sai Htoànđường≤6.623e−9m đãđịnhlượng; không nới ngưỡng tùy ý để đạt.
- **Đổi curve phải kiểm nhãn lại:**127nhãn PR/RP cũ va chạm sau fit; hai lầnRAMnhét chữ cùngkhe vẫn khó xác định chủđường đã dừng. Cácnhãn6SP30-4/6SP36-6/-7 chuyểnra cuốiđường với9leaders kiểm riêng. Clearancekhông thay nhìn owner thực.
- **Khác hãng phải khác giao diện:** không chỉ logo/tên. V3PRxanhnhạt/đầu tranglogo trái; RPđỏtrầm/than/logo phải vàđảokhối; AQxanhngọc/portrait. LogoPR01ôtrắng sátlogo bịloại;02vùnglogo trắng fullheightliềnméptrái, nềnxanhriêng đãđạt.
- **Đảo khối phải dịch cả clip:** RP01 chứa đủ15ηpath nhưng clipvẫnởvịtrícũ làm toàn bộηbiếnmất. Đếmpath không đủ. RP02dịchclip±404pt đúngpath, kiểm15cropthật và tọađộraw, ngoài vùngsửa0pixelđổi.
- **Giảm dung lượng không làm mờ:** AQ31dùng15thamchiếu ảnhpatchtrùng; dedupXObject qua catfix từ38.1MBcòn7.87MB, giữ31contentrawvà31renderpixel. Không resample/rasterhóatoàntrang.
- **Báo đúng giới hạn ảnh:** SUMOTOAQxóa vùng đãnhận diện, cơkhígiữ; ảnhPR/RPcápche vànguồnthấpnétdấumờUNKNOWN, không nói chắc sạch/HD. Ingiấy chưa kiểm; chiều dài/cânnặngthiếu không đoán.

Bằng chứng hiện hành: work/sp_brand_redesign_20261006/accepted_final.json; hai bộqa_visual/independent_curve_qa, mẫuSP_THREE_BRANDS_V3_20261006. 0Hdelta,137/149gốcgiữ. Các kết luậnV2 là lịch sử, không dùng để bỏqua phản hồi mới.
