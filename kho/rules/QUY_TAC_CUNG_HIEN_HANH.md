ĐÃ GỘP vào rules/QUY_TAC_HIEN_HANH.md ngày 13/10/2026 — chỉ tra lịch sử; lệch thì QUY_TAC_HIEN_HANH thắng. Các tệp rules/BO_SUNG_*, rules/PHOI_HOP_CHATGPT_CLAUDE.md, rules/QUY_TAC_DIEN_HONG_XA_SA_20261006.md nhắc dưới đây đã chuyển sang archive/rules_cu_20261013/ (bản .json vẫn ở rules/). Giữ tệp này tại chỗ vì templates/ còn trỏ tới.

# Quy tắc cứng và quyết định hiện hành — 06/10/2026

Anh Trung trực tiếp yêu cầu: “các việc a bảo sửa, nhắc em hay tất cả quy tắc cách làm lỗi đã xảy ra e ghi hết lại để sau k mắc nữa nhé. cái này lưu vào quy tắc cứng cho a. cách làm phương án làm cũng lưu lại cho a nhé để làm cho chuẩn. form mẫu e cũng lưu lại sau này a báo cần sửa thông số gì ở catalogue thì e lôi ra sửa lại cho nhanh nhé”.

Tệp này là đầu mối bắt buộc đọc cùng QUY_TAC_ANH_TRUNG.md, PHOI_HOP_CHATGPT_CLAUDE.md và sổ gốc trong manifest. Những yêu cầu/lỗi lịch sử giữ ở tài liệu đã lập, không xóa hoặc coi mọi báo cáo AI là quyết định của anh. Quyết định mới của anh ưu tiên trong đúng phạm vi; ghi ngày, lời giao, tệp/mã/đơn vị bị tác động, trạng thái và bằng chứng. Không hỏi lại điều đã rõ.

## 1. Các quyết định mới thay điều cũ

- **Phông chữ:** anh đã cho dùng phông giống hoặc sát nhất cho phần thiếu chữ. Không tiếp tục chờ quyền này. Phải phân biệt “gần giống” với “đúng phông”, kiểm dáng/cỡ/độ đậm/màu/căn lề trên PDF thật. Không vì quyền này mà tự làm lại 25 catalogue, cài phông mới hay bỏ kiểm nghiệm thu.
- **DWO:** Qmin=1 m³/h, Hmin=1 m cho bảy mã. DWO150 cả 220V/380V dùng Qmax33 m³/h, Hmax15 m; ảnh dòng380V bị đảo, anh đã đính chính. DWO500=3,7kW/Qmax72/Hmax25. Đọc bảng đủ bảy mã tại [quyết định gốc](../knowledge/QUYET_DINH_MOI_PHONG_GAN_NHAT_DWO_MINMAX_20261006.md). Không hỏi lại14số min, không lấy0, không nhầm giá trị khóa với dữ liệu thử nghiệm hãng. Các đoạn tự dựng vẫn là đường tham khảo.
- **Ba bộ nghiên cứu:** SP Perotac12trang, SL Redpump11trang, SA Perotac11trang; được nghiên cứu bố cục khác nhẹ, hình rõ, ưu tiên đúng/đẹp/nhanh/ít token. Lời giao tiếp theo chỉ yêu cầu thử một trang. Mẫu đã làm là SP trang6; chưa có quyền suy thành đã duyệt mẫu hoặc hoàn thành34trang. SA có cả dảiSS, giữ đúng từng dòng; không đổi thương hiệu SL thànhPerotac vì báo cáo cũ gọi nhầm.
- **Phạm vi hiện tại:** yêu cầu lưu quy tắc/mẫu không phải yêu cầu sửa PDF mới hoặc mở lại phương án đã dừng. 137/149 là mốc lịch sử của149việc gốc; không cộng các mẫu/phần mở rộng vào đó.

## 2. Chuẩn bắt buộc mỗi lần sửa

1. Đọc nguồn chung, tiến độ/checkpoint và hồ sơ đúng tệp; kiểm bản thật/SHA. Gián đoạn trước sửa catalogue phải chạy đủ BƯỚC0/43kiểm, health không thay BƯỚC0. Không làm lại phần đã đạt. Lần chỉ lưu tài liệu/quy tắc không tạo PDF không cần giả nhận đã chạy43kiểm mới.
2. Nguồn bất biến; một khóa ghi/một catalogue; kiểm đầu vào trước lô ghi. INPUT_CHANGED phải đọc lại/phân tích thay đổi, không bỏ SHA. Chỉ catfix ghi catalogue, không sửa catfix/cài thêm, không che bằng ô trắng/màu hay raster hóa cả trang.
3. Trước vẽ phải có bảng kê toàn bộ model, kW/HP/P1/P2 đúng nguồn, pha/điện áp/Hz, Q/H/đơn vị, tốc độ và dấu ≈/=/≤/≥, kích thước/ống, ảnh/logo/nội dung. Thiếu thì giữ CHƯA THỂ XÁC MINH, không thay bằng0 hoặc đoán. Mỗi số đổi có cũ→mới, nguồn/quyền và tác động đến bảng/đường/trang khác.
4. Q tăng thì H giảm theo yêu cầu anh, giữ các min/max/điểm làm việc đã khóa. Kiểm toàn đường, không chỉ các điểm lấy mẫu. Sửa số trung gian nguyên đúng quyền; khóa mâu thuẫn thì lập bằng chứng. Không áp đơn điệuH lênη hoặc công suất. Không gọi đường đi chính xác qua mọi ô nếu chỉ đạt sai số cho phép.
5. Chữ/nhãn phải đọc rõ và không bị bất kỳ đường/lưới/nhãn khác xuyên. Kiểm tất cả nhãn với tất cả đường lân cận, cả nét đứt/liền; không chỉ khoảng cách với đường mang chính nhãn đó. Không thu chữ nhỏ để che vấn đề, không dùng ảnh thu nhỏ làm chứng. Mỗi biểu đồ đồng màu/độ dày/độ rõ/nét mượt; đo từ PDF đã lưu.
6. Hình sản phẩm đúng model/cấu tạo; dùng ảnh gốc rõ. Không sinh lại cấu tạo bằngAI, không lấy phóng ảnh150ppi thành300ppi làm chứng nét hơn. Chữ/bảng/đồ thị kỹ thuật ưu tiênvector trong phạm vi thiết kế mới được giao. Logoảnhgốc vẫn phải công bố giới hạn, η dò ảnh không thành dữ liệu hãng.
7. Kiểm số, hình thức, bảo toàn và bản in là các kết quả riêng. Render mọi trang bị đổi ở cỡ đọc bình thường và phóng vùng rủi ro; người kiểm độc lập đọc nguồn và PDF thật. Giữ khổ/trang/tài nguyên/metadata/link/mục lục theo phạm vi; không nới vùng/ngưỡng0/đệm0 cho vừa lỗi. Quyền đổi bố cục không cho bỏ thông tin/ký hiệu.
8. Hai lần cùng cách sửa PDF không đạt: lưu cả hai, đóng cách đó. Không đổi tên, nới ngưỡng hoặc sửa riêng một nhãn rồi bỏ qua toàn cụm để tiếp tục vô hạn. Phương án mới phải nêu thay đổi thực chất và kiểm trước khi tạo ứng viên; hiện không mở lại mẫuSP6.
9. Bản chính chỉ nhận đúng byte ứng viên đã nghiệm thu sau sao lưu và đọc lại; không ghi trực tiếp lên bản đạt. Báo cáo8cột, ảnh trước/sau, mã kiểm, lỗi/giới hạn/bước tiếp theo. Không hứa bộ khóa ngăn mọi chương trình bên ngoài, không nhận AI khác đã đọc chỉ vì tệp đã lưu.

## 3. Lưu và tái sử dụng là việc bắt buộc

- Sau mỗi yêu cầu/sửa/nhắc hoặc lỗi có ý nghĩa: bổ sung quyết định, nguyên nhân đã biết (chưa biết ghi rõ), cách tránh, phạm vi áp dụng, bằng chứng và trạng thái. Giữ lịch sử, không biến một lỗi cục bộ thành quy luật vô căn cứ.
- Tra [sổ lỗi](../knowledge/LOI_VA_CACH_TRANH.md), [lỗi mẫuSP6](../knowledge/BAI_HOC_SP6_VE_LAI_20261006.md), [bản đồ chứng cứ](../knowledge/BAN_DO_MA_NGUON_VA_BANG_CHUNG.md) và checkpoint trước chọn cách.
- Tra [thư viện mẫu](../templates/catalogue/README.md) trước sửa thông số. Dữ liệu, cấu hình trình bày, mã dựng và bằng chứng tách riêng; mẫu cótrạngthái, SHA, tệp/model/phạmvi. MẫuCHƯAĐẠT chỉ tái dùng phần đã kiểm, không nhân rộng bố trí lỗi.
- Không chạy lại mã cũ chứa số/tọađộ/đườngdẫn/tokenkhóaSHA cốđịnh. Giữ bản lịch sử; lập bản tác vụ mới với nguồn mới được xác minh, khóa mới và đầu ra mới. Đọc đúng phần thay đổi, dùng phép kiểm tự động cho dữ liệu lặp; giữ kiểm hình cuối.

## 4. Đo chi phí

Ghi riêng token đầu vào mới/đệm/đầu ra và mốc đo; suy luận đã trong đầu ra, không cộng hai lần. Credit tài khoản dùng chung không là chi phí riêng một trang khi còn phiên khác chạy; không tự đổi sang USD/VND hoặc đặt tỷ lệ token/Credit. Chi phí thiết lập mẫu không được nhân thẳng thành giá mỗi trang. Hồ sơ đo gốc ở deliverables/SP TRANG 6 MAU VE LAI 20261006.


## Yêu cầu logo/bảng và kiểm công suất 06/10/2026

Đọc rules/BO_SUNG_LOGO_BANG_QH_CONG_SUAT_20261006.md: logo không có ô nền khác màu; bảng rõ khung MODEL/P₂/Q(m³/h,l/min)/H(m); giữ điểm làm việc,Qmax,Hmax; công khai cách đo độ khớp≥95%; ghi bất thường thứ tự công suất trong cùng dòng/điều kiện để sửa sau. Không tự đổi426H hoặc lặp cách đặt nhãn đãSTOP2.


## Điện và họng xả SA — chốt trực tiếp 06/10/2026

Bắt buộc áp [quy tắc điện/họng xả](QUY_TAC_DIEN_HONG_XA_SA_20261006.md): ≤3kW mới có thể có bản1pha, >3kW chỉ3pha; không tự tạo biến thể1pha khi chưa có model. Giếng nhựaSA thân4inch: 4SA4/6/8/10 xả1,5inch; 4SA12/16 xả2inch. Quy tắc có dữ liệuJSON để kiểm; không áp sang SP/SL/SS hoặc đồng nhất cỡ thân với họng xả.


## Model đầy đủ, nét bảng, trục Q/H — 06/10/2026

Đọc rules/BO_SUNG_FULL_MODEL_NET_BANG_TRUC_20261006.md: fullmodel3pha trênđường khi cócảhai; nétliền; Q ngaydướiQH/trênη; Total head H(m) dọctrục, bỏH(m)rời vàsốđếmmodel. Kẻbảngsaucùngtoànbộnềnô,cùngmàunét. Không chạy lại cách nhãn suffixđãSTOP2. Anhđãxácnhậnsửa mẫu.


## Cập nhật trạng thái mẫu SP6

Mốc cũ “hiện không mở lại mẫuSP6” đã được thay bởi lệnh trực tiếp “được rồi e sửa lại cho a đi”. Phương pháp mới full model theo tiếp tuyến đã kiểm đạt một trang, lưu SP6_FULL_MODEL_V3; không mở lại các cách STOP2. Các câu “chỉ lưu tài liệu” ở mốc trước là lịch sử, không phủ định lệnh sửa mới.

## Đủ ba thương hiệu — yêu cầu trực tiếp mới

Bắt buộc đọc [quy tắc ba thương hiệu](QUY_TAC_BA_THUONG_HIEU_20261006.md). Mọi catalogue phải được đối chiếu Redpump, Perotac, Aquaris; thiếu phải báo anh để làm, yêu cầu mới thiếu phải hỏi lại. Không được bỏ qua hoặc tự coi thiếu là đủ.


## Thiết kế dễ nhìn, dễ đọc, dễ hiểu và đơn giản — 06/10/2026

Anh Trung trực tiếp chốt: “Phương án thiết kế của e luôn phải dựa trên phương án dễ nhìn đọc hiếu và đơn giản ng dùng cần thông tin thôi k đc lòe loẹt khó nhìn”. Áp dụng cho mọi phương án thiết kế, mẫu và catalogue trong dự án, gồm Redpump, Perotac và Aquaris.

- Ưu tiên người dùng tìm, đọc và hiểu thông tin nhanh. Trình bày model, công suất, điện, Q/H, đơn vị và thông tin kỹ thuật cần thiết rõ ràng, có thứ tự nhất quán.
- Bố cục đơn giản; chữ dễ đọc ở kích thước sử dụng bình thường; bảng, ô và đường đặc tính dễ đối chiếu. Không thu nhỏ chữ hoặc nhồi nội dung để tạo vẻ đẹp hình thức.
- Dùng màu có tiết chế, tương phản rõ; màu thương hiệu phục vụ nhận diện và phân biệt thông tin. Không dùng màu lòe loẹt, nền/hiệu ứng/họa tiết trang trí làm khó đọc hoặc gây nhầm.
- Mỗi yếu tố trình bày phải giúp nhận diện, tìm hoặc hiểu thông tin. Bỏ trang trí không cần thiết; không bỏ thông số, đơn vị hoặc nội dung bắt buộc để đơn giản hóa.
- Khi chọn giữa các phương án, ưu tiên phương án dễ đọc và dễ tra thông số hơn. Kiểm hình thức trên tệp thật ở cỡ đọc bình thường; phương án rối, khó đọc hoặc cần giải thích cách nhìn là CHƯA ĐẠT và cần chỉnh trong phạm vi được giao.

Quy tắc có hiệu lực cho việc thiết kế tiếp theo; lượt này chỉ lưu quy tắc và bước kiểm, chưa sửa hoặc nghiệm thu lại các PDF hiện có.



## Điện áp thống nhất — 06/10/2026

Anh chốt mọi catalogue: **1 pha/1~ = 220–240 V; 3 pha/3~ = 380–415 V**. Áp dụng cùng quy tắc 1 pha ≤3 kW, trên 3 kW chỉ 3 pha. Kiểm bảng/tiêu đề/chú thích và mọi thông tin điện; không tự đổi model. Chi tiết và dữ liệu kiểm tại rules/QUY_TAC_DIEN_HONG_XA_SA_20261006.md/.json. Chỉ lưu quy tắc trong lượt này, chưa nhận đã sửa mọi tệp.


## Lệnh triển khai SP ba hãng và tổng hợp mới nhất

Đọc bắt buộc [CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md](CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md). Anh đã cho bắt đầu SP đủba hãng; mọiđầu raPDF; ngônngữAnh (AquarisđượcgiữÝcũ); sốQ/H nguyên; tốcđộtheonguồn dạng/min; chỉ50Hz; giếng6inch không1pha; họngxảgiếng4/5/6inch theoquytắcmới; phạmvi15nhóm vàngoạilệFS/Roots. Yêucầuđợi trướcđây đãkếtthúc bởi lời“em làm đi”; chỉSP đangthựchiện.


## Nguồn hãng thiếu và lưu lượng số lẻ — chốt mới

**Mọi catalogue: Redpump hoặcAquaris chưa cónguồnriêng thìdùng nguồnPerotac đãkiểm. Cónguồnriêng thìgiữnguồnriêng.** SPRedpump dùngPerotac,SPAquaris dùng32trangSPinoxđãkiểm phânloại. Qđượcgiữ1chữsốthậpphân theo nguồn (vd1.5), thayquytắcQnguyên tuyệtđối; Hgiữnguyên yêu cầusốnguyên. Chi tiếtphạmvi/nguồn tại CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md.


## Ngoại lệ danh mục SP mới nhất

Bỏ toàn bộ 4SP2/4SPM2 khỏi cả PEROTAC, REDPUMP, AQUARIS theo quyết định trực tiếp của anh. Giữ 3SP2 và nguồn gốc. AQUARIS đã thành 31 trang sau bỏ 4SP2; mốc “32 trang SP inox” phía trên là phân loại nguồn trước khi bỏ dải, không phải số trang bản giao mới. Xem hồ sơ SP ba hãng và CURRENT_CHECKPOINT trước dùng lại.

## Model có 1 pha phải có 3 pha — quyết định trực tiếp 06/10/2026

Anh Trung chốt: “Model nào có 1 pha thì phải có 3 pha nhé em không để trống 3 pha khi có 1 pha lưu quy tắc cho a”. Áp dụng toàn bộ catalogue, cả ba thương hiệu. Khi model1pha được liệt kê hợp lệ, bắt buộc có model3pha tương ứng, không để dấu gạch hoặc ô trống trong cột model3pha. Dùng quy ước tên đúng dòng sản phẩm (SP: bỏ chữ M); đường đặc tính ghi fullmodel3pha khi có hai bản. Đây là quyền bổ sung biến thể3pha mới, thay cách giữ trốngmodel3pha theo nguồn thiếu trước đó. Điện áp vẫn1pha220–240V/3pha380–415V, chỉ50Hz; >3kW và giếng6inch chỉ3pha. Không suy thêm kích thước/cân nặng/dòng điện3pha còn thiếu. Kiểm cả bảngQH, bảngkíchthước và nhãn đường.

Cùng lượt anh chốt PEROTAC/REDPUMP SP: tên4SP14; 4SP14-4 tạiQ3.6/H24 vàQ5.4/H23; đồng ý tách12→13trang. Hồsơ quyền: work/sp_three_brands/USER_FINAL_APPROVAL_20261006.md và user_decisions.json.

## Đường cong đều, sai lệch 5%, thiết kế lại AQUARIS và xóa SUMOTO — 06/10/2026

Anh trực tiếp chỉ lỗi đường AQUARIS 3SP1/5SP15 uốn gợn và giao: “màu sắc và thiết kế ... khác bản cũ ... chỉ lấy thông số bản cũ”, “các ảnh đại diện còn chữ sumoto ... xóa đi”, “đường ko đc ngoằn nghèo cong đều hết có thể lệch số ở bảng dưới ko quá 5% nếu cao hơn sửa số ở bảng thông số ... đây là quy tắc”.

- Đường Q–H phải giảm và cong đều, không gợn, đổi độ cong liên tiếp hoặc nhấp nhô. C1/C2 hoặc khớp số không tự chứng hình thức đạt. Ưu tiên đường đa thức toàn miền, kiểm đạo hàm/độ cong và nhìn PDF thật.
- Dung sai mới là |H_đường−H_bảng|/|H_bảng| ≤5% tại từng Q; H=0 thì giữ đúng0. Quyền này thay ngưỡng2% cũ trong phần đang sửa. Nếu vượt5%, được sửa H trung gian nguyên theo đường mới và lưu cũ→mới, không hỏi lại quyền này. Vẫn giữ Qmin/Qmax/Hmin/Hmax và điểm làm việc đã khóa; khóa mâu thuẫn phải báo, không phá khóa.
- AQUARIS SP dựng giao diện mới đơn giản, đổi màu/bố cục rõ rệt; kế thừa thông số đã chốt của AQUARIS, không ghi lùi các sửa cũ hoặc chép Perotac đè dữ liệu riêng. Giữ nội dung kỹ thuật, khổ và31trang hiện hành trừ khi anh giao khác.
- Xóa dấu SUMOTO còn trên ảnh đại diện của ba catalogue SP đang giao, giữ nguyên cấu tạo/biên dạng máy. Chỉ chỉnh dấu được xác minh; kiểm lại ảnh thực, không mặc nhiên nhận dấu nhỏ là đã sạch.
- Bản AQUARIS SHA9b2ca1ba...14e đã qua kiểm cũ nhưng bị anh trả lại về hình thức đường/giao diện; không dùng kết luận PASS cũ để bỏ qua lỗi này. Giữ tệp cũ làm bằng chứng, tạo ứng viên mới.

## Khác giao diện giữa các hãng và chặn lỗi cong gợn trước nghiệm thu — bổ sung trực tiếp 06/10/2026

Anh yêu cầu: PEROTAC và REDPUMP phải đổi màu sắc, nền đầu trang; “giao diện các hãng khác nhau với cùng loại bơm yêu cầu phải khác nhau”. Áp dụng mọi catalogue. Dữ liệu được dùng chung theo nguồn đã chốt, nhưng phải có cấu hình thiết kế riêng từng hãng, khác rõ ít nhất màu chủ đạo, xử lý nền đầu trang và cách trình bày. Không lòe loẹt, không chỉ thay logo/tên.

Anh tiếp tục chỉ lỗi cong ngoằn nghèo ở PEROTAC/REDPUMP và yêu cầu lưu ngay đầu dự án, kiểm kỹ khi nghiệm thu. Mở lại phần đường/giao diện của cả ba SP; không làm lại các số/kích thước đã đạt ngoài delta cần thiết. Bắt buộc kiểm từng đường toàn miền, sai lệch từng điểm ≤5%, các khóa; đồng thời nhìn mọi biểu đồ ở cỡ đọc thật và phóng vùng cần thiết để loại gợn, gãy, đổi độ cong bất thường. Không nhận PASS chỉ vì C2 hoặc số khớp. Phiếu QA phải có hai mục riêng, PDF/SHA/trang/biểu đồ và người kiểm; thiếu bằng chứng thì CHƯA ĐẠT. Không hứa không thể tái lỗi; dùng cửa kiểm bắt buộc để ngăn phát hành lỗi.

## Quyết định anh chốt trong phiên Claude 06/10/2026 — mục 1–18 (nhập 20261006T151425Z)

Nguồn: lời anh trực tiếp trong phiên Claude. Mục 14–18 là QUY TẮC CỨNG cho mọi phiên, mọi nhóm: ba hãng khác cả bố trí + màu sắc + cách trình bày; khóa việc theo phiên (`claude/khoa_viec.py` + `cat.py claim`); chạy song song nhiều AI; nghiệm thu hoàn chỉnh mới là xong; chỉ kiểm cái cần kiểm. Mục 14 mở rộng mục "Khác giao diện giữa các hãng" ở trên: thêm yêu cầu khác BỐ TRÍ.

1. **Vai trò:** Claude thay ChatGPT ROOT làm người điều phối, được ghi sổ TIEN DO.md và nhận bản chính sau nghiệm thu.
2. **Mục đích PDF:** đăng web và gửi Zalo (xem màn hình). Không phải bản gửi nhà in → RGB, không cần lề xén/dấu cắt; ưu tiên dung lượng gọn, chữ và đường vector rõ trên điện thoại/máy tính.
3. **12 việc gốc còn tồn (137/149):** anh trả lời "Làm tiếp" — Claude hiểu là VẪN LÀM, không bỏ. (Chờ anh xác nhận cách hiểu.)
4. **Ảnh sản phẩm:** làm đến catalogue nào thì gửi anh xem ảnh cũ của catalogue đó và hỏi; anh tải ảnh mới lên để thay. Không tự thay, không sinh ảnh.
5. **Duyệt mẫu:** mỗi nhóm làm mẫu trước, anh duyệt rồi mới dựng cả bộ.
6. **Dữ liệu thiếu:** làm đến nhóm nào hỏi nhóm đó, không hỏi dồn trước.
7. **Bìa/chân trang:** giữ thông tin theo bản cũ, hoặc không ghi, chỉ ghi tên hãng. Không tự thêm địa chỉ/điện thoại/website mới.

## WC cắt rác — anh chốt 06/10/2026 (phiên Claude)

8. Thiết kế lại cả bộ WC, mỗi hãng một giao diện riêng (cách B), làm mẫu trang 65WC cho mỗi hãng để anh duyệt trước.
9. Bốn mã mới 65WC30-40-7.5 (Qmax65/Hmax45), 80WC45-30-9.5 (120/40), 100WC120-15-9.5 (180/34), 150WC150-10-9.5 (240/27): cột áp tại Qmax = 1 m; điểm làm việc theo tên mã; chỉ 3 pha.
10. 9,5 kW ghi 13 HP.
11. Ảnh REDPUMP WC: bỏ chữ "7.5KW"/"11KW" in trên ảnh. Ảnh sản phẩm khác: anh chưa gửi ảnh mới → dùng ảnh cũ.
12. WC: mã 3 pha là **WC**, mã 1 pha là **WCD** (ví dụ 65WC25-10-1.5 / 65WCD25-10-1.5). Anh chốt 06/10 khi xem mẫu trang 65WC.
13. WC: cách chia bảng thông số cũng phải khác nhau giữa 3 hãng, không chỉ khác màu.

## Quy tắc cứng anh thêm 06/10/2026 ~15:10Z (phiên Claude) — áp cho MỌI phiên, mọi nhóm catalogue

14. **Ba hãng cùng một loại catalogue phải khác nhau cả ba mặt:** (a) **bố trí** — vị trí ảnh / khối thông tin / biểu đồ / bảng trên trang và cách chia bảng; (b) **màu sắc** — màu chủ đạo, nền đầu trang, màu đường và bảng; (c) **cách trình bày** — kiểu đầu trang, tiêu đề, bảng, nhãn, chú thích. Chỉ đổi màu hoặc logo là CHƯA ĐẠT. Số liệu vẫn giống nhau theo nguồn đã chốt; vẫn đơn giản, dễ đọc, không lòe loẹt. Trước khi dựng cả bộ: lập bảng 3 hãng × 3 mặt và làm mẫu cho anh duyệt. Mục QA "KHÁC GIAO DIỆN GIỮA CÁC HÃNG" chấm riêng từng mặt bố trí / màu / trình bày, đặt ba trang cùng model cạnh nhau để nhìn.
15. **Phiên nào làm việc nào thì khóa việc đó.** Trước khi bắt đầu: `python3 claude/khoa_viec.py xem` và `cat.py status`. Nhận khóa việc `khoa_viec.py nhan <TEN_VIEC> <MA_PHIEN> "<phạm vi>"`; nếu ghi một trong 25 catalogue gốc thì nhận thêm `cat.py claim`. Việc đang có phiên khác giữ: KHÔNG đọc-sửa, KHÔNG ghi, KHÔNG chiếm khóa kể cả khi khóa đã cũ — chọn việc khác hoặc báo anh. Chỉ ghi trong phạm vi đã khóa (tệp ứng viên, thư mục work của mình). Xong hoặc dừng thì nhả khóa kèm ghi chú kết quả. Tệp dùng chung (TRANG_THAI, QUYET_DINH, sổ): chỉ nối thêm đoạn của mình, đọc lại ngay trước khi ghi, không ghi đè đoạn của phiên khác. Không sửa tệp có niêm phong (rules/, tools/, procedures/...) khi còn phiên khác đang giữ khóa.
16. **Làm nhanh và tối ưu, chạy song song nhiều AI nhất có thể nhưng vẫn phải chính xác.** Tách việc thành các phần độc lập (theo hãng, theo nhóm, theo trang) và giao mỗi phần cho một AI phụ chạy cùng lúc; mỗi AI phụ một khóa riêng, một thư mục work riêng, một tệp đầu ra riêng, không hai AI ghi cùng một tệp. Phần dùng chung (thư viện vẽ, dữ liệu đã kiểm) chốt xong trước rồi mới tách. Việc cơ học dùng model rẻ; việc cần phán đoán (đường cong, thiết kế, nghiệm thu) dùng model mạnh. Không song song khi các phần phụ thuộc nhau hoặc cùng một tệp.
17. **Nghiệm thu hoàn chỉnh mới tính là xong.** Mỗi phần làm xong phải được kiểm lại độc lập (AI khác với AI đã làm), sai thì sửa rồi kiểm lại đúng chỗ sửa, đến khi đạt hết mới báo xong. Chưa kiểm hoặc còn lỗi = CHƯA XONG; không kiểm được = CHƯA THỂ XÁC MINH, ghi rõ.
18. **Chỉ kiểm cái cần kiểm.** Kiểm đúng phần vừa làm/vừa sửa và những gì bị nó ảnh hưởng trực tiếp (trang, biểu đồ, bảng, tệp đó). Không kiểm lan sang catalogue, nhóm, trang khác đã đạt và không đổi (chứng minh không đổi bằng SHA hoặc so sánh trang là đủ). Không đọc hết sổ dài, không xuất ảnh cả catalogue khi chỉ sửa vài trang.
