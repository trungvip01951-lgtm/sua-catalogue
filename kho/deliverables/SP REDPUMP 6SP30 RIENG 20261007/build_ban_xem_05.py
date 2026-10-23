import pikepdf, numpy as np, io, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Body','fontSPBody.ttf')); pdfmetrics.registerFont(TTFont('Bold','fontSPBold.ttf'))
W,H=595.28,841.89; s=1.2; ox=(W-404*s)/2; TOP=826.0
DARK=(0.16,0.17,0.19); GRID=(0.88,0.86,0.85); RED=(0.49,0.105,0.13); TITLE=(0.47,0.095,0.12); LINE=(0.59,0.55,0.54)
MAXKW=11.0
src=pikepdf.open('src13.pdf')
tab=json.load(open('check_v01.json')); allnames=sorted(tab,key=lambda k:tab[k]['H'][0])
names=[n for n in allnames if tab[n]['kW']<=MAXKW]; assert names==allnames[:9], names
PEAK=dict(zip(names,[66.0,66.8,67.5,68.3,69.0,69.8,70.5,71.3,72.0]))
ins=pikepdf.parse_content_stream(src.pages[5]); cur=None; segs=[]; hq=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a=[float(x) for x in i.operands]; P=np.array([cur,a[0:2],a[2:4],a[4:6]])
        if cur[1]<240 and a[4]<420: segs.append(P)
        elif cur[0]==53.0 and 357.2<a[4]<357.3 and cur[1]>270: hq.append(P)
        cur=a[4:6]
assert len(segs)==10 and len(hq)==19
hq.sort(key=lambda c:c[0][1]); SX=326/45
HQ={n:[((p[0]-53)/SX,(p[1]-266.0)/0.49) for p in P] for n,P in zip(allnames,hq)}      # control points in (Q,H)
t=np.linspace(0,1,401)
pts=np.vstack([((1-t)**3)[:,None]*P[0]+(3*(1-t)**2*t)[:,None]*P[1]+(3*(1-t)*t**2)[:,None]*P[2]+(t**3)[:,None]*P[3] for P in segs])
peak0=(pts[:,1]-209).max(); segn=[[((p[0]-53)/SX,(p[1]-209)/peak0) for p in P] for P in segs]
qs=(pts[:,0]-53)/SX; sh=(pts[:,1]-209)/peak0; qpk=float(qs[sh.argmax()])
json.dump({n:dict(peak=PEAK[n],at_Q={str(q):round(float(np.interp(q,qs,sh))*PEAK[n],1) for q in (6,12,18,24,30,36,42)}) for n in names},open('eta05.json','w'),indent=1)
COL=["#525252","#0891b2","#6d28d9","#16a34a","#ea580c","#1d4ed8","#854d0e","#be185d","#c1121f"]
rgb=lambda hx:tuple(int(hx[i:i+2],16)/255 for i in (1,3,5)); colour={n:rgb(COL[i]) for i,n in enumerate(names)}
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H),initialFontName='Body'); c.setTitle('REDPUMP 6SP30')
def eta_curve(c,n,X,Y,lw):
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(lw); c.setLineCap(1); p=c.beginPath(); pk=PEAK[n]
    p.moveTo(X(segn[0][0][0]),Y(segn[0][0][1]*pk))
    for sg in segn: p.curveTo(X(sg[1][0]),Y(sg[1][1]*pk),X(sg[2][0]),Y(sg[2][1]*pk),X(sg[3][0]),Y(sg[3][1]*pk))
    c.drawPath(p,stroke=1,fill=0)
# ============ page 1
yA=TOP-309*s                               # block A occupies source y 240..549
sx=lambda x: ox+(x-12)*s; sy=lambda y: yA+(y-240)*s
HM=160.0; pl,pr,pb,pt=sx(53),sx(379),sy(266),sy(511)
X=lambda q: pl+q/45*(pr-pl); Y=lambda h: pb+h/HM*(pt-pb)
c.setFillColorRGB(*TITLE); c.setFont('Bold',16*s); c.drawString(sx(24),sy(533),'6SP30')
c.setFillColorRGB(*DARK); c.setFont('Body',5.2*s); c.drawString(sx(24),sy(525),'US gpm'); c.drawString(sx(24),sy(516),'Imp gpm'); c.drawString(sx(391.5),sy(517),'ft')
QT=(0,10,20,30,40,45); c.setFont('Body',5.3*s)
for q,u,im,lm in zip(QT,(0,44,88,132,176,198),(0,37,73,110,147,165),(0,167,333,500,667,750)):
    c.drawCentredString(X(q),sy(525),str(u)); c.drawCentredString(X(q),sy(516),str(im)); c.drawCentredString(X(q),sy(244),str(lm))
c.drawString(sx(36.8),sy(244),'l/min')
c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
for h in (0,40,80,120,160): c.line(pl,Y(h),pr,Y(h))
for q in QT: c.line(X(q),pb,X(q),pt)
for h,ft in zip((0,40,80,120,160),(0,131,262,394,525)):
    c.setFont('Body',5.8*s); c.drawRightString(sx(49.5),Y(h)-2*s,str(h)); c.setFont('Body',5.2*s); c.drawString(sx(384),Y(h)-2*s,str(ft))
c.setFont('Bold',6*s)
for q in QT: c.drawCentredString(X(q),sy(254),str(q))
c.setFont('Bold',5.6*s); c.drawString(sx(36.2),sy(254),'m³/h')
c.saveState(); c.translate(sx(20),(pb+pt)/2); c.rotate(90); c.setFont('Bold',6.4*s); c.drawCentredString(0,0,'Total head H (m)'); c.restoreState()
c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,pb,pl,pt); c.line(pl,pb,pr,pb)
c.setLineCap(0)
for n in names:
    P=HQ[n]; c.setStrokeColorRGB(*RED); c.setLineWidth(0.75*s); p=c.beginPath(); p.moveTo(X(P[0][0]),Y(P[0][1])); p.curveTo(X(P[1][0]),Y(P[1][1]),X(P[2][0]),Y(P[2][1]),X(P[3][0]),Y(P[3][1])); c.drawPath(p,stroke=1,fill=0)
    c.setFillColorRGB(*RED); c.setFont('Bold',5.6*s); c.drawString(X(0)+3.5*s,Y(P[0][1])+2.2*s,n)
# efficiency chart (axis 40..75 %)
ph=200.0; eb=yA-16-ph; E0,E1=40,75; Ye=lambda e: eb+(e-E0)/(E1-E0)*ph
c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
for e in range(E0,E1+1,5): c.line(pl,Ye(e),pr,Ye(e))
for q in QT: c.line(X(q),eb,X(q),eb+ph)
c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
for e in range(E0,E1+1,5): c.drawRightString(pl-5,Ye(e)-2.1,str(e))
c.setFont('Bold',6*s)
for q in QT: c.drawCentredString(X(q),eb-12,str(q))
c.setFont('Bold',5.6*s); c.drawString(sx(36.2),eb-12,'m³/h'); c.drawString(sx(24),eb+ph+5,'η (%)')
c.saveState(); cp=c.beginPath(); cp.rect(pl,eb,pr-pl,ph); c.clipPath(cp,stroke=0,fill=0)
for n in names: eta_curve(c,n,X,Ye,0.75*s)
c.restoreState()
c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,eb,pl,eb+ph); c.line(pl,eb,pr,eb)
order=names[::-1]; e42=float(np.interp(42,qs,sh)); gap=10.0; mid=eb+ph*0.36; lx=pr+12
for i,n in enumerate(order):
    y1=mid+gap*((len(order)-1)/2-i)
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(0.4); c.line(X(42)+1.5,Ye(e42*PEAK[n]),lx-2.5,y1)
    c.setFillColorRGB(*colour[n]); c.setFont('Bold',5.4*s); c.drawString(lx,y1-2.2,f"{n}   {PEAK[n]:.1f}")
c.setFillColorRGB(*DARK); c.setFont('Body',5.0*s); c.drawString(lx,mid+gap*4+11,'Model   η max (%)')
# performance table: source rows 1..9 kept by clipping (source y 87.8..203); close the gap + new 'H (m)'
CY0=87.8; yC=eb-26-(203-CY0)*s; ty=lambda y: yC+(y-CY0)*s
c.setStrokeColorRGB(*LINE); c.setLineWidth(0.6*s); c.line(sx(149),ty(88.1),sx(180),ty(88.1))
c.setFillColorRGB(*DARK); c.setFont('Bold',6.8*s); c.drawCentredString(sx(164.5),ty((152+88.1)/2-2.5),'H (m)')
c.showPage()
# ============ page 2 : one small efficiency chart per model + dimensions
s2=1.2; ox2=(W-404*s2)/2
c.setFillColorRGB(*TITLE); c.setFont('Bold',11*s2); c.drawString(ox2+12*s2,TOP-20,'6SP30  |  Efficiency η (%) by model')
cols=3; gw=(380*s2)/cols; gh=124.0; top0=TOP-34; w=gw-40; h=76.0
for k,n in enumerate(names):
    r,cc=divmod(k,cols); x0=ox2+12*s2+cc*gw+24; y0=top0-r*gh-22-h
    Xs=lambda q,x0=x0: x0+q/45*w; Ys=lambda e,y0=y0: y0+e/80*h
    c.setLineWidth(0.3); c.setStrokeColorRGB(*GRID)
    for e in (0,20,40,60,80): c.line(x0,Ys(e),x0+w,Ys(e))
    for q in (0,15,30,45): c.line(Xs(q),y0,Xs(q),y0+h)
    c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5); c.line(x0,y0,x0,y0+h); c.line(x0,y0,x0+w,y0)
    c.setFillColorRGB(*DARK); c.setFont('Body',5.6)
    for e in (0,20,40,60,80): c.drawRightString(x0-3.5,Ys(e)-1.9,str(e))
    for q in (0,15,30,45): c.drawCentredString(Xs(q),y0-8.5,str(q))
    c.drawRightString(x0+w,y0-17,'Q (m³/h)')
    eta_curve(c,n,Xs,Ys,1.0)
    c.setFillColorRGB(*colour[n]); c.circle(Xs(qpk),Ys(PEAK[n]),1.6,stroke=0,fill=1)
    c.setFont('Bold',7.6); c.drawString(x0,y0+h+7,n)
    c.setFillColorRGB(*DARK); c.setFont('Body',6.6); c.drawRightString(x0+w,y0+h+7,f"η max {PEAK[n]:.1f} %")
gbot=top0-3*gh
DY0=431.8; yD=gbot-6-(549-DY0)*s2; yE=yD-8-122.7*s2
c.showPage(); c.save()
new=pikepdf.open(io.BytesIO(buf.getvalue()))
f6=new.copy_foreign(src.pages[5].as_form_xobject()); f9=new.copy_foreign(src.pages[8].as_form_xobject()); logo=new.copy_foreign(src.pages[5].Resources.XObject.SPBrandLogo)
def place(name,sx0,sy0,sx1,sy1,dx,dy,sc): return f"q {dx:.3f} {dy:.3f} {(sx1-sx0)*sc:.3f} {(sy1-sy0)*sc:.3f} re W n {sc} 0 0 {sc} {dx-sx0*sc:.3f} {dy-sy0*sc:.3f} cm /{name} Do Q\n"
LW=76.6; logo_ops=f"q {LW:.3f} 0 0 {LW*429/966:.3f} {(W-LW)/2:.3f} 22 cm /Logo Do Q\n"
p1=new.pages[0]; p1.Resources.XObject=pikepdf.Dictionary(Src=f6,Logo=logo)
p1.contents_add((place('Src',12,CY0,416,203,ox,yC,s)+logo_ops).encode(),prepend=True)
p2=new.pages[1]; p2.Resources.XObject=pikepdf.Dictionary(Src=f9,Logo=logo)
p2.contents_add((place('Src',416,DY0,822,549,ox2,yD,s2)+place('Src',416,14.3,822,137,ox2,yE,s2)+logo_ops).encode(),prepend=True)
new.save('v05.pdf'); print('yC',yC,'yE',yE,names)
