# catfix – HƯỚNG DẪN KỸ THUẬT (đọc hết trước khi viết code)

Bộ công cụ Python để sửa catalogue PDF/Excel **"vô hình"**: chữ mới là bản chép nét chữ có sẵn
trong chính file (cùng font, cỡ, màu, độ đậm, góc xoay), đặt đúng vị trí; mọi thứ khác giữ nguyên
từng byte. Đã kiểm thử trên các catalogue thật của anh Trung (`python tests/run_tests.py` → 43/43 ĐẠT),
chạy được trên máy chủ ChatGPT (Linux, /mnt/data) và thẳng trên máy anh (Windows).

> Quy ước: trong CODE số trang bắt đầu từ **0** (trang 1 = 0). Trong BÁO CÁO ghi số trang từ **1**.
> Toạ độ là điểm PDF (pt, 1 pt = 1/72 inch), gốc ở **góc dưới trái** trang, rect = (x0, y0, x1, y1).

## 0. Khởi động (mỗi phiên)
Chạy NGUYÊN VĂN đoạn code ở BƯỚC 0 của PROMPT CHUNG (tự nhận chạy trên máy anh hay máy chủ ChatGPT). Sau đó:
```python
sh('tests/run_tests.py')          # phải: TỔNG KẾT: 43/43 ĐẠT
print(S)                          # Session: chỗ lấy file vào (S.in_dir), lưu file ra (S.out_dir), báo cáo (S.report_dir)
S.src('Catalog cắt rác Aquaris WC (bản mới).pdf')    # đường dẫn file vào (tìm cả thư mục con)
S.dst('Catalog cắt rác Aquaris WC (bản mới).pdf')    # đường dẫn file ra: cùng tên, cùng thư mục con, trong S.out_dir
job = S.job('Catalog cắt rác Aquaris WC (bản mới).pdf')   # = Job(S.src(..), S.dst(..)), nhật ký vào S.report_dir
S.report('BAO CAO G08.md'); S.progress('G08', 'XONG', '12/12 ĐẠT'); print(S.read_progress())
```
Trên Windows: file đang mở (trình xem PDF, hoặc Editor/PdfDoc chưa `close()`) thì không ghi đè được –
`job.close()` / `E.close()` trước khi lưu lại cùng tên. Tesseract được tự tìm ở `C:\Program Files\Tesseract-OCR`.
Nếu công cụ chạy code giới hạn thời gian mỗi lần chạy (bị ngắt giữa chừng):
* chạy bài kiểm theo từng phần, mỗi lần 1 dòng: `sh('tests/run_tests.py', 'Môi trường', 'Bộ đọc')`,
  rồi `sh('tests/run_tests.py', 'nét vẽ')`, `'Chữ thật'`, `'Ảnh quét'`, `'Biểu đồ'`, `'Ảnh bìa'`,
  `'Excel'`, `'Cấu trúc'`, `'Đường dẫn'`, `'Windows'` – cộng lại phải đủ
  4+4+4+3+6+5+3+3+4+5+2 = 43 bài ĐẠT (lần chạy sau nhanh hơn nhờ bộ nhớ đệm OCR);
* trang khổ lớn / dày chữ (A3, IRG, CDLF): `T.learn([p], rect=vùng_cần, dpi=400)` thay vì cả trang 600 dpi;
* tách việc nhỏ (mỗi lần 1–3 trang). Kết quả OCR lưu đệm ở thư mục `CATFIX_CACHE` (BƯỚC 0 đặt sẵn).

## 1. Biết file trước khi sửa
```python
from catfix.inspect_pdf import summary, what_is_at
print(summary(src))                         # mỗi trang: ẢNH CẢ TRANG / CHỮ THẬT / CHỮ NÉT VẼ
what_is_at(src, 8, (505, 505, 540, 520))    # ở chỗ này là gì + nên dùng công cụ nào
```
| Loại chỗ cần sửa | Công cụ |
|---|---|
| CHỮ THẬT (lớp chữ có font) | `TextLayer` / `Job.text_replace` |
| CHỮ NÉT VẼ (chữ đã chuyển thành hình vector) | `OutlineText` / `Job.outline_replace` |
| ẢNH QUÉT (cả trang là ảnh) | `Raster` / `Job.raster_replace` |
| Ảnh ghép bìa (nhiều ảnh cắt nền) | `catfix.images` |
| Biểu đồ | `catfix.charts` |
| Excel | `catfix.xlsx.Xlsx` |

## 2. Cách nhanh: `Job` (nên dùng)
```python
job = S.job('<tên file vào>.pdf')     # = catfix.recipes.Job(src, dst); src = job.src, dst = job.dst (không bao giờ = src)
job.outline_dump(14)                                     # in các dòng chữ nét vẽ đọc được (trang 15)
job.outline_replace(14, 'Warranty: 1 year', 'Warranty: 2 years', align='left', expect=1)
job.text_replace(0, 'irrugation', 'irrigation', align='left', expect=1)
job.raster_replace(8, '1750', '175', align='center', search_rect=(600, 80, 700, 110))
job.save()                   # ghi dst + nhật ký .log.json (vào S.report_dir)
job.evidence(S.report('So sanh G05.png'))                # ảnh trước | sau từng chỗ sửa
r = job.check(raster=False)  # raster=True cho file ảnh quét
print(r['ok'], r['unexpected'], r['missing'], r['structure'])
```
* `align`: `'left'` giữ đầu chữ (chữ trong câu, nhãn căn trái) · `'center'` giữ tâm (ô bảng căn giữa,
  tiêu đề giữa) · `'right'` giữ cuối (cột số căn phải). Xem các ô cùng cột để chọn; với chữ nét vẽ có
  `job.T.guess_align(match)`.
* `expect=n`: bắt buộc tìm thấy đúng n chỗ – tránh sửa nhầm chỗ.
* `regex=True`: `old` là biểu thức chính quy, `new` có thể dùng `\1` (vd bỏ số 0 đầu tên model:
  `job.outline_replace(p, r'(\d+SP\d+)-0(\d)', r'\1-\2', align='center', regex=True)`).
* `job.check()` = (1) điểm ảnh thay đổi NGOÀI các vùng sửa phải rỗng, (2) mỗi vùng sửa phải có thay
  đổi, (3) cấu trúc file tốt. Vùng hợp lệ thêm: `job.check(extra_allowed={trang: [rect,...]})`.

## 3. Chữ nét vẽ – `OutlineText`
```python
from catfix.vector import Editor
from catfix.otext import OutlineText
E = Editor(src); T = OutlineText(E)
T.learn([14, 16])                 # OCR trang (vẽ riêng nét chữ đen/trắng) -> gán chữ cho từng hình
T.dump(14)                        # (x0,y0,x1,y1) + dòng chữ đọc được; '?' = hình chưa biết là chữ gì
T.dump(14, rect=(150, 470, 260, 490))
m = T.find(14, 'Warranty: 1 year')        # list Match (.text .bbox .glyphs .line)
T.replace(m[0], 'Warranty: 2 years', align='left')
T.delete(m[0], close_gap=False)           # xoá chữ (close_gap=True: dồn phần sau sang trái)
T.insert(key=14, text='...', x_origin=..., baseline=..., sid=m[0].glyphs[0].style, target_oi=m[0].glyphs[0].oi)
T.move(m[0], dx, dy)                      # dời chữ (vd căn lại mục lục)
E.save(dst)
```
* Đọc sai/thiếu chữ ('?' hoặc chữ lạ trong `dump`): xem ảnh vùng đó (`verify.crop(src, pi, rect, 300)`
  rồi hiển thị), sau đó **dạy**: `T.teach(14, rect_một_dòng, 'chữ đúng của dòng đó')` – số ký tự
  (không tính dấu cách) phải bằng số hình trong vùng. Nhãn lan ra mọi hình giống hệt trong file.
* Thiếu ký tự cùng kiểu chữ: công cụ tự tìm cùng font ở cỡ khác trong file và phóng/thu; nếu vẫn
  thiếu → báo lỗi `Không có chữ ... cùng kiểu chữ` → KHÔNG thay font khác, ghi CHƯA THỂ.
* Chữ có bản sao viền trắng (halo) phía sau: `replace(..., twins='auto')` tự sửa cả bản sao.
* Chữ xoay (nhãn trên đường cong): `T.similarity_decode(page, rect)` cho biết chữ + góc xoay;
  sửa bằng cách xoá hình cũ (`E.delete_group`) và chèn hình nguồn với ma trận xoay
  (`E.insert_path(page, oi, path, Mx=...)`), xem ví dụ ở mục 7.

## 4. Chữ thật – `TextLayer`
```python
from catfix.textlayer import TextLayer
TL = TextLayer(E)
TL.dump(0)                                # dòng chữ + font + cỡ
m = TL.find(0, '(KW)')                    # TMatch
TL.replace(m[0], '(kW)', align='center')  # cùng font/cỡ/màu; ký tự không có trong font -> KeyError
TL.delete(m[0])
TL.insert_like(ref_match, 'Speed 2900 r.p.m', origin=(x, y_baseline))   # thêm dòng mới cùng kiểu
```
* Font nhúng thường là font rút gọn (chỉ có ký tự đã dùng). Báo `Font ... không có ký tự` → tìm một
  đoạn chữ khác cùng font đầy đủ hơn trên cùng trang làm `ref` cho `insert_like`, hoặc báo CHƯA THỂ.
* Đổi nhiều chỗ một lúc theo mẫu: `job.text_replace(pages, r'(\d),(\d)', r'\1.\2', regex=True)`.
* `keep_rest=True` (mặc định): chữ phía sau trong cùng lệnh giữ nguyên vị trí (bảng, cột).
  Với đoạn văn chạy dài muốn chữ sau dồn tự nhiên: `keep_rest=False`.

## 5. Ảnh quét – `Raster`
```python
from catfix.raster import Raster
R = Raster(E)
R.images(3)                               # các ảnh trên trang (TEXT-CLIPPED = lớp chỉ hiện trong nét chữ, bỏ qua)
im = R.image_at(3, rect)                  # ảnh đang HIỂN THỊ ở vùng đó
cv = R.canvas(im)                         # sửa trên điểm ảnh gốc (giữ chất lượng JPEG cũ)
# ảnh có /Mask kiểu stencil (Perotac CM), Indexed, nhiều lớp:  cv = R.render_canvas(3, rect)
hits = R.find(cv, '1750', box=cv.box(search_rect))      # OCR (đã bỏ kẻ bảng)
bank = R.glyph_bank(cv, box=cv.box(learn_rect))         # mẫu chữ CÙNG font (vd cả bảng đó)
R.replace_word(cv, hits[0], '175', bank, align='center') # xoá chữ cũ, dán chữ mới chép từ ảnh
R.erase(cv, box=cv.box(rect))                           # xoá một vùng (vẽ lại nền)
R.copy_box(cv, src_box, (u, v))                         # chép một khối điểm ảnh (dời dòng/ô)
R.commit(cv)                                            # ghi vào PDF (ảnh mã hoá lại 1 lần, cùng bảng lượng tử)
E.save(dst)
```
* Luôn khoanh `search_rect` (vùng tìm) và `learn_rect` (vùng học chữ cùng font, cùng cỡ).
* Kiểm tra bằng `verify.ocr_check(dst, pi, rect, '175')` và `job.check(raster=True)`
  (file ảnh quét: ảnh được mã hoá lại một lần → vài điểm lẻ khác ≤ 1–2 mức màu là bình thường;
  ngưỡng kiểm `thr=48, min_size=2`).
* `R.noop_test(pi)` (trên Editor nháp) đo sai khác khi ghi lại ảnh không sửa gì: phải < 1 mức trung bình.

## 6. Ảnh ghép (bìa CDLF) – `catfix.images`
```python
from catfix import images
ims = {im.name: im for im in R.images(0)}
images.mirror_images(E, [ims[n] for n in ('R13','R16','R18','R20','R22','R25')], axis_x)   # lật cả cụm ảnh, chữ bìa không lật
images.delete_image(E, ims['R25'])                                                       # bỏ bơm đế gang
dst_box = images.fit_bbox(ims['R16'].page_bbox, slot_box, keep_aspect='height', anchor='bottom-center')
images.clone_image(E, ims['R16'], dst_box, after=ims['R25'], flip_h=True)               # đặt bản sao bơm
```
Ảnh nào là "bơm đế gang": xem ảnh từng `im.name` (`verify.crop(src, 0, im.page_bbox, 100)`).

## 7. Biểu đồ – `catfix.charts`
```python
from catfix import charts
P = E.page(pi)
gx, gy = charts.gridlines(P, plot_rect)                        # vị trí đường lưới dọc / ngang
xt = charts.snap_ticks(charts.ticks_from_labels(T, pi, xlabel_rect, 'x'), gx)
yt = charts.snap_ticks(charts.ticks_from_labels(T, pi, ylabel_rect, 'y'), gy)
ch = charts.Chart.from_ticks(xt, yt)       # ch.warning khác None = trục sai / đọc nhãn sai -> nhập tay
# hoặc nhập tay: charts.Chart.from_ticks([(0, x0), (20, x20)], [(0, y0), (180, y180)])
cur = charts.curve_objects(P, plot_rect, color=(0.133, 0.365, 0.635))   # các đường cong (màu nét)
old_pts = ch.to_data(charts.sample_path(P.object_pagepath(oi)))       # số hoá đường cũ
dev = ch.compare(old_pts, table_points)                                # lệch so với bảng
path = ch.smooth_path(table_points)        # đường cong mượt qua điểm bảng (đa thức bậc 2–3 nếu
print(ch.last_fit or ch.last_method)       #  lệch ≤ max(1, 2%); không được thì nội suy đơn điệu pchip)
E.replace_path(pi, oi, path)               # thay hình đường cũ – giữ nguyên màu, độ dày, lớp
E.insert_object_after(pi, oi_mẫu, path)    # thêm đường MỚI cùng kiểu với đường mẫu
```
* `table_points` = [(lưu lượng, cột áp), ...] lấy từ bảng ĐÃ SỬA của cùng trang, đơn vị đúng trục.
* Đường mới bắt đầu và kết thúc tại điểm đầu/cuối của bảng (không kéo dài thêm).
* Nhãn đường: giữ vị trí; nếu đầu đường mới lệch > 2 pt so với đường cũ thì dời nhãn (cả bản sao
  viền trắng) theo cùng độ lệch: `T.move(match_nhãn, 0, dy)`.
* Biểu đồ trên ảnh quét: dùng `charts.color_mask` (xoá đường cũ theo màu) + `R.erase(cv, mask=...)`
  + `charts.draw_polyline(cv, page_pts, color, width_px)` – CHỈ làm khi anh đã duyệt mẫu.

## 8. Excel – `catfix.xlsx` (sửa thẳng XML, ảnh/định dạng/khổ in giữ nguyên)
```python
from catfix.xlsx import Xlsx, diff_cells, diff_parts
X = Xlsx(S.src('Catalogue DWO (bản mới).xlsx'))
X.cells('Sheet1')['A11']                 # đọc
X.replace_in_cell('Sheet1', 'A11', '1 years', '1 year')
X.set_number('Sheet1', 'C27', 0.45)      # ô có công thức dùng chung -> tự chuyển cả nhóm thành số
X.replace_font_name('.VnCooper', 'Cooper Black')
from catfix.raster import Raster, ArrayCanvas      # sửa chữ trong ẢNH nằm trong Excel
cv = ArrayCanvas.from_bytes(X.get_media('xl/media/image2.jpeg'))
R = Raster(); h = R.find(cv, 'Noiyl')[0]; R.replace_word(cv, h, 'Nylon', R.glyph_bank(cv), align='left')
X.put_media('xl/media/image2.jpeg', cv.to_bytes())
src, dst = S.src('Catalogue DWO (bản mới).xlsx'), S.dst('Catalogue DWO (bản mới).xlsx')
X.save(dst); print(diff_cells(src, dst)); print(diff_parts(src, dst))
```
Lưu ý: sheet ẩn tên `SGV` (trống) – không đụng. Sheet dữ liệu là `Sheet1`.

## 9. Kiểm tra – `catfix.verify`
```python
from catfix import verify
verify.diff_regions(src, dst)                         # {trang: [rect,...]} vùng thay đổi
verify.outside_pixels(src, dst, {trang: [rect,...]})  # điểm ảnh đổi NGOÀI vùng cho phép (phải rỗng)
verify.structure_check(src, dst)                      # số trang, khổ trang, mở được, trang nào đổi
verify.compare_sheet(src, dst, [(pi, rect, 'nhãn'), ...], S.report('So sanh Gxx.png'))
verify.page_overview(src, dst, pi, 'trang.png')       # cả trang trước | sau, khung đỏ chỗ đổi
verify.ocr_check(dst, pi, rect, '175')                # đọc lại bằng OCR
verify.text_check(dst, pi, 'irrigation', absent='irrugation')   # đọc lại lớp chữ
verify.write_report(rows, S.report('BAO CAO Gxx.md'))
```

## 10. Lỗi thường gặp
| Hiện tượng | Cách xử lý |
|---|---|
| `find` không thấy | `dump` xem chữ đọc được; chữ có thể bị tách dấu cách khác, dùng `regex` hoặc `teach` |
| Thấy nhiều chỗ | khoanh `rect=` hoặc dùng `expect=` |
| Chữ mới lệch dòng / to nhỏ khác | sai kiểu chữ nguồn: kiểm `m.glyphs[0].style`; học thêm trang có cùng chữ |
| `KeyError ... không có chữ` | không có ký tự cùng font trong file → CHƯA THỂ, báo anh |
| Ảnh quét: chữ mới mờ/đậm khác | `learn_rect` sai vùng (khác cỡ chữ) → khoanh đúng bảng chứa chữ đó |
| Hết thời gian chạy | chia nhỏ, chạy tiếp (cache giữ kết quả OCR) |
| Kết quả `check` có `unexpected` | mở `page_overview`, tìm nguyên nhân, sửa lại – không được bỏ qua |
