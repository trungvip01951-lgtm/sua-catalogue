# DU_LIEU — số liệu gốc mỗi dòng bơm (một nguồn)

Tách ngày 13/10/2026 từ 62 catalogue đã duyệt (CATALOG SUA/CATALOGUE DA DUYET) bằng script đọc chữ trong PDF, không gõ tay. Lần sửa sau: đổi số TRONG tệp này (ghi cũ → mới ở cột nguon/ghi chú), rồi dựng bằng tools/ve_duong_cong.py — không dựng lại từ PDF.

Sheet:
- THONG_TIN: khoa | gia_tri | nguon (nhom, ten_dong_EN, hang_co, tan_so, so_cuc, toc_do_vg_ph, dieu_kien, ghi_chu).
- MODEL: hang | model_1pha | model_3pha | p2_kw | p2_hp | dong_A_1pha | dong_A_3pha | dien_ap_1pha | dien_ap_3pha | hong_hut | hong_xa | thong_so_khac | nguon | nghi_ngo.
- QH: hang | model | q_m3h | h_m | nguon (mỗi ô bảng Q–H một dòng).
- BANG (thiết bị không có Q–H: GB, RL, MIX, 4MIX, JLM_JBB, DN270): cột đúng như bảng PDF.
- KIEM: tự kiểm (số model = PDF, Q tăng H giảm, so giữa các hãng).

Lưu ý đã biết:
- WC: H tại Q lớn nhất trùng số thứ tự dòng trên trang (nghi số điền) — cột nghi_ngo; xem claude/VIEC_CHO_ANH.md.
- CM, SA 4 inch, SP: AQUARIS khác PEROTAC/REDPUMP ở một số model (khác nguồn) — giữ nguyên trừ khi anh chỉ đạo.
- KTZ_LH: chỉ có điểm định mức và điểm max (đường cong trong PDF là hình).
- MHI, IRG: chỉ 1 điểm danh định mỗi mã. IRG không vẽ đường (QĐ 71).
- so_cuc = 2 suy từ "n ≈ 2850–2900/min" (PDF không ghi chữ "cực").
- PEROTAC dùng tiền tố SS cho bơm giếng 2/2.5/3 inch (AQUARIS, REDPUMP dùng SA).
- Cột cân nặng (nếu PDF có) chỉ để tham khảo — không đưa lên catalogue mới.
