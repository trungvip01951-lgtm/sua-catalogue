# WC 3 hãng — thêm mã 200WC350-22-37 vào catalogue chuẩn (16/11/2026, phiên CLAUDE_20261116, QĐ 190)

Lệnh anh: ảnh báo giá (200WC350-22-37, Qmax 780 m³/h, Hmax 40 m, 37 kW 3 pha 380 V 50 Hz, 1450 rpm) + "Thêm mã này vào catalogue wc của cả 3 hãng".

## Cách làm
- Vá tại chỗ trang 200WC của 3 bản chính (PEROTAC tr.7, REDPUMP tr.6, AQUARIS tr.6) bằng them_ma.py: giữ khuôn trang, vẽ lại biểu đồ và bảng; trang khác không đụng.
- Gốc dựng = bản chính trước 16/11 (sau khi nhận bản mới thì nằm ở history/<UTC>_<HÃNG> - Bơm cắt rác WC/).
- 4 đường cũ: giữ nguyên hình (điểm điều khiển Bézier cũ co theo trục mới 0–800 / 0–45).

## Số liệu mã mới
| Mục | Giá trị | Nguồn |
|---|---|---|
| Qmax, Hmax, kW, tốc độ | 780 m³/h, 40 m, 37 kW, 1450 /min | lời anh (ảnh báo giá) |
| Điểm làm việc | 350 m³/h – 22 m | mã model (QĐ 177) |
| H tại Qmax | 5 m | nấc thứ 5 dải 200WC (QĐ 19: 11 kW = 1 m … 30 kW = 4 m) |
| HP | 50 | SUY RA (quy đổi 37 kW, giống catalogue riêng REDPUMP 13/11) |
| Ô H giữa | 40, 37, 34, 32, 29, 27, 24, 22, 20, 18, 15, 13, 11, 10, 8, 6, 5 tại Q = 0…750 bước 50, 780 | SUY RA: H = 40 − 0.056765·Q + 1.5248e-5·Q², làm tròn số nguyên |

## Thay đổi trên trang 200WC
- Ô tóm tắt: 11 – 30 kW → 11 – 37 kW; 600 → 780 m³/h; 32 → 40 m.
- Biểu đồ: trục Q 0–800 (vạch 100), trục H 0–45 (vạch 5), thêm đường + nhãn mã mới (AQUARIS màu tím #6b3fa0 như mã thứ 5 trang 300WC).
- Bảng: 13 → 17 cột Q (thêm 650, 700, 750, 780), thêm dòng mã mới.
- DU_LIEU/WC.xlsx: +1 dòng MODEL, +17 dòng QH, +1 dòng KIEM mỗi hãng; "Q max/H max của cỡ" dải 200WC → 780/40; sao lưu history/DU_LIEU_WC_truoc_QD190_20261116.xlsx.

## Kiểm
- doc_lai.py (3 hãng): trang khác 0 đổi; chữ cũ ngoài vùng vẽ lại 0 lệch; 4 dòng cũ nguyên số; dòng mới đúng; tiêu đề Q đúng; lệch cột 0.00 pt.
- tools/kiem_catalogue.py --goc --trang: ĐẠT 8/8 mỗi hãng (mục 9, 10 bỏ qua vì chỉ kiểm trang vá).
- AI khác nghiệm thu độc lập (mã kiểm tự viết): 6/6 mục ĐẠT — đường mới qua 0/40, 350/22, 780/5; lệch đường–bảng lớn nhất 4,6 % (ngưỡng 5 %); 4 đường cũ trùng bản gốc (≤ 0,002 m); bảng, nhãn trục, nét kẻ khớp kiểu trang 300WC; trang khác y nguyên chữ và nét.
- Ghi nhận: phông bị subset lại nên các trang khác của AQUARIS lệch khử răng cưa tối đa 15/255 (mắt không thấy); trang 200WC dùng phông nhúng mới cùng họ LiberationSans/Lato.
- Bản chính 16/11/2026: PEROTAC 56956e912125, REDPUMP 475b65a0de8b, AQUARIS dad9fa2667cd.
