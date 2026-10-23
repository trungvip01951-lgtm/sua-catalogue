from pathlib import Path
import os,sys,json,hashlib,datetime,ctypes
import numpy as np
G=Path(__file__).resolve().parent.parent
ST=G/'staging'
H=json.loads((G/'01 HANDOFF G09 READONLY SOURCE CURRENT TASK.json').read_text(encoding='utf-8-sig'))
A=json.loads((G/'05 ROOT REVIEW AND SEPARATE STAGING AUTHORITY.json').read_text(encoding='utf-8-sig'))
N=json.loads((G/'02 P7 GRID H50 GAP SOURCE VECTOR ROI NATIVE.json').read_text(encoding='utf-8-sig'))
B=json.loads((G/'03 CURRENT62 PATH STYLE AND96 TABLE LOCKS BASELINE.json').read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bh(d):return hashlib.sha256(d).hexdigest()
def dump(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
PKG=Path(H['runtime']['PdfDoc_file']).parent.parent
sys.path.insert(0,str(PKG));sys.dont_write_bytecode=True
from catfix import cs
from catfix.vector import Editor
from catfix.recipes import Job
from catfix.pdfdoc import PdfDoc,render
from PIL import Image
assert '43/43 ĐẠT' in (ST/'B0-tests-shortpath.txt').read_text(encoding='utf-8')
assert sha(G/'05 ROOT REVIEW AND SEPARATE STAGING AUTHORITY.json')=='1f99e858579d24fb1ab30bc16a6649de3927240438f760b4d63bf985baa04196'
assert sha(G/'01 HANDOFF G09 READONLY SOURCE CURRENT TASK.json')==A['handoff_SHA256']
assert sha(G/'02 P7 GRID H50 GAP SOURCE VECTOR ROI NATIVE.json')==H['ROI_native_SHA256']
assert sha(G/'03 CURRENT62 PATH STYLE AND96 TABLE LOCKS BASELINE.json')==H['baseline_SHA256']
for k in ['source','current']:assert sha(H[k])==H[k+'_SHA256']
for k in ['python','PdfDoc','recipes']:
 r=H['runtime'];assert sha(r[k if k=='python' else k+'_file'])==r[k+'_SHA256']
LOCK=ST/'REDPUMP-STAGING-WRITER-LOCK.json'
with LOCK.open('x',encoding='utf-8') as f:json.dump({'owner_thread':'01a10a28-8830-7218-85b9-62e36c4530fb','role':'Sua catalogue phan ba','pid':os.getpid(),'created':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Redpump staging only','source_hash':H['source_SHA256'],'current_hash':H['current_SHA256'],'authority_hash':sha(G/'05 ROOT REVIEW AND SEPARATE STAGING AUTHORITY.json'),'status':'PREPARING'},f,indent=2)
DEST=ST/'candidate-v1';DEST.mkdir(exist_ok=True)
OUT=DEST/Path(H['current']).name
assert not OUT.exists()
job=Job(H['current'],str(OUT),backend='pikepdf',log_path=str(DEST/'catfix-edit.log.json'))
D=job.E.doc
for p in H['current_native7']:
 data=D.page_content(p['page']-1);assert bh(data)==p['SHA256'];assert data==Path(p['path']).read_bytes()
P=job.E.page(6);o=P.objs[N['grid_native_object']]
assert np.array_equal(o['ctm'],np.array(N['grid']['style']['ctm']))
assert np.allclose(P.object_pagepath(1232)[0][1][0],[335.6112,387.4824],rtol=0,atol=1e-10)
assert np.allclose(P.object_pagepath(1232)[1][1][0],[523.3128,387.4824],rtol=0,atol=1e-10)
assert o['lw']==2.91667 and P.color_of(1232,'stroke')==(0.,0.,0.)
for layer in N['four_native_label_layers']:
 oi=layer['object'];assert P.objs[oi]['i0']==layer['i0'] and P.objs[oi]['i1']==layer['i1'];assert np.allclose(P.objs[oi]['bbox'],layer['bbox_page_bottom_left'],rtol=0,atol=1e-9)
roi=A['selected_allowed_ROI_page_bottom_left'];x0=N['grid_hidden_centerline_interval_page_bottom_left'][0]
x1=N['four_native_label_layers'][2]['bbox_page_bottom_left'][0]-.72
y=N['grid_centerline_y_page_bottom_left'];w=N['source_grid_physical_width_pt']
# Preserve the original round caps/joins and exact 0.24 CTM. Restore only blank label margin.
assert x0-w/2>=roi[0] and x1+w/2<407.3112 and y-w/2>=roi[1] and y+w/2<=roi[3]
ins=[cs.Instr([], 'q'),cs.Instr([cs.Name('R15')],'gs'),cs.Instr([0,0,0],'RG'),cs.Instr([2.91667],'w'),cs.Instr([1],'J'),cs.Instr([1],'j'),cs.Instr([[],0],'d'),cs.Instr([x0/.24,y/.24],'m'),cs.Instr([x1/.24,y/.24],'l'),cs.Instr([],'S'),cs.Instr([],'Q')]
# Insert after BOTH original white fields and before BOTH black source glyph layers.
index=P.objs[1396]['i0'];before=cs.serialize(P.ops[:index]);after=cs.serialize(P.ops[index:]);inserted=cs.serialize(ins)
original=D.page_content(6);assert before+after==original
native=before+inserted+after
ref=D.page_contents_refs(6);assert len(ref)==1
plan={'gap_direct_pt':N['grid_hidden_length_pt'],'historic_approx_gap_pt':N['prior_reported_gap_pt_diagnostic'],'not_forced_to_historic_value':True,'ROI':roi,'source_segment_centerline':[[x0,y],[x1,y]],'physical_width_pt':w,'source_cap_join':[1,1],'segment_length_pt':x1-x0,'right_round_cap_end_x':x1+w/2,'remaining_centerline_gap_to_original_right_end_pt':N['grid_hidden_centerline_interval_page_bottom_left'][1]-(x1+w/2),'glyph_bbox_min_x':407.3112,'glyph_clearance_pt':407.3112-(x1+w/2),'insert_index':index,'inserted_native_ascii':inserted.decode('latin1'),'original_native_exact_subsequence':True,'method':'one source-style black grid fragment over blank white margin, under both untouched 845 layers','scope':'partial grid gap improvement; does not join through glyphs','inserted_object_index':1396,'shifted_original_glyph_object_indices':[1397,1398],'original_grid_native_object':1232,'PDF_written_by':'catfix PdfDoc.set_stream + Job.save','candidate':str(OUT)}
dump(DEST/'plan.json',plan)
(DEST/'INSERTED-P7-NATIVE.bin').write_bytes(inserted)
D.set_stream(ref[0],native)
job.edits.append({'page':6,'rect':roi,'label':'H50 grid blank margin restored; 845 unchanged','kind':'source-vector-grid'})
job.E.log.append({'operation':'native-grid-fragment','plan':plan})
job.save();job.close()
R=PdfDoc(str(OUT));assert R.page_content(6)==native
for i in range(6):assert R.page_content(i)==Path(H['current_native7'][i]['path']).read_bytes()
R.close()
assert sha(H['source'])==H['source_SHA256'] and sha(H['current'])==H['current_SHA256']
for label,path in [('source',H['source']),('current',H['current']),('candidate',str(OUT))]:
 for dpi in [200,600,1200]:
  region=(392,376,426,400)
  Image.fromarray(render(path,6,dpi,clip=region)).save(DEST/f'{label}-p7-region-{dpi}.png')
dump(DEST/'authoring-receipt.json',{'candidate':str(OUT),'candidate_SHA256':sha(OUT),'source_held':True,'current_held':True,'native_insert_SHA256':bh(inserted),'lock':str(LOCK),'no_canonical_or_control_write':True})
print(json.dumps(plan,ensure_ascii=False));print('CANDIDATE SHA256',sha(OUT))
