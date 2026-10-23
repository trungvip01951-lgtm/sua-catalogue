"""One actual CATFIX sample: graft accepted SL resources onto current, no publish."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,hashlib,uuid,copy,importlib.util
from datetime import datetime,timezone
from catwork import start,HERE

def main():
    S,_,_=start()
    import sys;sys.path.insert(0,str(HERE))
    import next_work_sl_current_base_graft_prepared_caller2_actualfreeze as caller
    from catfix.recipes import Job
    from catfix.pdfdoc import PdfDoc
    from catfix.cs import Ref
    import pikepdf
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
    def write(p,v):
        with p.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
    cp=HERE/'next_work_sl_current_base_graft_prepared_caller2_actualfreeze.py'
    assert sha(cp)=='27256a4b6fde44ff803b2b1088f8b40d2cf43a4b45a26ace2d59ebc7eaa32305'
    pre=read(caller.PREFLIGHT)
    indep=Path(S.report('G04/DOC LAP SL GRAFT36 VA FREEZE39 40 KHONG RAM SAVE 20261004T040917Z-9f0732/01 DOC LAP SL36 GRAFT INPUT VA4 FROZEN STREAM39 40.json'))
    assert sha(indep)=='00b352e4132afa7011c2036e48d7303fa9463fb0d6554457699105713a07d6ca'
    ip=read(indep);assert ip['status']=='PASS_READ_ONLY_GRAFT_CODE_INPUT_AND_ACTUAL_FROZEN_PAYLOAD_ONLY'
    for p,h in ip['inputs_before_after_held'].items():assert sha(p)==h,p
    RAMp=Path(S.report('G04/ROOT SL10 C2 HEAD20 SOURCE AXIS RAM M2 QUEUEFIX 20261004T034822Z-cafb76/01 SL10 C2 HEAD20 ACTUAL RAM ALL DELTAS NO PDF.json'))
    RAM=read(RAMp);plan=read(RAM['math_plan']);b=read(plan['prior_M2_manifest'])
    assert sha(RAMp)=='5d44f8ebe8efc65a20a831241f132b57a258f4b452a3d83fb8f5a9beb39e5098'
    assert RAM['actual_native_SHA256']==pre['native_SHA256']=='7184d01f463d8eccfd5d1a85893850b7fd6d285f2d7c0edc36cf0ec8208606ee'
    assert sha(pre['current'])==pre['current_SHA256'] and sha(pre['source'])==pre['source_SHA256']
    # This is a draft save. Every internal frame diagnostic FAIL is retained;
    # no source-frame-pixel0 or full-group acceptance is declared.
    out=Path(S.report('G04'))/('ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
    project=Path(r'D:\ChatGPT\Sửa catalogue')
    spec=importlib.util.spec_from_file_location('root_sl_writer_coord',project/'tools/catalogue.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    file='Giếng/Redpump gieng SL_compressed (bản mới).pdf';ctx=C.context(file);C.validate_context(ctx)
    assert ctx['current_sha256']==pre['current_SHA256'] and ctx['source_sha256']==pre['source_SHA256']
    assert Path(S.result(Path(pre['current']).name))==Path(pre['current']) and Path(S.src(Path(pre['source']).name))==Path(pre['source'])
    actor='ROOT';session='root-sl-C2-current-base-one-actual-sample-20261004'
    claim=C.claim(file,actor,session,'Một mẫu CATFIX C2 với current base, existing Contents105, ảnh mới đúng frozen payload; chưa bản chính',3600)
    base=job=None;completed=False
    initial_record=dict(source=pre['source'],source_SHA256=pre['source_SHA256'],current=pre['current'],current_SHA256=pre['current_SHA256'],claim=claim,full_G04_complete=False)
    write(out/'00 CURRENT SOURCE CLAIM BEFORE ONE DRAFT SAVE.json',initial_record)
    try:
        C.check(claim['token'],actor,session)
        ramgate=dict(status='ROOT_AUTHORIZE_SL_CURRENT_BASE_GRAFT_RAM_ONLY_NO_PDF',reviewed_preflight_SHA256=caller.PRE_SHA,reviewed_helper_SHA256=caller.HELPER_SHA,reviewed_caller_SHA256=sha(cp),reviewed_actual_freeze05_SHA256=caller.F05_SHA,reviewed_actual_freeze06_SHA256=caller.F06_SHA,current_SHA256=pre['current_SHA256'],native_SHA256=pre['native_SHA256'],independent_preflight_path=str(indep),independent_preflight_SHA256=sha(indep),source_frame_pixel_FAIL_retained=True,PDF_save_authorized=False)
        gp=out/'01 ROOT REVIEWED RAM GRAFT GATE.json';write(gp,ramgate)
        base,grafted=caller.prepare_RAM(str(gp),sha(gp))
        gr=out/'02 ACTUAL CURRENT BASE RAM GRAFT READBACK NO SAVE.json';write(gr,json.loads(json.dumps(grafted,ensure_ascii=False)))
        # Freeze the expanded exact RAM resource graph, refs and metadata.
        expected={}
        def snap(v):
            if isinstance(v,Ref):
                if v in expected:return
                d=copy.deepcopy(base.get(v));o=base.pdf.get_object(tuple(v));raw=base.stream_raw(v) if isinstance(o,pikepdf.Stream) else None
                expected[v]=(d,raw);snap(d)
            elif isinstance(v,dict):
                for a in v.values():snap(a)
            elif isinstance(v,list):
                for a in v:snap(a)
        roots=copy.deepcopy([base.page_resources(p) for p in range(11)])
        for v in roots:snap(v)
        if '/Info' in base.pdf.trailer and base.pdf.trailer.Info.is_indirect:snap(Ref(base.pdf.trailer.Info.objgen))
        if '/Metadata' in base.pdf.Root:snap(Ref(base.pdf.Root.Metadata.objgen))
        pages=copy.deepcopy([base.page_dict(p) for p in range(11)]);contents=[base.page_content(p) for p in range(11)];contentrefs=[base.page_contents_refs(p) for p in range(11)]
        candidate=out/Path(pre['current']).name;assert not candidate.exists()
        savegate=dict(status='ROOT_AUTHORIZE_ONE_CATFIX_SL_CURRENT_BASE_DRAFT_PDF_ONLY',candidate=str(candidate),RAM_gate_SHA256=sha(gp),actual_RAM_graft_SHA256=sha(gr),source_SHA256=pre['source_SHA256'],current_SHA256=pre['current_SHA256'],accepted_native_SHA256=pre['native_SHA256'],old_assets_held_in_RAM=True,expanded_resource_nodes=len(expected),canonical_write_authorized=False,full_G04_complete=False,source_frame_pixel0_NOT_PASSED=True,original_allowed_ROI=b['allowed'],new_visual_sample=False)
        sg=out/'03 ROOT ONE DRAFT PDF SAVE GATE NOT CANONICAL.json';write(sg,savegate)
        C.check(claim['token'],actor,session)
        # Job handles the sole catalogue write, log and permitted-region check.
        job=Job(pre['current'],str(candidate),backend='pikepdf',log_path=str(out/'04 CATFIX ACTUAL SAVE LOG.json'))
        job.E.doc.close();job.E.doc=base;base=None
        for i,box in enumerate(b['allowed']):job._add(9,box,'C2 whole authorized chart' if i==0 else 'Planned integer table cell','accepted_same_M2_native_current_base_graft')
        assert len(job.edits)==27
        job.save()
        checked=job.check();assert checked['ok'] and not checked['unexpected'] and not checked['missing'],checked
        pic=out/'05 CATFIX SOURCE CURRENT VS ACTUAL27 REGIONS.png';job.evidence(str(pic),dpi=200)
        job.close();job=None
        saved=PdfDoc(str(candidate),backend='pikepdf')
        try:
            assert saved.n_pages==11
            assert [saved.page_resources(p) for p in range(11)]==roots
            assert [saved.page_dict(p) for p in range(11)]==pages
            assert [saved.page_contents_refs(p) for p in range(11)]==contentrefs
            assert [saved.page_content(p) for p in range(11)]==contents
            for ref,(d,raw) in expected.items():
                assert saved.get(ref)==d,('actual saved dictionary/ref differs from final RAM',ref)
                if raw is not None:assert saved.stream_raw(ref)==raw,('actual saved resource raw differs',ref)
        finally:saved.close()
        for p,h in ip['inputs_before_after_held'].items():assert sha(p)==h,p
        assert sha(pre['current'])==pre['current_SHA256'] and sha(pre['source'])==pre['source_SHA256']
        C.check(claim['token'],actor,session)
        rp=out/'06 ROOT ACTUAL CATFIX SL NATIVE ASSETS EXACT PENDING SAVED GRAPHICS.json'
        report=dict(initial_record,status='PASS_ACTUAL_SAVED_NATIVE_EXPANDED_RESOURCE_MAP_AND_JOB_CHECK_PENDING_INDEPENDENT_VISUAL_OUTSIDE',candidate=str(candidate),candidate_SHA256=sha(candidate),candidate_bytes=candidate.stat().st_size,actual_graft_report=str(gr),actual_graft_SHA256=sha(gr),native_SHA256=pre['native_SHA256'],all11_page_dicts_contents_refs_and_resources_exact_final_RAM=True,other10_pages_held=True,expanded_resources_metadata_nodes=len(expected),every_resource_dictionary_Ref_RAW_exact_to_final_RAM=True,Job_check=checked,source_frame_pixel0_NOT_PASSED=True,original_RAM_diagnostics_retained=True,CATFIX_save_calls=1,saved_via='catfix.recipes.Job.save -> Editor.save -> PdfDoc.save pikepdf',canonical_ledger_index_writes=0,comparison=str(pic),comparison_SHA256=sha(pic),full_G04_complete=False)
        write(rp,report);assert read(rp)==report;completed=True
        print(json.dumps(dict(candidate=str(candidate),SHA256=sha(candidate),receipt=str(rp),receipt_SHA256=sha(rp),resources_exact=len(expected),PDF_saves=1,canonical_writes=0),ensure_ascii=False))
    except Exception as ex:
        p=out/'99 FAILURE RETAIN SAMPLE DO NOT AUTOMATICALLY RETRY.json'
        write(p,dict(initial_record,error=repr(ex),candidate_exists=(out/Path(pre['current']).name).exists(),canonical_written=False))
        raise
    finally:
        if job is not None:job.close()
        if base is not None:base.close()
        C.release(claim['token'],actor,session,('One actual sample saved; awaiting independent actual checks: '+str(out)) if completed else ('Draft attempt stopped; no canonical write: '+str(out)))
if __name__=='__main__':main()
