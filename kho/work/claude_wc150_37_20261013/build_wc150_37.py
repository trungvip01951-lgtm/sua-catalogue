import pymupdf, os, sys, hashlib, numpy as np
K=os.path.expanduser("~/mnt/Sửa catalogue")
SRC=K+"/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm cắt rác WC.pdf"
OUT=sys.argv[1]
FR="/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"; FB="/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
fr=pymupdf.Font(fontfile=FR); fb=pymupdf.Font(fontfile=FB)
def col(i): return ((i>>16)&255)/255,((i>>8)&255)/255,(i&255)/255
NAVY=col(1258317); TXT=col(2046023); GREY=col(6057592); BLUE=col(1730206)
HEAD=(0.075,0.2,0.3); ROW=(0.93,0.96,0.98); GRID=(0.84,0.88,0.9); CURVE=(0.1,0.4,0.62); WHITE=(1,1,1); SUB=(0.8,0.867,0.902)
# du lieu 150WC300-30-37 (suy ra: quy doi dang duong 150WC200-25-22 Q x1.5, H x1.2; khoa 0/53, 300/30, 540/8)
b,c,d3=-0.06266333333333332,-5.7177777777777796e-05,3.5e-08
Hq=lambda q:53+b*q+c*q*q+d3*q**3
QT=list(range(0,541,60)); HT=[53,49,45,40,35,30,25,19,14,8]
src=pymupdf.open(SRC); doc=pymupdf.open(); doc.insert_pdf(src,from_page=0,to_page=0); doc.insert_pdf(src,from_page=5,to_page=5)
def spans(pg):
    for bl in pg.get_text("dict")["blocks"]:
        for l in bl.get("lines",[]):
            for s in l["spans"]: yield s
def put(pg,x,y,s,sz,bold=False,c=TXT,align="l"):
    f=fb if bold else fr; w=f.text_length(s,fontsize=sz)
    if align=="c": x-=w/2
    if align=="r": x-=w
    pg.insert_text((x,y),s,fontname="B" if bold else "R",fontsize=sz,color=c)
# ---- trang 1: chi doi so trang
p1=doc[0]
for s in spans(p1):
    if s["text"].strip()=="01 / 09": r1=pymupdf.Rect(s["bbox"]); o1=s["origin"]; sz1=s["size"]; c1=s["color"]
p1.add_redact_annot(r1+(-1,-1,1,1),fill=WHITE); p1.apply_redactions(images=0,graphics=0)
p1.insert_font("R",fontfile=FR); p1.insert_font("B",fontfile=FB)
put(p1,r1.x1,o1[1],"01 / 02",sz1,False,col(c1),"r")
# ---- trang 2
p=doc[1]
rep={"100":"300","10":"30","5.5":"37","5.5 – 22 kW":"37 kW","360 m³/h":"540 m³/h","44 m":"53 m","06 / 09":"02 / 02"}
todo=[]
for s in spans(p):
    t=s["text"].strip(); bb=pymupdf.Rect(s["bbox"])
    if t in rep and (bb.y0<200 or 230<bb.y0<320 or bb.y0>790) and bb.x0<1180 and not (590<bb.y0<740):
        if t in("100","10","5.5") and not (150<bb.y0<170): continue
        todo.append((bb,s["origin"],s["size"],s["color"],"Bold" in s["font"],rep[t],t))
    if bb.x0<300 and 464<bb.y0<520: todo.append((bb,None,0,0,0,None,t))
for bb,*_ in todo: p.add_redact_annot(bb+(-0.5,-0.5,0.5,0.5),fill=WHITE)
CH=pymupdf.Rect(625,96,1178,562); TB=pymupdf.Rect(38,589,1172,742)
p.add_redact_annot(CH,fill=WHITE); p.add_redact_annot(TB,fill=WHITE)
p.apply_redactions(images=0,graphics=1)
p.insert_font("R",fontfile=FR); p.insert_font("B",fontfile=FB)
for bb,o,sz,cc,bold,new,old in todo:
    if new is None: continue
    if old in("100","10","5.5"): put(p,(bb.x0+bb.x1)/2,o[1],new,sz,bold,col(cc),"c")
    elif old=="06 / 09": put(p,bb.x1,o[1],new,sz,bold,col(cc),"r")
    else: put(p,bb.x0,o[1],new,sz,bold,col(cc))
y=465.6-1.6
y+=12.4
for t in ["Three-phase: 380–415 V / 50 Hz","It can work in water containing fiber","Curve tolerance according to ISO 9906"]:
    put(p,40,y,t,8.4); y+=12.4
# ---- bieu do
L,R,T,B=737,1138,112,514; QM,HM=600,60
X=lambda q:L+(R-L)*q/QM; Y=lambda h:B-(B-T)*h/HM
for h in range(0,61,10):
    p.draw_line((L,Y(h)),(R,Y(h)),color=GRID,width=0.6); put(p,R+7,Y(h)+2.8,str(h),7.6,False,GREY)
for q in range(0,601,60):
    p.draw_line((X(q),T),(X(q),B),color=GRID,width=0.6)
    put(p,X(q),B+16,str(q),8.0,True,NAVY,"c"); put(p,X(q),B+29,str(round(q*1000/60)),7.2,False,GREY,"c")
p.draw_rect(pymupdf.Rect(L,T,R,B),color=GRID,width=0.6)
put(p,729,B+16,"Q (m³/h)",7.6,True,NAVY,"r"); put(p,729,B+29,"Q (l/min)",7.2,False,GREY,"r")
p.insert_text((652,(T+B)/2+34),"Total head H (m)",fontname="B",fontsize=8.2,color=NAVY,rotate=90)
qs=np.linspace(0,540,271); p.draw_polyline([pymupdf.Point(X(q),Y(Hq(q))) for q in qs],color=CURVE,width=1.4)
p.draw_circle((X(300),Y(30)),3.2,color=NAVY,fill=WHITE,width=1.2)
put(p,X(300)+7,Y(30)-6,"Rated point 300 m³/h – 30 m",7.4,False,GREY)
put(p,729,Y(53)+2.8,"150WC300-30-37",7.8,True,NAVY,"r")
# ---- bang du lieu
y0=592; p.draw_rect(pymupdf.Rect(40,y0,1168.2,y0+34),color=None,fill=HEAD)
put(p,142,y0+14,"MODEL",8.0,True,WHITE,"c"); put(p,90.5,y0+29,"3~  380–415 V",7.2,False,WHITE,"c"); put(p,192.5,y0+29,"1~  220–240 V",7.2,False,WHITE,"c")
put(p,278,y0+14,"P",8.6,True,WHITE,"l"); p.insert_text((284,y0+17),"2",fontname="B",fontsize=5.8,color=WHITE)
put(p,261,y0+29,"kW",7.2,False,WHITE,"c"); put(p,295,y0+29,"HP",7.2,False,WHITE,"c")
put(p,321.5,y0+21,"Q",8.6,True,WHITE,"c"); put(p,346,y0+14,"m³/h",7.0,False,WHITE,"c"); put(p,346,y0+29,"l/min",7.0,False,WHITE,"c")
cx=[389+i*(1137-389)/9 for i in range(10)]
for q,x in zip(QT,cx): put(p,x,y0+14,str(q),8.0,True,WHITE,"c"); put(p,x,y0+29,str(round(q*1000/60)),7.2,False,SUB,"c")
ry=y0+34; p.draw_rect(pymupdf.Rect(40,ry,1168.2,ry+16),color=None,fill=ROW)
put(p,90.5,ry+11,"150WC300-30-37",8.0,True,TXT,"c"); put(p,192.5,ry+11,"–",8.0,False,GREY,"c")
put(p,261,ry+11,"37",8.0,False,TXT,"c"); put(p,295,ry+11,"50",8.0,False,TXT,"c"); put(p,335,ry+11,"H (m)",8.0,True,BLUE,"c")
for h,x in zip(HT,cx): put(p,x,ry+11,str(h),8.0,False,TXT,"c")
p.draw_line((40,ry+16),(1168.2,ry+16),color=GRID,width=0.6)
doc.set_metadata({"title":"PEROTAC 150WC300-30-37 - Submersible sewage pump with cutter","author":"PEROTAC"})
doc.save(OUT,garbage=4,deflate=True)
print(hashlib.sha256(open(OUT,"rb").read()).hexdigest()[:16],os.path.getsize(OUT))
