"""Accept the reviewed SL supplement and adopt exact CATFIX bytes once, with backups.
Preserve the separate failed numeric-reference and source-frame diagnostics.
Never export a PDF; never alter originals or weaken the frozen outside mask.
"""
from pathlib import Path
from datetime import datetime
import hashlib,json,os,shutil,importlib.util
from catwork import start,fresh,HERE

S,_,_=start()
P=Path(r'D:\ChatGPT\Sửa catalogue')
R=Path(S.report('G04'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text(encoding='utf8'))

def write_new(p,obj):
    p=Path(fresh(p))
    with p.open('x',encoding='utf8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
    assert read(p)==obj
    return p

spec=importlib.util.spec_from_file_location('SL_root_coordinator',P/'tools/catalogue.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
rel='Giếng/Redpump gieng SL_compressed (bản mới).pdf'
ctx=C.context(rel);C.validate_context(ctx)
source=Path(S.src('Redpump gieng SL_compressed (bản mới).pdf'))
current=Path(S.dst('Redpump gieng SL_compressed (bản mới).pdf'))
assert source.resolve()==Path(ctx['source']).resolve() and current.resolve()==Path(ctx['current']).resolve()
source_sha='a01b7f84c0ebb4960a6b9601d98a04420c4c00f8bf1d48a23e1bde4e8b084038'
old_sha='b7c1febb60e0ebfcb88d233f87d8e10d0c0e5886214acc98e6f5cc2b2d32d435'
candidate=R/'ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE 20261004T041608Z-5ddd0c'/current.name
candidate_sha='ddb0bc676409b0078e62a8ed44ece585bc2e6bba3ae3a4fac3f2ece5ef85a0ae'
native_sha='7184d01f463d8eccfd5d1a85893850b7fd6d285f2d7c0edc36cf0ec8208606ee'
assert sha(source)==source_sha and sha(current)==old_sha and sha(candidate)==candidate_sha
assert current.resolve().is_relative_to(Path(S.out_dir).resolve())
assert not current.resolve().is_relative_to(Path(S.in_dir).resolve())
assert candidate.resolve().is_relative_to(R.resolve())
index=P/'state/catalogues.json';ledger=Path(S.report('TIEN DO.md'));seal=P/'state/control_manifest.json'
index_sha='93a91d990b21ddb015c57822612c98ea3f1814c07cf0b339343f4596a2118f3c'
ledger_sha='e1358a9867cf4301c9240e144dae13e74b535b17599c812980c04de3262b747f'
seal_sha='437f067cfb4c220cb460dac9cecbc8862c170e4bf1b3f9ae53b6155b7ec4ed82'
assert sha(index)==index_sha and sha(ledger)==ledger_sha and sha(seal)==seal_sha
before=read(index);assert before['catalogue_count']==25 and not C.controls()['changed']
for r in before['catalogues']:
    assert sha(Path(S.in_dir)/r['source_relative'])==r['source_sha256']
    assert sha(Path(S.out_dir)/r['current_relative'])==r['current_sha256']

evidence_specs=[
 ('graph','DOC LAP SL SAVED BIJECTION RAW GRAPH STRICTREF FAIL 20261004T042831Z-587252/01 SL SAVED ACTUAL REF BIJECTION DICT RAW DECODED NEW38.json','ef6f23698d318eb13752fb1e36348be5be076c05b951486973c6cc35655746ef'),
 ('native','DOC ACTUAL SL20 PATH40 CUBIC120 TABLE10 LABEL CHI DOC 20261004T043002Z-0369bb/01 ACTUAL SL NATIVE20 PATH40 CUBIC10 CAPTIONS120 TABLE ONLY.json','d229b0d4aac55926c8725c6bb362dfc715d671b042481dfb128d839de1edb79c'),
 ('outside','ROOT SL ACTUAL SAVED4 CROP11 OUTSIDE AND LITERAL META DELTA 20261004T042339Z-4bb725/05 ROOT ACTUAL SL4 CROP11 OUTSIDE TABLE120 READBACK.json','3bd4cc9adcdd0fa164f75c6a0b37d1db699fdcecc13a5ae8a7b9b4a8376df99e'),
 ('graphics','G03 SL ACTUAL SAVED4 DIRECT HEAD10 BODY10 LABEL10 AXIS PASS 20261004T042810Z-c87491/01 ACTUAL SAVED4 DIRECT GRAPHICS RGB NATIVE EXACT COREFAIL RETAINED.json','a28a2c37217cab40c81c4a7ab7fae0ca0c09f371141b63a7556598e4a708f397'),
 ('frame','G03 SL M2 CORE67 CROP13 EXACT CTM BODY FOOTPRINT NOTE 20261004T042312Z-5910f3/01 SL M2 CORE67 CROP13 ORIGINAL CTM BODY ROI POINTS NO RENDER.json','af9483f2c7189cd8f47b2b1c23883496a20f844c60a10f2e32b6894e537b7452'),
 ('failed_save_gate','ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE 20261004T041608Z-5ddd0c/99 FAILURE RETAIN SAMPLE DO NOT AUTOMATICALLY RETRY.json','1e92fbf4c1a49bae5537416141bc73002254aa3e59352ecc7a0bd22e80225e94'),
 ('math','G03 SL10 C2 DOC LAP FRACTION40 JOIN30 TABLE120 CHUA RAM 20261004T032612Z-b7e46e/01 DOC LAP SL10 C2 FRACTION40 JOIN30 TABLE120 PLAN PASS NO RAM.json','b621ec6f19ed0849294156df2abe339528078f8251306f97b672904887f097dc'),
]
E={};proofs=[]
for kind,relative,expected in evidence_specs:
    p=R/relative;assert sha(p)==expected,(kind,p)
    E[kind]=read(p);proofs.append(dict(kind=kind,path=str(p),SHA256=expected))
g,n,o,v=E['graph'],E['native'],E['outside'],E['graphics']
assert g['candidate_sha256']==n['candidate_SHA256']==o['candidate_SHA256']==v['candidate']['sha256']==candidate_sha
assert g['semantic_current_ref_bijection_complete'] and g['reverse_bijection_one_to_one']
assert g['aliases_and_shared_edges_preserved'] and g['all_errors']==[]
assert g['snapshot_scope_counts']['old_pdf_object_count']==128 and g['snapshot_scope_counts']['actual_pdf_object_count']==178
assert g['snapshot_scope_counts']['all_saved_indirect_objects_exactly_classified_as_old_or_expected_new50']
assert len(g['old_current_streams_checked'])==75 and len(g['new36_M2_raw_decoded_stream_checks'])==46
assert len(g['actual39_40_frozen_raw_decoded_dictionary_filter_SMasks'])==4
assert g['Info_XMP_Root_pageboxes_links_toc_metadata_typed_graph_checked']
renumbered=sum(row['old']!=row['actual'] for row in g['oldRef_to_actualRef_one_to_one']);assert renumbered==31
assert g['strict_literal_numeric_Ref_gate']=='FAIL_RETAINED'
assert n['native_SHA256']==o['actual_native_SHA256']==native_sha
assert n['counts']=={'curves':10,'painted_parts':20,'cubics':40,'joins':30,'numeric6b_anchors':120,'table_changed':26,'table_held':94,'caption10':10,'Do_names':42}
assert len(n['curves10'])==10
for curve in n['curves10']:
    assert curve['same_own_source_pen_dash_color_cap_join'] and curve['CTM_identity']
    assert curve['literal_controls_within_half_Num20'] and curve['derivative_strict_fall_Q_strict_rise_actual']
    assert len(curve['numeric12_actual'])==12 and all(a['PASS'] for a in curve['numeric12_actual'])
    assert len(curve['joins3_actual'])==3 and all(j['C0_literal_exact'] and j['absolute_both_below_1e_minus18'] for j in curve['joins3_actual'])
assert n['actual_max_numeric6b_ratio']<1 and n['native_names42_resolve']
assert len(n['caption10_source_payload_and_CTM'])==10 and len(n['table26_actual_patch_payload_and_CTM'])==26 and len(n['source94_cells_transfer_proof'])==94
assert len(o['outside11pages200'])==11
assert all(a['outside_changed_pixels']==0 and a['dpi']==200 and a['threshold']==0 and a['additional_pad']==0 and a['original_ROI_held'] for a in o['outside11pages200'])
assert len(o['crops4'])==4 and all(a['changed_pixels_vs_same_M2_RAM']==0 and a['from_actual_saved_PDF'] for a in o['crops4'])
assert len(o['table120_RGB3_resolutions'])==3 and all(a['changed_pixels_vs_table120_accepted_oldM2']==0 for a in o['table120_RGB3_resolutions'])
assert o['metadata_matches_current_literal'] is False and list(o['metadata_literal_deltas'])==['bookmarks']
assert v['overall']=='ACTUAL_SAVED_GRAPHICS_SCOPE_PASS; STRICT_SOURCE_FRAME_PIXEL_FAIL_RETAINED; FULL_G04_NOT_ACCEPTED'
assert len(v['photos4_direct_view_and_independent_RGB'])==4 and all(a['direct_view_this_turn'] and a['independent_decoded_RGB_changed_pixels']==0 for a in v['photos4_direct_view_and_independent_RGB'])
assert v['strict_source_frame_pixel_comparison_retained']['fullpage_core_counts150_200_600']==[23,44,0]
assert v['strict_source_frame_pixel_comparison_retained']['fullpage_max_RGB_delta']==[1,8,0]
assert v['strict_source_frame_pixel_comparison_retained']['FAIL_at150_200'] is True
for a in o['crops4']:assert sha(a['path'])==a['SHA256']

F=Path(S.report('G04/SL6SL25 C2 DA LUU NGHIEM THU PHAM VI BO SUNG 04-10-2026'))
assert not F.exists();F.mkdir(parents=True)
gate=dict(status='ROOT_ACCEPTS_SAVED_SL6SL25_SUPPLEMENT_ONLY_WITH_DIAGNOSTIC_FAILS_RETAINED',
 time=datetime.now().astimezone().isoformat(),source=str(source),source_SHA256=source_sha,current=str(current),old_current_SHA256=old_sha,
 candidate=str(candidate),candidate_SHA256=candidate_sha,accepted_native_SHA256=native_sha,
 authority='User requested Q increasing/H decreasing, uniform smooth redrawing and all discovered errors; active user goal explicitly grants full authority to redraw catalogue/curves and fix images. Later authority overrides old per-sample confirmation within this scope.',
 requirements_basis=[
  'PROMPT CHUNG6b: lệch mỗi điểm không quá max(1 đơn vị,2%); cùng màu/cùng độ dày; thay đúng đường cũ.',
  'PROMPT CHUNG6c: bắt đầu/kết thúc tại điểm đầu/cuối bảng.',
  'PROMPT CHUNG nghiệm thu2: vùng cho phép gồm hộp chỗ sửa và biểu đồ vẽ lại; outside đã khóa200/ngưỡng0/đệm0 giữ nguyên.',
  'PROMPT CHUNG4: không xoá thông tin tài liệu/liên kết/mục lục. Entire old typed graph and raw streams were verified via exact bijection, not by ignoring dictionary differences.'
 ],
 actual_numeric_table_geometry_PASS=True,actual_graphics_PASS=True,actual_outside_frozen_regions_PASS=True,
 semantic_old_resource_content_metadata_preserved_PASS=True,
 literal_numeric_object_ID_preservation='FAIL_RETAINED_31_RENUMBERED_NOT_CLAIMED_IDENTICAL',
 literal_bookmark_xref_identity='FAIL_RETAINED_7_RENUMBERED_DESTINATIONS_AND_METADATA_VALUES_PRESERVED',
 trailer_deltas=g['trailer_deltas_recorded_not_called_old_resource_deltas'],
 source_frame_pixel0='FAIL_RETAINED_23_44_0_FULLPAGE_CORE_WITH_MAX_RGB1_8_0; crop4_9_0_max1_1_0',
 acceptance_boundary='Internal numeric IDs and pixels inside the authorized chart are not additional user requirements. This accepts preserved resource content/destinations and independently observed original axis geometry/style. It DOES NOT change failed diagnostic outcomes, thresholds, mask, renderer, or metadata claims.',
 forbidden_claims=['All numeric references stayed identical','All source-frame pixels stayed identical','All metadata dictionaries including numeric xrefs literal-identical','All G04 or all SL curves complete','All anchors below1m','Manufacturer physical extrema inferred'],
 original149_accepted_count=135,full_G04_complete=False,full_SL_complete=False,full_goal_complete=False,
 remaining='Other SL diagrams/tables/captions and full catalogue scope remain;21 equal table pairs outside6SL25 still require assessment.',
 counts=n['counts'],index_before_SHA256=index_sha,ledger_before_SHA256=ledger_sha,seal_SHA256=seal_sha,
 evidence=proofs,new_RAM_samples=0,new_PDF_saves=0)
gate_path=write_new(F/'01 ROOT CONG NGHIEM THU ACTUAL SL10 VA GIOI HAN.json',gate)
actor,session='ROOT','root-SL6SL25-C2-actual-adopt-20261004'
claim=C.claim(rel,actor,session,'Tiếp nhận đúng byte mẫu CATFIX SL6SL25 đã kiểm số/đồ họa/toàn vẹn; sao lưu hiện hành; không sửa nguồn',3600)
try:
    C.check(claim['token'],actor,session)
    backup=Path(fresh(F/'BAN TRUOC'/current.name));shutil.copyfile(current,backup);assert sha(backup)==old_sha
    lb=Path(fresh(F/'TIEN DO TRUOC TIEP NHAN.md'));ib=Path(fresh(F/'DANH MUC TRUOC TIEP NHAN.json'))
    shutil.copyfile(ledger,lb);shutil.copyfile(index,ib);assert sha(lb)==ledger_sha and sha(ib)==index_sha
    stage=current.with_name('.CHATGPT_SL6SL25_DA_NGHIEM_THU_20261004.pdf');assert not stage.exists()
    with stage.open('xb') as f:
        with candidate.open('rb') as src:shutil.copyfileobj(src,f)
    assert sha(stage)==candidate_sha
    write_new(F/'02 ROOT SAO LUU VA STAGE DUNG BYTE TRUOC TIEP NHAN.json',dict(gate=str(gate_path),gate_SHA256=sha(gate_path),source_SHA256=sha(source),old_current_SHA256=sha(current),candidate_SHA256=sha(candidate),backup=str(backup),backup_SHA256=sha(backup),stage=str(stage),stage_SHA256=sha(stage),ledger_backup=str(lb),ledger_backup_SHA256=sha(lb),index_backup=str(ib),index_backup_SHA256=sha(ib)))
    for p in proofs:assert sha(p['path'])==p['SHA256']
    C.check(claim['token'],actor,session)
    assert sha(index)==index_sha and sha(ledger)==ledger_sha and sha(source)==source_sha and sha(current)==old_sha and sha(stage)==candidate_sha
    os.replace(stage,current)
    assert sha(current)==sha(candidate)==candidate_sha and sha(backup)==old_sha
    for r in before['catalogues']:
        assert sha(Path(S.in_dir)/r['source_relative'])==r['source_sha256']
        assert sha(Path(S.out_dir)/r['current_relative'])==(candidate_sha if r['source_relative']==rel else r['current_sha256'])
    assert sha(seal)==seal_sha and not C.controls()['changed']
    report=Path(fresh(F/'03 BAO CAO8 COT SL6SL25 C2 DA LUU NGHIEM THU.md'))
    report_text='''BÁO CÁO G04 – phần bổ sung 6SL25 Redpump, trang 10 đã lưu

| # việc | File | Trang | Cũ | Mới | Cách sửa/kiểm | Kết quả | Bằng chứng |
|---|---|---|---|---|---|---|---|
| Quy tắc Q–H bổ sung | Redpump SL | 10 | Bảng có đoạn bằng hoặc tăng ngược, đường cũ chưa mượt/khớp đủ mốc | 10 đường giảm liên tục, cùng màu/nét, 40 đoạn cong nối mượt | Đọc 20 đối tượng đường thật, 40 đoạn, 30 chỗ nối; kiểm đạo hàm toàn miền và 120 mốc trên PDF đã lưu | ĐẠT dung sai max(1 đơn vị, 2%); không nhận mọi mốc lệch dưới 1 m | Phiếu lệnh vẽ d229b0d và toán b621ec6 |
| Bảng Q–H bổ sung | Redpump SL | 10 | 120 ô nguồn | 26 ô sửa dạng nguyên, 94 ô giữ; 110 cặp giảm | Giữ mức lớn nhất/nhỏ nhất trong bảng và dải Q0–33; đầu mới 5 hàng bằng mức lớn nhất đã có trong chính hàng nguồn | ĐẠT theo bảng đã khóa; không suy cực đại/cực tiểu vật lý hoặc điểm định mức ngoài nguồn | Phiếu d229b0d; phương án a12f601 |
| Nhãn và khung | Redpump SL | 10 | Mực đường cũ ở đầu/nhãn cần dọn | Đủ 10 nhãn chữ nguồn sạch, khung liền nét, đầu/thân 10 đường đồng bộ | Tự xem toàn biểu đồ ở 600 điểm/inch; đồ họa độc lập mở đủ 4 ảnh từ chính PDF đã lưu; giữ dữ liệu ảnh nhãn/mặt nạ/ma trận | ĐẠT hình thức; có giới hạn nguồn ảnh quét 150 điểm/inch | Phiếu đồ họa a28a2c3 |
| Ngoài vùng | Redpump SL | 1–11 | Chỉ cho phép vùng biểu đồ đã khóa và 26 ô | 10 trang khác giống toàn ảnh; ngoài vùng trên đủ 11 trang không đổi điểm ảnh | 200 điểm/inch, ngưỡng 0, không đệm thêm; không nới vùng sau lỗi | ĐẠT 0 điểm ngoài vùng | ROOT 3bd4cc9 |
| Tài nguyên/thông tin | Redpump SL | Toàn tệp | 128 đối tượng/75 luồng trong bản giao trước | 128 đối tượng giữ nội dung và quan hệ; thêm 50 đối tượng dự kiến; phân loại đủ 178 đối tượng | Đối chiếu hai chiều 1–1, kiểu từ điển/ảnh/mặt nạ/nén/dữ liệu thô/giải mã/khổ/liên kết/mục lục; 74 luồng cũ nguyên, 1 luồng trang 10 thay đúng mẫu | ĐẠT bảo toàn nội dung; không nhận số định danh bất biến | Phiếu tài nguyên ef6f236 |
| Số định danh nội bộ | Redpump SL | Toàn tệp | Số định danh 128 đối tượng cũ | 31 số định danh đổi; 7 số mục lục đổi; định danh tệp thứ hai và số đối tượng trong phần tổng kết tệp đổi | Kiểm ánh xạ cùng nội dung/mục đích; giữ lỗi cổng so số định danh cũ | CHƯA ĐẠT phép so số định danh nguyên; không phát hiện mất dữ liệu. Đã khai báo, không sửa báo cáo lỗi | ef6f236; phiếu 99 lỗi gốc giữ |
| Điểm ảnh khung | Redpump SL | 10 | Khung nguồn | Lõi khung ảnh cắt 4/9/0; toàn trang 23/44/0 tại 150/200/600; chênh màu lớn nhất toàn trang 1/8/0 | Các điểm khác giao vùng biểu đồ nguyên; ảnh nguồn/ma trận giữ; trục nhìn liền, đúng màu/đậm/vị trí. Nguyên nhân dựng ảnh bên trong chưa đo riêng | CHƯA ĐẠT phép so điểm ảnh khung bằng 0 ở 150/200; không nâng ngưỡng/bỏ mép | af9483f; d6aaa7c; đồ họa a28a2c3 |
| Phạm vi còn lại | Redpump SL/G04 | Toàn tệp | Các đồ thị/bảng khác còn việc bổ sung | Chỉ nhận 6SL25 trang 10, giữ phần gốc đã đạt | Phần bổ sung không cộng 149 việc gốc; chưa nhận toàn SL/G04 | CHƯA XONG toàn phạm vi; 135/149 gốc giữ | Sổ TIEN DO và cổng ROOT 01 |

Nguồn 25 catalogue không đổi; 24 bản giao khác giữ. Bản SL trước, sổ và danh mục được sao lưu nguyên byte. Bản giao nhận đúng byte ứng viên CATFIX ddb0bc676409, không xuất lại PDF. Ngoài vùng giữ đúng mặt nạ và ngưỡng đã khóa. Các phép kiểm số định danh và điểm ảnh khung thất bại vẫn là CHƯA ĐẠT trong hồ sơ.

Điều kiện nghiệm thu của anh là nội dung và hình thức bảo toàn ngoài vùng được phép; đường giảm, mượt, đồng bộ, khớp bảng; trang/thông tin/liên kết/mục lục giữ chức năng và giá trị. Phép kiểm bảo toàn nội dung qua ánh xạ đầy đủ độc lập không bỏ hoặc chuẩn hóa sai khác từ điển. Số định danh nội bộ và điểm ảnh trong vùng biểu đồ sửa được khai báo riêng; không nới vùng hoặc ngưỡng để gọi chúng là đạt.

Giải thích: Q là lưu lượng, H là cột áp; ID là số định danh nội bộ; raw là dữ liệu thô; RGB là ba thành phần màu; trailer là phần tổng kết cấu trúc tệp; SHA-256 là mã kiểm nội dung; CATFIX là bộ công cụ sửa; PDF là định dạng tài liệu.
'''
    with report.open('x',encoding='utf8',newline='\n') as f:f.write(report_text)
    publication=write_new(F/'04 ROOT DA TIEP NHAN DUNG ACTUAL SL VA SAO LUU.json',dict(status='ACCEPTED_SL6SL25_SUPPLEMENT_CANONICAL_EXACT_CATFIX_BYTES',time=datetime.now().astimezone().isoformat(),gate=str(gate_path),gate_SHA256=sha(gate_path),current=str(current),current_SHA256=sha(current),source=str(source),source_SHA256=sha(source),candidate=str(candidate),candidate_SHA256=sha(candidate),backup=str(backup),backup_SHA256=sha(backup),ledger_backup=str(lb),ledger_backup_SHA256=sha(lb),index_backup=str(ib),index_backup_SHA256=sha(ib),report=str(report),report_SHA256=sha(report),sources25_held=True,other_currents24_held=True,control_seal_held=True,new_PDF_saves=0,literal_refs_and_frame_diagnostics_FAIL_retained=True,original149_accepted_count=135,full_SL_complete=False,full_G04_complete=False,full_goal_complete=False))
    S.progress('G04 – SL6SL25 đường/bảng bổ sung','ĐẠT PHẠM VI BỔ SUNG ĐÃ LƯU; TOÀN SL/G04 CHƯA XONG',
      'Đã tiếp nhận ddb0bc676409 đúng byte PDF CATFIX sau kiểm độc lập tệp thực: 10 đường/20 nét/40 đoạn cong/120 mốc đạt dung sai; 26 ô nguyên sửa+94 giữ, mức lớn/nhỏ nhất bảng và đầu/cuối giữ; 10 nhãn/đầu/thân/khung đạt hình thức. Ngoài 11 trang ở 200 điểm/inch, ngưỡng0/đệm0=0; 25 nguồn/24 bản khác giữ, bản cũ+sổ+danh mục sao lưu. 128 đối tượng cũ/75 luồng kiểm bảo toàn nội dung, 50 đối tượng mới đúng; 31 số định danh và7số mục lục/phần tổng kết tệp đổi đã khai báo. Kiểm số định danh nguyên vẫn CHƯA ĐẠT; điểm ảnh khung toàn trang23/44/0 tại150/200/600, chênh màu lớn nhất1/8/0 vẫn CHƯA ĐẠT150/200; không nới vùng/ngưỡng. Chỉ nhận phạm vi6SL25; SLkhác/G04 còn, giữ135/149gốc. Hồ sơG04/SL6SL25 C2 DA LUU NGHIEM THU PHAM VI BO SUNG 04-10-2026.')
    end=write_new(F/'05 ROOT SL DA GHI SO CHO REFRESH INDEX.json',dict(publication=str(publication),publication_SHA256=sha(publication),ledger_SHA256_after=sha(ledger),source_SHA256=sha(source),canonical_SHA256=sha(current),index_refresh_pending=True,full_goal_complete=False))
    print(json.dumps(dict(publication=str(publication),publication_SHA256=sha(publication),gate_SHA256=sha(gate_path),final_receipt=str(end),final_receipt_SHA256=sha(end),ledger_SHA256_after=sha(ledger),sources25_held=True,other_currents24_held=True),ensure_ascii=False),flush=True)
finally:
    C.release(claim['token'],actor,session,'SL6SL25 tiếp nhận một lần hoặc giữ lỗi có bằng chứng tại '+str(F)+'; đọc bản chính/cổng/04/05 trước tiếp tục, không chạy lại chương trình tiếp nhận.')
