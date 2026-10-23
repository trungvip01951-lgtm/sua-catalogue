# ĐƯỜNG DẪN MỚI từ 10/10/2026 — gửi ChatGPT/Codex và mọi AI làm dự án Sửa catalogue

Anh Trung chốt 10/10/2026: thư mục `C:\Users\H2\Desktop\Catalog Sua` ĐÃ GỘP vào kho và KHÔNG CÒN ở Desktop.

| Cũ | Mới |
|---|---|
| `C:\Users\H2\Desktop\Catalog Sua` | `D:\ChatGPT\Sửa catalogue\CATALOG SUA` |
| Sổ: `C:\...\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\TIEN DO.md` | `D:\ChatGPT\Sửa catalogue\CATALOG SUA\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\TIEN DO.md` |

- Cấu trúc bên trong giữ nguyên (BẢN MỚI 01-10-2026, BẢN MỚI 03-10-2026 (ChatGPT), CATALOGUE DA DUYET, NGUON BO SUNG…).
- `manifest.json` đã đổi đường dẫn và niêm phong lại (`state/control_manifest.json`).
- catfix: ROOT_WIN trong `catfix/session.py` vẫn là đường cũ (gói gốc, không sửa) → trên Windows đặt biến môi trường `CATFIX_ROOT=D:\ChatGPT\Sửa catalogue\CATALOG SUA` trước khi chạy.
- Tệp trung gian (ảnh png, json lớn, cache) đã gom vào `_CHO_XOA_20261010` — đừng đọc/ghi ở đó; cần tệp nào thì tra `history/don-rac-gop-kho-20261010/da_chuyen.csv` (cột 2 = đường cũ, cột 3 = chỗ hiện tại).
- Cập nhật bộ nhớ của mình (ví dụ `.codex/memories`) sang đường mới.
