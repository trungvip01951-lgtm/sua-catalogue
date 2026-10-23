# Tổng hợp yêu cầu anh Trung — bắt đầu SP ba hãng, 06/10/2026

Nguồn: anh gửi từng yêu cầu và dặn chờ; lệnh mới “em làm đi cái nào cảm thấy số liệu sai thì hỏi a tiếp; đầu tiên em làm catalogue giếng SP cho a cả 3 hãng nhé” cho phép lưu và triển khai SP. Chỉ SP đang thực hiện; các loại khác lưu hàng đợi, không tự sửa đồng loạt. Lời giao rõ ba bản khác hãng và tái dùng dữ liệu giải quyết câu hỏi cũ về ba bản riêng hay gộp.

## Quy tắc hiện hành bổ sung, ưu tiên hơn mục cũ trong cùng phạm vi

1. Đầu ra mọi catalogue là PDF, không bàn giao Excel. Nguồn Excel của SS/DWO vẫn giữ bất biến.
2. Thiết kế đơn giản, dễ nhìn/đọc/hiểu, ưu tiên thông tin. Lưu bản sửa, dữ liệu, bố cục và bằng chứng để lần sau chỉ sửa phần ảnh hưởng; không làm lại phần đã đạt. Tra sổ gốc và tệp mới nhất trước nhận việc, ghi rõ hãng/phạm vi đã đạt và việc còn.
3. Cùng dòng khác hãng được tái dùng dữ liệu đã kiểm nếu thông số giống nhau, đổi thương hiệu/bố cục để phân biệt. Không mặc định các bộ nguồn khác nhau cùng số; phần mâu thuẫn hỏi anh. Không tự thay nguồn của hãng này bằng nguồn hãng khác khi chưa rõ phạm vi.
4. Ngôn ngữ catalogue: tiếng Anh, không tiếng Việt. Riêng Aquaris có thể giữ tiếng Ý đã có trong bản cũ; chuyển các ngôn ngữ khác sang tiếng Anh, giữ thương hiệu/model/đơn vị.
5. Mọi số lưu lượng Q và cột áp H hiển thị là số nguyên, không phần thập phân. Không tự làm tròn khóa max/min/điểm làm việc, hoặc làm các cột Q trùng nhau; gặp xung đột hỏi anh. Dữ liệu nội bộ giữ độ chính xác để tính và kiểm.
6. Chỉ 50 Hz. Bỏ phần thông số 60 Hz, không đổi nhãn 60 thành50 rồi giữ dữ liệu.
7. Tốc độ theo đúng catalogue gốc từng sản phẩm, có thể2950/2850/2900; chỉ chuẩn hóa thành n ≈ [tốc độ] /min theo ký hiệu nguồn, bỏ số1 trong1/min. Không áp2850 cho mọi bơm.
8. 1pha=220–240V,3pha=380–415V; >3kW chỉ3pha. Bơm giếng6inch bỏ TẤT CẢ bản1pha kể cả≤3kW. Trục ngang3M đầu inox vàCM không có1pha. Không mở rộng lệnh bỏ1pha sangCDX/DWO nếu chưa xác định anh giao phạm vi đó.
9. Họng xả bơm giếng nói chung: thân6inch=3inch; thân5inch=2,5inch; thân4inch dải4/6/8/10=1,5inch, dải12/16=2inch. Lệnh này mở rộng quy tắc cũ chỉSA nhựa. Dải4inch khác chưa được chỉ rõ thì giữ nguồn và hỏi nếu thấy nghi ngờ; không suy theo chuỗi con.
10. Bảng thiếu/trắng ô phải đối chiếu nguồn, không đoán/nội suy để lấp. Kiểm từng hàng/cột, khung ô đều nét, không coi ô trống bất thường là hoàn tất.

## Danh sách theo số anh đã chốt

| Số | Loại | Hãng/đầu ra phải làm | Yêu cầu riêng |
|---|---|---|---|
|1|CM|Aquaris,Perotac,Redpump|Bỏ1pha; khôi phục ôH ởQ12m³/h(200l/min) hai dòngCM32-160/1.5 và/2.2; bảng kích thước/khối lượng Aquaris trắng phải đối chiếu nguồn|
|2|3M|Aquaris,Perotac,thêmRedpump|Bỏ1pha; đổi3M32-160/30 thành3M32-160/3|
|3|WC cắt rác|Aquaris,Perotac,Redpump|Thêm4mã ở bảng dưới, không đoán điểm trung gian|
|4|SS nước thải|Perotac,thêmAquaris vàRedpump|SS-250 là3pha,khôngM/F;SSM-250F là1pha,cóM/F; PDF từ nguồnExcel|
|5|SP giếng|Aquaris,Perotac,thêmRedpump|LÀM TRƯỚC; bỏ1pha6inch,sửa họng xả; xóaSUMOTO trên ảnh4SP; xóa cả hai dòngTop chock/Bottom support nếu có, giữ dòng khác; áp mẫu đồ thị đã chốt|
|6|SA giếng|Aquaris,Perotac,thêmRedpump|Redpump dùng nguồnSL đổiSL thànhSA, kiểm dữ liệu trước tái dùng|
|7|SL riêng|Bỏ khỏi hàng đợi làm riêng|Giữ nguyên nguồnSL để làmSA Redpump, không xóa file|
|8|FS|ChỉAquaris, hai nguồn hiện có|FS inox bỏOutlet/họngxả; không áp bỏhọngxả mọibơm|
|9|IRG|Perotac,thêmAquaris vàRedpump|Bỏkíchthước/cânnặng; xóa3dòng đa ngôn ngữ vềinox304 cócho mọi model ởảnh khoanh|
|10|GB con sò|Perotac,thêmRedpump vàAquaris|Bỏkíchthước/cânnặng;3pha cóS(ví dụGB-2200S),1pha khôngS(GB-2200)|
|11|KTZ–LH|Giữ phạm vi trước:Perotac,Redpump|Aquaris chưa có trong danh mục; khi đến nhóm hỏi bổ sung theo quy tắcba hãng, không tự ghi đủ|
|12|CDLF|Aquaris,Perotac,thêmRedpump|Quy tắcchung vàviệc tồnđọng|
|13|CDX|Perotac,thêmRedpump vàAquaris|Quy tắcchung vàviệc tồnđọng|
|14|DWO|ĐủPerotac,Aquaris,Redpump|PDF; giữbảy bộmin/max đãchốt|
|15|Roots|Giữ nguyênPerotac|Không tự làmthêmhãng hoặc mởsửa ngoài lời giao|

FS chỉAquaris vàRoots chỉPerotac là ngoại lệ rõ của anh, không hỏi lại yêu cầu đủba hãng ởhai nhóm này. Đây làdanh sáchviệc mới, không cộng vào149việc gốc.

## Bốn mãWC mới

|Model|Qmax(m³/h)|Hmax(m)|
|---|---:|---:|
|65WC30-40-7.5|65|45|
|80WC45-30-9.5|120|40|
|100WC120-15-9.5|180|34|
|150WC150-10-9.5|240|27|

Chưa có đầy đủ điểm trung gian/min của4mã; không tự lấy0. Mục “Ảnh giếng inox ở catalogue” là lời nhắc chưa đủ nội dung, ngoài yêu cầu cụ thể xóaSUMOTO đã rõ.

## SP thực hiện ngay

Dùng bản mới nhất và mẫu SP6_FULL_MODEL_V3 đã đạt kiểm số/hình trongphạmvimẫu. MẫuV3 cần cập nhật theo lệnhmới bỏtoàn bộ1pha6inch vàđịnhdạngtốcđộ. Các phươngánSTOP2 cũ vẫnđóng. Cần kiểm bộAquaris32trang vàPerotac12trang trước dùngchung; giữ cácphần đúng đãkiểm, hỏi dữliệu nghi ngờ thayvì tự đoán. Mỗi hãng mộtPDF riêng, đúngnguồn và phạmvi, dữliệu/mã/bằngchứng lưu dùng lại.


## Chốt tiếp: SP inox, số lẻ lưu lượng và nguồn thay thế — 06/10/2026

- Chỉ triển khai SP giếng inox lúc này. Anh nghiAquaris32trang ghépSA/SP vàyêu cầutách nếu cóSA. Đãxem đủ32trang thật: bìa/mụclục vàcácdải3SP,4SP,5SP,6SP,8SP,10SP đều ghiSTAINLESS STEEL; chưa thấySA/plastic. Khôngcắt cácdải3SP/5SP vì bộPerotac khôngcó.
- Anh trảlời câuhỏiQ lẻ: “làm đúng số lẻ lưu lại quy tắc là đc lẻ 1 số VD 1,5”. Lưu lượngQ được giữ tốiđa1chữsố thậpphân theo nguồn (tiếngAnh dùngdấuchấm,vd1.5). Thay yêu cầuQnguyên tuyệtđối. CộtápH vẫnsốnguyên theo lệnhtrước; chỗnguồn/khóaH lẻ hoặcQcầnnhiềuhơn1số phải hỏi, không tựlàmtròn khóa.
- AnhchốtSPRedpump dùngdanhmục/sốliệuPerotac.
- Quy tắcchung mới: “tất cả catalogue nếu ko có nguồn thì REDPUMP lấy ở perotac, AQUARIS lấy ở perotac”. Áp mọi dòngcatalogue thiếu nguồnhãngriêng: dùng bộPerotac đãkiểm làmnguồn kỹthuật; lưu nguồn/SHA/dữliệuphụthuộc. Hãngđãcónguồnriêng thìgiữ; không lấyPerotacđè nguồnAquarisđangcó. Vẫn kiểmđiện/model/QH vàkhông coi dữliệunguồn nghi ngờ làđạt. Nếu Perotaccũngthiếudữliệu hoặc nguồnmâu thuẫn, hỏi anh.
- Đây làquyền dùngnguồn thaythế, khôngtựmởrộng hãng/phạmvi đãngoạilệ: FS chỉAquaris,Roots giữPerotac; cácnhómkhác chờđến lượt.



## Bỏ dải 4SP2 ở cả ba hãng — quyết định trực tiếp 06/10/2026

Anh trả lời câu hỏi 11 mã 4SPM2 thiếu công suất: **“Xoá dải 2 này đi cho a ko cần làm cả 3 hãng”**. Áp dụng bỏ toàn bộ **4SP2**, gồm các biến thể 4SPM2, khỏi catalogue SP của PEROTAC, REDPUMP và AQUARIS. Không mở rộng sang **3SP2** hoặc các dải khác. Nguồn gốc giữ nguyên.

- PEROTAC/REDPUMP: bỏ 11 dòng kích thước 4SP2. Không còn cần hỏi công suất các mã đã bỏ. Bảng Q–H Perotac vốn không có 4SP2.
- AQUARIS: bỏ nguyên trang 4SP2, cập nhật mục lục và folio; bản mới 31 trang, giữ 3SP2.
- Quy tắc nguồn chung vẫn giữ: REDPUMP/AQUARIS thiếu nguồn riêng thì lấy PEROTAC; có nguồn riêng thì giữ nguồn riêng. Không lấy Perotac thay bộ Aquaris đang có.

