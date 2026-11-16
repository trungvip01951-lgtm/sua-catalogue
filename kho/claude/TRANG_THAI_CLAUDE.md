# Trạng thái ngắn cho AI — cập nhật 14/11/2026

Mốc đọc nhanh đầu phiên, không phải sổ tiến độ. Thẩm quyền: rules/, tệp thật, sổ TIEN DO.md gốc. Giữ tệp ≤ 6 KB; mỗi phiên GHI ĐÈ mục 4 (không nối thêm dòng). Bản cũ: archive/claude/TRANG_THAI_CLAUDE_20261114_cu.md, …_20261013_cu.md (chỉ tra theo từ khoá).

## 1. Đầu phiên

- Đọc: rules/QUY_TAC_HIEN_HANH.md → rules/HO_SO_HANG.md → rules/CHUAN_TRINH_BAY.md → tệp này. Khi cần: rules/QUYET_DINH_ANH.md (nhật ký, số QĐ — nơi DUY NHẤT ghi quyết định), rules/LOI_DA_GAP.md, claude/VIEC_CHO_ANH.md, claude/LOI_ANH_BAO.md.
- Đám mây (từ 23/10, QĐ 183): kho ở GitHub riêng tư trungvip01951-lgtm/sua-catalogue, thư mục kho/; xem CLAUDE.md ở gốc repo. Hook .claude/hooks/session-start.sh tự cài tesseract + qpdf, nối `$HOME/mnt/Sửa catalogue` → kho/, cài thư viện. Làm xong phải commit + push; máy anh `git pull` trước khi làm. Giữ `.gitattributes` `* -text`. Tệp rác không đưa lên: xem .gitignore.
- Python: `$HOME/cfenv/bin/python -B -X utf8`, chạy tại kho/. Lệnh dự án: `claude/cat.py health|status|context|claim…` ("changed" phải rỗng; "missing_paths: python" là lỗi sẵn có, bỏ qua). `bash claude/dau_phien.sh test` (43/43) CHỈ bắt buộc khi dùng catfix.
- Khoá việc: `claude/khoa_viec.py xem` → `nhan <VIỆC> <PHIÊN> "<phạm vi>"` → `nha <VIỆC> <PHIÊN> "<ghi chú>"` (đủ 3 tham số).
- Mỗi lệnh shell ≤ 170 giây. Sổ TIEN DO.md và state/CURRENT_CHECKPOINT.md: chỉ grep theo từ khoá.
- Xem PDF: xuất PNG vào claude/_xem/ (tên cố định, ghi đè; thư mục này không lên GitHub), 70–110 dpi cả trang, 250–300 dpi vùng cắt. Nháp: `$HOME/claude_work/<việc>` (ngoài kho, mất khi máy đám mây bị thu hồi — chép mã dựng + xlsx vào work/<việc>/ trước khi commit).

## 2. Nơi gốc dữ liệu

| Gì | Ở đâu |
|---|---|
| Quy tắc, hồ sơ hãng, chuẩn trình bày, nhật ký quyết định, lỗi đã gặp | rules/ |
| Số liệu từng nhóm (một nguồn cho bảng + đường) | DU_LIEU/<nhóm>.xlsx (đọc DU_LIEU/README.md) |
| Ảnh tách từ bản đã duyệt | KHO_ANH/<nhóm>/<mã băm>.<đuôi> + KHO_ANH/DANH_MUC.csv |
| 62 PDF anh đã duyệt | CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/ + DANH SACH.txt (mã kiểm khớp 62/62, đo 16/11) |
| Catalogue riêng theo báo giá (mã dựng, xlsx, báo cáo, PDF) | work/claude_<việc>_<ngày>/ |
| Bản chính 25 catalogue gốc / nguồn bất biến | CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT)/ ; BẢN MỚI 01-10-2026, NGUON BO SUNG … |
| Công cụ | tools/ (ve_duong_cong.py, kiem_catalogue.py, nhan_ban_chinh.py, niem_phong.py) |
| Skill dự án | claude/skill/sua-catalogue/SKILL.md (+ .zip để tải lên tài khoản) |

## 3. Trạng thái

- Claude là người điều phối (QĐ 1). 62 PDF đã duyệt: AQUARIS 20, PEROTAC 21, REDPUMP 21 — không làm lại (QĐ 147).
- Từ 13/10 việc chính là CATALOGUE RIÊNG theo báo giá (QTH 4.16–4.18): mỗi việc một thư mục work/, PDF đặt tên "HÃNG - Tên … <số bản>.pdf" (QĐ 163). Chưa bản nào trong số này vào CATALOGUE DA DUYET.
- Rà soát toàn dự án 14/11 (QĐ 184): kết quả + đề xuất chờ anh duyệt ở claude/RA_SOAT_20261114.html.
- DU_LIEU/CM.xlsx hàng AQUARIS 3 mã (CM 32-160/3, CM 40-250/11, CM 65-200/22) đang mang số báo giá (QĐ 165) trong khi bản AQUARIS CM đã duyệt còn số cũ — chờ anh duyệt bản vá "AQUARIS - Bơm trục ngang CM 1.pdf" (khoá CM_AQUARIS_BG đang giữ). Bản cũ: history/DU_LIEU_CM_truoc_QD165_20261030.xlsx.
- Lỗi công cụ đã biết: xem claude/RA_SOAT_20261114.html mục công cụ.

## 4. Đang ở đâu (16/11/2026, phiên CLAUDE_20261116)

Catalogue riêng đã giao, chờ anh duyệt hoặc trả lời (chi tiết + câu hỏi: claude/VIEC_CHO_ANH.md mục A, B):

| Ngày | Catalogue (hãng) | Thư mục work/ | Bản mới nhất |
|---|---|---|---|
| 16/11 | CDLF thêm dải 65–200 + trang cấu tạo 120/150/200, 3 hãng | claude_cdlf_them_dai_20261116 | ĐÃ NHẬN BẢN CHÍNH (QĐ 187); mã dựng: dung_<hãng>.py + lib.py |
| 14/11 | 50GDL18-15×9 (REDPUMP) | claude_gdl_redpump_20261114 | 1 — hỏi ảnh, điện áp |
| 13/11 | WC 150WC/200WC 37–132 kW, 14 mã (REDPUMP) | claude_wc_redpump_20261113 | 3, tiếng Anh + tiếng Việt |
| 03/11 | TKP600 / TKP800 (REDPUMP) | claude_tkp_redpump_20261103 | 1 |
| 03/11 | 6SP60, 15 mã (REDPUMP) | claude_6sp60_20261103 | 4 |
| 30/10 | CM AQUARIS vá 3 mã theo báo giá | claude_cm_aquaris_bg_20261030 | 1 — hỏi CM 32-200/5.5 |
| 30/10 | FC 75/40 (PEROTAC) | claude_fc7540_20261030 | 1 |
| 29/10 | RPX 2 mã (REDPUMP) — KHÔNG có trên GitHub (QĐ 169) | claude_rpx_redpump_20261029 | 1 — hỏi thứ tự tên |
| 27/10 | CM 32-160/3; CDLF8-12T + CDLF16-8T (PEROTAC) | claude_bg27102026_20261027 | 1 |
| 24/10 | CM 32-250/7.5 + CM 40-160/4 (AQUARIS) | claude_cm2_aquaris_20261024 | 2 |
| 23/10 | SS-150 (PEROTAC) | claude_ss150_20261023 | 2 |
| 16/10 | 300IRG800-30-110 (REDPUMP); 200WC450-32-55 (PEROTAC) | claude_irg300_20261016; claude_wc200_55_20261016 | ứng viên 04; 01 |
| 15/10 | 250SWQ500-5 (REDPUMP) | claude_swq_20261015 | ứng viên 03 |
| 13–14/10 | 80WQX40-15-5.5, 150WC300-30-37, SF 3 hãng, cụm MHI-Q (PEROTAC) | claude_wqx_…, claude_wc150_37_20261014, claude_sf_…, claude_mhi2_… | xem VIEC_CHO_ANH |

Đã xong: REDPUMP 6SP30 (17B, anh duyệt QĐ 157); đánh giá biên bản thử V250/V450F/V750 so với SS (work/claude_v_ss_20261103/DANH_GIA.md).
Mẫu mã dựng nên chép khi làm việc mới: REDPUMP 1 trang — work/claude_gdl_redpump_20261114/build_gdl.py; REDPUMP nhiều trang, 2 thứ tiếng — work/claude_wc_redpump_20261113/build_wcl.py; PEROTAC — work/claude_fc7540_20261030/build_fc7540.py; AQUARIS — work/claude_cm2_aquaris_20261024/build_cm2.py.

## 5. Giữ kho gọn

- Không xoá tệp có nội dung: tệp bỏ thì mv sang archive/ và ghi archive/DA_CHUYEN_<ngày>.csv. Không bao giờ dọn rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/.
- Cuối phiên: ghi đè mục 4, cập nhật claude/VIEC_CHO_ANH.md, ghi bàn giao claude/BAN_GIAO_<UTC>.md ≤ 2 KB, commit + push.
