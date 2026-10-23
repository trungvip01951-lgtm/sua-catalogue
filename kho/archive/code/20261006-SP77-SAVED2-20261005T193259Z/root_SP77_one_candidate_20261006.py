"""ROOT single CATFIX candidate from a frozen reviewed SP77 native plan.
No refit/font/image creation. One existing content payload replaces ref160.
No canonical publication or automatic retry. Reads saved result before review.
"""
import os
for task_env in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[task_env]='1'
import argparse,copy,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as F
import pikepdf,pymupdf as fitz,numpy as np
from PIL import Image
PROJECT=Path(r'D:\ChatGPT\Sửa catalogue')
sys.path.insert(0,str(PROJECT/'tools'));sys.path.insert(0,str(PROJECT/'vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT'))
import catalogue as C
from catfix.pdfdoc import PdfDoc
from catfix.cs import Ref,parse,serialize
from catfix import verify
import qa_sol_SP8_existing24_frozen207_oneSave_writer_208 as B
from g04_perotac_whole_actual_read50 import render_document,metadata
from root_SP8_one_actual_frozen_20261005 import outside
R=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05')
OUT=R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE1'
sha=B.sha;dig=B.dig;rd=B.rd;typed=B.typed;guard=B.guard
def write(p,z):return B.write(p,z)
class Graph:
 def __init__(self,native,aliases):self.native=native;self.map={};self.rev={};self.streams=[];self.aliases=aliases;self.resource_additions=[]
 def walk(self,a,b,path):
  ai,bi=getattr(a,'is_indirect',False),getattr(b,'is_indirect',False);assert ai==bi
  if ai:
   ar,br=tuple(a.objgen),tuple(b.objgen)
   if ar in self.map:assert self.map[ar]==br;return
   assert br not in self.rev;self.map[ar]=br;self.rev[br]=ar
  edited=isinstance(a,pikepdf.Stream)and tuple(a.objgen)==(160,0)
  if isinstance(a,pikepdf.Stream):
   assert isinstance(b,pikepdf.Stream)
   if edited:assert b.read_bytes()==self.native
   else:assert a.read_raw_bytes()==b.read_raw_bytes()and B.decoded(a)==B.decoded(b),('STREAM_CHANGED',path)
   self.streams.append({'path':path,'old':list(a.objgen),'saved':list(b.objgen),'edited160':edited,
    'RAW_before':dig(a.read_raw_bytes()),'RAW_saved':dig(b.read_raw_bytes())})
  if isinstance(a,(pikepdf.Dictionary,pikepdf.Stream)):
   assert isinstance(b,(pikepdf.Dictionary,pikepdf.Stream))
   extra=set(b.keys())-set(a.keys());assert not set(a.keys())-set(b.keys()),path
   if extra:
    assert path.endswith('/Resources/XObject')and extra=={'/'+r['alias']for r in self.aliases}and not self.resource_additions,('NEW_KEYS',path,extra)
    self.resource_additions.append({'path':path,'extra_aliases':sorted(extra)})
    # Their old nodes are all already reachable through accepted SP25/SP95.
    # Check target bijection only after the full old graph is walked.
   else:assert set(a.keys())==set(b.keys())
   for k in a.keys():
    if edited and k=='/Length':assert b[k]==len(b.read_raw_bytes())
    else:self.walk(a[k],b[k],path+k)
  elif isinstance(a,pikepdf.Array):
   assert isinstance(b,pikepdf.Array)and len(a)==len(b)
   for i,(x,y)in enumerate(zip(a,b)):self.walk(x,y,path+'['+str(i)+']')
  elif isinstance(a,pikepdf.Name):assert isinstance(b,pikepdf.Name)and str(a)==str(b)
  elif isinstance(a,pikepdf.String):assert isinstance(b,pikepdf.String)and bytes(a)==bytes(b)
  else:assert type(a)==type(b)and a==b,('LEAF_CHANGED',path,str(a),str(b))
def saved_graph(current,candidate,native,baseline,aliases):
 with pikepdf.open(current)as a,pikepdf.open(candidate)as b:
  g=Graph(native,aliases);g.walk(a.Root,b.Root,'Root')
  for k in('/Info','/Encrypt'):
   assert(k in a.trailer)==(k in b.trailer)
   if k in a.trailer:g.walk(a.trailer[k],b.trailer[k],'Trailer'+k)
  assert len(a.objects)==len(b.objects)==len(g.map)==len(g.rev)==225
  assert len(g.streams)==197 and sum(v['edited160']for v in g.streams)==1
  assert len(g.resource_additions)==1
  for r in aliases:
   actual=b.pages[8].Resources.XObject['/'+r['alias']]
   assert tuple(actual.objgen)==g.map[tuple(r['existing_Ref'])]
  expected=baseline.copy();expected[8]=dig(native)
  d=PdfDoc(str(candidate),backend='pikepdf')
  try:
   assert[dig(d.page_content(i))for i in range(12)]==expected
   image=d.resource(d.page_resources(8),'XObject','X11')
   assert tuple(image)==g.map[(166,0)] and dig(d.stream_raw(image))=='c3c8e360d59ab43eee382610bb3815dd5a656671761e81161e91063a1b94b444'
  finally:d.close()
  return {'bijection225':True,'stream197_other196_RAW_decoded_held':True,'stream_proofs':g.streams,
   'mapping':[{'old':list(k),'saved':list(v)}for k,v in sorted(g.map.items())],'native12_SHA256':expected,'X11_RAW_held':True,
   'resource_additions':g.resource_additions,'aliases11_to_old_nodes_exact':True}
def run(planpath,gatepath):
 p,g=rd(planpath),rd(gatepath)
 assert g['allow_one_candidate']is True and g['canonical']is False and g['maximum_Save_calls']==1
 assert g['writer_SHA256']==sha(__file__)and g['plan_SHA256']==sha(planpath)
 assert g['marker_success']is True and sha(g['marker_path'])==g['marker_SHA256']
 assert g['ROOT_font_style_scoped_selected']is True and len(g['font_style_receipts'])==2
 for r in g['font_style_receipts']:assert sha(r['path'])==r['SHA256']
 guard(p['guards']);guard(g['guards'])
 native=Path(p['native']['path']).read_bytes();assert dig(native)==p['native']['SHA256']and serialize(parse(native))==native
 assert p['status']=='ROOT_SELECTED_STATIC15_LABEL15_TABLE7_NO_PDF'
 assert all(x['PASS_positive_gap']for x in p['gaps225'])and all(x['unique_nearest_owner']for x in p['labels15'])
 assert not p['obstacles']and len(p['table7'])==7 and len(p['labels15'])==15
 ctx=C.context(Path(p['current']).name);C.validate_context(ctx)
 assert ctx['source_sha256']==p['guards'][p['source']]and ctx['current_sha256']==p['guards'][p['current']]
 assert not OUT.exists(),'CANDIDATE1_ALREADY_CONSUMED_NO_AUTOMATIC_RETRY'
 OUT.mkdir();candidate=OUT/Path(p['current']).name
 actor='/root';session='SP77-SOURCE-SUFFIX-CANDIDATE1'
 lease=C.claim(Path(p['current']).name,actor,session,'Single CATFIX SP77 frozen15/source labels15/table7 candidate; no canonical or retry',1800)
 job=None;calls=0
 try:
  write(OUT/'00 CLAIM INPUT GATE.json',{'lease':lease,'plan':str(planpath),'plan_SHA256':sha(planpath),'gate':str(gatepath),'gate_SHA256':sha(gatepath)})
  from catfix.recipes import Job
  C.check(lease['token'],actor,session);guard(p['guards']);guard(g['guards'])
  job=Job(p['current'],str(candidate),backend='pikepdf',log_path=str(OUT/'01 CATFIX LOG.json'));d=job.E.doc
  before=[B.profile(d,Ref(o.objgen))for o in d.pdf.objects];resources=typed([d.page_resources(i)for i in range(12)])
  assert len(before)==225 and sum(x['stream']for x in before)==197
  assert[dig(d.page_content(i))for i in range(12)]==p['baseline_native12']
  assert d.page_contents_refs(8)==[Ref((160,0))]and d.resource(d.page_resources(8),'XObject','X11')==Ref((166,0))
  assert job._R is None;d.set_stream(Ref((160,0)),native);job.E.pages.clear()
  expected_resources=copy.deepcopy(resources)
  for r in p['aliases11']:
   newname=d.add_xobject_to_page(8,Ref(tuple(r['existing_Ref'])),prefix='CfxSP77Token')
   assert newname==r['alias'];expected_resources[8]['XObject'][newname]={'Ref':r['existing_Ref']}
  after=[B.profile(d,Ref(o.objgen))for o in d.pdf.objects]
  # Page9 is the sole old dictionary with11 new source-node aliases.
  changed=[(a,b)for a,b in zip(before,after)if a!=b and a['Ref']!=[160,0]]
  assert len(after)==225 and len(changed)==1 and changed[0][0]['Ref']==[12,0]
  assert typed([d.page_resources(i)for i in range(12)])==expected_resources
  for roi in p['allowed_page_ROIs']:job._add(8,list(map(lambda v:float(F(v)),roi)),'SP77 curves15/source suffix15/minimal table7','SP77-source-suffix-frozen')
  write(OUT/'02 RAM OLD223 HELD.json',{'old_profiles':before,'after_profiles':after,'resources12_before':resources,'resources12_expected_after':expected_resources,
   'page12_dictionary_alias11_change':changed,'newimage_newfont_newContent':0,'newaliases_to_old_images':11})
  C.check(lease['token'],actor,session);guard(p['guards']);guard(g['guards'])
  calls+=1;job.save();check=job.check(raster=True);write(OUT/'03 CATFIX CHECK.json',check);job.close();job=None
  graph=saved_graph(p['current'],candidate,native,p['baseline_native12'],p['aliases11']);write(OUT/'04 SAVED GRAPH225.json',graph)
  photos=[];keepers=[];outside24=[]
  with fitz.open(p['current'])as before_doc,fitz.open(candidate)as saved:
   ma,mb=metadata(before_doc),metadata(saved)
   assert json.loads(json.dumps(ma,default=str))==json.loads(json.dumps(mb,default=str))
   for i,cap in enumerate(p['captures'],1):
    clip=list(map(lambda v:float(F(v)),cap['page_bbox']))if cap.get('page_bbox')else None
    for label,doc in [('BEFORE',before_doc),('SAVED',saved)]:
     a,m=render_document(doc,8,cap['dpi'],clip);fp=OUT/f'{i:02d} {label} {cap["tag"]}.png';Image.fromarray(a).save(fp)
     photos.append({**cap,'name':label,'path':str(fp),'SHA256':sha(fp),'RGB_SHA256':dig(a.tobytes()),'geometry':m})
   for k in p['keepers']:
    clip=list(map(lambda v:float(F(v)),k['page_bbox']));a,am=render_document(before_doc,8,600,clip);b,bm=render_document(saved,8,600,clip)
    assert am==bm and a.shape==b.shape;delta=np.abs(a.astype(np.int16)-b.astype(np.int16))
    keepers.append({**k,'dpi':600,'changed_pixels':int(np.any(delta!=0,2).sum()),'maximum_delta':int(delta.max())})
   for dpi in(100,200):
    for pi in range(12):
     a,am=render_document(before_doc,pi,dpi);b,bm=render_document(saved,pi,dpi);assert am==bm and a.shape==b.shape
     outside24.append({'page':pi+1,**outside(a,b,am,p['allowed_page_ROIs']if pi==8 else[],dpi)})
  write(OUT/'05 ACTUAL PICTURES.json',photos)
  write(OUT/'06 KEEPER OUTSIDE24.json',{'keepers':keepers,'outside24':outside24})
  assert all(v['changed_pixels']==v['maximum_delta']==0 for v in keepers),'KEEPER_DELTA'
  assert all(v['strict0_pad0_pixels']==v['strict0_max_delta']==0 for v in outside24),'OUTSIDE_STRICT0_DELTA'
  official=verify.outside_pixels(p['current'],str(candidate),{9:[list(map(lambda v:float(F(v)),r))for r in p['allowed_page_ROIs']]},dpi=200,thr=0,min_size=0,pad=0)
  assert not official and check['ok'],('CATFIX_OR_OUTSIDE',official,check)
  guard(p['guards']);guard(g['guards']);C.check(lease['token'],actor,session)
  z={'status':'SP77_CANDIDATE1_SAVED_NUMBER_GRAPH_PASS_VISUAL_PENDING_NOT_ADOPTED',
   'plan':str(planpath),'plan_SHA256':sha(planpath),'gate':str(gatepath),'gate_SHA256':sha(gatepath),
   'source':p['source'],'current':p['current'],'source_SHA256':ctx['source_sha256'],'current_SHA256':ctx['current_sha256'],
   'candidate':str(candidate),'candidate_SHA256':sha(candidate),'native_SHA256':dig(native),'graph':graph,
   'pictures':photos,'keepers':keepers,'outside24':outside24,'Job_check':check,
   'operations':{'Job':1,'Save_calls':calls,'actual_same_method_attempts':1,'newaliases_to_old_source_images':11,'newimages':0,'newfonts':0,'refit':0,'canonical':0,'control':0},
   'original_task_count':'137/149 unchanged; expanded15curves7cells only','full_catalogue_complete':False,'visual':'PENDING_ROOT_AND_INDEPENDENT'}
  print(json.dumps(write(OUT/'07 SAVED CANDIDATE RECEIPT.json',z),ensure_ascii=False))
 except Exception as e:
  write(OUT/'99 FAILURE NO RETRY.json',{'error':type(e).__name__+': '+str(e),'Save_calls':calls,'candidate_exists':candidate.exists(),'candidate_SHA256':sha(candidate)if candidate.exists()else None,'actual_consumed':1,'canonical':0,'retry':False});raise
 finally:
  try:
   if job:job.close()
  finally:C.release(lease['token'],actor,session,'SP77 candidate1 ended; no canonical adoption or retry; '+str(OUT))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('plan',type=Path);ap.add_argument('gate',type=Path);a=ap.parse_args();run(a.plan,a.gate)
