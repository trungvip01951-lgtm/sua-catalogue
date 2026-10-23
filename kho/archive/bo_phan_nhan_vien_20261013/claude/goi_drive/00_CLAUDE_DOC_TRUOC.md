# Sửa catalogue — gói Google Drive cho nhân viên · bộ quy tắc 2026.10.13

Claude của nhân viên: đọc tệp này đầu mỗi cuộc trò chuyện. Trả lời tiếng Việt, ngắn gọn; chữ tiếng Anh phải dịch và giải thích.

## 1. Làm theo skill
Mọi việc catalogue làm theo skill **sua-catalogue** (bản nhân viên). Chưa có skill thì báo nhân viên nhờ anh Trung cài (tệp `sua-catalogue.zip` ở gốc thư mục này), trong lúc đó đọc thẳng các tệp ở mục 3.

## 2. Quyền
- Chỉ ghi vào `NV_LAM/<tên nhân viên>/` và một dòng của mình trong `NV_LAM/KHOA_VIEC`.
- Không sửa, ghi đè, xoá tệp nào khác. Không tự phát hành. Bản chính chỉ anh Trung cập nhật sau nghiệm thu.
- Nhân viên muốn đổi quy tắc/cách làm: ghi đề xuất vào `NV_LAM/<tên>/DE_XUAT.md`.

## 3. Bản đồ thư mục
| Thư mục | Nội dung |
|---|---|
| `QUY_TAC/rules/QUY_TAC_HIEN_HANH.md` | Quy tắc đang áp dụng — đọc đầu tiên |
| `QUY_TAC/rules/HO_SO_HANG.md` (+ `.json`) | Hồ sơ thiết kế 3 hãng |
| `QUY_TAC/rules/CHUAN_TRINH_BAY.md` | Chuẩn ảnh, biểu đồ, bảng, chữ, tệp; mẫu lệnh; định nghĩa hoàn thành |
| `QUY_TAC/rules/LOI_DA_GAP.md` | Lỗi đã gặp — tìm theo từ khoá nhóm |
| `QUYET_DINH_ANH/` | Nhật ký quyết định anh Trung, trạng thái, việc đang chờ anh |
| `CATALOG SUA/CATALOGUE DA DUYET/<HÃNG>/` | Catalogue đã duyệt — điểm bắt đầu khi sửa (chỉ đọc) |
| `DU_LIEU/<NHÓM>.xlsx` | Số liệu gốc từng nhóm (THONG_TIN, MODEL, QH hoặc BANG, KIEM) |
| `KHO_ANH/` | Ảnh đã tách + `DANH_MUC.csv` (ĐẠT / CẦN THAY KHI CÓ DỊP) |
| `CONG_CU/tools/` | `kiem_catalogue.py` (kiểm 10 mục), `ve_duong_cong.py` (vẽ Q–H + bảng theo hãng) |
| `CONG_CU/templates/`, `CONG_CU/catfix_original/` | Mẫu cũ, bộ sửa PDF cũ (chỉ khi sửa tại chỗ) |
| `CATALOG SUA/BẢN MỚI 01-10-2026`, `NGUON BO SUNG …` | Nguồn gốc, chỉ đọc |
| `BAN_GIAO_RIENG/` | 3 bản giao riêng: 6SP30 Redpump, QXN40-60 Perotac, DWO 200-300 |
| `NV_LAM/` | Nơi DUY NHẤT được ghi |
| `PHIEN_BAN.txt` | Phiên bản bộ quy tắc của gói; mới hơn skill thì dùng tệp trên Drive |

Tài liệu cũ ghi đường máy anh Trung `D:\ChatGPT\Sửa catalogue\<x>`: `rules|procedures|knowledge` = `QUY_TAC/<x>`; `tools|templates` = `CONG_CU/<x>`; `deliverables` = `BAN_GIAO_RIENG`. Lệnh `dau_phien.sh`, `khoa_viec.py`, `cat.py`, thư mục `state/`, `work/`, `history/` chỉ có trên máy anh: bỏ qua.

## 4. Lưu ý dữ liệu đã biết (13/10/2026)
- Catalogue WC cả 3 hãng: cột áp ở điểm lưu lượng lớn nhất của mỗi dòng trùng số thứ tự dòng trên trang (1, 2, 3…) — nghi số điền, đang chờ anh Trung xử lý; đừng chép số này sang bản mới khi chưa có chỉ đạo.
- KTZ-LH: chưa có bảng Q–H (đường cong là hình) — sửa đường cong thì hỏi anh.
- AQUARIS CM, SA 4 inch, SP khác số với PEROTAC/REDPUMP ở một số model — là nguồn khác nhau, giữ nguyên trừ khi anh chỉ đạo.
