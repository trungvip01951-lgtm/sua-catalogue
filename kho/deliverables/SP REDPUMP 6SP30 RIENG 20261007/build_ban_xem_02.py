import pikepdf, numpy as np, io, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Body','fontSPBody.ttf')); pdfmetrics.registerFont(TTFont('Bold','fontSPBold.ttf'))
W,H=595.28,841.89; s=1.25; ox=(W-404*s)/2; TOP=824.0
DARK=(0.16,0.17,0.19); GRID=(0.88,0.86,0.85); RED=(0.49,0.105,0.13)
ETA_MAX=68.0
# --- eta source trace from the accepted PDF (page 6, left panel)
src=pikepdf.open('src13.pdf')
ins=pikepdf.parse_content_stream(src.pages[5]); cur=None; segs=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a=[float(x) for x in i.operands]
        if cur[1]<240 and a[4]<420: segs.append([cur,a[0:2],a[2:4],a[4:6]])
        cur=a[4:6]
assert len(segs)==10
SX=326/45
def qe(pt): return ((pt[0]-53)/SX,(pt[1]-209)/0.3)
segs=[[qe(p) for p in sg] for sg in segs]
t=np.linspace(0,1,2001)
def bez(P):
    P=np.array(P); return ((1-t)**3)[:,None]*P[0]+(3*(1-t)**2*t)[:,None]*P[1]+(3*(1-t)*t**2)[:,None]*P[2]+(t**3)[:,None]*P[3]
allp=np.vstack([bez(sg) for sg in segs]); old_peak=allp[:,1].max(); k=68.0/old_peak
qpk=allp[allp[:,1].argmax(),0]
segs=[[(q,e*k) for q,e in sg] for sg in segs]
info=dict(old_peak=float(old_peak),scale=float(k),q_at_peak=float(qpk),eta_at_Q={str(q):round(float(np.interp(q,allp[:,0],allp[:,1]*k)),1) for q in (0,6,12,18,24,30,36,42)})
json.dump(info,open('eta02.json','w'),indent=1); print(info)
# --- layout
yA=TOP-309*s            # region A bottom (src y 240..549)
pl=ox+(53-12)*s; pw=326*s; pr=pl+pw
pb=yA-94.75; ph=80.0    # eta plot 0..80 %
X=lambda q: pl+q/45*pw; Y=lambda e: pb+e/80*ph
yC=pb-33-187*s          # region C bottom (src y 16..203)
LOGO_W=85.6; LOGO_H=LOGO_W*429/966; LOGO_Y=24.0
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H),initialFontName='Body'); c.setTitle('REDPUMP 6SP30')
# page 1 overlay: efficiency chart
c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
for e in (0,20,40,60,80): c.line(pl,Y(e),pr,Y(e))
for q in (0,10,20,30,40,45): c.line(X(q),pb,X(q),pb+ph)
c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,pb,pl,pb+ph); c.line(pl,pb,pr,pb)
c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
for e in (0,20,40,60,80):
    c.drawRightString(pl-5,Y(e)-2.3,str(e)); c.drawString(pr+5,Y(e)-2.3,str(e))
c.setFont('Bold',6*s)
for q in (0,10,20,30,40,45): c.drawCentredString(X(q),pb-11.5,str(q))
c.setFont('Bold',5.6*s); c.drawString(ox+(36.2-12)*s,pb-11.5,'m³/h')
c.drawString(ox+(24-12)*s,pb+ph+6,'η (%)')
c.setStrokeColorRGB(*RED); c.setLineWidth(0.75*s); c.setLineCap(1); p=c.beginPath()
p.moveTo(X(segs[0][0][0]),Y(segs[0][0][1]))
for sg in segs: p.curveTo(X(sg[1][0]),Y(sg[1][1]),X(sg[2][0]),Y(sg[2][1]),X(sg[3][0]),Y(sg[3][1]))
c.drawPath(p,stroke=1,fill=0)
c.setFillColorRGB(*RED); c.circle(X(qpk),Y(68),1.7,stroke=0,fill=1)
c.setFont('Bold',6*s); c.drawCentredString(X(qpk),Y(68)+5,'η max 68 %')
c.setFont('Bold',5.4*s); c.drawString(X(42)+3,Y(segs[-1][3][1])-2.3,'6SP30')
c.showPage(); c.showPage(); c.save()
new=pikepdf.open(io.BytesIO(buf.getvalue()))
def form(pg):
    return new.copy_foreign(src.pages[pg].as_form_xobject())
f6=form(5); f9=form(8)
logo=new.copy_foreign(src.pages[5].Resources.XObject.SPBrandLogo)
def place(name,sx0,sy0,sx1,sy1,dx,dy):
    # show src rect [sx0,sy0,sx1,sy1] scaled by s with lower-left at (dx,dy)
    return f"q {dx:.3f} {dy:.3f} {(sx1-sx0)*s:.3f} {(sy1-sy0)*s:.3f} re W n {s} 0 0 {s} {dx-sx0*s:.3f} {dy-sy0*s:.3f} cm /{name} Do Q\n"
def logo_ops(): return f"q {LOGO_W:.3f} 0 0 {LOGO_H:.3f} {(W-LOGO_W)/2:.3f} {LOGO_Y:.3f} cm /Logo Do Q\n"
p1=new.pages[0]; p1.Resources.XObject=pikepdf.Dictionary(Src=f6,Logo=logo)
pre=place('Src',12,240,416,549,ox,yA)+place('Src',12,16,416,203,ox,yC)+logo_ops()
p1.contents_add(pre.encode(),prepend=True)
p2=new.pages[1]; p2.Resources.XObject=pikepdf.Dictionary(Src=f9,Logo=logo)
yD=TOP-205*s; yE=yD-14-122.7*s
p2.contents_add((place('Src',416,344,822,549,ox,yD)+place('Src',416,14.3,822,137,ox,yE)+logo_ops()).encode(),prepend=True)
new.docinfo['/Title']='REDPUMP 6SP30'
new.save('v02.pdf',linearize=False)
print('layout',dict(yA=yA,pb=pb,yC=yC,yD=yD,yE=yE,ox=ox))
