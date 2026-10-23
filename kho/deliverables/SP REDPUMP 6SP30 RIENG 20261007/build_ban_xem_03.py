import pikepdf, numpy as np, io, json, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Body','fontSPBody.ttf')); pdfmetrics.registerFont(TTFont('Bold','fontSPBold.ttf'))
W,H=595.28,841.89; s=1.1; s2=1.25; ox=(W-404*s)/2; ox2=(W-404*s2)/2; TOP=826.0
DARK=(0.16,0.17,0.19); GRID=(0.88,0.86,0.85); RED=(0.49,0.105,0.13)
ETA_TOP=68.0
src=pikepdf.open('src13.pdf')
# --- H-Q curves read from the accepted PDF page 6 (left panel), table read from the same page text
tab=json.load(open('check_v01.json'))           # model -> kW, H(table)
names=sorted(tab,key=lambda k:tab[k]['H'][0])
ins=pikepdf.parse_content_stream(src.pages[5]); cur=None; curves=[]
for i in ins:
    op=str(i.operator)
    if op=='m': cur=[float(x) for x in i.operands]
    elif op=='c':
        a=[float(x) for x in i.operands]
        if cur[0]==53.0 and 357.2<a[4]<357.3 and cur[1]>270: curves.append(np.array([cur,a[0:2],a[2:4],a[4:6]]))
        cur=a[4:6]
assert len(curves)==19
curves.sort(key=lambda c:c[0][1])
SX=326/45
def Hfun(c):
    # x control points are evenly spaced -> Q linear in t ; H cubic in t
    qmax=(c[3][0]-53)/SX; hy=(c[:,1]-266.0)/0.49
    def h(q):
        t=np.asarray(q)/qmax; return (1-t)**3*hy[0]+3*(1-t)**2*t*hy[1]+3*(1-t)*t**2*hy[2]+t**3*hy[3]
    return h,qmax
qq=np.linspace(0,42,421)
raw={}
for nm,c in zip(names,curves):
    h,qmax=Hfun(c); assert abs(qmax-42)<0.01
    raw[nm]=qq*h(qq)/367.0/tab[nm]['kW']*100     # hydraulic power / rated P2, %
kmax=max(v.max() for v in raw.values()); k=ETA_TOP/kmax
eta={nm:v*k for nm,v in raw.items()}
rep={nm:dict(kW=tab[nm]['kW'],raw_peak=round(float(raw[nm].max()),1),peak=round(float(eta[nm].max()),1),q_peak=round(float(qq[eta[nm].argmax()]),1),
     at_Q={str(q):round(float(eta[nm][q*10]),1) for q in (6,12,18,24,30,36,42)}) for nm in names}
json.dump(dict(k=k,raw_max=kmax,models=rep),open('eta03.json','w'),indent=1)
# --- layout page 1
yA=TOP-309*s
pl=ox+(53-12)*s; pw=326*s; pr=pl+pw
ph=160.0; pb=yA-16-ph
X=lambda q: pl+q/45*pw; Y=lambda e: pb+e/80*ph
yC=pb-24-187*s
LOGO_W=76.6; LOGO_H=LOGO_W*429/966; LOGO_Y=22.0
COL=["#c1121f","#1d4ed8","#15803d","#b45309","#7e22ce","#0e7490","#be185d","#4d7c0f","#1e3a8a","#ea580c","#0f766e","#a21caf","#854d0e","#2563eb","#dc2626","#16a34a","#6d28d9","#0891b2","#525252"]
rgb=lambda hx:tuple(int(hx[i:i+2],16)/255 for i in (1,3,5))
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(W,H),initialFontName='Body'); c.setTitle('REDPUMP 6SP30')
c.setLineWidth(0.3*s); c.setStrokeColorRGB(*GRID)
for e in range(0,81,10): c.line(pl,Y(e),pr,Y(e))
for q in (0,10,20,30,40,45): c.line(X(q),pb,X(q),pb+ph)
c.setStrokeColorRGB(*DARK); c.setLineWidth(0.5*s); c.line(pl,pb,pl,pb+ph); c.line(pl,pb,pr,pb)
c.setFillColorRGB(*DARK); c.setFont('Body',5.3*s)
for e in range(0,81,10): c.drawRightString(pl-5,Y(e)-2.1,str(e))
c.setFont('Bold',6*s)
for q in (0,10,20,30,40,45): c.drawCentredString(X(q),pb-11,str(q))
c.setFont('Bold',5.6*s); c.drawString(ox+(36.2-12)*s,pb-11,'m³/h')
c.drawString(ox+(24-12)*s,pb+ph+5,'η (%)')
# curves: order by value at Q=42 (top to bottom) for colour + label assignment
order=sorted(names,key=lambda n:-eta[n][-1])
colour={n:rgb(COL[i]) for i,n in enumerate(order)}
c.setLineCap(1); c.setLineJoin(1)
for n in names:
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(0.7*s); p=c.beginPath()
    e=eta[n]; d=np.gradient(e,qq)            # Hermite -> cubic Bezier, 14 segments of 3 m3/h
    p.moveTo(X(0),Y(e[0]))
    for a in range(0,420,30):
        b=a+30; dq=qq[b]-qq[a]
        p.curveTo(X(qq[a]+dq/3),Y(e[a]+d[a]*dq/3),X(qq[b]-dq/3),Y(e[b]-d[b]*dq/3),X(qq[b]),Y(e[b]))
    c.drawPath(p,stroke=1,fill=0)
# labels column right of the plot, spread to at least 7.4 pt apart
ys=[Y(eta[n][-1]) for n in order]; gap=7.4
lab=ys[:]
for _ in range(400):
    for i in range(1,len(lab)):
        if lab[i-1]-lab[i]<gap:
            m=(lab[i-1]+lab[i])/2; lab[i-1]=m+gap/2; lab[i]=m-gap/2
hi=pb+ph-3; lo=pb+3
sh=max(0,max(lab)-hi)-max(0,lo-min(lab)); lab=[v-sh for v in lab]
lx=pr+13
for n,y0,y1 in zip(order,ys,lab):
    c.setStrokeColorRGB(*colour[n]); c.setLineWidth(0.35); c.line(X(42)+1.2,y0,lx-2.5,y1)
    c.setFillColorRGB(*colour[n]); c.setFont('Bold',5.2*s); c.drawString(lx,y1-2.0,n)
c.showPage(); c.showPage(); c.save()
new=pikepdf.open(io.BytesIO(buf.getvalue()))
f6=new.copy_foreign(src.pages[5].as_form_xobject()); f9=new.copy_foreign(src.pages[8].as_form_xobject())
logo=new.copy_foreign(src.pages[5].Resources.XObject.SPBrandLogo)
def place(name,sx0,sy0,sx1,sy1,dx,dy,sc):
    return f"q {dx:.3f} {dy:.3f} {(sx1-sx0)*sc:.3f} {(sy1-sy0)*sc:.3f} re W n {sc} 0 0 {sc} {dx-sx0*sc:.3f} {dy-sy0*sc:.3f} cm /{name} Do Q\n"
logo_ops=f"q {LOGO_W:.3f} 0 0 {LOGO_H:.3f} {(W-LOGO_W)/2:.3f} {LOGO_Y:.3f} cm /Logo Do Q\n"
p1=new.pages[0]; p1.Resources.XObject=pikepdf.Dictionary(Src=f6,Logo=logo)
p1.contents_add((place('Src',12,240,416,549,ox,yA,s)+place('Src',12,16,416,203,ox,yC,s)+logo_ops).encode(),prepend=True)
p2=new.pages[1]; p2.Resources.XObject=pikepdf.Dictionary(Src=f9,Logo=logo)
yD=824-205*s2; yE=yD-14-122.7*s2
p2.contents_add((place('Src',416,344,822,549,ox2,yD,s2)+place('Src',416,14.3,822,137,ox2,yE,s2)+logo_ops).encode(),prepend=True)
new.docinfo['/Title']='REDPUMP 6SP30'
new.save('v03.pdf')
print('k',round(k,4),'raw max',round(kmax,2),'yC',yC,'pb',pb)
for n in names: print(n,rep[n])
