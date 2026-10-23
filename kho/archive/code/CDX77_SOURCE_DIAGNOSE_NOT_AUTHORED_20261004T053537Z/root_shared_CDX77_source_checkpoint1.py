"""Save current evidence, failed method and next action for both AIs. No catalogue write."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil

P=Path(r'D:\ChatGPT\Sửa catalogue'); W=Path(__file__).resolve().parent
J=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=J(P/'manifest.json');R=Path(M['paths']['reports'])
F=R/'G15/ROOT CDX77 DIRECT26 FONTFAIL SOURCE RGB OWNERS NO SAMPLE 20261004T052516Z-bfe615'
CDLF=R/'G16/G03 CDLF101 ALL24 SOURCE NATIVE WORDS BEFORE CTM NO SAMPLE 20261004T051453Z-fee629'
DWO=R/'G18/DWO7 MODEL14 MIN VA BO CUC CHUA UI CHECKPOINT 20261004T045249Z-3433c0'
guards={str(p):sha(p) for p in (P/'state/catalogues.json',P/'state/control_manifest.json',Path(M['paths']['progress']))}
assert sha(P/'state/catalogues.json')=='ba655ad04b012e388e7209cad669ba494dbb61ddbc7466169d0c1735dd75e4f5'
assert sha(Path(M['paths']['progress']))=='f0d9a2a9943c5f9c53b5764b883556403a13ce61b06d1ea1cf2b75b5f1658115'
assert sha(P/'state/control_manifest.json')=='437f067cfb4c220cb460dac9cecbc8862c170e4bf1b3f9ae53b6155b7ec4ed82'
references=[
 (F/'01 CDX77 ROOT DIRECT26 FONTFAIL SOURCE RGB241 OWNERS.json','831b409e4f2bd981502366436c32edac23f78dbce61d8d252db37f32ad24c006'),
 (F/'04 DINH CHINH SO DEM THUC238 115123 FROZEN84.json','f49a8aa1df91b0cddf9f88ff6001058b2d99e4281587ae13d43f614d2d031363'),
 (F/'05 BAO CAO CDX26 8COT DINH CHINH238.md','890b7aa7a0bad0030f21018a752786df2a294b42c29c89dd1f32dbf7c99785b1'),
 (CDLF/'04 FINAL F FONT SOURCE24 NO SAMPLE.json','544d573f611e01638be4c846c56b913483f9b59a2f322a7e9fdfafb86682beee'),
 (CDLF/'05 FINAL F NGUON24 BAO CAO8 COT.md','0e42e4cd4ab75d227f3a47b248fbddd9a8cd1f4708a40e66daf44321b3ec91ad'),
 (DWO/'01 DWO7 MIN14 SOURCE DOCS PRINTAREAS PACKAGE ONLY.json','d8be09622f285b399b1d9f549887003dd0ec8924c50f9f3bec7821378a30da45'),
]
for q,h in references:assert sha(q)==h,str(q)
cdx=J(references[0][0]);norm=J(references[1][0])
assert norm['actual_source_RGB_domain_counts']==[115,123] and cdx['source_glyph_method_ready'] is False
index=J(P/'state/catalogues.json')
for a in index['catalogues']:
 assert sha(Path(M['paths']['source'])/a['source_relative'])==a['source_sha256']
 assert sha(Path(M['paths']['output'])/a['current_relative'])==a['current_sha256']

stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
archive=P/'archive/code'/('CDX77_SOURCE_DIAGNOSE_NOT_AUTHORED_'+stamp)
archive.mkdir(parents=True,exist_ok=False)
copies=[]
for name in ('root_CDX77_direct_graphics_sourceplan1.py','root_CDX77_normalize_receipt1.py','root_shared_CDX77_source_checkpoint1.py'):
 src=W/name; dst=archive/name; assert not dst.exists();shutil.copyfile(src,dst);assert sha(src)==sha(dst)
 copies.append({'source':str(src),'archive':str(dst),'sha256':sha(dst),'executed_one_shot_not_replayable':True})
aman=archive/'MANIFEST_CODE_ONLY_DO_NOT_RUN.json'
with aman.open('x',encoding='utf-8') as f:json.dump({'scope':'read-only diagnosis and source evidence code; no accepted authoring method','files':copies},f,ensure_ascii=False,indent=2)
update=P/'state/updates'/('20261004-CDX77-FONTFAIL-CDLF24-DWO14-'+stamp+'.md')
text='''# Mốc tiếp tục: CDX chữ nguồn, CDLF F và DWO thiếu số

Không có catalogue mới được tiếp nhận trong mốc này. 135/149 việc gốc giữ. Danh mục25 nguồn và25 bản đã lưu được đối chiếu mã thực, không đổi; sổ, danh mục và khóa luật giữ. Các phần WC/CM/CDLF/3M/SL6SL25 đã đạt không làm lại. Mốc này bổ sung chẩn đoán và chuyển phương pháp, không thay quyền anh hoặc nghiệm thu.

| Phạm vi | Bằng chứng mới | Trạng thái và bước tiếp |
|---|---|---|
| CDX trang4–5 | ROOT mở26 ảnh liên tục (12 ảnh lượt hiện tại); hai ảnh nguồn600 khớp RGB render mới từ PDF gốc. 117 đoạn cong của mẫu RAM có hồ sơ40/41 kiểm kỹ thuật; màu/nét thân nhìn thấy đồng bộ | Chữ tiêu đề/trục/số tô lại bằng đa giác bị gợn so nguồn; đảo ảnh nhãn còn nét đỏ/viền màu cũ. CHƯA ĐẠT hình thức, không lưu/tiếp nhận RAM cũ |
| Chữ CDX | Đọc Do X13/X19, CTM và byte ảnh nguồn/current giữ;115 ô chữ trang4+123 trang5=238 ô RGB được khóa nguồn. Chưa ghép cụm, chưa author | Dùng nguyên RGB cụm chữ từ chính ảnh/Do nguồn qua phép cắt; giữ font/cỡ/AA, kiểm cả nền/lưới/khoảng hở. Không tô lại contour hoặc làm mượt glyph. Bộ nguồn mới chưa sẵn sàng author |
| CDX#118 | Đọc đầy đủ prompt G15: ghi tên model theo cột áp và vẽ thêm đường thiếu trang5. Hai mã185/185-B cùngQ12/H21;150/150-B cùngQ10/H20. Trang4 còn xung đột ghép đường4, đường5 lệch+1.194m tạiQ4.2/H22 | Câu cũ “không được thêm đường thứ5” là diễn giải của tác nhân, không phải lệnh anh. Giữ đầy đủ phạm vi#118. Câu hỏi185-B dùng chung đường hay số đầu/cuối riêng đã gửi, còn chờ. Không tự chọnB theo thứ tự bảng/khối lượng |
| CDLF#101 | Đã đọc đủ24 trang nguồn,242/256 ứng viênF đã nhận diện khác kiểu;14cropRGB nguồn mở trực tiếp; nhãnCDL xoay có chân cong, F tìm được không chân. Ma trận ngoài tỉ lệ đều, không tự bóp ngang | 16 nhãn xoay giữ; CHƯA THỂ F nguyên cùng kiểu. Phần nhận dạng ảnh và trang12raster có giới hạn nên không kết luận toàn tệp không cóF. Không dùng font khác, không ghép chữ từ bộ phận rời |
| DWO Excel | Đã kiểm thêm3 workbook gốc không cóQmin/Hmin;7mã thiếu14 số. Mẫu khungcd2f978e đã lưu và kiểm20 phần/59 ô/3 ảnh, khungB38:S67,2vùng in; khoảnghở ảnh tối thiểu12.044pt theoXML | Mẫu chưa nhận bản chính. Không tạo điểm0/min/duty giả. G18#123 thực sự yêu cầu kiểmPDF/bản in: XML chưa chứng đủ2trang hoặcFan cover trêntrang1. Câu hỏi số nhỏ nhất vẫn chờ; không hỏi lại điểm làm việc chưa rõ |
| SL ngoài6SL25 | 5chart/565ô nguồn đã đọc;21cặp bằng cần đối chiếu đường và làm tròn. Phương án toán3SL4 giữ70số/đầu-cuối,7đường/C1; chưa author. ROOT mở7crop nhãn900, suffix thấp vẫn mờ | Tiếp tục khóa đúng model từ≥2mốcQH nhìn thấy và các hàng nguồn, không chọn theo rank. Tách ngưỡngcontrast tự đặt khỏi yêu cầu anh; phép thửFAIL cũ vẫn giữ. 11chart chưa kiểm mới vẫn nằm trong phạm vi |

Những lỗi cần tránh:

1. Đừng dùng diện tích nét hoặc số nhóm để kết luận cùng kiểu chữ. Mẫu CDX tô contour đạt kiểm cấu trúc vẫn bị gợn rõ ở tiêu đề, trục và số. Cần mở ảnh thật ở cỡ xem/in và phóng lớn so nguồn.
2. Giữ nguyên cả hình chữ nhật nguồn quanh nhãn có thể giữ luôn nét đỏ/lưới cũ. Vùng có chữ phải kiểm mực cũ ngoài thân glyph và khoảng hở thật, không chỉ checksum ảnh hoặc “island preserved”.
3. Chọn ảnh theo thứ tựDo phải xét clip thật, nhất làTr7 (cắt ảnh theo chữ ẩn). Hai ảnh toàn trang gần cùngCTM không chứng ảnh vẽ sau che toàn ảnh trước. SPp4 đang điều tra clip chữ6SP của/X6; không coi kết luận sơ bộ về/X5 bị che là đã xác minh.
4. Chuỗi model trùng điểm làm việc không chứng cùng toàn bộ đường. Ghép theo cột áp là yêu cầu, nhưng bảng/ảnh không tự cung cấp số đầu/cuối còn thiếu.
5. Phiếu CDX đầu có tên241 và dòng126/85 sai mô tả. Dữ liệu danh sách thật là115/123=238 ô và84 tệp kiểm. Đính chính04 và báo cáo05 là phiên dùng đọc; phiếu01 vẫn giữ nguyên để truy vết.

Nguồn hồ sơ:

'''
text+='\n'.join('- '+str(q)+' | SHA-256 '+h for q,h in references)
text+='\n\nMã chỉ đọc đã chép vào '+str(archive)+'. Các chương trình đã chạy và có tên tệp/hàm chạy ngay; không chạy lại hoặc bỏ khóa băm. SHA-256 là mã kiểm nội dung; RGB là ba thành phần màu; CTM là ma trận đổi tọa độ; Do là lệnh vẽ ảnh; Tr7 là chế độ dùng chữ làm vùng cắt; RAM là bộ nhớ; XML là cấu trúc dữ liệu trong Excel.\n'
with update.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
cp=P/'state/CURRENT_CHECKPOINT.md';before=sha(cp)
backup=P/'history'/('CURRENT_CHECKPOINT-before-CDX77-source-'+stamp+'.md')
assert not backup.exists();shutil.copyfile(cp,backup);assert sha(backup)==before
addition='\n\n## Mốc chẩn đoán chữ và nguồn sau SL6SL25\n\nĐọc [mốcCDX/CDLF/DWO mới](updates/'+update.name+') trước dùng các dòng lịch sử vềCDX không thêmđường5. PromptG15#118 yêu cầu đủ tênmodel vàđườngthiếu; câu diễn giải cũkhông thay quyềnanh. CDX26ảnh cho thấy chữcontourgợn vànhãn cònmực cũ, chưanhậnRAM; nguyênRGB238ô đangchuẩn bị. CDLF đãđọc24trang nhưngF cùngkiểu vẫnchưacó chứng. DWO14sốmin vàbảnin vẫnchờ/CHƯATHỂ. Khôngcatalogue,sổ,danhmụcnào đổi;135/149gốc giữ.\n'
with cp.open('a',encoding='utf-8',newline='\n') as f:f.write(addition)
assert cp.read_text(encoding='utf-8').endswith(addition)
assert {p:sha(p) for p in guards}==guards
receipt={'time_UTC':datetime.now(timezone.utc).isoformat(),'shared_update':str(update),'update_sha256':sha(update),
         'checkpoint_sha256':sha(cp),'checkpoint_backup':str(backup),'checkpoint_backup_sha256':sha(backup),
         'archive_manifest':str(aman),'archive_manifest_sha256':sha(aman),'code_copies':len(copies),
         'guards_before_after_held':guards,'catalogue_or_ledger_or_index_writes':0,'all25sources_and25current_files_held':True,
         'original_jobs_completed_now':0,'goal_complete':False}
out=F/'06 ROOT SHARED CHECKPOINT CDX77 SOURCE NO CATALOGUE WRITE.json'
with out.open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
assert J(out)['catalogue_or_ledger_or_index_writes']==0
print(json.dumps({'receipt':str(out),'receipt_sha256':sha(out),'update':str(update),'checkpoint_sha256':sha(cp),'no_catalogue_ledger_index_write':True},ensure_ascii=False))
