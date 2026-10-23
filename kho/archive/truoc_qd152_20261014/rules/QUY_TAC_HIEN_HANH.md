# QUY TẮC HIỆN HÀNH — dự án Sửa catalogue

Phiên bản 2026.10.13 (gộp ngày 13/10/2026 theo QĐ 147–149). Đây là tệp quy tắc DUY NHẤT đang áp dụng.
Thứ tự đọc đầu phiên: **tệp này → rules/HO_SO_HANG.md → rules/CHUAN_TRINH_BAY.md → claude/TRANG_THAI_CLAUDE.md**.
Ưu tiên khi lệch: lời anh Trung mới nhất (đúng phạm vi anh nói) > tệp này > mọi tệp cũ (rules/QUY_TAC_CUNG_HIEN_HANH.md, rules/QUY_TAC_ANH_TRUNG.md, procedures/, knowledge/, archive/).

Ký hiệu nguồn: **QĐ N** = rules/QUYET_DINH_ANH.md mục N (nhật ký nguyên văn). QTC = rules/QUY_TAC_CUNG_HIEN_HANH.md; PVI = rules/CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md (số = điều); BTH = rules/QUY_TAC_BA_THUONG_HIEU_20261006.md; QAT = rules/QUY_TAC_ANH_TRUNG.md; DHX = rules/QUY_TAC_DIEN_HONG_XA_SA_20261006.json (bản chữ ở archive/rules_cu_20261013/); LOGO = archive/rules_cu_20261013/BO_SUNG_LOGO_BANG_QH_CONG_SUAT_20261006.md; LAB = claude/LOI_ANH_BAO.md. Các tệp này giữ lời anh ngày 03–06/10, chỉ tra khi cần, không đọc đầu phiên.

## 1. Phạm vi hãng và nhóm

- 62 PDF trong CATALOG SUA/CATALOGUE DA DUYET là bản anh đã duyệt: giữ nguyên, không làm lại. Lỗi thấy trên bản cũ chỉ là bài học; chỉ sửa khi anh ra lệnh sửa đúng catalogue đó (QĐ 147, 149).
- Mỗi hãng một PDF riêng; tiếng Anh, không tiếng Việt; chỉ 50 Hz (PVI 1, 4, 6). CM AQUARIS giữ 2 dòng tiếng Ý của nguồn (QĐ 103).

| Nhóm | Hãng làm | Nguồn |
|---|---|---|
| CM, 3M, WC, SS, SP, SA, IRG, GB, KTZ-LH, CDLF, CDX, DWO, MIX, 4MIX, 2CDX, MHI / IVT-MHI | cả 3 | PVI; QĐ 23, 31, 80, 107, 110, 149 |
| FS / FC (bản gang và bản inox) | FS = AQUARIS; FC = PEROTAC, REDPUMP | QĐ 126, 127, 149 |
| Máy thổi khí Root (chỉ dòng RL, bỏ RW) | PEROTAC, REDPUMP | QĐ 131, 133 |
| Bơm định lượng JLM-JBB | chỉ AQUARIS | QĐ 22 |
| Đĩa phân phối khí DN270 / DN128 | PEROTAC, REDPUMP | QĐ 77 |
| SL | không làm; nguồn SL dùng làm SA REDPUMP | QĐ 30 |
| QXN40-60 | PEROTAC, AQUARIS (đang chờ anh duyệt) | QĐ 112 |

- Hãng chưa có nguồn riêng: dùng số PEROTAC đã kiểm; có nguồn riêng thì giữ nguồn riêng (PVI "Chốt tiếp"). Mã chung nhưng số khác giữa hãng (SA, SP): giữ số riêng từng hãng, chỉ thêm mã còn thiếu (QĐ 127). KTZ AQUARIS dùng số + ảnh PEROTAC (QĐ 31).
- Mọi việc phải đối chiếu đủ 3 hãng; anh giao thiếu hãng (ngoài bảng trên) thì hỏi lại anh (BTH).

## 2. Quy ước mã

| Nhóm | Quy ước | Nguồn |
|---|---|---|
| IRG | IRG<cỡ>-<cánh>/<kW>, vd IRG40-100/0.75; kW nguyên ghi "/3"; bơm 4 cực thêm "-4" (IRG80-160/11-4); chỉ giữ họ (I), bỏ A/B/C; cỡ họng không có (I) giữ họ thường; hai model cùng cỡ cánh cùng kW: giữ model Q/H lớn hơn | QĐ 47, 56, 68, 99 |
| CDX | số theo catalogue Ebara; viết liền CDX90/10 (3 pha), CDXM90/10 (1 pha); mọi model đủ 1 và 3 pha; ghi "2 poles", không ghi vòng/phút; CDX120/15, CDX200/15 = 1.1 kW (có bản CDXM); CDX200/25 = 2.2 kW | QĐ 45, 58, 122, 123, 130 |
| 2CDX | 2CDX… 3 pha, 2CDXM… 1 pha (có 120/30, 120/40, 200/30, 200/40); 2CDX200/50 chỉ 3 pha; mọi mã 110 °C; không ghi nhãn H3/H4 | QĐ 108 |
| DWO | số theo Ebara (bộ min/max DWO cũ trong QTC bỏ); …T = 3 pha, …M = 1 pha; có DWO037T/M, DWO100T/M, DWO300M, DWO400M; DWO550T = 4 kW / 5.5 HP, 3 pha, Qmax 72, Hmax 19, họng như DWO400T; bỏ DWO500; DWO037/100 hút–xả 1¼"; giữ cả bản 1 trang và 2 trang | QĐ 46, 57, 64, 105 |
| 3M | số sau "/" là kW có dấu chấm: /1.1, /1.5, /2.2, /3.0, /4.0, /5.5, /7.5…; bỏ 3M 65-160/15.0 | QĐ 28, 94 |
| WC | 3 pha WC, 1 pha WCD (65WC25-10-1.5 / 65WCD25-10-1.5); 9.5 kW ghi 13 HP | QĐ 10, 12 |
| SP | 1 pha có chữ M (4SPM…), 3 pha không M; bỏ dải 4SP2 và 3SP ở cả 3 hãng; bỏ 4SP8-13, 8SP120-9, 10SP125-9, 10SP135-9; dải 6SP30 REDPUMP là bản sửa riêng, không áp vào catalogue SP | QTC; QĐ 79, 134, 140, 142 |
| SA | AQUARIS ghi SA mọi cỡ; PEROTAC giữ tên SS ở dải nguồn ghi SS, REDPUMP ghi SA; bỏ 4SA2 cả 3 hãng; AQUARIS bỏ 4SA8/5 | QĐ 92, 129, 130 |
| CDLF | 3 pha CDLF<dải>-<tầng>T, 1 pha CDLFM<dải>-<tầng> (vd CDLF4-2T / CDLFM4-2) | QĐ 96 |
| GB | 3 pha có "S" (GB-2200S), 1 pha không "S"; GB-9500S (không phải 9000S) = 9.5 kW / 12.5 HP | PVI 10; QĐ 90, 114 |
| FC | PEROTAC, REDPUMP đổi FS → FC (FS 75/40T → FC 75/40T), còn lại giữ nguyên | QĐ 126, 127 |
| CM | ghi CM 32-125/0.75 (không 0.7); AQUARIS không có CM 32-125/0.7 và /1.1 cũ | QĐ 104, 114 |
| MHI | tiêu đề "IVT-MHI Series"; bỏ chữ MHI-EH / MHI-QH | QĐ 110 |
| MIX, 4MIX | mã MIX chung 3 hãng; 5 model 4 cực; MIX-0.4 ghi 0.55 HP; MIX-1.1: Qmax 240 m³/h, tốc độ dòng 2.8 m/s; 4MIX = toàn thân inox, số như MIX | QĐ 23, 24, 80 |
| Đĩa phân phối khí | DN270 = đĩa 10 inch, Ø 270 mm; DN128 = đĩa 5 inch, Ø 128 mm | QĐ 77 |
| QXN | QXN40-60 dùng số QXN40/3-15; AQUARIS ghi 11 kW / 15 HP | QĐ 112 |

Danh sách đổi mã đầy đủ ngày 09/10 (dùng cho dự án web): claude/THAY_DOI_MA_20261009.csv.

## 3. Điện, pha, tốc độ, họng, vật liệu

- Ghi điện: 1 pha = "1~ 220–240 V 50 Hz"; 3 pha = "3~ 380–415 V 50 Hz" (DHX). Không ghi 60 Hz.
- ≤ 3 kW mới có thể có bản 1 pha; > 3 kW chỉ 3 pha; không tự tạo bản 1 pha khi chưa có lệnh (DHX).
- Nguồn không ghi pha theo model: ≤ 3 kW có cả 1 và 3 pha — áp IRG, CDLF, DWO, SA AQUARIS. Chỉ 3 pha: CM, 3M, giếng 6 inch, KTZ, 4 mã WC thêm 06/10 (QĐ 9, 36; PVI 8).
- Có model 1 pha thì bắt buộc có model 3 pha tương ứng (QTC).
- SP: 2 / 2.5 / 3 inch có 1 pha; 4 inch ≤ 2.2 kW có 1 pha; 6 inch không 1 pha (QĐ 130 câu 15); 5 inch chỉ 3 pha (QĐ 136 — điều phối tự chọn, chờ anh xem).
- SA PEROTAC, REDPUMP: mã 3 kW ở dải 4SA6, 4SA10 có thêm bản 1 pha (QĐ 140).
- Tốc độ ghi theo nguồn từng sản phẩm (2950 / 2900 / 2850…), dạng "n ≈ … min⁻¹"; không áp một số cho mọi bơm (PVI 7; QĐ 114).
- Họng xả bơm giếng: thân 6" = 3"; thân 5" = 2½"; thân 4" dải 4/6/8/10 = 1½", dải 12/16 = 2" (PVI 9; DHX). Dải 4" khác: giữ nguồn.
- HP theo nguồn. CM AQUARIS: IP55, chất lỏng tối đa 120 °C, cánh bơm ghi như PEROTAC (QĐ 66, 102). Trục CM: PEROTAC và AQUARIS AISI 316, REDPUMP AISI 304 (LAB 3; QĐ 114).

## 4. Số liệu

1. Một model: lưu lượng Q tăng thì cột áp H giảm (QAT, lời anh 03/10).
2. Đường Q–H cong đều: tối đa 1 điểm uốn, không đoạn phẳng rồi gãy, không móc đầu/cuối (tools/kiem_catalogue.py mục 4; tools/ve_duong_cong.py chặn khi số SỬA tạo gợn mới, gợn có sẵn trong số đã duyệt chỉ cảnh báo); lệch đường so với bảng ≤ 5% tại từng điểm; vượt 5% thì được sửa H trung gian, ghi cũ → mới (QTC "Đường cong đều").
3. Giữ Qmin, Qmax, Hmin, Hmax và điểm làm việc đã khoá; khoá mâu thuẫn thì báo anh, không tự phá (QAT; QTC).
4. Thứ tự công suất: cùng dải / cùng họng, model công suất lớn hơn phải cho Q và H lớn hơn, đường không cắt nhau (QĐ 20). Ngoại lệ anh chốt: DWO037, DWO100 so với DWO150 (QĐ 63); 14 cặp KTZ-LH giữ theo nguồn (QĐ 95); 4 cặp GB giữ theo bảng (QĐ 90). Hai model cùng kW cùng dải bỏ model nhỏ hơn: CHỈ đã chốt cho IRG (QĐ 56) và SA (QĐ 92); nhóm khác (vd SP còn 4SP3-52/-60 cùng 4 kW) hỏi anh trước.
5. H có số lẻ theo nguồn thì giữ (QĐ 27). Q giữ tối đa 1 chữ số lẻ theo nguồn (PVI "Chốt tiếp"). Dùng dấu chấm thập phân.
6. Dòng điện A: giữ cột A ở mọi catalogue; mã thiếu số thì điền số suy ra từ các mã cùng catalogue, cùng pha (đường thẳng I = a + b·P2, làm tròn 0,1 A, tăng theo kW), ghi "số suy ra" (QĐ 73).
7. Ô thiếu: không điền 0, không đoán; ghi CHƯA THỂ XÁC MINH và hỏi anh theo từng nhóm (QĐ 6). Dấu "–" chỉ ở đầu/cuối dãy (ngoài dải chạy của bơm) hoặc ở cột model 1 pha; ô trống nằm giữa dãy H thì điền theo đường của chính model, ghi "số dựng" (LAB 4). Cấm ô "*" (QĐ 149).
8. Mã anh thêm chỉ có max/min: mốc H giữa điền theo đường mã lân cận, ghi suy ra (QĐ 127). Mã thêm vào giữa dải: nhỏ hơn mã trên một cấp, lớn hơn mã dưới một cấp (QĐ 130).
9. WC: cột áp tại Qmax theo bậc công suất trong cùng cỡ họng — nhỏ nhất 1 m, mỗi nấc công suất +1 m (QĐ 19).
10. Mọi số dựng, số suy ra, số sửa theo quyền anh: ghi cũ → mới và loại số trong báo cáo (QĐ 29, 33, 89, 149).
11. Không tự nội suy hiệu suất η hay NPSH khi nguồn không có (QĐ 130, 149).
12. Bảng và đường sinh từ MỘT tệp số liệu DU_LIEU/<nhóm>.xlsx; số của 3 hãng giống nhau từng ký tự, trừ chỗ anh cho khác (QĐ 149).
13. Chính tả tiếng Anh sai của nguồn: sửa; câu sai ngữ pháp: viết lại giữ nghĩa, không thêm ý, không thêm số (QĐ 100, 102).

## 5. Nội dung cấm và bắt buộc

- CẤM: dòng bảo hành (QĐ 34); cân nặng/khối lượng (QĐ 114 — GIỮ bảng kích thước và họng hút/xả; quy tắc bỏ D×R×C chỉ áp cho web); 60 Hz; tiếng Việt; ô "*"; tên hãng linh kiện NSK / NTN / T.I. (vật liệu MIX, 4MIX ghi "High quality") (QĐ 114).
- BẮT BUỘC: "50 Hz" ở trang đầu mọi sản phẩm có động cơ; dưới biểu đồ có khối điều kiện + "Typical values, not guaranteed"; chỉ ghi "ISO 9906:2012 Grade 3B" khi nhà cung cấp xác nhận (QĐ 149).
- Bìa, chân trang: giữ thông tin bản cũ hoặc chỉ tên hãng; không tự thêm địa chỉ, điện thoại, website (QĐ 7).
- Logo nguyên bản của 3 hãng; logo REDPUMP giữ chữ "Italy Standard"; logo không đặt trong ô nền khác màu (QĐ 24, 53; LOGO). Không chép logo, màu, bố cục của hãng bơm thật (QĐ 149).
- Dựng đầy đủ: có trang bìa + chi tiết cấu tạo – vật liệu theo nguồn/mẫu anh đưa; nguồn không có thì hỏi anh (QĐ 83). IRG có hình cắt đánh số 1–9 + bảng vật liệu (QĐ 82).
- Riêng từng nhóm: PEROTAC WC có trang cấu tạo + tính năng (phớt SiC, trục AISI 304, không cảm biến), REDPUMP/AQUARIS không có (QĐ 74–76); SS ghi "Special mechanical seal available on request." và "Impeller type: open" (QĐ 104, 114); KTZ ghi "up to 15 kW" (QĐ 103); FS 300/80 và FS khổ ngang bỏ họng xả và cỡ ren (QĐ 49, 61).

## 6. Biểu đồ và giao diện 3 hãng

- Mọi nhóm mặc định có biểu đồ Q–H; thiếu bảng số thì tự vẽ từ thông số có (Hmax tại Q = 0, điểm định mức theo tên, Qmax), ghi điểm suy ra và hỏi anh (QĐ 145). NGOẠI LỆ: IRG KHÔNG vẽ đường (QĐ 82; anh chọn 3.2 ở QĐ 149).
- Thiết bị không phải bơm ly tâm (GB, Root RL, máy khuấy, định lượng, đĩa phân phối khí): lấy bản đã duyệt làm mẫu (QĐ 149).
- 3 hãng cùng dòng khác nhau ≥ 5/6 trục: màu, phông, bìa, bảng, biểu đồ, đồ họa phụ. Cấm dùng chung khuôn rồi chỉ đổi màu, lật trái-phải, đảo khối (QĐ 13, 14, 149). Giá trị từng hãng: rules/HO_SO_HANG.md.
- AQUARIS: mỗi model một màu trong cùng biểu đồ (QĐ 54); PEROTAC, REDPUMP một tông.
- Khổ: chỉ A4 — AQUARIS dọc 595×842, PEROTAC và REDPUMP ngang 842×595 (QĐ 149).
- Chữ thân ≥ 9 pt; số trong bảng, nhãn trục, nhãn đường ≥ 7 pt (nên 8); không đủ chỗ thì tách trang, không thu nhỏ chữ (QĐ 149).
- Thiết kế đơn giản, dễ đọc, không lòe loẹt (QTC "Thiết kế dễ nhìn"). Số đo chuẩn: rules/CHUAN_TRINH_BAY.md.

## 7. Ảnh

- Ảnh anh gửi là ẢNH MẪU: tách nền, xoá logo/chữ/tem lạ, căn đẹp, đủ nguyên thân bơm, không lẹm (QĐ 55, 145, 146).
- Được vẽ lại một phần hoặc tự tạo ảnh mới dựa trên ảnh mẫu, giữ đúng cấu tạo bơm; ảnh tự tạo/vẽ lại phải GỬI ANH DUYỆT trước khi dùng (QĐ 146, 149).
- Một AI khác so ảnh gốc với ảnh đã làm, phóng từng vùng, xác nhận không lẹm rồi mới đưa vào catalogue (QĐ 146).
- Ảnh REDPUMP dùng chung PEROTAC ở các nhóm anh đã cho (QĐ 104); REDPUMP SS giữ ảnh cũ (QĐ 118); SS PEROTAC 3 ảnh có phao, không chữ dưới ảnh (QĐ 116); ảnh dải SP mới dùng ảnh cùng cỡ của hãng kia (QĐ 127).
- Chuẩn ảnh (độ nét, nền, bóng, soi viền) và kho ảnh KHO_ANH/: rules/CHUAN_TRINH_BAY.md mục 1.

## 8. Quy trình làm việc

1. Đầu phiên: đọc 4 tệp ở đầu; tra lỗi cũ ở rules/LOI_DA_GAP.md, việc chờ anh ở claude/VIEC_CHO_ANH.md.
2. Khoá việc: `claude/khoa_viec.py xem`, rồi `nhan <VIỆC> <PHIÊN> "<phạm vi>"`, xong thì `nha`. Việc phiên khác đang giữ: không đọc-sửa, không ghi, không chiếm khoá. Ghi bản chính gốc trong BẢN MỚI 03-10: thêm `cat.py claim` (QĐ 15).
3. Cách làm PDF: DỰNG MỚI là chính (DU_LIEU + HO_SO_HANG + mã dựng ở templates/<nhóm>/); catfix chỉ dùng khi sửa tại chỗ bản gốc; 43/43 bài kiểm (claude/dau_phien.sh test) chỉ bắt buộc khi dùng catfix (QĐ 149).
4. Mã dựng đạt lưu ở templates/<nhóm>/, không để trong work/ (QĐ 149).
4b. Sửa catalogue đã duyệt: mặc định VÁ đúng chỗ, giữ khổ/bố cục bản đã duyệt, kiểm bằng `tools/kiem_catalogue.py --goc` (chỉ tính lỗi mới); dựng lại cả catalogue theo chuẩn mới chỉ khi anh chọn — đang chờ anh chốt (claude/VIEC_CHO_ANH.md).
5. Mỗi nhóm làm mẫu, anh duyệt rồi mới dựng cả bộ (QĐ 5). Tách phần độc lập cho nhiều AI chạy song song, mỗi AI một khoá, một thư mục, một tệp ra; việc cơ học dùng model rẻ, việc cần phán đoán dùng model mạnh (QĐ 16).
6. Nghiệm thu: AI khác kiểm độc lập; chưa kiểm = CHƯA XONG, không kiểm được = CHƯA THỂ XÁC MINH (QĐ 17). Chỉ kiểm phần vừa làm và phần bị ảnh hưởng (QĐ 18). Định nghĩa hoàn thành: rules/CHUAN_TRINH_BAY.md mục 8.
7. Anh báo lỗi: chỉ ghi vào claude/LOI_ANH_BAO.md (nguyên văn, đánh số); anh bảo "sửa" mới sửa, sửa một lượt (QĐ 106).
8. Hỏi anh: gom câu hỏi một lần, gộp cả câu cũ chưa trả lời (QĐ 92); lựa chọn đánh số; nêu dẫn chứng cụ thể (model, trang, số cũ/mới); không hỏi lại điều đã chốt; thuật ngữ tiếng Anh phải dịch.
9. Bản anh duyệt: chép đúng byte vào CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/<HÃNG> - <tên nhóm>.pdf và cập nhật DANH SACH.txt; bản bị thay sao lưu sang history/<UTC>_<tên>/ — làm cả bước bằng tools/nhan_ban_chinh.py; không xoá (QĐ 72, 147).
10. PDF chỉ để đăng web và gửi Zalo: RGB, không kiểm bản in (QĐ 2, 149).
11. Nháp để ngoài kho; mỗi phiên một việc; cuối phiên ghi đè mục 4 của claude/TRANG_THAI_CLAUDE.md và ghi bàn giao ngắn.
12. Không xoá tệp: tệp bỏ thì `mv` sang archive/ và ghi archive/DA_CHUYEN_<ngày>.csv. Không bao giờ dọn rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/ (QĐ 149; rules/LOI_DA_GAP.md).

## 9. Cách cập nhật quy tắc về sau

1. Anh ra quyết định mới → chép nguyên văn vào cuối rules/QUYET_DINH_ANH.md (số tiếp theo, ngày giờ, phiên).
2. Cùng lượt sửa điều liên quan trong tệp này (ghi số QĐ mới) và đánh "(đã thay bởi mục N)" vào mục cũ trong nhật ký; sửa HO_SO_HANG (.md và .json cùng lúc) hoặc CHUAN_TRINH_BAY nếu chạm tới.
3. Nếu là lỗi: thêm một dòng vào rules/LOI_DA_GAP.md và phép kiểm vào tools/kiem_catalogue.py.
4. Tăng số phiên bản ở dòng đầu tệp này; niêm phong lại bằng `tools/niem_phong.py "<lý do>"` (rồi `claude/cat.py health` phải "changed": []); báo anh 1 dòng.
5. Không bao giờ xoá rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/; nháp để ngoài kho.
