# Hồ sơ thiết kế 3 hãng — bản người đọc

Bản máy đọc: rules/HO_SO_HANG.json (phiên bản `2026.10.13`). Hai tệp phải khớp từng giá trị; sửa một tệp thì sửa tệp kia cùng lượt. Nguồn: phương án anh duyệt 13/10/2026 (rules/QUYET_DINH_ANH.md mục 149; claude/PHUONG_AN_DA_DUYET_20261013.md). Màu đo từ 62 bản đã duyệt. Trong ngoặc `…` là giá trị đúng như trong json.

## 1. Chung cho cả 3 hãng (`chung`)

| Mục | Giá trị | Nghĩa |
|---|---|---|
| Khổ A4 dọc (`kho_A4_doc`) | 595 × 842 pt | rộng × cao; pt = point, 1/72 inch |
| Khổ A4 ngang (`kho_A4_ngang`) | 842 × 595 pt | |
| Lề (`le_mm`) | 12–15 mm | khoảng trắng mép trang |
| Lưới cột (`luoi_cot`) | 12 cột | chia bề ngang trang để căn khối |
| Cỡ chữ tối thiểu (`co_chu_pt`) | tiêu đề trang ≥ 16 pt (`tieu_de_trang_min`); chữ thân ≥ 9 pt (`than_min`); số trong bảng ≥ 7 pt (`bang_min`), nên 8 pt (`bang_nen`); nhãn trục ≥ 7 pt (`nhan_truc_min`); nhãn đường ≥ 7 pt (`nhan_duong_min`) | không đủ chỗ thì tách trang, không thu chữ |
| Nét đường đặc tính (`net_duong_pt_min`) | ≥ 1.5 pt | |
| Lưới chính biểu đồ (`luoi_chinh_pt`) | 0.5 pt | |
| Tương phản (`tuong_phan`) | chữ ≥ 4.5 : 1 (`chu`); chữ lớn và nét đường ≥ 3.0 : 1 (`chu_lon_va_net`) | tỉ số sáng chữ/nền theo chuẩn WCAG (chuẩn dễ đọc trên màn hình) |
| Số đường tối đa mỗi biểu đồ (`so_duong_toi_da_moi_bieu_do`) | 8 | nhiều hơn thì tách biểu đồ |
| Giới hạn riêng AQUARIS | 7 đường | bảng màu Okabe–Ito bỏ vàng chỉ có 7 màu |
| Công suất tối đa có bản 1 pha (`dien.mot_pha_kw_toi_da`) | 3 kW | đề xuất 13/10, chưa anh duyệt |
| Ngưỡng giống giao diện giữa 2 hãng (`nguong_giong_giao_dien`) | 0.6 | đề xuất 13/10, chưa anh duyệt; > 0.6 = quá giống |
| Vùng trống liền tối đa (`khoang_trong_lien_toi_da`) | 0.10 = 10% chiều cao trang | |
| Dung lượng tệp (`dung_luong_mb`) | mục tiêu ≤ 5 MB (`muc_tieu`), tối đa 10 MB (`toi_da`) | |
| Ảnh (`anh`) | ≥ 200 ppi tại kích thước đặt (`ppi_min`); ảnh bìa ≥ 300 ppi (`ppi_bia_min`); ảnh gốc cạnh dài ≥ 1000 px (`canh_dai_goc_px_min`); sản phẩm chiếm 0.80–0.85 cạnh dài ô ảnh (`ty_le_khung`); bóng tiếp xúc độ đục 0.15–0.25 (`bong_do_duc`) | ppi = điểm ảnh trên mỗi inch khi in ra đúng cỡ đặt |
| Khối điều kiện dưới biểu đồ (`khoi_dieu_kien_duong_cong`) | "Curves at 50 Hz, 2 poles (≈ 2900 min⁻¹), clean water at 20 °C, kinematic viscosity 1 mm²/s. Typical values, not guaranteed." | số cực và tốc độ đổi theo nguồn; nghĩa: "đường ở 50 Hz, 2 cực, nước sạch 20 °C, độ nhớt 1 mm²/s; giá trị điển hình, không cam kết" |
| Bảng màu nhiều đường (`okabe_ito_bo_vang`) | #0072B2, #D55E00, #009E73, #CC79A7, #56B4E9, #E69F00, #000000 (theo thứ tự) | bảng màu Okabe–Ito (dễ phân biệt cả với người mù màu), đã bỏ màu vàng #F0E442 vì khó đọc trên nền trắng |
| Chữ cấm (`chu_cam`) | "warranty", "guarantee period", "60 Hz", "60Hz", "weight", "kg" | bảo hành, thời hạn bảo hành, 60 Hz, cân nặng |
| Ghi điện (`dien`) | 1 pha (`mot_pha`): "1~ 220–240 V 50 Hz"; 3 pha (`ba_pha`): "3~ 380–415 V 50 Hz" | |

## 2. Từng hãng (`hang`)

| Trục thiết kế | AQUARIS | PEROTAC | REDPUMP |
|---|---|---|---|
| Khổ (`kho`) | A4 dọc (`A4_doc`) | A4 ngang (`A4_ngang`) | A4 ngang (`A4_ngang`) |
| Phông (`phong`) | Lato | Liberation Sans | Liberation Sans |
| Màu chính (`mau.chinh`) | xanh rêu #0D6159 | xanh than #13334D | than #2B2E33 |
| Màu phụ | cờ Ý #009246 / #FFFFFF / #CE2B37 (`mau.co_y`) | màu đường #1A669E (`mau.duong`) | đỏ đô nhấn #A31A1F (`mau.nhan`) |
| Màu nền khối (`mau.nen`) | #F0F7F5 | #EDF5FA | #F7F2F0 |
| Đồ họa phụ (`do_hoa_phu`) | dải cờ Ý (`dai_co_y`) | băng đầu trang xanh nhạt (`bang_dau_trang_xanh_nhat`) | cột tối bên trái chiếm 28–30% bề ngang (`cot_toi_trai_28_30_phan_tram`) |
| Bìa (`bia`) | ảnh trên-trái, ô số liệu nổi bật, nhiều khoảng trắng (`anh_tren_trai_o_so_lieu_noi_bat`) | logo trái, chia 3 cột (`logo_trai_chia_3_cot`) | cột tối trái chứa tên dòng + dải hiệu năng, ảnh bên phải (`cot_toi_trai_ten_dong_dai_hieu_nang_anh_phai`) |
| Màu đường biểu đồ (`bieu_do.mau_duong`) | mỗi model một màu, bảng Okabe–Ito (`moi_model_mot_mau_okabe_ito`) | một tông xanh (`mot_tong_xanh`) | đỏ/xám (`do_xam`) |
| Nhãn đường (`bieu_do.nhan`) | số khoanh tròn + chú giải (`so_khoanh_tron_va_chu_giai`) | tên model ở đầu trái đường (`ten_model_dau_trai_duong`) | tên model trong ô màu ở cuối phải đường (`ten_model_trong_o_mau_cuoi_phai_duong`) |
| Trục cột áp H (`bieu_do.truc_H`) | bên trái (`trai`) | bên trái (`trai`) | bên phải (`phai`) |
| Nền biểu đồ (`bieu_do.nen`) | #FFFFFF | #FFFFFF | xám rất nhạt #F4F4F4 (cũng là `mau.nen_bieu_do`) |
| Hướng bảng (`bang.huong`) | mỗi model một CỘT (`model_theo_cot`) | mỗi model một DÒNG (`model_theo_dong`) | mỗi model một DÒNG (`model_theo_dong`) |
| Kẻ bảng (`bang.ke`) | kẻ ngang mảnh (`ngang_manh`) | kẻ đầy đủ, mảnh (`day_du_manh`) | đầu bảng nền tối chữ trắng, sọc xám xen kẽ (`dau_bang_toi_chu_trang_soc_xam`) |
| Ảnh sản phẩm (`anh`) | nền #FFFFFF, bóng tiếp xúc mờ (`tiep_xuc_mo`) | nền #FFFFFF, không bóng (`khong`) | nền #FFFFFF, bóng đổ dưới đế (`do_duoi_de`) |

## 3. Luật dùng hồ sơ

- 3 bản cùng dòng phải khác ≥ 5/6 trục: màu, phông, bìa, bảng, biểu đồ, đồ họa phụ. PEROTAC và REDPUMP cùng phông nên 5 trục còn lại BẮT BUỘC khác.
- Cấm dùng chung một khuôn biểu đồ/bảng rồi chỉ đổi màu, lật trái-phải hay đảo vị trí khối.
- Mẫu nhìn theo: catalogue CM và MIX đã duyệt. Không chép logo, màu, bố cục của hãng bơm thật.
- Số liệu (model, kW, Q, H, A…) của 3 hãng giống nhau từng ký tự; chỉ trình bày khác.
