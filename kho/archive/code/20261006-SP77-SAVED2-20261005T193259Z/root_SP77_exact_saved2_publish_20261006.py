"""Publish only ROOT-reviewed saved SP77 bytes, after backup and peer evidence.
No PDF authoring, Save, refitting or repeat candidate. Original taskcount holds.
"""
import argparse,json,hashlib,shutil,os,importlib.util
from pathlib import Path
from datetime import datetime,timezone
import root_SP77_final2_one_candidate_20261006 as W
from catfix.session import Session
PROJECT=W.PROJECT;R=W.R;C=W.C;sha=W.sha
REL='Giếng/Perotac bơm giếng SP_compressed (bản mới).pdf'
OLD='659f506de9a066ebc9582eeea69923157d7bd9029fedfc4a898bdbefe0baf892'
NEW='48c8535c4c8a025991be53caf414242cbb500eb43ac59f804a2008204691a6a2'
SOURCE='e1b94dc6f23c35d18d61cee71d9d88c844b1070d14ff662bbabe2256cdd690c9'
OUT=R/'SP77 SAVED2 DA LUU NGHIEM THU PHAM VI'
def stamp():return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('accept',type=Path);ap.add_argument('accept_sha');ap.add_argument('--publish',action='store_true');args=ap.parse_args()
 assert sha(args.accept)==args.accept_sha;a=W.rd(args.accept)
 assert a['allow_adopt_exact_saved_candidate']is True and a['candidate_SHA256']==NEW and a['current_before_SHA256']==OLD and a['source_SHA256']==SOURCE
 assert a['ROOT_opened_saved27']and a['keeper6_actual_pixel0']and a['outside24_actual_pixel0']and a['visual_scoped_pass']
 W.guard(a['evidence_guards']);candidate=Path(a['candidate']);assert sha(candidate)==NEW
 S=Session();ctx=C.context(REL);C.validate_context(ctx);src,cur=Path(ctx['source']),Path(ctx['current'])
 assert sha(src)==SOURCE and sha(cur)==OLD
 idx=PROJECT/'state/catalogues.json';ledger=Path(S.report('TIEN DO.md'));cp=PROJECT/'state/CURRENT_CHECKPOINT.md';seal=PROJECT/'state/control_manifest.json'
 inventory=W.rd(idx);assert inventory['catalogue_count']==25;control={str(p):sha(p)for p in(idx,ledger,cp,seal)}
 def hold(adopted=False):
  for row in inventory['catalogues']:
   assert sha(Path(S.in_dir)/row['source_relative'])==row['source_sha256']
   expected=NEW if adopted and row['source_relative']==REL else row['current_sha256']
   assert sha(Path(S.out_dir)/row['current_relative'])==expected
 def guards():
  W.guard(control);W.guard(a['evidence_guards']);assert sha(src)==SOURCE and sha(cur)==OLD and sha(candidate)==NEW and sha(args.accept)==args.accept_sha
 h=C.health();assert h['coordination_integrity']=='ok'and not h['controls']['changed']and not h['missing_paths'];hold();guards()
 assert cur.resolve().is_relative_to(Path(S.out_dir).resolve())and not cur.resolve().is_relative_to(Path(S.in_dir).resolve())
 if not args.publish:
  print(json.dumps({'status':'READONLY_PREFLIGHT_PASS','candidate_SHA256':NEW,'original137_of149_held':True,'PDF_Save':0,'canonical':0},ensure_ascii=False));return
 OUT.mkdir(exist_ok=False);tag=stamp();session='ROOT-SP77-SAVED2-'+tag;lease=C.claim(REL,'ROOT',session,'Publish exact saved48c853 SP77 P9 scoped; 0PDFSave,137of149 held',1800);adopted=False
 try:
  C.check(lease['token'],'ROOT',session);guards();backup=OUT/'BAN TRUOC'/cur.name;backup.parent.mkdir();shutil.copyfile(cur,backup);assert sha(backup)==OLD
  backups={}
  for p,name in((idx,'INDEX TRUOC.json'),(ledger,'TIEN DO TRUOC.md'),(cp,'CHECKPOINT TRUOC.md')):
   q=OUT/name;shutil.copyfile(p,q);assert sha(q)==control[str(p)];backups[str(p)]={'path':str(q),'SHA256':sha(q)}
  stage=cur.with_name('.CHATGPT_SP77_EXACT_ACCEPTED_'+tag+'.pdf');assert not stage.exists()
  assert stage.resolve().parent==cur.resolve().parent and stage.resolve().is_relative_to(Path(S.out_dir).resolve())
  with stage.open('xb')as target,candidate.open('rb')as origin:shutil.copyfileobj(origin,target)
  assert sha(stage)==NEW
  W.write(OUT/'01 BACKUP BEFORE EXACT ACCEPT.json',{'before':str(backup),'before_SHA256':OLD,'stage':str(stage),'stage_SHA256':NEW,'controls_backups':backups,'accept':str(args.accept),'accept_SHA256':args.accept_sha})
  guards();C.check(lease['token'],'ROOT',session);os.replace(stage,cur);adopted=True;assert sha(cur)==NEW;hold(True)
  note=('SP Perotac trang9 dải8SP77 đã nhận đúng bản48c8535c:15 đường cong mượt/giảm khiQ tăng, cùng màu98/108/110 và bề dày0,7773689114693686điểm với dảiSP đã đạt. '
   'Giữ56đoạn vật lý/41nốiC2;70đoạn vẽ chỉ tách chính xác tạiQ24,không khớp lại.135H được kiểm;7số trung gian giảm đúng1:Q12 của/2:40→39,/3:60→59,/4:80→79,/10:201→200,/12:241→240,/14:281→280;Q24 của/2:39→38. '
   '128H/30đầu-cuối bảng/mã/kW/HP/điện giữ;#49=175 giữ,không đếm lại.15nhãn dùng37lượt nguyênRGB ngân hàng chữ nguồn/cỡ tự nhiên;11tên ảnh mới trỏ11đối tượng cũ,0ảnh/phông/luồng mới. '
   'Mẫu1 bị loại vì4mép bảo vệ đổi; mẫu2 cuối2/2 thu mép vào trong và ngắt riêng lưới qua hộp nhãn,không phủ trắng/không dời đường/chữ/số đã chốt. '
   'ROOT mở27ảnh lưu và dựng lại27đúngRGB;tác nhân độc lập kiểm cấu trúc/số/hình.6vùng bảo vệ600 và24kiểm ngoài100/200/ngưỡng0/đệm0 đổi0.15tiết diện nét thật đo0,7684..0,7886điểm,đồng bút;không lấy ảnh thu nhỏ chứng độ dày. '
   '225đối tượng/197luồng qua quan hệ đầy đủ;196luồng RAW/mặt nạ/bộ lọc giữ,chỉ nội dung160 và11alias ởtài nguyênP9 đổi.12lệnh trang khớp;11trang khác giữ.Info/XMP/khổ/liên kết/dấu trang/phông gốc giữ. '
   'Nhận xét ban đầu vạchQ24 xuyên chữ1 đã được chẩn đoán bằng nguồn/RGB/tọa độ và đính chính;giữ phiếu cũ để truy vết,không sửaPDF thêm. '
   'Chữ bitmap nguồn còn hạt/viền màu; tên phông/ảnh hưởng pha/độ nét toàn bộ chữ CHƯA THỂ XÁC MINH. Các đầu bảng được giữ không chứng cực đại vật lý/điểm làm việc hoặc số thử nghiệm hãng. '
   '137/149việc gốc không đổi,15đường/7ô là phần mở rộng.12mãgốc vàphầnmở rộng còn;toànSP/G05/dự án CHƯA XONG.25nguồn/24kếtquảkhác giữ;sao lưu bản trước và3tệp điều phối. Tiếp nhận chỉchép đúng byte,0SavePDFmới.')
  rows=[['Mở rộng đường','Perotac SP','9 — 8SP77','15 đường ảnh cũ','15 đường giảm/mượt/cùng nét','56đoạn C2 giữ;70đoạn chỉ tách nét','ĐẠT PHẠM VI','Số học/ảnh/tệp thật độc lập'],
   ['Mở rộng bảng','Perotac SP','9','7ô trùng đầu hoặc gây bằng','39/59/79/200/240/280 và38','Mỗiô giảm1,giữ số nguyên','ĐẠT','135H;128giữ/30đầu-cuối;#49=175'],
   ['Nhãn đường','Perotac SP','9','Nhãn và nét nguồn sát nhau','15suffix dưới tiêu đề8SP77','37lượtRGB nguyên;grid riêng ngắt qua chữ','ĐẠT ĐỌC TRONG GIỚI HẠN','27ảnh/nguồn1;fringe vàphase UNKNOWN'],
   ['Bảo vệ','Perotac SP','9 và12trang','Trục/title/ETA/left/table','6keeper600/24outside100/200=0','Giữ ngưỡng0/đệm0','ĐẠT','Ownrender độc lập0/0'],
   ['Tệp thật','Perotac SP','12trang',OLD[:8],NEW[:8],'225nodes/197streams;196RAWheld','ĐẠT PHẠM VI','11aliases oldimages;metadataheld'],
   ['Mẫu lỗi','Perotac SP','9','Mẫu1 keeperFAIL','Mẫu2 là lượt cuối2/2','Inset+gridclip,không đổi bộ số/đường','LƯU BẰNG CHỨNG','Khôngthử3/khôngnới threshold'],
   ['Chữ phóng lớn','Perotac SP','9','JPEG fringe/raster nhỏ','Giữ nguyên nguồn','Không tẩy RGB hoặc nhận toàn chữ nét','CHƯA THỂ XÁC MINH','Fontname/phase/sharpening'],
   ['Tiến độ','Dự án','G05','137/149gốc','137/149gốc giữ','Phần mở rộng tính riêng','CHƯA XONG TOÀN BỘ','12mãgốc vàmở rộng còn']]
  report=OUT/'02 BAO CAO8 COT.md'
  with report.open('x',encoding='utf8')as f:f.write('# G05 — 8SP77 đã lưu và nghiệm thu đúng phạm vi\n\n| # việc | File | Trang | Cũ | Mới | Cách sửa | Kết quả | Bằng chứng |\n|---|---|---|---|---|---|---|---|\n'+''.join('| '+' | '.join(row)+' |\n'for row in rows)+'\n'+note+'\n\nQ=lưu lượng;H=cột áp;C2=nối liên tục cả hướng vàđộ cong;RGB=đỏ/lục/lam;alias=tên trỏ ảnh đãcó;keeper=vùng giữ;outside=ngoài vùng sửa;RAW=byte mãhóa gốc;phase=pha đặt điểm ảnh;fringe=viền màu;UNKNOWN=chưa thể xác minh.\n')
  pub=OUT/'03 ROOT EXACT PUBLICATION.json'
  W.write(pub,{'status':'ACCEPTED_SP77_P9_15CURVES_TABLE7_SAVED2_SCOPED_ONLY','source':str(src),'source_SHA256':SOURCE,'current':str(cur),'current_SHA256':NEW,
   'candidate':str(candidate),'candidate_SHA256':NEW,'backup':str(backup),'backup_SHA256':OLD,'accept':str(args.accept),'accept_SHA256':args.accept_sha,
   'evidence_guards':a['evidence_guards'],'report':str(report),'report_SHA256':sha(report),'original149_accepted':137,'whole_SP_complete':False,
   'source25_other24_held':True,'font_sharpness_identity_phase_UNKNOWN':True,'operations':{'exact_copy':1,'PDF_Save':0,'new_candidate':0,'marker':0}})
  S.progress('G05 — 8SP77 đường15/bảng7 đãlưu','ĐẠT PHẠM VI;137/149GIỮ;TOÀN SP CÒN',note+' Hồsơ '+str(OUT)+'.')
  spec=importlib.util.spec_from_file_location('refresh_SP77',PROJECT/'tools/refresh_index.py');ri=importlib.util.module_from_spec(spec);spec.loader.exec_module(ri)
  snap=ri.snapshot(C.manifest());assert snap['catalogue_count']==25 and all(not row['source_changed_from_initial_anchor']for row in snap['catalogues'])
  previous={row['source_relative']:row['current_sha256']for row in inventory['catalogues']}
  assert all(row['current_sha256']==(NEW if row['source_relative']==REL else previous[row['source_relative']])for row in snap['catalogues'])
  history=PROJECT/'history'/('inventory-'+tag+'-SP77.json');ri.fresh_json(history,dict(snap,actor='ROOT',reason='SP77 exact saved2 '+str(pub)));ri.replace_state(idx,snap)
  update=PROJECT/'state/updates'/('20261006-SP77-DA-LUU-'+tag+'.md')
  with update.open('x',encoding='utf8')as f:f.write('# 8SP77 đúng phạm vi đã lưu\n\n'+note+'\n\nHồ sơ: '+str(pub)+'\n\nCDX29b916d2/SL5b762e84 giữ. STOP2 SP4SP5/SLP6/6SL15 vẫn giữ,không chạy lại. DWOmin/preview/phông và12mãgốc còn. SP36/46 chỉ global-affine bế tắc; procedure dùng từngđoạn trục khôngđều,đang đọc tĩnh, chưanative/PDF.\n')
  with cp.open('a',encoding='utf8')as f:f.write('\n\n## 8SP77 đã lưu '+tag+'\n\nĐọc [mốc SP77](updates/'+update.name+') sau mốc cũ. '+note+'\n')
  knowledge=PROJECT/'knowledge'/('SP77_FINAL2_SOURCE135_TABLE7_'+tag+'.md')
  with knowledge.open('x',encoding='utf8')as f:f.write('# 8SP77 — nghiệm thu và cách tránh lỗi\n\n'+note+'\n\nBODY2sourcepixels[[1022,201,1522,592],[1522,245,1638,592]]. Không dùng mép sharedkeeper trongmẫu1[[1021,198,1523,592],[1523,244,1643,592]]. Grid ngắt nguyênhộp nhãn bằngclip15bbox+1/4pt;khôngphủtrắng. Helperclip_prefix chuyên2BODYkhôngdùngthẳngcho15gridholes;staticfailuređãgiữ trướcPDF. Source1 cóthânthẳng/viềnxám,đừngđọcnhầm thànhvạchQ24: đọc66pixel/tọađộnguồn nguyêntrongsaved. Pixeloutside/keeper0 khôngchứngfontidentity/sharpening.\n')
  assert sha(seal)==control[str(seal)];hold(True);C.validate_context(C.context(REL))
  end=OUT/'04 FINAL READBACK.json';W.write(end,{'publication':str(pub),'publication_SHA256':sha(pub),'current_SHA256':sha(cur),'source_SHA256':sha(src),
   'index_SHA256':sha(idx),'ledger_SHA256':sha(ledger),'checkpoint_SHA256':sha(cp),'control_seal_SHA256':sha(seal),
   'history':str(history),'update':str(update),'knowledge':str(knowledge),'controls_backups':backups,'source25_other24_held':True,'original149_accepted':137,
   'whole_goal_complete':False,'PDF_Save':0})
  print(json.dumps({'publication':str(pub),'publication_SHA256':sha(pub),'readback':str(end),'readback_SHA256':sha(end),'current_SHA256':sha(cur)},ensure_ascii=False))
 except Exception as e:
  W.write(OUT/'99 FAILED NO AUTO RETRY.json',{'error':repr(e),'adopted':adopted,'current_SHA256':sha(cur),'source_SHA256':sha(src),'auto_retry':False});raise
 finally:C.release(lease['token'],'ROOT',session,'SP77 publication ended '+str(OUT))
if __name__=='__main__':main()
