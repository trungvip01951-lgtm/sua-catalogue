"""Second/final actual C2/Q0 RAM sample; inspect every full-band change, no PDF write."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import uuid,json,hashlib,numpy as np
from PIL import Image
import pymupdf as fitz
from catwork import start,HERE

def main():
    S,_,_=start();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text(encoding='utf8'))
    import sys;sys.path.insert(0,str(HERE))
    from root_sl6sl25_C2_head_RAM_builder2_queuefix import build
    from g04_perotac_whole_actual_read50 import render_document,metadata
    from g04_perotac_whole_pdf_tools46 import pixel_at,page_at_pixel
    from catfix.raster import Raster
    from catfix import cs
    pp=Path(S.report('G04/ROOT SL6SL25 PLAN10 C2 EXACT120 20261004T032005Z-5a842c/01 SL10 C2 FRACTION40 SEGMENTS120 ANCHORS PLAN.json'));assert sha(pp)=='7615213844bfceb27fcffd74eed39714c47b63a18595f43081a98f7aa3d1b8ef';plan=read(pp)
    bp=Path(plan['prior_M2_manifest']);b=read(bp);guards=dict(plan['guarded_files']);guards[str(pp)]=sha(pp)
    guards[str(HERE/"root_sl6sl25_C2_head_RAM_builder2_queuefix.py")]=sha(HERE/"root_sl6sl25_C2_head_RAM_builder2_queuefix.py")
    guards[str(Path(__file__))]=sha(Path(__file__))
    for p,h in guards.items():assert sha(p)==h
    out=Path(S.report('G04'))/('ROOT SL10 C2 HEAD20 SOURCE AXIS RAM M2 QUEUEFIX '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
    j=None
    try:
        j,recipe,before,after,content=build(S,b,plan);E=j.E;P=E.page(9);doc=E.doc.doc
        assert hashlib.sha256(content).hexdigest()==recipe['content_SHA256']
        native=out/'SL P10 C2 HEADS SOURCE AXIS RAM M2 QUEUEFIX NATIVE.bin'
        with native.open('xb') as f:f.write(content)
        rgb=np.array(b['style']['RGB'])/255
        obs=[(i,o) for i,o in enumerate(P.objs) if o['op']=='S' and P.color_of(i,'stroke') is not None and np.allclose(P.color_of(i,'stroke'),rgb,rtol=0,atol=1e-8)]
        assert len(obs)==20;exact=[]
        for k,r in enumerate(plan['records10']):
            segs=[[[F(v) for v in p] for p in s['controls_page_fraction']] for s in r['segments4']]
            for side,(oi,o) in enumerate(obs[2*k:2*k+2]):
                group=segs[:1] if side==0 else segs[1:]
                ins=P.ops[o['i0']:o['i1']];assert [v.op for v in ins]==['m']+['c']*len(group)
                expected=[group[0][0]]+[[v for p in s[1:] for v in p] for s in group]
                for q,values in zip(ins,expected):
                    actual=[F(v.group('num').decode()) for v in cs._TOK.finditer(q.raw) if v.lastgroup=='num'];assert len(actual)==len(values)
                    assert all(abs(a-z)<=F(1,2*10**20) for a,z in zip(actual,values))
                old=recipe['replacements20'][2*k+side]['old_style']
                for field in ('lw','dash','cap','join','stroke','stroke_cs'):assert o.get(field)==old[field],(r['model'],side,field)
                assert o['clip'][0]<=float(segs[0][0][0]) and o['clip'][0]<=b['Q_local'][0]['page_x']
                exact.append(dict(model=r['model'],part=side,actual_object=oi,actual_fraction_all_controls_within_half_Num20=True,curve_clip_contains_Q0=True,pen_dash_color_original=True,cubic_count=len(group)))
        R=Raster(E);im=next(z for z in R.images(9) if z.name=='X18');cv=R.canvas(im)
        assert [im.W,im.H]==[1738,1236]
        assert abs(cv.to_px(b['Q_local'][0]['page_x'],400)[0]-1352.5)<1e-10
        # Caption resources/placements inherited literally from the old M2.
        for c in b['captions']:
            drawn=next(z for z in R.images(9) if z.name==c['image_name']);assert np.allclose(drawn.page_bbox,c['physical_box'],rtol=0,atol=1e-7)
        pictures=[];bands=[];protected=[];outside=[]
        with fitz.open(b['source']) as source,fitz.open(b['input']) as current,fitz.open(b['candidate']) as M2:
            assert metadata(doc)==metadata(M2)
            def image(ar,name,dpi,rect):
                p=out/(name+'.png');Image.fromarray(ar).save(p);pictures.append(dict(path=str(p),SHA256=sha(p),dpi=dpi,rect=rect,from_actual_RAM=True))
            def native_grid(shape,m):
                z=np.array(cv.to_px(*page_at_pixel([.5,.5],m)));x=np.array(cv.to_px(*page_at_pixel([1.5,.5],m)));y=np.array(cv.to_px(*page_at_pixel([.5,1.5],m)));yy,xx=np.indices(shape)
                return z[0]+xx*(x[0]-z[0])+yy*(y[0]-z[0]),z[1]+xx*(x[1]-z[1])+yy*(y[1]-z[1])
            f=b['frame'];whole=[f[0]-15,f[1]-8,f[2]+15,f[3]+15]
            for dpi in (150,200,600):
                aa,m=render_document(source,9,dpi,whole);zz,mz=render_document(doc,9,dpi,whole);assert aa.shape==zz.shape and m==mz
                u,v=native_grid(aa.shape[:2],m);changed=np.any(aa!=zz,axis=2)
                ext=(u>=1350)&(u<1664)&(v>=181)&(v<472);band=ext&((u<1356)|(u>=1657)|(v<187)|(v>=466)|((u>=1551)&(v<215)))
                core=ext&((u<1351)|(u>=1659)|(v<185)|(v>=468)|((u>=1551)&(v<215)))
                yy,xx=np.where(changed&band)
                all_delta=[dict(native=[float(u[y,x]),float(v[y,x])],source_RGB=aa[y,x].tolist(),actual_RAM_RGB=zz[y,x].tolist(),outside_axis_restore_and_new_head_strip=bool(core[y,x])) for y,x in zip(yy,xx)]
                bands.append(dict(dpi=dpi,whole_OLD_mandatory_band_changed=int((changed&band).sum()),all_changed_pixel_records=all_delta,omitted_pixels=0,
                    wider_frame_core_changed=int((changed&core).sum()),old_band_is_not_redefined_as_all_frame='Every original-band change recorded;1353–1355 overlaps pump heads. Source-axis actual core restoration is separately measured, not assumed exact.',
                    source_axis_restore_clip_box=recipe['source_axis_restore_page_box']))
                for name,box in [('TITLE',[747.8,491.8,796.5,504.5])]+[(f"FEET{r['feet']}",r['source_restore_box']) for r in b['feet_source_holes']]+[('ETA',[647,330,803,362])]:
                    a,m=render_document(source,9,dpi,box);z,mz=render_document(doc,9,dpi,box);assert m==mz and a.shape==z.shape
                    protected.append(dict(name=name,dpi=dpi,box=box,changed_pixels=int(np.any(a!=z,axis=2).sum())))
                a,m=render_document(M2,9,dpi,[454.8,33.8,815.04,174.2]);z,mz=render_document(doc,9,dpi,[454.8,33.8,815.04,174.2]);assert m==mz and np.array_equal(a,z)
                if dpi in (150,600):image(zz,'SL10 C2 NEW WHOLE QH '+str(dpi),dpi,whole)
                if dpi==600:
                    box=[f[0]-3,f[1]-2,f[0]+12,f[3]+2];z,_=render_document(doc,9,600,box);image(z,'SL10 C2 NEW LEFT ALL10 HEADS600',600,box)
                    box=[670,386,700,499];z,_=render_document(doc,9,600,box);image(z,'SL10 C2 NEW ALL10 CAPTIONS600',600,box)
            for pi in range(11):
                a,m=render_document(current,pi,200);z,mz=render_document(doc,pi,200);assert m==mz and a.shape==z.shape;mask=np.zeros(a.shape[:2],bool)
                if pi==9:
                    for box in [b['body']]+[r['inner_box'] for r in b['table_changes']]:
                        p0,p1=pixel_at(box[:2],m),pixel_at(box[2:],m);x0,y0=np.floor(np.minimum(p0,p1)).astype(int);x1,y1=np.ceil(np.maximum(p0,p1)).astype(int);mask[max(0,y0):min(mask.shape[0],y1),max(0,x0):min(mask.shape[1],x1)]=True
                changed=np.any(a!=z,axis=2);outside.append(dict(page=pi+1,outside_changed_pixels=int((changed&~mask).sum()),total_changed_pixels=int(changed.sum()),dpi=200,threshold=0,additional_pad=0))
        for p,h in guards.items():assert sha(p)==h
        report=dict(status='ACTUAL_RAM_M2_NATIVE20_C2_EXACT_SCOPE_VISUAL_PENDING',created_utc=datetime.now(timezone.utc).isoformat(),math_plan=str(pp),math_plan_SHA256=sha(pp),recipe=recipe,
            actual20_native_checks=exact,actual_native_file=str(native),actual_native_SHA256=sha(native),table120_RAM_exact_M2_all3_resolutions=True,
            original_band_all_changes150_200_600=bands,protected_title_feet_eta_all_changes=protected,outside11pages200_threshold0=outside,pictures=pictures,
            original_Q0_frame_live_native1352_5=True,source_axis_core_REQUIRES_visual_readback=True,no_ROI_enlargement=True,guarded_files=guards,
            numeric_plan_only_no_independent_saved_PDF_acceptance=True,Editor_instances=1,PDF_saves=0,canonical_ledger_index_claim_writes=0,full_G04_complete=False)
        jp=out/'01 SL10 C2 HEAD20 ACTUAL RAM ALL DELTAS NO PDF.json'
        report=json.loads(json.dumps(report,ensure_ascii=False,default=lambda x:x.tolist() if hasattr(x,'tolist') else str(x)))
        with jp.open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
        assert read(jp)==report
        print(json.dumps(dict(path=str(jp),SHA256=sha(jp),native_SHA256=sha(native),outside11=[r['outside_changed_pixels'] for r in outside],protected_changes=[(r['name'],r['dpi'],r['changed_pixels']) for r in protected],old_bands=[(r['dpi'],r['whole_OLD_mandatory_band_changed'],r['wider_frame_core_changed']) for r in bands],PDF_saves=0),ensure_ascii=False),flush=True)
    except Exception as ex:
        q=out/'00 FAILURE KEEP ORIGINAL SAMPLE NO AUTO RETRY.json'
        with q.open('x',encoding='utf8') as f:json.dump(dict(error=repr(ex),PDF_saved=False,canonical_changed=False),f,ensure_ascii=False,indent=2)
        raise
    finally:
        if j is not None:j.close()
if __name__=='__main__':main()
