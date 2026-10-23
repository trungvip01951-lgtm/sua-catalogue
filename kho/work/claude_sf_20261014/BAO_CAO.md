# Catalogue MỚI dòng SF (Showfou SF áp cao) — 3 hãng (14/10/2026, phiên CLAUDE_20261014T0750Z)
Lệnh anh 14:48: "vẽ lại catalogue FS này cho a nhé làm cả hãng cho a nhé song cho a 3 file a tự cập nhật vào" + chọn "1. Làm catalogue MỚI", "1. Giữ mã SF cả 3 hãng" (QĐ 154).
Nguồn: Catalog bơm nước thải Showfou SF áp cao.pdf (1 trang ảnh quét). Bảng số đọc 2 cách (mắt trên ảnh phóng 230 dpi + nhận dạng chữ tesseract), khớp; AI khác so lại từng ô: 0 lỗi.
Tệp: AQUARIS (A4 dọc, 3 trang), PEROTAC (A4 ngang, 4 trang), REDPUMP (A4 ngang, 4 trang) - Bơm chìm nước thải SF áp cao.pdf. Số liệu: SF.xlsx (12 mã 3 pha, 8 mã 1 pha có phao, 98 điểm Q–H). Mã dựng: build_sf.py (+ tools/ve_duong_cong.py). Ảnh: sf_cut.png (tách nền từ ảnh nguồn, không vẽ lại).
Bỏ theo quy tắc: "Warranty: 2 years", "Other voltages or frequency 60Hz" (còn "Other voltages"), "Curve tolerance according to ISO 9906", tốc độ ghi n ≈ 2850 /min theo nguồn. Sửa chữ: "Top chock" → "Top cover"; "three phase with no D marked" → "three-phase models without "m"".
Kiểm tự động kiem_catalogue.py: 3 tệp ĐẠT 8/8 (2 mục bỏ qua: DANH SACH); khác giao diện 3 hãng ĐẠT (cảnh báo: màu chính PEROTAC–REDPUMP gần nhau, theo hồ sơ hãng).
Kiểm độc lập: số ĐẠT, nội dung ĐẠT, khác giao diện ĐẠT; hình thức: nhãn đường dồn → đã chia PEROTAC/REDPUMP thành 3 biểu đồ × 4 đường; gạch nối mã AQUARIS (U+2010) → đã đổi về "-".
Còn lại: PEROTAC tr.4 nhãn "SF27-55-7.5" đặt giữa đường 7.5 và 5.5 (3 đường bắt đầu sát nhau 57.9/58.5/60.6 m) — do công cụ đặt nhãn.
Chưa đưa vào CATALOGUE DA DUYET, DU_LIEU, KHO_ANH (anh tự cập nhật).

14/10/2026 16:18 anh: "REDPUMP e làm cái ảnh còn nền trắng bên trong này sửa cho a" → làm trong suốt 7 mảng nền trắng kẹt (trong 2 vòng cáp, trong khung tay cầm, khe dưới kẹp cáp) + làm mềm mép phần trên (y<230); không đổi màu điểm nào, 0 điểm tối bị xoá; AI khác kiểm ảnh: không lẹm. Dựng lại cả 3 tệp (cùng ảnh), kiem_catalogue 8/8 × 3.

14/10/2026 16:35 anh: "PErotac cho 2 ảnh có phao và k phao vào làm đại diện cho a nhé" (QĐ 156) → PEROTAC trang 1 đặt 2 ảnh: không phao = Three-phase SF…, có phao = Single-phase, floating switch SFm…F. Ảnh gốc giữ nguyên (SF_PEROTAC_*_anh_gui.png); ảnh tách nền sf_pe_*.png (rembg isnet + giữ thân inox đục, bỏ bóng dưới đế, bỏ nền kẹt giữa cáp/phao và thân, trong khung tay cầm). AI khác kiểm: không lẹm; 2 lỗi nền sót đã sửa. AQUARIS, REDPUMP không đổi. kiem_catalogue 8/8 × 3.
