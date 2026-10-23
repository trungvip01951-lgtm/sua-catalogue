"""Read-only localization of candidate1 keeper pixels; no PDF authorship."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,sys,hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np,pymupdf as fitz
from PIL import Image
sys.path.insert(0,r'D:\ChatGPT\Sửa catalogue\vendor\catfix_original\GOI_SUA_CATALOGUE_CHATGPT')
from g04_perotac_whole_actual_read50 import render_document
import root_SP77_static15_material_20261006 as M
P=M.R/'ROOT8SP77 STATIC15 20261005T183933Z-ac1b75/02 FULL STATIC15 FONT15 TABLE7 NO PDF.json'
D=M.R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE1'
OUT=D/'LOCALIZED KEEPER READONLY'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=json.loads(P.read_text(encoding='utf8'));candidate=D/Path(p['current']).name
 assert sha(candidate)=='ceff326d6b06bf67195ec1b997c1d504797c98111c8117d3d8a29eaf05d3f8a0'
 assert sha(p['current'])==p['guards'][p['current']]
 OUT.mkdir(exist_ok=False);rows=[]
 with fitz.open(p['current'])as before,fitz.open(candidate)as after:
  for k in p['keepers']:
   clip=list(map(lambda s:float(F(s)),k['page_bbox']))
   a,am=render_document(before,8,600,clip);b,bm=render_document(after,8,600,clip)
   assert am==bm;dd=np.max(np.abs(a.astype('int16')-b.astype('int16')),axis=2);yy,xx=np.where(dd>0)
   if len(xx):
    Tinv=~fitz.Matrix(am['T']);points=[]
    for x,y in zip(xx,yy):
     pt=fitz.Point((x+am['origin'][0]+.5)/am['scale'],(y+am['origin'][1]+.5)/am['scale'])*Tinv
     points.append(M.uv([F(str(pt.x)),F(str(pt.y))]))
    uv=np.array([[float(v)for v in r]for r in points]);bounds=[*uv.min(0),*uv.max(0)]
    unique_x=sorted(set(np.round(uv[:,0],3).tolist()));unique_y=sorted(set(np.round(uv[:,1],3).tolist()))
   else:bounds=None;unique_x=[];unique_y=[]
   row={**k,'changed_pixels':len(xx),'max_delta':int(dd.max()),'changed_uv_center_bounds':bounds,
        'unique_source_u_centres':unique_x,'unique_source_v_centres':unique_y}
   for tag,ar in [('BEFORE',a),('SAVED',b)]:
    fp=OUT/(k['tag']+' '+tag+'.png');Image.fromarray(ar).save(fp);row[tag]={'path':str(fp),'sha':sha(fp)}
   rows.append(row)
 fp=OUT/'01 EXACT KEEPER DELTA LOCALIZATION NO PDF.json'
 fp.write_text(json.dumps({'source_current':p['current'],'current_SHA':sha(p['current']),'candidate':str(candidate),'candidate_SHA':sha(candidate),
   'dpi':600,'threshold':0,'keepers':rows,'PDF_Save':0,'canonical':0},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps({'path':str(fp),'sha':sha(fp),'rows':[{k:r[k]for k in('tag','changed_pixels','max_delta','changed_uv_center_bounds')}for r in rows]},ensure_ascii=False))
if __name__=='__main__':main()
