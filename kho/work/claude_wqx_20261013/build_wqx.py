import pymupdf, glob, os, sys, io, hashlib
from PIL import Image
K=os.path.expanduser("~/mnt/Sửa catalogue")
REF=glob.glob(K+"/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/*FC inox.pdf")[0]
PHOTO=K+"/work/claude_wqx_20261013/ANH GOC 80WQX40-15-5.5 (anh gui 13-10-2026).png"
OUT=sys.argv[1]
FR="/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
FB="/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
def rgb(h): return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
NAVY=rgb("14334D"); BLUE=rgb("1A669E"); LIGHT=rgb("EDF5FA"); GREY=rgb("5C6F7E"); TXT=rgb("1F3A4F"); LINE=rgb("C9D8E3"); WHITE=(1,1,1)
ref=pymupdf.open(REF)
# logo: lay nguyen anh goc tu catalogue FC inox da duyet (xref 15 + mat na)
lx=15; base=pymupdf.Pixmap(ref,lx)
sm=ref.xref_get_key(lx,"SMask")
if sm[0]=="xref":
    mask=pymupdf.Pixmap(ref,int(sm[1].split()[0])); base=pymupdf.Pixmap(base,mask)
logo_png=base.tobytes("png")
im=Image.open(PHOTO).convert("RGB").crop((90,270,940,1420))
b=io.BytesIO(); im.save(b,"JPEG",quality=90); photo=b.getvalue()
d=pymupdf.open(); p=d.new_page(width=595.2,height=841.92)
p.insert_font("R",fontfile=FR); p.insert_font("B",fontfile=FB)
def T(x,y,s,sz,f="R",c=TXT): p.insert_text((x,y),s,fontname=f,fontsize=sz,color=c)
def W(s,sz,f="R"): return pymupdf.Font(fontfile=FB if f=="B" else FR).text_length(s,fontsize=sz)
def R(r,fill=None,col=None,w=0.6): p.draw_rect(pymupdf.Rect(r),color=col,fill=fill,width=w)
def H(x,y,s,w):  # tieu de muc
    T(x,y,s,9,"B",BLUE); p.draw_line((x,y+4),(x+w,y+4),color=BLUE,width=0.8)
# dau trang
R((190,0,595.2,78),fill=LIGHT)
p.insert_image(pymupdf.Rect(40,16,174.5,62),stream=logo_png)
T(208,52,"80WQX",30,"B",NAVY)
s="SINGLE MODEL  /  DATA SHEET"; T(555-W(s,10,"B"),36,s,10,"B",NAVY)
s="Stainless steel submersible sewage pump"; T(555-W(s,8),52,s,8,"R",GREY)
p.draw_line((0,78),(595.2,78),color=LINE,width=0.6)
# anh
pr=pymupdf.Rect(40,98,40+252,98+252*1150/850)
p.insert_image(pr,stream=photo); R(pr,col=LINE,w=0.6)
T(40,pr.y1+12,"Actual product photo",7,"R",GREY)
# thong so chinh
x0,x1=312,555; y=106; H(x0,y,"KEY DATA",x1-x0); y+=12
rows=[("Model","80WQX40-15-5.5"),("Power","5.5 kW  /  7.5 HP"),("Power supply","3~  380–415 V  /  50 Hz"),
("Max. flow","80 m³/h  (1333 l/min)"),("Max. head","25 m"),("Rated flow","40 m³/h  (667 l/min)"),
("Rated head","15 m"),("Discharge","DN80, flanged"),("Construction","Stainless steel"),("Origin","Made in Taiwan")]
for i,(a,v) in enumerate(rows):
    if i%2==0: R((x0,y,x1,y+20),fill=LIGHT)
    T(x0+6,y+13,a,8,"R",TXT); T(x1-6-W(v,8,"B"),y+13,v,8,"B",NAVY); y+=20
y+=22; H(x0,y,"PRODUCT NOMENCLATURE",x1-x0); y+=20
for a,v in [("80","Discharge diameter DN (mm)"),("WQX","Stainless steel submersible sewage pump"),("40","Rated flow (m³/h)"),("15","Rated head (m)"),("5.5","Power (kW)")]:
    T(x0,y,a,11,"B",NAVY); T(x0+42,y,v,8,"R",TXT); y+=17
T(x0,y+2,"Example: 80WQX40-15-5.5",7,"R",GREY)
# tinh nang + ung dung
y=pr.y1+42
H(40,y,"FEATURES",252); H(312,y,"APPLICATION",243)
fy=y+18
for s in ["Stainless steel pump body and motor housing.","Flanged DN80 discharge.","Two lifting eyes for handling and installation.","Support stand for free-standing installation.","Supplied with power cable."]:
    T(42,fy,"•",8,"R",BLUE); T(52,fy,s,8,"R",TXT); fy+=16
T(314,y+18,"•",8,"R",BLUE); T(324,y+18,"Pumping of sewage and wastewater.",8,"R",TXT)
# bang du lieu
y=fy+26; H(40,y,"PERFORMANCE DATA",515); y+=12
cols=[("MODEL","",40,150),("POWER","kW",150,200),("","HP",200,245),("MAX. FLOW","m³/h",245,310),("","l/min",310,370),("MAX. HEAD","m",370,430),("RATED FLOW","m³/h",430,495),("RATED HEAD","m",495,555)]
R((40,y,555,y+34),fill=NAVY)
for a,u,l,r in cols:
    c=(l+r)/2
    if a=="POWER": c=(150+245)/2
    if a=="MAX. FLOW": c=(245+370)/2
    if a: T(c-W(a,7,"B")/2,y+13,a,7,"B",WHITE)
    if u: T((l+r)/2-W(u,7)/2,y+27,u,7,"R",rgb("CCDDE6"))
vals=["80WQX40-15-5.5","5.5","7.5","80","1333","25","40","15"]
R((40,y+34,555,y+54),fill=LIGHT)
for (a,u,l,r),v in zip(cols,vals):
    c=(l+r)/2; T(c-W(v,8,"B")/2,y+47,v,8,"B",NAVY)
p.draw_line((40,y+54),(555,y+54),color=LINE,width=0.6)
T(40,y+68,"Supply 3~ 380–415 V, 50 Hz. Rated flow and rated head according to the model designation.",7,"R",GREY)
# chan trang
p.draw_line((40,800),(555,800),color=LINE,width=0.6)
T(40,815,"PEROTAC  /  80WQX40-15-5.5",7,"B",GREY); s="01 / 01"; T(555-W(s,7),815,s,7,"R",GREY)
d.set_metadata({"title":"PEROTAC 80WQX40-15-5.5 - Stainless steel submersible sewage pump","author":"PEROTAC"})
d.save(OUT,garbage=4,deflate=True)
print(hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16], os.path.getsize(OUT))
