"""Read-only acceptance checks on actual catfix-generated candidate PDFs."""
from pathlib import Path
import sys,json,hashlib,math
import fitz,numpy as np,pikepdf
W=Path(__file__).parent;R=W.parent.parent
read=lambda p:json.loads(Path(p).read_text(encoding='utf8'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
brand=sys.argv[1].upper();path=Path(sys.argv[2]);plan=read(W/'perotac_writer'/f'{brand}-plan.json');data=read(W/'audit/perotac_dataset.json');rows={r['model']:r for r in data['records']}
rows['6SP60-20']['H'][-2:]=[103,72] # Explicit original task133, actual accepted canonical table.
def bez(a,t):
 a=np.asarray(a);return (1-t)**3*a[0]+3*t*(1-t)**2*a[1]+3*t*t*(1-t)*a[2]+t**3*a[3]
def ev(segs,x):
 for a in segs:
  if a[0][0]-1e-6<=x<=a[3][0]+1e-6:
   lo=0.;hi=1.
   for _ in range(55):
    t=(lo+hi)/2
    if bez(a,t)[0]<x:lo=t
    else:hi=t
   return bez(a,(lo+hi)/2)[1]
 raise ValueError(x)
doc=fitz.open(path);assert len(doc)==len(plan['pages'])
numeric=[];actual_counts=[];content_errors=[];phase_errors=[];curve_checks=[]
render=W/'perotac_writer'/f'{brand}-render';render.mkdir(exist_ok=True)
for i,(page,p) in enumerate(zip(doc,plan['pages'])):
 assert abs(page.rect.width-831.5599975585938)<.001 and abs(page.rect.height-595)<.001
 drawings=page.get_drawings();candidate=[]
 for d in drawings:
  if d.get('width') is not None and abs(d['width']-.75)<1e-5 and d['items'] and all(z[0]=='c' for z in d['items']):
   candidate.append(d)
 assert len(candidate)==len(p['curves']),(i+1,len(candidate),len(p['curves']))
 for d,c in zip(candidate,p['curves']):
  assert not d.get('dashes') or d['dashes'].replace(' ','')=='[]0'
  actual=[[[pt.x,595-pt.y] for pt in item[1:]] for item in d['items']]
  assert np.array(actual).shape==np.array(c['segments_page']).shape
  delta=float(np.max(abs(np.array(actual)-np.array(c['segments_page']))));assert delta<.0002,(i+1,c['model'],delta)
  assert max(abs(float(a)-b) for a,b in zip(d['color'],c['color']))<1e-6
  r=rows[c['model']];first=actual[0][0];last=actual[-1][-1]
  # Locked physical endpoints define affine conversion for exact parsed paths.
  sx=(last[0]-first[0])/(r['Q'][-1]-r['Q'][0]);sy=(last[1]-first[1])/(r['H'][-1]-r['H'][0])
  for q,h in zip(r['Q'],r['H']):
   x=first[0]+(q-r['Q'][0])*sx;y=ev(actual,x);hc=float(r['H'][0]+(y-first[1])/sy);err=float(abs(hc-h));pct=float(err/max(abs(h),1e-12)*100)
   numeric.append({'page':i+1,'model':r['model'],'Q':q,'H_table':h,'H_curve_actual_pdf':hc,'error_m':err,'error_percent':pct,'within_5percent':pct<=5.00001,'within_original_tolerance':err<=max(1,.02*h)+1e-5})
  curve_checks.append({'model':r['model'],'actual_path_max_control_error_pt':delta})
 actual_counts.append(len(candidate));textpage=page.get_textpage();full=textpage.extractText()
 chars=[c for b in textpage.extractRAWDICT()['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans'] for c in s['chars']]
 charboxes=np.array([c['bbox'] for c in chars])
 for bad in ['60 Hz','60Hz','60 HZ','1/min','4SP2-','4SPM2-',' models','Top chock','Bottom support']:
  if bad in full:content_errors.append({'page':i+1,'forbidden':bad})
 for rec in p['texts']:
  # Every horizontal string must survive actual PDF extraction at the planned baseline.
  if rec['matrix']!=[1,0,0,1]:continue
  xx=rec['x'];yy=rec['baseline_top'];ww=rec['width'];sz=rec['size']
  mask=(charboxes[:,0]>=xx-.5)&(charboxes[:,1]>=yy-sz*1.25)&(charboxes[:,2]<=xx+ww+.5)&(charboxes[:,3]<=yy+sz*.3)
  txt=''.join(chars[j]['c'] for j in np.flatnonzero(mask)).strip()
  if rec['text'] not in txt:content_errors.append({'page':i+1,'text_not_read_back':rec['text'],'actual':txt,'bbox':[xx,yy,ww,sz]})
 for tab in p['tables']:
  if tab['kind']=='performance' and tab['family'].startswith('6'):
   box=fitz.Rect(tab['bbox']);text=textpage.extractTextbox(box)
   if '220–240 V' in text or '220-240 V' in text or '1~' in text or 'SPM' in text:phase_errors.append({'page':i+1,'family':tab['family']})
 page.get_pixmap(dpi=170,alpha=False).save(str(render/f'page-{i+1:02d}.png'))
doc.close()
with pikepdf.open(path) as d,pikepdf.open(data['current']) as old:
 meta=lambda z:bytes(z.Root.Metadata.read_bytes()) if '/Metadata' in z.Root else None
 metaheld=meta(d)==meta(old);infoheld=str(d.docinfo)==str(old.docinfo)
 fontfiles=[]
 for o in d.objects:
  if isinstance(o,pikepdf.Stream) and '/Length1' in o:fontfiles.append(hashlib.sha256(o.read_bytes()).hexdigest())
summary={'candidate':str(path),'sha256':sha(path),'brand':brand,'pages':len(plan['pages']),'curves':sum(actual_counts),'H_points':len(numeric),'max_error_percent':max(x['error_percent'] for x in numeric),'failed_H_points':[x for x in numeric if not x['within_5percent'] or not x['within_original_tolerance']],'content_errors':content_errors,'phase_errors':phase_errors,'metadata_held':metaheld,'docinfo_held':infoheld,'canonical_held':sha(data['current'])==data['current_sha256'],'original_held':sha(data['source'])==data['source_sha256'],'status':'READ_ONLY_NUMERIC_QA_NOT_VISUAL_ACCEPTANCE','visual_review':'PENDING','paper_print':'NOT_RUN','points':numeric,'actual_curve_paths':curve_checks}
(W/'perotac_writer'/f'{brand}-qa.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['points','actual_curve_paths','content_errors']},ensure_ascii=False));print('content_errors',len(content_errors))
