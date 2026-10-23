# vendor/fonts — phông nhúng cho tools/ve_duong_cong.py

Chép ngày 13/10/2026 từ máy dựng (Linux, gói Debian) để công cụ luôn dùng đúng phông hồ sơ hãng,
không phụ thuộc phông cài trên máy (máy thiếu Lato từng bị thay lặng lẽ bằng Inter).

| Tệp | Họ phông | Dùng cho | Nguồn | Giấy phép |
|---|---|---|---|---|
| Lato-Regular.ttf, Lato-Bold.ttf | Lato 2.0 | AQUARIS | gói Debian fonts-lato 2.0-2.1 (/usr/share/fonts/truetype/lato), gốc http://www.latofonts.com — (c) 2010-2011 Łukasz Dziedzic | SIL Open Font License 1.1 — LICENSE_Lato_OFL-1.1.txt |
| LiberationSans-Regular.ttf, LiberationSans-Bold.ttf | Liberation Sans 2.1.5 | PEROTAC, REDPUMP | gói Debian fonts-liberation2 2.1.5-1 (/usr/share/fonts/truetype/liberation2), gốc https://github.com/liberationfonts — (c) 2012 Red Hat, Inc. (Reserved Font Name "Liberation"), dữ liệu số hóa (c) 2010 Google | SIL Open Font License 1.1 — LICENSE_LiberationSans_OFL-1.1.txt |

Tệp LICENSE_*.txt là tệp copyright của gói Debian, có toàn văn SIL OFL 1.1.
OFL cho phép nhúng phông vào PDF và phân phối kèm phần mềm; không bán riêng phông, không đổi tên phông khi sửa.

Thứ tự ve_duong_cong.py tìm phông: <thư mục chứa script>/../fonts, <gốc kho>/vendor/fonts, rồi phông hệ thống
(nhận phông theo tên ghi trong tệp, không theo tên tệp). Thiếu phông đúng hồ sơ hãng -> dừng mã 3, trừ khi chạy
với --cho-phep-phong-gan-giong.

MD5:
```
01dcf602cb7f7116bde159f25c4bbe89  Lato-Bold.ttf
fa62c04b03d3f7d2333a33c311d9747d  Lato-Regular.ttf
325b7a9216a21a25b2c044a771af8fd7  LiberationSans-Bold.ttf
04fde74a0b0a76a6d1732e74faf789cd  LiberationSans-Regular.ttf
```
