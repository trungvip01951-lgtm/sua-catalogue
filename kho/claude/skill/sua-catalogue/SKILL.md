---
name: sua-catalogue
description: Dùng cho MỌI việc dự án Sửa catalogue bơm công ty Trung Kiên (PEROTAC, REDPUMP, AQUARIS) - nhận lệnh mẫu 6 ô, sửa/tạo catalogue theo hồ sơ hãng, vẽ đường Q-H, kiểm tự động, nghiệm thu, nhận bản chính, ghi quyết định.
---

# Sửa catalogue — skill dự án (bộ quy tắc 2026.10.13)

Người dùng là người phụ trách dự án (anh Trung hoặc nhân viên anh giao). Trả lời tiếng Việt, ngắn gọn; chữ tiếng Anh phải dịch và giải thích. Không đoán số liệu: thiếu thì ghi CHƯA THỂ XÁC MINH và hỏi. Quyết định chốt/duyệt cuối cùng là của anh Trung (hoặc người anh uỷ quyền, ghi rõ tên trong nhật ký).

## 0. Kho và tệp phải đọc

Kho: `D:\ChatGPT\Sửa catalogue` (phiên Claude nối máy: `$HOME/mnt/Sửa catalogue`, làm bằng shell trên máy). Tệp thật trong kho thắng skill này khi lệch.

Đầu phiên đọc, theo thứ tự (dưới 40 KB):
1. `rules/QUY_TAC_HIEN_HANH.md` — quy tắc đang áp dụng.
2. `rules/HO_SO_HANG.md` (+ `rules/HO_SO_HANG.json` máy đọc) — khổ, màu, phông, bố cục, kiểu biểu đồ/bảng/ảnh từng hãng.
3. `rules/CHUAN_TRINH_BAY.md` — chuẩn ảnh, biểu đồ, bảng, chữ, tệp; mẫu lệnh; định nghĩa hoàn thành.
4. `claude/TRANG_THAI_CLAUDE.md` và `claude/VIEC_CHO_ANH.md`.
Tra khi cần: `rules/LOI_DA_GAP.md` (lỗi đã gặp, tìm theo từ khoá nhóm), `rules/QUYET_DINH_ANH.md` (nhật ký nguyên văn), sổ `CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT)/_BAO CAO/TIEN DO.md` (chỉ tìm theo từ khoá, không đọc hết).

| Nơi gốc | Nội dung |
|---|---|
| `CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/` + `DANH SACH.txt` | 62 catalogue đã duyệt (không sửa trực tiếp) |
| `DU_LIEU/<NHÓM>.xlsx` | Số liệu gốc mỗi nhóm (THONG_TIN, MODEL, QH hoặc BANG, KIEM) — đọc `DU_LIEU/README.md` |
| `KHO_ANH/` + `DANH_MUC.csv` | Ảnh đã tách, trạng thái ĐẠT / CẦN THAY KHI CÓ DỊP |
| `templates/<nhóm>/` | Mã dựng đã đạt (bắt buộc lưu ở đây) |
| `tools/` | `ve_duong_cong.py`, `kiem_catalogue.py`, `nhan_ban_chinh.py`, `niem_phong.py`; phông ở `vendor/fonts/` |
| `CATALOG SUA/BẢN MỚI 01-10-2026`, `NGUON BO SUNG …` | Nguồn gốc, chỉ đọc |

Python trên máy: `$HOME/cfenv/bin/python -B -X utf8` (chưa có thì `bash claude/dau_phien.sh env`). Mọi lệnh dưới chạy tại gốc kho.

## 1. Nhận lệnh — mẫu 6 ô

```
1. Việc: Tạo mới | Sửa | Đổi ảnh
2. Dòng bơm: (vd CM, SP 4 inch, WC)
3. Hãng: PEROTAC | REDPUMP | AQUARIS | Cả 3
4. Sửa gì: (model — thông số — cũ → mới; hoặc trang số …)
5. Tệp đính kèm: (catalogue nhà cung cấp, ảnh — ghi model cho từng ảnh)
6. Ghi chú:
```
Lệnh ngắn vẫn được ("Sửa CM PEROTAC: CM 32-160/2.2 cột áp tại 9 m³/h 28.5 → 29.5", "Duyệt …", "Trả lại …: …"). Thiếu ô nào hỏi đúng ô đó MỘT lần, lựa chọn đánh số. Lệnh trái quy tắc đã chốt: nêu điều quy tắc + số QĐ, hỏi lại một lần.

## 2. Quy trình — chép danh sách ra và đánh dấu

- [ ] 1. Đọc lệnh (đủ 6 ô) và 4 tệp đầu phiên; tìm từ khoá nhóm trong LOI_DA_GAP.
- [ ] 2. Khoá: `python3 claude/khoa_viec.py xem`, rồi `nhan <NHOM_HANG> <MA_PHIEN> "<phạm vi>"` (mỗi lần làm ứng viên mới sau khi đã nhả thì nhận lại). Việc phiên/AI khác đang giữ: không đụng, không chiếm khoá. Tệp dùng chung (TRANG_THAI, QUYET_DINH, sổ): đọc lại ngay trước khi ghi, chỉ nối đoạn của mình. Không sửa tệp có niêm phong khi phiên khác đang giữ khoá.
- [ ] 3. Làm trong thư mục nháp NGOÀI kho (`$HOME/claude_work/<việc>/`). Số liệu: sửa trên BẢN SAO `DU_LIEU/<NHÓM>.xlsx`, ghi cũ → mới.
- [ ] 4. Dựng (mục 3) hoặc vá (mục 4).
- [ ] 5. Kiểm tự động (mục 5) → sửa → kiểm lại; cùng một cách hỏng 2 lần thì đổi cách.
- [ ] 6. Nhìn PDF thật (ảnh xem lưu `claude/_xem/xem_1..8.png`, tên cố định, ghi đè): trang ~110 dpi, vùng biểu đồ và vùng ảnh 250–300 dpi; 3 hãng đặt cạnh nhau. Nhờ một AI khác kiểm độc lập phần thẩm mỹ. Lập phiếu QA.
- [ ] 7. Gửi người phụ trách theo mẫu trả lời (mục 7); chờ "Duyệt".
- [ ] 8. Duyệt → `nhan_ban_chinh.py` (mục 8); khi đó mới cập nhật `DU_LIEU/` gốc bằng bản sao đã sửa và lưu mã dựng vào `templates/<nhóm>/`.
- [ ] 9. Nhả khoá; ghi đè mục 4 `claude/TRANG_THAI_CLAUDE.md`; bàn giao `claude/BAN_GIAO_<UTC>.md` ≤ 2 KB.

## 3. Dựng mới (tạo mới, hoặc dựng lại cả catalogue)

- Khổ chuẩn: AQUARIS A4 dọc 595×842; PEROTAC, REDPUMP A4 ngang 842×595. Bố cục, màu, phông, kiểu bảng/biểu đồ/ảnh theo `rules/HO_SO_HANG.md`. Mẫu nhìn theo: CM và MIX đã duyệt.
- Biểu đồ + bảng: `python tools/ve_duong_cong.py --du-lieu <xlsx> --hang <HÃNG> --ra <pdf> [--model …] [--kieu bieu_do|bang|ca_hai] [--so-voi DU_LIEU/<NHÓM>.xlsx]`, chèn vào trang bằng pymupdf `show_pdf_page`. Mã thoát 2 = số liệu sai hoặc số SỬA tạo gợn (chỉnh điểm kề, số nguyên, ghi cũ → mới, hoặc hỏi); 3 = không vừa khổ / thiếu phông. Cảnh báo ghi ở `<pdf>.canh_bao.txt` — đọc hết (vd "THIẾU DÒNG ĐIỆN A" ở vài model → điền số suy ra vào DU_LIEU theo QUY_TAC_HIEN_HANH 4.6 rồi vẽ lại).
- Ba hãng cùng dòng khác ≥ 5/6 trục (màu, phông, bìa, bảng, biểu đồ, đồ hoạ phụ); cấm chung khuôn rồi chỉ đổi màu, lật trái-phải, đảo khối. Số liệu giống nhau theo nguồn (AQUARIS CM, SA 4", SP có số riêng — giữ).
- MẶC ĐỊNH CÓ BIỂU ĐỒ Q–H cho mọi catalogue (QĐ 145), trừ IRG (QĐ 149, anh chọn 3.2). Thiếu bảng số thì tự vẽ từ thông số có (Hmax tại Q = 0, điểm định mức theo tên model, Qmax), ghi điểm suy ra trong báo cáo và hỏi xác nhận, nhưng vẫn giao bản có đường. KTZ-LH chưa có bảng Q–H (đường là hình) — sửa đường thì hỏi.
- Bìa/chân trang: giữ theo bản cũ hoặc chỉ ghi tên hãng. Phông: dùng `vendor/fonts/` (Lato, Liberation Sans bản 2 — bản 1 làm gạch trong mã model thành gạch mềm, tìm chữ không thấy).

## 4. Vá catalogue đã duyệt (sửa vài số, vài trang, đổi ảnh)

- VÁ đúng chỗ, giữ khổ/bố cục bản đã duyệt (catalogue cũ có khổ lẻ và biểu đồ > 8 đường là bản anh đã duyệt) — anh đã chốt (QĐ 152); dựng lại cả catalogue chỉ khi anh ra lệnh riêng.
- Tìm MỌI chỗ chứa số cần đổi (`page.search_for`, cả bảng, nhãn, chú thích; một số có thể lặp nhiều chỗ), xoá vùng bằng redaction rồi ghi lại đúng phông, cỡ, màu, căn lề cũ. Đổi số Q–H thì vẽ lại cả biểu đồ của nhóm trang đó bằng `ve_duong_cong.py` theo kiểu hãng, cùng khung cũ.
- Thiết bị không có Q–H (máy thổi khí GB/RL, máy khuấy MIX/4MIX, bơm định lượng JLM-JBB, đĩa phân phối khí): số ở `DU_LIEU/<NHÓM>.xlsx` sheet BANG (RL thêm HIEU_NANG); sửa số trên trang theo cách vá ở trên; biểu đồ đặc thù (đường hiệu năng RL, biểu đồ đĩa) giữ kiểu bản đã duyệt.
- Kiểm bản vá: `kiem_catalogue.py <pdf vá> --goc <pdf đã duyệt> --trang <các trang đổi>` — chỉ lỗi MỚI mới tính.

## 5. Kiểm tự động

`python tools/kiem_catalogue.py <pdf|thư mục> [--bo3 <AQ> <PE> <RE>] [--du-lieu <xlsx>] [--goc <pdf> --trang 2,3] [--khong-qh] [--json out.json]` — 10 mục: (1) chữ cấm + "50 Hz"; (2) điện/pha; (3) bảng Q↑H↓, "–", thứ tự công suất, WC theo QĐ 19; (4) đường lệch ≤ 5%, cong đều (≤ 1 điểm uốn, không đoạn phẳng rồi gãy), không móc, ≤ 8 đường (AQUARIS 7); (5) chữ chồng, cỡ chữ; (6) ảnh ppi, tràn mép, chồng, 1 ảnh nhiều cỡ; (7) tương phản; (8) khổ, dung lượng, phông, RGB, khoảng trống; (9) khác giao diện 3 hãng; (10) mã kiểm khớp DANH SACH. CHƯA THỂ XÁC MINH thì kiểm tay mục đó và ghi rõ.

## 6. Quy tắc chính (đầy đủ ở rules/)

- Đường: PCHIP qua đúng điểm bảng; Q tăng H giảm; giữ Qmin/Qmax/Hmin/Hmax/điểm làm việc; trục Q m³/h + l/min, H m. Dòng dưới biểu đồ: "Curves at 50 Hz, 2 poles (≈ 2900 min⁻¹), clean water at 20 °C, kinematic viscosity 1 mm²/s. Typical values, not guaranteed." Không ghi ISO 9906 trừ khi anh xác nhận nhà cung cấp thử theo chuẩn đó.
- Bảng: Model 1 pha | Model 3 pha | P2 kW | P2 HP | A | Q (m³/h trên, l/min dưới); "–" chỉ ở cột 1 pha; "1~ 220–240 V 50 Hz", "3~ 380–415 V 50 Hz"; pha theo QUY_TAC_HIEN_HANH mục 3; H số lẻ theo nguồn thì giữ; cột A: nguồn không có A thì bỏ cột (công cụ tự bỏ, QĐ 152); nguồn có A mà vài mã thiếu thì giữ cột, điền số suy ra vào DU_LIEU theo QUY_TAC_HIEN_HANH 4.6.
- Chữ: thân ≥ 9 pt, bảng/nhãn ≥ 7 pt (không đủ chỗ thì tách trang), tiêu đề ≥ 16 pt; tương phản chữ ≥ 4,5:1.
- Ảnh: nền trắng/trong suốt; ≥ 200 ppi tại kích thước đặt (bìa ≥ 300); sản phẩm 80–85 % ô; mỗi cỡ một ảnh; xoá logo/chữ hãng gốc; soi viền trên nền trắng/xám/đen phóng 300 %. Ảnh tự tạo/vẽ lại phải gửi anh duyệt trước khi dùng. Lấy ảnh ĐẠT từ KHO_ANH; ảnh mới đã duyệt thì thêm vào KHO_ANH.
- Ảnh đại diện từ ảnh anh gửi (QĐ 145, 146): ảnh anh gửi là ảnh MẪU — tách nền (kho, thùng, túi, cáp cuộn, vật thừa), xoá logo/chữ/tem lạ, căn đẹp trên nền sạch, bóng mềm dưới chân; đủ nguyên thân bơm, KHÔNG lẹm nắp, bulong, tai móc, cáp, mặt bích, vỏ xoắn, chân đế; lỗi nhỏ thì chỉnh màu/vẽ bù, không cắt thêm vào thân; mặt nạ tay đo toạ độ trên ảnh phóng to có lưới. Công cụ đã thử: `rembg` isnet-general-use tốt; SAM theo điểm làm mất tai móc, lỗ bích; BiRefNet tràn bộ nhớ 8 GB — đừng thử lại; vẽ lại cáp bằng `cv2.polylines` phóng 4 lần. Lưu cạnh ứng viên: PNG nền trong suốt + JPG nền trắng; ảnh gốc giữ nguyên. Một AI khác so ảnh gốc với ảnh đã làm, phóng từng vùng, xác nhận không lẹm.
- Tệp: ≤ 5 MB (tối đa 10), RGB, phông nhúng một lần, lưu `garbage=4, deflate`; tên "HÃNG - Tên dòng.pdf"; "50 Hz" ở trang 1 với sản phẩm có động cơ.
- Cấm: bảo hành, cân nặng (GIỮ bảng kích thước và họng hút/xả), 60 Hz, tiếng Việt trong PDF, ô "*".

## 7. Mẫu trả lời và phiếu QA

Trả lời luôn theo thứ tự: (1) kết quả một câu; (2) ảnh xem trước trang đổi (3 hãng cạnh nhau nếu làm cả 3); (3) bảng thay đổi cũ → mới; (4) phiếu kiểm: số mục ĐẠT / CHƯA ĐẠT / CHƯA THỂ XÁC MINH; (5) câu hỏi gom một lần (gọi đúng tên catalogue/model, nêu hiện trạng + dẫn chứng, lựa chọn đánh số + đề xuất) và phần chưa xong.
Phiếu QA có hai mục riêng **KHÁC GIAO DIỆN GIỮA CÁC HÃNG** (chấm bố trí / màu / trình bày) và **ĐƯỜNG CONG ĐỀU** (có ảnh đại diện mới thì thêm **ẢNH KHÔNG LẸM**); bốn kết quả riêng: kiểm số, hình thức, bảo toàn, kiểm tự động; mỗi yêu cầu ĐẠT / CHƯA ĐẠT / CHƯA THỂ XÁC MINH. Chỉ báo xong khi đạt hết (định nghĩa hoàn thành: CHUAN_TRINH_BAY mục 8).

## 8. Nhận bản chính (sau khi được duyệt)

`python tools/nhan_ban_chinh.py --ung-vien <pdf> --dich "<HÃNG>/<HÃNG> - <tên dòng>.pdf" --ly-do "<câu>" [--thu]`: sao lưu bản cũ sang `history/<UTC>_<tên>/`, chép đúng byte, đọc lại mã kiểm, cập nhật DANH SACH.txt và sổ TIEN DO. Chạy `--thu` trước.

## 9. Ghi quyết định và cập nhật quy tắc

Quyết định mới → chép NGUYÊN VĂN vào cuối `rules/QUYET_DINH_ANH.md` (số tiếp theo, ngày giờ, ai nói) → cùng lượt sửa điều liên quan trong `QUY_TAC_HIEN_HANH.md` / `HO_SO_HANG` (.md và .json) / `CHUAN_TRINH_BAY.md`, đánh "(đã thay bởi mục N)" vào mục cũ → nếu là lỗi: thêm dòng `LOI_DA_GAP.md` và phép kiểm vào `kiem_catalogue.py` (chạy `tools/test_cong_cu_moi.py`) → `python tools/niem_phong.py "<lý do>"` rồi `python claude/cat.py health` phải "changed": [] → sửa skill này ở `claude/skill/sua-catalogue/SKILL.md` nếu chạm tới → báo một dòng.

## 10. Làm nhanh và tiết kiệm

- Tách phần độc lập (theo hãng/nhóm/trang) cho nhiều AI chạy song song; mỗi AI một khoá, một thư mục nháp, một tệp ra; giao kèm phạm vi, tệp được ghi, quy tắc, cách kiểm, định dạng trả về.
- Việc cơ học (đọc bảng, tách số, xuất ảnh) dùng model rẻ; phán đoán (thiết kế, đường cong, nghiệm thu) dùng model mạnh. Chỉ kiểm phần vừa làm và phần bị ảnh hưởng.
- Không cài gì lên máy anh, không đụng giấy phép Office. Không chạy lại mã lịch sử có số/toạ độ/mã kiểm cố định.
- Không xoá tệp: tệp bỏ thì `mv` sang `archive/` và ghi `archive/DA_CHUYEN_<ngày>.csv`. Không bao giờ dọn `rules/`, `DU_LIEU/`, `KHO_ANH/`, `templates/`, `CATALOG SUA/`, `vendor/`.
