"""Complete shared recording from the already verified phone byte receipt.
Explicit bookkeeping recovery only; no re-upload, re-download or PDF mutation.
"""
import json
from pathlib import Path
import root_SP77_final2_one_candidate_20261006 as W
from catfix.session import Session
D=W.R/'SP77 GUI DIEN THOAI EXACT 20261005T192655Z';P=W.PROJECT
def main():
 fp=D/'01 PHONE EXACT ACCEPTED SP48 VERIFIED.json';z=W.rd(fp);C=W.C;ctx=C.context('Perotac bơm giếng SP_compressed (bản mới).pdf');C.validate_context(ctx)
 assert z['complete_bytes_equal_local']is True and z['download_SHA256']==z['canonical_SHA256']==ctx['current_sha256']=='48c8535c4c8a025991be53caf414242cbb500eb43ac59f804a2008204691a6a2'
 assert z['source_SHA256']==ctx['source_sha256']and z['url']=='https://at.adobe.com/rn3o0vz5LxbmEFCX'
 ledger=Path(C.manifest()['paths']['progress']);cp=P/'state/CURRENT_CHECKPOINT.md';seal=P/'state/control_manifest.json';sealed=W.sha(seal)
 assert W.sha(ledger)==W.sha(D/'TIEN DO TRUOC.md')and W.sha(cp)==W.sha(D/'CHECKPOINT TRUOC.md')
 assert not (D/'02 SHARED READBACK.json').exists()
 W.write(D/'99 BOOKKEEPING IMPORT FAILURE RECOVERY.json',{'original_error':'ModuleNotFoundError: No module named catfix after verified phone receipt and knowledge written',
  'verified_receipt':str(fp),'verified_receipt_SHA256':W.sha(fp),'download_verified_before_error':True,
  'PDF_or_canonical_affected':False,'ledger_checkpoint_before_error_held':True,'recovery':'Load existing configured CATFIX package through reviewed writer, then finish ledger/checkpoint once. No upload/download/Save repeated.'})
 knowledge=P/'knowledge/SP77_GUI_DIEN_THOAI_20261005T192655Z.md';assert knowledge.exists()
 Session().progress('G05 SP77 giao điện thoại','137/149GIỮ;ĐÚNG BẢN48 ĐÃ ĐẠT',z['url']+';tải lại HTTP200/PDF/'+str(z['download_bytes'])+'byte trùng SHA48c853. Toàn SP/dự án còn,chữ/phông/pha/độ nét chưa xác minh;0Save catalogue khi upload. Phiếu '+str(fp)+'.')
 with cp.open('a',encoding='utf8')as f:f.write('\n\n## SP77 đã giao điện thoại 20261005T192655Z\n\nURL:'+z['url']+'. Tải lại đủ '+str(z['download_bytes'])+'byte/PDF/HTTP200 trùng bản48c853. Trang9 đường15/bảng7 đã nghiệm thu;137/149gốc giữ,toànSP/dự án còn;phông/pha/độ nét chưa xác minh. Hồsơ:'+str(fp)+'. Lỗi nhập thư viện sau tải đã phục hồi riêng khâu ghi sổ,không lặp upload/tải hay sửaPDF.\n')
 assert W.sha(seal)==sealed and C.context('Perotac bơm giếng SP_compressed (bản mới).pdf')==ctx
 q=D/'02 SHARED READBACK.json';W.write(q,{'phone_receipt':str(fp),'phone_SHA256':W.sha(fp),'canonical_SHA256':ctx['current_sha256'],
  'ledger_SHA256':W.sha(ledger),'checkpoint_SHA256':W.sha(cp),'seal_SHA256':sealed,'knowledge':str(knowledge),'knowledge_SHA256':W.sha(knowledge),
  'explicit_bookkeeping_recovery_only':True,'PDF_Save':0,'upload_repeated':0,'download_repeated':0,'wholegoal_complete':False})
 print(json.dumps({'proof':str(fp),'SHA256':W.sha(fp),'url':z['url'],'download_bytes':z['download_bytes'],'shared_readback':str(q),'shared_SHA256':W.sha(q)},ensure_ascii=False))
if __name__=='__main__':main()
