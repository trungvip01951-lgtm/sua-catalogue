# Phương án hoàn thiện dự án Sửa catalogue — 13/10/2026 (CHỜ ANH DUYỆT)

Căn cứ: rà 13/10/2026 (chỉ đọc) toàn bộ quy tắc trong kho + đo tự động 62 PDF trong CATALOGUE DA DUYET + xem bằng mắt 5 nhóm (WC, SP, CM, MIX, CDX). Chưa xem bằng mắt: 2CDX, FS/FC, KTZ, SA, 3M, MHI, CDLF, IRG, GB, RL, DN270, DWO, SS, 4MIX, JLM.

## 1. Hiện trạng
| Mặt | Kết quả | Bằng chứng |
|---|---|---|
| Số lượng | 62 PDF đủ phạm vi, SHA khớp DANH SACH 62/62 | đo |
| Chữ cấm | warranty 0/62, 60 Hz 0/62, phông nhúng 62/62 | đo |
| 3 hãng khác nhau | WC, CM, MIX đạt; SP PEROTAC–REDPUMP chỉ lật trái-phải; CDX biểu đồ P–R giống hệt; biểu đồ WC 3 hãng cùng khuôn | mắt |
| Ảnh | MIX tốt (310–345 ppi). WC, SP, CDX, GB, CDLF có ảnh mờ (83–136 ppi), viền răng cưa, nền chưa tách, 1 ảnh dùng cho 3 cỡ SP | đo + mắt |
| Biểu đồ | nhãn không đè (soi 4 trang); AQUARIS CDX tr2 đường CDX70/07 có móc gãy cuối đường | mắt |
| Tệp | SP AQUARIS 14,7 MB, SP REDPUMP 14,2 MB (phông nhúng lặp, ảnh trùng); chữ 4,5–6 pt ở SP P/R, RL P/R; khổ trang lẻ, khác nhau | đo |
| Quy tắc | mâu thuẫn ~8 điểm, lỗi thời nhiều chỗ, ~105 quyết định chỉ nằm trong nhật ký 60 KB; TRANG_THAI 53 KB | đọc |
| Thiếu | hồ sơ thiết kế từng hãng, chuẩn ảnh có số, chuẩn biểu đồ, mẫu lệnh, kiểm tự động, mẫu dựng cho 18/19 nhóm | đọc |
| Mã dựng | mã dựng các nhóm nằm trong work/ đã bị xoá đợt dọn 12/10 (Claude đánh giá sai là nháp) → lần sửa sau phải dựng lại từ PDF | đo |

## 2. Lỗi cụ thể trên catalogue đã duyệt
1. PEROTAC WC tr2, REDPUMP WC tr1: ảnh bơm + ống dẫn mờ, viền răng cưa, đế bị cắt, vệt trắng.
2. REDPUMP WC tr1: nền nước bắn mờ, vỡ hạt.
3. AQUARIS WC tr1: ảnh còn phông xám, đế trưng bày, cuộn cáp.
4. AQUARIS SP tr1: 1 ảnh dùng cho 6"/8"/10"; ảnh 4"/5" lệch tông, không bóng, viền xanh mép trái.
5. SP PEROTAC vs REDPUMP: cùng biểu đồ, cùng bảng, chỉ lật trái-phải, đổi màu.
6. CDX PEROTAC vs REDPUMP tr2: biểu đồ giống hệt; AQUARIS CDX tr2 đường ② có móc gãy, các đường gần thẳng.
7. Ảnh/bản vẽ < 150 ppi: GB cả 3 hãng (83–89), CDLF PEROTAC (92), RL tr1 P/R (85–91), CDX tr1 + bản vẽ nổ (97–124), SA AQUARIS (136).
8. Khoảng trống lớn: REDPUMP CM tr1, REDPUMP CDX tr1, PEROTAC CM tr1, AQUARIS/PEROTAC CDX tr1, AQUARIS WC tr1.
9. Chữ < 6 pt: SP PEROTAC ~8.000 ký tự, SP REDPUMP ~6.600, RL P/R ~900 (nhỏ nhất 4,5 pt).
10. Thiếu "50 Hz": FS/FC inox 3 hãng, Root RL P/R.
11. Root RL P/R còn khối lượng "Weight … kg" (QD 102(6) bỏ cân nặng mọi catalogue).
12. REDPUMP SP: ảnh 1732×1240 đặt 2 lần chồng nhau, tràn mép tr1/10/16/19.

## 3. Quy tắc bổ sung
### 3.1 Một tệp quy tắc hiện hành duy nhất
rules/QUY_TAC_HIEN_HANH.md (≤20 KB, chia theo chủ đề: phạm vi hãng, mã, điện, số liệu, biểu đồ, ảnh, trình bày, tệp, nghiệm thu). QUYET_DINH chỉ là nhật ký; mỗi quyết định mới phải cập nhật luôn tệp hiện hành. Sửa/đánh dấu lỗi thời: QUY_TAC_ANH_TRUNG (Desktop), START_HERE/manifest (python Codex), DUONG_DAN_MOI (_CHO_XOA, history), AGENTS (catfix-only, DWO cũ), CHOT_PHAM_VI + QUY_TAC_BA_THUONG_HIEU (FS/Roots/KTZ), TRANG_THAI (bảo hành), LOI_VA_CACH_TRANH (dòng A), CAU_HOI/THONG_KE (lỗi thời), DANH SACH.txt (30 dòng lặp, _BAN CU).
### 3.2 Hồ sơ thiết kế từng hãng (rules/HO_SO_HANG.md)
| | AQUARIS | PEROTAC | REDPUMP |
|---|---|---|---|
| Khổ | A4 dọc 595×842 | A4 ngang 842×595 | A4 ngang 842×595 |
| Màu chính | xanh rêu #0D6159, cờ Ý #009246/#FFFFFF/#CE2B37, nền #F0F7F5 | xanh than #13334D, đường #1A669E, nền #EDF5FA | than #2B2E33, đỏ đô #A31A1F, nền #F7F2F0 |
| Phông | Lato | Liberation Sans | phông khác P (vd Roboto Condensed — bản quyền mở) |
| Bố cục | dải cờ Ý, ảnh trên trái, ô số liệu nổi bật | băng đầu trang xanh nhạt, logo trái, 3 cột | cột tối bên trái 28–30% bề ngang |
| Biểu đồ | nhiều màu, số khoanh tròn + chú giải | 1 tông xanh, nhãn tên đầu trái đường, trục H trái | đỏ/xám, nhãn cuối phải đường, trục H phải, tô nhạt vùng làm việc |
| Bảng | model theo cột | model theo dòng, kẻ dòng mảnh | model theo dòng, sọc xám xen kẽ, đầu bảng tối |
| Ảnh | nền trắng, bóng mềm | nền trắng, không bóng | nền trắng/xám rất nhạt, bóng đổ dưới đế |
Cấm: dùng chung một khuôn biểu đồ/bảng rồi chỉ đổi màu, lật trái-phải, đảo vị trí khối.
### 3.3 Chuẩn ảnh sản phẩm
- Nền trắng #FFFFFF hoặc trong suốt; cấm nền trang trí (nước bắn, phông xám, đế trưng bày, cáp).
- ≥200 ppi ở kích thước hiển thị (ảnh lớn trang bìa ≥300 ppi); bản vẽ cấu tạo/nổ: vector hoặc ≥200 ppi.
- Sản phẩm chiếm ~80% cạnh dài ô ảnh, căn giữa; cùng góc nhìn, cùng tông màu, cùng kiểu bóng trong một catalogue.
- Mỗi cỡ/model một ảnh riêng; dùng chung ảnh cho cỡ khác phải được anh cho phép.
- Soi viền 300 dpi: không viền trắng/xanh, răng cưa, sót nền, sót logo/chữ hãng khác, không cắt cụt đế/ống.
- Ảnh anh gửi: xoá logo, chữ, tách nền, cân màu. Ảnh vẽ lại/tự tạo: đưa anh duyệt trước khi dùng.
- KHO_ANH/<nhóm>/<model>_<hãng>.png: mỗi ảnh đã duyệt lưu một lần, ghi trạng thái; catalogue sau lấy từ kho, không cắt lại.
### 3.4 Chuẩn biểu đồ
Nội suy trơn đơn điệu (PCHIP) qua điểm dữ liệu; Q tăng H giảm; lệch ≤5%; không móc đầu/cuối, không gợn; giữ Qmin/Qmax/Hmin/Hmax, điểm làm việc; trục Q m³/h (+ l/min), H m; lưới nhạt; nhãn không đè; mỗi model một đường; đường đến hết dải Q của bảng.
### 3.5 Chuẩn chữ, bố cục
Chữ thường ≥7 pt, bảng ≥6 pt, nhãn đường ≥6,5 pt (không đủ chỗ thì tách trang); khoảng trống liền ≤10% chiều cao trang; lề ≥10 mm; ghi "50 Hz" cho mọi sản phẩm có động cơ; không bảo hành, không cân nặng, không kích thước D×R×C (giữ họng hút/xả), không tiếng Việt.
### 3.6 Chuẩn tệp
≤5 MB/tệp; RGB; phông nhúng 1 lần dạng rút gọn; lưu garbage=4 + deflate, gộp ảnh trùng; tên "HÃNG - Tên dòng.pdf"; khổ theo hồ sơ hãng.
### 3.7 Bỏ/đổi
Bỏ kiểm "bản in" (PDF không in); bỏ mốc 137/149; 43/43 chỉ bắt buộc khi sửa tại chỗ bằng catfix — dựng mới thì thay bằng kiem_catalogue.py; một hệ khoá (khoa_viec.py); mã dựng đạt phải lưu vào templates/<nhóm>/ (không để trong work/).

## 4. Công cụ tự động
1. kiem_catalogue.py: chữ cấm, điện/pha, bảng (Q↑H↓, ô "–", thứ tự công suất), đường so bảng ≤5% + móc, nhãn đè, ppi ảnh, cỡ chữ, khổ, dung lượng, khoảng trống, độ giống giữa 3 hãng, SHA → phiếu ĐẠT/CHƯA ĐẠT.
2. Thư viện dựng: DU_LIEU/<nhóm>.xlsx (một nguồn số liệu) + HO_SO_HANG + mã dựng chung → 1 lệnh ra 3 PDF.
3. nhan_ban_chinh.py: sao lưu, chép, SHA, DANH SACH, TIEN DO, TRANG_THAI, gói Drive NV trong 1 lệnh.
4. cap_nhat_goi_drive.py.

## 5. Mẫu lệnh cho người không biết gì
- Sửa: "Sửa catalogue <tên dòng> hãng <AQUARIS/PEROTAC/REDPUMP/cả 3>: <model> <thông số> <cũ> → <mới>" (+ ảnh đính kèm nếu đổi ảnh).
- Tạo mới: "Tạo catalogue <tên dòng> cho <hãng>. Nguồn: <tệp đính kèm>."
- Đổi ảnh: "Đổi ảnh <model> trong catalogue <tên dòng> hãng <…>" + ảnh.
- Duyệt: "Duyệt <tên>" / "Trả lại <tên>: <lỗi>".
AI tự làm phần còn lại: đọc quy tắc, khoá, dựng, kiểm tự động, kiểm mắt, gửi ảnh xem trước 3 hãng cạnh nhau + bảng thay đổi cũ→mới, gom câu hỏi 1 lần.

## 6. Cập nhật skill (điều phối + nhân viên)
Đầu phiên chỉ đọc QUY_TAC_HIEN_HANH + HO_SO_HANG + TRANG_THAI (≤6 KB); thay 43/43 bằng kiem_catalogue.py (trừ sửa catfix); sửa phạm vi hãng (FS/FC 3 hãng, Roots P+R, KTZ 3 hãng); H lẻ giữ; ảnh theo 3.3; thêm 3.2–3.6; lưu mã dựng vào templates; mẫu lệnh mục 5; luồng trả lời chuẩn; nhận bản chính 1 lệnh; skill NV + gói Drive đồng bộ cùng bản.

## 7. Lộ trình
GĐ1 quy tắc + hồ sơ hãng + skill + gói Drive + mẫu lệnh. GĐ2 kiem_catalogue.py, chạy 62 PDF → danh sách lỗi đầy đủ. GĐ3 sửa lỗi mục 2 + kho ảnh (anh duyệt mẫu trước). GĐ4 thư viện dựng 19 nhóm.
