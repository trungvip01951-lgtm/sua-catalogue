"""Add an explicit correction; preserve the original receipt and its mistakes."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone

F=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G15\ROOT CDX77 DIRECT26 FONTFAIL SOURCE RGB OWNERS NO SAMPLE 20261004T052516Z-bfe615')
P=F/'01 CDX77 ROOT DIRECT26 FONTFAIL SOURCE RGB241 OWNERS.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(P)=='831b409e4f2bd981502366436c32edac23f78dbce61d8d252db37f32ad24c006'
j=json.loads(P.read_text(encoding='utf-8'))
counts=[len(x['source_RGB_glyph_domains']) for x in j['source_RGB_owners']]
assert counts==[115,123] and sum(counts)==238 and j['frozen_files_checked']==84
rows=j['report_rows_8cols']
rows[5][3]='115/123 nhóm contour tô đen'
rows[5][4]='Đã khóa238 ô RGB ảnh nguồn (115/123), chưa ghép'
rows[6][5]='health/context+mã băm trước/sau+84 bằng chứng'
assert all(len(r)==8 for r in rows)
note={'captured_UTC':datetime.now(timezone.utc).isoformat(),'original_receipt':{'path':str(P),'sha256':sha(P)},
      'correction':'Tên tệp241 và dòng báo cáo126/85 là lỗi mô tả; không đổi nội dung danh sách đo thật, không đổi nghiệm thu.',
      'actual_source_RGB_domain_counts':counts,'actual_domain_total':sum(counts),'actual_frozen_files_verified':84,
      'corrected_report_rows_8cols':rows,'original_receipt_retained':True,'new_RAM_or_PDF':False,'canonical_or_ledger_modified':False,
      'acceptance':'CHƯA ĐẠT hình thức mẫu cũ; phương án nguyênRGB mới chưa author'}
q=F/'04 DINH CHINH SO DEM THUC238 115123 FROZEN84.json'
with q.open('x',encoding='utf-8') as f:f.write(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
md=['# Đính chính số đếm của phiếu CDX77','',
    'Danh sách thực có115 ô RGB trang4 và123 ô trang5, tổng238;84 tệp chứng cứ được kiểm trong hai danh mục. Tên241 và dòng126/85 trong phiếu đầu là lỗi mô tả. Phiếu đầu được giữ nguyên để truy vết. Không tạo mẫu mới hoặc đổi kết quả nghiệm thu.','',
    '| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |','|---|---|---|---|---|---|---|---|']
md+=['| '+' | '.join(r)+' |' for r in rows]
md+=['',f'Mã kiểm phiếu gốc: `{sha(P)}`; phiếu đính chính04: `{sha(q)}`.']
r=F/'05 BAO CAO CDX26 8COT DINH CHINH238.md'
with r.open('x',encoding='utf-8') as f:f.write('\n'.join(md)+'\n')
assert sha(P)=='831b409e4f2bd981502366436c32edac23f78dbce61d8d252db37f32ad24c006'
assert json.loads(q.read_text(encoding='utf-8'))['actual_domain_total']==238
print(json.dumps({'correction':str(q),'sha256':sha(q),'md_sha256':sha(r),'counts':counts,'frozen':84},ensure_ascii=False))
