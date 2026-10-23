# Trạng thái ngắn cho AI — cập nhật 13/10/2026

Mốc đọc nhanh đầu phiên, không phải sổ tiến độ. Thẩm quyền: rules/, tệp thật, sổ TIEN DO.md gốc. Giữ tệp ≤ 6 KB; mỗi phiên ghi đè mục 4. Bản cũ (53 KB, lịch sử 06–13/10): archive/claude/TRANG_THAI_CLAUDE_20261013_cu.md (chỉ tra theo từ khoá).

## 1. Đầu phiên

- Đọc: rules/QUY_TAC_HIEN_HANH.md → rules/HO_SO_HANG.md → rules/CHUAN_TRINH_BAY.md → tệp này. Khi cần: rules/QUYET_DINH_ANH.md (nhật ký, số QĐ), rules/LOI_DA_GAP.md, claude/VIEC_CHO_ANH.md, claude/LOI_ANH_BAO.md.
- Khoá việc: `python3 claude/khoa_viec.py xem` → `nhan <VIỆC> <PHIÊN> "<phạm vi>"` → `nha`.
- Môi trường Claude (Linux): `bash claude/dau_phien.sh env` (cài offline từ vendor/wheels, vài giây). `bash claude/dau_phien.sh test` (43/43) CHỈ bắt buộc khi dùng catfix.
- Lệnh dự án: `$HOME/cfenv/bin/python -B -X utf8 claude/cat.py health|status|context|claim…`. health báo "missing_paths: python" là lỗi sẵn có (manifest.json trỏ Python Windows) — bỏ qua; "controls.changed" phải rỗng.
- Mỗi lệnh shell ≤ 170 giây; tiến trình nền bị dừng khi lệnh kết thúc; trong kho không xoá được bằng rm.
- Sổ CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/TIEN DO.md và state/CURRENT_CHECKPOINT.md: chỉ grep theo từ khoá.
- Xem PDF: xuất PNG vào claude/_xem/xem_1…8.png (tên cố định, ghi đè), 110 dpi cả trang, 250–300 dpi vùng cắt.
- Đám mây (từ 23/10): kho ở GitHub riêng tư trungvip01951-lgtm/sua-catalogue, thư mục kho/. Hook .claude/hooks/session-start.sh (gốc repo) tự cài tesseract-ocr + qpdf, nối `$HOME/mnt/Sửa catalogue` → /home/user/sua-catalogue/kho, chạy `dau_phien.sh env` (wheels offline chỉ hợp Python 3.10 → tải mạng bản mới, QĐ 23/10). Làm xong phải commit + push; máy anh `git pull` trước khi làm. Kho có `.gitattributes` `* -text` để giữ CRLF, nếu bỏ thì niêm phong lệch.

## 2. Nơi gốc dữ liệu

| Gì | Ở đâu |
|---|---|
| Quy tắc, hồ sơ hãng, chuẩn trình bày, nhật ký quyết định, lỗi đã gặp | rules/ |
| Số liệu từng nhóm (một nguồn cho bảng + đường) | DU_LIEU/<nhóm>.xlsx |
| Ảnh đã duyệt | KHO_ANH/<nhóm>/<model>_<hãng>.png |
| Mã dựng đạt | templates/<nhóm>/ (bắt buộc; không để trong work/) |
| 62 PDF anh đã duyệt | CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/ + DANH SACH.txt |
| Bản chính 25 catalogue gốc | CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT)/ (nguồn bất biến: BẢN MỚI 01-10-2026) |
| Nguồn anh gửi thêm | CATALOG SUA/NGUON BO SUNG 2026100x/ |
| Công cụ | tools/ |
| Tệp đã chuyển chỗ | archive/ (danh sách archive/DA_CHUYEN_20261013.csv) |

## 3. Trạng thái

- Claude là người điều phối (QĐ 1): ghi sổ TIEN DO.md, nhận bản chính sau nghiệm thu.
- 62 PDF đã duyệt: AQUARIS 20, PEROTAC 21, REDPUMP 21; mã kiểm khớp DANH SACH.txt 62/62 (13/10). Không làm lại (QĐ 147).
- Skill dự án (một bản duy nhất): nguồn ở claude/skill/sua-catalogue/SKILL.md — sửa ở đây rồi đóng zip tải lên tài khoản Claude của người phụ trách.
- 13/10/2026 23:09 anh bỏ toàn bộ phần dành riêng cho nhân viên (gói Drive NV, skill NV, NV_LAM, tools/dong_bo_drive.py → archive/bo_phan_nhan_vien_20261013/; thư mục D:\ChatGPT\Sửa catalogue - DRIVE NV đã xoá). Cả dự án dùng 1 bộ quy tắc + 1 skill để anh giao nguyên cho nhân viên phụ trách.
- Việc chờ anh: claude/VIEC_CHO_ANH.md (QXN40-60, 80WQX40-15-5.5, 150WC300-30-37, SS-450, MHI, 4MIX, QĐ 136–138, mốc 137/149, bảng giá). Lỗi anh báo đang mở: không (LOI_ANH_BAO 4/4 đã sửa).
- Phương án 13/10 (QĐ 149) chia đợt A→D: A gộp quy tắc (xong 13/10); công cụ tools/kiem_catalogue.py, nhan_ban_chinh.py, ve_duong_cong.py, niem_phong.py, DU_LIEU/, KHO_ANH/ do các phiên khác — xem khoá trong claude/khoa/.

## 4. Đang ở đâu (16/10/2026, phiên CLAUDE_20261016T0826Z)

- REDPUMP 300IRG800-30-110 (bơm trục đứng IRG, catalogue riêng 1 trang) ứng viên 04 chờ anh duyệt: work/claude_irg300_20261016/ (BAO_CAO.md, build_irg300_04.py, IRG300_04.xlsx); có Qmin/Hmin thì đường chỉ vẽ Qmin–Qmax (QĐ 16/10 15:39). Đường qua 600/35, 800/30, 880/21 theo lệnh anh; điểm khác SUY RA (claude/QUYET_DINH_ANH_20261016.md).
- PEROTAC 200WC450-32-55 (bơm cắt rác, catalogue riêng 2 trang) ứng viên 01 chờ anh duyệt: work/claude_wc200_55_20261016/ (BAO_CAO.md, build_wc200_55.py, WC200_55.xlsx); chờ anh xác nhận dòng web 50–600/30–4 và H 5 m tại Qmax.
- Còn chờ anh: REDPUMP 250SWQ500-5 ứng viên 03 (work/claude_swq_20261015/); PEROTAC MHI-Q ứng viên 07; SF 3 hãng; 150WC300-30-37 ứng viên 02.
- Mẫu dựng catalogue riêng 1 model REDPUMP: build_irg300.py (đọc nhãn vạch trục tổng quát, có dải làm việc). Trong kho không ghi đè được tệp → dựng ở $HOME/claude_work rồi cp sang tên mới.

- 17/10 (phiên CLAUDE_20261017T0850Z): REDPUMP 6SP30 catalogue riêng (A4 dọc, gốc bản 16 ad416b37fb9b) thêm ảnh, vật liệu, IP68/IE3/2850, bỏ cột kg — ứng viên 17A (5506fbe3cbab) và 17B (ba29a33c8174) chờ anh chọn: work/claude_6sp30_20261017/ (BAO_CAO.md, build_6sp30_17.py).

## 5. Giữ kho gọn

- Không xoá tệp: tệp bỏ thì mv sang archive/ và ghi archive/DA_CHUYEN_<ngày>.csv (đường cũ, đường mới, lý do).
- Không bao giờ dọn rules/, DU_LIEU/, KHO_ANH/, templates/, CATALOG SUA/ (bài học 12/10: mã dựng trong work/ bị xoá nhầm).
- Nháp: $HOME/claude_work/<việc> (ngoài kho). Cuối phiên: ghi đè mục 4 + bàn giao ngắn claude/BAN_GIAO_<UTC>.md ≤ 2 KB.

- 23/10 (phiên CLAUDE_20261023T0255Z): đưa kho lên đám mây (claude/QUYET_DINH_ANH_20261023.md). Đám mây: 43/43 ĐẠT, môi trường 4/4, controls.changed rỗng (sau khi anh đẩy lại giữ CRLF). Không sửa catalogue nào.
