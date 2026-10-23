"""Read the already-saved SL draft: exact M2 crops and strict outside pixels."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import hashlib,json,uuid
from datetime import datetime,timezone
import numpy as np
import pymupdf as fitz
from PIL import Image
from catwork import start,HERE

def main():
    S,_,_=start()
    import sys;sys.path.insert(0,str(HERE))
    from g04_perotac_whole_actual_read50 import render_document,metadata
    from g04_perotac_whole_pdf_tools46 import pixel_at
    sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
    read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
    ram=Path(S.report('G04/ROOT SL10 C2 HEAD20 SOURCE AXIS RAM M2 QUEUEFIX 20261004T034822Z-cafb76/01 SL10 C2 HEAD20 ACTUAL RAM ALL DELTAS NO PDF.json'))
    assert sha(ram)=='5d44f8ebe8efc65a20a831241f132b57a258f4b452a3d83fb8f5a9beb39e5098'
    r=read(ram);plan=read(r['math_plan']);b=read(plan['prior_M2_manifest'])
    candidate=Path(S.report('G04/ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE 20261004T041608Z-5ddd0c'))/Path(b['input']).name
    assert sha(candidate)=='ddb0bc676409b0078e62a8ed44ece585bc2e6bba3ae3a4fac3f2ece5ef85a0ae'
    for p,h in r['guarded_files'].items():assert sha(p)==h,p
    out=Path(S.report('G04'))/('ROOT SL ACTUAL SAVED4 CROP11 OUTSIDE AND LITERAL META DELTA '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
    crops=[];outside=[];table=[]
    with fitz.open(candidate) as saved,fitz.open(b['input']) as current,fitz.open(b['candidate']) as oldM2:
        md_current=metadata(current);md_saved=metadata(saved)
        md_diff={k:dict(current=md_current[k],actual=md_saved[k]) for k in md_current if md_current[k]!=md_saved[k]}
        # Literal bookmark xrefs are diagnostic data. Keep their full delta;
        # do not block independent pixel observation or pretend zero change.
        assert hashlib.sha256(saved[9].read_contents()).hexdigest()==r['actual_native_SHA256']
        for i,q in enumerate(r['pictures'],1):
            ar,_=render_document(saved,9,q['dpi'],q['rect']);old=np.array(Image.open(q['path']).convert('RGB'))
            assert ar.shape==old.shape
            changed=int(np.any(ar!=old,axis=2).sum())
            p=out/(f'{i:02d} ACTUAL SAVED '+Path(q['path']).name);Image.fromarray(ar).save(p)
            crops.append(dict(path=str(p),SHA256=sha(p),accepted_RAM_picture=q['path'],accepted_RAM_SHA256=q['SHA256'],dpi=q['dpi'],rect=q['rect'],changed_pixels_vs_same_M2_RAM=changed,from_actual_saved_PDF=True))
        for dpi in (150,200,600):
            a,m=render_document(oldM2,9,dpi,[454.8,33.8,815.04,174.2]);z,mz=render_document(saved,9,dpi,[454.8,33.8,815.04,174.2]);assert m==mz and a.shape==z.shape
            table.append(dict(dpi=dpi,changed_pixels_vs_table120_accepted_oldM2=int(np.any(a!=z,axis=2).sum())))
        for pi in range(11):
            a,m=render_document(current,pi,200);z,mz=render_document(saved,pi,200);assert m==mz and a.shape==z.shape
            mask=np.zeros(a.shape[:2],bool)
            if pi==9:
                for box in b['allowed']:
                    p0,p1=pixel_at(box[:2],m),pixel_at(box[2:],m);x0,y0=np.floor(np.minimum(p0,p1)).astype(int);x1,y1=np.ceil(np.maximum(p0,p1)).astype(int)
                    mask[max(0,y0):min(mask.shape[0],y1),max(0,x0):min(mask.shape[1],x1)]=True
            changed=np.any(a!=z,axis=2)
            outside.append(dict(page=pi+1,dpi=200,threshold=0,additional_pad=0,original_ROI_held=True,outside_changed_pixels=int((changed&~mask).sum()),total_changed_pixels=int(changed.sum())))
    for p,h in r['guarded_files'].items():assert sha(p)==h,p
    report=dict(status='ACTUAL_SAVED_RENDER_CHECK_NO_ADOPTION',candidate=str(candidate),candidate_SHA256=sha(candidate),actual_native_SHA256=r['actual_native_SHA256'],crops4=crops,table120_RGB3_resolutions=table,outside11pages200=outside,metadata_matches_current_literal=(not md_diff),metadata_literal_deltas=md_diff,original_RAM_crop_and_fullpage_frame_pixel_FAIL_retained=True,literal_saved_Refs_match_RAM_FAILED=True,PDF_saves=0,new_visual_samples=0,canonical_ledger_index_writes=0,full_G04_complete=False)
    report=json.loads(json.dumps(report,ensure_ascii=False,default=str))
    p=out/'05 ROOT ACTUAL SL4 CROP11 OUTSIDE TABLE120 READBACK.json'
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert read(p)==report
    print(json.dumps(dict(report=str(p),SHA256=sha(p),crops_delta=[q['changed_pixels_vs_same_M2_RAM'] for q in crops],table_delta=[q['changed_pixels_vs_table120_accepted_oldM2'] for q in table],outside=[q['outside_changed_pixels'] for q in outside]),ensure_ascii=False))
if __name__=='__main__':main()
