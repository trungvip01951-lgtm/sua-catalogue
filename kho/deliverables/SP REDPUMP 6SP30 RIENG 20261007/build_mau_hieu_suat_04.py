import pikepdf, numpy as np, io, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Body','fontSPBody.ttf')); pdfmetrics.registerFont(TTFont('Bold','fontSPBold.ttf'))
W,H=595.28,841.89; s=1.05; ox=(W-404*s)/2; TOP=826.0
DARK=(0.16,0.17,0.19); GRID=(0.88,0.86,0.85); RED=(0.49,0.105,0.13)
LO,HI=66.0,72.0
src=pikepdf.open('src13.pdf')
tab=json.load(open('check_v01.json')); names=sorted(tab,key=lambda k:tab[k]['H'][0])   # -2 ... -42
# shape = the catalogue's own eta trace (page 6, left panel), normalised to peak 1
ins=pikepdf.parse_content_stream(src.pages[5]); cur=None; segs=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a=[float(x) for x in i.operands]
        if cur[1]<240 and a[4]<420: segs.append(np.array([cur,a[0:2],a[2:4],a[4:6]]))
        cur=a[4:6]
assert len(segs)==10
SX=326/45; t=np.linspace(0,1,401)
pts=np.vstack([((1-t)**3)[:,None]*P[0]+(3*(1-t)**2*t)[:,None]*P[1]+(3*(1-t)*t**2)[:,None]*P[2]+(t**3)[:,None]*P[3] for P in segs])
peak0=(pts[:,1]-209).max()
segn=[[((p[0]-53)/SX,(p[1]-209)/peak0) for p in P] for P in segs]     # (Q, shape 0..1)
qs=(pts[:,0]-53)/SX; sh=(pts[:,1]-209)/peak0; qpk=float(qs[sh.argmax()])
peaks={n:LO+(HI-LO)*i/(len(names)-1) for i,n in enumerate(names)}
rep={n:dict(peak=round(peaks[n],1),at_Q={str(q):round(float(np.interp(q,qs,sh))*peaks[n],1) for q in (6,12,18,24,30,36,42)}) for n in names}
json.dump(dict(q_peak=qpk,models=rep),open('eta04.json','w'),indent=1)
COL=["#525252","#0891b2","#6d28d9","#16a34a","#dc2626","#2563eb","#854d0e","#a21caf","#0f766e","#ea580c","#1e3a8a","#4d7c0f","#be185d","#0e7490","#7e22ce","#b45309","#15803d","#1d4ed8","#c1121f"]
rgb=lambda hx:tuple(int(hx[i:i+2],16)/255 for i in (1,3,5)); colour={n:rgb(COL[i]) for i,n in enumerate(names)}
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H),initialFontName='Body'); c.setTitle('REDPUMP 6SP30')
def curve(c,n,X,Y,lw):
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(lw); c.setLineCap(1); p=c.beginPath(); pk=peaks[n]
    p.moveTo(X(segn[0][0][0]),Y(segn[0][0][1]*pk))
    for sg in segn: p.curveTo(X(sg[1][0]),Y(sg[1][1]*pk),X(sg[2][0]),Y(sg[2][1]*pk),X(sg[3][0]),Y(sg[3][1]*pk))
    c.drawPath(p,stroke=1,fill=0)
# ================= page 1 : option A — one chart, axis zoomed 40..75 %
yA=TOP-309*s; pl=ox+(53-12)*s; pw=326*s; pr=pl+pw; ph=200.0; pb=yA-16-ph; E0,E1=40,75
X=lambda q: pl+q/45*pw; Y=lambda e: pb+(e-E0)/(E1-E0)*ph
yC=pb-24-187*s
c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
for e in range(E0,E1+1,5): c.line(pl,Y(e),pr,Y(e))
for q in (0,10,20,30,40,45): c.line(X(q),pb,X(q),pb+ph)
c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
for e in range(E0,E1+1,5): c.drawRightString(pl-5,Y(e)-2.1,str(e))
c.setFont('Bold',6*s)
for q in (0,10,20,30,40,45): c.drawCentredString(X(q),pb-11,str(q))
c.setFont('Bold',5.6*s); c.drawString(ox+(36.2-12)*s,pb-11,'m³/h'); c.drawString(ox+(24-12)*s,pb+ph+5,'η (%)')
c.saveState(); cp=c.beginPath(); cp.rect(pl,pb,pw,ph); c.clipPath(cp,stroke=0,fill=0)
for n in names: curve(c,n,X,Y,0.65*s)
c.restoreState()
c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,pb,pl,pb+ph); c.line(pl,pb,pr,pb)
order=names[::-1]; e42=float(np.interp(42,qs,sh)); ys=[Y(e42*peaks[n]) for n in order]
gap=7.6; mid=pb+ph*0.42; lab=[mid+gap*((len(order)-1)/2-i) for i in range(len(order))]; lx=pr+13
for n,y0,y1 in zip(order,ys,lab):
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(0.35); c.line(X(42)+1.2,y0,lx-2.5,y1)
    c.setFillColorRGB(*colour[n]); c.setFont('Bold',5.2*s); c.drawString(lx,y1-2.0,f"{n}  {peaks[n]:.1f}")
c.setFillColorRGB(*DARK); c.setFont('Body',5.0*s); c.drawString(lx,lab[0]+9,'Model  η max (%)')
c.showPage()
# ================= page 2 : option B — one small chart per model
c.setFillColorRGB(0.47,0.095,0.12); c.setFont('Bold',16*s); c.drawString(ox,TOP-22,'6SP30'); c.setFont('Bold',9); c.drawString(ox+62,TOP-22,'|  Efficiency η (%) by model')
cols,rows=4,5; gw=(404*s)/cols; gh=128.0; top0=TOP-44; w=gw-34; h=78.0
for k,n in enumerate(names):
    r,cc=divmod(k,cols); x0=ox+cc*gw+22; y0=top0-r*gh-22-h
    Xs=lambda q,x0=x0: x0+q/45*w; Ys=lambda e,y0=y0: y0+e/80*h
    c.setLineWidth(0.3); c.setStrokeColorRGB(*GRID)
    for e in (0,20,40,60,80): c.line(x0,Ys(e),x0+w,Ys(e))
    for q in (0,15,30,45): c.line(Xs(q),y0,Xs(q),y0+h)
    c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5); c.line(x0,y0,x0,y0+h); c.line(x0,y0,x0+w,y0)
    c.setFillColorRGB(*DARK); c.setFont('Body',5.3)
    for e in (0,20,40,60,80): c.drawRightString(x0-3.5,Ys(e)-1.9,str(e))
    for q in (0,15,30,45): c.drawCentredString(Xs(q),y0-8,str(q))
    curve(c,n,Xs,Ys,0.9)
    c.setFillColorRGB(*colour[n]); c.circle(Xs(qpk),Ys(peaks[n]),1.5,stroke=0,fill=1)
    c.setFont('Bold',7.2); c.drawString(x0,y0+h+7,n)
    c.setFillColorRGB(*DARK); c.setFont('Body',6.2); c.drawRightString(x0+w,y0+h+7,f"η max {peaks[n]:.1f} %")
r,cc=divmod(19,cols); x0=ox+cc*gw+22; y0=top0-r*gh-22-h
c.setFillColorRGB(*DARK); c.setFont('Body',6.2); c.drawString(x0,y0+h-6,'Horizontal axis: Q (m³/h)'); c.drawString(x0,y0+h-17,'Vertical axis: η (%)'); c.drawString(x0,y0+h-28,'50 Hz  |  n ≈ 2850 /min')
c.showPage(); c.save()
new=pikepdf.open(io.BytesIO(buf.getvalue()))
f6=new.copy_foreign(src.pages[5].as_form_xobject()); logo=new.copy_foreign(src.pages[5].Resources.XObject.SPBrandLogo)
def place(name,sx0,sy0,sx1,sy1,dx,dy,sc): return f"q {dx:.3f} {dy:.3f} {(sx1-sx0)*sc:.3f} {(sy1-sy0)*sc:.3f} re W n {sc} 0 0 {sc} {dx-sx0*sc:.3f} {dy-sy0*sc:.3f} cm /{name} Do Q\n"
LW=76.6; logo_ops=f"q {LW:.3f} 0 0 {LW*429/966:.3f} {(W-LW)/2:.3f} 22 cm /Logo Do Q\n"
p1=new.pages[0]; p1.Resources.XObject=pikepdf.Dictionary(Src=f6,Logo=logo)
p1.contents_add((place('Src',12,240,416,549,ox,yA,s)+place('Src',12,16,416,203,ox,yC,s)+logo_ops).encode(),prepend=True)
p2=new.pages[1]; p2.Resources.XObject=pikepdf.Dictionary(Logo=logo); p2.contents_add(logo_ops.encode(),prepend=True)
new.save('v04.pdf'); print('yC',yC,'qpk',qpk); print({n:rep[n]['peak'] for n in names})
