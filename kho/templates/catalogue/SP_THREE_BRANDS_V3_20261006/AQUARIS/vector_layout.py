"""Vector authoring helpers for the newly authorized AQUARIS design. No PDF writes here."""
from pathlib import Path
import math,html,base64
import pikepdf,fitz
from fontTools.ttLib import TTFont
W=597.9998779296875;H=852.9998779296875
INK=(.12,.19,.21);TEAL=(.05,.38,.35);MUTED=(.36,.43,.45);GRID=(.83,.88,.87);PALE=(.94,.97,.96);WHITE=(1,1,1)
F={}
for key,fn in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:
 t=TTFont('C:/Windows/Fonts/'+fn);F[key]={'tt':t,'path':Path('C:/Windows/Fonts/'+fn),'cmap':t.getBestCmap(),'up':t['head'].unitsPerEm,'used':set()}
def n(v):return f'{v:.8f}'.rstrip('0').rstrip('.') if abs(v)>1e-9 else '0'
def rgb(c,stroke=False):return ' '.join(n(v) for v in c)+(' RG' if stroke else ' rg')
def sc(c):return 'rgb('+','.join(str(round(v*255)) for v in c)+')'
def tw(s,fs,font='Body'):
 f=F[font];return sum(f['tt']['hmtx'][f['cmap'][ord(c)]][0] for c in s)*fs/f['up']
def fmt(v):
 if v is None:return '-'
 return str(v) if isinstance(v,str) else f'{v:g}'
class Page:
 def __init__(self,index):self.index=index;self.ops=['q','[] 0 d'];self.svg=[];self.texts=[];self.images=[];self.curves=[];self.tables=[]
 def text(self,s,x,y,fs=9,font='Body',color=INK,align='left',rotate=False):
  s=str(s);width=tw(s,fs,font)
  if align=='right':x-=width
  elif align=='center':x-=width/2
  if not rotate:assert x>=0 and x+width<=W+.02 and 0<y<H,(self.index,s,x,y,width)
  F[font]['used'].update(ord(c) for c in s);mat=[0,1,-1,0,x,H-y] if rotate else [1,0,0,1,x,H-y]
  self.ops.append(f'BT /AQ{font} {n(fs)} Tf {rgb(color)} '+' '.join(n(v) for v in mat)+f' Tm <{s.encode("utf-16-be").hex()}> Tj ET')
  self.texts.append({'text':s,'x':x,'y':y,'size':fs,'font':font,'width':width,'rotate':rotate})
  tr=f'translate({x},{y}) rotate(-90)' if rotate else f'translate({x},{y})'
  self.svg.append(f'<text transform="{tr}" font-family="Arial" font-size="{fs}" font-weight="'+('bold' if font=='Bold' else 'normal')+f'" fill="{sc(color)}">{html.escape(s)}</text>')
 def line(self,x,y,x2,y2,color=GRID,lw=.55):
  self.ops.append(f'{rgb(color,True)} {n(lw)} w 0 J {n(x)} {n(H-y)} m {n(x2)} {n(H-y2)} l S')
  self.svg.append(f'<path d="M{x},{y} L{x2},{y2}" stroke="{sc(color)}" stroke-width="{lw}" fill="none"/>')
 def rect(self,x,y,w,h,c):
  self.ops.append(f'{rgb(c)} {n(x)} {n(H-y-h)} {n(w)} {n(h)} re f')
  self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sc(c)}"/>')
 def curve(self,segments,X,Y,model):
  op=[rgb(TEAL,True),'0.95 w 1 J 1 j [] 0 d'];sv='';actual=[]
  for j,s in enumerate(segments):
   pts=[(X(q),Y(h)) for q,h in s];actual.append(pts)
   if j==0:op.append(f'{n(pts[0][0])} {n(H-pts[0][1])} m');sv+=f'M{pts[0][0]},{pts[0][1]} '
   op.append(' '.join(n(v) for x,y in pts[1:] for v in [x,H-y])+' c');sv+='C'+' '.join(f'{x},{y}' for x,y in pts[1:])+' '
  op.append('S');self.ops.extend(op);self.svg.append(f'<path d="{sv}" fill="none" stroke="{sc(TEAL)}" stroke-width="0.95"/>');self.curves.append({'model':model,'segments':actual,'width':.95,'color':TEAL})
 def paragraph(self,lines,x,y,width,fs=9,leading=13):
  for s in lines:
   parts=s.split();row=''
   for word in parts:
    test=(row+' '+word).strip()
    if tw(test,fs)>width and row:self.text(row,x,y,fs);y+=leading;row=word
    else:row=test
   self.text(row,x,y,fs);y+=leading
  return y
 def source_image(self,xref,x,y,w,h):self.images.append({'xref':xref,'target':[x,y,w,h]})
def embed_fonts(pdf):
 out=pikepdf.Dictionary()
 for name,f in F.items():
  t=f['tt'];up=f['up'];ff=pdf.make_stream(f['path'].read_bytes());ff.Length1=len(f['path'].read_bytes());base='ArialMT' if name=='Body' else 'Arial-BoldMT'
  desc=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.FontDescriptor,FontName=pikepdf.Name('/'+base),Flags=32,FontBBox=pikepdf.Array([getattr(t['head'],k)*1000/up for k in ['xMin','yMin','xMax','yMax']]),ItalicAngle=0,Ascent=t['hhea'].ascent*1000/up,Descent=t['hhea'].descent*1000/up,CapHeight=t['OS/2'].sCapHeight*1000/up,StemV=80,FontFile2=ff))
  gm=bytearray((max(f['used'])+1)*2);ww=pikepdf.Array()
  for code in sorted(f['used']):
   glyph=f['cmap'][code];gm[code*2:code*2+2]=t.getGlyphID(glyph).to_bytes(2,'big');ww.append(code);ww.append(pikepdf.Array([t['hmtx'][glyph][0]*1000/up]))
  cid=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font,Subtype=pikepdf.Name.CIDFontType2,BaseFont=pikepdf.Name('/'+base),CIDSystemInfo=pikepdf.Dictionary(Registry='Adobe',Ordering='Identity',Supplement=0),FontDescriptor=desc,DW=1000,W=ww,CIDToGIDMap=pdf.make_stream(bytes(gm))))
  cm=b'/CIDInit /ProcSet findresource begin 12 dict begin begincmap /CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def /CMapName /AQUCS def /CMapType 2 def 1 begincodespacerange <0000> <FFFF> endcodespacerange 1 beginbfrange <0000> <FFFF> <0000> endbfrange endcmap CMapName currentdict /CMap defineresource pop end end'
  out['/AQ'+name]=pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font,Subtype=pikepdf.Name.Type0,BaseFont=pikepdf.Name('/'+base),Encoding=pikepdf.Name('/Identity-H'),DescendantFonts=pikepdf.Array([cid]),ToUnicode=pdf.make_stream(cm)))
 return out
