"""Verify full phone-download bytes against accepted local PDF and record once."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,urllib.request,shutil
P=Path(r'D:\ChatGPT\Sửa catalogue');sys.path.insert(0,str(P/'tools'));import catalogue as C
R=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05')
URL='https://at.adobe.com/rn3o0vz5LxbmEFCX';EXPECTED='48c8535c4c8a025991be53caf414242cbb500eb43ac59f804a2008204691a6a2'
def main():
 ctx=C.context('Perotac bơm giếng SP_compressed (bản mới).pdf');C.validate_context(ctx);assert ctx['current_sha256']==EXPECTED
 h=C.health();assert not h['controls']['changed']and h['coordination_integrity']=='ok'
 with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=30)as response:
  b=response.read();status=response.status;mime=response.headers.get('Content-Type','').split(';')[0]
 assert status==200 and mime=='application/pdf'and b.startswith(b'%PDF-')
 assert hashlib.sha256(b).hexdigest()==EXPECTED and b==Path(ctx['current']).read_bytes()
 assert C.context('Perotac bơm giếng SP_compressed (bản mới).pdf')==ctx
 tag=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');out=R/('SP77 GUI DIEN THOAI EXACT '+tag);out.mkdir(exist_ok=False)
 cp=P/'state/CURRENT_CHECKPOINT.md';ledger=Path(C.manifest()['paths']['progress']);seal=P/'state/control_manifest.json';before={str(p):C.digest(p)for p in(cp,ledger,seal)}
 for p,name in((cp,'CHECKPOINT TRUOC.md'),(ledger,'TIEN DO TRUOC.md')):
  q=out/name;shutil.copyfile(p,q);assert C.digest(q)==before[str(p)]
 fp=out/'01 PHONE EXACT ACCEPTED SP48 VERIFIED.json'
 z={'status':'PHONE_DOWNLOAD_EXACT_ACCEPTED_SP48_SCOPED_PASS','url':URL,'asset':'urn:aaid:sc:AP:363588b8-7419-4671-b589-d85c13673170',
  'canonical':ctx['current'],'canonical_SHA256':EXPECTED,'source':ctx['source'],'source_SHA256':ctx['source_sha256'],
  'download_SHA256':hashlib.sha256(b).hexdigest(),'download_bytes':len(b),'http_status':status,'mime':mime,'complete_bytes_equal_local':True,
  'scope':'SP P9 8SP77 fifteen smooth consistentcurves +seven integer intermediatecells;30tableends and128H held. Source rasterfringe/fontidentity/phase/sharpness UNKNOWN;wholeSP/projectunfinished.',
  'original149_accepted':137,'goal_complete':False,'authority':'Anh yêu cầu liên kết điện thoại;upload same acceptedPDF viaAdobe absolute files/no invented path;init already called earlier.',
  'operations':{'PDF_Save':0,'new_candidate':0,'canonical':0,'marker':0}}
 with fp.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 knowledge=P/'knowledge'/('SP77_GUI_DIEN_THOAI_'+tag+'.md')
 with knowledge.open('x',encoding='utf8')as f:f.write('# Perotac SP — bản48c853 đã giao điện thoại\n\n[Catalogue đã sửa]('+URL+'). Đã tải lại đủ '+str(len(b))+' byte và so toàn tệp/mã với bản chính48c853.\n\nTrang9 8SP77 có15đường mượt/đồngnét và7ô nguyên giảm1;128H/30đầu bảng giữ. Chữ nguồn còn hạt khi phóng lớn,không nhận toànfont/phase/độ nét đã đạt.137/149gốc giữ,phần mở rộng tính riêng,toànSP/dự án còn. Liên kết có thể hết hạn;filePC giữ nguyên.\n\nBằng chứng:'+str(fp)+'\n')
 from catfix.session import Session
 Session().progress('G05 SP77 giao điện thoại','137/149GIỮ;ĐÚNG BẢN48 ĐÃ ĐẠT',URL+';tải lạiHTTP200/PDF/'+str(len(b))+'byte trùngSHA48c853.ToànSP/dựán còn,chữfont/phase/sharpnessUNKNOWN;0Savecatalogue khiupload. Phiếu '+str(fp)+'.')
 with cp.open('a',encoding='utf8')as f:f.write('\n\n## SP77 đã giao điện thoại '+tag+'\n\nURL:'+URL+'.Tải lại đủ'+str(len(b))+'byte/PDF/HTTP200 trùng bản48c853. Trang9 đường15/bảng7 đã nghiệm thu;137/149gốc giữ,toànSP/dự án còn;font/phase/sharpness UNKNOWN. Hồsơ:'+str(fp)+'.\n')
 assert C.digest(seal)==before[str(seal)]and C.context('Perotac bơm giếng SP_compressed (bản mới).pdf')==ctx
 end=out/'02 SHARED READBACK.json'
 with end.open('x',encoding='utf8')as f:json.dump({'phone_receipt':str(fp),'phone_SHA256':C.digest(fp),'canonical_SHA256':C.digest(Path(ctx['current'])),
  'ledger_SHA256':C.digest(ledger),'checkpoint_SHA256':C.digest(cp),'seal_SHA256':C.digest(seal),'knowledge':str(knowledge),'new_PDF_Save':0,'wholegoal_complete':False},f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({'proof':str(fp),'SHA256':C.digest(fp),'url':URL,'download_bytes':len(b),'canonical_SHA256':EXPECTED,'shared_readback':str(end)},ensure_ascii=False))
if __name__=='__main__':main()
