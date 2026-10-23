"""Inspect frozen CDX evidence and original glyph owners. Never author a PDF."""
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
import hashlib, importlib.util, json
import numpy as np
import pikepdf
import pymupdf as fitz
from PIL import Image
from catwork import start

HERE = Path(__file__).resolve().parent
S, _, _ = start()
from catfix.vector import VPage
from catfix import cs

PROJECT = Path(r'D:\ChatGPT\Sửa catalogue')
AUTHOR = Path(r'C:\Users\H2\Documents\Codex\2026-10-03\catalogue-cdx-perotac-dong-bo-do-thi')
O, W = AUTHOR/'outputs', AUTHOR/'work'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
dig = lambda b: hashlib.sha256(b).hexdigest()
J = lambda p: json.loads(Path(p).read_text(encoding='utf-8-sig'))
record = lambda p: dict(path=str(p), bytes=Path(p).stat().st_size, sha256=sha(p))
spec = importlib.util.spec_from_file_location('cdx_project_readonly', PROJECT/'tools/catalogue.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
health = C.health(); context = C.context('CDX Perotac (bản mới).pdf'); C.validate_context(context)
assert health['result'] == 'ĐẠT CẤU TRÚC DỰ ÁN'
source, current = S.src('CDX Perotac (bản mới).pdf'), S.dst('CDX Perotac (bản mới).pdf')
assert str(Path(source)) == context['source'] and str(Path(current)) == context['current']
assert context['source_sha256'] == 'ef57c37be06a3f954baac6b7549d0dda8788bf089925b6b23e68d62ed23216da'
assert context['current_sha256'] == '194a943e106e7a71426464823231494a2331c16bd74a0c3654d77a9dc888241a'
guards = {str(p): sha(p) for p in (Path(source), Path(current), PROJECT/'state/catalogues.json', PROJECT/'state/control_manifest.json', Path(context['progress_ledger']))}
frozen = {}
for name in ('cdx_uniform_76_QH_readonly_handoff_manifest.json', 'cdx_uniform_70_P45_RAM_handoff_manifest.json'):
    manifest = J(O/name)
    for a in manifest['files']:
        p = Path(a['path']); got = record(p)
        assert got['sha256'] == a['sha256'] and got['bytes'] == a['bytes'], str(p)
        frozen[str(p)] = got
    frozen[str(O/name)] = record(O/name)
qa = J(O/'cdx_uniform_68_P45_RAM_actual_QA.json')
layout = J(W/'cdx_uniform_p45_layout_source.json')
matching = J(O/'cdx_uniform_57_P4_P5_source_matching.json')
tables = J(O/'cdx_uniform_73_current_QH_tables_readback.json')
assert len(qa['checks']) == 41 and sum(qa['checks'].values()) == 40
assert qa['fail_checks'] == ['p4_source_islands_fully_inside_pixels_identical']

# The following flags record actual images ROOT opened with view_image.
# Earlier 14 images were opened in the immediately preceding continuous work;
# twelve distinct images were opened in this goal turn. This is not OCR acceptance.
reviewed = []
for page in (4, 5):
    for variant in ('source', 'RAM'):
        for dpi in (150, 600):
            reviewed.append({**record(O/f'cdx_uniform_67_P{page}_{variant}_chart_{dpi}dpi.png'),
                             'direct_view_turn': 'current' if dpi == 600 else 'previous_continuous_work'})
    for tile in range(1, 5):
        reviewed.append({**record(O/f'cdx_uniform_67_P{page}_RAM_600dpi_tile{tile}.png'),
                         'direct_view_turn': 'previous_continuous_work'})
    reviewed.append({**record(O/f'cdx_uniform_73_P{page}_current_model_QH_table300.png'),
                     'direct_view_turn': 'previous_continuous_work'})
for number in (3, 4, 5, 6):
    for variant in ('source', 'RAM'):
        reviewed.append({**record(O/f'cdx_uniform_67_P4_island_{number}_{variant}_200dpi.png'),
                         'direct_view_turn': 'current'})
assert len(reviewed) == 26 and sum(x['direct_view_turn'] == 'current' for x in reviewed) == 12

def content(p):
    v = p.obj['/Contents']; parts = list(v) if isinstance(v, pikepdf.Array) else [v]
    return b''.join(x.read_bytes() for x in parts)

owners, fresh_source_renders = [], []
ph = 841.9199829101562
with pikepdf.open(source) as src, pikepdf.open(current) as cur, fitz.open(source) as fs:
    for lp in layout['pages']:
        pi = lp['page']-1; name = lp['source_main_image_name']
        vp = VPage(cs.parse(content(src.pages[pi])))
        cv = VPage(cs.parse(content(cur.pages[pi])))
        own = [x for x in vp.images if x['name'] == name and not x.get('textclip')]
        now = [x for x in cv.images if x['name'] == name and not x.get('textclip')]
        assert len(own) == len(now) == 1 and np.array_equal(own[0]['ctm'], now[0]['ctm'])
        asset = src.pages[pi].Resources.XObject['/'+name]
        ca = cur.pages[pi].Resources.XObject['/'+name]
        assert asset.read_raw_bytes() == ca.read_raw_bytes()
        rgb = np.asarray(pikepdf.PdfImage(asset).as_pil_image().convert('RGB'))
        groups = []
        for g in lp['glyph_groups']:
            box = g['source_domain_native']; x0,y0,x1,y1 = box
            crop = rgb[y0:y1,x0:x1]
            assert crop.size and (x1-x0,y1-y0) == (crop.shape[1],crop.shape[0])
            target = g.get('target_native_origin', [x0,y0])
            groups.append({'id':g['id'], 'source_native_box':box,
                           'target_native_origin':target, 'uniform_scale':1,
                           'native_rgb_sha256':dig(crop.tobytes()),
                           'old_method_polygons_not_replayed':len(g['polygons']),
                           'clean_whole_glyph_cluster_acceptance':'NOT_RUN; requires direct cluster/background/grid examination'})
        owners.append({'page':pi+1, 'main_Do_name':name, 'main_Do_index':own[0]['i'],
                       'main_image_objgen_source':list(asset.objgen),
                       'main_image_objgen_current':list(ca.objgen),
                       'source_current_CTM_exact':True, 'CTM':own[0]['ctm'].tolist(),
                       'source_current_image_raw_exact':True, 'raw_sha256':dig(asset.read_raw_bytes()),
                       'native_RGB_dimensions':[int(rgb.shape[1]),int(rgb.shape[0])],
                       'source_RGB_glyph_domains':groups,
                       'no_new_image_or_font_stream_created':True,
                       'proposed_method':'keep original RGB clusters through clips to the existing source image Do; never fill recreated glyph polygons',
                       'ready_to_author':False})
        b = lp['whole_region_pdf_pt']; clip = fitz.Rect(b[0],ph-b[3],b[2],ph-b[1])
        pix = fs[pi].get_pixmap(dpi=600, clip=clip, alpha=False, colorspace=fitz.csRGB)
        with Image.open(O/f'cdx_uniform_67_P{pi+1}_source_chart_600dpi.png') as im:
            stored = np.asarray(im.convert('RGB'))
        arr = np.frombuffer(pix.samples,np.uint8).reshape(pix.height,pix.width,pix.n)
        assert arr.shape == stored.shape and np.array_equal(arr, stored)
        fresh_source_renders.append({'page':pi+1,'dpi':600,'stored_source_PNG_RGB_equals_fresh_original_render':True,
                                     'fresh_RGB_sha256':dig(arr.tobytes()), 'rendered_PNG_saved':False})

table_bindings = []
for mp in matching['pages']:
    tp = next(x for x in tables['pages'] if x['page']==mp['page'])
    for a, t in zip(mp['model_candidates'],tp['rows']):
        assert a['current_model']==t['model'] and a['Q_m3_h']==t['rated_Q_m3_h'] and a['H_m_table']==t['rated_H_m']
        table_bindings.append({'page':mp['page'],'model':t['model'],'rated_Q_m3_h':t['rated_Q_m3_h'],
                               'rated_H_m':t['rated_H_m'],'geometric_candidates_only':a['compatible_curve_numbers'],
                               'model_binding_acceptance':'CHƯA THỂ XÁC MINH; no automatic rank or closest-error assignment'})
assert len(table_bindings)==12
after = {p:sha(p) for p in guards}; assert guards==after
for a in frozen.values(): assert sha(a['path'])==a['sha256']

rows = [
 ['118/bổ sung','CDX Perotac','4–5','7/4 đường ảnh nguồn','7/4 đường mẫu RAM','Xem nguồn/mẫu150 và600,8mảnh600','ĐẠT RIÊNG thân nhìn thấy đồng màu/nét; không phải nghiệm thu toàn model','26 ảnh đã mở; 117 cubic có chứng cứ40/41 cũ giữ'],
 ['118/bổ sung','CDX Perotac','4–5','Chữ ảnh nguồn','Chữ tô đa giác nguồn trong mẫu RAM','So hai cặp source/RAM600 đúng nguồn thật','CHƯA ĐẠT: tiêu đề, chữ trục và số trục bị gợn; không tiếp nhận phương pháp tô đa giác','Nguồn600 RGB khớp render mới; RAM600 Performance/Flow/P/H và số'],
 ['118/bổ sung','CDX Perotac','4','Nhãn số sát đường/lưới cũ','Giữ nguyên đảo ảnh nhãn trong mẫu','Mở đủ8ảnh nhãn3/4/5/6 nguồn/RAM200 và toànchart600','CHƯA ĐẠT hình thức: còn nét đỏ/viền màu cũ cạnh nhãn2/3/4/5/6; không quy hết cho10pixel','10pixel/maxRGB1 FAIL nội nhãn của68 vẫn giữ; nguyên nhân10pixel CHƯA XÁC MINH'],
 ['118','CDX Perotac','4','Hai mã cùng ứng viên đường4','Chưa gán tên model','Đọc lại12hàng định mức hiện hành; đối chiếu57','CHƯA THỂ: 90/15 và120/15 xung đột; đường5 tạiQ4.2 lệch+1.194m soH22','Không đổi điểm định mức, không coi gần số là khóa danh tính'],
 ['118','CDX Perotac','5','5model/4đường','Cần ghi đủ tên và thêm đường thiếu','Đọc nguyên prompt G15#118; sửa cách hiểu cũ trong kế hoạch77','CHƯA XONG: prompt yêu cầu đường thứ5; không có lệnh anh cấm thêm','200/185 và185-B cùngQ12/H21; câu hỏi dữ liệu185-B đã gửi, đang chờ'],
 ['118/bổ sung','CDX Perotac','4–5','115/126 nhóm contour tô đen','Đã khóa115/126 ô RGB ảnh nguồn, chưa ghép','Đọc Do thực/X13-X19/CTM/raw ảnh; không tạoEditor/RAM','ĐẠT RIÊNG nguồn; sạch glyph/cụm và vùng lưới CHƯA KIỂM','owners trong01JSON; không dùng phông ngoài hoặc tự làm mượt lại font'],
 ['bảo toàn','CDX Perotac','1–5','Bản194a và nguồn ef57','Giữ nguyên','health/context+mã băm trước/sau+85 bằng chứng','ĐẠT giữ đầu vào; 0PDF mới/0sửa sổ/danh mục','guards_before/after; không chạy builder65 hoặc accepted_writer50'],
]
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
folder=Path(S.report_dir)/'G15'/f'ROOT CDX77 DIRECT26 FONTFAIL SOURCE RGB OWNERS NO SAMPLE {stamp}-{uuid4().hex[:6]}'
folder.mkdir(parents=False,exist_ok=False)
receipt={'scope':'CDX p4–5 actual frozen RAM graphics review + pure source RGB owners; full #118 retained',
         'captured_UTC':datetime.now(timezone.utc).isoformat(), 'overall':'CHƯA ĐẠT HÌNH THỨC; DO NOT SAVE OLD RAM METHOD',
         'new_PDF_saved':False,'new_RAM_built':False,'Editor_opened':False,'ledger_or_index_modified':False,
         'source_current_inputs':context,'health':health,'guards_before':guards,'guards_after':after,
         'frozen_files_checked':len(frozen),'frozen_files':list(frozen.values()),
         'direct_images':reviewed,'direct_current_turn':12,'direct_continuous_work_total':26,
         'fresh_original_render_confirmation':fresh_source_renders,'source_RGB_owners':owners,
         'frozen_RAM_SHA':qa['RAM_pdf_sha256'],'frozen_RAM_technical_not_rerun':{'total':41,'pass':40,'fail_checks':qa['fail_checks']},
         'body_visual_only':'PASS uniform/smooth visible parts; no model/pointwise/full-curve data acceptance',
         'recreated_native_font_visual':'FAIL jitter in titles/axes/numbers compared to actual source600',
         'source_numeric_island_old_ink_visual':'FAIL retained red fragments/coloured fringe beside labels',
         '10_interior_pixel_FAIL_cause':'UNKNOWN; no filter/ROI/threshold change',
         'job118_original_scope':'model names on all curves + draw missing fifth curve on p5; original permission present',
         'older_no_fifth_authorized_phrase':'NOT USER AUTHORITY; superseded interpretation only, original evidence left intact',
         'model_bindings':table_bindings,'original_job118_accepted':False,'original_total135_of149_unchanged':True,
         'source_glyph_method_ready':False,'source_glyph_cluster_acceptance':'NOT_RUN',
         'report_rows_8cols':rows}
jpath=folder/'01 CDX77 ROOT DIRECT26 FONTFAIL SOURCE RGB241 OWNERS.json'
jpath.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# CDX trang4–5: chữ dựng lại chưa đạt, chuyển phương pháp giữ RGB chữ nguồn','',
    'ROOT đã mở26 ảnh trong công việc liên tục, trong đó12 ảnh được mở ở lượt này. Hai ảnh nguồn600 đã đối chiếu RGB với render mới từ PDF gốc và trùng hoàn toàn. Không tạo mẫu RAM/PDF mới, không ghi bản chính, sổ hoặc danh mục.','',
    'Thân đường nhìn thấy đồng nét và mượt, nhưng chữ tô đa giác gợn rõ hơn chữ nguồn. Những đảo ảnh nhãn số còn giữ nét đỏ/viền màu của đường cũ. Mẫu này chưa đủ đẹp để tiếp nhận. Điểm ảnh nội nhãn10/maxRGB1 được giữ CHƯA ĐẠT; nguyên nhân chưa xác minh.','',
    'G15#118 thực sự yêu cầu ghi tên model theo cột áp và thêm đường thiếu trang5. Câu trong kế hoạch cũ nói chưa được phép thêm đường thứ5 là diễn giải của tác nhân, không phải giới hạn anh giao. Chưa có số đầu/cuối cho185-B hoặc khóa150/150-B; không tự chọn theo thứ tự bảng. Câu hỏi185-B đã gửi để lấy dữ liệu còn thiếu.','',
    '| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |',
    '|---|---|---|---|---|---|---|---|']
md += ['| '+' | '.join(r)+' |' for r in rows]
md += ['', 'Bước tiếp: lấy nguyên RGB cụm chữ từ đúng ảnh/Do đang hiển thị trong CDX; kiểm cả thân chữ, cỡ, nền và khoảng hở với lưới trước khi author. Không vẽ lại contour chữ, không đổi phông, không lặp builder65. Giữ đầy đủ phạm vi#118 và giới hạn dữ liệu.',
       '',f'Mã kiểm01 JSON: `{sha(jpath)}`.']
(folder/'02 BAO CAO CDX26 CHU VA NHAN CHUA DAT 8COT.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
manifest_out={'files':[record(jpath),record(folder/'02 BAO CAO CDX26 CHU VA NHAN CHUA DAT 8COT.md'),record(HERE/'root_CDX77_direct_graphics_sourceplan1.py')],
              'all_original_inputs_held':guards==after,'new_PDF_or_RAM':False}
(folder/'03 MANIFEST CHI DOC.json').write_text(json.dumps(manifest_out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert J(jpath)['source_glyph_method_ready'] is False
print(json.dumps({'folder':str(folder),'receipt_sha256':sha(jpath),'direct_images':26,'current_turn_direct':12,
                  'source_RGB_domains':[len(p['source_RGB_glyph_domains']) for p in owners],
                  'frozen_verified':len(frozen),'new_RAM_or_PDF':False,'source_current_guards_held':True},ensure_ascii=False))
