"""ROOT writer: use reviewed JSON plans, retain accepted13page documents, save exclusively with catfix."""
from pathlib import Path
import sys,json,hashlib,subprocess,importlib.util
import fitz,pikepdf
from PIL import Image
R=Path(__file__).parent;ROOT=R.parents[1]
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 version=sys.argv[1] if len(sys.argv)>1 else '01'
 lock=load(R/'lock.json')
 gate=subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'tools/catalogue.py'),'check','--actor',lock['actor'],'--session',lock['session'],'--token',lock['token']],capture_output=True,text=True,encoding='utf8');assert gate.returncode==0,gate.stdout
 sp=importlib.util.spec_from_file_location('design',R/'design_preview.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 sys.path.insert(0,str(ROOT/'vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT'));from catfix.vector import Editor
 frozen=pikepdf.open(m.BASE);rd=fitz.open(m.BASE)
 accept=load(ROOT/'work/sp_three_brands/perotac_redpump_accepted.json')
 for brand in ['PEROTAC','REDPUMP']:
  plan=load(R/f'design/{brand}-design-plan.json');assert plan['curve_status'].startswith('NEW_CURVES'),plan['curve_status']
  base=Path(accept['brands'][brand]['canonical']);assert sha(base)==plan['accepted_baseline_sha256']
  for pp in plan['pages']:
   for t in pp['texts']:m.FONTS[t['font']]['used'].update(ord(c) for c in t['text'])
  e=Editor(str(base));pdf=e.doc.pdf;assert len(pdf.pages)==13;fonts=m.embed_fonts(pdf)
  for i,pp in enumerate(plan['pages']):
   pg=e.doc._pages[i];res=pikepdf.Dictionary(pg.Resources);ff=pikepdf.Dictionary(res.get('/Font',{}));xo=pikepdf.Dictionary(res.get('/XObject',{}));io=[]
   for key,obj in fonts.items():ff[key]=obj
   for im in pp['images']:
    x,y,w,h=im['target'];key='/SP'+im['name']
    if 'file' in im:
     path=Path(im['file']);img=Image.open(path);assert img.format=='JPEG' and img.mode=='RGB'
     obj=pdf.make_stream(path.read_bytes());obj.Type=pikepdf.Name.XObject;obj.Subtype=pikepdf.Name.Image;obj.Width=img.width;obj.Height=img.height;obj.ColorSpace=pikepdf.Name.DeviceRGB;obj.BitsPerComponent=8;obj.Filter=pikepdf.Name.DCTDecode;xo[key]=obj
     io.append(f'q {m.n(w)} 0 0 {m.n(h)} {m.n(x)} {m.n(m.HEIGHT-y-h)} cm {key} Do Q')
    else:
     infos=rd[im['source_page']-1].get_image_info(xrefs=True);info=next(z for z in infos if z['xref']==184) if im['source_page']==11 else max(infos,key=lambda z:z['width']*z['height'])
     xo[key]=pdf.copy_foreign(frozen.get_object((info['xref'],0)))
     x0,y0,x1,y1=im['source_crop_pt'];bx0,by0,bx1,by1=info['bbox'];sc=w/(x1-x0);assert abs(sc-h/(y1-y0))<1e-5
     io.append(f'q {m.n(x)} {m.n(m.HEIGHT-y-h)} {m.n(w)} {m.n(h)} re W n {m.n((bx1-bx0)*sc)} 0 0 {m.n((by1-by0)*sc)} {m.n(x+(bx0-x0)*sc)} {m.n(m.HEIGHT-y-(by1-y0)*sc)} cm {key} Do Q')
   res.Font=ff;res.XObject=xo;pg.Resources=res;e.doc.set_page_content(i,('\n'.join(pp['pdf_content_ops_prepared_not_written']+io)).encode('ascii'))
  out=ROOT/'deliverables/SP BA HANG THIET KE RIENG 20261006';out.mkdir(exist_ok=True);target=out/f'{brand} SP - REVIEW {version}.pdf';assert not target.exists();assert sha(base)==plan['accepted_baseline_sha256'];e.save(str(target));e.close();print(brand,str(target),sha(target))
 rd.close();frozen.close()
if __name__=='__main__':main()
