from pathlib import Path
import json,sys,hashlib,collections,math,os
import numpy as np
from PIL import Image
ST=Path(__file__).resolve().parent;G=ST.parent;OUT=ST/'candidate-v4';QA=OUT/'QA';QA.mkdir(exist_ok=True)
H=json.loads((G/'01 HANDOFF G09 READONLY SOURCE CURRENT TASK.json').read_text(encoding='utf-8-sig'));A=json.loads((G/'05 ROOT REVIEW AND SEPARATE STAGING AUTHORITY.json').read_text(encoding='utf-8-sig'));B=json.loads((G/'03 CURRENT62 PATH STYLE AND96 TABLE LOCKS BASELINE.json').read_text(encoding='utf-8-sig'));PLAN=json.loads((OUT/'plan.json').read_text(encoding='utf-8'));C=OUT/Path(H['current']).name
sys.path.insert(0,str(Path(H['runtime']['PdfDoc_file']).parent.parent));sys.dont_write_bytecode=True
from catfix.vector import Editor
from catfix.pdfdoc import PdfDoc,render,fitz
from catfix import verify,cs
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
bh=lambda d:hashlib.sha256(d).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
assert sha(H['current'])==H['current_SHA256'];assert sha(H['source'])==H['source_SHA256']
D=PdfDoc(H['current']);R=PdfDoc(str(C));P=Editor(H['current']);E=Editor(str(C))
# Strict native retention proof: reconstruct saved P7 exclusively from its original raw operators plus isolated clipping commands.
oldp=P.page(6);pre=(OUT/'INSERTED-PREFIX.bin').read_bytes();post=(OUT/'INSERTED-SUFFIX.bin').read_bytes();mp={}
for oi in [1394,1395]:
 for index,data in [(oldp.objs[oi]['i0'],pre),(oldp.objs[oi]['i1']+1,post)]:mp[index]=mp.get(index,b'')+data
rebuilt=b''.join(mp.get(i,b'')+cs.serialize([ins]) for i,ins in enumerate(oldp.ops));assert rebuilt==R.page_content(6)
NATIVE=[]
for i in range(7):NATIVE.append({'page':i+1,'current':bh(D.page_content(i)),'candidate':bh(R.page_content(i)),'same':D.page_content(i)==R.page_content(i)})
assert all(n['same'] for n in NATIVE[:6])
def vector_sig(V,oi):
 o=V.objs[oi]
 if o['op']=='n':return {'nonpaint_clip_object':True,'bbox':[float(x) for x in o['bbox']]}
 return {'path':[[op,[[float(x),float(y)] for x,y in pts]] for op,pts in V.object_pagepath(oi)],'style':{k:o[k].tolist() if isinstance(o[k],np.ndarray) else o[k] for k in ['op','fill','stroke','lw','dash','gs','fill_cs','stroke_cs','ctm']}}
CURVES=[]
for c in B['curves62']:
 p=P.page(c['page']-1);e=E.page(c['page']-1);v1=[vector_sig(p,i) for i in c['objects']];mapped=[];v2=[]
 for oi,sg in zip(c['objects'],v1):
  candidates=[oi] if vector_sig(e,oi)==sg else [i for i in range(len(e.objs)) if vector_sig(e,i)==sg]
  assert len(candidates)==1, (c['model'],oi,candidates)
  mapped.append(candidates[0]);v2.append(vector_sig(e,candidates[0]))
 assert v1==v2
 h=bh(json.dumps(v1,sort_keys=True,default=str).encode());CURVES.append(dict(c,readback_exact=True,current_candidate_equal=True,candidate_object_indices=mapped,independent_path_style_hash=h))
assert len(CURVES)==62
# 96 anchor locks belong to 32 LH rows; preserve the full dictionaries rather than pretending five fields are five locks.
TABLE={'anchor_count':96,'curve_row_count':32,'complete_original_lock_dictionaries':B['LH_table96_locks'],'page6_native_byte_identical':NATIVE[5]['same'],'verification':'All original P6 instructions and rendering unchanged; no numeric re-extraction or refit','all96_preserved':True}
assert len(TABLE['complete_original_lock_dictionaries'])==32
# Original label glyphs and both backgrounds retain their own source paths, style and raw paint operations.
ep=E.page(6)
GLYPHS=[]
for oi in [1394,1395,1396,1397]:
 sig=vector_sig(oldp,oi);matches=[i for i,o in enumerate(ep.objs) if vector_sig(ep,i)==sig];assert matches
 GLYPHS.append({'original_object':oi,'candidate_objects':matches,'path_style_exact':True})
# Raw streams: compare actual payloads independent of object renumbering during a legal PDF save.
import pikepdf
pd=pikepdf.open(H['current']);pc=pikepdf.open(str(C));braw=[];craw=[]
for target,arr,skip in [(pd,braw,set(o.objgen for o in pd.pages[6].Contents if False))] if False else []:pass
old_content_ref=pd.pages[6].Contents.objgen;new_content_ref=pc.pages[6].Contents.objgen
for pdf,arr,skip in [(pd,braw,old_content_ref),(pc,craw,new_content_ref)]:
 for ob in pdf.objects:
  if isinstance(ob,pikepdf.Stream) and ob.objgen!=skip:arr.append(bh(bytes(ob.read_raw_bytes())))
STREAMS={'non_p7_raw_streams_current':len(braw),'non_p7_raw_streams_candidate':len(craw),'raw_stream_multisets_same':collections.Counter(braw)==collections.Counter(craw)}
assert STREAMS['raw_stream_multisets_same']
def semantic(x,seen=None):
 if isinstance(x,pikepdf.Stream):return {'dictionary':{str(k):semantic(v) for k,v in x.items() if str(k) not in ['/Length','/Filter','/DecodeParms']},'raw_sha256':bh(x.read_raw_bytes())}
 if isinstance(x,pikepdf.Dictionary):return {str(k):semantic(v) for k,v in x.items()}
 if isinstance(x,pikepdf.Array):return [semantic(v) for v in x]
 return str(x)
RES=[]
for i in range(7):
 r1=semantic(pd.pages[i].Resources);r2=semantic(pc.pages[i].Resources);assert r1==r2;RES.append({'page':i+1,'resources_semantic_and_streams_exact':True,'hash':bh(json.dumps(r1,sort_keys=True).encode())})
META={'Info_same':semantic(pd.docinfo)==semantic(pc.docinfo),'XMP_raw_same':pd.Root.Metadata.read_raw_bytes()==pc.Root.Metadata.read_raw_bytes(),'XMP_decoded_same':pd.Root.Metadata.read_bytes()==pc.Root.Metadata.read_bytes(),'outline_same':semantic(pd.Root.get('/Outlines'))==semantic(pc.Root.get('/Outlines')),'annots_per_page_same':all(semantic(pd.pages[i].get('/Annots'))==semantic(pc.pages[i].get('/Annots')) for i in range(7))}
assert all(META.values());pd.close();pc.close()
roi=A['selected_allowed_ROI_page_bottom_left'];allowed={7:[roi]};render_checks=[]
# Render all 7 pages at both requested scales, comparing strict-zero outside the UNEXPANDED ROI.
for dpi in [200,600]:
 for i in range(7):
  current=render(H['current'],i,dpi);cand=render(str(C),i,dpi)
  Image.fromarray(cand).save(QA/f'candidate-p{i+1:02d}-{dpi}.png')
  Image.fromarray(current).save(QA/f'current-p{i+1:02d}-{dpi}.png')
  hh,ww=current.shape[:2];diff=np.zeros((hh,ww),dtype=bool)
  for y in range(0,hh,256):diff[y:y+256]=np.any(current[y:y+256]!=cand[y:y+256],axis=2)
  ok=np.zeros_like(diff)
  if i==6:
   s=dpi/72.;mb=D.mediabox(i);xa=max(0,math.floor((roi[0]-mb[0])*s));xb=min(ww,math.ceil((roi[2]-mb[0])*s));ya=max(0,math.floor((mb[3]-roi[3])*s));yb=min(hh,math.ceil((mb[3]-roi[1])*s));ok[ya:yb,xa:xb]=True
  bad=int((diff & ~ok).sum());assert bad==0
  yy,xx=np.where(diff);box=None if not len(xx) else [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
  render_checks.append({'page':i+1,'dpi':dpi,'changed_pixels':int(diff.sum()),'outside_ROI_strict0_pixels':bad,'pixel_diff_bbox':box})
  if dpi==600:
   for n,(x0,y0,x1,y1) in enumerate([(0,0,ww//2,hh//2),(ww//2,0,ww,hh//2),(0,hh//2,ww//2,hh),(ww//2,hh//2,ww,hh)],1):Image.fromarray(cand[y0:y1,x0:x1]).save(QA/f'zoom-p{i+1:02d}-q{n}-600.png')
  del current,cand,diff,ok
  print('Rendered and strict checked',i+1,dpi,flush=True)
# Source P7 at matching full geometry; this is historical context only, not the base for the new ROI acceptance.
for dpi in [200,600]:Image.fromarray(render(H['source'],6,dpi)).save(QA/f'source-p07-{dpi}.png')
# Regional 1200dpi strict ROI and unchanged glyph/red-pixel evidence.
region=(392,376,426,400);aa=render(H['current'],6,1200,clip=region);bb=render(str(C),6,1200,clip=region)
# Pixel-perfect protected glyph bbox, already proven native exact.
glyphbox=(407.1,383.0,417.0,392.1)
ga=render(H['current'],6,1200,clip=glyphbox);gb=render(str(C),6,1200,clip=glyphbox);assert np.array_equal(ga,gb)
red_a=(aa[:,:,0]>180)&(aa[:,:,1]<120)&(aa[:,:,2]<120);red_b=(bb[:,:,0]>180)&(bb[:,:,1]<120)&(bb[:,:,2]<120)
assert np.array_equal(red_a,red_b)
# Disclosed official threshold diagnostic; acceptance still includes the stricter pixel counts above.
official=verify.outside_pixels(H['current'],str(C),allowed,dpi=200,thr=48,min_size=2,pad=2,merge=4)
assert not official
structure=verify.structure_check(H['current'],str(C));assert structure['ok'] and structure['changed_pages']==[7]
result={'candidate':str(C),'candidate_SHA256':sha(C),'source_SHA256':sha(H['source']),'current_SHA256':sha(H['current']),'source_current_hashes_held':True,'B0':'43/43 PASS via existing Windows short paths in same staging','original_native_operator_retention':True,'only_new_clipping_prefixes_suffixes':True,'native_pages':NATIVE,'all62_curve_path_style_checks':CURVES,'LH96_locks':TABLE,'label_background_glyph_path_style_checks':GLYPHS,'raw_streams':STREAMS,'resources':RES,'metadata_links':META,'render_checks':render_checks,'glyph_1200dpi_pixels_identical':True,'red_1200dpi_mask_identical':True,'official_outside_ROI_48_min2_pad2_merge4':official,'structure':structure,'plan':PLAN,'visual_review_pending':True,'source_current_candidate_regions_200_600_1200':True,'not_whole_project_completion':True}
dump(QA/'QA-machine.json',result);D.close();R.close();P.close();E.close()
print('MACHINE QA PASSED',sha(C),flush=True)
