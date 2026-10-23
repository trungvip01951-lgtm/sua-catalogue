"""Explicit second and LAST sample preparation of the same SP77 method.
No PDF write: only inset clip boundaries and grid holes change. Frozen paths,
font source bytes, all anchors, table parts, style and acceptance limits hold.
"""
import copy,json,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
import root_SP77_static15_material_20261006 as M
from catfix.cs import parse,serialize
from g04_SL_BODY_nativegrid_frozen44_CATFIX_helper2 import clip_prefix
R=M.R
OLD=R/'ROOT8SP77 STATIC15 20261005T183933Z-ac1b75/02 FULL STATIC15 FONT15 TABLE7 NO PDF.json'
OUT=R/'ROOT8SP77 FINAL SAMPLE2 STATIC INSET GRID LABEL HOLES'
NEWBODY=[[1022,201,1522,592],[1522,245,1638,592]]
def rec(p):return {'path':str(p),'SHA256':M.sha(p)}
def put(p,b):
 with p.open('xb')as f:f.write(b)
 return rec(p)
def write(p,z):
 with p.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 return rec(p)
def main():
 assert M.sha(OLD)=='9f0cb528c849ae85a69f1745da5557da9d60608064325d311d33aabe0d309972'
 old=M.rd(OLD);M.guard(old['guards']);assert old['BODY_sourcepixels']==M.BODY
 if OUT.exists():
  assert not list(OUT.iterdir()),'STATIC_OUTPUT_EXISTS_NO_OVERWRITE'
 else:OUT.mkdir()
 z=copy.deepcopy(old);oldnative=Path(old['native']['path']).read_bytes();start,end=old['original_base_unchanged_byte_range'];base=oldnative[start:end]
 assert M.dig(base)==old['base_original_native_SHA256']
 oldclip=b''.join(M.S.rect_raw(M.pagebox(b))for b in M.BODY)+b'W\nn\n'
 newclip=b''.join(M.S.rect_raw(M.pagebox(b))for b in NEWBODY)+b'W\nn\n'
 curve=Path(old['new_curves']['path']).read_bytes();grid=Path(old['new_grid']['path']).read_bytes()
 assert curve.count(oldclip)==grid.count(oldclip)==1
 newcurve=curve.replace(oldclip,newclip,1)
 assert newcurve.split(b'RG\n',1)[1]==curve.split(b'RG\n',1)[1],'CURVE_BODY_LITERAL_CHANGED'
 # The grid ends before the word, including the gap between separate source
 # glyph rectangles. This is a path clipping operation, never a white fill.
 boxes=[]
 for l in old['labels15']:
  ps=[[F(v)for v in p]for p in l['full_RGB_hull_page_fraction']]
  pad=F(1,4);box=[min(p[0]for p in ps)-pad,min(p[1]for p in ps)-pad,max(p[0]for p in ps)+pad,max(p[1]for p in ps)+pad]
  assert all(any(F(b[0])<=M.uv(p)[0]<=F(b[2])and F(b[1])<=M.uv(p)[1]<=F(b[3])for b in NEWBODY)for p in ([box[0],box[1]],[box[2],box[3]]))
  boxes.append(box)
 for i,a in enumerate(boxes):
  for b in boxes[i+1:]:assert a[2]<=b[0]or b[2]<=a[0]or a[3]<=b[1]or b[3]<=a[1],'GRID_HOLES_OVERLAP'
 media=[F(-2),F(-2),F('833.55999999999994543032'),F(597)]
 # The earlier complement helper is deliberately specialized for two BODY
 # tiles; label holes use disjoint rectangle geometry directly instead.
 holesclip=b'q\n'+M.S.rect_raw(media)+b''.join(M.S.rect_raw(b)for b in boxes)+b'W*\nn\n'
 holesproof={'geometry':'Media rectangle plus15 disjoint full-word boxes, evenodd',
  'boxes_page_fraction':[list(map(str,b))for b in boxes],'overlap':False,'fill':False,
  'static_failed_helper_shape_assumption_before_any_PDF':True}
 newgrid=grid.replace(oldclip,newclip+holesclip+b'\n',1)
 assert newgrid.endswith(b'S\nQ\nEMC\n');newgrid=newgrid[:-len(b'S\nQ\nEMC\n')]+b'S\nQ\nQ\nEMC\n'
 actualholes=[M.pagebox(b)for b in NEWBODY]+[M.pagebox(r['target_hole_bbox'])for r in old['table7']]
 prefix,proof=clip_prefix(media,actualholes)
 font=Path(old['font_native']['path']).read_bytes();table=Path(old['table_native']['path']).read_bytes()
 native=prefix+b'\n'+base+b'\nQ\n'+newgrid+b'\n'+newcurve+b'\n'+font+b'\n'+table
 assert serialize(parse(native))==native
 qq=mark=0
 for op in parse(native):
  assert op.op in M.S.ARITY and len(op.operands)==M.S.ARITY[op.op]
  qq+=1 if op.op=='q'else -1 if op.op=='Q'else 0
  mark+=1 if op.op in('BMC','BDC')else -1 if op.op=='EMC'else 0
  assert qq>=0 and mark>=0
 assert qq==mark==0
 assert not any(op.op in('f','f*','F','B','B*','b','b*')for op in parse(newgrid+newcurve+font+table))
 z.update(BODY_sourcepixels=NEWBODY,actual_complement_holes_page=[list(map(str,p))for p in actualholes],
  sample1_plan=rec(OLD),sample1_actual_failure=rec(R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE1/99 FAILURE NO RETRY.json'),
  keeper_delta_diagnosis=rec(R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE1/LOCALIZED KEEPER READONLY/01 EXACT KEEPER DELTA LOCALIZATION NO PDF.json'),
  second_last_same_method=True,actual_same_method_attempts=1,next_actual_ordinal=2,maximum_actual_same_method_attempts=2,
  new_grid=put(OUT/'GRID SAME16 FRAME INSET FULL LABEL HOLES15.bin',newgrid),
  new_curves=put(OUT/'CURVES SAME70 ONLY INSET CLIP.bin',newcurve),native=put(OUT/'NATIVE P9 EXISTING160 SAMPLE2.bin',native),
  complement_clip=proof,grid_label_holes=[{'suffix':l['suffix'],'page_bbox':list(map(str,b)),'margin_pt':'1/4'}for l,b in zip(old['labels15'],boxes)],
  grid_label_clip_proof=holesproof,original_base_unchanged_byte_range=[len(prefix)+1,len(prefix)+1+len(base)],
  actual_change='Second and last of same way: inset clear/paint clip, grid only clipped around full word; curves/font/table/anchors/styles unchanged.',
  original_allowed_ROIs_held=True,operation_note='Static only; no PDF/Job/Save. Not a renamed new method or a reset of sample count.')
 z['guards'].update({str(OLD):M.sha(OLD),str(__file__):M.sha(__file__)})
 for k in('source_physical_held15','aliases11','labels15','gaps225','labelpairs105','table7','keepers','allowed_page_ROIs','styles'):
  assert z[k]==old[k],('FROZEN_CHANGED',k)
 M.guard(z['guards']);p=write(OUT/'01 EXPLICIT LAST2 STATIC NO PDF.json',z)
 # Copy the prior proven writer into a clearly counted sample2, with finite
 # output guards; graph/resource/numeric/pixel gates do not change.
 writer=Path(__file__).with_name('root_SP77_final2_one_candidate_20261006.py')
 oldwriter=Path(__file__).with_name('root_SP77_one_candidate_20261006.py');s=oldwriter.read_text(encoding='utf8')
 s=s.replace('CANDIDATE1','CANDIDATE2').replace('candidate1','candidate2')
 s=s.replace("'actual_consumed':1","'actual_consumed':2").replace("'actual_same_method_attempts':1","'actual_same_method_attempts':2")
 needle="assert g['allow_one_candidate']is True and g['canonical']is False and g['maximum_Save_calls']==1"
 assert s.count(needle)==1
 s=s.replace(needle,needle+"\n assert g['actual_ordinal']==2 and g['maximum_same_method_samples']==2 and p['second_last_same_method']is True")
 with writer.open('x',encoding='utf8')as f:f.write(s)
 print(json.dumps({'plan':p,'writer':rec(writer),'PDF_Save':0,'original_count':'137/149 unchanged'},ensure_ascii=False))
if __name__=='__main__':main()
