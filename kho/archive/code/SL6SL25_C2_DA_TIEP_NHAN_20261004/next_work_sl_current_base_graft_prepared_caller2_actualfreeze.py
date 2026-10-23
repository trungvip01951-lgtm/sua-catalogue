"""Prepared CATFIX RAM caller2 using actual frozen RGB+SMask39/40 only.

Import-safe; NO PDF save, CLI, main, render or Editor. Caller1 remains frozen.
ROOT supplies its reviewed RAM gate and owns/closes the returned current Doc.
"""
from pathlib import Path
import hashlib,json,sys,zlib,copy

PREFLIGHT=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\SL PATCH39 40 SOURCE REPLAY PURE GRAFT PREFLIGHT 20261004T040113Z-a78e5e\05 PURE SOURCE39 40 STREAMS CURRENT BASE WRITER PREFLIGHT.json')
PRE_SHA='69ab555f9d7dd779098a438e8a5840ea9629c919c84e1a885b807b44d577d19f'
HELPER_SHA='ec2812866822ff6f919d86b00fd471c946642f9aac26bc9f5d9aacff15596178'
FREEZE05=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\ROOT SL SAME M2 ACTUAL39 40 RAW MASK FREEZE 20261004T040340Z-2d253e\05 ACTUAL SAME SL M2 PATCH39 40 RAW SMASK FROZEN.json')
F05_SHA='63557e637dc38ba23c22aa761f39e5d5f201509ca54bbbf783ac352763f6c0f5'
FREEZE06=FREEZE05.with_name('06 ROOT NORMALIZED FREEZE READBACK NO REBUILD.json')
F06_SHA='240e267aa6f3ba8a0b7301a193c6b6308fb4375f170ff61a96ba1e1349e299a7'
PKG=Path(r'D:\ChatGPT\Sửa catalogue\vendor\catfix_original\GOI_SUA_CATALOGUE_CHATGPT')
API_SHA='b63ff57761f41174e9c493b3ddc51a0e73da02a5b55892e3568503407cf43853'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read_actual_patches(p):
    """Read/validate only. Compare source recipe bins byte-for-byte too."""
    assert sha(FREEZE05)==F05_SHA and sha(FREEZE06)==F06_SHA
    f5=json.loads(FREEZE05.read_text(encoding='utf-8'));f6=json.loads(FREEZE06.read_text(encoding='utf-8'))
    assert f6['status']=='PASS_NORMALIZED_JSON_AND_ACTUAL_RAW_DECODED_RESOURCE_READBACK'
    assert f6['actual_freeze']==str(FREEZE05) and f6['actual_freeze_sha256']==F05_SHA
    assert f6['same_native_sha256']==f5['same_native_SHA256']==p['native_SHA256']
    assert f5['resources2']==f6['resources2'] and f5['PDF_saves']==f6['PDF_saves']==0
    assert [e['resource_name'] for e in f6['resources2']]==['CfxPatch39','CfxPatch40']
    replay={e['name']:e for e in p['patches']};patches=[];evidence=[]
    for e in f6['resources2']:
        parts={z['role']:z for z in e['parts']};assert set(parts)=={'image','SMask'}
        im,sm=parts['image'],parts['SMask'];di,ds=im['dictionary'],sm['dictionary']
        common={'Type','Subtype','Width','Height','ColorSpace','BitsPerComponent','Length','Filter'}
        assert set(di)==common|{'SMask'} and set(ds)==common
        assert di['Type']==ds['Type']=='XObject' and di['Subtype']==ds['Subtype']=='Image'
        assert di['BitsPerComponent']==ds['BitsPerComponent']==8 and di['Filter']==ds['Filter']=='FlateDecode'
        assert di['ColorSpace']=='DeviceRGB' and ds['ColorSpace']=='DeviceGray'
        assert (di['Width'],di['Height'])==(ds['Width'],ds['Height'])
        assert di['SMask']==sm['ref'] and len(im['ref'])==len(sm['ref'])==2
        w,h=di['Width'],di['Height'];name=e['resource_name'];old=replay[name]
        assert (w,h)==(old['width'],old['height'])
        q={'name':name,'width':w,'height':h,'actual_frozen_image_dictionary':di,'actual_frozen_SMask_dictionary':ds}
        for role,encoded,decoded,n in [('image','RGB_raw','pixels',3),('SMask','SMask_raw','alpha',1)]:
            z=parts[role];rawp=Path(z['raw_path']);assert sha(rawp)==z['raw_SHA256']
            raw=rawp.read_bytes();assert len(raw)==z['raw_bytes']==z['dictionary']['Length']
            dec=zlib.decompress(raw);assert len(dec)==z['decoded_bytes']==w*h*n
            assert hashlib.sha256(dec).hexdigest()==z['decoded_SHA256']
            assert sha(old[encoded+'_file'])==old[encoded+'_SHA256']==z['raw_SHA256']
            assert Path(old[encoded+'_file']).read_bytes()==raw
            assert old[decoded+'_SHA256']==z['decoded_SHA256']
            q[encoded]=raw;q[encoded+'_SHA256']=z['raw_SHA256'];q[decoded+'_SHA256']=z['decoded_SHA256']
        patches.append(q)
        evidence.append({'name':name,'image_ref_actual_freeze':im['ref'],'SMask_ref_actual_freeze':sm['ref'],
            'actual_RAM_image_and_SMask_raw_both_exact_to_source_recipe_replay':True,'dimension_dictionary_Filter_SMask_match':True,
            'Interpolate_DecodeParms_other_attrs_absent_in_both_actual_dictionaries':True,
            'image_RAW_SHA256':im['raw_SHA256'],'image_decoded_SHA256':im['decoded_SHA256'],
            'SMask_RAW_SHA256':sm['raw_SHA256'],'SMask_decoded_SHA256':sm['decoded_SHA256']})
    return patches,evidence

def prepare_RAM(root_gate_path,root_gate_sha256):
    gatep=Path(root_gate_path);assert sha(gatep)==root_gate_sha256
    gate=json.loads(gatep.read_text(encoding='utf-8-sig'))
    assert gate['status']=='ROOT_AUTHORIZE_SL_CURRENT_BASE_GRAFT_RAM_ONLY_NO_PDF'
    assert gate['reviewed_preflight_SHA256']==PRE_SHA and gate['reviewed_helper_SHA256']==HELPER_SHA
    assert gate['reviewed_caller_SHA256']==sha(__file__)
    assert gate['reviewed_actual_freeze05_SHA256']==F05_SHA and gate['reviewed_actual_freeze06_SHA256']==F06_SHA
    assert sha(PREFLIGHT)==PRE_SHA
    p=json.loads(PREFLIGHT.read_text(encoding='utf-8'))
    for k in ('current','source','donor_M2','native'):assert sha(p[k])==p[k+'_SHA256']
    for f,h in p['guards'].items():assert sha(f)==h,f
    assert sha(p['helper_path'])==HELPER_SHA and sha(PKG/'catfix/pdfdoc.py')==API_SHA
    assert gate['current_SHA256']==p['current_SHA256'] and gate['native_SHA256']==p['native_SHA256']
    patches,patch_evidence=read_actual_patches(p)
    sys.path.insert(0,str(PKG));sys.path.insert(0,str(Path(__file__).resolve().parent))
    from catfix.pdfdoc import PdfDoc
    from catfix.cs import Ref,Name
    import pikepdf
    from next_work_sl_graft_existing_pure1 import graft_current_RAM_only
    base=donor=None
    try:
        base=PdfDoc(p['current'],backend='pikepdf');donor=PdfDoc(p['donor_M2'],backend='pikepdf')
        assert base.path==p['current'] and base.path!=p['donor_M2']
        protected={}
        def snapshot(v):
            if isinstance(v,Ref):
                if v in protected:return
                d=copy.deepcopy(base.get(v));raw=None;decoded=None;filters=None
                o=base.pdf.get_object(tuple(v))
                if isinstance(o,pikepdf.Stream):
                    raw=base.stream_raw(v);dd,fl,_=base.stream_decoded(v);decoded=dd;filters=fl
                protected[v]={'dict':d,'raw':raw,'decoded':decoded,'remaining_filters':filters}
                snapshot(d)
            elif isinstance(v,dict):
                for z in v.values():snapshot(z)
            elif isinstance(v,list):
                for z in v:snapshot(z)
        roots=copy.deepcopy([base.page_resources(pi) for pi in range(11)])
        for z in roots:snapshot(z)
        info0=copy.deepcopy(base.get(base.pdf.trailer.Info)) if '/Info' in base.pdf.trailer else None
        if '/Info' in base.pdf.trailer and base.pdf.trailer.Info.is_indirect:snapshot(Ref(base.pdf.trailer.Info.objgen))
        if '/Metadata' in base.pdf.Root:
            assert base.pdf.Root.Metadata.is_indirect;snapshot(Ref(base.pdf.Root.Metadata.objgen))
        receipt=graft_current_RAM_only(base,donor,Path(p['native']).read_bytes(),patches)
        donor.close();donor=None
        assert (base.get(base.pdf.trailer.Info) if '/Info' in base.pdf.trailer else None)==info0
        # New39/40 dictionary equality allows only newly allocated SMask Ref.
        xr=base.page_resources(9)['XObject']
        for q in patches:
            im=base.get(xr[q['name']]);sm=im['SMask'];expected_im={k:(Name(v) if k in ('Type','Subtype','ColorSpace','Filter') else v) for k,v in q['actual_frozen_image_dictionary'].items() if k!='SMask'}
            expected_im['SMask']=sm
            expected_sm={k:(Name(v) if k in ('Type','Subtype','ColorSpace','Filter') else v) for k,v in q['actual_frozen_SMask_dictionary'].items()}
            assert im==expected_im and base.get(sm)==expected_sm
            assert base.stream_raw(xr[q['name']])==q['RGB_raw'] and base.stream_raw(sm)==q['SMask_raw']
        for ref,old in protected.items():
            assert base.get(ref)==old['dict'],('protected dictionary/Ref changed',ref)
            if old['raw'] is not None:
                assert base.stream_raw(ref)==old['raw'],('protected raw changed',ref)
                dd,fl,_=base.stream_decoded(ref);assert dd==old['decoded'] and fl==old['remaining_filters']
        for k in ('current','source','donor_M2','native'):assert sha(p[k])==p[k+'_SHA256']
        for f,h in p['guards'].items():assert sha(f)==h,f
        assert sha(FREEZE05)==F05_SHA and sha(FREEZE06)==F06_SHA
        receipt.update(ROOT_gate=str(gatep),ROOT_gate_SHA256=root_gate_sha256,current_base_path=p['current'],current_base_SHA256=p['current_SHA256'],
            donor_M2_used_only_for_missing36images=True,preflight_SHA256=PRE_SHA,caller_SHA256=sha(__file__),helper_SHA256=HELPER_SHA,
            actual_freeze05_SHA256=F05_SHA,actual_freeze06_SHA256=F06_SHA,actual_RAM2images4streams_verified=patch_evidence,
            actual_RAW_dictionary_Filter_dimensions_SMask_grafted_exact=True,source_recipe_replay_all4_RAW_bins_confirmed_against_actual_RAM=True,
            existing_protected_resource_metadata_Refs_checked=len(protected),existing_protected_dictionary_raw_decoded_Filter_Refs_exact=True,
            original_strict_frame_FAIL_retained=True,PDF_saves=0,full_G04_complete=False,
            next='ROOT owns fresh context/lease and separate one-PDF gate before CATFIX save; saved native/expanded resource map/old assets/meta/pages/outside pixels still require actual independent readback.')
        return base,receipt
    except Exception:
        if base is not None:base.close()
        raise
    finally:
        if donor is not None:donor.close()

# Deliberately no CLI/main/save call. ROOT controls execution and close.
