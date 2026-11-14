# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from khung import build, table, card
ok = '<span class="tag ok">đã sửa</span>'; c = lambda s: f'<code>{s}</code>'
A = [
 ('A1', 'Tệp rác bị đưa lên GitHub', '338 tệp: 290 mảnh tệp do ổ đĩa để lại trong <code>state/</code>, 28 ảnh xem tạm (67 phiên bản trong lịch sử), 14 tệp bộ đệm Python, 6 tệp khoá/tạm của LibreOffice.', 'Gỡ khỏi GitHub, thêm <code>.gitignore</code> để không lọt lại.'),
 ('A2', 'Quy tắc hiện hành dừng ở 23/10', '22 quyết định của anh (QĐ 159–180) chưa được gộp vào <code>rules/QUY_TAC_HIEN_HANH.md</code>, dù quy tắc mục 9 bắt buộc gộp ngay.', 'Bản 2026.11.14: thêm 4.16–4.18 (catalogue riêng theo báo giá, số báo giá là điểm làm việc, mã WC là điểm làm việc, có Qmin thì chỉ vẽ Qmin–Qmax) và 6 ngoại lệ (bản tiếng Việt, 5 m/10 m của WC lớn, IRG có đường khi anh yêu cầu, không nâng hiệu suất…).'),
 ('A3', 'Quyết định ghi rải, thiếu số', 'Lời anh ngày 15/10, 16/10, 23/10 nằm ở 3 tệp riêng không có số QĐ; lệnh "làm bản chuẩn RPX / PRX / AQX" ngày 29/10 chưa được ghi ở đâu.', 'Chép nguyên văn thành QĐ 181–185 trong <code>rules/QUYET_DINH_ANH.md</code>; ghi quy tắc "chỉ ghi quyết định ở một tệp".'),
 ('A4', 'Tệp trạng thái lỗi thời', '<code>claude/TRANG_THAI_CLAUDE.md</code> ghi "cập nhật 13/10", vượt cỡ cho phép, thiếu 10 catalogue làm từ 29/10 đến 14/11.', 'Viết lại (6 KB): bảng 13 việc đang chờ anh, nơi gốc dữ liệu, mẫu mã dựng nên chép.'),
 ('A5', 'Danh sách việc chờ anh thiếu', '<code>claude/VIEC_CHO_ANH.md</code> dừng ở 14/10.', 'Thêm 13 catalogue riêng chờ duyệt (kèm câu hỏi còn mở) và 2 việc chờ anh trả lời.'),
 ('A6', 'Skill trong kho lỗi thời', 'Còn ghi "nối điểm bằng PCHIP", chưa có quy tắc tên tệp (QĐ 163), chưa nói kho ở GitHub, chưa có catalogue riêng theo báo giá.', 'Cập nhật <code>claude/skill/sua-catalogue/SKILL.md</code> và đóng lại tệp zip. Bản trên tài khoản của anh còn cũ hơn nữa — xem B1.'),
 ('A7', 'Dẫn chiếu sai', 'Sổ lỗi dẫn "QTH 8.13" (không có); <code>LOI_ANH_BAO</code> dẫn QĐ 95 (số cũ, nay là 106); <code>DU_LIEU/README</code> dẫn QĐ 71 (nay là 82); chuẩn trình bày ghi tên ảnh kho là "model_hãng.png" trong khi tệp thật đặt theo mã băm; quy tắc ghi tốc độ "min⁻¹" trong khi 62 bản đã duyệt ghi "/min".', 'Sửa cả 5 chỗ cho khớp thực tế.'),
 ('A8', 'Sổ lỗi thiếu bài học mới', 'Các lỗi gặp từ 30/10 chưa ghi.', 'Thêm 8 dòng vào <code>rules/LOI_DA_GAP.md</code> (C5–C7, A19–A22).'),
 ('A9', 'Công cụ vẽ đường in sai số cực', 'Ô ghi chữ "…n ≈ 2850 /min" bị in thành "2850 poles"; máy 4 cực thiếu tốc độ bị ghép "4 poles ≈ 2900"; nguồn không có số cực vẫn in "2 poles ≈ 2900" mà không cảnh báo; dòng số liệu sai tên model bị bỏ lặng lẽ (bảng vẽ ra thiếu điểm).', 'Sửa <code>tools/ve_duong_cong.py</code>: chỉ nhận số cực 2–12 và tốc độ 300–3600; ghi "KHÔNG GHI" thì bỏ hẳn cụm; in số mặc định thì có cảnh báo; dòng lạc thì dừng và báo số dòng. Đã quét 111 lượt đọc trên mọi tệp số liệu: không tệp nào bị ảnh hưởng.'),
 ('A10', 'Công cụ kiểm báo sai ở catalogue riêng', 'Nấc cột áp WC (QĐ 19) chỉ đếm trong PDF đang kiểm nên catalogue 1 mã luôn "sai"; chưa biết QĐ 179; "04 / 04" cạnh chữ "VẬT LIỆU" bị coi là điện áp; chân trang dài bị coi là chữ thân nhỏ; bản tiếng Việt anh yêu cầu bị tính lỗi.', 'Sửa <code>tools/kiem_catalogue.py</code>; thêm cờ <code>--tieng-viet</code>. Kiểm lại: WC 37–132 kW bản Anh và bản Việt, PEROTAC 200WC450-32-55 từ CHƯA ĐẠT thành ĐẠT 8/8; WC đã duyệt vẫn đạt.'),
 ('A11', 'Lệnh kiểm kho luôn báo CHƯA ĐẠT', '<code>cat.py health</code> báo thiếu Python (đường dẫn Windows) từ 23/10 nên kết quả thật bị che; <code>niem_phong.py</code> thiếu lý do thì văng lỗi sau khi đã ghi tệp; nhả khoá thiếu tham số không nói rõ khoá còn giữ.', 'Sửa <code>claude/cat.py</code>, <code>tools/niem_phong.py</code>, <code>claude/khoa_viec.py</code>.'),
 ('A12', 'Khởi động phiên đám mây lãng phí', 'Mỗi máy mới chép 154 MB thư viện bản Python 3.10 (không dùng được trên máy 3.13), cài hỏng rồi mới tải mạng; <code>openpyxl</code> không nằm trong danh sách cài; cài tesseract/qpdf hỏng thì không báo.', 'Sửa <code>claude/dau_phien.sh</code> và hook đầu phiên.'),
]
B = [
 dict(id='B1', t='Skill "sua-catalogue" trên tài khoản Claude của anh là bản cũ (trước 13/10)', rec=1,
      now='Bản đang được nạp mỗi phiên (7,8 KB) vẫn bảo AI đọc tệp quy tắc cũ, bắt chạy 43 bài kiểm trước mọi việc, và ghi "không chép catalogue lên đám mây". Bản trong kho (15 KB) đã đúng.',
      why='Em không tải skill lên tài khoản thay anh được. Tệp đã đóng sẵn: <code>kho/claude/skill/sua-catalogue.zip</code>.',
      opts=[('Anh tải tệp zip mới lên (Settings/Cài đặt → Capabilities/Tính năng → Skills/Kỹ năng → thay skill sua-catalogue)', 'AI mọi phiên sau đọc đúng quy tắc ngay từ đầu.'), ('Để nguyên', 'Vẫn chạy được vì CLAUDE.md trong kho ghi "lệch thì theo kho", nhưng mỗi phiên tốn chữ đọc một bản sai.')]),
 dict(id='B2', t='Số liệu gốc CM của AQUARIS đang lệch catalogue đã duyệt', rec=1,
      now='Ngày 30/10 em đã ghi số báo giá của 3 mã (CM 32-160/3, CM 40-250/11, CM 65-200/22) vào <code>DU_LIEU/CM.xlsx</code>, trong khi "AQUARIS - Bơm trục ngang CM.pdf" đã duyệt vẫn mang số cũ. Bản vá "AQUARIS - Bơm trục ngang CM 1.pdf" chờ anh từ hôm đó. Trang tự kiểm trong tệp số liệu vẫn ghi 3 mã này "giống 2 hãng kia" — đã sai.',
      why='Đây là lỗi quy trình của em: số liệu gốc chỉ được sửa sau khi anh duyệt. Đã ghi vào sổ lỗi (C6).',
      opts=[('Duyệt bản vá "AQUARIS CM 1" → em thay bản đã duyệt, cập nhật trang tự kiểm', 'Số liệu gốc và PDF đã duyệt khớp lại. Còn 2 câu hỏi của bản vá ở mục D9 trong danh sách việc chờ anh.'), ('Trả số liệu gốc về số cũ; bản vá chỉ là catalogue riêng theo báo giá', 'Đúng quy tắc 4.16 (số báo giá không sửa số gốc).'), ('Giữ nguyên, anh xem bản vá sau', 'Lệch tiếp tục tồn tại; em đã ghi cảnh báo trong tệp trạng thái.')]),
 dict(id='B3', t='Nơi lưu mã dựng: quy tắc ghi một đằng, thực tế một nẻo', rec=1,
      now='Quy tắc 8.4 bắt lưu mã dựng đạt ở <code>templates/&lt;nhóm&gt;/</code>, nhưng thư mục đó chỉ có mẫu SP từ 06/10; cả 25 mã dựng thật nằm trong <code>work/&lt;việc&gt;/</code> cùng số liệu và báo cáo.',
      why='Từ khi kho lên GitHub, <code>work/</code> không còn bị xoá nhầm như đợt 12/10.',
      opts=[('Đổi quy tắc: catalogue riêng lưu trọn bộ ở work/&lt;việc&gt;/; templates/ chỉ dành cho bộ dựng 3 hãng đã duyệt', 'Khớp thực tế, không phải chép đi chép lại.'), ('Giữ quy tắc, em chép 25 mã dựng sang templates/', 'Hai nơi cùng giữ một mã, dễ lệch.')]),
 dict(id='B4', t='Viết một thư viện dựng trang dùng chung', rec=1,
      now='Mỗi catalogue riêng em viết lại một tệp mã khoảng 11 KB. Hiện có 25 tệp, 286 KB; 20 tệp chép lại cùng một khối mã (gộp phông, bảng, tiêu đề, đánh dấu điểm làm việc).',
      why='Thư viện chung (cột tối REDPUMP, băng đầu trang PEROTAC, dải cờ AQUARIS, bảng, biểu đồ + điểm làm việc, hai thứ tiếng) ước giảm khoảng 60% số chữ phải viết mỗi catalogue, và sửa lỗi một chỗ là đủ.',
      opts=[('Làm, có bộ kiểm thử, dựng lại 3 catalogue gần nhất để so từng trang', 'Tốn một phiên; các catalogue sau nhanh và rẻ hơn.'), ('Không làm', 'Giữ cách chép mã từ việc trước.')]),
 dict(id='B5', t='Dòng điều kiện dưới biểu đồ của các nhóm đã duyệt đang in số cực / tốc độ mặc định', rec=1,
      now='Công cụ in "2 poles (≈ 2900 min⁻¹)" khi số liệu không ghi rõ: MHI và FS/FC inox (nguồn không ghi), WC và IRG (có cả máy 2 cực và 4 cực), KTZ-LH, MIX, CM AQUARIS (2850/2900), CDX và 2CDX (quy tắc ghi "2 poles", không ghi vòng/phút).',
      why='Em chưa đổi cách in cho các nhóm này vì bản đã duyệt đang dùng câu đó; từ hôm nay công cụ chỉ cảnh báo.',
      opts=[('Từ lần dựng hoặc vá tới: in đúng theo nguồn (thêm số cực theo từng model; nguồn không ghi thì bỏ cụm)', 'Trang được vá sẽ có câu điều kiện khác bản cũ một chút, nhưng đúng.'), ('Giữ câu mặc định như bản đã duyệt', 'Máy 4 cực vẫn có thể bị ghi 2 cực 2900 trên trang dựng lại.')]),
 dict(id='B6', t='Đổi kW sang HP không thống nhất giữa các dòng', rec=1,
      now='90 kW = 120 HP (IRG, KTZ-LH) nhưng 125 HP (CM); 132 kW = 176 / 180; 160 kW = 215 / 220; 9,5 kW = 12,5 (GB) / 13 (WC). Ngược lại 125 HP = 90 kW (CM) và 92–93 kW (SP).',
      why='Quy tắc hiện tại là "HP theo nguồn". Catalogue riêng mới (WC 37–132 kW) em đang lấy theo IRG: 120 và 176 HP.',
      opts=[('Giữ bản đã duyệt theo nguồn; catalogue mới dùng một bảng cố định 90 = 120, 132 = 176, 160 = 215 (sát công thức kW ÷ 0,746)', 'Không đụng bản đã duyệt.'), ('Thống nhất toàn bộ về một bảng', 'Phải vá catalogue CM đã duyệt của cả 3 hãng (20 dòng).'), ('Anh cho bảng quy đổi riêng', '')]),
 dict(id='B7', t='Kiểm độc lập bằng AI khác: quy tắc bắt buộc, gần đây em bỏ qua', rec=1,
      now='Quy tắc 8.6 ghi "chưa kiểm = CHƯA XONG". Từ 03/11, các catalogue riêng (TKP, 6SP60 bản 3–4, WC 37–132 kW, GDL) chỉ có kiểm tự động và em tự nhìn PDF; em có ghi rõ trong báo cáo.',
      why='Kiểm độc lập mỗi bản tốn thêm khoảng một nửa công dựng.',
      opts=[('Catalogue riêng ≤ 2 trang: kiểm tự động + nhìn PDF là đủ; ≥ 3 trang hoặc trước khi đưa vào "đã duyệt" thì bắt buộc AI khác kiểm', 'Ghi thành quy tắc để không còn lệch.'), ('Luôn kiểm độc lập mọi bản như quy tắc cũ', 'Chắc hơn, tốn hơn.'), ('Kiểm bù ngay 4 catalogue trên rồi mới áp phương án 1', '')]),
 dict(id='B8', t='Dọn kho: chuyển tệp cũ sang archive/ (không xoá)', rec=1,
      now='<code>claude/</code> có 41 tệp bàn giao cũ, 556 tệp khoá đã nhả, 3 tệp quyết định đã chép thành QĐ 181–183, các báo cáo 09–13/10 (150 KB); ngoài gốc kho có <code>Claude outputs/</code>, <code>_CLAUDE_NHAP_CHO_XOA/</code>, <code>deliverables/</code>; <code>history/</code> có 65 tệp niêm phong (mỗi lần niêm phong sinh 2 tệp, 1 tệp thừa).',
      why='Không ảnh hưởng số liệu; kho gọn, tìm nhanh.',
      opts=[('Làm: giữ 5 bàn giao mới nhất, gom khoá cũ thành 1 bảng, chuyển phần còn lại sang archive/ có danh sách', ''), ('Không dọn', '')]),
 dict(id='B9', t='Sổ tiến độ TIEN DO.md và thư mục state/ đã ngừng được ghi', rec=1,
      now='Sổ dừng ở 16/10 (172 KB), <code>state/</code> dừng ở 23/10; lệnh xem trạng thái chỉ đọc được dòng đến 10/10. Từ 17/10 thực tế theo dõi bằng tệp trạng thái, báo cáo từng việc và lịch sử GitHub.',
      why='Quy tắc vẫn ghi "Claude ghi sổ TIEN DO" nên đang lệch.',
      opts=[('Đóng sổ: ghi một dòng chốt, sửa quy tắc cho khớp cách đang làm', ''), ('Ghi bù từ 17/10 và tiếp tục ghi sổ sau mỗi việc', 'Thêm một nơi phải ghi mỗi lần.')]),
 dict(id='B10', t='5 tệp quy tắc cũ vẫn nằm trong rules/', rec=1,
      now='<code>QUY_TAC_CUNG_HIEN_HANH.md</code> (tên dễ nhầm là đang áp dụng), <code>QUY_TAC_ANH_TRUNG.md</code>, <code>CHOT_PHAM_VI…</code>, <code>QUY_TAC_BA_THUONG_HIEU…</code>, <code>QUY_TAC_DIEN_HONG_XA…json</code> — 46 KB, chỉ để tra lời anh ngày 03–06/10.',
      why='Đã có lỗi C4 vì quy tắc rải nhiều tệp. Chuyển đi phải sửa danh sách niêm phong và 9 chỗ dẫn chiếu.',
      opts=[('Chuyển sang archive/rules_cu_20261013/, sửa dẫn chiếu, niêm phong lại', ''), ('Giữ nguyên', '')]),
 dict(id='B11', t='Giảm lượng chữ AI phải đọc đầu mỗi phiên', rec=1,
      now='Bắt buộc đọc 4 tệp + AGENTS + CLAUDE: khoảng 49 KB. Chuẩn trình bày lặp lại nhiều điều của quy tắc hiện hành (khổ giấy, chữ cấm, câu điều kiện, bảng); skill lặp lại lần nữa.',
      why='Ước bớt 6–8 KB mỗi phiên nếu mỗi điều chỉ ghi một nơi.',
      opts=[('Rút gọn: mỗi điều một nơi, tệp kia chỉ dẫn số mục', 'Em gửi anh bản so sánh trước khi thay.'), ('Giữ nguyên', '')]),
 dict(id='B12', t='Thư mục RPX không có trên GitHub', rec=1,
      now='<code>work/claude_rpx_redpump_20261029/</code> (sách REDPUMP RPX) chỉ nằm trên máy đám mây vì bộ lọc chặn đẩy tài liệu lấy từ sách mẫu của hãng khác; anh đã chọn "chỉ tải PDF". Máy bị thu hồi là mất mã dựng và số liệu.',
      why='Cần mã dựng nếu anh muốn sửa sách này hoặc làm bản PRX / AQX.',
      opts=[('Chỉ đẩy phần em tự viết (mã dựng, tệp số liệu, báo cáo); không đẩy ảnh và phần dịch từ sách mẫu', ''), ('Giữ nguyên, chấp nhận dựng lại từ đầu khi cần', '')]),
 dict(id='B13', t='Các lỗi công cụ còn lại — sửa lớn hơn nên chờ anh đồng ý', rec=1,
      now='(a) Công cụ kiểm trả "thành công" cả khi còn mục CHƯA THỂ XÁC MINH. (b) Chế độ so với bản gốc bỏ sót lỗi mới cùng loại trên cùng trang. (c) Công cụ nhận bản chính chép đè trước, hỏng giữa chừng thì không hoàn lại. (d) Làm tròn lít/phút: 12,5 thành 12. (e) Hai công cụ có hai bộ đọc số liệu đã lệch nhau. (f) Mã không còn dùng. (g) Chưa ghim phiên bản thư viện (máy anh PyMuPDF 1.28, đám mây 2.0).',
      why='Đều đã dựng lại được ca lỗi; chưa gây sai catalogue nào đã giao.',
      opts=[('Sửa hết trong một phiên riêng, có ca kiểm thử cho từng lỗi', ''), ('Chỉ sửa a, b, c (liên quan nghiệm thu)', ''), ('Chưa sửa', '')]),
 dict(id='B14', t='Các số đáng ngờ ở mục C', rec=2,
      now='10 nhóm số liệu trái thông lệ kỹ thuật (bảng mục C). Đều là số theo catalogue nguồn hoặc số anh đưa.',
      why='Em không tự sửa số đã duyệt.',
      opts=[('Giữ nguyên, chỉ ghi nhận', ''), ('Em lập bảng câu hỏi để anh gửi nhà cung cấp xác nhận (model, số đang ghi, vì sao nghi)', ''), ('Anh chỉ định mã nào cần sửa', '')]),
]
C = [
 ('C1', 'Bơm giếng SA 4 inch, mã nhỏ nhất mỗi họ', '4SA6/5 (0,37 kW): 6 m³/h – 22 m; 4SA4/6 (0,37 kW): 4,2 m³/h – 29 m; AQUARIS 4SA3/5 (0,25 kW)', 'Công suất nước bơm ra bằng 86–97% công suất động cơ; bơm giếng 4 inch thường chỉ 55–65%. Có thể kW ghi thấp một nấc.', 'cao'),
 ('C2', 'IRG300-400/110-4 (cả 3 hãng)', '720 m³/h – 50 m, 110 kW', 'Bằng 89% công suất động cơ; hai mã cùng cỡ chỉ 65–67%.', 'cao'),
 ('C3', 'CM 100-250/55; CM 80-125/7.5', '300 m³/h – 59 m; 144 m³/h – 16,5 m', '88% và 86%; các mã cùng cỡ 73–80%.', 'vừa'),
 ('C4', 'WC 37–132 kW (REDPUMP, số anh đưa)', '150WC200-90-132: 200 m³/h – 90 m dùng 37% công suất; 200WC…-90/-110/-132: cột áp max 75–105 m ở 1450 vòng/phút; 200WC350-22-37: 780 m³/h qua DN200', 'Mã 132 kW dư công suất nhiều; cột áp cao vậy ở 4 cực cần cánh rất lớn (ước 470–555 mm) — nên xác nhận số cực; 780 m³/h qua DN200 là 6,9 m/s. Số cực/tốc độ trong catalogue là em suy theo dải.', 'vừa'),
 ('C5', '6SP60-15 (REDPUMP)', 'Công suất trục tính theo đường hiệu suất = 101% công suất động cơ', 'Sát hoặc quá tải nhẹ ở điểm hiệu suất cao nhất.', 'thấp'),
 ('C6', 'DWO037T (cả 3 hãng)', 'Chỉ có 2 điểm: 1 m³/h – 12 m và 6 m³/h – 1 m', 'Không đủ để vẽ đường; 6 mã DWO khác có 4–9 điểm.', 'vừa'),
 ('C7', 'SP AQUARIS', '116 dòng mã 3 pha để trống điện áp', 'Trang nguồn không ghi; khi dựng lại phải điền theo quy tắc ghi điện.', 'vừa'),
 ('C8', 'CDLF (cả 3 hãng)', '57 dòng trống họng hút/xả', 'Trang nguồn cỡ đó không ghi.', 'thấp'),
 ('C9', 'TKP600 (REDPUMP)', '0,4 kW ghi 0,54 HP', 'MIX/4MIX ghi 0,4 kW = 0,55 HP; nên ghi 0,55 cho thống nhất.', 'thấp'),
 ('C10', '50GDL18-15×9 (REDPUMP)', '18 m³/h – 135 m, 11 kW', 'Cần hiệu suất bơm 60–63%; hợp lý nhưng sát, không dư công suất.', 'thấp'),
]
D = [
 ('Mã kiểm 62 PDF đã duyệt so với DANH SACH.txt', '62 / 62 khớp'),
 ('Ảnh trong KHO_ANH so với danh mục', '202 / 202 khớp'),
 ('Hồ sơ hãng bản chữ so với bản máy đọc', 'khớp mọi màu, số, chuỗi'),
 ('Số liệu gốc: 3.243 đường Q–H, 21.714 điểm', '0 đường có cột áp tăng khi lưu lượng tăng; 0 điểm trùng; 0 giá trị âm'),
 ('Thứ tự công suất trong cùng họ (14.920 cặp)', '0 ca mã lớn nằm dưới mã nhỏ trên cả dải'),
 ('PEROTAC so với REDPUMP', 'chỉ khác 1 ô (4SA10/6 tại 1,8 m³/h: 40 và 39 m), đã có ghi chú'),
 ('WC đã duyệt: đường đi qua điểm làm việc ghi trong mã (QĐ 177)', '45 / 45 mã trong 5%'),
 ('Bộ kiểm thử công cụ sau khi sửa', '16/16, 31/31, 4/4, 8/8 đạt (thêm 2 ca mới)'),
 ('Niêm phong quy tắc và công cụ', 'đã niêm phong lại, không tệp nào lệch'),
]
mau = {'cao': 'bad', 'vừa': 'warn', 'thấp': 'mut'}
body = ('<h2 id="a">A. Đã sửa luôn <small>12 nhóm — không cần anh làm gì</small></h2><p class="lead">Chỉ gồm những chỗ em chắc chắn: sai so với quyết định của anh, sai so với tệp thật, hoặc lỗi công cụ đã dựng lại được.</p>'
        + table(['#', 'Vấn đề', 'Hiện trạng tìm thấy', 'Đã làm'], [(i, f'<b>{t}</b>', n, d) for i, t, n, d in A])
        + '<h2 id="b">B. Đề xuất chờ anh duyệt <small>14 mục — chọn số rồi bấm "Chép câu trả lời" ở cuối trang</small></h2><p class="lead">Mỗi mục: hiện đang thế nào, vì sao cần quyết, các lựa chọn và hệ quả. Mục có nhãn xanh là phương án em đề xuất.</p>'
        + ''.join(card(x) for x in B)
        + '<h2 id="c">C. Số liệu trái thông lệ kỹ thuật <small>10 nhóm — em không sửa, cần anh hoặc nhà cung cấp xác nhận (mục B14)</small></h2><p class="lead">Cách đo: công suất nước bơm ra = 9,81 × lưu lượng (m³/h) ÷ 3600 × cột áp (m), so với công suất động cơ P2. Tỉ lệ trên 85% là đáng ngờ vì bơm thật hiếm khi đạt. Phần "vì sao" là nhận định chuyên môn, chưa đối chiếu catalogue nhà máy.</p>'
        + table(['#', 'Dòng / mã', 'Số đang ghi', 'Vì sao đáng ngờ', 'Mức'], [(i, f'<b>{t}</b>', n, w, f'<span class="tag {mau[m]}">{m}</span>') for i, t, n, w, m in C])
        + '<h2 id="d">D. Đã kiểm, không có lỗi</h2><p class="lead">Số đo ngày 14/11/2026 trên kho GitHub nhánh claude/bold-ritchie-u7uzep.</p>'
        + table(['Phép kiểm', 'Kết quả'], D)
        + '<h2 id="e">E. Cách em rà</h2><ul class="tight"><li>Em đọc toàn bộ quy tắc, hồ sơ hãng, chuẩn trình bày, nhật ký 185 quyết định, sổ lỗi, tệp trạng thái, AGENTS.md, CLAUDE.md, skill (bản trong kho và bản trên tài khoản).</li><li>Một AI khác soát độc lập 14 tệp mã công cụ: chạy các bộ kiểm thử, dựng lại từng lỗi (31 phát hiện, em đã sửa 12, còn lại ở B13).</li><li>Một AI khác soát độc lập 21 tệp số liệu gốc và 5 tệp số liệu catalogue riêng bằng script (mục C, D).</li><li>Chưa làm: chạy lại công cụ kiểm trên cả 62 PDF đã duyệt (đã có báo cáo 13/10); so từng trang PDF với số liệu gốc.</li></ul><p class="note">Nhật ký: QĐ 184 trong rules/QUYET_DINH_ANH.md. Danh sách tệp đổi: lịch sử GitHub ngày 14/11/2026.</p>')
d = dict(kicker='Dự án Sửa catalogue · PEROTAC · REDPUMP · AQUARIS · 14/11/2026', title='Rà soát toàn bộ dự án: đã sửa 12 nhóm lỗi, còn 14 đề xuất chờ anh duyệt',
         sub='Lỗi, chỗ thiếu nhất quán, chỗ lãng phí và số liệu đáng ngờ trong quy tắc, skill, công cụ, số liệu và kho tệp. Việc anh cần làm ngay: mục B1 (tải lại skill) và B2 (số liệu CM AQUARIS).',
         tiles=[('ok', '12', 'nhóm lỗi đã sửa'), ('warn', '14', 'đề xuất chờ anh chọn'), ('bad', '10', 'nhóm số liệu cần xác nhận'), ('ok', '59/59', 'ca kiểm thử công cụ đạt'), ('', '338', 'tệp rác gỡ khỏi GitHub')],
         nav=[('a', 'A. Đã sửa'), ('b', 'B. Chờ duyệt'), ('c', 'C. Số liệu đáng ngờ'), ('d', 'D. Đã kiểm'), ('e', 'E. Cách rà')], body=body)
open(sys.argv[1], 'w', encoding='utf-8').write(build(d)); print('ok', len(build(d)))
