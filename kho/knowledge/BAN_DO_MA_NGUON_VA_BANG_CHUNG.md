# Bản đồ mã nguồn và bằng chứng

Kho này lưu cả công cụ gốc, mã phiên cũ và lỗi; không tự chạy mọi tệp đã lưu.

| Nơi | Nội dung và cách dùng |
|---|---|
| vendor/GOI_SUA_CATALOGUE_CHATGPT.zip | Gói nguyên byte anh cung cấp; mã đối chiếu tại vendor/ORIGINAL_PACKAGE_MANIFEST.json |
| vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT | Gói đã giải nén riêng, không đổi catfix; gồm README, tasks162 và18 prompt nhóm |
| vendor/prompts_on_desktop | Bản sao nguyên văn prompt/tài liệu trên Desktop để tra khác biệt với ZIP |
| vendor/legacy/batdau.py | Đoạn khởi động nguyên văn đã dùng; tools/bootstrap_legacy.py gọi nó khi chạy BƯỚC0 |
| archive/CODE_INDEX.json | Danh mục mã nguồn: đường gốc, vị trí trongZIP, SHA-256, kích thước; có mã tốt và mã bị loại |
| archive/TEXT_EVIDENCE_INDEX.json | Bản lưu bất biến báo cáoJSON/Markdown/CSV/chẩn đoán, khác tài liệu tiến độ sống |
| archive/EVIDENCE_INDEX.json | Con trỏ và mã kiểm mọi ảnh/PDF/biểu đồ/báo cáo tại thời điểm chụp; không nhân bản mọi tệp lớn |
| state/catalogues.json |25 catalogue nguồn, bản hiện hành đúng nhánh/đổi tên đã giao và mãSHA; số thực do công cụ chụp xác nhận |
| state/CURRENT_CHECKPOINT.md | Mốc đọc tiếp, chỉ là bản bàn giao; mở sổ gốc trước ghi |
| history/ | Các ảnh chụp trạng thái/luật/bản sổ chỉ đọc theo giờ; không phải sổtiếnđộ thứhai |
| work/ | Hồ sơ phối hợp/QA mới từng tác nhân; không tự ghiPDF nguồn hay bản chính ở đây |

## Các chương trình có giá trị tham khảo

- `root_per_wc_photo_actual_m1_readback.py`, `root_per_wc_photo_publish_accepted_m1.py`: đọc/tiếpnhận M1ảnh8trang; hàm tiếpnhận đã chạy, không chạy lại.
- `root_cdx_actual_m1_readback.py`, `root_cdx_p3_publish_accepted_m1.py`: đọc4đường/184chữ/mọi5trang và tiếp nhậnp3;#118p4/p5 không được coi xong.
- `g04_perotac_whole_source_island_builder60.py`, `g04_perotac_whole_saved_qa63.py`, `g04_perotac_whole_m1_locked65.py`: nguồn RAM9đảo/QA/khóaM1 **chưa chạy**; các phiên mới70+ có chẩn đoán khác, phải đọc mốc trước dùng.
- Bộ SA mới 77/78/79/80 và bàn giao RAM V4 chỉ là nghiên cứu trong bộ nhớ, toàn chữ trục chưa đạt, 0 PDF. Writer65 gắn V2 không được dùng cho V4. Ba atlas đủ 62 cụm nằm trong G04/PHUONG AN DONG BO TOAN BIEU DO P08/RAMV4 DOC LAI CA62 CUM CHU TRUC SOURCE ACTUAL CHI DOC.
- `g04_redpump_whole_caption_island_RAM_builder.py`, `...RAM1.py`: nghiên cứu13cụm nguồn **chưa đạt hình thức**, không mẫu chuẩn đã nghiệm thu.
- Trong workspace `catalogue-perotac-sp-dong-bo-do-thi`: bộv22/v23/v24 đã khóa chuẩn bị nhưngFAILdáng4/chữtrục. Không lấy chữFINALcũ hayfill98/98làPASSđồhọa.
- Trong workspace `catalogue-gb-native-tiep-tuc`: writer/QA M2 đã dùng; đối chiếu biênnhậnG10 trước chạy.
- `root_excel_curves_inventory_20261003.py`, `root_excel_new_scope_checkpoint.py`: đọc2Excel và ghi phạmvi thiếu min, không tácgiả7đường đã xong.
- `g01_per_sa_*` và hồ sơ RA SOAT NGOAI TRANG8 G01 LAN1: đọc1827mốc/231tậpcon; là kiểm nguồn, không đãsửa4điểmsai.

Mã lịch sử thường chứa tên nguồn, tọa độ, số bảng, SHA và `fresh()`/ROOT-lock. Phải dùng đúng đối tượng/tệp/phiên được ghi hoặc tạo phương án mới, không thaySHA để chạy qua. Có thể giải nén bản lịch sử vào thư mục work mới chỉ để đọc/so; không ghi đè mã đang dùng.

## Tìm nhanh bằng PowerShell

```powershell
rg -n -F 'CDX' archive/CODE_INDEX.json archive/TEXT_EVIDENCE_INDEX.json
rg -n -F 'H FEET 200' archive/EVIDENCE_INDEX.json
rg -n -F 'CHƯA THỂ' state/CURRENT_CHECKPOINT.md knowledge/LOI_VA_CACH_TRANH.md
```

Đường dẫn gốc trong index dẫn đúng chứng cứ thật. KhoZIP giữ bản đã đọc lúc chụp; filegốc đổi sau đó phải so lại. SHA chỉ chứng đúng byte phiên nào, không chứng thông số/đồhọa đạt. Không xóa các mẫu sai chỉ vì đã có bản đạt.


## Thư viện mẫu có phiên bản 06/10/2026

`templates/catalogue/README.md` là đầu mối; `SP6_VECTOR_V1/inventory.json` ghi con trỏ vàSHA các PDF/PNG/dữliệu/mãnguồn nguyênbản. Phầnmã lưu `.py.txt` chỉđểđọc; mẫu SP6 hìnhFAIL/STOP2, sốđạt riêng. `PHIEU_DOI_THONG_SO.json` và `procedures/SUA_THONG_SO_TU_MAU.md` dùng khi anh nêu thôngsốmới. Thưviện không thay sổgốc, không tựnhậnbảnchính.
