import pikepdf, numpy as np, io, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Body','fontSPBody.ttf')); pdfmetrics.registerFont(TTFont('Bold','fontSPBold.ttf'))
import sys
W,H=595.28,841.89; s=1.1 if sys.argv[1]=='M' else 1.2; ox=(W-404*s)/2; TOP=826.0
DARK=(0.16,0.17,0.19); GRID=(0.88,0.86,0.85); RED=(0.49,0.105,0.13); TITLE=(0.47,0.095,0.12); LINE=(0.59,0.55,0.54); STRIPE=(0.985,0.971,0.967)
KW0,KW1=4.0,15.0
src=pikepdf.open('src13.pdf')
tab=json.load(open('check_v01.json')); allnames=sorted(tab,key=lambda k:tab[k]['H'][0])
names=[n for n in allnames if KW0<=tab[n]['kW']<=KW1]; i0=allnames.index(names[0]); N=len(names)
assert names==allnames[i0:i0+N] and N==9, names
import sys; MODE=sys.argv[1]; OUT=sys.argv[2]
PEAK=dict(zip(names,[67.0,67.3,67.5,67.8,68.0,68.3,68.5,68.8,69.0]))   # multi-curve version: about 68 %, slightly higher with more stages
ins=pikepdf.parse_content_stream(src.pages[5]); cur=None; hq=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a=[float(x) for x in i.operands]; P=np.array([cur,a[0:2],a[2:4],a[4:6]])
        if cur[0]==53.0 and 357.2<a[4]<357.3 and cur[1]>270: hq.append(P)
        cur=a[4:6]
assert len(hq)==19
hq.sort(key=lambda c:c[0][1]); SX=326/45
HQ={n:[((p[0]-53)/SX,(p[1]-266.0)/0.49) for p in P] for n,P in zip(allnames,hq)}
# efficiency: the catalogue's own eta(Q) trace (page 6) as common shape, peak per model; plotted against HEAD of the model
cur=None; segs=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a_=[float(x) for x in i.operands]
        if cur[1]<240 and a_[4]<420: segs.append(np.array([cur,a_[0:2],a_[2:4],a_[4:6]]))
        cur=a_[4:6]
assert len(segs)==10
tt=np.linspace(0,1,401)
pts=np.vstack([((1-tt)**3)[:,None]*P[0]+(3*(1-tt)**2*tt)[:,None]*P[1]+(3*(1-tt)*tt**2)[:,None]*P[2]+(tt**3)[:,None]*P[3] for P in segs])
qs=(pts[:,0]-53)/SX; shp=(pts[:,1]-209); shp=shp/shp.max()
qq=np.linspace(0,42,421); SH=np.interp(qq,qs,shp); ETA={}; HH={}
for n in names:
    P=HQ[n]; t=qq/P[3][0]; HH[n]=(1-t)**3*P[0][1]+3*(1-t)**2*t*P[1][1]+3*(1-t)*t**2*P[2][1]+t**3*P[3][1]; ETA[n]=SH*PEAK[n]
rep={n:dict(kW=tab[n]['kW'],peak=PEAK[n],H_at_peak=round(float(HH[n][ETA[n].argmax()]),1),Q_at_peak=round(float(qq[ETA[n].argmax()]),1),
     points={str(q):dict(H=round(float(HH[n][q*10]),1),eta=round(float(ETA[n][q*10]),1)) for q in (6,12,18,24,30,36,42)}) for n in names}
json.dump(dict(models=rep),open('eta10.json','w'),indent=1)
COL=["#525252","#0891b2","#6d28d9","#16a34a","#ea580c","#1d4ed8","#854d0e","#be185d","#c1121f"]
rgb=lambda hx:tuple(int(hx[i:i+2],16)/255 for i in (1,3,5)); colour={n:rgb(COL[i]) for i,n in enumerate(names)}
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H),initialFontName='Body'); c.setTitle('REDPUMP 6SP30')
DUTY={}
def sheet(mode):
    global yHdr,yRows,r_top,r_bot
    yA=TOP-309*s; sx=lambda x: ox+(x-12)*s; sy=lambda y: yA+(y-240)*s
    HM=200.0; pl,pr,pb,pt=sx(53),sx(379),sy(266),sy(511)
    X=lambda q: pl+q/45*(pr-pl); Y=lambda h: pb+h/HM*(pt-pb)
    c.setFillColorRGB(*TITLE); c.setFont('Bold',16*s); c.drawString(sx(24),sy(533),'6SP30')
    c.setFillColorRGB(*DARK); c.setFont('Body',5.2*s); c.drawString(sx(24),sy(525),'US gpm'); c.drawString(sx(24),sy(516),'Imp gpm'); c.drawString(sx(391.5),sy(517),'ft')
    QT=(0,10,20,30,40,45); c.setFont('Body',5.3*s)
    for q,u,im,lm in zip(QT,(0,44,88,132,176,198),(0,37,73,110,147,165),(0,167,333,500,667,750)):
        c.drawCentredString(X(q),sy(525),str(u)); c.drawCentredString(X(q),sy(516),str(im)); c.drawCentredString(X(q),sy(244),str(lm))
    c.drawString(sx(36.8),sy(244),'l/min')
    c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
    HT=(0,50,100,150,200)
    for h in HT: c.line(pl,Y(h),pr,Y(h))
    for q in QT: c.line(X(q),pb,X(q),pt)
    for h in HT:
        c.setFont('Body',5.8*s); c.drawRightString(sx(49.5),Y(h)-2*s,str(h)); c.setFont('Body',5.2*s); c.drawString(sx(384),Y(h)-2*s,str(round(h*3.28084)))
    c.setFont('Bold',6*s)
    for q in QT: c.drawCentredString(X(q),sy(254),str(q))
    c.setFont('Bold',5.6*s); c.drawString(sx(36.2),sy(254),'m³/h')
    c.saveState(); c.translate(sx(20),(pb+pt)/2); c.rotate(90); c.setFont('Bold',6.4*s); c.drawCentredString(0,0,'Total head H (m)'); c.restoreState()
    c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,pb,pl,pt); c.line(pl,pb,pr,pb)
    for n in names:
        P=HQ[n]; c.setStrokeColorRGB(*RED); c.setLineWidth(0.75*s); p=c.beginPath(); p.moveTo(X(P[0][0]),Y(P[0][1])); p.curveTo(X(P[1][0]),Y(P[1][1]),X(P[2][0]),Y(P[2][1]),X(P[3][0]),Y(P[3][1])); c.drawPath(p,stroke=1,fill=0)
        c.setFillColorRGB(*RED); c.setFont('Bold',5.6*s); c.drawString(X(0)+3.5*s,Y(P[0][1])+2.2*s,n)
    if mode=='Q':
        # efficiency chart, standard presentation: eta against flow Q, one curve valid for the whole family
        ph=200.0; eb=yA-16-ph; Ye=lambda e: eb+e/80*ph
        c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
        for e in range(0,81,10): c.line(pl,Ye(e),pr,Ye(e))
        for q in QT: c.line(X(q),eb,X(q),eb+ph)
        c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
        for e in range(0,81,10): c.drawRightString(pl-5,Ye(e)-2.1,str(e)); c.drawString(pr+5,Ye(e)-2.1,str(e))
        c.setFont('Bold',6*s)
        for q in QT: c.drawCentredString(X(q),eb-12,str(q))
        c.setFont('Bold',5.6*s); c.drawString(sx(36.2),eb-12,'m³/h'); c.drawString(sx(24),eb+ph+5,'η (%)')
        e=SH*68.0; de=np.gradient(e,qq); c.setLineCap(1); c.setStrokeColorRGB(*RED); c.setLineWidth(0.9*s); p=c.beginPath(); p.moveTo(X(0),Ye(e[0]))
        for a in range(0,420,20):
            b=a+20; dq=qq[b]-qq[a]; p.curveTo(X(qq[a]+dq/3),Ye(e[a]+de[a]*dq/3),X(qq[b]-dq/3),Ye(e[b]-de[b]*dq/3),X(qq[b]),Ye(e[b]))
        c.drawPath(p,stroke=1,fill=0)
        k=e.argmax(); c.setFillColorRGB(*RED); c.circle(X(qq[k]),Ye(e[k]),1.9,stroke=0,fill=1)
        c.setFont('Bold',6*s); c.drawCentredString(X(qq[k]),Ye(e[k])+6,'η max 68 %')
        c.setFont('Bold',5.4*s); c.drawString(X(13),Ye(12),'6SP30-4 … 6SP30-17')
        c.setFillColorRGB(*DARK); c.setFont('Body',5.0*s); c.drawString(X(13),Ye(12)-8.5,'Pump efficiency, same curve for all models')
        c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,eb,pl,eb+ph); c.line(pl,eb,pr,eb)
    else:
        # efficiency against flow Q, one curve per model, axis from 0
        ph=245.0; eb=yA-16-ph; E0,E1=0,70; Ye=lambda e: eb+(e-E0)/(E1-E0)*ph
        c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
        for e in range(E0,E1+1,10): c.line(pl,Ye(e),pr,Ye(e))
        for q in QT: c.line(X(q),eb,X(q),eb+ph)
        c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
        for e in range(E0,E1+1,10): c.drawRightString(pl-5,Ye(e)-2.1,str(e))
        c.setFont('Bold',6*s)
        for q in QT: c.drawCentredString(X(q),eb-12,str(q))
        c.setFont('Bold',5.6*s); c.drawString(sx(36.2),eb-12,'m³/h'); c.drawString(sx(24),eb+ph+5,'η (%)')
        c.saveState(); cp=c.beginPath(); cp.rect(pl,eb,pr-pl,ph); c.clipPath(cp,stroke=0,fill=0); c.setLineCap(1)
        for n in names:
            e=ETA[n]; de=np.gradient(e,qq); c.setStrokeColorRGB(*colour[n]); c.setLineWidth(0.5); p=c.beginPath(); p.moveTo(X(0),Ye(e[0]))
            for a in range(0,420,20):
                b=a+20; dq=qq[b]-qq[a]; p.curveTo(X(qq[a]+dq/3),Ye(e[a]+de[a]*dq/3),X(qq[b]-dq/3),Ye(e[b]-de[b]*dq/3),X(qq[b]),Ye(e[b]))
            c.drawPath(p,stroke=1,fill=0)
        c.restoreState()
        c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,eb,pl,eb+ph); c.line(pl,eb,pr,eb)
        lx=pr+12; gap=10.0; mid=eb+ph*0.5
        for i,n in enumerate(names[::-1]):
            y1=mid+gap*((N-1)/2-i)
            c.setStrokeColorRGB(*colour[n]); c.setLineWidth(1.2); c.line(lx,y1,lx+9,y1)
            c.setFillColorRGB(*colour[n]); c.setFont('Bold',5.4*s); c.drawString(lx+12,y1-2.2,f"{n}   {PEAK[n]:.1f}")
        c.setFillColorRGB(*DARK); c.setFont('Body',5.0*s); c.drawString(lx+12,mid+gap*4+11,'Model   η max (%)')
    # duty point markers on 6SP30-5
    DN='6SP30-5'; MK=(0.87,0.06,0.06)
    def tag(x,y,lines,left=False):
        c.setFont('Bold',5.6*s); w=max(c.stringWidth(t,'Bold',5.6*s) for t in lines)+8; h=len(lines)*7.6*s/1.1+5
        if left: x=x-w
        c.setFillColorRGB(1,1,1); c.setStrokeColorRGB(*MK); c.setLineWidth(0.6); c.roundRect(x,y,w,h,2,stroke=1,fill=1)
        c.setFillColorRGB(*MK)
        for i,t in enumerate(lines): c.drawString(x+4,y+h-(i+1)*7.6*s/1.1+1.5,t)
    for DQ,left,oe,oh in ((27.0,False,2.6,-2.4),(25.0,True,-3.4,2.4)):
        k=int(round(DQ*10)); dh=float(HH[DN][k]); de=float(ETA[DN][k]); DUTY[DQ]=dict(H=dh,eta=de)
        c.setStrokeColorRGB(*MK); c.setFillColorRGB(*MK); c.setLineWidth(0.8); c.setDash(4,2.5); c.setLineCap(0)
        c.line(X(DQ),pb,X(DQ),Y(dh)); c.line(pl,Y(dh),X(DQ),Y(dh)); c.line(X(DQ),eb,X(DQ),Ye(de)); c.line(pl,Ye(de),X(DQ),Ye(de))
        c.setDash(); c.circle(X(DQ),Y(dh),2.4,stroke=0,fill=1); c.circle(X(DQ),Ye(de),2.4,stroke=0,fill=1)
        c.setFont('Bold',5.6*s); c.drawRightString(pl-5,Ye(de)-2.1+oe,f"{de:.1f}"); c.drawRightString(sx(49.5),Y(dh)-2*s+oh,f"{dh:.1f}")
        c.drawCentredString(X(DQ),eb-12,f"{DQ:g}"); c.drawCentredString(X(DQ),sy(254),f"{DQ:g}")
        sgn=-7 if left else 7
        tag(X(DQ)+sgn,Y(dh)+6,[DN,f"Q = {DQ:g} m³/h   H = {dh:.1f} m"],left)
        tag(X(DQ)+sgn,Ye(de)-34,[DN,f"Q = {DQ:g} m³/h   η = {de:.1f} %"],left)
    # performance table = source header (y 151.7..203) + source rows i0+1 .. i0+N
    RH=7.1; r_top=152-i0*RH; r_bot=152-(i0+N)*RH
    yHdr=eb-26-(203-151.7)*s; yRows=yHdr-(r_top-(r_bot-0.3))*s
    ty=lambda y: yRows+(y-(r_bot-0.3))*s
    c.setFillColorRGB(1,1,1); c.rect(sx(149.3),ty(r_bot+0.3),(179.7-149.3)*s,(r_top-r_bot-0.3)*s,stroke=0,fill=1)
    c.setFillColorRGB(*STRIPE)
    for k in range(N):
        if (i0+k)%2==0: c.rect(sx(149.3),ty(r_top-(k+1)*RH),(179.7-149.3)*s,RH*s,stroke=0,fill=1)
    c.setStrokeColorRGB(*LINE); c.setLineWidth(0.6*s); c.line(sx(149),ty(r_bot),sx(180),ty(r_bot)); c.line(sx(149),ty(r_bot),sx(149),ty(r_top)); c.line(sx(180),ty(r_bot),sx(180),ty(r_top))
    c.setFillColorRGB(*DARK); c.setFont('Bold',6.8*s); c.drawCentredString(sx(164.5),ty((r_top+r_bot)/2-2.5),'H (m)')
sheet(MODE)
c.showPage()
# page 2: dimensions (source page 9 right column): title+header (y 504.7..549) + rows
s2=1.2; ox2=(W-404*s2)/2; DH=8.1; d_top=505-i0*DH; d_bot=505-(i0+N)*DH
yDh=TOP-(549-504.7)*s2; yDr=yDh-(d_top-(d_bot-0.3))*s2; yE=yDr-10-122.7*s2
c.showPage(); c.save()
new=pikepdf.open(io.BytesIO(buf.getvalue()))
f6=new.copy_foreign(src.pages[5].as_form_xobject()); f9=new.copy_foreign(src.pages[8].as_form_xobject()); logo=new.copy_foreign(src.pages[5].Resources.XObject.SPBrandLogo)
def place(name,sx0,sy0,sx1,sy1,dx,dy,sc): return f"q {dx:.3f} {dy:.3f} {(sx1-sx0)*sc:.3f} {(sy1-sy0)*sc:.3f} re W n {sc} 0 0 {sc} {dx-sx0*sc:.3f} {dy-sy0*sc:.3f} cm /{name} Do Q\n"
LW=76.6; logo_ops=f"q {LW:.3f} 0 0 {LW*429/966:.3f} {(W-LW)/2:.3f} 22 cm /Logo Do Q\n"
for p1 in (new.pages[0],):
  p1.Resources.XObject=pikepdf.Dictionary(Src=f6,Logo=logo)
  p1.contents_add((place('Src',12,r_bot-0.3,416,r_top,ox,yRows,s)+place('Src',12,151.7,416,203,ox,yHdr,s)+logo_ops).encode(),prepend=True)
p2=new.pages[1]; p2.Resources.XObject=pikepdf.Dictionary(Src=f9,Logo=logo)
p2.contents_add((place('Src',416,d_bot-0.3,822,d_top,ox2,yDr,s2)+place('Src',416,504.7,822,549,ox2,yDh,s2)+place('Src',416,14.3,822,137,ox2,yE,s2)+logo_ops).encode(),prepend=True)
new.save(OUT); print('DUTY',DUTY); print(names,'yRows',yRows)
for n in names: print(n,rep[n])
