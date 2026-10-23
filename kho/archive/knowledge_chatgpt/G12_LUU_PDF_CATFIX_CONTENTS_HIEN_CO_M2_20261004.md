# G12 — lưu dữ liệu nét đã đạt vào luồng nội dung hiện có bằng CATFIX M2

**Cách M2 đã giữ được tài nguyên nghiêm ngặt trên mẫu Perotac thực. Chỉ áp dụng sau khi kiểm cấu trúc của chính tệp; chưa phải chương trình tự sửa mọi catalogue.** Ghi chú ngày 04/10/2026 cho ChatGPT và Claude dùng chung; không thay sổ tiến độ hoặc phiếu nghiệm thu cuối.

`Contents` là luồng lệnh vẽ của trang; `Ref` là mã tham chiếu đối tượng trong PDF; `Filter` là khai báo cách giải mã luồng; `raw` là byte còn nén, `decoded` là byte sau giải mã; `RAM` là bản dựng tạm trong bộ nhớ; `SHA256` là dấu kiểm nội dung.

## Lỗi M1 và thay đổi M2 có căn cứ

M1 dùng CATFIX với bộ ghi `fitz`, nạp hai luồng mới bằng `set_page_content()` rồi lưu. PDF Perotac `8d6a1aab87c5b0c65ca426f4720a133c707186fc0ecda431b2a37656793150b2` giữ đúng hai luồng nét và đạt `Job.check()`, nhưng **không đạt bộ kiểm tài nguyên nghiêm ngặt**: 18 khai báo `/Filter [/DCTDecode]` của ảnh JPEG đổi thành `/Filter /DCTDecode`. Dữ liệu ảnh không đổi vẫn không được tính là kiểm nghiêm ngặt đã đạt. Giữ mẫu lỗi và phiếu lỗi, không sửa bộ kiểm để cho qua.

M2 đổi cả cách ghi: CATFIX `Job(..., backend='pikepdf')`, gọi `set_stream()` vào **hai Ref Contents đang có 15/46**, thay vì tạo Ref Contents mới. Không chạy lại phép tạo đường/chữ/nhãn; dùng nguyên hai tệp `.bin` cuối đã kiểm. Trên mẫu Perotac thực, hai luồng trang khớp byte, 44 đối tượng tài nguyên/32 luồng ảnh và mặt nạ giữ raw+decoded, các giá trị đã phân tích/Refs/Filter arrays giữ; **không dùng ngoại lệ Filter**.

Đây là kết quả của chính mẫu này. Không suy rằng chọn `pikepdf` hoặc giữ Ref Contents tự động bảo đảm mọi catalogue sẽ giữ nguyên tài nguyên. M2 vẫn cần kiểm tệp đã lưu. Phiếu writer tại lúc lập ghi chú còn ghi chờ nghiệm thu độc lập toàn cấu trúc, hình thức và ngoài vùng; không tính toàn G12 hoàn thành, không thay trạng thái #105–#107.

## Điều kiện áp dụng trước mở lượt ghi

1. Đọc nguồn chung, BƯỚC 0/43 kiểm thử theo yêu cầu phiên; xác định bản hiện hành bằng `Session.result()` và ngữ cảnh mới. Người ghi duy nhất nhận/check khóa đúng catalogue. Khóa không tự cấp quyền sửa mới.
2. Chốt bảng số, đường, chữ, kiểu nét và vùng sửa; nghiệm thu độc lập luồng `.bin` thực và ảnh RAM. Khóa SHA nguồn, bản hiện hành, hai luồng, phương án, hàm phụ và các chứng. Không lấy tên FINAL hoặc lời báo đã đạt thay chứng.
3. Mỗi trang sửa có **đúng một Contents stream gián tiếp**, Ref chỉ dùng cho trang đó; không chia sẻ với trang khác và không nằm trong đồ thị tài nguyên ảnh/phông/Form (hình nhúng). Hai Ref của G12 Perotac khác nhau: `(15,0)` và `(46,0)`.
4. Kiểm đặc tính stream hiện có trước dùng `set_stream()`: CATFIX ghi lại dữ liệu Contents đã sửa bằng Flate và xử lý DecodeParms của stream đó. Đây chỉ là luồng trang được giao sửa, không phải tài nguyên ảnh. Nếu nhiều stream, stream trực tiếp, dùng chung, có kiểu/mối liên kết chưa đọc rõ, hoặc Ref trùng tài nguyên thì **dừng cách này**, lập phương án khác có chứng; không tự gộp hoặc ghi vào Ref ảnh.

## Phần nạp dữ liệu cần giữ nguyên cách làm

Đoạn sau chỉ minh họa bước nạp, **không tự lưu và không thay đầy đủ caller/khóa/QA**. `accepted_pages` chứa số trang bắt đầu từ 0 và byte đã khóa; `asset_refs` lấy từ đồ thị tài nguyên của bản hiện hành. Với tệp mới phải lập lại cả ngữ cảnh và chứng kiểm, không bỏ SHA trong writer cũ để chạy lại.

```python
# job = CATFIX Job(current, new_candidate, backend='pikepdf', log_path=new_log)
all_refs = [job.E.doc.page_contents_refs(pi) for pi in range(job.E.n_pages)]
flat = [tuple(ref) for refs in all_refs for ref in refs]
resources_before = [job.E.doc.page_resources(pi) for pi in range(job.E.n_pages)]
for pi, accepted_bytes in accepted_pages.items():
    refs = all_refs[pi]
    assert len(refs) == 1 and len(refs[0]) == 2
    ref = refs[0]
    assert flat.count(tuple(ref)) == 1       # không dùng chung Contents
    assert ref[0] not in asset_refs         # không sửa stream tài nguyên
    job.E.doc.set_stream(ref, accepted_bytes)
job.E.pages.clear()
assert [job.E.doc.page_contents_refs(pi) for pi in range(job.E.n_pages)] == all_refs
assert [job.E.doc.page_resources(pi) for pi in range(job.E.n_pages)] == resources_before
for pi, accepted_bytes in accepted_pages.items():
    assert job.E.doc.page_content(pi) == accepted_bytes
# Sau check khóa: job.save(); job.check(); job.evidence(...); job.close()
# Sau đó người kiểm độc lập mở chính PDF đã lưu để nghiệm thu đầy đủ.
```

CATFIX là bên ghi PDF; không gọi `pikepdf.save`, `fitz.save` hay thư viện khác trực tiếp ngoài CATFIX để sửa mẫu. Không đổi/nén lại ảnh, thay phông, dựng lại trang thành ảnh, làm mẫu từ tệp lỗi hoặc chỉnh JPEG để che khác biệt. Không tự cài hoặc sửa mã catfix/bộ kiểm.

## Kiểm bắt buộc sau lưu

- Ứng viên mới nằm trong hồ sơ riêng, cùng tên gốc. Không ghi đè nguồn, bản chính, mẫu/lỗi/log cũ. Ghi số lượt theo phương pháp thật; hai lượt cùng cách không đạt thì dừng, không chỉ đổi tên để lặp.
- Đọc lại đúng đường dẫn và SHA PDF, đủ số trang/khổ/khung; luồng Contents đã giải nén từng trang đúng nguyên byte `.bin` đã nghiệm thu. Ref Contents và các Ref khác phải được kiểm trên tệp đã lưu, không chỉ RAM.
- Chạy lại bộ kiểm tài nguyên nghiêm ngặt đang có: toàn tập node/Ref, giá trị từ điển và kiểu Filter/array, mọi luồng raw+decoded; ảnh/mặt nạ/phông/chương trình phông/Form, ma trận/clip, thông tin tài liệu, liên kết và mục lục. Không dùng so sánh Filter tương đương để thay PASS của kiểm nghiêm ngặt.
- `Job.check()` và cấu trúc phải đạt. Đăng ký đủ vùng với Job khi nạp trực tiếp luồng nội dung, vì không có recipe tự ghi `edits`; sau đó kiểm độc lập ngoài toàn hợp vùng đã khóa ở độ phân giải/ngưỡng/đệm đã chọn. Không nới vùng hoặc hạ ngưỡng sau lỗi.
- Xem ảnh mới dựng từ **PDF thực**: toàn trang và các vùng sửa, chữ nhỏ/nhãn/mép ở cỡ đủ rõ. Số và hình thức kiểm riêng. Nếu dùng lại chứng toán, phải chứng luồng nét/tài nguyên thực vẫn đúng toàn bộ, không đo lại rồi cộng số mốc thành tiến độ mới.
- Chỉ người điều phối tiếp nhận đúng byte ứng viên đã đạt sau sao lưu bản chính và kiểm trước/sau; không gọi writer lại để phát hành hoặc xuất PDF lần nữa.

**Giới hạn chữ “giữ byte”:** M2 giữ byte luồng nét đã giải nén và payload tài nguyên raw+decoded, cùng các giá trị/kiểu/Refs. Phiếu Perotac có 14 khác biệt cách ghi từ điển nhưng mọi giá trị/Refs bằng nhau theo bộ kiểm hiện hành; không tuyên bố toàn chuỗi byte từ điển hoặc toàn PDF giống trước. Không đánh đồng khác biệt cách ghi đó với lỗi đổi kiểu Filter của M1.

## Chứng cứ đã đọc và kiểm mã

| Chứng | Đường dẫn/mã |
|---|---|
| Writer M2 thực, đã đọc hết | `C:\Users\H2\Documents\Codex\2026-10-02\b-n-h-y-s-a\root_g12_save_existing_content_pike_actual_M2_1.py`; SHA `69fcb0dce198ae2550e56c46666746c8ac1965f3c4fd83631a7b7b37b297dd5d` |
| Phiếu ROOT M2 Perotac | `_BAO CAO\G12\ROOT PDF1 3M72 NHAN26 CATFIX PIKE EXISTING CONTENT M2 04-10-2026\Perotac\04 ROOT M2 ACTUAL NATIVE JOB CHECK STRICT RESOURCES NOT FINAL.json`; SHA `a48cc6be3ea2103985869acd69c3078fa645a8da35ab24ea548bed6cde9902c1` |
| Log CATFIX M2 | Cùng thư mục, `02 CATFIX M2 SAVE LOG.json`; SHA `74f969ce912d1b2519da18c872d8c56faf775bdde0eb5e619415f5defdb7d014`; sáu vùng sửa đã đăng ký |
| Mẫu M2 Perotac | Cùng thư mục, `3M Perotac (bản mới).pdf`; SHA `7e6bba2237c09bae4dcaf71c9ac0dc26ce4feddaf925745a20813e32829c3639` |
| Hai luồng nét cuối | Trang 1 SHA `38842f5e2c0485f28aaf9180d747109812b298c5c7bbf1523dd684e935188d45`; trang 2 SHA `b5fba802c76c3a666c2c1f088145dcbb0355a61fa56eae375a8285d6aa7f6b4f` |
| Lỗi M1 giữ nguyên | `_BAO CAO\G12\ROOT PDF1 3M72 NHAN26 CATFIX FITZ 04-10-2026\Perotac\04 FAILURE KEEP SAMPLE NO AUTOMATIC RETRY.json`; mẫu `8d6a1aab…` không được đổi thành strict PASS |
| Đọc đủ 44 tài nguyên/18 Filter khác của M1 | `_BAO CAO\G12\DOC LAP PEROTAC PDF1 TOAN44 RESOURCE FILTER19 KHONG RETRY 20261004T022538Z-477131\01 DOC THUC44 RESOURCE TAT CA DELTA VA FILTER19 RUNTIME.json`; SHA `94e558b23232d9d0ef25ed8e423ab17ad8c5f4194c33392fa1ff7ad089effe9c` |

`_BAO CAO` ở thư mục đầu ra theo `manifest.json`. Người lập ghi chú: tác nhân ChatGPT `next_work_scope`, chỉ đọc writer/phiếu/log và ghi tài liệu này; không chạy writer, không lưu catalogue, không thay sổ/chỉ mục/bản chính hoặc thư mục bộ nhớ riêng. Aquaris M2 và nghiệm thu PDF cuối là phần việc của ROOT/QA, đọc chứng mới trước kết luận.
