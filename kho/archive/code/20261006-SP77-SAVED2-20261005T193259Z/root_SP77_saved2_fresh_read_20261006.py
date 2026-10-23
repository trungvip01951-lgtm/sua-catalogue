"""ROOT fresh read of saved candidate2, with representative visible pen checks.
No PDF authoring or additional sample. Whole-font sharpening remains unknown.
"""
import os
for n in('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[n]='1'
import json,hashlib,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np,pymupdf as fitz
from scipy.ndimage import map_coordinates
from PIL import Image
import root_SP77_static15_material_20261006 as M
from catfix.pdfdoc import PdfDoc
from catfix.cs import parse
from g04_perotac_whole_actual_read50 import render_document,metadata
from g04_perotac_whole_pdf_tools46 import pixel_at
R=M.R;D=R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE2'
PLAN=R/'ROOT8SP77 FINAL SAMPLE2 STATIC INSET GRID LABEL HOLES/01 EXPLICIT LAST2 STATIC NO PDF.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=M.rd(PLAN);receipt=M.rd(D/'07 SAVED CANDIDATE RECEIPT.json');candidate=Path(receipt['candidate'])
 assert sha(candidate)=='48c8535c4c8a025991be53caf414242cbb500eb43ac59f804a2008204691a6a2'
 M.guard(p['guards']);pics=M.rd(D/'05 ACTUAL PICTURES.json');saved=[r for r in pics if r['name']=='SAVED'];assert len(saved)==27
 original=M.rd(M.PURE);physical={r['model'].split('-')[-1]:np.array(r['segments_QH_decimal20'],float)for r in original['records15']}
 assert all(k['changed_pixels']==k['maximum_delta']==0 for k in receipt['keepers'])
 assert all(k['strict0_pad0_pixels']==k['strict0_max_delta']==0 for k in receipt['outside24'])
 doc=PdfDoc(str(candidate),backend='pikepdf')
 try:
  natives=[sha for sha in map(M.dig,[doc.page_content(i)for i in range(12)])]
  expected=p['baseline_native12'].copy();expected[8]=p['native']['SHA256'];assert natives==expected
  native=doc.page_content(8);assert native==Path(p['native']['path']).read_bytes()
  sourcebase=native[slice(*p['original_base_unchanged_byte_range'])];assert M.dig(sourcebase)==p['base_original_native_SHA256']
 finally:doc.close()
 read=[];profiles=[]
 with fitz.open(candidate)as current,fitz.open(p['current'])as before:
  assert json.loads(json.dumps(metadata(current),default=str))==json.loads(json.dumps(metadata(before),default=str))
  for cap in saved:
   clip=[float(F(x))for x in cap['page_bbox']]if cap.get('page_bbox')else None
   a,am=render_document(current,8,cap['dpi'],clip);b=np.array(Image.open(cap['path']).convert('RGB'))
   assert a.shape==b.shape and am==cap['geometry'];delta=np.abs(a.astype('int16')-b.astype('int16'))
   read.append({'tag':cap['tag'],'path':cap['path'],'SHA256':sha(cap['path']),'fresh_RGB_SHA256':M.dig(a.tobytes()),
    'geometry_same':True,'fresh_vs_writer_changed':int(np.any(delta!=0,2).sum()),'fresh_vs_writer_maxdelta':int(delta.max())})
   assert not delta.any(),('CAPTURE_RECIPE_DELTA',cap['tag'])
  chart=next(r for r in saved if r['tag']=='CHART600');clip=[float(F(x))for x in chart['page_bbox']];a,am=render_document(current,8,600,clip)
  # 0.12 pt is one600dpi pixel; declare finite raster tolerance before measuring.
  offsets=np.linspace(-8,8,257);along=np.linspace(-.4,.4,5);chroma=np.array([10,12],float);norm=float(chroma@chroma)
  for suffix,segs in physical.items():
   Q=36.;c=next(c for c in segs if c[0,0]<=Q<=c[-1,0]);lo,hi=0.,1.
   for _ in range(70):
    t=(lo+hi)/2;pt=(1-t)**3*c[0]+3*(1-t)**2*t*c[1]+3*(1-t)*t*t*c[2]+t**3*c[3]
    if pt[0]<Q:lo=t
    else:hi=t
   tangent=3*(1-t)**2*(c[1]-c[0])+6*(1-t)*t*(c[2]-c[1])+3*t*t*(c[3]-c[2])
   pp=np.array([float(M.X0)+float(M.AX)*pt[0],float(M.Y0)+float(M.HY)*pt[1]])
   direction=np.array([float(M.AX)*tangent[0],-float(M.HY)*tangent[1]]);direction/=np.linalg.norm(direction)
   normal=np.array([-direction[1],direction[0]]);center=pixel_at(pp,am);values=[];colors=[]
   for dl in along:
    coords=center+dl*direction+offsets[:,None]*normal
    rgb=np.array([map_coordinates(a[:,:,k].astype(float),[coords[:,1]-.5,coords[:,0]-.5],order=1,mode='constant',cval=255)for k in range(3)]).T
    alpha=np.clip(((rgb[:,1]-rgb[:,0])*10+(rgb[:,2]-rgb[:,0])*12)/norm,0,1);values.append(alpha);colors.append(rgb)
   alpha=np.mean(values,0);rgb=np.mean(colors,0);width=float(np.trapezoid(alpha,offsets)*72/600);peak=float(alpha.max())
   core=rgb[alpha>.98];med=np.median(core,axis=0).tolist()if len(core)else None
   result=abs(width-float(M.WIDTH))<=.12 and peak>.90 and med is not None and max(abs(np.array(med)-[98,108,110]))<1.5
   profiles.append({'suffix':suffix,'Q_m3h':Q,'physical_point':pt.tolist(),'normal_equivalent_color_width_pt':width,
    'chosen_native_width_pt':float(M.WIDTH),'tolerance_before_measure_one600pixel_pt':.12,'peak_chroma':peak,'core_RGB_median':med,'PASS_representative_ink':bool(result)})
  assert all(r['PASS_representative_ink']for r in profiles)
 z={'status':'ROOT_FRESH_SAVED2_NATIVE12_CAPTURE27_VISIBLE_PEN15_SCOPED_NOT_ADOPTED','candidate':str(candidate),'candidate_SHA256':sha(candidate),
  'current_held_SHA256':sha(p['current']),'source_held_SHA256':sha(p['source']),'plan':str(PLAN),'plan_SHA256':sha(PLAN),
  'fresh_native12':natives,'old_base569_unchanged':True,'fresh_actual_captures27':read,'visible_pen15':profiles,
  'ROOT_manually_opened_all27_saved':True,'ROOT_actual_visual_observations':{
   'curves':'All15 smooth with consistent gray stroke and dash rhythm; no visible worm/trace fragments.',
   'labels':'All15 literal suffixes recognized in27 saved images. Source bitmap1 is a vertical stroke; grid-vs1 attribution is being checked independently, no full visual acceptance yet.',
   'table7_read':['39','59','79','200','240','280','38'],'title':'8SP77 visible unchanged; axes/ETA/leftphoto retained.'},
  'font_identity_phase_sharpness':'UNKNOWN; original source raster fringe held',
  'no_full_catalogue_acceptance':True,'canonical_adopted':False,'operations':{'PDF_Save':0,'Job':0,'new_candidate':0,'canonical':0,'control':0}}
 fp=D/'08 ROOT FRESH READ27 PEN15 NO ADOPT.json'
 with fp.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({'path':str(fp),'sha':sha(fp),'fresh27pixel0':True,'representative15ink':all(r['PASS_representative_ink']for r in profiles),
  'width_range_pt':[min(r['normal_equivalent_color_width_pt']for r in profiles),max(r['normal_equivalent_color_width_pt']for r in profiles)]},ensure_ascii=False))
if __name__=='__main__':main()
