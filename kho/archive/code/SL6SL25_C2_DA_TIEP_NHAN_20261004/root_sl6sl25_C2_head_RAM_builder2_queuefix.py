"""Second/final C2-head sample: source halo/core intact, sparse old-cap cleanup."""
def build(S,b,plan):
    import numpy as np,zlib,hashlib
    from catfix.cs import Instr,Name
    from catfix.raster import Raster
    from g12_full36_locked_path_and_source_glyph_math_next2 import precise_instr
    from root_sl6sl25_C2_head_RAM_builder1 import build as first_build
    j,r,before,after,content=first_build(S,b,plan);E=j.E
    # first_build already baked M1 into its in-memory page. The deferred
    # queues still refer to the pre-bake indices; discard only this page's
    # applied queues before preparing the second/final visual sample.
    applied=dict(deletions=len(E.dels.get(9,())),insertions=sum(len(v) for v in E.ins.get(9,{}).values()),modifications=len(E.mods.get(9,{})))
    for q in (E.dels,E.ins,E.mods):q.pop(9,None)
    E.pages.pop(9,None)
    assert E.build(9)==content
    P=E.page(9);R=Raster(E)
    im=next(z for z in R.images(9) if z.name=='X18');cv=R.canvas(im)
    old=r['original_cleaning_mask_recipe'];rows=np.asarray(old['source_grid_row_profiles_native']);cols=np.asarray(old['source_grid_column_profiles_native'])
    H,W=before.shape[:2];clean=before.copy();mask=np.zeros((H,W),bool);zones=[]
    # At the left source curve caps JPEG chroma was neutralized by the black
    # axis. The old colored-ink cleaner therefore left gray cap fragments.
    # Restrict extra cleaning to measured first-dash locations, right of the
    # complete native source axis+halo columns1351..1353. Source row/column
    # grid profiles replace only darker old-cap pixels; no rectangle is filled.
    hs=np.array([x['H'] for x in b['H_local']]);ys=np.array([x['page_y'] for x in b['H_local']])
    for model in b['model_paths']:
        yy=np.interp(model['H_source'][:2],hs,ys);vv=[cv.to_px(b['Q_local'][0]['page_x'],float(y))[1] for y in yy]
        v0=max(188,int(np.floor(min(vv)))-3);v1=min(465,int(np.ceil(max(vv)))+4)
        for v in range(v0,v1):
            for u in range(1354,1371):
                bg=np.rint(np.minimum(cols[u-1354],rows[v-185])).clip(0,255).astype(np.uint8)
                # Positive brightness deficit comes from the observed old head.
                # Preserve pixels already equal/lighter than source-grid profile.
                deficit=float(np.mean(bg.astype(float)-before[v,u].astype(float)))
                if deficit>=4:
                    clean[v,u]=bg;mask[v,u]=np.any(clean[v,u]!=before[v,u])
        zones.append(dict(model=model['model'],native_region=[1354,v0,1371,v1],source_first2_H=model['H_source'][:2],actual_source_grid_row_and_column_profiles=True))
    assert mask.any() and not mask[:,:1354].any()
    yy,xx=np.where(mask);bb=[int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1];u0,v0,u1,v1=bb
    alpha=np.ascontiguousarray(mask[v0:v1,u0:u1].astype(np.uint8)*255);pixels=np.ascontiguousarray(clean[v0:v1,u0:u1])
    sm=E.doc.new_image_xobject(zlib.compress(alpha.tobytes(),9),u1-u0,v1-v0,Name('DeviceGray'),8,'FlateDecode')
    ref=E.doc.new_image_xobject(zlib.compress(pixels.tobytes(),9),u1-u0,v1-v0,Name('DeviceRGB'),8,'FlateDecode',smask=sm)
    nm=R._register(9,ref);x0,y1=cv.to_page(u0,v0);x1,y0=cv.to_page(u1,v1)
    clipx=cv.to_page(1354,0)[0]
    tag=next(i for i,o in enumerate(P.ops) if o.op=='BMC' and str(o.operands[0])=='CfxSLP10OriginalDoExactMaskClipRAM117')
    patch=[Instr([],'q'),precise_instr([clipx,b['body'][1],b['body'][2]-clipx,b['body'][3]-b['body'][1]],'re'),Instr([],'W'),Instr([],'n'),precise_instr([x1-x0,0,0,y1-y0,x0,y0],'cm'),Instr([Name(nm)],'Do'),Instr([],'Q')]
    E.insert_instrs(9,tag,patch,before=True)
    axis=next(i for i,o in enumerate(P.ops) if o.op=='BMC' and str(o.operands[0])=='CfxSL6SL25SourceAxisCoreRestore1')
    assert P.ops[axis+2].op=='re'
    ax0=cv.to_page(1351,0)[0];ax1=cv.to_page(1354,0)[0]
    axisbox=[ax0,b['body'][1],ax1,b['body'][3]]
    E.modify_instr(9,axis+2,precise_instr([ax0,b['body'][1],ax1-ax0,b['body'][3]-b['body'][1]],'re'))
    content=E.build(9);E.doc.set_page_content(9,content);E.pages.clear()
    for q in (E.dels,E.ins,E.mods):q.pop(9,None)
    assert E.build(9)==content
    r.update(method='Second/final C2-head sample; source-axis complete core+halo restored through1354 and vertical clip uses original body; gray JPEG cap pixels cleaned sparsely from source-grid profiles.',
        source_axis_restore_page_box=axisbox,source_axis_restore_native_box=[1351,cv.to_px(0,b['body'][3])[1],1354,cv.to_px(0,b['body'][1])[1]],
        cleared_only_applied_M1_deferred_edits=applied,deferred_queue_fix_before_second_visual_sample=True,head_cleanup=dict(source_zones10=zones,native_bbox=bb,new_image_name=str(nm),sparse_changed_pixel_count=int(mask.sum()),unchanged_native_axis_columns1351_1353=True,
            all_changed_coordinates=[[int(x),int(y)] for x,y in zip(xx,yy)],alpha_SHA256=hashlib.sha256(alpha.tobytes()).hexdigest(),new_pixels_SHA256=hashlib.sha256(pixels.tobytes()).hexdigest(),
            source_profile_based_no_white_rectangle=True,extra_patch_after_M2_table_before_all_new_curves=True),
        new_C2_curves_unchanged_from_first_RAM=True,sample_number=2,maximum_samples_this_method=2,content_SHA256=hashlib.sha256(content).hexdigest())
    return j,r,before,clean,content
