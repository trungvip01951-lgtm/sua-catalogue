"""A finite ROOT source77 plan; reads PDFs only, no Job/save/image editing.
Frozen accepted physical controls are mapped once; no refit or font synthesis.
"""
import argparse,hashlib,json,math,sys,uuid
import numpy as np
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
from datetime import datetime,timezone
sys.path.insert(0,r'D:\ChatGPT\Sửa catalogue\vendor\catfix_original\GOI_SUA_CATALOGUE_CHATGPT')
from catfix.pdfdoc import PdfDoc
from catfix.cs import Ref,parse,serialize
import qa_sol_4SP8_SOURCE110_RGB16_STAGGER_STATIC_NATIVE_207 as S
import qa_sol_SP8_geometry206A_pure as G
from g04_SL_BODY_nativegrid_frozen44_CATFIX_helper2 import clip_prefix
R=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05')
PURE=R/'ROOT8SP77 SOURCE135 MIN7 PURE15 NO PDF 20261005T141700Z-234c80/02 PURE15 CURRENT135 MINIMAL7 C2 NO PDF.json'
PURESHA='8d2cbf77458eec40e8a54851b8f514480661a3326da26c88ebba185e993bb0a2'
INDEP=R/'INDEPENDENT8SP77 PURE15 FRACTION135 READONLY/01 OWN FRACTION PURE15 CURRENT135 ENDS30 C2 NO PDF.json'
MAP=R/'ROOT8SP77 AXES19 SAME CORES SELECTED 20261005T142120Z-2742e6/01 ROOT SELECTED19 SAME CORE ZERO PADDING NO PDF.json'
AXES=R/'8SP77 P9 AXES FRAME220 READONLY PROPOSAL/01 SOURCE P9 SP77 AXES FRAME PROPOSAL NO MAP.json'
SOURCE=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 01-10-2026\Giếng\Perotac bơm giếng SP_compressed (bản mới).pdf')
CURRENT=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\Giếng\Perotac bơm giếng SP_compressed (bản mới).pdf')
BODY=[[1021,198,1523,592],[1523,244,1643,592]]
KEEPERS={'TITLE':[1523,194,1645,244],'H_TEXT':[974,190,1021,594],
 'FEET_TEXT':[1643,190,1680,594],'UPPER_Q_TEXT':[1015,156,1664,198],
 'ETA_LOWER_Q_TEXT':[974,600,1680,742],'LEFT_ALL':[0,0,940,1240]}
PX,PY,TY=F(1039449,2165000),F(743751,1550000),F(1143,125000000)
SX,SY=PX*1732,PY*1240
U0,DU,V0,DV=F(2047,2),F(183,32),F(2355,4),-F(389,450)
X0,Y0,AX,HY=PX*U0,TY+SY-PY*V0,PX*DU,-PY*DV
WIDTH=S.WIDTH;HALF=WIDTH/2;GAP=F(7,20)
FONTBANK=R/'SP25 FONT13 TWO RECTANGLE IDENTITY CORRECTION STATIC NO SAMPLE 20261004T160409Z-294421/01 SOURCE13 TWO IDENTITY RECTANGLES FINAL PROPOSALS NO RAM.json'
sha=S.sha;dig=S.dig;rd=S.read;num=S.num;nums=S.nums;snap=S.snap
def pagebox(b):
 u,v,r,t=map(F,b);return [PX*u,TY+SY-PY*t,PX*r,TY+SY-PY*v]
def page(p):return [X0+AX*p[0],Y0+HY*p[1]]
def uv(p):return [p[0]/PX,(TY+SY-p[1])/PY]
def record(p):return {'path':str(p),'SHA256':sha(p)}
def write(p,z):
 with p.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 return record(p)
def put(p,b):
 with p.open('xb')as f:f.write(b)
 return record(p)
def guard(g):
 for p,h in g.items():assert sha(p)==h,('INPUT_CHANGED',p)
def transform(p,cs,sn,tr):return [snap(cs*p[0]-sn*p[1]+tr[0]),snap(sn*p[0]+cs*p[1]+tr[1])]
def imagepart(box,cs=F(1),sn=F(0),tr=(F(0),F(0))):
 # Original source image is kept at natural pitch. Virtual top left=(0,0).
 u,v,r,b=map(F,box);corners=[[u*PX,-b*PY],[r*PX,-b*PY],[r*PX,-v*PY],[u*PX,-v*PY]]
 poly=[transform(p,cs,sn,tr)for p in corners]
 cm=list(map(snap,[cs*SX,sn*SX,-sn*SY,cs*SY,tr[0]+sn*SY,tr[1]-cs*SY]))
 raw=b'q\n'+S.polygon_raw(poly)+b'W\nn\n'+(nums(cm)+' cm\n/X11 Do\nQ\n').encode('ascii')
 return raw,poly,cm
def make(materialpath):
 assert sha(PURE)==PURESHA and sha(INDEP)=='440a77e30fd4cf147968bb3a6dfffefc8830085b106f9261beaad49a733fc844'
 assert sha(AXES)=='390ea6b4969ded34e00a44db9dcdbc04c2768caae585b13c434b230eca901e14'
 guards={str(p):sha(p)for p in(PURE,INDEP,MAP,AXES,Path(__file__),Path(S.__file__),Path(G.__file__))}
 guards[str(SOURCE)]='e1b94dc6f23c35d18d61cee71d9d88c844b1070d14ff662bbabe2256cdd690c9'
 guards[str(CURRENT)]='659f506de9a066ebc9582eeea69923157d7bd9029fedfc4a898bdbefe0baf892'
 guard(guards);pure=rd(PURE);mapping=rd(MAP);axes=rd(AXES)
 assert list(map(F,mapping['selected_pixel_affine'].values()))==[U0,DU,V0,DV]
 d=PdfDoc(str(CURRENT),backend='pikepdf')
 try:
  assert d.page_contents_refs(8)==[Ref((160,0))] and d.resource(d.page_resources(8),'XObject','X11')==Ref((166,0))
  base=d.page_content(8);assert dig(base)=='650e19fd3631ba5646a33d01c6bcbd13f99d92bc995603c4cd19541638909e2d'
  assert dig(d.stream_raw(Ref((166,0))))=='c3c8e360d59ab43eee382610bb3815dd5a656671761e81161e91063a1b94b444'
  media=d.get(d.page_ref(8))['MediaBox'];natives=[dig(d.page_content(i))for i in range(12)]
 finally:d.close()
 curves=[];physical={};painted={};rows=[]
 for row in pure['records15']:
  suffix=row['model'].split('-')[-1];original=[[[F(v)for v in p]for p in seg]for seg in row['segments_QH_decimal20']]
  physical[suffix]=original;groups=[[],[]];splitproof=[]
  for seg in original:
   if seg[-1][0]<=24:groups[0].append(seg)
   elif seg[0][0]>=24:groups[1].append(seg)
   else:
    t=S.q_crossing(seg,F(24));a,b=G.split(seg,t);groups[0].append(a);groups[1].append(b)
    splitproof.append({'t':str(t),'Q':str(a[-1][0]),'error_Q':str(abs(a[-1][0]-24))})
  raw=('/CfxSP77Model'+suffix+' BMC\n').encode('ascii');projected=[];delta=[]
  for i,group in enumerate(groups):
   assert group;pg=[[[snap(v)for v in page(p)]for p in seg]for seg in group];projected+=pg
   raw+=(b'[6.58 2.81] 0 d\n'if i==0 else b'[] 0 d\n')+(nums(pg[0][0])+' m\n').encode('ascii')
   raw+=b''.join((nums([v for p in seg[1:]for v in p])+' c\n').encode('ascii')for seg in pg)+b'S\n'
   for old,new in zip(group,pg):
    for p,pp in zip(old,new):delta.append(max(abs((pp[0]-X0)/AX-p[0]),abs((pp[1]-Y0)/HY-p[1])))
  raw+=b'EMC\n';assert max(delta)<F(1,10**18)
  painted[suffix]=projected;curves.append(raw)
  rows.append({'model':row['model'],'suffix':suffix,'source_physical_segments_decimal20':row['segments_QH_decimal20'],
   'painted_page_controls_fraction':[[list(map(str,p))for p in s]for s in projected],
   'inverse_roundoff_max':str(max(delta)),'Q24_exact_subdivision':splitproof,'changes':row['changes']})
 assert len(rows)==15 and sum(map(len,physical.values()))==56
 bodypages=[pagebox(b)for b in BODY]
 grid=b'/CfxSP77SourceGrid BMC\nq\n'+b''.join(S.rect_raw(b)for b in bodypages)+b'W\nn\n'
 grid+=b'0.8941176470588235 0.8941176470588235 0.8941176470588235 RG\n0.35 w\n0 J\n1 j\n[] 0 d\n'
 gridrecords=[]
 for key,orientation in [('Q9_observed_table_anchor_ticks','vertical'),('H10_grid_ticks','horizontal')]:
  for tick in axes[key]:
   value=F(tick['Q_m3h']if orientation=='vertical'else tick['H_m'])
   if value==0 or orientation=='horizontal'and value==450:continue
   c=F(tick['source_cell_centre_plus_half_once'])
   pts=[[PX*c,TY+SY-PY*F(588.5)],[PX*c,TY+SY-PY*F(199.5)]]if orientation=='vertical'else[[PX*F(1023.5),TY+SY-PY*c],[PX*F(1641.5),TY+SY-PY*c]]
   grid+=(nums(pts[0])+' m\n'+nums(pts[1])+' l\nS\n').encode('ascii')
   gridrecords.append({'direction':orientation,'source_value':str(value),'measured_source_center':str(c),'page_points':[list(map(str,p))for p in pts]})
 grid+=b'0.2509803921568627 0.2509803921568627 0.2509803921568627 RG\n0.48 w\n'
 fbox=pagebox([F(1023.5),F(199.5),F(1641.5),F(588.5)])
 grid+=S.rect_raw(fbox)+b'S\nQ\nEMC\n'
 curve=b'/CfxSP77Frozen15 BMC\nq\n'+b''.join(S.rect_raw(b)for b in bodypages)+b'W\nn\n'
 curve+=(nums([F(x,255)for x in(98,108,110)])+' RG\n'+num(WIDTH)+' w\n0 J\n1 j\n').encode('ascii')+b''.join(curves)+b'Q\nEMC\n'
 out=R/('ROOT8SP77 STATIC15 '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir()
 z={'status':'STATIC_CURVES15_NO_MATERIAL_NO_PDF','guards':guards,'source':str(SOURCE),'current':str(CURRENT),
  'pure':record(PURE),'math_independent':record(INDEP),'axes':record(AXES),'map':record(MAP),
  'BODY_sourcepixels':BODY,'KEEPERS_sourcepixels':KEEPERS,'source_physical_held15':rows,
  'base_original_native_SHA256':dig(base),'baseline_native12':natives,
  'new_grid':put(out/'GRID SOURCE19 FRAME4.bin',grid),'grid_source_records16':gridrecords,
  'new_curves':put(out/'CURVES15 FROZEN56 Q24 DASH.bin',curve),
  'styles':{'curve_RGB':[98,108,110],'width':str(WIDTH),'cap':0,'join':1,'dash':[6.58,2.81],'solid_from_Q':24,
   'frame_RGB':[64,64,64],'frame_width_pt':.48,'grid_RGB':[228,228,228],'grid_width_pt':.35},
  'actual_same_method_attempts':0,'maximum_actual_same_method_attempts':2,'operations':{'PDF_readonly':1,'Job':0,'Save':0,'marker':0,'canonical':0,'control':0}}
 if materialpath is None:print(json.dumps(write(out/'01 STATIC CURVE CORE15 NO PDF.json',z),ensure_ascii=False));return
 # This source packet has table7 ready; four chart suffixes are UNKNOWN.
 # Only the original same-file accepted font bank is used for ALL15 labels.
 assert sha(FONTBANK)=='db644495cc90e76916f9ce9a7728ab44e8aaba1f4fe06419206aa47b13520d28'
 assert sha(materialpath)=='01e4cb308480aea05fc8c62da8b3a00966df8350695afae941b154229967b77f'
 material=rd(materialpath);bank=rd(FONTBANK);fonts={v['token']:v for v in bank['font13']}
 guards.update({str(materialpath):sha(materialpath),str(FONTBANK):sha(FONTBANK)})
 table=json.loads(json.dumps(material['table7']));assert len(table)==7
 for rec in table:
  old=rec['target_hole_bbox'];new=rec['parts_union_bbox'];rec['original_draft_hole_bbox']=old.copy()
  # ROOT declares the actual edit footprint before any PDF sample: it must
  # contain BOTH the old number and new natural-pitch source word. This is
  # not a post-render widening of an accepted gate or a font-size change.
  rec['target_hole_bbox']=[min(old[0],new[0]),min(old[1],new[1]),max(old[2],new[2]),max(old[3],new[3])]
  cell=rec['cell_context_bbox'];h=rec['target_hole_bbox']
  assert cell[0]<h[0]<h[2]<cell[2]and cell[1]<h[1]<h[3]<=cell[3]
 tokens=['-']+list('0123456789');refs={};aliases=[];sourcewords={}
 doc=PdfDoc(str(CURRENT),backend='pikepdf')
 try:
  for token in tokens:
   f=fonts[token];guards[f['RGB']]=f['RGB_SHA256'];assert sha(f['RGB'])==f['RGB_SHA256']
   rgb=Path(f['RGB']).read_bytes();matches=[];owners=[]
   for obj in doc.pdf.objects:
    if not hasattr(obj,'objgen')or not isinstance(obj, __import__('pikepdf').Stream):continue
    ref=Ref(obj.objgen);di=doc.get(ref)
    if di.get('Subtype')!='Image' or [di.get('Width'),di.get('Height')]!=f['native_size']:continue
    decoded,left,_=doc.stream_decoded(ref)
    if not left and decoded==rgb:
     al=[(pi+1,k)for pi in range(12)for k,r in doc.page_resources(pi).get('XObject',{}).items()if r==ref]
     matches.append({'Ref':list(ref),'RAW_SHA256':dig(doc.stream_raw(ref)),'decoded_RGB_SHA256':dig(decoded),'aliases':al})
     if any(str(k).startswith('CfxSP25Literal')and pi in(7,11)for pi,k in al):owners.append(ref)
   assert len(owners)==1,('NO_UNIQUE_ACCEPTED_SP25_SOURCE_REF',token,matches)
   ref=owners[0];alias='CfxSP77Token'+str(len(aliases)+1);refs[token]=ref
   aliases.append({'token':token,'alias':alias,'existing_Ref':list(ref),'source_RGB_SHA256':f['RGB_SHA256'],
    'native_size':f['native_size'],'source_original_bbox':f['source_bbox_halfopen'],'source_original_page':f['source_page'],
    'proposed_relative_font_y':f['proposed_relative_font_y'],'global_exact_matches':matches,'RAW_SHA256':dig(doc.stream_raw(ref))})
   assert list(map(F,f['source_pitch_fraction']))==[PX,PY]
 finally:doc.close()
 amap={v['token']:v for v in aliases}
 labels=[];polys={};glyph=b'/CfxSP77OriginalBank15 BMC\n'
 for row in rows:
  s=row['suffix'];toks=['-']+list(s);width=sum(fonts[t]['native_size'][0]for t in toks)
  height=max(fonts[t]['proposed_relative_font_y']+fonts[t]['native_size'][1]for t in toks)
  # One fixed source-pose plan, no resizing/rotation or adaptive retry.
  q=F(12)if int(s)<=10 else F(24);gap=F(3,5)if int(s)<=10 else F(6,5)
  seg=next(seg for seg in physical[s]if seg[0][0]<=q<=seg[-1][0]);tt=S.q_crossing(seg,q)
  point=G.point(seg,tt);anchor=list(map(snap,page(point)))
  left=anchor[0]-PX*width/2;bottom=anchor[1]+HALF+gap;top=bottom+PY*height
  raw=('/CfxSP77Suffix'+s+' BMC\n').encode('ascii');parts=[];corners=[];u=0
  for token in toks:
   f=fonts[token];w,h=f['native_size'];y=f['proposed_relative_font_y']
   x=left+PX*u;yy=top-PY*(y+h);box=[snap(x),snap(yy),snap(x+PX*w),snap(yy+PY*h)]
   cm=[snap(PX*w),F(0),F(0),snap(PY*h),box[0],box[1]]
   raw+=(b'q\n'+(nums(cm)+' cm\n/'+amap[token]['alias']+' Do\nQ\n').encode('ascii'))
   polygon=[[box[0],box[1]],[box[2],box[1]],[box[2],box[3]],[box[0],box[3]]]
   corners+=polygon;parts.append({'token':token,'alias':amap[token]['alias'],'existing_Ref':list(refs[token]),
    'source_RGB_SHA256':f['RGB_SHA256'],'native_size':f['native_size'],'page_cm_fraction':list(map(str,cm)),
    'page_RGB_rectangle_fraction':list(map(str,box)),'natural_pitch_no_scale_rotation':True})
   u+=w
  raw+=b'EMC\n';glyph+=raw;poly=G.hull(corners);polys[s]=poly
  assert all(any(F(b[0])<=uv(p)[0]<=F(b[2])and F(b[1])<=uv(p)[1]<=F(b[3])for b in BODY)for p in poly)
  labels.append({'suffix':s,'literal':'-'+s,'full_model':row['model'],'anchor_Q':str(q),'anchor_actual_QH':list(map(str,point)),
   'gap_parameter_pt':str(gap),'pose':'HORIZONTAL_ORIGINAL','parts':parts,'full_RGB_hull_page_fraction':[list(map(str,p))for p in poly],
   'source_bank_all15_uniform':True,'exact_fontname_phase':'UNKNOWN source original rectangles retained'})
 glyph+=b'EMC\n'
 obstacles=[];gaps=[];intervals={}
 print('STATIC SP77 one fixed horizontal15 plan; full225 hull/curve bounds',flush=True)
 for label in labels:
  s=label['suffix'];poly=polys[s]
  for owner,segs in painted.items():
   proof=G.minimum_curve_polygon_bounds(segs,poly);intervals[(s,owner)]=proof
   passed=proof['converged']and proof['lower2']>HALF*HALF
   gaps.append({'label':s,'curve_owner':owner,'lower_distance2_exact':str(proof['lower2']),
    'upper_distance2_exact':str(proof['upper2']),'converged':proof['converged'],'subdivisions':proof['subdivisions'],
    'gap_pt_lower_diagnostic':math.sqrt(float(proof['lower2']))-float(HALF),'PASS_positive_gap':passed})
   if not passed:obstacles.append({'label':s,'curve':owner,'kind':'GAP_UNPROVEN_OR_NONPOSITIVE'})
  own=intervals[(s,s)]['upper2'];other=min(intervals[(s,o)]['lower2']for o in painted if o!=s)
  label.update(unique_nearest_owner=own<other,own_distance2_upper_exact=str(own),other_distance2_min_lower_exact=str(other))
  if not own<other:obstacles.append({'label':s,'kind':'OWN_NOT_NEAREST'})
  print('LABEL',s,'own nearest',own<other,'gapmin',min(v['gap_pt_lower_diagnostic']for v in gaps if v['label']==s),flush=True)
 pair=[]
 for i,a in enumerate(labels):
  for b in labels[i+1:]:
   ds=G.polygon_distance2(polys[a['suffix']],polys[b['suffix']]);passed=ds>0
   pair.append({'a':a['suffix'],'b':b['suffix'],'distance2_exact':str(ds),'PASS_positive':passed})
   if not passed:obstacles.append({'label_pair':[a['suffix'],b['suffix']],'kind':'PAIR_COLLISION'})
 assert len(gaps)==225 and len(pair)==105
 # Source table number rectangles are used at native pitch with integer UV
 # translations. None of the old task49 patch (175) is clipped or repainted.
 number=b'/CfxSP77Table7OriginalParts BMC\n';tablerecords=[]
 for rec in table:
  hole=list(map(F,rec['target_hole_bbox']))
  parts=[];block=('/CfxSP77Table'+rec['model'].split('-')[-1]+'Q'+str(rec['Q_m3h'])+' BMC\n').encode('ascii')
  for part in rec['parts']:
   assert part['source_alias']=='X11'and part['donorRef']==[166,0]
   box=part['source_bbox'];target=list(map(F,part['target_uv_top_left_fraction']));u,v,r,b=map(F,box)
   du,dv=target[0]-u,target[1]-v;tr=[du*PX,TY+SY-dv*PY]
   raw,poly,cm=imagepart(box,tr=tr);block+=raw
   bb=[target[0],target[1],target[0]+r-u,target[1]+b-v]
   assert hole[0]<=bb[0]<bb[2]<=hole[2]and hole[1]<=bb[1]<bb[3]<=hole[3]
   parts.append({'source_bbox':box,'source_RGB_SHA256':part['source_RGB_SHA256'],'target_uv_top_left_fraction':list(map(str,target)),
    'actual_page_cm_fraction':list(map(str,cm)),'actual_clip_polygon_page_fraction':[list(map(str,p))for p in poly]})
  block+=b'EMC\n';number+=block;tablerecords.append({k:rec[k]for k in('model','Q_m3h','before','after','target_hole_bbox')})
  tablerecords[-1]['parts']=parts;tablerecords[-1]['original_draft_hole_bbox']=rec['original_draft_hole_bbox']
 number+=b'EMC\n'
 holes=bodypages+[pagebox(r['target_hole_bbox'])for r in table]
 prefix,clipproof=clip_prefix([F(media[0])-2,F(media[1])-2,F(media[2])+2,F(media[3])+2],holes)
 native=prefix+b'\n'+base+b'\nQ\n'+grid+b'\n'+curve+b'\n'+glyph+b'\n'+number
 assert serialize(parse(native))==native and b'cmq'not in native
 qq=mark=0
 for op in parse(native):
  assert op.op in S.ARITY and len(op.operands)==S.ARITY[op.op],('BAD_OPERATOR',op.op,len(op.operands))
  qq+=1 if op.op=='q'else -1 if op.op=='Q'else 0;mark+=1 if op.op in('BMC','BDC')else -1 if op.op=='EMC'else 0
  assert qq>=0 and mark>=0
 assert qq==mark==0
 assert sum(op.op=='Do'for op in parse(glyph))==37
 assert sum(op.op=='c'for op in parse(curve))==70 and sum(op.op=='S'for op in parse(curve))==30
 assert not any(op.op in('f','f*','F','B','B*','b','b*')for op in parse(grid+curve+glyph+number))
 captures=[{'tag':'FULLPAGE','dpi':200,'page_bbox':None},
  {'tag':'CHART','dpi':200,'page_bbox':list(map(str,pagebox([960,150,1680,745])))},
  {'tag':'CHART600','dpi':600,'page_bbox':list(map(str,pagebox([974,190,1680,595])))},
  {'tag':'TABLE','dpi':400,'page_bbox':list(map(str,pagebox([950,820,1697,1186])))},
  {'tag':'FRAME_TITLE','dpi':600,'page_bbox':list(map(str,pagebox([1515,190,1650,260])))}]
 for l in labels:
  allx=[p[0]for p in polys[l['suffix']]];ally=[p[1]for p in polys[l['suffix']]]
  captures.append({'tag':'LABEL'+l['suffix'],'dpi':900,'page_bbox':list(map(str,[min(allx)-2,min(ally)-2,max(allx)+2,max(ally)+2]))})
 for r in table:
  u,v,rr,b=r['cell_context_bbox'];captures.append({'tag':'CELL'+r['model'].split('-')[-1]+'Q'+str(r['Q_m3h']),
   'dpi':600,'page_bbox':list(map(str,pagebox([u-2,v-2,rr+2,b+2])))})
 z.update(status='ROOT_SELECTED_STATIC15_LABEL15_TABLE7_NO_PDF'if not obstacles else'STATIC_ONE_LAYOUT_OBSTACLES_NO_PDF',
  material_source_packet=record(materialpath),fontbank=record(FONTBANK),aliases11=aliases,labels15=labels,gaps225=gaps,labelpairs105=pair,
  table7=tablerecords,obstacles=obstacles,native=put(out/'NATIVE P9 EXISTING160 STATIC.bin',native),
  font_native=put(out/'FONT15 ORIGINAL37 EXISTING11.bin',glyph),table_native=put(out/'TABLE7 ORIGINAL11 PARTS.bin',number),
  complement_clip=clipproof,original_base_unchanged_byte_range=[len(prefix)+1,len(prefix)+1+len(base)],
  allowed_page_ROIs=[list(map(str,r))for r in holes],captures=captures,
  keepers=[{'tag':k,'page_bbox':list(map(str,pagebox(b)))}for k,b in KEEPERS.items()],
  resource_changes='11 new aliases reference existing original font image nodes; no new stream/image/font/content object',
  font_style_ROOT_selection='PENDING_DIRECT_COMMON_GLYPH_COMPARISON; native preparation is not an actual authoring gate',
  operation_note='Exactly one static layout, no PDF rendering/sample/editor/Job/save/marker; no repeat hidden as a new method')
 guard(guards);print(json.dumps(write(out/'02 FULL STATIC15 FONT15 TABLE7 NO PDF.json',z),ensure_ascii=False))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--material',type=Path);make(ap.parse_args().material)
