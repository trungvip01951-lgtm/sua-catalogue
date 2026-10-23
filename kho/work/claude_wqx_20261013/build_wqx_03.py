import pymupdf, glob, os, sys, io, hashlib, numpy as np
from PIL import Image
K=os.path.expanduser("~/mnt/Sửa catalogue")
REF=glob.glob(K+"/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/*FC inox.pdf")[0]
CUT=K+"/work/claude_wqx_20261013/ANH DAI DIEN 80WQX40-15-5.5 (v2 nen trong suot).png"
OUT=sys.argv[1]
FR="/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
FB="/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
def rgb(h): return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
NAVY=rgb("14334D"); BLUE=rgb("1A669E"); LIGHT=rgb("EDF5FA"); GREY=rgb("5C6F7E"); TXT=rgb("1F3A4F"); LINE=rgb("C9D8E3"); GRID=rgb("DCE6EE"); WHITE=(1,1,1)
# --- du lieu (bao gia BG-13102026-004 + ten model); duong cong khoa qua (0;25) (40;15) (80;1)
QT=[0,20,40,60,80]; HT=[25,20,15,9,1]
c3=-1.0e-5; A=np.array([[40,1600],[80,6400.]]); a1,a2=np.linalg.solve(A,np.array([-10-64000*c3,-24-512000*c3]))
Hq=lambda q: 25+a1*q+a2*q**2+c3*q**3
ref=pymupdf.open(REF); lx=15; base=pymupdf.Pixmap(ref,lx); sm=ref.xref_get_key(lx,"SMask")
if sm[0]=="xref": base=pymupdf.Pixmap(base,pymupdf.Pixmap(ref,int(sm[1].split()[0])))
logo_png=base.tobytes("png")
cut=Image.open(CUT).convert("RGBA")
bgc=tuple(int(x*255) for x in LIGHT); bgim=Image.new("RGB",cut.size,bgc); bgim.paste(cut,mask=cut.split()[3])
b=io.BytesIO(); bgim.save(b,"JPEG",quality=92); photo=b.getvalue(); cw,ch=cut.size
d=pymupdf.open(); p=d.new_page(width=595.2,height=841.92)
p.insert_font("R",fontfile=FR); p.insert_font("B",fontfile=FB)
fr=pymupdf.Font(fontfile=FR); fb=pymupdf.Font(fontfile=FB)
def T(x,y,s,sz,f="R",c=TXT): p.insert_text((x,y),s,fontname=f,fontsize=sz,color=c)
def W(s,sz,f="R"): return (fb if f=="B" else fr).text_length(s,fontsize=sz)
def C(x,y,s,sz,f="R",c=TXT): T(x-W(s,sz,f)/2,y,s,sz,f,c)
def R(r,fill=None,col=None,w=0.6): p.draw_rect(pymupdf.Rect(r),color=col,fill=fill,width=w)
def H(x,y,s,w): T(x,y,s,9,"B",BLUE); p.draw_line((x,y+4),(x+w,y+4),color=BLUE,width=0.8)
# dau trang
R((190,0,595.2,78),fill=LIGHT)
p.insert_image(pymupdf.Rect(40,16,174.5,62),stream=logo_png)
T(208,52,"80WQX",30,"B",NAVY)
s="SINGLE MODEL  /  DATA SHEET"; T(555-W(s,10,"B"),36,s,10,"B",NAVY)
s="Stainless steel submersible sewage pump"; T(555-W(s,8),52,s,8,"R",GREY)
p.draw_line((0,78),(595.2,78),color=LINE,width=0.6)
# anh dai dien tren nen sang
panel=pymupdf.Rect(40,96,292,404); R(panel,fill=LIGHT)
ih=panel.height-10; iw=ih*cw/ch; cx=(panel.x0+panel.x1)/2
p.insert_image(pymupdf.Rect(cx-iw/2,panel.y0+5,cx+iw/2,panel.y1-5),stream=photo)
# thong so chinh
x0,x1=312,555; y=104; H(x0,y,"KEY DATA",x1-x0); y+=10
rows=[("Model","80WQX40-15-5.5"),("Power","5.5 kW  /  7.5 HP"),("Power supply","3~  380–415 V  /  50 Hz"),
("Max. flow","80 m³/h  (1333 l/min)"),("Max. head","25 m"),("Rated flow","40 m³/h  (667 l/min)"),
("Rated head","15 m"),("Discharge","DN80, flanged"),("Construction","Stainless steel"),("Origin","Made in Taiwan")]
for i,(a,v) in enumerate(rows):
    if i%2==0: R((x0,y,x1,y+17),fill=LIGHT)
    T(x0+6,y+11.5,a,8,"R",TXT); T(x1-6-W(v,8,"B"),y+11.5,v,8,"B",NAVY); y+=17
y+=20; H(x0,y,"PRODUCT NOMENCLATURE",x1-x0); y+=18
for a,v in [("80","Discharge diameter DN (mm)"),("WQX","Stainless steel submersible sewage pump"),("40","Rated flow (m³/h)"),("15","Rated head (m)"),("5.5","Power (kW)")]:
    T(x0,y,a,10,"B",NAVY); T(x0+42,y,v,8,"R",TXT); y+=15
# tinh nang + ung dung
y=424; H(40,y,"FEATURES",252); H(312,y,"APPLICATION",243)
fy=y+17
for s in ["Stainless steel pump body and motor housing.","Flanged DN80 discharge.","Two lifting eyes for handling and installation.","Support stand for free-standing installation.","Supplied with power cable."]:
    T(42,fy,"•",8,"R",BLUE); T(52,fy,s,8,"R",TXT); fy+=14
T(314,y+17,"•",8,"R",BLUE); T(324,y+17,"Pumping of sewage and wastewater.",8,"R",TXT)
# bieu do Q-H
y=520; H(40,y,"PERFORMANCE CURVE",515)
L,Rr,Tp,Bt=78,520,538,676; QMAX,HMAX=90,30
X=lambda q: L+(Rr-L)*q/QMAX; Y=lambda h: Bt-(Bt-Tp)*h/HMAX
for h in range(0,31,5):
    p.draw_line((L,Y(h)),(Rr,Y(h)),color=GRID if h else LINE,width=0.5); s=str(h); T(L-6-W(s,7),Y(h)+2.5,s,7,"R",GREY)
for q in range(0,91,10):
    p.draw_line((X(q),Tp),(X(q),Bt),color=GRID if q else LINE,width=0.5)
    C(X(q),Bt+11,str(q),7,"B",NAVY); C(X(q),Bt+21,str(round(q*1000/60)),6.5,"R",GREY)
T(40,Bt+11,"Q (m³/h)",7,"B",NAVY); T(40,Bt+21,"Q (l/min)",6.5,"R",GREY)
p.insert_text((52,(Tp+Bt)/2+28),"Total head H (m)",fontname="B",fontsize=7,color=NAVY,rotate=90)
qs=np.linspace(0,80,161); pts=[pymupdf.Point(X(q),Y(Hq(q))) for q in qs]
p.draw_polyline(pts,color=BLUE,width=1.6)
for q,h in zip(QT,HT):
    if q==40: p.draw_circle((X(q),Y(h)),3,color=NAVY,fill=WHITE,width=1.2)
T(X(40)+6,Y(15)-5,"Rated point 40 m³/h – 15 m",6.5,"R",GREY)
T(X(2)+4,Y(25)-5,"80WQX40-15-5.5",7.5,"B",NAVY)
# bang du lieu
y=712; R((40,y,555,y+30),fill=NAVY)
T(48,y+12,"MODEL",7,"B",WHITE); C(156,y+12,"POWER",7,"B",WHITE)
C(140,y+24,"kW",6.5,"R",rgb("CCDDE6")); C(172,y+24,"HP",6.5,"R",rgb("CCDDE6"))
T(196,y+12,"Q",7,"B",WHITE); T(208,y+12,"m³/h",6.5,"R",rgb("CCDDE6")); T(208,y+24,"l/min",6.5,"R",rgb("CCDDE6"))
cx=[280,343,406,469,532]
for q,xx in zip(QT,cx): C(xx,y+12,str(q),7,"B",WHITE); C(xx,y+24,str(round(q*1000/60)),6.5,"R",rgb("CCDDE6"))
R((40,y+30,555,y+48),fill=LIGHT)
T(48,y+42,"80WQX40-15-5.5",8,"B",NAVY); C(140,y+42,"5.5",8,"B",NAVY); C(172,y+42,"7.5",8,"B",NAVY); T(208,y+42,"H (m)",8,"B",BLUE)
for h,xx in zip(HT,cx): C(xx,y+42,str(h),8,"B",NAVY)
p.draw_line((40,y+48),(555,y+48),color=LINE,width=0.6)
T(40,y+60,"Supply 3~ 380–415 V, 50 Hz. Rated flow and rated head according to the model designation.",6.5,"R",GREY)
p.draw_line((40,800),(555,800),color=LINE,width=0.6)
T(40,815,"PEROTAC  /  80WQX40-15-5.5",7,"B",GREY); s="01 / 01"; T(555-W(s,7),815,s,7,"R",GREY)
d.set_metadata({"title":"PEROTAC 80WQX40-15-5.5 - Stainless steel submersible sewage pump","author":"PEROTAC"})
d.save(OUT,garbage=4,deflate=True)
print(hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16], os.path.getsize(OUT))
