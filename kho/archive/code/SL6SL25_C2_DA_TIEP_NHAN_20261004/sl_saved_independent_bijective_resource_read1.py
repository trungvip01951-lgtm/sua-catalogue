"""Actual saved SL graph readback: no mutation/Editor/render/save."""
import os
for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS"):os.environ[k]="1"
from pathlib import Path
import hashlib,json,zlib,sys,io,datetime,uuid,csv
from decimal import Decimal
import pikepdf
from PIL import Image
PKG=Path(r"D:\ChatGPT\Sửa catalogue\vendor\catfix_original\GOI_SUA_CATALOGUE_CHATGPT")
sys.path.insert(0,str(PKG))
from catfix.pdfdoc import decode_stream
R=Path(r"C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04")
PF=R/"SL PATCH39 40 SOURCE REPLAY PURE GRAFT PREFLIGHT 20261004T040113Z-a78e5e"/"05 PURE SOURCE39 40 STREAMS CURRENT BASE WRITER PREFLIGHT.json"
F5=R/"ROOT SL SAME M2 ACTUAL39 40 RAW MASK FREEZE 20261004T040340Z-2d253e"/"05 ACTUAL SAME SL M2 PATCH39 40 RAW SMASK FROZEN.json"
DIR=R/"ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE 20261004T041608Z-5ddd0c"
SAVED=DIR/"Redpump gieng SL_compressed (bản mới).pdf"
FAIL=DIR/"99 FAILURE RETAIN SAMPLE DO NOT AUTOMATICALLY RETRY.json"
EXPECTED_SHA="ddb0bc676409b0078e62a8ed44ece585bc2e6bba3ae3a4fac3f2ece5ef85a0ae"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def shab(b):return hashlib.sha256(b).hexdigest()
def jf(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def py(v):
 if isinstance(v,pikepdf.Name):return str(v)[1:]
 if isinstance(v,pikepdf.Array):return [py(x) for x in v]
 if isinstance(v,(pikepdf.Dictionary,pikepdf.Stream)):return {str(k)[1:]:py(x) for k,x in v.items()}
 if isinstance(v,pikepdf.String):return bytes(v)
 if isinstance(v,Decimal):return float(v)
 return v
def kind(v):
 if isinstance(v,pikepdf.Stream):return "Stream"
 if isinstance(v,pikepdf.Dictionary):return "Dictionary"
 if isinstance(v,pikepdf.Array):return "Array"
 if isinstance(v,pikepdf.Name):return "Name"
 if isinstance(v,pikepdf.String):return "String"
 if v is None:return "Null"
 if isinstance(v,bool):return "Boolean"
 if isinstance(v,int):return "Integer"
 if isinstance(v,(Decimal,float)):return "Real"
 return type(v).__name__
def atom(v):
 k=kind(v)
 if k=="String":return {"String_hex":bytes(v).hex()}
 if k=="Name":return {"Name":str(v)}
 if k=="Real":return {"Real":str(v.normalize() if isinstance(v,Decimal) else Decimal(str(v)).normalize())}
 return {k:v}
def brief(v):
 k=kind(v)
 if k in ("Dictionary","Stream"):return {"kind":k,"ref":list(v.objgen),"keys":sorted(str(x) for x in v)}
 if k=="Array":return {"kind":k,"length":len(v)}
 return atom(v)
def decoded(s):
 raw=s.read_raw_bytes()
 stage,left,_=decode_stream(raw,py(s.get("/Filter")),py(s.get("/DecodeParms")))
 if left:
  assert [str(x) for x in left] in (["DCTDecode"],["DCT"]),left
  with Image.open(io.BytesIO(stage)) as im:
   color=py(s.get("/ColorSpace"))
   # ICCBased remains an Array whose ICC stream and all fields are checked
   # by the typed graph. Decode JPEG in its native mode; do not collapse
   # the ColorSpace Array into a device-space Name to pass the comparison.
   mode={"DeviceRGB":"RGB","DeviceGray":"L","DeviceCMYK":"CMYK"}.get(color,im.mode) if isinstance(color,str) else im.mode
   pix=im.convert(mode).tobytes()
  return {"raw_SHA256":shab(raw),"nonimage_decoded_SHA256":shab(stage),"fully_decoded_SHA256":shab(pix),
          "raw_bytes":len(raw),"fully_decoded_bytes":len(pix),"remaining_image_filters":left,
          "pixel_decode":"Pillow JPEG"}
 return {"raw_SHA256":shab(raw),"nonimage_decoded_SHA256":shab(stage),"fully_decoded_SHA256":shab(stage),
         "raw_bytes":len(raw),"fully_decoded_bytes":len(stage),"remaining_image_filters":[],
         "pixel_decode":"Non-image stream filters fully decoded"}

class Compare:
 def __init__(self,label,old,new,expected_native=None,newnames=None):
  self.label=label;self.old=old;self.new=new;self.expected_native=expected_native;self.newnames=newnames or set()
  self.map={};self.rev={};self.seen=set();self.errors=[];self.streams=[];self.nodes=0;self.changedrefs=[]
  self.oldpages={p.obj.objgen:i for i,p in enumerate(old.pages)} if old else {}
  self.extra_seen=set()
 def err(self,path,why,a,b):self.errors.append({"path":path,"why":why,"old":brief(a),"actual":brief(b)})
 def walk(self,a,b,path,page=None):
  ka,kb=kind(a),kind(b)
  if ka!=kb:self.err(path,"TYPED_NODE_KIND_CHANGED",a,b);return
  ai=getattr(a,"is_indirect",False);bi=getattr(b,"is_indirect",False)
  if ai!=bi:self.err(path,"INDIRECTNESS_CHANGED",a,b)
  if ai and bi:
   ar,br=a.objgen,b.objgen
   if ar in self.map and self.map[ar]!=br:self.err(path,"OLD_REF_ALIASED_TO_TWO_ACTUAL_REFS",a,b);return
   if br in self.rev and self.rev[br]!=ar:self.err(path,"TWO_OLD_REFS_MERGED_ACTUAL_ALIAS_CHANGED",a,b);return
   self.map[ar]=br;self.rev[br]=ar
   if ar!=br:self.changedrefs.append({"path":path,"oldRef":list(ar),"actualRef":list(br)})
   if ar in self.oldpages:page=self.oldpages[ar]
   if (ar,br) in self.seen:return
   self.seen.add((ar,br))
  self.nodes+=1
  if ka in ("Dictionary","Stream"):
   ak,bk=set(a.keys()),set(b.keys())
   expanded=(self.label=="CURRENT" and page==9 and path.endswith("/Resources/XObject"))
   if expanded:
    expected=ak|{"/"+n for n in self.newnames}
    if bk!=expected:self.err(path,"EXPANDED_XOBJECT_KEYS_DIFFER_EXPECTED38",a,b)
    self.extra_seen={str(x)[1:] for x in bk-ak}
   elif ak!=bk:self.err(path,"DICTIONARY_KEYS_CHANGED",a,b)
   content10=(self.label=="CURRENT" and ka=="Stream" and a.objgen==(105,0))
   for k in sorted(ak & bk):
    if content10 and str(k)=="/Length":continue
    self.walk(a[k],b[k],path+str(k),page)
   if ka=="Stream":
    try:
     da,db=decoded(a),decoded(b)
     if content10:
      expectedraw=zlib.compress(self.expected_native)
      eq=(b.read_bytes()==self.expected_native and b.read_raw_bytes()==expectedraw)
      if not eq:self.err(path,"PAGE10_CONTENT_NOT_EXPECTED_FROZEN_NATIVE_OR_API_RAW",a,b)
      self.streams.append({"path":path,"oldRef":list(a.objgen),"actualRef":list(b.objgen),
         "authorized_delta":"ONLY current page10 Contents105 replaced by native7184 via CATFIX set_stream",
         "expected_native_SHA256":shab(self.expected_native),"old":da,"actual":db,
         "actual_raw_equals_CATFIX_zlib_compress":b.read_raw_bytes()==expectedraw,
         "actual_native_byte_exact":b.read_bytes()==self.expected_native})
     else:
      if da!=db:self.err(path,"OLD_RESOURCE_STREAM_RAW_OR_DECODED_CHANGED",a,b)
      self.streams.append({"path":path,"oldRef":list(a.objgen),"actualRef":list(b.objgen),"old":da,"actual":db,
                           "raw_and_decoded_exact":da==db,"dictionary_typed_exact_after_bijective_ref_mapping":True})
    except Exception as e:
     self.errors.append({"path":path,"why":"STREAM_DECODER_FAILED","error":repr(e)})
  elif ka=="Array":
   if len(a)!=len(b):self.err(path,"ARRAY_LENGTH_CHANGED",a,b)
   for i,(x,y) in enumerate(zip(a,b)):self.walk(x,y,path+"["+str(i)+"]",page)
  elif atom(a)!=atom(b):self.err(path,"TYPED_LEAF_VALUE_CHANGED",a,b)

def frozen_check(saved,freeze,old_actual_targets):
 errors=[];rows=[];refmap={};rev={};actualtargets=set()
 for resource in freeze["resources2"]:
  name=resource["resource_name"];s=saved.pages[9].Resources.XObject["/"+name];im,mask=resource["parts"]
  assert im["dictionary"]["SMask"]==mask["ref"]
  for expected,stream in [(im,s),(mask,s.SMask)]:
   oldref=tuple(expected["ref"]);actualref=stream.objgen
   if oldref in refmap and refmap[oldref]!=actualref:errors.append({"name":name,"why":"FROZEN_ALIAS_SPLIT"})
   if actualref in rev and rev[actualref]!=oldref:errors.append({"name":name,"why":"FROZEN_NEW_REFS_MERGED"})
   if actualref in old_actual_targets:errors.append({"name":name,"why":"NEW_FROZEN_IMAGE_ALIASES_OLD_RESOURCE"})
   refmap[oldref]=actualref;rev[actualref]=oldref;actualtargets.add(actualref)
   ed=expected["dictionary"];actualkeys={str(x)[1:] for x in stream.keys()}
   if set(ed)!=actualkeys:errors.append({"name":name,"role":expected["role"],"why":"FROZEN_DICTIONARY_KEYS_CHANGED","expected":sorted(ed),"actual":sorted(actualkeys)})
   for key,v in ed.items():
    if key=="SMask":
     if stream.SMask.objgen!=tuple(refmap.get(tuple(v),s.SMask.objgen)):errors.append({"name":name,"why":"SMASK_REF_EDGE_CHANGED"})
    elif key in ("Type","Subtype","ColorSpace","Filter"):
     if kind(stream["/"+key])!="Name" or str(stream["/"+key])!="/"+v:
      errors.append({"name":name,"key":key,"why":"NAME_TYPE_OR_VALUE_CHANGED"})
    elif kind(stream["/"+key])!="Integer" or stream["/"+key]!=v:
     errors.append({"name":name,"key":key,"why":"INTEGER_TYPE_OR_VALUE_CHANGED"})
   raw=Path(expected["raw_path"]).read_bytes();actualraw=stream.read_raw_bytes();dec=zlib.decompress(actualraw)
   if raw!=actualraw:errors.append({"name":name,"role":expected["role"],"why":"FROZEN_RAW_PAYLOAD_CHANGED"})
   if shab(dec)!=expected["decoded_SHA256"]:errors.append({"name":name,"role":expected["role"],"why":"FROZEN_DECODED_PAYLOAD_CHANGED"})
   rows.append({"name":name,"role":expected["role"],"frozenRef":list(oldref),"actualRef":list(actualref),
      "raw_frozen_SHA256":expected["raw_SHA256"],"raw_actual_SHA256":shab(actualraw),"decoded_frozen_SHA256":expected["decoded_SHA256"],
      "decoded_actual_SHA256":shab(dec),"dictionary_names_and_types_preserved":True,"mask_alias_edge":list(s.SMask.objgen) if expected["role"]=="image" else None})
 return errors,rows,refmap,actualtargets
def main():
 p=jf(PF);freeze=jf(F5)
 assert sha(SAVED)==EXPECTED_SHA
 assert sha(PF)=="69ab555f9d7dd779098a438e8a5840ea9629c919c84e1a885b807b44d577d19f"
 assert sha(F5)=="63557e637dc38ba23c22aa761f39e5d5f201509ca54bbbf783ac352763f6c0f5"
 paths=[PF,F5,SAVED,FAIL,Path(__file__),Path(p["current"]),Path(p["source"]),Path(p["donor_M2"]),Path(p["native"]),PKG/"catfix/pdfdoc.py"]
 paths.extend(Path(x["raw_path"]) for r in freeze["resources2"] for x in r["parts"])
 before={str(x):sha(x) for x in paths}
 for key in ("current","source","donor_M2","native"):assert before[p[key]]==p[key+"_SHA256"]
 native=Path(p["native"]).read_bytes();assert shab(native)=="7184d01f463d8eccfd5d1a85893850b7fd6d285f2d7c0edc36cf0ec8208606ee"
 newnames={"CfxPatch"+str(i) for i in range(3,41)}
 with pikepdf.Pdf.open(p["current"]) as old,pikepdf.Pdf.open(SAVED) as actual,pikepdf.Pdf.open(p["donor_M2"]) as donor:
  assert len(old.pages)==len(actual.pages)==len(donor.pages)==11
  C=Compare("CURRENT",old,actual,native,newnames)
  C.walk(old.Root,actual.Root,"Root")
  if ("/Info" in old.trailer)!=("/Info" in actual.trailer):C.err("Trailer/Info","INFO_PRESENCE_CHANGED",old.trailer.get("/Info"),actual.trailer.get("/Info"))
  if "/Info" in old.trailer:C.walk(old.trailer.Info,actual.trailer.Info,"Trailer/Info")
  assert C.extra_seen==newnames
  missing=Compare("DONOR_M2_NEW36",None,None)
  for i in range(3,39):
   name="/CfxPatch"+str(i)
   missing.walk(donor.pages[9].Resources.XObject[name],actual.pages[9].Resources.XObject[name],"Donor"+name)
  overlap=set(missing.rev)&set(C.rev)
  if overlap:missing.errors.append({"why":"NEW36_ALIAS_OLD_RESOURCE","actualRefs":[list(x) for x in sorted(overlap)]})
  frozenerrors,frozenrows,frozenmaps,frozentargets=frozen_check(actual,freeze,set(C.rev))
  if frozentargets&set(missing.rev):frozenerrors.append({"why":"FROZEN39_40_ALIAS_DONOR36","actualRefs":[list(x) for x in sorted(frozentargets&set(missing.rev))]})
  page_summary=[]
  for i,(a,b) in enumerate(zip(old.pages,actual.pages)):
   refs=lambda x:([x.obj.Contents] if isinstance(x.obj.Contents,pikepdf.Stream) else list(x.obj.Contents))
   ar,br=refs(a),refs(b);assert len(ar)==len(br)
   achunk=b"\n".join(x.read_bytes() for x in ar);bchunk=b"\n".join(x.read_bytes() for x in br)
   page_summary.append({"page":i+1,"old_pageRef":list(a.obj.objgen),"actual_pageRef":list(b.obj.objgen),
      "oldContentsRefs":[list(x.objgen) for x in ar],"actualContentsRefs":[list(x.objgen) for x in br],
      "old_native_SHA256":shab(achunk),"actual_native_SHA256":shab(bchunk),
      "native_exact":achunk==bchunk,"p10_native_frozen_exact":bchunk==native if i==9 else None,
      "literalRefs_exact":[x.objgen for x in ar]==[x.objgen for x in br]})
  assert all(x["native_exact"] for x in page_summary if x["page"]!=10)
  assert page_summary[9]["p10_native_frozen_exact"]
  oldobjrefs={o.objgen for o in old.objects if getattr(o,"is_indirect",False)}
  actualobjrefs={o.objgen for o in actual.objects if getattr(o,"is_indirect",False)}
  trailer_diag=[]
  for key in sorted(set(old.trailer)|set(actual.trailer)):
   if key in ("/Root","/Info"):continue
   a,b=old.trailer.get(key),actual.trailer.get(key)
   def simple(v):
    if isinstance(v,pikepdf.Array):return [simple(x) for x in v]
    if isinstance(v,(pikepdf.Dictionary,pikepdf.Stream)):return {str(k):simple(x) for k,x in v.items()}
    return atom(v)
   if simple(a)!=simple(b):trailer_diag.append({"key":key,"old":simple(a),"actual":simple(b)})
  errors=C.errors+missing.errors+frozenerrors
  all_actual_mapped=set(C.rev)|set(missing.rev)|frozentargets
  if all_actual_mapped!=actualobjrefs:
   errors.append({"why":"SAVED_OBJECT_COVERAGE_INCOMPLETE_OR_EXTRA_OBJECTS",
     "actual_uncovered":[list(x) for x in sorted(actualobjrefs-all_actual_mapped)],
     "mapped_not_in_saved":[list(x) for x in sorted(all_actual_mapped-actualobjrefs)]})
  if oldobjrefs!=set(C.map):
   errors.append({"why":"OLD_OBJECT_COVERAGE_INCOMPLETE","old_uncovered":[list(x) for x in sorted(oldobjrefs-set(C.map))]})
  if errors:
   status="FAIL_ACTUAL_DATA_OR_TYPED_RESOURCE_CHANGE"
  else:status="PASS_SEMANTIC_OLD_RESOURCE_RAW_GRAPH_AND_EXPECTED_NEW38_ONLY_LITERAL_REF_FAIL"
  oldrefchanges=sorted(C.map.items())
  assert len(C.map)==len(C.rev)
  literal_resource_ref_FAIL=any(a!=b for a,b in C.map.items())
  assert literal_resource_ref_FAIL
  snapshot={"old_pdf_object_count":len(oldobjrefs),"actual_pdf_object_count":len(actualobjrefs),
            "old_Root_Info_reachable_indirect_nodes_checked":len(C.map),
            "old_unreachable_indirect_objects_outside_resource_structural_scope":[list(x) for x in sorted(oldobjrefs-set(C.map))],
            "new38_M2_unique_indirect_nodes":len(missing.map),"new39_40_unique_indirect_nodes":len(frozenmaps)}
  snapshot["all_saved_indirect_objects_exactly_classified_as_old_or_expected_new50"]=all_actual_mapped==actualobjrefs
 for f,h in before.items():assert sha(f)==h,f
 out=R/("DOC LAP SL SAVED BIJECTION RAW GRAPH STRICTREF FAIL "+datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
 result={"status":status,"candidate":str(SAVED),"candidate_sha256":EXPECTED_SHA,"input_hashes_before_after_held":before,
   "strict_literal_numeric_Ref_gate":"FAIL_RETAINED","semantic_current_ref_bijection_complete":not C.errors,
   "oldRef_to_actualRef_one_to_one":[{"old":list(a),"actual":list(b)} for a,b in oldrefchanges],
   "reverse_bijection_one_to_one":len(C.map)==len(C.rev),"aliases_and_shared_edges_preserved":not C.errors,
   "actual11_page_readback":page_summary,"typed_nodes_compared":C.nodes,"old_current_streams_checked":C.streams,
   "new36_M2_ref_bijection":[{"M2":list(a),"actual":list(b)} for a,b in sorted(missing.map.items())],
   "new36_M2_typed_nodes_compared":missing.nodes,"new36_M2_raw_decoded_stream_checks":missing.streams,
   "actual39_40_frozen_raw_decoded_dictionary_filter_SMasks":frozenrows,
   "all_errors":errors,"snapshot_scope_counts":snapshot,"trailer_deltas_recorded_not_called_old_resource_deltas":trailer_diag,
   "no_Filter_array_scalar_normalization":True,"source_current_readback_held":True,
   "declared_authorized_changes_only":["page10 direct Resources/XObject exactly38 new named images3..40","page10 Contents105 logical content replaced by native7184 via exact CATFIX zlib encoding"],
   "Info_XMP_Root_pageboxes_links_toc_metadata_typed_graph_checked":True,
   "saved_graphics_and_saved_outside_pixels":"NOT_RUN_BY_THIS_VERIFIER_ROOT_SEPARATE",
   "old_frame150_200_FAIL":"RETAINED_UNCHANGED_NOT_CONVERTED_TO_ZERO","full_G04_complete":False,
   "Editor_RAM_graft_save_render_called":False,"canonical_ledger_index_written":False,
   "acceptance_boundary":"Only semantic resources/raw/typed aliases and explicit expected new content/images if noerrors. Numeric literalRef gate remainsFAIL. No unconditional canonical acceptance."}
 result["supersedes_initial_decoder_issue_receipt"]={"prior_SHA256":"41b23cbc6d9bf165e5229c8663850e581c4a4241dc10be4339137fd7862a8bfd",
    "reader_correction":"13 JPEG images use ICCBased Array ColorSpace; preserve the typed Array/profile graph and decode JPEG in its native mode. Initial reader failed because it used a list as a Python dict lookup key, not because image data changed."}
 jp=out/"01 SL SAVED ACTUAL REF BIJECTION DICT RAW DECODED NEW38.json"
 with jp.open("x",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
 cp=out/"02 MAP OLDREF ACTUALREF.csv"
 with cp.open("x",encoding="utf-8-sig",newline="") as f:
  w=csv.writer(f);w.writerow(["old_object","old_generation","actual_object","actual_generation"])
  for a,b in oldrefchanges:w.writerow([*a,*b])
 md=out/"03 KET LUAN SL SAVED GIU FAIL REF SO.md"
 md.write_text(status+"\n\n"
   "Đã đọc trực tiếp current và tệp lưu thật, lập ánh xạ đối tượng hai chiều và so mọi kiểu dữ liệu/thuộc tính/bộ lọc/tham số giải mã/nội dung nén/giải mã trong graph Root/11trang/Resources/Info/XMP. "
   "38 ảnh mới được so với36ảnh M2 và2ảnh39/40 đóng băng; không đổi mảng bộ lọc thành tên đơn để cho qua.\n\n"
   "Kiểm số đối tượng nguyên dạng vẫn CHƯA ĐẠT. Hiển thị và ngoài vùng thay đổi của tệp lưu thật do ROOT kiểm riêng. "
   "Không lưu/sửa PDF, không thay bản chính hay tiến độ. Chưa nhận toàn G04.\n\n"
   "Số lỗi dữ liệu/cấu trúc thật phát hiện: "+str(len(errors))+".\n"
   "SHA-256 JSON: "+sha(jp)+"\n",encoding="utf-8")
 man=out/"04 MANIFEST.json";man.write_text(json.dumps({"files":[{"path":str(x),"sha256":sha(x)} for x in [jp,cp,md]],"candidate_sha256":EXPECTED_SHA},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 assert jf(jp)==result
 print(json.dumps({"report":str(jp),"sha256":sha(jp),"manifest_sha256":sha(man),"status":status,
     "errors":errors[:15],"error_count":len(errors),"oldRef_nodes":len(C.map),"changed_oldRefs":sum(a!=b for a,b in C.map.items()),
     "old_streams":len(C.streams),"new36streamnodes":len(missing.streams),"frozen4":len(frozenrows),
     "trailer_diag":trailer_diag,"snapshot_counts":snapshot},ensure_ascii=False))
if __name__=="__main__":main()
