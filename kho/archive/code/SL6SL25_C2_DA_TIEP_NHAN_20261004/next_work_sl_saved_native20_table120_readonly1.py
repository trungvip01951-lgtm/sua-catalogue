"""Independent actual saved SL path/Do/payload/table transfer reader; no PDF save."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,copy,datetime,uuid

PKG=Path(r'D:\ChatGPT\Sửa catalogue\vendor\catfix_original\GOI_SUA_CATALOGUE_CHATGPT')
SAVED=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\ROOT SL C2 CURRENT BASE ONE CATFIX ACTUAL SAMPLE 20261004T041608Z-5ddd0c\Redpump gieng SL_compressed (bản mới).pdf')
SAVED_SHA='ddb0bc676409b0078e62a8ed44ece585bc2e6bba3ae3a4fac3f2ece5ef85a0ae'
RAM=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\ROOT SL10 C2 HEAD20 SOURCE AXIS RAM M2 QUEUEFIX 20261004T034822Z-cafb76\01 SL10 C2 HEAD20 ACTUAL RAM ALL DELTAS NO PDF.json')
RAM_SHA='5d44f8ebe8efc65a20a831241f132b57a258f4b452a3d83fb8f5a9beb39e5098'
MATH=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G04\G03 SL10 C2 DOC LAP FRACTION40 JOIN30 TABLE120 CHUA RAM 20261004T032612Z-b7e46e\01 DOC LAP SL10 C2 FRACTION40 JOIN30 TABLE120 PLAN PASS NO RAM.json')
MATH_SHA='b621ec6f19ed0849294156df2abe339528078f8251306f97b672904887f097dc'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def plain(v):
    if hasattr(v,'tolist'):return v.tolist()
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [plain(x) for x in v]
    return v
def bez(c,t):return sum(v*(1-t)**(3-i)*t**i*n for i,(v,n) in enumerate(zip(c,(1,3,3,1))))
def interp(value,xs,ys):
    assert xs[0]<=value<=xs[-1]
    if value==xs[-1]:return ys[-1]
    for x0,x1,y0,y1 in zip(xs,xs[1:],ys,ys[1:]):
        if x0<=value<=x1:return y0+(y1-y0)*(value-x0)/(x1-x0)
    raise AssertionError(value)
def overlap(a,b):return min(a[2],b[2])>max(a[0],b[0])+1e-7 and min(a[3],b[3])>max(a[1],b[1])+1e-7

def main():
    sys.path.insert(0,str(PKG))
    from catfix.pdfdoc import PdfDoc
    from catfix.cs import parse,Ref,_TOK
    from catfix.vector import VPage,apply
    from catfix.session import Session
    assert sha(SAVED)==SAVED_SHA and sha(RAM)==RAM_SHA and sha(MATH)==MATH_SHA
    ram=read(RAM);math=read(MATH);pp=Path(ram['math_plan']);plan=read(pp)
    assert sha(pp)==ram['math_plan_SHA256']=='7615213844bfceb27fcffd74eed39714c47b63a18595f43081a98f7aa3d1b8ef'
    bp=Path(plan['prior_M2_manifest']);b=read(bp);assert sha(bp)==plan['prior_M2_manifest_SHA256']
    table=read(b['plan_file']);assert sha(b['plan_file'])==b['plan_SHA256']
    guards=dict(ram['guarded_files']);guards.update({str(SAVED):SAVED_SHA,str(RAM):RAM_SHA,str(MATH):MATH_SHA,str(Path(__file__).resolve()):sha(__file__)})
    for p,h in guards.items():assert sha(p)==h,p
    assert math['overall'].startswith('PASS_PURE_PLAN10_40BEZIER_30C2_120TABLE')
    def inventory(path):
        D=PdfDoc(str(path),backend='pikepdf')
        try:
            rawcontent=D.page_content(9);P=VPage(parse(rawcontent));xr=D.resolve(D.page_resources(9)['XObject']);assets={}
            for n,ref in xr.items():
                dd=D.get(ref);raw=D.stream_raw(ref);decoded,left,_=D.stream_decoded(ref);sm=dd.get('SMask');mask=None
                if sm is not None:
                    mask={'dict':D.get(sm),'raw':D.stream_raw(sm),'decoded':D.stream_decoded(sm)[0]}
                assets[n]={'ref':list(ref),'dict':dd,'raw':raw,'decoded':decoded,'remaining_filters':left,'SMask':mask}
            return rawcontent,P,assets,[list(x) for x in D.page_contents_refs(9)]
        finally:D.close()
    native,P,assets,refs=inventory(SAVED)
    old_native,oldP,old_assets,old_refs=inventory(b['candidate'])
    current_native,currentP,current_assets,current_refs=inventory(b['input'])
    source_native,sourceP,source_assets,source_refs=inventory(b['source'])
    assert native==Path(ram['actual_native_file']).read_bytes() and hashlib.sha256(native).hexdigest()==ram['actual_native_SHA256']=='7184d01f463d8eccfd5d1a85893850b7fd6d285f2d7c0edc36cf0ec8208606ee'
    images={str(z['name']):z for z in P.images};oldimages={str(z['name']):z for z in oldP.images}
    assert set(images)==set(assets)=={'CfxPatch'+str(k) for k in range(1,41)}|{'X18','X19'}
    assert sum(str(z['name'])=='X18' for z in P.images)==2 and len(P.images)==43
    strokes=[(i,o) for i,o in enumerate(P.objs) if o['op']=='S'];assert len(strokes)==20
    # VPage omits cap/join from its state, so read those operators directly.
    state={'cap':0,'join':0};stack=[];at={}
    for i,z in enumerate(P.ops):
        if z.op=='q':stack.append(dict(state))
        elif z.op=='Q':state=stack.pop() if stack else state
        elif z.op=='J':state['cap']=int(z.operands[0])
        elif z.op=='j':state['join']=int(z.operands[0])
        if z.op=='S':at[i]=dict(state)
    tol=F(1,2*10**20);curves=[];actual_segments=[]
    hs=[F(str(x['H'])) for x in b['H_local']];ys=[F(str(x['page_y'])) for x in b['H_local']]
    for k,r in enumerate(plan['records10']):
        assert r['model']==b['model_paths'][k]['model'];segs=[]
        for part,(oi,o) in enumerate(strokes[2*k:2*k+2]):
            expected=[[[F(v) for v in pt] for pt in s['controls_page_fraction']] for s in (r['segments4'][:1] if part==0 else r['segments4'][1:])]
            ins=P.ops[o['i0']:o['i1']];assert [z.op for z in ins]==['m']+['c']*len(expected)
            values=[[F(t.group('num').decode()) for t in _TOK.finditer(z.raw) if t.lastgroup=='num'] for z in ins]
            target=[expected[0][0]]+[[v for pt in s[1:] for v in pt] for s in expected]
            assert all(len(v)==len(w) and all(abs(a-e)<=tol for a,e in zip(v,w)) for v,w in zip(values,target))
            start=values[0]
            for v in values[1:]:
                seg=[start,[v[0],v[1]],[v[2],v[3]],[v[4],v[5]]];segs.append(seg);start=seg[-1]
                assert all(seg[j][0]<seg[j+1][0] and seg[j][1]>=seg[j+1][1] for j in range(3)) and seg[0][1]>seg[-1][1]
            spec=ram['recipe']['replacements20'][2*k+part];assert spec['model']==r['model']
            for field in ('lw','dash','stroke','stroke_cs'):assert plain(o.get(field))==plain(spec['old_style'][field]),(r['model'],part,field)
            assert plain(o['ctm'])==[[1,0,0],[0,1,0],[0,0,1]]
            assert at[o['i1']]=={'cap':b['style']['cap'],'join':b['style']['join']}
            assert o['clip'][0]<=float(expected[0][0][0])<=o['clip'][2]
        assert len(segs)==4;actual_segments.append(segs)
        numeric=[]
        for a in r['anchors12_checked']:
            i=a['segment'];psegs=r['segments4'];control=[[F(v) for v in pt] for pt in psegs[i]['controls_page_fraction']]
            x=F(a['page_x']);t=(x-control[0][0])/(control[3][0]-control[0][0]);xx=bez([pt[0] for pt in segs[i]],t);yy=bez([pt[1] for pt in segs[i]],t)
            assert abs(xx-x)<=tol and abs(yy-F(a['page_y']))<=tol
            H=interp(yy,ys,hs);targetH=F(a['H_table']);lim=max(F(1),targetH/50);assert abs(H-targetH)<=lim
            numeric.append({'Q':a['Q'],'H_table':a['H_table'],'actual_H_fraction':str(H),'absolute_H_error_fraction':str(abs(H-targetH)),'tolerance_fraction':str(lim),'ratio':float(abs(H-targetH)/lim),'PASS':True})
        source=b['model_paths'][k]['H_source'];locked=r['H_locked'];assert max(source)==max(locked) and min(source)==min(locked)
        assert r['Q']==b['model_paths'][k]['Q'] and min(r['Q'])==0 and max(r['Q'])==33
        assert all(locked[j]>locked[j+1] for j in range(11))
        assert segs[0][0]==[[F(v) for v in pt] for pt in r['segments4'][0]['controls_page_fraction']][0] or all(abs(a-e)<=tol for a,e in zip(segs[0][0],[F(v) for v in r['segments4'][0]['controls_page_fraction'][0]]))
        joins=[]
        for left,right in zip(segs,segs[1:]):
            assert left[-1]==right[0]
            wl=left[-1][0]-left[0][0];wr=right[-1][0]-right[0][0]
            dl=3*(left[3][1]-left[2][1])/wl;dr=3*(right[1][1]-right[0][1])/wr
            ddl=6*(left[3][1]-2*left[2][1]+left[1][1])/wl**2;ddr=6*(right[2][1]-2*right[1][1]+right[0][1])/wr**2
            assert abs(dl-dr)<F(1,10**18) and abs(ddl-ddr)<F(1,10**18)
            joins.append({'C0_literal_exact':True,'actual_C1_slope_difference':str(dl-dr),'actual_C2_second_derivative_difference':str(ddl-ddr),'absolute_both_below_1e_minus18':True})
        curves.append({'model':r['model'],'actual_native_painted_parts':2,'actual_cubics':4,'same_own_source_pen_dash_color_cap_join':True,'CTM_identity':True,'literal_controls_within_half_Num20':True,'derivative_strict_fall_Q_strict_rise_actual':True,
            'joins3_actual':joins,'numeric12_actual':numeric,'source_TABLE_max_value':max(source),'locked_TABLE_max_value':max(locked),'source_TABLE_min_value':min(source),'locked_TABLE_min_value':min(locked),
            'Q0_table_corrected_to_preserve_source_max':source[0]!=locked[0],'TABLE_endpoints_page_coordinates_locked':True,'physical_factorymax_or_duty_inferred':False})
    tag=next(i for i,z in enumerate(P.ops) if z.op=='BMC' and str(z.operands[0])=='CfxSLP10OriginalDoExactMaskClipRAM117')
    assert [z.op for z in P.ops[tag+1:tag+11]]==['q','m','l','l','l','l','l','h','W','n']
    polygon=ram['recipe']['curve_clip_polygon_page_fraction']
    for z,pt in zip(P.ops[tag+2:tag+8],polygon):
        vv=[F(t.group('num').decode()) for t in _TOK.finditer(z.raw) if t.lastgroup=='num'];assert all(abs(a-F(e))<=tol for a,e in zip(vv,pt))
    def box(image):
        pts=[apply(image['ctm'],x,y) for x,y in [(0,0),(1,0),(0,1),(1,1)]]
        return [min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts)]
    def held_asset(name,old):
        a=assets[name];assert a['raw']==old['raw'] and a['decoded']==old['decoded'] and a['remaining_filters']==old['remaining_filters']
        ad,bd=dict(a['dict']),dict(old['dict']);ad.pop('SMask',None);bd.pop('SMask',None);assert ad==bd
        if old['SMask'] is not None:
            assert a['SMask'] is not None and a['SMask']==old['SMask']
        else:assert a['SMask'] is None
        return {'name':name,'old_ref':old['ref'],'actual_saved_ref':a['ref'],'raw_SHA256':hashlib.sha256(a['raw']).hexdigest(),'decoded_SHA256':hashlib.sha256(a['decoded']).hexdigest(),'dictionary_and_masks_held_except_numeric_SMASK_Ref':True}
    captions=[]
    for c in b['captions']:
        n=c['image_name'];held=held_asset(n,old_assets[n]);assert plain(images[n]['ctm'])==plain(oldimages[n]['ctm'])
        bb=box(images[n]);assert all(abs(a-e)<=1e-7 for a,e in zip(bb,c['physical_box']))
        assert hashlib.sha256(assets[n]['SMask']['decoded']).hexdigest()==c['alpha_SHA256']
        captions.append(dict(model=c['model'],physical_box_actual=bb,source_font_pixels_and_alpha_held=True,external_font=c['external_font'],**held))
    patches=[]
    for k,c in enumerate(b['table_changes']):
        name='CfxPatch'+str(3+k);held=held_asset(name,old_assets[name]);assert plain(images[name]['ctm'])==plain(oldimages[name]['ctm'])
        bb=box(images[name]);assert all(abs(a-e)<=1e-7 for a,e in zip(bb,c['actual_patch_box']))
        inner=c['inner_box'];assert bb[0]>=inner[0]-1e-7 and bb[1]>=inner[1]-1e-7 and bb[2]<=inner[2]+1e-7 and bb[3]<=inner[3]+1e-7
        patches.append(dict(model=c['model'],Q=c['Q'],source_H=c['H_source'],locked_H=c['H_proposed'],actual_box=bb,**held))
    assert len(patches)==26
    currentimages={str(z['name']):z for z in currentP.images}
    for name in ('CfxPatch1','CfxPatch2'):
        held_asset(name,current_assets[name])
        assert plain(images[name]['ctm'])==plain(currentimages[name]['ctm'])
        assert plain(images[name]['clip'])==plain(currentimages[name]['clip'])
    # Source whole raster and its first/original drawing stay exact. The extra
    # original-image Do is source-axis restoration, wholly outside TABLE cells.
    assert assets['X18']['raw']==current_assets['X18']['raw']==source_assets['X18']['raw']
    assert assets['X18']['decoded']==current_assets['X18']['decoded']==source_assets['X18']['decoded']
    first=next(z for z in P.images if str(z['name'])=='X18');cf=next(z for z in currentP.images if str(z['name'])=='X18');sf=next(z for z in sourceP.images if str(z['name'])=='X18')
    assert plain(first['ctm'])==plain(cf['ctm'])==plain(sf['ctm'])
    allcells=[c for row in table['proposals'] for c in row['all_source_cells']];assert len(allcells)==120
    changed={(x['model'],float(x['Q'])) for x in b['table_changes']};heldcells=[]
    new_noncell=[box(images['CfxPatch'+str(k)]) for k in range(29,41)]
    restored=[z for z in P.images if str(z['name'])=='X18'][1];new_noncell.append(list(restored['clip']))
    for c in allcells:
        if (c['model'],float(c['Q'])) in changed:continue
        assert c['current_H_cell_changed_pixels']==0
        assert all(not overlap(c['page_rect'],x['actual_box']) for x in patches)
        assert all(not overlap(c['page_rect'],bb) for bb in new_noncell)
        heldcells.append({'model':c['model'],'Q':c['Q'],'H_source_held':c['H_source'],'source_native_raster_payload_and_first_Do_held':True,'no_new_TABLE_or_plot_overlay_intersects_cell':True})
    assert len(heldcells)==94
    for p,h in guards.items():assert sha(p)==h,p
    S=Session();assert S.mode=='local';out=Path(S.report('G04'))/('DOC ACTUAL SL20 PATH40 CUBIC120 TABLE10 LABEL CHI DOC '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
    report={'status':'PASS_ACTUAL_SAVED_NATIVE_GEOMETRY_PAYLOAD_TABLE120_ONLY_STRICT_REFS_FAIL_RETAINED','candidate':str(SAVED),'candidate_SHA256':SAVED_SHA,'native_SHA256':hashlib.sha256(native).hexdigest(),
        'page10_actual_Contents_refs':refs,'page10_current_Contents_refs':current_refs,'literal_Ref_identity':'FAIL_RETAINED_CONTENTS105_TO106_AND_OTHERS_RENUMBERED','oldRefs_unchanged_claimed':False,
        'native_names42_resolve':True,'actual_image_Draws':43,'curves10':curves,'caption10_source_payload_and_CTM':captions,'table26_actual_patch_payload_and_CTM':patches,'source94_cells_transfer_proof':heldcells,
        'counts':{'curves':10,'painted_parts':20,'cubics':40,'joins':30,'numeric6b_anchors':120,'table_changed':26,'table_held':94,'caption10':10,'Do_names':42},
        'actual_max_numeric6b_ratio':max(a['ratio'] for r in curves for a in r['numeric12_actual']),
        'pure_math_reused':{'path':str(MATH),'SHA256':MATH_SHA,'scope':'All120 anchors re-evaluated from actual literal controls too; full planned C2/derivative proof transfers through halfNum20 quantization.'},
        'original_frame_pixels150_200':'FAIL_RETAINED; no rendering in this scope','saved_graphics_or_metadata_or_whole_bijective_ref_acceptance':'SEPARATE_SCOPE_NOT_CLAIMED','full_G04_complete':False,
        'guards_before_after_held':guards,'Editor_instances':0,'renders':0,'PDF_saves':0,'canonical_ledger_index_written':0}
    f=out/'01 ACTUAL SL NATIVE20 PATH40 CUBIC10 CAPTIONS120 TABLE ONLY.json'
    report=plain(report)
    with f.open('x',encoding='utf-8',newline='\n') as z:z.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert read(f)==report
    print(json.dumps({'report':str(f),'SHA256':sha(f),'candidate_SHA256':SAVED_SHA,'counts':report['counts'],'max_ratio':report['actual_max_numeric6b_ratio'],'strict_Refs_FAIL_retained':True,'PDF_saves':0},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
