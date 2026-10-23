# Bắt đầu tại đây — dự án Sửa catalogue (cập nhật 13/10/2026)

## 1. Đọc (theo thứ tự)

1. rules/QUY_TAC_HIEN_HANH.md 2. rules/HO_SO_HANG.md 3. rules/CHUAN_TRINH_BAY.md 4. claude/TRANG_THAI_CLAUDE.md
Khi cần: rules/QUYET_DINH_ANH.md, rules/LOI_DA_GAP.md, claude/VIEC_CHO_ANH.md, claude/LOI_ANH_BAO.md.
Hai cửa kiểm bắt buộc trước khi ký đạt: **KHÁC GIAO DIỆN GIỮA CÁC HÃNG** và **ĐƯỜNG CONG ĐỀU** (xem AGENTS.md).

## 2. Kiểm kho và khoá việc

Chạy bằng Python của máy mình (Claude trên Linux: `$HOME/cfenv/bin/python -B -X utf8`, dùng `claude/cat.py` thay cho `tools/catalogue.py` để dịch đường dẫn):

```
python -B -X utf8 tools/catalogue.py health     # cấu trúc kho + niêm phong quy tắc ("changed" phải rỗng)
python -B -X utf8 tools/catalogue.py status     # dòng cuối sổ TIEN DO + khoá bản chính
python -B -X utf8 claude/khoa_viec.py xem       # khoá việc của các phiên
```

`health` không phải kiểm catalogue; trên Linux báo "missing_paths: python" là lỗi sẵn có (manifest.json trỏ Python Windows) — bỏ qua. Nhận khoá: `claude/khoa_viec.py nhan <VIỆC> <PHIÊN> "<phạm vi>"`; ghi bản chính gốc thì thêm `catalogue.py claim --file … --actor … --session … --purpose …`, xong `release`.

## 3. Làm

- Dựng mới là chính: DU_LIEU/<nhóm>.xlsx (số liệu) + KHO_ANH/ (ảnh) + rules/HO_SO_HANG.json + mã dựng templates/<nhóm>/ → 3 PDF. Kiểm bằng tools/kiem_catalogue.py (10 mục), nhận bản bằng tools/nhan_ban_chinh.py, đồng bộ gói nhân viên bằng tools/dong_bo_drive.py (các công cụ này đang được viết từ 13/10 — chưa có thì làm tay theo CHUAN_TRINH_BAY).
- catfix chỉ khi sửa tại chỗ bản gốc. Khi đó đọc prompt chung và vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT/README_KY_THUAT.md, chạy 43 bài kiểm (Claude: `bash claude/dau_phien.sh test`; Windows: `python -B -X utf8 tools/bootstrap_legacy.py --tests`) — phải có "TỔNG KẾT: 43/43 ĐẠT" và môi trường 4/4 ĐƯỢC. catfix trên Windows cần biến `CATFIX_ROOT=D:\ChatGPT\Sửa catalogue\CATALOG SUA`.
- Ứng viên lưu tệp mới ở thư mục việc riêng; AI khác kiểm độc lập; anh duyệt thì chép đúng byte vào CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/ và cập nhật DANH SACH.txt.

## 4. Nơi gốc

| Gì | Ở đâu |
|---|---|
| Nguồn bất biến của anh | CATALOG SUA/BẢN MỚI 01-10-2026, CATALOG SUA/NGUON BO SUNG 2026100x |
| Bản chính 25 catalogue gốc | CATALOG SUA/BẢN MỚI 03-10-2026 (ChatGPT) |
| Bản anh đã duyệt (62 PDF) | CATALOG SUA/CATALOGUE DA DUYET |
| Quy tắc | rules/ |
| Số liệu, ảnh, mã dựng | DU_LIEU/, KHO_ANH/, templates/<nhóm>/ |
| Ảnh chụp trạng thái, niêm phong quy tắc | state/ (cập nhật bằng tools/refresh_index.py --actor ROOT --reason "…" [--seal-controls], do điều phối chạy) |

## 5. Catalogue mới

Anh đưa tệp nguồn + việc theo mẫu lệnh 6 ô. AI tự áp quy tắc, chỉ hỏi dữ liệu thật sự thiếu. Giữ bản gốc, tạo thư mục đầu ra riêng; mã dựng đạt lưu templates/<nhóm>/.
