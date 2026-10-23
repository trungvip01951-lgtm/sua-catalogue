# Trạng thái ngắn cho Claude — cập nhật 06/10/2026 (UTC 20261006T1150Z)

Đây là **mốc đọc nhanh đầu phiên**, không phải sổ tiến độ. Thẩm quyền vẫn là sổ `TIEN DO.md` gốc, `rules/` và tệp thật. Lệch nhau thì tin sổ gốc và tệp thật, rồi sửa tệp này. Giữ tệp dưới ~6 KB: mốc cũ thì xóa khỏi đây (đã có trong sổ gốc).

## 1. Đầu phiên (≈2 phút, ít token)

```
bash "$HOME/mnt/Sửa catalogue/claude/dau_phien.sh" env     # cài môi trường riêng, ngoài kho
bash "$HOME/mnt/Sửa catalogue/claude/dau_phien.sh" test    # 43 bài kiểm catfix + health
```
- **08/10: cài OFFLINE.** Bộ cài Python (pymupdf, scipy, opencv, pikepdf, fonttools, pytesseract, numpy…) lưu sẵn ở `vendor/wheels/` (tệp >25 MB tách `.partNN`); `env` tự ghép và cài trong ~7 giây, không tải mạng (mạng máy anh rất chậm, tải từ mạng sẽ quá 180 giây và bị ngắt). Chạy `env` và `test` THÀNH HAI LỆNH riêng; không chạy pip nền (bị tắt khi lệnh kết thúc). Trong thư mục kho không xoá/ghi đè được bằng rm; ghi ảnh xem bằng open(...,"wb").
- Phải ra `43/43 ĐẠT` và `Môi trường ĐƯỢC: 4/4`; chưa đủ thì KHÔNG sửa catalogue, không sửa catfix cho qua.
- Lệnh dự án: `$HOME/cfenv/bin/python -B -X utf8 claude/cat.py health|status|context|claim|check|heartbeat|release|receipt ...` (lớp bọc dịch đường dẫn Windows→mount theo `claude/paths_linux.json`; công cụ gốc `tools/catalogue.py` không đổi).
- catfix: đặt `CATFIX_ROOT="$HOME/mnt/Sửa catalogue/CATALOG SUA"`, `PYTHONPATH` trỏ gói trong `vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT`.
- **10/10/2026: Catalog Sua ĐÃ GỘP vào kho** → `D:\ChatGPT\Sửa catalogue\CATALOG SUA` (C:\Users\H2\Desktop\Catalog Sua đã xóa sau khi đối chiếu SHA 6694/6694). Mọi chỗ ghi `Catalog Sua\…` bên dưới nay là `CATALOG SUA\…` trong kho. Rác chờ xóa: `_CHO_XOA_20261010` (anh xem rồi mới xóa hẳn).
- **11/10/2026 18:40:** Claude (điều phối) đã đọc `DUONG_DAN_MOI_20261010.md`, bàn giao 10/10 và mục này; dùng đường mới `CATALOG SUA`. Chạy lại 43/43 phiên này: CHƯA (môi trường Linux trên máy không khởi động được lúc 11/10) — phải chạy `dau_phien.sh env` rồi `test` trước khi sửa catalogue.
- Mount: `Sửa catalogue` (kho, D:, gồm cả CATALOG SUA), `b-n-h-y-s-a` (workspace cũ của ChatGPT, chỉ đọc khi cần).
- Môi trường Claude: Linux, Python 3.10, scipy 1.15, pikepdf 10.13 — khác máy ChatGPT (Windows, 3.12, scipy 1.18, pikepdf 10.16). Sau mỗi lần ghi phải đo lại số trên PDF đã lưu.

- **12/10/2026: ĐÃ DỌN RÁC KHO** (anh duyệt): còn 1.645 tệp/609 MB; `_CHO_XOA_20261010`, `history/` cũ, `work/` cũ, bằng chứng G01–G18, `_BAN CU` đã xoá hẳn. Chi tiết `claude/BAN_GIAO_20261012T0930Z.md`. Câu "tra history/don-rac-gop-kho-20261010" trong DUONG_DAN_MOI không còn dùng được.


- **12/10/2026 16:57: anh bỏ dự án ChatNoiBo** — đã xoá work/nv_giamdoc_*, deliverables/ung_vien_nhan_vien, cfenv_win, bộ cài Windows; 18:47 xoá luôn D:\ChatGPT\ChatNoiBo và D:\ChatGPT\cfenv_win; nhả khoá SS_PEROTAC của phiên ChatNoiBo (việc SS-450 Qmax 18→24 chưa làm xong, chưa ghi bản chính).

- **12/10/2026: gói Drive cho nhân viên** ở `D:\ChatGPT\Sửa catalogue - DRIVE NV` (737 tệp, 428 MB; CATALOG SUA khớp SHA 425/425; catfix trong gói 43/43). NV chỉ ghi `NV_LAM/`; bản chính vẫn ở kho này. Bản chính đổi thì phải cập nhật lại gói.

## 2. Đọc gì, khi nào

- Luôn đọc: tệp này + `rules/QUY_TAC_CUNG_HIEN_HANH.md` (18 KB, quy tắc cứng).
- Trước khi sửa một catalogue: `claude/cat.py context --file ...`, prompt nhóm, `procedures/` đúng loại, `templates/catalogue/README.md`, và `grep` từ khóa trong `knowledge/LOI_VA_CACH_TRANH.md`.
- Sổ `TIEN DO.md` (125 KB) và `state/CURRENT_CHECKPOINT.md` (59 KB): **chỉ grep theo mã việc/tên tệp**, hoặc `cat.py status` để lấy các dòng cuối. Không đọc hết.

## 3. Quy tắc cứng tóm tắt (chi tiết ở rules/)

- Nguồn `BẢN MỚI 01-10-2026` bất biến. Chỉ catfix ghi catalogue. Một catalogue một bên ghi, có khóa `claim`. Không cài gì lên máy anh, không đụng giấy phép Office.
- Ứng viên lưu tệp mới ở hồ sơ riêng; bản chính chỉ nhận đúng byte ứng viên đã nghiệm thu, sau sao lưu và đọc lại SHA.
- Q tăng thì H giảm. Đường Q–H cong đều, không gợn; sai lệch từng điểm bảng ≤5%; giữ Qmin/Qmax/Hmin/Hmax và điểm làm việc đã khóa; H trung gian được sửa số nguyên (ghi cũ→mới). Q được 1 số lẻ theo nguồn.
- Cùng loại bơm, ba hãng PEROTAC/REDPUMP/AQUARIS phải khác rõ màu, nền đầu trang, cách trình bày. Thiết kế đơn giản, dễ đọc, không lòe loẹt. Mọi catalogue đối chiếu đủ ba hãng; hãng thiếu nguồn riêng dùng nguồn Perotac đã kiểm.
- Điện: 1 pha 220–240 V, 3 pha 380–415 V, chỉ 50 Hz; >3 kW và giếng 6 inch chỉ 3 pha; có model 1 pha thì phải có model 3 pha. SA nhựa 4 inch: 4SA4/6/8/10 xả 1,5 inch, 4SA12/16 xả 2 inch. Bỏ 4SP2/4SPM2, giữ 3SP2.
- Phông: được dùng phông giống/sát nhất cho chữ thiếu, phải ghi rõ "gần giống". DWO: Qmin=1, Hmin=1; DWO150 33/15; DWO500 3,7 kW 72/25.
- Phiếu QA có hai mục riêng **KHÁC GIAO DIỆN GIỮA CÁC HÃNG** và **ĐƯỜNG CONG ĐỀU**, kèm PDF/SHA/trang/biểu đồ đã nhìn. Kiểm số, hình thức, bảo toàn, bản in là bốn kết quả riêng. Thiếu dữ liệu ghi CHƯA THỂ XÁC MINH, không đoán, không đặt 0.
- Hai lần cùng một cách không đạt thì dừng cách đó. Không chạy lại mã lịch sử có số/tọa độ/SHA cố định. Báo cáo 8 cột.

## 3b. Quy tắc anh thêm 06/10 — đã nhập rules/QUY_TAC_CUNG_HIEN_HANH.md mục cuối (1–18), niêm phong lại 20261006T151425Z

- Ba hãng cùng loại catalogue: khác cả **bố trí + màu sắc + cách trình bày** (không chỉ màu/logo); QA chấm riêng ba mặt.
- **Khóa việc theo phiên:** `python3 claude/khoa_viec.py xem|nhan|nha` (+ `cat.py claim` nếu ghi 25 catalogue gốc). Việc phiên khác giữ thì không động vào, không chiếm khóa.
- Tách việc độc lập cho **nhiều AI chạy song song**, mỗi AI một khóa/thư mục/tệp ra riêng; vẫn phải chính xác.
- **Kiểm độc lập + sửa + kiểm lại đạt hết mới là xong**; chỉ kiểm phần vừa làm và phần bị ảnh hưởng, không kiểm lan man.

## 4. Đang ở đâu

- Mốc cuối sổ gốc: **SP ba hãng V3 đã nhận** 20261006T093634Z — AQUARIS 31 trang, PEROTAC 13, REDPUMP 13; PDF ở `deliverables/SP BA HANG THIET KE RIENG 20261006`; mẫu `templates/catalogue/SP_THREE_BRANDS_V3_20261006`. V2 bị trả lại, không phát hành.
- Tồn của V3: dấu mờ PR/RP chưa xác minh; ảnh chỉ nét bằng nguồn; in giấy chưa kiểm.
- Việc gốc: **137/149** (không cộng phần mở rộng). Tồn theo bảng mốc cũ, phải grep sổ trước khi nhận: #34, #52, #137, G12 (3 việc), G13 (#110/#154/#155), #128, #101, #123 (in Excel, Office chặn) = 12 việc. #53 (giữ hợp lệ, sổ dòng 05/10 23:16) và #118 (CDX đạt, G15 8/8, sổ dòng 06/10 00:58) ĐÃ ĐÓNG — đối chiếu sổ gốc 06/10 15:15Z. Phần lớn kẹt phông; quyền phông gần nhất nay đã có nên có thể mở lại.
- Mở rộng còn dở (ghi 03–04/10, có thể cũ): đồ họa SA/SL ngoài trang 8, SL Redpump trang 8, biểu đồ DWO Excel, GB 48 đường thiếu bảng số.
- Không có khóa nào đang giữ (kiểm 06/10 11:49Z).

## 5. Vai trò — anh đã xác nhận 06/10/2026

Anh Trung xác nhận trực tiếp trong phiên Claude ngày 06/10/2026: **Claude thay vai người điều phối** (trước là ChatGPT ROOT) — được ghi thêm dòng vào sổ `TIEN DO.md` gốc và nhận bản chính sau nghiệm thu, theo đúng quy trình sao lưu/đọc lại SHA. Các câu "chỉ ChatGPT ROOT ghi sổ" trong tài liệu cũ là trạng thái lịch sử. Vẫn giữ: một catalogue một bên ghi, nhận khóa trước ghi, kiểm `status` xem có khóa lạ trước mỗi lô. Nếu thấy dấu hiệu ChatGPT vừa ghi (khóa mới, SHA bản chính đổi ngoài dự kiến) thì dừng và báo anh.

## 4b. Mục tiêu lớn (rules/CHOT_PHAM_VI_VA_QUY_TAC_20261006_SP_BA_HANG.md)

15 nhóm, mỗi hãng một PDF riêng, tiếng Anh, chỉ 50 Hz: 1 CM, 2 3M, 3 WC (+4 mã mới), 4 SS, **5 SP (XONG V3)**, 6 SA (Redpump lấy nguồn SL), 7 SL (không làm riêng), 8 FS (chỉ Aquaris), 9 IRG, 10 GB, 11 KTZ–LH (hỏi Aquaris khi tới), 12 CDLF, 13 CDX, 14 DWO, 15 Roots (chỉ Perotac). Danh sách này không cộng vào 149 việc gốc. Đọc tệp phạm vi trước khi nhận nhóm.

## 4·. Việc đang mở (06/10 14:36Z)

AQUARIS SP trang 1–2 thiết kế mới: **ứng viên 01 đã lưu qua catfix và QA đạt**, đã gửi anh. Chờ anh duyệt. Đọc `work/claude_aq_p12_20261006/BAO_CAO_8_COT.md`. Nếu anh duyệt: claim lại, kiểm SHA bản chính 8170fe4d…, sao lưu vào history/, chép đúng byte ứng viên e6f0541b… lên bản chính, đọc lại, ghi sổ, refresh inventory. Nếu anh sửa: sửa `build_preview.py`, xem thử, lưu UNG VIEN 02 (không ghi đè 01). Anh đã chốt: giữ dải ba màu Ý; bảo hành 2 năm ghi chung cả dòng Aquaris; giữ phông Lato + Liberation Sans; ảnh bơm được phóng + tăng nét (không AI). Chưa làm: áp ảnh nét hơn cho trang 3–31 (cần anh giao). Rác cần xóa khi có quyền: `work/claude_aq_p12_20261006/AQUARIS SP - MAU TRANG 1-2 v1 (XEM THU).pdf`.

## 4··. WC + SP — ĐÃ NHẬN BẢN CHÍNH 07/10 ~06:55Z — ANH ĐÃ DUYỆT bộ này (07/10, sau khi xem 4 tệp), đã chép vào `Catalog Sua\CATALOGUE DA DUYET\<HÃNG>`

- **WC:** PEROTAC 2dbe9399… (9 trang: trang 1 cấu tạo + tính năng, phớt SiC), REDPUMP bf45e427…, AQUARIS f96fe393…. Họng 250 theo số anh (1100; 17/20/24). Biên nhận `history/wc-hong250-va-trang-cau-tao-accepted-20261007T065348Z`. Hồ sơ `work/claude_wc_20261006` (`BAO_CAO_8_COT.md`, `BANG_SO_DA_DOI.md`, `QA_UNG_VIEN_P11_R07_A07.json`). Nền đọc số/nền dựng = bản CŨ ở `history/wc-three-brand-redesign-accepted-20261007T040504Z/<HÃNG> BEFORE.pdf` (`wc_data.C`); dựng lại: `run_data.py <trang>`, `wc_build.py candidate <HÃNG> <số>` (PEROTAC 12, REDPUMP 08, AQUARIS 08), `wc_qa.py PEROTAC=.. [REDPUMP=..] [AQUARIS=..]`. Còn mở nhỏ: dòng "Submersible sewage pumps with cutter"; 15 kW và 18,5 kW trang 150WC cùng Hmax 40; phớt SiC PEROTAC chưa đối chiếu hàng thật.
- **SP:** AQUARIS 9d16add3… (ứng viên 04: trang 1–2 mới, ảnh bơm mới 6/8/10 inch, bỏ bảo hành, mỗi model một màu), PEROTAC 793c4419…, REDPUMP 6db87426… (bỏ bảo hành). Biên nhận `history/sp-three-brand-accepted-20261007T065655Z`. Mã AQUARIS: `work/claude_aq_p12_20261006/{build_preview,inner_new,sp_mau,qa_candidate}.py` — LƯU Ý: `build_preview.py` còn trỏ nền dựng vào bản chính (nay đã đổi) → muốn dựng lại phải trỏ BASE/CANON sang `history/sp-three-brand-accepted-20261007T065655Z/AQUARIS BEFORE.pdf` (8170fe4d…). Dải 6SP30 REDPUMP: anh nói sửa riêng, không áp vào catalogue 13 trang; phiên cowork-0145B2… nếu đọc bản chính REDPUMP SP thì SHA nay là 6db87426… (bản trước 2face7a1… ở history).
- Thư mục đã duyệt đang có 10 tệp (SP, WC, máy khuấy ×3; định lượng AQUARIS), bản bị thay nằm trong `_BAN CU`. Định lượng + máy khuấy chưa có "bản chính" trong 25 gốc (nhóm mới).
- Bài học: không viết `#` giữa dòng nhiều lệnh `;`; mỗi lần gọi shell ≤ ~170 s; tệp chuyển từ phiên về máy có thể bị mã hóa lại → so SHA điểm ảnh; trang SP 26–27 có khổ/tỉ lệ khác (QA phải nhân hệ số); đoạn đường gần thẳng dễ dính "đổi chiều cong" giả → `concave_refine` trong `wc_curves.py`.

## 4a. Quyết định mới của anh trong phiên Claude

Đọc `claude/QUYET_DINH_ANH_20261006_PHIEN_CLAUDE.md`: PDF để đăng web/Zalo; hỏi ảnh theo từng catalogue; duyệt mẫu trước; thiếu dữ liệu hỏi theo từng nhóm; bìa/chân trang giữ cũ hoặc chỉ ghi hãng.

## 4c. Nhìn PDF thật

Xuất PNG trang cần soi vào `claude/_xem/` với **tên cố định** `xem_1.png`…`xem_8.png` (ghi đè, không tạo tên mới), `device_stage_files` rồi Read. Đã thử 06/10: xem được. 110 dpi cho cả trang, 250–300 dpi cho vùng cắt biểu đồ.

## 6. Giữ kho gọn

- Tệp nháp, ảnh soi, bản sao thử: để ở `$HOME/claude_work/<việc>` (ngoài kho, mất khi hết phiên). Chỉ ghi vào kho: ứng viên đạt, báo cáo 8 cột, phiếu QA, ảnh bằng chứng tối thiểu (vùng rủi ro, không xuất cả catalogue).
- Mỗi phiên một việc. Cuối phiên: cập nhật mục 4 của tệp này (ghi đè, không nối dài) và ghi một bàn giao ngắn `claude/BAN_GIAO_<UTC>.md` ≤2 KB; chỉ giữ 3 bàn giao mới nhất ở đây, cũ hơn đã nằm trong sổ gốc.

## 4d. Nhóm 16 Bơm định lượng JLM/JBB + nhóm 17 Máy khuấy MIX — nguồn mẫu đã nhập 06/10 ~16:05Z, CHỜ ANH CHỐT

Nguồn: `Catalog Sua\NGUON BO SUNG 20261006\`. Đã kiểm thông số, chưa sửa gì: đọc `work/claude_nguon_moi_20261006/PHIEU_KIEM_THONG_SO.md` (18 điểm định lượng, 8 điểm máy khuấy, 3 câu cần anh chốt: phạm vi hãng, các số mâu thuẫn, ảnh). Quyết định mục 19 trong `claude/QUYET_DINH_ANH_20261006_PHIEN_CLAUDE.md`. Chưa làm mẫu.

## 4e. Nhóm 16 định lượng AQUARIS + nhóm 17 máy khuấy MIX 3 hãng — ĐÃ DỰNG, kiểm độc lập ĐẠT, CHỜ ANH DUYỆT (06/10 ~16:45Z)

Thay mục 4d. Đọc `work/claude_dl_mk_20261006/BAN_GIAO.md` (tệp, SHA, việc đã làm, 6 câu chờ anh chốt) và `QA/QA_DOC_LAP.md`. PDF ở `deliverables/DINH LUONG - MAY KHUAY 20261006/`. Anh sửa thì: định lượng sửa `DINHLUONG/dl_build.py` rồi `candidate 04` (không ghi đè); máy khuấy sửa `MAYKHUAY/mk_build.py`. Quyết định mục 20–21.
- 4e cập nhật 17:10Z: định lượng nay là ỨNG VIÊN 04 (4 trang, JBB một trang); máy khuấy đã thêm Poles = 4; kiểm độc lập lượt 3 ĐẠT cả 4 tệp; quyết định mục 22–23. Chờ anh duyệt cuối; còn JLM5001 SPM + cỡ nối PVC dòng lớn cần hãng xác nhận.

## 4f. MẪU 12 nhóm (1 CM, 2 3M, 4 SS, 6 SA, 7 SL, 8 FS, 9 IRG, 10 GB, 11 KTZ–LH, 12 CDLF, 13 CDX, 14 DWO) — ĐÃ DỰNG, kiểm độc lập ĐẠT, CHỜ ANH DUYỆT (20261006T181750Z, phiên cowork-015f6Z8nKVANAKeMRK7J4HcG)

32 PDF xem thử (1 trang/hãng/nhóm) ở `deliverables/MAU 12 NHOM 20261006/`; đọc `DOC TRUOC - KET QUA VA CAU HOI.md` ở đó (bảng kết quả + câu hỏi gom cho anh). Chưa ứng viên, chưa claim, bản chính không đổi. Mã + data + báo cáo từng nhóm: `work/claude_mau12_20261006/MAU_<NHÓM>/` (phiếu kiểm ở `qa/`); thư viện dùng chung `work/claude_mau12_20261006/chung/mau_lib.py` (fit_curve có chặn gãy `smooth`, readback, contact) + hai tệp hướng dẫn AI phụ / AI kiểm — dùng lại cho đợt dựng cả bộ. Khóa MAU_* đã nhả.
- Bước tiếp khi anh duyệt nhóm nào: nhận khóa nhóm đó, áp câu trả lời của anh, dựng cả bộ từ mã mẫu (mỗi hãng một AI), BƯỚC 0, kiểm độc lập, rồi mới lưu ứng viên. KTZ dùng đường HAI cung nối trơn tại điểm định mức; GB lấy nguyên hình học đường nguồn; IRG nguồn không có đường Q–H; DWO là đường tham khảo.
- Lưu ý: `cat.py health` báo CHƯA ĐẠT ở phiên chỉ nối 2 thư mục vì thiếu mount `b-n-h-y-s-a` (missing_paths: python); BƯỚC 0 vẫn 43/43, môi trường 4/4. Rác chờ quyền xóa: `work/claude_mau12_20261006/chung/_selftest.*`, `_contact.png`, `__pycache__`; `MAU_KTZ_LH/curves*.json` (chỉ v5 dùng).

## 4g. MẪU 12 nhóm — ĐÃ ÁP 10 câu anh trả lời 07/10 (QUYET_DINH mục 25–35), kiểm độc lập lại ĐẠT (20261006T193753Z)

Anh nói: mẫu WC đã duyệt; mẫu 12 nhóm anh xem kỹ rồi trả lời sau → CHƯA dựng cả bộ. Đọc phần "CẬP NHẬT 07/10" cuối `deliverables/MAU 12 NHOM 20261006/DOC TRUOC - KET QUA VA CAU HOI.md` (đã đổi gì + 7 việc còn chờ anh) và `ANH CAN THAY - GUI ANH TRUNG.md`. Hướng dẫn áp cho AI phụ: `work/claude_mau12_20261006/chung/AP_QUYET_DINH_0710.md`. Quy tắc mới phải nhớ khi dựng cả bộ: không in bảo hành ở MỌI catalogue (WC, SP đã có ứng viên/bản chính CHƯA bỏ — việc tồn); H lẻ giữ theo nguồn; 3M ghi /3.0, /5.5; pha ≤ 3 kW có 1~ (IRG, CDLF, DWO, SA Aquaris); thứ tự công suất mục 20 — cặp nào vướng số khóa thì hỏi anh, không tự phá khóa. Không làm SL. Khóa MAU_* đã nhả. Mục 25–35 CHƯA nhập rules/ (niêm phong) — nhập ở lượt refresh kế tiếp khi không còn khóa.

## 4·6SP30. REDPUMP 6SP30 tách riêng — 07/10 02:30Z, CHỜ ANH DUYỆT BẢN XEM 02 (phiên cowork-0145B2…)

Thư mục `deliverables/SP REDPUMP 6SP30 RIENG 20261007`: BAN XEM 01 (cắt nguyên từ V3, SHA 582874ae…), **BAN XEM 02** (A4 dọc 2 trang, SHA 2283b817…), `KIEM DUONG QH 6SP30 - 20261007.md`, `build_ban_xem_02.py`. Bản 13 trang gốc (2face7a1…) và bản chính KHÔNG đổi. Đây là bản xem/mẫu, CHƯA phải ứng viên catfix.
- Anh yêu cầu 07/10: (1) kiểm đường Q–H khớp điểm bảng chưa; (2) làm biểu đồ hiệu suất như mẫu 50 MS, hiệu suất bơm 68%; (3) thêm logo Redpump cuối trang.
- Kết quả đo: hai đầu đường trùng bảng; mốc giữa lệch tới 4,3% (trong ≤5%), cao hơn bảng ở Q12–18, thấp hơn ở Q30. Đường η V3 đỉnh 70,7% tại Q≈28,8 → bản 02 co về 68% (×0,9617), vẽ khung η riêng 0–80%, một đường chung cho cả dải.
- CHỜ ANH: (a) η một đường chung hay 19 đường riêng (cần số từng model); (b) xử lý lệch Q–H: giữ ≤5% / sửa số bảng theo đường (ghi cũ→mới) / ép đường qua đúng điểm (sẽ gợn); (c) vị trí logo.
- Lưu ý kỹ thuật: bản 02 ghép bằng pikepdf+reportlab trên đám mây vì shell trên máy anh không khởi động được (07/10 ~02:10Z) nên CHƯA chạy được `dau_phien.sh` 43/43; trang gốc nhúng nguyên làm Form nên chữ ẩn của 6SP18 vẫn còn trong tệp. Khi anh duyệt: chạy 43/43, dựng ứng viên sạch qua catfix. Khóa `SP_REDPUMP_6SP30` phiên này đang giữ.
- **BẢN XEM 03 (07/10 ~03:00Z, SHA c0be3668…):** anh chốt hiệu suất MỖI MODEL MỘT ĐƯỜNG (19 đường, khác màu, có nhãn), thiết kế theo mẫu 50 MS. Cách tính: η = Q×H/(367×P2)×0,9444 (H lấy từ đường Q–H trong PDF, P2 định mức; hệ số để model cao nhất 6SP30-35 = 68%). Đỉnh từng model 51,1–68,0% (bảng trong tệp KIEM). `build_ban_xem_03.py`. Shell máy anh đã chạy lại. CHỜ ANH: duyệt cách tính/giao diện; câu (b) lệch Q–H và (c) logo vẫn mở; câu (a) đã đóng.
- **BẢN XEM 05 (07/10 ~04:00Z, SHA 486355b6…) — bản hiện hành, thay 03/04:** anh chốt (1) hiệu suất mọi bơm trong khoảng 66–72%; (2) dải 6SP30 Redpump CHỈ làm đến 11 kW, bỏ hết model lớn hơn → còn 9 model 6SP30-2…-13. Bản 05: vẽ lại biểu đồ Q–H trục 0–160 m (9 đường, toạ độ đúng như V3), η 9 đường chia đều 66,0→72,0% theo thứ tự model (hình dạng lấy từ đường η gốc của catalogue), trục η 40–75% cho khỏi rít; trang 2 có 9 biểu đồ η nhỏ riêng từng model + bảng kích thước 9 dòng. Bảng số cắt từ trang gốc (9 dòng đầu). `build_ban_xem_05.py`. CHỜ ANH: chọn kiểu vẽ η (một khung trục 40–75 hay 9 khung nhỏ), lệch Q–H ≤4,3%, vị trí logo. Chưa phải ứng viên catfix; chưa chạy 43/43.
- **BẢN XEM 07 (07/10 ~05:00Z, SHA 133de513…) — bản hiện hành, thay 05:** anh đổi: (1) dải 6SP30 Redpump làm từ **4 kW đến 15 kW** → 9 model 6SP30-4…-17 (thay lệnh "đến 11 kW"); (2) biểu đồ hiệu suất vẽ **η theo cột áp H** (trục ngang H 0–200 m), không phải η–Q. Bản 07: Q–H trục 0–200 m (toạ độ như V3); η–H 9 đường tách hẳn, đỉnh chia đều 66,0→72,0% theo thứ tự model, hình dạng lấy từ đường η gốc; bảng số và bảng kích thước cắt 9 dòng từ trang gốc. `build_ban_xem_07.py`. CHỜ ANH duyệt; lệch Q–H ≤4,3% và vị trí logo vẫn mở. Chưa phải ứng viên catfix; chưa chạy 43/43.
- **BẢN XEM 08 (07/10 ~06:00Z, SHA 52768bdd…) — bản hiện hành, thay 07:** anh bảo tra mạng xem "model thấp hiệu suất thấp" có đúng không rồi làm lại. Kết quả tra: đúng hướng nhưng chênh nhỏ và chỉ rõ ở bơm 1–3 tầng (Berkeley/Pentair: 1 tầng −2,5; 2 tầng −1; 3 tầng −0,5; từ 4 tầng 0. Kansas State L886: 1 tầng −4; 3 tầng 0; 6 tầng +1). Số sau mã 6SP30 = số tầng (H0/tầng ≈11,4 m, đo từ bảng). Bản 08 đổi cách chia đỉnh: η = 72,3 − 12,6/số tầng, neo 2 tầng = 66% và 42 tầng = 72% → 9 model 4–15 kW: 69,1 / 69,8 / 70,2 / 70,5 / 70,7 / 71,0 / 71,3 / 71,5 / 71,6. Còn lại như bản 07 (η theo cột áp). `build_ban_xem_08.py`. CHỜ ANH duyệt.
- **BẢN XEM 09 (07/10 ~07:00Z, SHA a5c62dd5…) — bản hiện hành, thay 08:** anh chốt hiệu suất **khoảng 68% cho mọi model** và hỏi cách vẽ η theo cột áp có đúng không. Tra: chuẩn ngành là η theo LƯU LƯỢNG, một đường chung cho cả dải (Grundfos ecademy: head/power/efficiency/NPSH "as a function of the flow", ISO 9906; Pedrollo 6SR và Lowara Z6: một đường η theo Q cho cả họ; Pedrollo 6SR27 đỉnh 69%, 6SR36 72%). η theo cột áp không thấy catalogue nào dùng. Bản 09: trang 1 = chuẩn (η–Q một đường đỉnh 68%, em đề xuất); trang 2 = η–H 9 đường đều đỉnh 68% (để anh so); trang 3 = kích thước. 9 model 4–15 kW. `build_ban_xem_09.py`. CHỜ ANH chọn trang 1 hay trang 2; lệch Q–H ≤4,3% vẫn mở.
- **BẢN 10A + 10B (07/10 ~08:00Z) — hiện hành, thay 09:** anh bảo cho 2 bản đều vẽ η theo LƯU LƯỢNG: **10A** một đường chung đỉnh 68% (SHA 0b51e1a7…); **10B** mỗi model một đường (SHA a53a0921…), đỉnh em chia đều 67,0→69,0 theo thứ tự model (quanh 68%), trục η cắt 50–70% để tách đường. Bỏ phương án η theo cột áp. 9 model 4–15 kW; mỗi tệp 2 trang (trang 2 = kích thước). `build_ban_xem_10.py Q|M <tệp ra>`. CHỜ ANH chọn 10A hay 10B; lệch Q–H ≤4,3% vẫn mở.

## 4h. MẪU 11 nhóm — LÀM LẠI theo 23 câu anh trả lời lượt 2 + nguồn mới CDX/DWO + màu đường AQUARIS; kiểm độc lập ĐẠT (20261007T035635Z)

Giao diện 11 nhóm anh ĐÃ DUYỆT (mục 40) → bước tiếp là dựng cả bộ, nhưng còn 10 mục chờ anh: đọc phần "CẬP NHẬT 07/10 LƯỢT 2" cuối `deliverables/MAU 12 NHOM 20261006/DOC TRUOC - KET QUA VA CAU HOI.md`. Quy tắc mới: AQUARIS mỗi model một màu đường (`chung/aq_palette.py`, mục 52); CDX và DWO lấy số ở `Catalog Sua\NGUON BO SUNG 20261007\` (không dùng logo/ảnh/chữ của hãng nguồn); IRG chỉ giữ họ (I), tên IRG<DN>-<cánh>/<kW>; DWO hậu tố T = 3 pha, M = 1 pha.
- ẢNH: anh gửi ảnh từng catalogue trong chat, lưu nguyên bản ở `Catalog Sua\NGUON BO SUNG 20261007\ANH ANH GUI\<NHÓM> - <HÃNG>.png` (đã có CM AQUARIS, CM PEROTAC, 3M PEROTAC, 3M AQUARIS). CHỜ anh báo "xong" mới thay; khi thay: xóa logo in trên ảnh, cắt/căn cho đẹp (mục 53).
- VIỆC ANH ĐÃ DUYỆT, CHƯA LÀM (mục 36–39): WC — bỏ bảo hành + AQUARIS mỗi model một màu → ứng viên mới → kiểm → chép bản chính; SP — bỏ bảo hành, AQUARIS trang 1–2 mới (bỏ dòng bảo hành 2 năm trên bìa), màu đường AQUARIS; định lượng + máy khuấy — nhận bản. Cần mount `b-n-h-y-s-a` để `cat.py health` đạt trước khi ghi bản chính.
- Khóa MAU_* đã nhả. Mục 25–53 CHƯA nhập rules/.


## 4i. MẪU — ÁP 15 câu anh trả lời lượt 3 (QUYET_DINH mục 54–60) cho IRG, DWO, CDX, CM, FS; kiểm độc lập ĐẠT trừ DWO thứ tự công suất (20261007T045709Z)

Đọc phần "CẬP NHẬT 07/10 LƯỢT 3" cuối `deliverables/MAU 12 NHOM 20261006/DOC TRUOC - KET QUA VA CAU HOI.md` (bảng đổi + SHA + 8 mục chờ anh). Phiếu: `work/claude_mau12_20261006/MAU_<NHÓM>/qa/PHIEU_QA_DOC_LAP_LUOT3.md`.
- IRG 11 model (bỏ trùng tên bé hơn); DWO 7 cỡ (037, 100, 150, 200, 300, 400 đủ T+M; 550T); CDX tên liền + CDXM200/25 + trang 2 kích thước (sơ đồ tự vẽ, không chép hình nguồn); CM AQUARIS /3 lấy số PEROTAC, bỏ cột A và n; FS khổ ngang bỏ mọi cỡ họng xả.
- CHẶN: DWO037/DWO100 theo số khóa Hmax 12 trái thứ tự công suất với DWO150 (3 cặp) — chờ anh chọn giữ/đổi/cho số thật; chưa được dựng cả bộ DWO trước khi anh chốt.
- Quy tắc anh chốt dùng khi dựng cả bộ: IRG mọi cỡ họng chỉ giữ họ (I), trùng tên sau khi đổi /kW thì giữ model Q/H lớn hơn, số nguyên ghi "/3"; CDX 3 pha "CDX90/10", 1 pha "CDXM90/10", mọi model đủ hai pha; DWO mọi cỡ ≤ 3 kW đủ T và M; FS bỏ cả cỡ ren.
- Chưa làm: thay ảnh (chờ anh báo gửi xong); SA AQUARIS bản chính 298→293, 87→89 (mục 60; cần claim + catfix); dựng cả bộ 11 nhóm; nhập mục 25–60 vào rules/. WC, SP 6SP30 do phiên khác làm — không đụng.
- Khóa MAU_CM, MAU_FS, MAU_IRG, MAU_CDX, MAU_DWO đã nhả.


## 4j. MẪU — ÁP 6 câu anh trả lời lượt 4 (QUYET_DINH mục 61–66) cho DWO, CM; kiểm độc lập ĐẠT (20261007T054700Z)
- DWO: giữ số khóa DWO037/DWO100 (ngoại lệ thứ tự công suất anh chốt, mục 61) → DWO hết bị chặn; họng 1"1/4. CM AQUARIS: cánh bơm ghi như PEROTAC. IRG 4 cực: đuôi "-4" (IRG80-160/11-4).
- CHỜ ANH: ô "*" (hỏi lại rõ); phương án giảm số CM 32-200/4 ở Q 21–27 (PA1/PA2 trong DOC TRUOC phần LƯỢT 4) — CHƯA sửa số.
- Khóa MAU_DWO, MAU_CM đã nhả. SHA mới xem DOC TRUOC phần LƯỢT 4.


## 4k. MẪU — ÁP 3 câu anh trả lời lượt 5 (QUYET_DINH mục 67–69) cho DWO, CDX, CM; kiểm độc lập ĐẠT (20261007T062428Z)
- DWO, CDX: bỏ hẳn dòng điện (A), hết ô "*"; CDXM200/25 = như CDX200/25. CM 32-200/4: Q 24 = 33, Q 27 = 28 ở cả ba hãng (bản chính CM chưa đổi — áp khi dựng cả bộ).
- CHỜ ANH: có bỏ cột dòng điện ở các nhóm khác không (chưa hỏi được rõ); ảnh. Sau đó dựng cả bộ 11 nhóm.
- Khóa MAU_DWO, MAU_CDX, MAU_CM đã nhả. SHA mới xem DOC TRUOC phần LƯỢT 5.


## 4l. MẪU — lượt 6: anh ĐỔI Ý, GIỮ dòng điện (A) mọi catalogue; mã thiếu số thì điền số suy ra từ các mã có nguồn (QUYET_DINH mục 70 thay 67); DWO, CDX kiểm độc lập ĐẠT (20261007T064612Z)
- Quy tắc dùng khi dựng cả bộ: ô dòng điện không có nguồn → đường thẳng bình phương tối thiểu I = a + b·P2 trên các mã có số nguồn cùng catalogue, cùng pha; làm tròn 0,1 A; kiểm tăng theo kW; ghi trong báo cáo là số suy ra. DWO 7 ô, CDX 1 ô (xem DOC TRUOC phần LƯỢT 6).
- Mẫu 11 nhóm hiện không còn câu hỏi chặn. CHỜ ANH: báo gửi xong ảnh → thay ảnh → dựng cả bộ (việc lớn: trình phương án trước).
- Khóa MAU_DWO, MAU_CDX đã nhả.

## 4f. Nhóm 18 Đĩa phân phối khí DN270 + DN128 (PEROTAC, REDPUMP) — ỨNG VIÊN 03, kiểm độc lập ĐẠT, CHỜ ANH DUYỆT (07/10 ~07:00Z)

Đọc `work/claude_dia_20261007/BAN_GIAO.md` (tệp, SHA, ánh xạ nguồn, 3 mâu thuẫn trong mẫu chờ anh quyết) và `QA/QA_DOC_LAP.md`. PDF ở `deliverables/DIA PHAN PHOI KHI 20261007/`. Sửa thì đổi `dia_lib.py`/`dia_pages.py` rồi `dia_build.py giao 04`. Quyết định mục 24–25.

## 4·4MIX. Máy khuấy chìm 4MIX toàn thân inox, 3 hãng — ANH ĐÃ DUYỆT, đã lưu thư mục đã duyệt (20261007T065946Z, phiên cowork-01TM6dfcKzom)
Anh nói "khuấy ok rồi lưu vào". Đã chép đúng byte vào `Catalog Sua\CATALOGUE DA DUYET\<HÃNG>\<HÃNG> - Máy khuấy chìm 4MIX.pdf` (PEROTAC be225809…, REDPUMP 8bb05707…, AQUARIS e79c3332…), DANH SACH.txt đã cập nhật. Nguồn dựng: `work/claude_4mix_20261007/mix4_build.py`, báo cáo `BAO_CAO.md`. Mác SUS304 coi như anh nhận theo bản duyệt (anh không trả lời riêng). Chưa kiểm bản in. Rác chờ quyền xóa: `work/claude_4mix_20261007/zz_scratch_zoom_docl.png`.
- 4f cập nhật 20261007T070318Z: đĩa phân phối khí đã chép vào `Catalog Sua\CATALOGUE DA DUYET\PEROTAC|REDPUMP\<HÃNG> - Đĩa phân phối khí DN270-DN128.pdf` (đúng byte ứng viên 03), DANH SACH.txt đã cập nhật. Lưu ý cho mọi phiên: anh nói "lưu vào" = chép vào CATALOGUE DA DUYET (không chỉ thư mục bản chính).


## 4m. THAY ẢNH 4 trang mẫu (CM, 3M: PEROTAC + AQUARIS) + NHẬN BẢN CHÍNH SA AQUARIS 2 ô (20261007T071553Z)
- Ảnh: xem DOC TRUOC phần "THAY ẢNH". Còn chờ anh gửi ảnh các nhóm khác + ảnh 3M PEROTAC lớn hơn + ảnh REDPUMP cho CM, 3M.
- SA AQUARIS bản chính `Giếng/Aquaris bơm giếng SA 1_300dpi_75% (bản mới).pdf`: 1f800916… → 1f8c12b2… (catfix outline_replace 2 ô trang 5; kiểm độc lập ĐẠT; sao lưu + biên nhận `history/sa-aquaris-2-o-accepted-20261007T071404Z`; inventory làm mới `history/inventory-20261007T071516Z-f5c91955.json`; health ĐẠT; claim + khóa đã nhả). Không chép vào CATALOGUE DA DUYET (bản cũ chỉ sửa 2 ô).
- Cách chạy làm mới kiểm kê trên Linux: bọc `tools/refresh_index.py` như `claude/cat.py` (nạp tools/catalogue.py dưới tên `catalogue`, dịch `paths` theo `claude/paths_linux.json`, argv `--actor ROOT --reason ...`); phải nối thêm thư mục `C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a` thì health mới ĐẠT.
- Mục 50 (tra ảnh AI đã tạo trong dự án báo cáo công ty): CHƯA làm được — phiên không nối thư mục dự án đó; mục 53 đã thay bằng cách anh gửi ảnh.
- VIỆC LỚN CHƯA LÀM: dựng cả bộ 11 nhóm (31 PDF) theo mẫu đã duyệt — chờ anh duyệt phương án. Mục 25–70 chưa nhập rules/ (đang có phiên khác giữ khóa).


## 4n. MẪU IRG V5 — BỎ đường đặc tính (QUYET_DINH mục 71–72), kiểm độc lập ĐẠT, CHỜ ANH DUYỆT (20261007T075050Z)
- Mã: `work/claude_mau12_20261006/MAU_IRG/irg_mau_v5.py` (nhập lại irg_mau.py, chỉ đổi bố trí; điều phối tự làm vì AI phụ IRG đã bị dừng). Logo REDPUMP/AQUARIS nay lấy từ mẫu GB đã giao vì bản chính WC đã đổi (xref cũ sai) — các mã mẫu khác còn trỏ xref logo vào bản chính WC cũng sẽ lỗi khi dựng lại: sửa như vậy.
- Tệp AQUARIS mới mang tên `IRG - AQUARIS - MAU (BAN MOI khong duong dac tinh).pdf` vì tệp cũ đang bị mở trên máy anh; khi ghi đè được thì gộp về tên chuẩn.
- Anh xác nhận hướng chung: khi dựng đầy đủ thì thêm trang bìa + chi tiết cấu tạo – vật liệu (có thể ở đầu catalogue) theo mẫu/nguồn anh đưa. Phương án dựng cả bộ 3 đợt: anh CHƯA trả lời.
- Khóa MAU_IRG đã nhả.
- **BẢN 11B (07/10 ~09:00Z, SHA 24b0bd67…) — thay 10B:** anh bảo bản nhiều đường phải vẽ trục hiệu suất TỪ 0 mới chuẩn. Bản 11B: η–Q 9 đường, trục 0–70%, đường đi từ gốc 0; đỉnh vẫn 67,0→69,0 (quanh 68%); thu trang còn 1,1 lần để khung η cao 245 pt. Hệ quả đã báo anh: vẽ từ 0 thì 9 đường sát nhau (cách ~0,9 pt ở đỉnh, chập ở hai sườn); muốn tách hơn phải nới khoảng đỉnh (vd 66–70) — CHỜ ANH. Bản 10A (một đường) giữ nguyên. `build_ban_xem_11.py M <tệp ra>`.
- **BẢN 12 (07/10 ~10:00Z, SHA 1db78d4d…):** anh báo "catalogue ok rồi" (bản 11B: nhiều đường η–Q, trục từ 0, 9 model 4–15 kW) và bảo kẻ điểm làm việc cho 6SP30-5 tại Q = 27 m³/h, kẻ lưu lượng thẳng lên rồi dóng ngang sang hiệu suất, hiệu suất ≥66%. Bản 12 = 11B + đường kẻ đỏ nét đứt ở cả hai biểu đồ: H = 40,9 m, η = 67,1% (đọc từ đường của 6SP30-5, đỉnh 67,3%). `build_ban_xem_12.py M <tệp ra>`. Chưa phải ứng viên catfix; lệch Q–H ≤4,3% vẫn mở.
- **BẢN 13 (07/10 ~10:30Z, SHA a44ea4ca…) — thay 12:** anh bảo thêm một đường kẻ tại 25 m³/h. Bản 13 = 11B + hai điểm làm việc của 6SP30-5: Q 25 → H 42,9 m, η 66,3%; Q 27 → H 40,9 m, η 67,1%. `build_ban_xem_13.py M <tệp ra>`.
- **BẢN 15 (07/10 ~11:00Z, SHA ec128468…) — thay 13:** anh thêm điểm 20 và 23 m³/h (6SP30-5) và 33 m³/h (6SP30-7). Bản 15 = 11B + 5 điểm làm việc, đổi nhãn từng điểm thành một bảng nhỏ trong mỗi biểu đồ: 6SP30-5 Q20 → H 47,4 / η 60,6; Q23 → 44,8 / 64,6; Q25 → 42,9 / 66,3; Q27 → 40,9 / 67,1; 6SP30-7 Q33 → 46,0 / 66,7. Danh sách điểm ở biến PTS trong `build_ban_xem_15.py M <tệp ra>`.
- **BẢN 16 (07/10 ~11:40Z, SHA ad416b37…) — MẪU CHỜ ANH DUYỆT, chưa thay bản 15:** anh hỏi vẽ lại cho mọi điểm hiệu suất đều trên 65% được không. Làm được bằng cách nâng đỉnh cả 9 model thêm 4,9 điểm, giữ nguyên hình dạng đường: đỉnh 71,9 (-4) → 73,9 (-17), 6SP30-5 = 72,2; trục η 0–80. 5 điểm: 65,1 / 69,4 / 71,1 / 72,0 (6SP30-5 tại Q 20/23/25/27) và 71,5 (6SP30-7 tại Q 33). Đã báo anh: việc này đổi số đỉnh của catalogue anh đã duyệt (quanh 68%) và chưa có số thử máy; phương án làm bẹt đường (giữ đỉnh 68) em không khuyên. `build_ban_xem_16.py M <tệp ra>`.


## 4o. DỰNG CẢ BỘ 11 NHÓM — XONG, kiểm độc lập ĐẠT, ĐÃ LƯU 32 tệp vào `Catalog Sua\CATALOGUE DA DUYET` (20261007T184046Z; QUYET_DINH mục 73–90)
- Ứng viên cuối trong `work/claude_bo_20261007/<NHÓM>/UNG VIEN 0x/` (CM 03; 3M, SS, FS, IRG, GB, KTZ_LH, CDLF, CDX, DWO 02; SA 03); phiếu `…/<NHÓM>/qa/PHIEU_QA_DOC_LAP*.md` (DWO: `PHIEU_QA_DIEU_PHOI_UV02.md` — AI kiểm DWO bị anh dừng nên điều phối tự kiểm). SHA + tên tệp đã lưu: `work/claude_bo_20261007/BIEN_NHAN_LUU_DA_DUYET_20261007T184046Z.json`, `CATALOGUE DA DUYET\DANH SACH.txt`.
- CHƯA thay bản chính trong `BẢN MỚI 03-10-2026 (ChatGPT)`: cố ý hoãn — mã dựng của 11 nhóm còn đọc nguồn/ảnh/logo từ các tệp đó (thay là hỏng dựng lại, như lỗi logo WC), và anh còn câu chưa trả lời. Khi anh chốt hết: claim từng tệp gốc, sao lưu history/, ghi đúng byte, refresh inventory (cách bọc ở mục 4m), health.
- Hướng dẫn dùng lại: `chung/DUNG_CA_BO_0710.md` (dựng), `chung/KIEM_CA_BO_0710.md` (kiểm). AI phụ IRG mới: ab4c43320b7b4e034.
- Câu còn chờ anh: `claude/CAU_HOI_CHO_ANH_20261008.md`. Ảnh SS xóa phao (`work/claude_bo_20261007/SS/anh/`) chờ anh duyệt.
- Khóa BO_* đã nhả. Mục 25–90 chưa nhập rules/.

## 4p. LƯỢT 11 — viết lại tiếng Anh + việc riêng; ĐÃ THAY BẢN CHÍNH BẢN MỚI 03-10 và CATALOGUE DA DUYET (20261008T010555Z; QUYET_DINH mục 91)
- Bản cuối: CM UV05, 3M UV03, SS UV03, SA UV04, FS UV03, IRG UV03, GB UV05, KTZ_LH UV04, CDLF UV03, CDX UV03, DWO "UNG VIEN 03 - 1 TRANG" và "- 2 TRANG" trong `work/claude_bo_20261007/`. SHA từng tệp: `history/bo-11-nhom-luot11-accepted-20261008T010555Z/BIEN_NHAN.json`.
- BẢN MỚI 03-10: 16 bản chính cũ đã thay (bản cũ nằm trong thư mục history trên, tên "<HÃNG> <NHÓM> BEFORE - …"), 13 tệp PDF mới cho hãng trước chưa có (3M/SA/IRG/GB/CDLF/CDX Redpump; IRG/GB/KTZ/CDX Aquaris; SS 3 hãng). DWO CHƯA đưa vào BẢN MỚI 03-10: chờ anh chọn bản 1 trang hay 2 trang. Excel SS/DWO và Redpump SL không đụng.
- CATALOGUE DA DUYET: 35 tệp (DWO có 2 bản mỗi hãng), 32 tệp cũ sang `_BAN CU`.
- LƯU Ý DỰNG LẠI: mã dựng từng nhóm đọc logo/ảnh/số từ bản chính CŨ → trước khi chạy lại phải trỏ về tệp BEFORE trong history hoặc nguồn 01-10. Tên trong danh mục của 2 bản CM PEROTAC/REDPUMP là "…trục ngnag…" (lỗi gõ của nguồn) — claim phải dùng tên đó.
- Inventory: `history/inventory-20261008T010613Z-70814863.json` (25 catalogue gốc; 13 tệp mới không nằm trong danh mục 25). health ĐẠT; khóa cat đã nhả; khóa BO_* đã nhả.
- Kiểm: `work/claude_bo_20261007/QA_DIEU_PHOI_LUOT11.md`, `KIEM_NGU_PHAP_DOC_LAP_L11.md`. In giấy CHƯA KIỂM.
- Còn chờ anh: `claude/CAU_HOI_CHO_ANH_20261008.md` (bản cập nhật). Việc sau: nhập QUYET_DINH mục 25–91 vào rules/ khi không phiên nào giữ khóa.

## 4q. LƯỢT 12 — KTZ "up to 15 kW" + DWO hai bản vào BẢN MỚI 03-10 (20261008T012502Z; QUYET_DINH mục 92)
- KTZ_LH bản cuối = UNG VIEN 05 (PEROTAC ad59e2d4a7af, REDPUMP 9e572914f911, AQUARIS 01e2647e699b): chỉ đổi "below 15 kW" → "up to 15 kW" trang 1; đã thay bản chính + CATALOGUE DA DUYET (bản 04 sang _BAN CU).
- DWO: 6 PDF mới trong `BẢN MỚI 03-10\Trục ngang\DWO <Hãng> - bản 1 trang|2 trang (bản mới).pdf`; anh tự chọn, chưa bỏ bản nào.
- Biên nhận `history/bo-11-nhom-luot12-accepted-20261008T012502Z/BIEN_NHAN.json`; inventory `history/inventory-20261008T012517Z-901c07d9.json`; health ĐẠT; không còn khóa của phiên này.
- Đang chờ anh trả lời 5 câu hỏi lại (xem `claude/CAU_HOI_CHO_ANH_20261008.md`). CM AQUARIS giữ tiếng Ý; 3M giữ câu inox 304; FS hai dòng phớt khác nhau là đúng.

## 4r. LƯỢT 13 — SS thêm dòng phớt đặc biệt; CM AQUARIS bỏ CM 32-125/0.7 và /1.1 (20261008T015320Z; QUYET_DINH mục 93)
- SS bản cuối = UNG VIEN 04 (PEROTAC e0ab97f296b8, REDPUMP 35ece03286a4, AQUARIS 10c1e2107ba4). CM bản cuối = UNG VIEN 06 (AQUARIS 8432ec866df5, 66 model, 11 trang; PEROTAC/REDPUMP như UV05).
- Đã thay bản chính + CATALOGUE DA DUYET (bản trước sang _BAN CU). Biên nhận `history/bo-11-nhom-luot13-accepted-20261008T015320Z/BIEN_NHAN.json`; inventory `history/inventory-20261008T015324Z-ffd38b4b.json`; health ĐẠT; không còn khóa của phiên này.
- Hết câu hỏi mở của bộ 11 nhóm, trừ: anh chọn bản DWO 1 trang hay 2 trang; anh xác nhận cách hiểu "xóa 3 mã" = bỏ hai model CM 32-125 ở AQUARIS. GB giữ tên dòng, CDX giữ Features, REDPUMP dùng chung ảnh PEROTAC.

## 4s. LƯỢT 14 — anh xác nhận (QUYET_DINH mục 94): CM AQUARIS bỏ hai model 32-125 là đúng; DWO giữ cả hai bản 1 trang và 2 trang. Không đổi tệp. Bộ 11 nhóm không còn câu hỏi mở; còn lại: in giấy chưa kiểm, nhập QUYET_DINH 25–94 vào rules/.

## 4t. CÁCH LÀM MỚI (QUYET_DINH mục 95): anh nhắn lỗi → chỉ ghi vào `claude/LOI_ANH_BAO.md`, không sửa; anh bảo "sửa" thì sửa một lượt tất cả lỗi đang MỞ.

## 4u. 2CDX — catalogue MỚI ba hãng, ỨNG VIÊN 02 chờ anh duyệt (20261008T033050Z; QUYET_DINH mục 96)
- Mã: `work/claude_2cdx_20261008` (d2_data.py → data.json; _mk.py sinh d2_trang.py từ cdx_trang23.py; d2_bo.py [luu] "UNG VIEN 0x"). 11 model, 2 trang/hãng. Bản giao: `deliverables/2CDX BA HANG 20261008`. Phiếu: `work/claude_2cdx_20261008/PHIEU_QA_2CDX_UV02.md`.
- SHA: PEROTAC 2553ee8a1c29, REDPUMP 31c51ead9250, AQUARIS 2febca607c92. Kiểm độc lập số: 0 sai/1.166 ô.
- CHƯA chép vào CATALOGUE DA DUYET / BẢN MỚI 03-10 (chờ anh duyệt). Chờ anh trả lời 3 câu: bản 1 pha cho 120/30, 120/40, 200/30, 200/40; dòng "110 °C for H version"; nhãn pha H3/H4.

## 4v. 2CDX — ỨNG VIÊN 03 ĐÃ CHÉP vào CATALOGUE DA DUYET (20261008T033855Z; QUYET_DINH mục 97)
- Thêm 4 mã 1 pha (dòng điện suy ra), 110 °C mọi mã. SHA: PEROTAC 705aa97fd359, REDPUMP b388312451b2, AQUARIS d133cd244b1e. Tệp: `CATALOGUE DA DUYET\<HÃNG>\<HÃNG> - Bơm trục ngang 2CDX.pdf`; DANH SACH.txt đã thêm 3 dòng. Phiếu `work/claude_2cdx_20261008/PHIEU_QA_2CDX_UV03.md`.
- Anh ĐÃ DUYỆT bản này (QUYET_DINH mục 98). CHƯA đưa vào BẢN MỚI 03-10 (anh chưa bảo). In giấy chưa kiểm. Khóa BO_2CDX đã nhả.

## 4w. MHI / IVT-MHI — catalogue MỚI ba hãng, ỨNG VIÊN 03 chờ anh duyệt (20261008T041101Z; QUYET_DINH mục 99)
- Mã: `work/claude_mhi_20261008` (mhi_doc.py số hóa nét mẫu → duong_nguon.json; mhi_data.py → data.json; mhi_bo.py [luu] "UNG VIEN 0x"). 17 model MHI + 14 cụm IVT-MHI, 3 trang/hãng. Bản giao `deliverables/MHI BA HANG 20261008`; phiếu `work/claude_mhi_20261008/PHIEU_QA_MHI_UV03.md`.
- SHA: PEROTAC 81e072ac170d, REDPUMP b24fa9b9ef52, AQUARIS 653f20fae4bb. Kiểm độc lập: bảng 0 sai; đường cong ĐẠT.
- CHƯA chép vào CATALOGUE DA DUYET / BẢN MỚI 03-10. Chờ anh: duyệt; đường cong vẽ theo bảng (bảng và nét mẫu lệch nhau); MHI-805 điểm định mức 31 m; các mã chỉ 3 pha.

## 4x. MHI / IVT-MHI — ỨNG VIÊN 03 anh ĐÃ DUYỆT, đã chép CATALOGUE DA DUYET (20261008T041958Z; QUYET_DINH mục 100)
- Tệp: `CATALOGUE DA DUYET\<HÃNG>\<HÃNG> - Bơm trục ngang MHI.pdf`; DANH SACH.txt thêm 3 dòng (bản trước lưu ở work/claude_mhi_20261008). CHƯA đưa vào BẢN MỚI 03-10. In giấy chưa kiểm.
- Còn mở (anh chưa trả lời): MHI-805 định mức 31 m; ghi chú 805/1602–1604 chỉ 3 pha. Khóa BO_MHI đã nhả.

## 4g. QXN40-60 — PEROTAC ỨNG VIÊN 06 + AQUARIS ỨNG VIÊN 03 (11 kW / 15 HP theo lệnh anh, còn lại giữ), kiểm độc lập ĐẠT, CHỜ ANH DUYỆT (08/10)
Đọc `work/claude_qxn_20261008/BAN_GIAO.md`. Anh duyệt ("ok rồi lưu vào") thì chép đúng byte vào `Catalog Sua\CATALOGUE DA DUYET\PEROTAC\PEROTAC - Bơm chìm QXN40-60.pdf` và `...\AQUARIS\AQUARIS - Bơm chìm QXN40-60.pdf` + cập nhật DANH SACH.txt. Quyết định mục 26 (anh thêm AQUARIS 08/10).

## 4u-L15. LƯỢT 15 — sửa 4 lỗi anh báo + rà soát toàn bộ, ĐÃ THAY bản chính + CATALOGUE DA DUYET (20261008T053327Z; QUYET_DINH mục 96)
- Rà soát (chỉ đọc) 4 AI: số + chữ toàn bộ (work/claude_bo_20261007/RA_SOAT_LOI_SO_CHU_L15.md), hình 3 hãng (work/claude_bo_20261007/RA_SOAT_HINH/<HÃNG>/BAO_CAO.md).
- Bản cuối: CM UV08, 3M UV04, CDX UV05, DWO UV04 (1 + 2 trang), CDLF UV04, GB UV06, IRG UV04 (work/claude_bo_20261007/); SP work/claude_sp_l15_20261008/UNG VIEN 01; WC + MIX + 4MIX work/claude_wc_mix_l15_20261008/UNG VIEN 01.
- Kiểm: script so bản đã duyệt ↔ mới (diff_l15.py, trong2.py: 0 ô trống giữa dãy, 0 dòng tăng ngược ở CM/3M); AI khác kiểm độc lập 9/9 mục ĐẠT (work/claude_bo_20261007/KIEM_L15/PHIEU_KIEM_DOC_LAP_L15.md).
- Bản chính: 29 tệp thay (sao lưu + BIEN_NHAN history/bo-11-nhom-luot15-accepted-20261008T053327Z/); SP AQUARIS bản chính đúng là "Giếng/G02 (gồm cả G01)/…" (không phải tệp cùng tên ở cấp Giếng). MIX/4MIX không có bản chính PDF → chỉ CATALOGUE DA DUYET. Inventory history/inventory-20261008T053407Z-4d7a10d8.json; health ĐẠT.
- Không đụng: dải 6SP30 REDPUMP (khoá phiên khác — biểu đồ 6SP30 REDPUMP vẫn lệch, nhãn 6SP30-5/-6 ngoài trục); MHI, 2CDX, QXN (phiên khác).
- Chờ anh: claude/CAU_HOI_CHO_ANH_20261008.md.

## 4v-L16. LƯỢT 16 — áp 10 câu anh trả lời + bỏ khối lượng mọi catalogue; ĐÃ THAY bản chính + CATALOGUE DA DUYET (20261008T064928Z; QUYET_DINH mục 102)
- Bản cuối: CM UV09, 3M UV05, SS UV05, SA UV05, FS UV04, GB UV07, KTZ_LH UV06, CDLF UV05, CDX UV06 (work/claude_bo_20261007/); SP UV03 (work/claude_sp_l15_20261008/); WC AQUARIS UV02, ĐĨA UV02, MIX/4MIX UV03 (work/claude_wc_mix_l15_20261008/).
- Kiểm: diff_l16.py (số chỉ mất kg/đổi đúng chỗ); AI khác kiểm độc lập 9/9 ĐẠT (work/claude_bo_20261007/KIEM_L16/PHIEU_KIEM_DOC_LAP_L16.md); sau đó sửa thêm SP AQUARIS bỏ NSK 18 chỗ + vẽ sát 3SP1-40, MIX/4MIX "High quality".
- Bản chính: 31 tệp thay (history/bo-11-nhom-luot16-accepted-20261008T064928Z/); MIX/4MIX chỉ CATALOGUE DA DUYET. Inventory history/inventory-20261008T064955Z-88111d6e.json; health ĐẠT; khoá nhả.
- CÒN: 2CDX (phiên khác làm, cả 3 hãng tr.2) còn khối lượng → phiên làm 2CDX phải bỏ theo QUYET_DINH 102.6; dải 6SP30 REDPUMP (khoá phiên khác) còn khối lượng; MHI chưa rà. 3M 40-200/11.0 cột n = 235 theo nguồn (các mã f ≥ 584 khác 278) — chờ anh.

## 4w-L17. LƯỢT 17 — 2CDX + 6SP30 REDPUMP bỏ khối lượng (20261008T070501Z; QUYET_DINH mục 103)
- SP REDPUMP UV04 (work/claude_sp_l15_20261008/UNG VIEN 04, adb8e5da02f6): tr.6 căn 6SP30 thẳng 6SP18 + nhãn không ra khung; tr.9 bỏ khối lượng 6SP30. Đã thay bản chính "Giếng/Redpump bơm giếng SP (bản mới).pdf" + CATALOGUE DA DUYET.
- 2CDX UV04 (work/claude_2cdx_20261008/UNG VIEN 04: 5ab141cdf63d / 9f9cc7a3af04 / 9537165202cc): bỏ 66 ô kg tr.2; chỉ CATALOGUE DA DUYET (2CDX chưa có trong BẢN MỚI 03-10 — anh chưa bảo).
- Biên nhận history/bo-11-nhom-luot17-accepted-20261008T070501Z/; health ĐẠT; khoá nhả. Không còn khối lượng ở catalogue nào trong CATALOGUE DA DUYET. Không còn câu chờ anh.

## 4x-L18. LƯỢT 18 — SS PEROTAC thay 3 ảnh đại diện (20261008T142954Z; QUYET_DINH mục 104–105)
- Ứng viên `work/claude_bo_20261007/SS/UNG VIEN 06/PEROTAC - SS.pdf` (b617cdf9d4e7) đã thay bản chính `Nước thải/SS Perotac (bản mới).pdf` + CATALOGUE DA DUYET; sao lưu + biên nhận `history/ss-perotac-anh-luot18-accepted-20261008T142954Z/`. Mã: `ss_page.py` (NEWP/CAPS_P; bản trước `ss_page_UV05_truoc_doi_anh.py`). REDPUMP/AQUARIS SS không đổi (UV05).
- Anh chốt (mục 106): REDPUMP SS GIỮ ảnh cũ; PEROTAC không cần ảnh không phao. Không còn câu chờ.

## 4·GIA. Bảng giá tối thiểu — cập nhật thông số theo CATALOGUE DA DUYET (20261008T233404Z, chỉ ĐỌC catalogue, không sửa PDF)
- Đầu ra: `Catalog Sua\GIA TOI THIEU 08-10-2026\Gia toi thieu - cap nhat thong so theo catalogue 09-10-2026.xlsx` (gốc anh gửi để cùng thư mục). Giá/công thức giữ nguyên; 247 ô thông số sửa (tô vàng, trang NHAT KY THAY DOI); thêm 47 dòng mới (2CDX 15, MHI 17, IVT-MHI 14, đĩa DN128); cột AQUARIS riêng ở Giếng nhựa, Giếng inox, Trục ngang.
- Anh chốt 09/10: chỉ thêm dòng hàng mới, họ đã có thì chỉ cập nhật mã đang có; dòng thêm mới ghi lưu lượng max và cột áp max.
- Kiểm độc lập ĐẠT (~2.100 ô, 0 sai). Còn 12 câu trong trang CAN ANH XEM chờ anh trả lời.
- Dữ liệu trích: $HOME/claude_work/json/*.json (nháp ngoài kho).

## 4y-L19. LƯỢT 19 — SA AQUARIS thêm 2 / 2.5 / 3 / 6 inch (20261009T022835Z; QUYET_DINH mục 107)
- UV06 `work/claude_bo_20261007/SA/UNG VIEN 06/AQUARIS - SA.pdf` (2ca42825d673, 18 trang) đã thay bản chính + CATALOGUE DA DUYET; biên nhận `history/sa-aquaris-them-2-3-6-inch-accepted-20261009T022835Z/`. Mã: bo_data.aq_ext/aq_all, bo_build (trang dải AQUARIS theo cỡ, ảnh Ph_f2/f3/f6), bo_page.table_A (rated None, cột hẹp khi nhiều Q). Bản mã trước: `*_UV05_truoc_them_co.py`. PEROTAC/REDPUMP SA không đổi.
- Anh chốt (mục 109): giữ tên SA; giữ ảnh PEROTAC + xoá tem đỏ → UV07 962ad7e5a369 đã thay bản chính + CATALOGUE DA DUYET (history/sa-aquaris-xoa-tem-anh-accepted-20261009T024619Z/).
- 20261009T023008Z: bản 2 file giá (… 09-10-2026 (ban 2).xlsx) áp câu trả lời anh 09/10 (xoá 6 dòng, đổi FS300/80M, DN128, IRG -4 ghi chú, AQUARIS đang bổ sung, 2CDX theo ảnh). 3 việc sửa catalogue WC/CDX ghi ở QUYET_DINH mục 09/10, CHƯA LÀM.

## 4z-L20. CM AQUARIS thêm 6 mã số PEROTAC — XONG 20261009T024859Z, đã thay bản chính + CATALOGUE DA DUYET (24ef59e17cb7) (09/10; QUYET_DINH mục 108)
- Ứng viên nháp `work/claude_bo_20261007/CM/UNG VIEN 10/AQUARIS - CM.pdf` (12 trang, 72 model): CM 32 +2 mã, CM 40 +2 mã, trang mới AQ80b (CM 80-250/37, /45, lưới Q PEROTAC). Mã: bo_data.aq_groups (pick), curves_AQ.json chép đường PR 6 mã; bo_cm (A_data trang >9 model thu biểu đồ/dòng; images_for AQUARIS không cần assets.npz). Bản trước: *_UV09_truoc_them_6ma.*
- Anh chọn "1" (mục 109): dải CM 40-250 AQUARIS cả 4 mã số PEROTAC (/11, /15 giữ I(A) nguồn; đường nguồn cũ lưu `curves_AQ_CM40-250_11_15_nguon_AQ.json`). kiem 2003/2003, TTCS 0; kiểm độc lập 5/5 ĐẠT (`qa/PHIEU_KIEM_DOC_LAP_L20_AQUARIS.md`). Biên nhận history/cm-aquaris-them-6-ma-accepted-20261009T024859Z/.

## 4·5VIEC. 5 việc 09/10 — XONG, đã nhận bản chính + CATALOGUE DA DUYET (phiên cowork-01PauH56, 09/10 ~10:00Z)
- JBB, WC, CDX, SA, SP, FC: mã kiểm và biên nhận ở claude/BAN_GIAO_20261009T095953Z.md; TIEN DO 4 dòng 20261009T083145Z…093832Z; inventory-20261009T093903Z.
- Quyết định: QUYET_DINH 110, 116–123 (lưu ý: 111–113 là phiên ROOTS).
- Báo cáo cho dự án SEO web: claude/BAO_CAO_THAY_DOI_CATALOGUE_20261009.md + THAY_DOI_MA_20261009.csv.
- Còn: bản in chưa kiểm. Không giữ khoá nào.

## 4·RL. ROOTS RL PEROTAC + REDPUMP — XONG, ANH ĐÃ DUYỆT, ĐÃ VÀO CATALOGUE DA DUYET (09/10 ~04:20Z, phiên cowork-016jaZa4; QUYET_DINH 111–112)
- CATALOGUE DA DUYET\PEROTAC\PEROTAC - Máy thổi khí Root RL.pdf (20 tr, 4b23aae2b7b3); \REDPUMP\REDPUMP - Máy thổi khí Root RL.pdf (21 tr, 42eebb8e3e88) = đúng byte deliverables/ROOTS RL 20261009/*(BAN 02 DA SUA SO).pdf.
- Mã: work/claude_roots_rl_20261009 (rl_data.py → model.json; rl_build.py <HÃNG> <tệp>; rl_qa.py). Nguồn: Catalog Sua\NGUON BO SUNG 20261009\Root - catalogue mau anh gui 09-10-2026.pdf. 7 ô sửa: data/sua_theo_anh.json.
- Kiểm: bảng hiệu suất 1776 ô (1769 giữ nguồn + 7 sửa đúng), kích thước 180, phụ kiện 571 khớp; 111 đường lệch ≤2,49%; kiểm độc lập 3 lượt (qa/QA_DOC_LAP.md).
- Anh chốt 09/10 11:27 (QUYET_DINH 113): bản chính BẢN MỚI 03-10 Perotac Root (RL+RW) GIỮ NGUYÊN; bản RL mới chỉ ở CATALOGUE DA DUYET. Việc ROOTS RL đóng.
- 20261009T085243Z: bảng giá bản 4 — trang Giếng nhựa (17 mã) và Giếng inox (45 mã) khác thông số giữa hãng đã tách 3 dòng REDPUMP/PEROTAC/AQUARIS (anh chốt 09/10 15:50); kiểm 5.799 ô giá: 0 sai.
- 20261009T085713Z: bảng giá bản 5 — anh sửa 15:55 'tách ra thành 3 mục riêng... mục 1 redpump, mục 2 perotac, mục 3 aquaris': trang Giếng nhựa, Giếng inox, Trục ngang chia 3 mục đủ danh sách mỗi hãng; kiểm 4.926 ô giá: 0 sai.

## 4c. Phiên 20261012T0656Z — Test report CDLF42 (chỉ đọc catalogue, không sửa catalogue)
- 3 bảng test tiếng Anh CDLF42-4T/5T/6T (xlsx+pdf) ở `Claude outputs/TEST REPORT CDLF42 12-10-2026/`. Q-H lấy từ bảng hiệu suất CDLF bản 03-10 (3 hãng trùng số). Cột đo điện/tốc độ/áp/hiệu suất để trống chờ số test thật. Rác LibreOffice trong `_to_delete/` chờ anh xoá.

- **13/10/2026 (CLAUDE_WQX_20261013):** catalogue riêng PEROTAC 80WQX40-15-5.5 (bơm chìm nước thải inox, 1 trang) — ứng viên 03 (đường Q–H + ảnh đại diện v2 không lẹm, AI khác kiểm ĐẠT) ở work/claude_wqx_20261013, chờ anh duyệt; 01/01b/02 bỏ. Đọc BAO_CAO.md ở đó.
- **13/10/2026 14:10 (CLAUDE_WQX_20261013):** catalogue riêng PEROTAC 150WC300-30-37 (cắt rác, 2 trang A3) — ứng viên 01 ở work/claude_wc150_37_20261013, chờ anh chốt Hmax (báo giá 25–30 m mâu thuẫn tên model). Đọc BAO_CAO.md ở đó.
