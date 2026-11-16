# DU_LIEU — số liệu gốc mỗi dòng bơm (một nguồn)

Tách ngày 13/10/2026 từ 62 catalogue đã duyệt (CATALOG SUA/CATALOGUE DA DUYET) bằng script đọc chữ trong PDF, không gõ tay. Lần sửa sau: đổi số TRONG tệp này (ghi cũ → mới ở cột nguon/ghi chú), rồi dựng bằng tools/ve_duong_cong.py — không dựng lại từ PDF.

Sheet:
- THONG_TIN: khoa | gia_tri | nguon (nhom, ten_dong_EN, hang_co, tan_so, so_cuc, toc_do_vg_ph, dieu_kien, ghi_chu).
- MODEL: hang | model_1pha | model_3pha | p2_kw | p2_hp | dong_A_1pha | dong_A_3pha | dien_ap_1pha | dien_ap_3pha | hong_hut | hong_xa | thong_so_khac | nguon | nghi_ngo.
- QH: hang | model | q_m3h | h_m | nguon (mỗi ô bảng Q–H một dòng).
- BANG (thiết bị không có Q–H: GB, RL, MIX, 4MIX, JLM_JBB, DN270): cột đúng như bảng PDF.
- KIEM: tự kiểm (số model = PDF, Q tăng H giảm, so giữa các hãng).

Lưu ý đã biết:
- WC: H tại Qmax = 1, 2, 3… m theo nấc công suất trong cùng cỡ họng — ĐÚNG quyết định 19 của anh, không phải lỗi.
- CM, SA 4 inch, SP: AQUARIS khác PEROTAC/REDPUMP ở một số model (khác nguồn) — giữ nguyên trừ khi anh chỉ đạo.
- KTZ_LH: chỉ có điểm định mức và điểm max (đường cong trong PDF là hình).
- MHI, IRG: chỉ 1 điểm danh định mỗi mã. IRG không vẽ đường (QĐ 82, 149; số cũ 71).
- so_cuc = 2 suy từ "n ≈ 2850–2900/min" (PDF không ghi chữ "cực").
- THONG_TIN so_cuc / toc_do_vg_ph nên là SỐ trơn (2, 2900); chữ giải thích để ở cột nguon. Nguồn không ghi cả hai thì điền "KHÔNG GHI" vào cả hai ô để khối điều kiện dưới biểu đồ bỏ cụm số cực – tốc độ (14/11/2026).
- PEROTAC dùng tiền tố SS cho bơm giếng 2/2.5/3 inch (AQUARIS, REDPUMP dùng SA).
- Cột cân nặng (nếu PDF có) chỉ để tham khảo — không đưa lên catalogue mới.
- CDLF (16/11/2026, QĐ 186–187): thêm dải CDLF65, 85, 120, 150, 200 (87 mã mỗi hãng, chỉ 3 pha) từ catalogue CDL nhà cung cấp; tốc độ 2900 /min (65, 85) và 2950 /min (120–200) ghi ở cột thong_so_khac cùng bộ kích thước; THONG_TIN.toc_do_vg_ph vẫn là 2900 của các dải cũ.
