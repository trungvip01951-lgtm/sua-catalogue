# PEROTAC — Cụm 2 bơm tăng áp MHI-Q (QĐ 155) — 14/10/2026, phiên CLAUDE_20261014T0925Z

Ứng viên: `PEROTAC - Cụm 2 bơm tăng áp MHI-Q (UNG VIEN 07).pdf` — sha256 2d4209d8bf42, 0.38 MB, 2 trang A4 ngang. Bản 01–06 là nháp cũ (bỏ).
Số liệu: MHI-Q.xlsx (MODEL, QH). Mã dựng: build_mhiq.py (python build_mhiq.py <gốc kho> <thư mục có MHI-Q.xlsx, chart_*.pdf, img/> <tệp ra>). Đường: tools/ve_duong_cong.py --rong-pt 380 --cao-pt 330.
Ảnh đại diện: img/MHI-Q_PEROTAC_v4.jpg/.png (từ ảnh 1 anh gửi; tách nền, bỏ pallet/ván đỏ/thùng gỗ, xoá nhãn bình áp + 2 tem bơm). CHƯA vào KHO_ANH — chờ anh duyệt.

## Số suy ra (QĐ 155: cột áp = bơm đơn, 2 bơm song song Q×2)
- Đường 1 bơm: lấy mẫu từ đường MHI-403 / MHI-1604 trong PEROTAC - Bơm trục ngang MHI.pdf tr.2 (đã duyệt); Hmax 28 / 36, định mức 4/21 và 16/27, Qmax 7 / 26 theo DU_LIEU/MHI.xlsx.
- MHI-403Q 1 bơm H tại Q 0–7: 28, 27.4, 26, 23.8, 21, 17.5, 13.4, 8.8. MHI-1604Q tại Q 0/4/8/12/16/20/24/26: 36, 35.6, 34, 31.2, 27, 21.6, 14.7, 10.8.
- Áp cài đặt 2.4 / 3.0 bar lấy theo IVT-MHI403 / IVT-MHI1604.
- Lệch với báo giá anh gửi: báo giá ghi 403Q 8.1 m³/h / 33 m; 1604Q 26.1 / 48 m — không dùng (anh chọn suy từ bơm đơn).

## Kiểm
- kiem_catalogue.py: ĐẠT 6 · CHƯA ĐẠT 0 · CHƯA THỂ XÁC MINH 2 (mục 2 điện/pha, mục 3 bảng Q–H: công cụ không đọc được kiểu bảng 2 hàng 1 bơm/2 bơm → kiểm tay: AI kiểm độc lập đối chiếu 34/34 ô khớp, Q tăng H giảm) · BỎ QUA 2 (chỉ 1 hãng; chưa vào DANH SACH).
- Kiểm độc lập (AI khác, 4 lượt): số liệu ĐẠT, lệch đường ≤ 0.6% so với đường bản duyệt; ảnh không lẹm ĐẠT (lần 4); vòng tròn điểm định mức đúng trên đường.
- Câu chưa có nguồn (chỉ suy từ ảnh): van chặn từng bơm, bình áp/đồng hồ/cảm biến, tủ biến tần inox, ống góp inox; "Apartment buildings, hotels and offices"; thông số 0–90 °C/10 bar/IP54/8 m lấy của bơm đơn.
