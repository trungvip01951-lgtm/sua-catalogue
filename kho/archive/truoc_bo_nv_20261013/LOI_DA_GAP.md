# Lỗi đã gặp — bài học để không lặp lại

Mỗi dòng là lỗi THẬT: anh Trung báo (A), thấy khi rà 13/10/2026 trên 62 bản đã duyệt (B — claude/PHUONG_AN_HOAN_THIEN_20261013.md mục 2), hoặc lỗi cách làm (C). Lỗi trên 62 bản đã duyệt KHÔNG sửa lại trừ khi anh ra lệnh (QĐ 147); chúng là bài học cho bản dựng mới.
Cột "Kiểm tự động" = số mục của tools/kiem_catalogue.py (đánh số như phương án 13/10): 1 chữ cấm + 50 Hz · 2 điện/pha · 3 bảng (Q tăng H giảm, dấu "–", thứ tự công suất, số model = số nhãn) · 4 đường (≤5%, điểm uốn, móc, ≤8 đường) · 5 chữ chồng, cỡ chữ · 6 ảnh (ppi, tràn mép, chồng 2 lần, 1 ảnh nhiều cỡ) · 7 tương phản · 8 tệp (A4, dung lượng, phông lặp, RGB, khoảng trống) · 9 khác giao diện 3 hãng · 10 mã kiểm khớp DANH SACH. "mắt" = chưa có phép kiểm tự động, phải nhìn PDF thật.
QTH = rules/QUY_TAC_HIEN_HANH.md; CTB = rules/CHUAN_TRINH_BAY.md; QĐ = rules/QUYET_DINH_ANH.md.

| # | Lỗi | Ví dụ (tệp / trang) | Quy tắc chặn | Kiểm tự động |
|---|---|---|---|---|
| A1 | Đường Q–H uốn gợn, ngoằn nghèo dù khớp số | AQUARIS SP 3SP1, 5SP15; SP V2 PEROTAC/REDPUMP bị anh trả lại (06/10) | QTH 4.2; CTB 2.2 (PCHIP, không điểm uốn) | 4 + mắt |
| A2 | 3 hãng cùng loại quá giống, chỉ đổi màu/logo | SP V2 ba hãng (06/10) | QTH 6; HO_SO_HANG (≥5/6 trục) | 9 |
| A3 | Ảnh còn chữ/logo/tem hãng khác | SP ba hãng chữ SUMOTO (06/10); CDX PEROTAC logo "THT maybomnuochcm.vn" (LOI_ANH_BAO 2); REDPUMP WC chữ "7.5KW/11KW" (QĐ 11); AQUARIS WC tem nắp động cơ (QĐ 114); ảnh SA tem đỏ (QĐ 129) | QTH 7; CTB 1.6 | mắt |
| A4 | Ô "–" nằm giữa dãy H | CM AQUARIS tr.3 (CM 40-125/1.1, /1.5, /2.2), tr.9; CM PEROTAC/REDPUMP tr.5, tr.10; 3M cả 3 hãng tr.4–5 (LOI_ANH_BAO 4) | QTH 4.7; CTB 3.2 | 3 |
| A5 | Vật liệu ghi sai | CM PEROTAC + AQUARIS trục "AISI 304" phải là 316 (LOI_ANH_BAO 3) | QTH 3 | mắt (đối chiếu DU_LIEU) |
| A6 | Bảng/đường có đoạn Q tăng mà H không giảm | nguồn 6SL25 Q 0→3 (03/10); CM 65-200 tại Q 54, CM 80-160/11 tại Q 90 (QĐ 93) | QTH 4.1 | 3, 4 |
| A7 | Đường công suất lớn chạm/cắt đường nhỏ hơn | CM 32-200/5.5 chạm /4 tại Q 24 (QĐ 67, 71); AQUARIS 4SA8/5 chạm 4SA8/6 (QĐ 92) | QTH 4.4 | 3 |
| A8 | Logo xấu/sai, đặt trong ô nền to khác màu | PEROTAC SP trang 6 mẫu (06/10) | QTH 5 | mắt |
| A9 | Kẻ bảng đậm/mờ không đều; nhãn đường chỉ ghi hậu tố (-30, -28) | SP6 mẫu V1 (06/10) | CTB 3.6, 2.6 | 5 + mắt |
| A10 | Ghi bảo hành | WC, SP, SS, SA nguồn; bìa SP AQUARIS "2 năm" (QĐ 34, 40) | QTH 5 | 1 |
| A11 | Ghi cân nặng | mọi catalogue trước 08/10 (QĐ 114); Root RL P/R còn "Weight … kg" (B11) | QTH 5 | 1 |
| A12 | Tên model sai | GB-9000S → GB-9500S (QĐ 90); CM 32-125/0.7 → /0.75 (QĐ 114) | QTH 2 | mắt (đối chiếu DU_LIEU) |
| A13 | Catalogue mới không có đường đặc tính; ảnh để nguyên nền kho/hộp/túi | PEROTAC 80WQX40-15-5.5 ứng viên 01b (13/10 09:26, QĐ 145) | QTH 6, 7 | mắt |
| A14 | Ảnh đại diện bị cắt xén, lẹm vào thân bơm | PEROTAC 80WQX40-15-5.5 ứng viên 02 (13/10 09:38, QĐ 146) | QTH 7; CTB 1.3, 1.8 | 6 + mắt |
| B1 | Ảnh bơm + ống mờ, viền răng cưa, đế bị cắt, vệt trắng | PEROTAC WC tr.2; REDPUMP WC tr.1 | CTB 1.2, 1.3, 1.7 | 6 |
| B2 | Nền ảnh trang trí (nước bắn) mờ, vỡ hạt | REDPUMP WC tr.1 | CTB 1.1 | 6 + mắt |
| B3 | Ảnh còn phông xám, đế trưng bày, cuộn cáp | AQUARIS WC tr.1 | CTB 1.1 | mắt |
| B4 | Một ảnh dùng cho nhiều cỡ; ảnh lệch tông, không bóng, viền xanh mép trái | AQUARIS SP tr.1 (6"/8"/10"; 4"/5") | CTB 1.4, 1.5 | 6 |
| B5 | Hai hãng chỉ lật trái-phải, đổi màu | SP PEROTAC vs REDPUMP | HO_SO_HANG mục 3 | 9 |
| B6 | Biểu đồ hai hãng giống hệt; đường có móc gãy, gần thẳng | CDX PEROTAC vs REDPUMP tr.2; AQUARIS CDX tr.2 đường ② (CDX70/07) | CTB 2.2; HO_SO_HANG | 4, 9 |
| B7 | Ảnh/bản vẽ dưới 150 ppi | GB 3 hãng (83–89 ppi), CDLF PEROTAC (92), Root RL tr.1 P/R (85–91), CDX tr.1 + bản vẽ nổ (97–124), SA AQUARIS (136) | CTB 1.2 (≥ 200 ppi) | 6 |
| B8 | Khoảng trống lớn trên trang | REDPUMP CM tr.1, REDPUMP CDX tr.1, PEROTAC CM tr.1, AQUARIS/PEROTAC CDX tr.1, AQUARIS WC tr.1 | CTB 4.4 (≤ 10%) | 8 |
| B9 | Chữ quá nhỏ (dưới 6 pt) | SP PEROTAC ~8.000 ký tự, SP REDPUMP ~6.600, Root RL P/R ~900 (nhỏ nhất 4,5 pt) | CTB 4.1 | 5 |
| B10 | Thiếu "50 Hz" | FS/FC inox 3 hãng; Root RL P/R | CTB 4.6 | 1 |
| B11 | Còn khối lượng "Weight … kg" | Root RL PEROTAC, REDPUMP | QTH 5 | 1 |
| B12 | Ảnh đặt 2 lần chồng nhau, tràn mép | REDPUMP SP: ảnh 1732×1240 ở tr.1/10/16/19 | CTB 1, 5 | 6 |
| B13 | Tệp quá nặng (phông nhúng lặp, ảnh trùng) | SP AQUARIS 14,7 MB; SP REDPUMP 14,2 MB | CTB 5.1–5.2 | 8 |
| B14 | Khổ trang lẻ, khác nhau giữa các tệp | nhiều tệp trong 62 bản (rà 13/10 mục 1) | QTH 6 (chỉ A4) | 8 |
| B15 | DANH SACH.txt lặp dòng, còn mã kiểm cũ, nhắc thư mục _BAN CU đã xoá | CATALOGUE DA DUYET/DANH SACH.txt (30 dòng DWO lặp; đã dọn 13/10) | QTH 8.9 | 10 |
| B16 | Số điền: cột áp ở điểm Q lớn nhất của mỗi dòng = 1, 2, 3… đúng thứ tự dòng trên trang (lỗi dựng cũ) | WC cả 3 hãng, mọi trang bảng (50WC 1→6 … 300WC 1→5), 45 dòng/hãng — phát hiện 13/10 | Số liệu chỉ lấy từ nguồn; cấm điền số thứ tự | 3 |
| C1 | Mã dựng các nhóm để trong work/ bị xoá đợt dọn kho 12/10 (đánh giá sai là nháp) → lần sửa sau phải dựng lại từ PDF | toàn bộ nhóm đã dựng 07–09/10 | QTH 8.4, 8.13 (mã dựng ở templates/<nhóm>/; không dọn rules/, DU_LIEU/, KHO_ANH/, templates/) | — |
| C2 | Nhận ĐẠT chỉ vì số khớp / đường liên tục, không nhìn PDF thật | SP V2 (06/10) | CTB 8.6–8.7 | 4 + mắt |
| C3 | Nhiều phiên ghi trùng số quyết định (19, 20, 25, 26, 96–97, 111–115) | archive/claude/QUYET_DINH_ANH_20261006_PHIEN_CLAUDE.md (đã đánh số lại 13/10 thành rules/QUYET_DINH_ANH.md) | QTH 9.1 (đọc lại số cuối ngay trước khi ghi) | — |
| C4 | Quy tắc rải ở nhiều tệp, mâu thuẫn, lỗi thời (Desktop, python Codex, "chỉ catfix", DWO cũ, bảo hành) | rules/ và AGENTS/START_HERE trước 13/10 | QTH là tệp hiện hành duy nhất; QTH 9 | — |

Lỗi kỹ thuật thời catfix (phông, ảnh quét, đo vùng…): knowledge/LOI_VA_CACH_TRANH.md — chỉ tra khi dùng catfix.
