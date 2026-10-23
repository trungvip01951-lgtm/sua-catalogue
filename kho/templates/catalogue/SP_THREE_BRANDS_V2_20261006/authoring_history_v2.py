"""Reusable SP authoring plan. PDF writes exclusively through catfix.Editor.

Preflight does not save a PDF. Unanswered data/page decisions block --save.
"""
from pathlib import Path
import sys,json,math,hashlib,subprocess,html,base64
import numpy as np
import fitz,pikepdf
from fontTools.ttLib import TTFont

ROOT=Path(r'D:\ChatGPT\Sửa catalogue'); W=ROOT/'work/sp_three_brands'
OUT=W/'perotac_writer';OUT.mkdir(exist_ok=True)
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sys.path.insert(0,str(ROOT/'vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT'))
from catfix.vector import Editor
DATA=read(W/'audit/perotac_dataset.json'); RR=DATA['records']
BY={r['model']:r for r in RR}
BY['6SP30-17']['segments']=read(W/'geometry/6sp30_17_pdf_tolerance_fix.json')['segments_after']
task133=read(W/'geometry/6sp60_20_restore_task133.json')
BY['6SP60-20']['H']=task133['H_after'];BY['6SP60-20']['segments']=task133['segments_after']
for r in read(W/'audit/sp30_six_new_table_curves.json')['rows']:BY[r['model']]['segments']=r['segments']
DEC=read(W/'user_decisions.json')
assert DEC.get('single_phase_requires_three_phase_model') is True
PHASE_ADDED=[]
for r in RR:
 e=r['display_electrical_variants']
 if e['single_phase_model'] and not e['three_phase_model']:
  e['three_phase_model']=e['single_phase_model'].replace('SPM','SP')
  PHASE_ADDED.append(e['three_phase_model'])
if DEC.get('4SP14_two_H_cells_approved') is True or '--conditional-plan' in sys.argv:
 proposal=read(W/'geometry/4sp14_4_conditional_refit.json')
 BY['4SP14-4']['H']=proposal['H_proposed'];BY['4SP14-4']['segments']=proposal['segments_proposed']
BASE=Path(DATA['current']);assert sha(BASE)==DATA['current_sha256']
assert sha(DATA['source'])==DATA['source_sha256']
INTRO=read(W/'assets_audit/perotac_intro_content.json')['intro']
D4=read(W/'assets_audit/perotac_dimensions_4inch.json')['rows']
D4=[r for r in D4 if r['family'] not in DEC.get('excluded_SP_families_all_brands',[])]
for r in D4:
 if r['single_phase_model'] and not r['three_phase_model']:
  r['three_phase_model']=r['single_phase_model'].replace('SPM','SP')
D6=read(W/'assets_audit/perotac_dimensions_6inch.json')['rows']
D8=read(W/'assets_audit/perotac_dimensions_8_10inch.json')['rows']
ETA={x['family']:x for x in read(W/'assets_audit/eta/eta_traces.json')['records']}
PAN={p['family']:p for p in read(W/'geometry/perotac_labels.json')['panels']}
V3=read(ROOT/'work/sp6_fullmodel/label_plan.json')
for fam,left,qm,hm in [('6SP36',24,60,450),('6SP46',428,72,350)]:
 PAN[fam]={'family':fam,'left':left,'plot':[left+29,94,326,190],'Q_axis_max':qm,'H_axis_max':hm,'labels':[x for x in V3['labels'] if x['family']==fam],'unplaced':[]}
WIDTH=831.5599975585938;HEIGHT=595.
NAVY=(.075,.20,.30);INK=(.12,.22,.28);TEAL=(.15,.37,.46);PALE=(.94,.97,.98);GRID=(.84,.88,.90);BORDER=(.32,.48,.56)
FONTS={}
for name,path in [('Body','C:/Windows/Fonts/arial.ttf'),('Bold','C:/Windows/Fonts/arialbd.ttf')]:
 tt=TTFont(path);assert not(tt['OS/2'].fsType&2)
 FONTS[name]={'tt':tt,'path':Path(path),'cmap':tt.getBestCmap(),'up':tt['head'].unitsPerEm,'used':set()}
def n(v):return f'{v:.8f}'.rstrip('0').rstrip('.') if abs(v)>1e-9 else '0'
def rgb(c,stroke=False):return ' '.join(n(x) for x in c)+(' RG' if stroke else ' rg')
def svgcolor(c):return 'rgb('+','.join(str(round(255*x)) for x in c)+')'
def fmt(v):
 if v is None:return '–'
 if isinstance(v,str):return v
 return f'{v:g}'
def width(s,size,font='Body'):
 f=FONTS[font];return sum(f['tt']['hmtx'][f['cmap'][ord(c)]][0] for c in s)*size/f['up']
class Page:
 def __init__(self,source_page,brand):
  self.source_page=source_page;self.brand=brand;self.ops=['q','[] 0 d'];self.svg=[];self.texts=[];self.curves=[];self.images=[];self.tables=[]
 def rect(self,x,y,w,h,color):
  self.ops.append(f'{rgb(color)} {n(x)} {n(HEIGHT-y-h)} {n(w)} {n(h)} re f')
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{svgcolor(color)}"/>')
 def line(self,x,y,x2,y2,color=GRID,lw=.3):
  self.ops.append(f'{rgb(color,True)} {n(lw)} w 0 J {n(x)} {n(HEIGHT-y)} m {n(x2)} {n(HEIGHT-y2)} l S')
  self.svg.append(f'<path d="M{x},{y} L{x2},{y2}" fill="none" stroke="{svgcolor(color)}" stroke-width="{lw}"/>')
 def text(self,s,x,y,size=7,font='Body',color=INK,align='left',matrix=(1,0,0,1)):
  s=str(s);ww=width(s,size,font)
  if align=='center':x-=ww/2
  elif align=='right':x-=ww
  assert 0<=x<WIDTH and 0<y<HEIGHT,(s,x,y)
  if matrix==(1,0,0,1):assert x+ww<=WIDTH+.01,(s,x,ww)
  FONTS[font]['used'].update(ord(c) for c in s)
  self.ops.append(f'BT /SP{font} {n(size)} Tf {rgb(color)} '+ ' '.join(n(z) for z in [*matrix,x,HEIGHT-y])+f' Tm <{s.encode("utf-16-be").hex()}> Tj ET')
  self.texts.append({'text':s,'x':x,'baseline_top':y,'size':size,'font':font,'matrix':matrix,'width':ww})
  a,b,c,d=matrix;self.svg.append(f'<text transform="matrix({a} {-b} {-c} {d} {x} {y})" font-family="Arial" font-size="{size}" font-weight="'+('bold' if font=='Bold' else 'normal')+f'" fill="{svgcolor(color)}">{html.escape(s)}</text>')
 def path(self,segs,X,Y,lw=.75,model=None):
  ops=[rgb(TEAL,True),f'{n(lw)} w','1 J 1 j','[] 0 d'];actual=[]
  for j,seg in enumerate(segs):
   pts=[(X(q),HEIGHT-Y(h)) for q,h in seg];actual.append(pts)
   if j==0:ops.append(f'{n(pts[0][0])} {n(pts[0][1])} m')
   ops.append(' '.join(n(v) for p in pts[1:] for v in p)+' c')
  ops.append('S');self.ops.append('\n'.join(ops))
  s=''
  for j,seg in enumerate(segs):
   pts=[(X(q),Y(h)) for q,h in seg]
   if j==0:s+=f'M{pts[0][0]},{pts[0][1]} '
   s+='C'+' '.join(f'{x},{y}' for x,y in pts[1:])+' '
  self.svg.append(f'<path d="{s}" fill="none" stroke="{svgcolor(TEAL)}" stroke-width="{lw}" stroke-linecap="round" stroke-linejoin="round"/>')
  if model:self.curves.append({'model':model,'segments_page':actual,'width':lw,'color':TEAL})
 def header(self,title,index,total):
  # Brand variation is restricted to the header and accent; technical geometry is shared.
  accent=TEAL if self.brand=='PEROTAC' else (.55,.12,.15)
  if self.brand=='PEROTAC':
   self.images.append({'name':'BrandLogo','file':str(ROOT/'templates/catalogue/SP6_LOGO_TABLE_V2/assets/PEROTAC ORIGINAL.jpg'),'target':[24,7,88,30.09]})
   self.text(title,WIDTH-24,19,10,'Bold',NAVY,'right')
   self.text('Stainless steel submersible pumps  |  50 Hz  |  n ≈ 2850 /min',WIDTH-24,34,7,'Body',INK,'right')
  else:
   self.images.append({'name':'BrandLogo','file':str(W/'assets_audit/Redpump-WC-logo-original.jpeg'),'target':[WIDTH-104,5,80,35.53]})
   self.text(title,24,19,10,'Bold',NAVY)
   self.text('Stainless steel submersible pumps  |  50 Hz  |  n ≈ 2850 /min',24,34,7)
  self.line(24,45,WIDTH-24,45,accent,1.2)
  self.line(24,581,WIDTH-24,581,GRID,.45)
  self.text(self.brand+'  /  SP SERIES',24,591,6,'Bold',NAVY)
  self.text(f'{index:02d} / {total:02d}',WIDTH-24,591,6,'Body',INK,'right')

def grid(p,x,y,widths,heights):
 xs=[x];ys=[y]
 for a in widths:xs.append(xs[-1]+a)
 for a in heights:ys.append(ys[-1]+a)
 for xx in xs:p.line(xx,y,xx,ys[-1],BORDER,.6)
 for yy in ys:p.line(x,yy,xs[-1],yy,BORDER,.6)
 return xs,ys
def performance_table(p,fam,left,top=374,rowh=7.7):
 rr=[r for r in RR if r['family']==fam];two=fam.startswith('4');fixed=[47,47,20,20,31] if two else [75,25,25,31]
 cw=380;qw=(cw-sum(fixed))/len(rr[0]['Q']);ww=fixed+[qw]*len(rr[0]['Q']);xs=[left]
 for w in ww:xs.append(xs[-1]+w)
 hhead=33;bottom=top+hhead+len(rr)*rowh;assert bottom<579,(fam,bottom)
 p.text('PERFORMANCE DATA',left,top-7,8,'Bold',NAVY)
 p.rect(left,top,cw,hhead,(.87,.93,.96))
 for i in range(len(rr)):
  if i%2==0:p.rect(left,top+hhead+i*rowh,cw,rowh,PALE)
 modelend=2 if two else 1;powerend=modelend+2;qi=powerend
 p.text('MODEL',(xs[0]+xs[modelend])/2,top+8,6.5,'Bold',align='center')
 pc=(xs[modelend]+xs[powerend])/2;p.text('P',pc-1.4,top+8,6.5,'Bold',align='center');p.text('2',pc+1.6,top+10,4.5,'Bold')
 for i,s in enumerate(['1~','3~'] if two else ['3~']):
  cx=(xs[i]+xs[i+1])/2;p.text(s,cx,top+19,6,'Bold',align='center');p.text('220–240 V' if two and i==0 else '380–415 V',cx,top+29,5.5,align='center')
 for j,s in enumerate(['kW','HP'],modelend):p.text(s,(xs[j]+xs[j+1])/2,top+23,6,'Bold',align='center')
 p.text('Q',xs[qi]+5.5,top+23,6.5,'Bold',align='center');p.text('m³/h',(xs[qi]+11+xs[qi+1])/2,top+19,5.5,'Bold',align='center');p.text('l/min',(xs[qi]+11+xs[qi+1])/2,top+29,5.3,align='center')
 p.text('H (m)',(xs[qi]+xs[qi+1])/2,top+hhead+len(rr)*rowh/2+2.5,6.8,'Bold',align='center')
 for j,q in enumerate(rr[0]['Q'],qi+1):
  p.text(fmt(q),(xs[j]+xs[j+1])/2,top+19,6,'Bold',align='center');p.text(str(round(q*1000/60)),(xs[j]+xs[j+1])/2,top+29,5.4,align='center')
 cells=[]
 for i,r in enumerate(rr):
  e=r['display_electrical_variants'];vals=([e['single_phase_model'] or '–',e['three_phase_model'] or '–'] if two else [e['three_phase_model']])+[fmt(r['kW']),fmt(r['HP'])]
  for j,s in enumerate(vals):p.text(s,(xs[j]+xs[j+1])/2,top+hhead+i*rowh+rowh*.74,5.7 if j<modelend else 6,align='center')
  for j,h in enumerate(r['H'],qi+1):p.text(fmt(h),(xs[j]+xs[j+1])/2,top+hhead+i*rowh+rowh*.74,6,align='center')
  cells.append({'model':r['model'],'values':vals+[fmt(h) for h in r['H']]})
 # Draw all grid lines once, after every background, including distinct first two header rows.
 for yy in [top,top+11,top+33,bottom]:p.line(left,yy,left+cw,yy,BORDER,.6)
 for i in range(1,len(rr)):
  yy=top+33+i*rowh;p.line(left,yy,xs[qi],yy,BORDER,.6);p.line(xs[qi+1],yy,xs[-1],yy,BORDER,.6)
 for j,xx in enumerate(xs):p.line(xx,top if j in [0,modelend,powerend,len(xs)-1] else top+11,xx,bottom,BORDER,.6)
 p.line(xs[qi]+11,top+11,xs[qi]+11,top+33,BORDER,.6);p.line(xs[qi]+11,top+22,xs[-1],top+22,BORDER,.6)
 p.tables.append({'kind':'performance','family':fam,'cells':cells,'bbox':[left,top,left+cw,bottom]})

def tick_step(v):
 ideal=v/5;base=10**math.floor(math.log10(ideal))
 return next(base*s for s in [1,2,2.5,5,10] if base*s>=ideal-1e-8)
def ticks(v):
 step=tick_step(v);a=np.arange(0,v+step*.001,step).tolist()
 if abs(a[-1]-v)>1e-8:a.append(v)
 return a
def cut_spans(a,b,cuts):
 cursor=a;out=[]
 for lo,hi in sorted(cuts):
  lo=max(a,lo);hi=min(b,hi)
  if hi<=lo:continue
  if lo>cursor:out.append((cursor,lo))
  cursor=max(cursor,hi)
 if cursor<b:out.append((cursor,b))
 return out
def panel(p,fam):
 a=PAN[fam];left=a['left'];px,py,pw,ph=a['plot'];qm=a['Q_axis_max'];hm=a['H_axis_max'];large=fam=='6SP30'
 assert not a.get('unplaced'),('UNPLACED',fam)
 p.text(fam,left,62 if large else 65,16,'Bold',NAVY)
 X=lambda q:px+q/qm*pw;Y=lambda h:py+ph-h/hm*ph
 boxes=[]
 for l in a['labels']:
  z=np.array(l['ink_quad_page']);boxes.append([z[:,0].min()-.35,z[:,1].min()-.35,z[:,0].max()+.35,z[:,1].max()+.35])
 for h in ticks(hm):
  yy=Y(h)
  for x1,x2 in cut_spans(px,px+pw,[(b[0],b[2]) for b in boxes if b[1]<=yy<=b[3]]):p.line(x1,yy,x2,yy)
  p.text(fmt(h),px-5,yy+2,5.8,align='right');p.text(str(round(h*3.280839895)),px+pw+5,yy+2,5.2)
 for q in ticks(qm):
  xx=X(q)
  for y1,y2 in cut_spans(py,py+ph,[(b[1],b[3]) for b in boxes if b[0]<=xx<=b[2]]):p.line(xx,y1,xx,y2)
  p.text(str(round(q*4.40286754)),xx,70 if large else 79,5.3,align='center');p.text(str(round(q*3.66615483)),xx,79 if large else 88,5.3,align='center')
 p.text('US gpm',left,70 if large else 79,5.2);p.text('Imp gpm',left,79 if large else 88,5.2)
 p.text('ft',px+pw+14,py-6,5.3,align='center')
 title='Total head H (m)';p.text(title,left-4,py+ph/2+width(title,6.4,'Bold')/2,6.4,'Bold',matrix=(0,1,-1,0))
 p.line(px,py,px,py+ph,INK,.5);p.line(px,py+ph,px+pw,py+ph,INK,.5)
 for r in RR:
  if r['family']==fam:p.path(r['segments'],X,Y,model=r['model'])
 for lab in a['labels']:p.text(lab['text'],lab['x'],lab['baseline_top'],lab['size'],'Bold',TEAL,matrix=tuple(lab['pdf_text_matrix_abcd']))
 if fam=='6SP46':p.line(452,265,457,265,TEAL,.45)
 for lab in a['labels']:
  if 'leader' in lab:p.line(*lab['leader'][0],*lab['leader'][1],TEAL,.45)
 qy=341 if large else py+ph+12
 for q in ticks(qm):p.text(fmt(q),X(q),qy,6,'Bold',align='center');p.text(str(round(q*1000/60)),X(q),qy+10,5.3,align='center')
 p.text('m³/h',px-5,qy,5.6,'Bold',align='right');p.text('l/min',px-5,qy+10,5.3,align='right')
 ey=359 if large else 319;eh=27 if large else 29;eta=ETA[fam];em=eta['source_frame_eta_max_inferred_from_visible_tick_spacing']
 p.text('η (%)',left,ey+2,5.6,'Bold')
 for v in [0,40,80] if em==90 else [0,20,40,60]:
  yy=ey+eh-v/em*eh;p.line(px,yy,px+pw,yy);p.text(str(v),px-5,yy+2,5.1,align='right')
 for q in ticks(qm):p.line(X(q),ey,X(q),ey+eh)
 # Keep the trace unchanged; display it only inside the shared Q-axis domain.
 clipid='eta-'+fam;p.svg.append(f'<defs><clipPath id="{clipid}"><rect x="{px}" y="{ey}" width="{pw}" height="{eh}"/></clipPath></defs><g clip-path="url(#{clipid})">')
 p.ops.append(f'q {n(px)} {n(HEIGHT-ey-eh)} {n(pw)} {n(eh)} re W n')
 p.path(eta['curve_physical_segments_Q_m3h_eta_percent'],X,lambda h:ey+eh-h/em*eh,.65)
 p.ops.append('Q');p.svg.append('</g>')
 p.line(px,ey,px,ey+eh,INK,.45);p.line(px,ey+eh,px+pw,ey+eh,INK,.45)
 performance_table(p,fam,left,410 if large else 374,7.1 if large else 7.7)

def mini_table(p,x,y,ww,headers,rows,rh=10,size=6.1):
 widths=ww;cw=sum(ww);p.rect(x,y,cw,20,(.87,.93,.96));xs=[x]
 for a in widths:xs.append(xs[-1]+a)
 for j,s in enumerate(headers):p.text(s,(xs[j]+xs[j+1])/2,y+13,5.6,'Bold',align='center')
 for i,row in enumerate(rows):
  if i%2==0:p.rect(x,y+20+i*rh,cw,rh,PALE)
  for j,v in enumerate(row):
   s=fmt(v);assert width(s,size)<widths[j]-2,(s,widths[j])
   p.text(s,(xs[j]+xs[j+1])/2,y+20+i*rh+rh*.74,size,align='center')
 grid(p,x,y,widths,[20]+[rh]*len(rows))
 return y+20+len(rows)*rh
def intro(p,item):
 fam=item['family'];body=item['body_inches'];x=24
 p.text(fam,x,71,23,'Bold',NAVY);p.text(f'{body}-inch stainless steel well pumps',x,86,8)
 y=106
 def section(title,lines):
  nonlocal y
  p.text(title,x,y,8,'Bold',TEAL);y+=12
  for s in lines:p.text(s,x,y,6.9);y+=10
  y+=10
 section('Applications',item['source_applications'])
 c=item['source_operating_conditions'];section('Operating conditions',[f'Maximum fluid temperature: {c["max_fluid_temperature_C"]} °C',f'Maximum sand content: {c["max_sand_content_percent"]}%',f'Minimum well diameter: {body} in'])
 motor=[s.replace('①','1.').replace('②','2.') for s in item['source_motor_and_pump'] if not(body==6 and 'Single-phase' in s)]
 section('Motor and pump',motor)
 section('Options on request',[s for s in item['source_options'] if '60 Hz' not in s and not(body==6 and 'Single phase' in s)])
 section('Warranty: 1 year',['According to our general sales conditions'])
 mats=[[a,b.replace('① ','').replace(' ② ',' / ')] for a,b in item['source_materials'] if a not in ['Top chock','Bottom support']]
 # The source duplicates Shaft with two different material entries; preserve both.
 my=max(y,423);mini_table(p,24,my,[100,173],['COMPONENT','MATERIAL'],mats,10,6)
 photo_box={1:[307,89,354,438],4:[229,103,339,435],9:[248,91,293,441],11:[241,88,289,439]}[item['source_page']]
 targetx=302 if body==6 else 335
 p.images.append({'name':'PumpPhoto','source_page':item['source_page'],'source_crop_pt':photo_box,'target':[targetx,96,photo_box[2]-photo_box[0],photo_box[3]-photo_box[1]]})
 # Model-code explanation reuses source meanings in clear English.
 code=item['source_model_code_example'].replace('(M) ','') if body==6 else item['source_model_code_example']
 p.text(code,311,472,10,'Bold',TEAL)
 lines=['Well diameter / SP series','Rated flow / Number of impellers']
 if body==4:lines+=['M: single phase','No M: three phase']
 if body==10:lines+=['A: special impeller']
 for i,s in enumerate(lines):p.text(s,311,487+i*11,6)

def dimension_drawing(p,x,y,h,body_mm,motor_mm=None):
 # P/M/T measurement schematic; numeric dimensions are in the adjacent source tables.
 pw=22;split=y+h*.60
 p.line(x,y,x+pw,y,INK,.6);p.line(x,y,x,y+h,INK,.6);p.line(x+pw,y,x+pw,y+h,INK,.6);p.line(x,y+h,x+pw,y+h,INK,.6);p.line(x,split,x+pw,split,INK,.6)
 for yy in np.arange(y+14,split-5,12):p.line(x+4,yy,x+pw-4,yy,GRID,.4)
 for xx,ya,yb,label in [(x-10,y,split,'P'),(x-10,split,y+h,'M'),(x+pw+12,y,y+h,'T')]:
  p.line(xx,ya,xx,yb,INK,.5);p.line(xx-3,ya,xx+3,ya,INK,.5);p.line(xx-3,yb,xx+3,yb,INK,.5);p.text(label,xx-5 if xx<x else xx+4,(ya+yb)/2+2,6,'Bold')
 p.text('DN',x+pw/2,y-8,6,'Bold',align='center')
 if body_mm is not None:p.text('Ø '+fmt(body_mm)+' mm',x+pw/2,y+h+14,5.6,align='center')
 if motor_mm:p.text('Motor Ø '+fmt(motor_mm)+' mm',x+pw/2,y+h+25,5.3,align='center')

def dims4(p):
 p.text('4SP  |  Dimensions and weights',112,59,9,'Bold',NAVY)
 x=112;y=66;w=WIDTH-24-x;fixed=[56,56,34]+[(w-146)/10]*10;heads=['1~ MODEL','3~ MODEL','DN (in)','P','M 1~','M 3~','T 1~','T 3~','Pump','Motor 1~','Motor 3~','Total 1~','Total 3~']
 rows=[]
 for r in D4:
  valid=r['hydraulic_row_key'] not in BY or BY[r['hydraulic_row_key']]['kW']<=3
  vals=[r['single_phase_model'] if valid else None,r['three_phase_model'],fmt(r['DN_inches_user']) if r['DN_inches_user'] else r['DN_inches_source'],r['P_mm'],r['M_single_mm'] if valid else None,r['M_three_mm'],r['T_single_mm'] if valid else None,r['T_three_mm'],r['pump_weight_kg'],r['motor_single_weight_kg'] if valid else None,r['motor_three_weight_kg'],r['total_single_weight_kg'] if valid else None,r['total_three_weight_kg']]
  rows.append(vals)
 mini_table(p,x,y,fixed,heads,rows,8.0,6.6)
 p.text('P / M / T: mm   |   Weights: kg   |   1~ 220–240 V   |   3~ 380–415 V',112,579,6)
 dimension_drawing(p,53,145,310,100,95)
 p.tables.append({'kind':'dimensions4','rows':rows})
def dimension_families(p,families,left=24,top=75,draw=True):
 y=top;allrows=D6+D8
 for fam in families:
  rr=[r for r in allrows if r['model'].split('-')[0]==fam]
  outlet=rr[0].get('DN_inches_user',rr[0]['DN_inches_source'])
  p.text(f'{fam}  |  Outlet {fmt(outlet)} in',left,y-9,10,'Bold',NAVY)
  rows=[[r['model'],r['P_mm'],r['M_mm'],r['T_mm'],r['pump_weight_kg'],r['motor_weight_kg'],r['total_weight_kg']] for r in rr]
  # Include the varying motor diameter for 8/10-inch families.
  extra=not fam.startswith('6')
  if extra:
   rows=[row[:4]+[r['motor_diameter_mm']]+row[4:] for row,r in zip(rows,rr)];ww=[69,42,42,42,43,47,47,48];heads=['MODEL','P','M','T','Motor Ø','Pump','Motor','Total']
  else:ww=[78,48,48,48,52,53,53];heads=['MODEL','P','M','T','Pump','Motor','Total']
  y=mini_table(p,left,y,ww,heads,rows,8.1,6.1)+29
  p.tables.append({'kind':'dimensions','family':fam,'rows':rows})
 assert y<600,(families,y)
 p.text('Dimensions: mm   |   Weights: kg   |   3~ 380–415 V',left,min(y-12,575),6)
 if draw and y<515:
  body_mm=145 if families[0].startswith('6') else 200 if families[0].startswith('8') else 222
  dimension_drawing(p,left+175,y+5,min(130,550-y),body_mm,145 if families[0].startswith('6') else None)

def make_pages(brand):
 # Page split is a conditional design only until directly approved by the user.
 split=DEC.get('split_perotac_page2') is True or '--conditional-plan' in sys.argv
 layout=[(1,['intro4','4SP3']),(2,['4SP5','4SP8'])]
 if split:layout.append((2,['4SP10','4SP14']))
 else:layout[1][1]+=['4SP10','4SP14']
 layout += [(3,['dims4']),(4,['intro6','6SP10']),(5,['6SP18','6SP30']),(6,['6SP36','6SP46']),(7,['6SP60','dims6a']),(8,['dims6b','dims6c']),(9,['intro8','8SP77']),(10,['8SP95','dims8']),(11,['intro10','10SP135']),(12,['10SP160','dims10'])]
 pages=[]
 for j,(src,items) in enumerate(layout):
  p=Page(src,brand);p.header('SP SERIES  /  '+('DIMENSIONS' if all('dims' in a for a in items) else 'PERFORMANCE & TECHNICAL DATA'),j+1,len(layout))
  for item in items:
   if item.startswith('intro'):intro(p,next(t for t in INTRO if str(t['body_inches'])==item[5:]))
   elif item=='dims4':dims4(p)
   elif item=='dims6a':dimension_families(p,['6SP10','6SP18'],428,70,False)
   elif item=='dims6b':dimension_families(p,['6SP30','6SP36'],24,70)
   elif item=='dims6c':dimension_families(p,['6SP46','6SP60'],428,70)
   elif item=='dims8':dimension_families(p,['8SP77','8SP95'],428,70)
   elif item=='dims10':dimension_families(p,['10SP135','10SP160'],428,70)
   else:panel(p,item)
  p.ops.append('Q');pages.append(p)
 return pages

def embed_fonts(pdf):
 result=pikepdf.Dictionary()
 for name,f in FONTS.items():
  tt=f['tt'];up=f['up'];cmap=f['cmap'];raw=f['path'].read_bytes();ff=pdf.make_stream(raw);ff.Length1=len(raw);base='ArialMT' if name=='Body' else 'Arial-BoldMT'
  desc=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.FontDescriptor,FontName=pikepdf.Name('/'+base),Flags=32,FontBBox=pikepdf.Array([getattr(tt['head'],k)*1000/up for k in ['xMin','yMin','xMax','yMax']]),ItalicAngle=0,Ascent=tt['hhea'].ascent*1000/up,Descent=tt['hhea'].descent*1000/up,CapHeight=tt['OS/2'].sCapHeight*1000/up,StemV=80 if name=='Body' else 120,FontFile2=ff))
  gm=bytearray((max(f['used'])+1)*2);ww=pikepdf.Array()
  for code in sorted(f['used']):
   glyph=cmap[code];gm[code*2:code*2+2]=tt.getGlyphID(glyph).to_bytes(2,'big');ww.append(code);ww.append(pikepdf.Array([tt['hmtx'][glyph][0]*1000/up]))
  cid=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font,Subtype=pikepdf.Name.CIDFontType2,BaseFont=pikepdf.Name('/'+base),CIDSystemInfo=pikepdf.Dictionary(Registry='Adobe',Ordering='Identity',Supplement=0),FontDescriptor=desc,DW=1000,W=ww,CIDToGIDMap=pdf.make_stream(bytes(gm))))
  cmapbytes=b'/CIDInit /ProcSet findresource begin 12 dict begin begincmap /CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def /CMapName /SPUnicode def /CMapType 2 def 1 begincodespacerange <0000> <FFFF> endcodespacerange 1 beginbfrange <0000> <FFFF> <0000> endbfrange endcmap CMapName currentdict /CMap defineresource pop end end'
  result['/SP'+name]=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font,Subtype=pikepdf.Name.Type0,BaseFont=pikepdf.Name('/'+base),Encoding=pikepdf.Name('/Identity-H'),DescendantFonts=pikepdf.Array([cid]),ToUnicode=pdf.make_stream(cmapbytes)))
 return result

def preview_pages(brand,pages):
 # Pure SVG previews, no PDF is created or edited before outstanding decisions.
 folder=OUT/(brand+'-conditional-preview');folder.mkdir(exist_ok=True)
 src=fitz.open(BASE)
 for i,p in enumerate(pages):
  svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}"><rect width="100%" height="100%" fill="white"/>']+p.svg
  for im in p.images:
   x,y,w,h=im['target']
   if 'file' in im:
    raw=Path(im['file']).read_bytes();uri='data:image/jpeg;base64,'+base64.b64encode(raw).decode('ascii')
    svg.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{uri}"/>')
   else:
    page=src[im['source_page']-1];pix=page.get_pixmap(dpi=200,clip=fitz.Rect(im['source_crop_pt']),alpha=False);uri='data:image/png;base64,'+base64.b64encode(pix.tobytes('png')).decode('ascii')
    svg.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{uri}"/>')
  svg.append('</svg>');raw=''.join(svg).encode('utf8');(folder/f'page-{i+1:02d}.svg').write_bytes(raw)
  with fitz.open(stream=raw,filetype='svg') as d:d[0].get_pixmap(dpi=180,alpha=False).save(str(folder/f'page-{i+1:02d}.png'))
 src.close()

def save(brand,pages):
 assert DEC.get('split_perotac_page2') is True,'User page-count decision required'
 assert DEC.get('family_4SP14_or15')!='PENDING_USER_REPLY','User naming decision required'
 assert DEC.get('4SP14_two_H_cells_approved') is True,'User H correction required'
 lock=read(OUT/'active_lock.json')
 gate=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/catalogue.py'),'check','--actor',lock['actor'],'--session',lock['session'],'--token',lock['token']],capture_output=True,text=True,encoding='utf8');assert gate.returncode==0,gate.stdout+gate.stderr
 (OUT/f'{brand}-prewrite-lock.json').write_text(gate.stdout,encoding='utf8')
 E=Editor(str(BASE));pdf=E.doc.pdf;original_pages=list(pdf.pages)
 if len(pages)==13:
  # A distinct new page object avoids sharing an editable content dictionary.
  newpage=pdf.add_blank_page(page_size=(WIDTH,HEIGHT));newpage.Resources=pikepdf.Dictionary(original_pages[1].Resources)
  del pdf.pages[-1];pdf.pages.insert(2,newpage);E.doc._pages=list(pdf.pages)
 fonts=embed_fonts(pdf);rd=fitz.open(BASE)
 for pi,p in enumerate(pages):
  page=E.doc._pages[pi];res=pikepdf.Dictionary(page.Resources);fs=pikepdf.Dictionary(res.get('/Font',{}))
  for name,obj in fonts.items():fs[name]=obj
  res.Font=fs;xo=pikepdf.Dictionary(res.get('/XObject',{}));imgops=[]
  for im in p.images:
   tx,ty,ww,hh=im['target'];key='/SP'+im['name']
   if 'file' in im:
    from PIL import Image
    f=Path(im['file']);ii=Image.open(f);iw,ih=ii.size;obj=pdf.make_stream(f.read_bytes());obj.Type=pikepdf.Name.XObject;obj.Subtype=pikepdf.Name.Image;obj.Width=iw;obj.Height=ih;obj.ColorSpace=pikepdf.Name.DeviceRGB;obj.BitsPerComponent=8;obj.Filter=pikepdf.Name.DCTDecode;xo[key]=obj
    imgops.append(f'q {n(ww)} 0 0 {n(hh)} {n(tx)} {n(HEIGHT-ty-hh)} cm {key} Do Q')
   else:
    sp=rd[im['source_page']-1];infos=sp.get_image_info(xrefs=True)
    info=next(z for z in infos if z['xref']==184) if im['source_page']==11 else max(infos,key=lambda z:z['width']*z['height'])
    obj=pdf.get_object((info['xref'],0));xo[key]=obj
    sx0,sy0,sx1,sy1=im['source_crop_pt'];bx0,by0,bx1,by1=info['bbox'];scale=ww/(sx1-sx0);assert abs(scale-hh/(sy1-sy0))<1e-5
    imgops.append(f'q {n(tx)} {n(HEIGHT-ty-hh)} {n(ww)} {n(hh)} re W n {n((bx1-bx0)*scale)} 0 0 {n((by1-by0)*scale)} {n(tx+(bx0-sx0)*scale)} {n(HEIGHT-ty-(by1-sy0)*scale)} cm {key} Do Q')
  res.XObject=xo;page.Resources=res;E.doc.set_page_content(pi,('\n'.join(p.ops+imgops)).encode('ascii'))
 rd.close();dest=ROOT/'deliverables/SP BA HANG 20261006';dest.mkdir(exist_ok=True);target=dest/f'{brand} SP - REVIEW 02.pdf';assert not target.exists()
 E.save(str(target));E.close();return target

if __name__=='__main__':
 # Optional geometry replacement is produced independently in pure JSON.
 alt=W/'geometry/geometry_alternatives_pass.json'
 if alt.exists():
  obj=read(alt)
  for a in obj['panels']:
   if not a['family'].startswith('4') or DEC.get('split_perotac_page2') is True or '--conditional-plan' in sys.argv:PAN[a['family']]=a
 right=W/'geometry/right_panels_conditional.json'
 if right.exists() and (DEC.get('split_perotac_page2') is True or '--conditional-plan' in sys.argv):
  for a in read(right)['panels']:PAN[a['family']]=a
 if DEC.get('4SP14_two_H_cells_approved') is True or '--conditional-plan' in sys.argv:
  for a in read(W/'geometry/4sp14_refit_geometry.json')['panels']:PAN[a['family']]=a
 ownerfix=W/'geometry/geometry_owner_leaders_v2.json'
 assert ownerfix.exists(),'Need independent preflight for ambiguous 6SP18/30 label ownership'
 for a in read(ownerfix)['panels']:PAN[a['family']]=a
 for a in PAN.values():
  for lab in a['labels']:
   lab['text']=lab['text'].replace('SPM','SP')
 large=PAN['6SP30'];large['plot'][1]+=14
 for lab in large['labels']:
  lab['baseline_top']+=14
  lab['ink_quad_page']=[[x,y+14] for x,y in lab['ink_quad_page']]
  if 'leader' in lab:lab['leader']=[[x,y+14] for x,y in lab['leader']]
 brand='REDPUMP' if '--redpump' in sys.argv else 'PEROTAC'
 pages=make_pages(brand)
 plan={'brand':brand,'source_sha256':DATA['source_sha256'],'current_sha256':DATA['current_sha256'],'decisions':DEC,'phase_models_added_by_user_rule':PHASE_ADDED,'conditional_plan_only':False,'approved_4SP14_correction_used':True,'pages':[{'source_page':p.source_page,'texts':p.texts,'curves':p.curves,'images':p.images,'tables':p.tables} for p in pages],'eta_status':'Source graphical reproduction; not independent test data; viewport limited to shared Q-axis domain','canonical_adopted':False}
 (OUT/f'{brand}-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
 print('PREFLIGHT built',brand,len(pages),'pages;',sum(len(p.curves) for p in pages),'QH curves; no PDF saved yet')
 if '--preview' in sys.argv:preview_pages(brand,pages)
 if '--save' in sys.argv:print(save(brand,pages))
