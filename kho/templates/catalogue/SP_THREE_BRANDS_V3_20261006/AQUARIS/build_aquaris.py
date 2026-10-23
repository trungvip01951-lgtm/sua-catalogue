"""Authorized full visual redesign; reuse verified AQUARIS data, catfix-only PDF save."""
from pathlib import Path
import sys,json,math,hashlib,subprocess,base64
import numpy as np
import fitz,pikepdf
from PIL import Image
from vector_layout import *
R=Path(r'D:\ChatGPT\Sửa catalogue');D=Path(__file__).parent
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=read(R/'work/sp_three_brands/aquaris_accepted.json');BASE=Path(receipt['canonical']);EXPECTED=receipt['canonical_after']
assert sha(BASE)==EXPECTED
DATA=read(D/'curves/AQUARIS_CONCAVE_197_NO_H_DELTA.json');TABLES=read(D/'tables/complete_table_metadata.json')['tables'];INFO=read(D/'assets/aquaris_nonqh_content.json')
BY={r['model']:r for r in DATA['records']};META={t['family']:t for t in TABLES};SMALL={r['family']:r for r in INFO['small_families']};LARGE={r['family']:r for r in INFO['large_families']}
DOC=fitz.open(BASE);PHOTO={}
for i,p in enumerate(DOC):
 ims=[im for im in p.get_image_info(xrefs=True) if im['height']>im['width']*3 and im['bbox'][3]-im['bbox'][1]>150 and im['xref']]
 if ims:PHOTO[i+1]=max(ims,key=lambda im:im['bbox'][3]-im['bbox'][1])
STAMP=read(D/'assets/SUMOTO_ASSET_AUDIT.json');PATCH={}
for g in STAMP['groups']:
 for im in g['images']:
  x=im['xref'];rect=im['stamp_rect_native']
  if not rect:continue
  if x in [436,438]:PATCH[x]={'source_xref':442,'rect':rect,'source_size':[67,665]}
  else:
   base=450 if x in [450,455] else 458 if x==458 else 468
   head=Image.open(D/f'assets/AQ-x{base}-head-native.png')
   PATCH[x]={'file':str(D/f'assets/clean-head-{base}.png'),'rect':rect,'head_size':list(head.size)}
def sourcephoto(p,sourcepage,x,y,maxw,maxh):
 im=PHOTO[sourcepage];scale=min(maxw/im['width'],maxh/im['height']);ww=im['width']*scale;hh=im['height']*scale
 p.source_image(im['xref'],x+(maxw-ww)/2,y+(maxh-hh)/2,ww,hh)
def heading(p,family,subtitle='STAINLESS STEEL SUBMERSIBLE PUMPS'):
 p.text(family,30,55,32,'Bold');p.text(subtitle,31,78,8.8,'Bold',TEAL)
 p.source_image(432,446,21,121,41.5);p.line(30,94,568,94,TEAL,1.2)
 p.line(30,822,568,822,GRID,.6);p.text('AQUARIS  /  SP SERIES',30,837,8,'Bold',MUTED);p.text(f'{p.index:02d} / 31',568,837,8,'Body',MUTED,'right')
def section(p,title,x,y):p.text(title.upper(),x,y,9.5,'Bold',TEAL)
def modelcode(p,info,x,y,width,small=False):
 mc=info['model_code'];fs=8 if small else 10
 p.text('MODEL CODE',x,y,8,'Bold',TEAL);p.text(mc['example_source_literal'],x+76,y,fs,'Bold')
 lines=['Well diameter / SP series / Capacity (m³/h) / Stage / Motor power (kW)',mc['well_label_source']]
 return p.paragraph(lines,x,y+14,width,7.5 if small else 8,11)
def chart(p,rows,plot):
 x,y,w,h=plot;qm=max(max(r['Q']) for r in rows);hm=max(r['H'][0] for r in rows)
 step=10**math.floor(math.log10(hm/5));step=next(v*step for v in [1,2,2.5,5,10] if v*step>=hm/5)
 ymax=math.ceil(hm*1.04/step)*step;X=lambda q:x+q/qm*w;Y=lambda v:y+h-v/ymax*h
 for tick in np.arange(0,ymax+step*.01,step):p.line(x,Y(tick),x+w,Y(tick));p.text(fmt(tick),x+w+7,Y(tick)+3,7.5,'Body',MUTED)
 # Exact axis proportions; at most seven main ticks, one decimal where needed.
 qstep=10**math.floor(math.log10(qm/5));qstep=next(v*qstep for v in [1,2,2.5,5,10] if v*qstep>=qm/6)
 ticks=list(np.arange(0,qm+1e-8,qstep))
 if abs(ticks[-1]-qm)>1e-6:ticks.append(qm)
 for q in ticks:
  p.line(X(q),y,X(q),y+h);p.text(fmt(round(float(q),1)),X(q),y+h+16,8,'Bold',TEAL,'center');p.text(fmt(round(float(q)*1000/60,1)),X(q),y+h+30,7.3,'Body',MUTED,'center')
 p.line(x,y,x,y+h,MUTED,.65);p.line(x,y+h,x+w,y+h,MUTED,.65)
 p.text('Q (m³/h)',x-8,y+h+16,7.5,'Bold',TEAL,'right');p.text('Q (l/min)',x-8,y+h+30,7.2,'Body',MUTED,'right')
 p.text('Total head H (m)',x-81,y+h*.64,8.2,'Bold',TEAL,rotate=True)
 ordered=sorted(rows,key=lambda r:-r['H'][0]);ys=[Y(r['H'][0])+2.7 for r in ordered]
 for j in range(1,len(ys)):ys[j]=max(ys[j],ys[j-1]+10.2)
 overflow=max(0,ys[-1]-(y+h-4));ys=[v-overflow for v in ys]
 for j in range(len(ys)-2,-1,-1):ys[j]=min(ys[j],ys[j+1]-10.2)
 assert ys[0]>=y-3,(p.index,ys)
 for r,ly in zip(ordered,ys):
  p.curve(r['segments'],X,Y,r['model']);p.text(r['model'],x-8,ly,7.8,'Bold',TEAL,'right')
  p.line(x-5,ly-2.7,x,Y(r['H'][0]),TEAL,.4)
 p.tables.append({'type':'axes','plot':plot,'Qmax':qm,'Hmax':ymax,'models':[r['model'] for r in ordered]})
def performance_table(p,t,top):
 rows=t['rows'];cr=[BY[r['model']] for r in rows];qs=sorted(set(q for r in cr for q in r['Q']))
 dims=[]
 for k,label in [('length_mm','Length'),('length1_mm','Length1'),('length2_mm','Length2'),('weight_kg','Weight')]:
  if any(r.get(k) is not None for r in rows):dims.append((k,label,'kg' if k=='weight_kg' else 'mm'))
 x=30.;ww=538.;rh=13.;hh=43.;widths=[79,28,28,27]+[(ww-79-56-27-len(dims)*39)/len(qs)]*len(qs)+[39]*len(dims);xx=[x]
 for v in widths:xx.append(xx[-1]+v)
 bottom=top+hh+rh*len(rows);assert bottom<=817.1
 section(p,'Performance data',30,top-12)
 p.rect(x,top,ww,hh,TEAL)
 for j in range(len(rows)):
  if j%2==0:p.rect(x,top+hh+j*rh,ww,rh,PALE)
 p.text('MODEL',(xx[0]+xx[1])/2,top+26,8,'Bold',WHITE,'center')
 pc=(xx[1]+xx[3])/2;p.text('P',pc-4,top+13,9,'Bold',WHITE);p.text('2',pc+2,top+15,6,'Bold',WHITE)
 for i,s in [(1,'kW'),(2,'HP')]:p.text(s,(xx[i]+xx[i+1])/2,top+33,8,'Bold',WHITE,'center')
 p.text('Q',(xx[3]+xx[4])/2,top+13,9,'Bold',WHITE,'center');p.text('m³/h',(xx[3]+xx[4])/2,top+26,7,'Body',WHITE,'center');p.text('l/min',(xx[3]+xx[4])/2,top+38,6.8,'Body',WHITE,'center')
 p.text('FLOW / TOTAL HEAD',(xx[4]+xx[4+len(qs)])/2,top+12,8,'Bold',WHITE,'center')
 for j,q in enumerate(qs):
  cx=(xx[4+j]+xx[5+j])/2;p.text(fmt(q),cx,top+26,8,'Bold',WHITE,'center');p.text(fmt(round(q*1000/60,1)),cx,top+38,7,'Body',WHITE,'center')
 for j,(_,label,unit) in enumerate(dims):
  k=4+len(qs)+j;cx=(xx[k]+xx[k+1])/2;p.text(label,cx,top+16,7,'Bold',WHITE,'center');p.text(unit,cx,top+34,7,'Body',WHITE,'center')
 for j,(m,r) in enumerate(zip(rows,cr)):
  yy=top+hh+j*rh+9.3
  p.text(r['model'],(xx[0]+xx[1])/2,yy,8,'Bold',INK,'center')
  for k,v in [(1,m['kw']),(2,m['HP'])]:p.text(fmt(v),(xx[k]+xx[k+1])/2,yy,8,'Body',INK,'center')
  for k,q in enumerate(qs):
   hv=dict(zip(r['Q'],r['H'])).get(q);p.text(fmt(hv),(xx[4+k]+xx[5+k])/2,yy,8,'Body',INK,'center')
  for k,(key,_,_) in enumerate(dims):
   col=4+len(qs)+k;p.text(fmt(m.get(key)),(xx[col]+xx[col+1])/2,yy,8,'Body',INK,'center')
 # Merged H column remains clear, every other cell has the same complete border.
 p.text('H (m)',(xx[3]+xx[4])/2,top+hh+rh*len(rows)/2+3,8,'Bold',TEAL,'center')
 for k,v in enumerate(xx):
  start=top+19 if k==2 else top+17 if 5<=k<4+len(qs) else top
  p.line(v,start,v,bottom,GRID,.55)
 for yy in [top,top+hh,bottom]:p.line(x,yy,x+ww,yy,GRID,.55)
 p.line(xx[1],top+19,xx[3],top+19,GRID,.55);p.line(xx[3],top+17,xx[4+len(qs)],top+17,GRID,.55);p.line(xx[3],top+30,xx[4+len(qs)],top+30,GRID,.55)
 for j in range(1,len(rows)):
  yy=top+hh+j*rh;p.line(x,yy,xx[3],yy,GRID,.55);p.line(xx[4],yy,x+ww,yy,GRID,.55)
 p.tables.append({'type':'QH','family':t['family'],'top':top,'bottom':bottom,'x_columns':xx,'Q':qs,'models':[r['model'] for r in cr],'row_height':rh,'header_height':hh,'dimensions':dims})
def performance(p,t):
 fam=t['family'];small=fam in SMALL;heading(p,fam)
 if small:
  info=SMALL[fam];section(p,'Applications',30,112);p.paragraph(info['applications'],30,127,253,8,12)
  section(p,'Pump / motor',309,112);p.paragraph(info['pump_motor'],309,127,257,8,12)
  modelcode(p,info,30,204,538,True)
 top=817-(43+13*len(t['rows']));charttop=262 if small else 157;chartbottom=top-76
 plot=[185 if small else 127,charttop,358 if small else 416,chartbottom-charttop]
 assert plot[3]>=220,(fam,plot)
 if small:sourcephoto(p,SMALL[fam]['page'],30,250,62,chartbottom-245)
 meta=f'n ≈ {t["rpm"]} /min  |  50 Hz  |  Outlet: {fmt(t["outlet_inches_output"])} in'
 if fam.startswith('6'):meta+='  |  3-phase: 380–415 V'
 p.text(meta,30,244 if small else 116,8,'Body',MUTED)
 dh=t['diffuser_height_mm']
 if dh is not None:
  s=' / '.join(fmt(v) for v in dh) if isinstance(dh,list) else fmt(dh)
  p.text('Diffuser height: '+s+' mm',30,top-27,8,'Body',MUTED)
 chart(p,[BY[r['model']] for r in t['rows']],plot);performance_table(p,t,top)
def introduction(p,info):
 heading(p,info['family']);sourcephoto(p,info['page'],33,123,96,648)
 x=162;y=122
 for title,key in [('Applications','applications'),('Operating conditions','operating_conditions'),('Motor and pump','motor_and_pump')]:
  section(p,title,x,y);y=p.paragraph(info[key],x,y+15,403,8.5,13)+10
 section(p,'Warranty: '+str(info['warranty']['years'])+' years',x,y);p.text(info['warranty']['condition'],x,y+15,8.5);y+=40
 y=modelcode(p,info,x,y,403,False)+18
 section(p,'Components and materials',x,y);y+=10;rh=15;cols=[x,x+138,568]
 p.rect(x,y,406,23,TEAL);p.text('COMPONENT',x+8,y+15,8,'Bold',WHITE);p.text('MATERIAL',x+146,y+15,8,'Bold',WHITE)
 for j,(c,m) in enumerate(info['materials']):
  yy=y+23+j*rh
  if j%2==0:p.rect(x,yy,406,rh,PALE)
  p.text(c,x+7,yy+10.5,8);p.text(m,x+145,yy+10.5,7.7)
 for xx in cols:p.line(xx,y,xx,y+23+rh*len(info['materials']))
 for yy in [y,y+23]+[y+23+rh*j for j in range(1,len(info['materials'])+1)]:p.line(x,yy,568,yy)
 assert y+23+rh*len(info['materials'])<812,(p.index,y)
def cover(p):
 p.source_image(432,30,30,155,53);p.text('SP SERIES',30,145,40,'Bold',TEAL)
 p.text('Stainless steel',30,185,27,'Bold');p.text('submersible pumps',30,220,27,'Bold')
 p.text('PERFORMANCE & TECHNICAL DATA',31,254,10,'Bold',MUTED);p.line(30,277,568,277,TEAL,1.2)
 pages=[3,5,9,14,22,28];width=538/6
 for i,pg in enumerate(pages):
  sourcephoto(p,pg,30+i*width,320,width,400);fam=next(v['family'] for v in INFO['page_map'] if v['page']==pg)
  p.text(fam.split('SP')[0]+' in',30+i*width+width/2,751,11,'Bold',TEAL,'center')
 p.text('50 Hz  |  3–10 inch well pumps',30,790,11,'Body',MUTED)
 p.line(30,822,568,822);p.text('AQUARIS  /  SP SERIES',30,837,8,'Bold',MUTED);p.text('01 / 31',568,837,8,'Body',MUTED,'right')
def contents(p):
 heading(p,'Contents','STAINLESS STEEL SUBMERSIBLE PUMPS  /  50 Hz')
 groups=[('3 inch',['3SP1','3SP2']),('4 inch',['4SP3','4SP5','4SP8','4SP14']),('5 inch',['5SP10','5SP15','5SP20','5SP25','5SP30']),('6 inch',['6SP20','6SP30','6SP46','6SP60']),('8 inch',['8SP77','8SP95','8SP120']),('10 inch',['10SP125','10SP160'])]
 for i,(label,fams) in enumerate(groups):
  y=140+i*103;p.text(label,30,y,18,'Bold',TEAL)
  text='  /  '.join(fams);p.text(text,145,y,12,'Bold')
  p.text('Stainless steel submersible pumps',145,y+22,9,'Body',MUTED)
  pgs=[v['page'] for v in INFO['page_map'] if v.get('family') in fams];p.text(f'Pages {min(pgs):02d}–{max(pgs):02d}',145,y+42,9,'Bold',TEAL)
  p.line(30,y+68,568,y+68)
def make_pages():
 pages=[]
 for i in range(1,32):
  p=Page(i)
  if i==1:cover(p)
  elif i==2:contents(p)
  elif any(t['current_page_31']==i for t in TABLES):performance(p,next(t for t in TABLES if t['current_page_31']==i))
  else:introduction(p,next(v for v in LARGE.values() if v['page']==i))
  pages.append(p)
 return pages
def imops(pdf,p):
 xo=pikepdf.Dictionary();ops=[]
 for j,im in enumerate(p.images):
  ref=im['xref'];obj=pdf.get_object((ref,0));key='/AQIMG'+str(j);xo[key]=obj;x,y,w,h=im['target']
  ops.append(f'q {n(w)} 0 0 {n(h)} {n(x)} {n(H-y-h)} cm {key} Do Q')
  if ref not in PATCH:continue
  a=PATCH[ref];iw=int(obj.Width);ih=int(obj.Height);u0,v0,u1,v1=a['rect'];sx=w/iw;sy=h/ih;cx=x+u0*sx;cy=y+v0*sy;cw=(u1-u0)*sx;ch=(v1-v0)*sy;pk='/AQP'+str(j)
  if 'source_xref' in a:
   po=pdf.get_object((a['source_xref'],0));pw=float(po.Width)*sx;ph=float(po.Height)*sy
  else:
   # Lossless decode/embedding of the tool output; only PDF clipping selects the logo region.
   raw=Image.open(a['file']).convert('RGB');po=pdf.make_stream(raw.tobytes());po.Type=pikepdf.Name.XObject;po.Subtype=pikepdf.Name.Image;po.Width=raw.width;po.Height=raw.height;po.ColorSpace=pikepdf.Name.DeviceRGB;po.BitsPerComponent=8
   pw=a['head_size'][0]*sx;ph=a['head_size'][1]*sy
  xo[pk]=po;ops.append(f'q {n(cx)} {n(H-cy-ch)} {n(cw)} {n(ch)} re W n {n(pw)} 0 0 {n(ph)} {n(x)} {n(H-y-ph)} cm {pk} Do Q')
 return xo,ops
def save(pages):
 lock=read(D/'lock.json');gate=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'tools/catalogue.py'),'check','--actor',lock['actor'],'--session',lock['session'],'--token',lock['token']],capture_output=True,text=True,encoding='utf8');assert gate.returncode==0,gate.stdout
 sys.path.insert(0,str(R/'vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT'));from catfix.vector import Editor
 e=Editor(str(BASE));pdf=e.doc.pdf;fonts=embed_fonts(pdf)
 for pi,p in enumerate(pages):
  pg=e.doc._pages[pi];res=pikepdf.Dictionary(pg.Resources);ff=pikepdf.Dictionary(res.get('/Font',{}))
  for k,v in fonts.items():ff[k]=v
  xo,io=imops(pdf,p);orig=pikepdf.Dictionary(res.get('/XObject',{}))
  for k,v in xo.items():orig[k]=v
  res.Font=ff;res.XObject=orig;pg.Resources=res
  # Source has two smaller pages. Preserve all page boxes, fit the new content uniformly inside each actual page.
  box=DOC[pi].rect;scale=min(box.width/W,box.height/H);dx=(box.width-W*scale)/2;dy=(box.height-H*scale)/2
  fitted=['q',f'{n(scale)} 0 0 {n(scale)} {n(dx)} {n(dy)} cm']+p.ops+io+['Q','Q']
  e.doc.set_page_content(pi,('\n'.join(fitted)).encode('ascii'))
 out=R/'deliverables/AQUARIS SP THIET KE MOI 20261006';out.mkdir(exist_ok=True);target=out/'AQUARIS SP - REVIEW 02.pdf';assert not target.exists()
 assert sha(BASE)==EXPECTED;e.save(str(target));e.close();print('SAVED',target,sha(target));return target
def preview(pages):
 folder=D/'preview';folder.mkdir(exist_ok=True)
 for p in pages:
  parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="white"/>']+p.svg
  for j,im in enumerate(p.images):
   x,y,w,h=im['target'];ref=im['xref'];raw=DOC.extract_image(ref);uri='data:image/'+raw['ext']+';base64,'+base64.b64encode(raw['image']).decode('ascii')
   parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{uri}"/>')
   if ref not in PATCH:continue
   a=PATCH[ref];u0,v0,u1,v1=a['rect'];sx=w/raw['width'];sy=h/raw['height'];cx=x+u0*sx;cy=y+v0*sy;cw=(u1-u0)*sx;ch=(v1-v0)*sy
   if 'source_xref' in a:
    out=DOC.extract_image(a['source_xref']);data=out['image'];ext=out['ext'];pw=out['width']*sx;ph=out['height']*sy
   else:data=Path(a['file']).read_bytes();ext='png';pw=a['head_size'][0]*sx;ph=a['head_size'][1]*sy
   uri='data:image/'+ext+';base64,'+base64.b64encode(data).decode('ascii')
   parts.append(f'<defs><clipPath id="patch{j}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath></defs><image x="{x}" y="{y}" width="{pw}" height="{ph}" preserveAspectRatio="none" clip-path="url(#patch{j})" xlink:href="{uri}"/>')
  parts.append('</svg>');raw=''.join(parts).encode('utf8');(folder/f'page-{p.index:02}.svg').write_bytes(raw)
  with fitz.open(stream=raw,filetype='svg') as f:f[0].get_pixmap(dpi=140).save(str(folder/f'page-{p.index:02}.png'))
if __name__=='__main__':
 pages=make_pages();plan={'base':str(BASE),'base_sha256':EXPECTED,'pages':[{'page':p.index,'texts':p.texts,'images':p.images,'curves':p.curves,'tables':p.tables} for p in pages],'patches':PATCH,'source_data':str(D/'curves/AQUARIS_CONCAVE_197_NO_H_DELTA.json')}
 (D/'layout_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8');print('PREFLIGHT',len(pages),'pages',sum(len(p.curves) for p in pages),'curves')
 if '--preview' in sys.argv:preview(pages)
 if '--save' in sys.argv:save(pages)
