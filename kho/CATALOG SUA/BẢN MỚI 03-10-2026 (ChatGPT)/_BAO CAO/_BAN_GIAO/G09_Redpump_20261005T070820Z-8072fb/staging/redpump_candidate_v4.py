from pathlib import Path
import json,sys,os,hashlib
import numpy as np
ST=Path(__file__).resolve().parent;G=ST.parent
H=json.loads((G/'01 HANDOFF G09 READONLY SOURCE CURRENT TASK.json').read_text(encoding='utf-8-sig'));A=json.loads((G/'05 ROOT REVIEW AND SEPARATE STAGING AUTHORITY.json').read_text(encoding='utf-8-sig'));N=json.loads((G/'02 P7 GRID H50 GAP SOURCE VECTOR ROI NATIVE.json').read_text(encoding='utf-8-sig'))
sys.path.insert(0,str(Path(H['runtime']['PdfDoc_file']).parent.parent));sys.dont_write_bytecode=True
from catfix.recipes import Job
from catfix import cs
from catfix.pdfdoc import PdfDoc,render
from PIL import Image
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(H['current'])==H['current_SHA256'] and sha(H['source'])==H['source_SHA256']
lock=ST/'REDPUMP-STAGING-WRITER-LOCK.json';l=json.loads(lock.read_text(encoding='utf-8'));l.pop('owner_thread',None);l['coordinator_thread']='01a10a18-ec94-72d9-9756-c388bf6cd0db';l['owner']='Sua catalogue phan ba (Redpump sole writer)';l['revision']='v4 SOURCE GRID REVEAL FITZ BALANCED';lock.write_text(json.dumps(l,ensure_ascii=False,indent=2),encoding='utf-8')
DEST=ST/'candidate-v4';DEST.mkdir(exist_ok=True);OUT=DEST/Path(H['current']).name;assert not OUT.exists()
J=Job(H['current'],str(OUT),backend='fitz',log_path=str(DEST/'catfix-edit.log.json'));P=J.E.page(6);D=J.E.doc;orig=D.page_content(6)
roi=A['selected_allowed_ROI_page_bottom_left'];glyph_min_x=407.3112
slot=[roi[0],roi[1],glyph_min_x-.37,roi[3]]
# The cutout is in the blank label margin, 0.37pt from the black glyph bbox.
# It clips the two white background fills only. Original grid/curves/glyphs stay byte exact.
outer=[398,382,418,393]
assert all(P.objs[oi]['bbox'][0]>outer[0] and P.objs[oi]['bbox'][1]>outer[1] and P.objs[oi]['bbox'][2]<outer[2] and P.objs[oi]['bbox'][3]<outer[3] for oi in [1394,1395])
assert slot[0]>=roi[0] and slot[1]>=roi[1] and slot[2]<=roi[2] and slot[3]<=roi[3]
assert np.array_equal(P.objs[1394]['ctm'],np.diag([.24,.24,1]))
def rectins(r):return cs.Instr([r[0]/.24,r[1]/.24,(r[2]-r[0])/.24,(r[3]-r[1])/.24],'re')
prefix=cs.serialize([cs.Instr([],'q'),rectins(outer),rectins(slot),cs.Instr([],'W*'),cs.Instr([],'n')],nd=10)
suffix=b'\nQ\n'
patches=[]
for oi in [1394,1395]:
 o=P.objs[oi];patches.extend([(o['i0'],prefix),(o['i1']+1,suffix)])
byindex={}
for index,data in patches:byindex[index]=byindex.get(index,b'')+data
chunks=[]
for i,ins in enumerate(P.ops):
 if i in byindex:chunks.append(byindex[i])
 chunks.append(cs.serialize([ins]))
# No original instruction is altered; concatenating per-instruction raw is exact for this file.
assert b''.join(cs.serialize([i]) for i in P.ops)==orig
native=b''.join(chunks)
parsed=cs.parse(native);assert sum(i.op=='q' for i in parsed)-sum(i.op=='Q' for i in parsed)==sum(i.op=='q' for i in P.ops)-sum(i.op=='Q' for i in P.ops)
D.set_stream(D.page_contents_refs(6)[0],native)
J.edits.append({'page':6,'rect':roi,'label':'Reveal existing source H50 through blank margin only','kind':'native-clip-white-background-only'})
plan={'method':'Two isolated even-odd clips around original duplicate white fills; reveal the exact original source grid beneath their blank margin','gap_direct_before_pt':N['grid_hidden_length_pt'],'historic_approx_gap_not_used_pt':N['prior_reported_gap_pt_diagnostic'],'allowed_ROI':roi,'white_margin_cutout':slot,'glyph_bbox_min_x':glyph_min_x,'glyph_clearance_pt':glyph_min_x-slot[2],'expected_remaining_centerline_gap_pt':N['grid_hidden_centerline_interval_page_bottom_left'][1]-slot[2],'original_grid_path_style_and_all_original_operators_untouched':True,'source_grid_physical_width_pt':N['source_grid_physical_width_pt'],'no_new_line_or_white_paint':True,'no_glyph_or_halo_outline_edit':True,'cutout_does_not_intersect_black_glyphs':True,'outer_clip_rect_contains_entire_original_white_fill':outer,'two_white_layers_not_double_gap':True,'inserted_prefix_ascii':prefix.decode('latin1'),'inserted_suffix_ascii':suffix.decode('latin1'),'patch_indices':[(i,len(d)) for i,d in patches],'patch_count':len(patches),'candidate':str(OUT),'v1_retained_as_review_draft':True,'v2_REJECTED_XMP_RAW_AND_DECODED_CHANGED':True,'v3_REJECTED_CLIP_STATE_Q_COLLISION':True,'backend':'fitz','v1_reason_not_selected':'Overlaid fragment seam and 4-decimal serializer width rounding; v2 reuses the untouched original grid instead'}
J.E.log.append(plan);J.save();J.close()
(DEST/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');(DEST/'INSERTED-PREFIX.bin').write_bytes(prefix);(DEST/'INSERTED-SUFFIX.bin').write_bytes(suffix)
R=PdfDoc(str(OUT));assert R.page_content(6)==native
for i in range(6):assert R.page_content(i)==Path(H['current_native7'][i]['path']).read_bytes()
R.close()
for label,path in [('source',H['source']),('current',H['current']),('candidate',str(OUT))]:
 for dpi in [200,600,1200]:Image.fromarray(render(path,6,dpi,clip=(392,376,426,400))).save(DEST/f'{label}-p7-region-{dpi}.png')
assert sha(H['source'])==H['source_SHA256'] and sha(H['current'])==H['current_SHA256']
print('CANDIDATE',OUT);print('SHA256',sha(OUT));print('EXPECTED GAP',plan['expected_remaining_centerline_gap_pt'])
