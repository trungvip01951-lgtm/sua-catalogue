"""Pure array reconstruction and CATFIX RAM-only current-base graft helper.

No file IO, PDF open/save, Editor, renderer or module import side effects.
ROOT must review the recipe and all native/assets gates before calling this.
"""

def reconstruct_patches39_40(before, recipe):
    import numpy as np,zlib,hashlib
    old=recipe['original_cleaning_mask_recipe'];head=recipe['head_cleanup']
    assert before.shape==(1236,1738,3) and before.dtype==np.uint8
    cols=np.asarray(old['source_grid_column_profiles_native'])
    rows=np.asarray(old['source_grid_row_profiles_native'])
    assert cols.shape==(305,3) and rows.shape==(283,3)
    clean=before.copy();changed=np.asarray(old['changed_native_coordinates'],dtype=int)
    xx,yy=changed[:,0],changed[:,1]
    assert len(changed)==old['changed_native_pixels']==31100
    assert len({tuple(v) for v in changed})==len(changed)
    assert np.all((xx>=1357)&(xx<1656)&(yy>=188)&(yy<465)&~((xx>=1550)&(yy<216)))
    clean[yy,xx]=np.rint(np.minimum(cols[xx-1354],rows[yy-185])).clip(0,255).astype(np.uint8)
    # Caption cleanup follows the exact source-paper override of the builder,
    # after the curve-grid pass. Apply only frozen actual-change coordinates.
    for c in old['caption_recovery']:
        paper=np.asarray(c['actual_source_paper_RGB'],dtype=np.uint8)
        inside=np.zeros(len(changed),bool)
        for u0,v0,u1,v1 in c['native_erase_boxes']:
            inside|=(xx>=u0)&(xx<u1)&(yy>=v0)&(yy<v1)
        letter=inside&np.any(before[yy,xx]<paper-1,axis=1)
        clean[yy[letter],xx[letter]]=paper
    assert np.array_equal(np.stack([np.where(np.any(clean!=before,axis=2))[1],np.where(np.any(clean!=before,axis=2))[0]],axis=1),changed)
    # Patch40 is a separate source-profile replay. Its two sample hashes were
    # observed in the actual accepted RAM; both must match before any graft.
    clean40=before.copy();coords=np.asarray(head['all_changed_coordinates'],dtype=int)
    x40,y40=coords[:,0],coords[:,1]
    assert len(coords)==head['sparse_changed_pixel_count']==797
    bg=np.rint(np.minimum(cols[x40-1354],rows[y40-185])).clip(0,255).astype(np.uint8)
    assert np.all(np.mean(bg.astype(float)-before[y40,x40].astype(float),axis=1)>=4)
    clean40[y40,x40]=bg
    assert np.array_equal(np.stack([np.where(np.any(clean40!=before,axis=2))[1],np.where(np.any(clean40!=before,axis=2))[0]],axis=1),coords)
    def patch(name,bbox,a,xy):
        u0,v0,u1,v1=bbox;p=np.ascontiguousarray(a[v0:v1,u0:u1]);alpha=np.zeros((v1-v0,u1-u0),np.uint8)
        alpha[xy[:,1]-v0,xy[:,0]-u0]=255
        out={'name':name,'width':u1-u0,'height':v1-v0,'native_bbox':bbox,'pixels':p.tobytes(),'alpha':alpha.tobytes()}
        out.update(RGB_raw=zlib.compress(out['pixels'],9),SMask_raw=zlib.compress(out['alpha'],9))
        out.update({k+'_SHA256':hashlib.sha256(out[k]).hexdigest() for k in ('pixels','alpha','RGB_raw','SMask_raw')})
        return out
    p39=patch('CfxPatch39',old['patches'][0]['native_bbox'],clean,changed)
    p40=patch('CfxPatch40',head['native_bbox'],clean40,coords)
    assert p40['pixels_SHA256']==head['new_pixels_SHA256'] and p40['alpha_SHA256']==head['alpha_SHA256']
    return [p39,p40]

def graft_current_RAM_only(base, donor, native, patches, expected_old_xobject_names=('CfxPatch1','CfxPatch2','X18','X19')):
    """Mutate only CATFIX PdfDoc buffers; caller owns close/save and actual QA.

    base is current pikepdf PdfDoc; donor is guarded M2 pikepdf PdfDoc.
    Name registration uses CATFIX add_xobject_to_page, no direct PDF mutation.
    Existing page10 Resources and XObject must both be direct/unshared.
    """
    from catfix.cs import Name,Ref,parse
    import hashlib,copy
    assert base.backend==donor.backend=='pikepdf' and base.n_pages==donor.n_pages==11
    pi=9;pd=base.pdf.pages[pi].obj
    assert '/Resources' in pd and not pd.Resources.is_indirect
    assert '/XObject' in pd.Resources and not pd.Resources.XObject.is_indirect
    res0=copy.deepcopy([base.page_resources(p) for p in range(base.n_pages)])
    pg0=copy.deepcopy([base.page_dict(p) for p in range(base.n_pages)])
    content0=[base.page_content(p) for p in range(base.n_pages)]
    refs=[base.page_contents_refs(p) for p in range(base.n_pages)]
    assert len(refs[pi])==1 and isinstance(refs[pi][0],Ref)
    assert all(refs[pi][0] not in rs for p,rs in enumerate(refs) if p!=pi)
    xr=base.resolve(res0[pi]['XObject']);assert set(xr)==set(expected_old_xobject_names)
    di=donor.resolve(donor.page_resources(pi)['XObject'])
    names={str(i.operands[0]) for i in parse(native) if i.op=='Do'}
    assert names==set(expected_old_xobject_names)|{'CfxPatch'+str(k) for k in range(3,41)}
    held={n:(base.get(v),base.stream_raw(v)) for n,v in xr.items()}
    # The sole Contents ref must not alias an existing reachable asset stream.
    def reachable(v,seen):
        if isinstance(v,Ref):
            if v in seen:return
            seen.add(v);reachable(base.get(v),seen)
        elif isinstance(v,dict):
            for z in v.values():reachable(z,seen)
        elif isinstance(v,list):
            for z in v:reachable(z,seen)
    assets=set()
    for z in res0:reachable(z,assets)
    assert refs[pi][0] not in assets
    copied={};mapping=[]
    def image_copy(ref):
        if ref in copied:return copied[ref]
        d=donor.get(ref);raw=donor.stream_raw(ref)
        assert str(d.get('Type'))=='XObject' and str(d.get('Subtype'))=='Image'
        assert str(d['ColorSpace']) in ('DeviceGray','DeviceRGB') and d['BitsPerComponent']==8
        assert str(d['Filter'])=='FlateDecode' and not isinstance(d['Filter'],list)
        assert not any(isinstance(v,Ref) for k,v in d.items() if k!='SMask')
        sm=image_copy(d['SMask']) if 'SMask' in d else None
        known={'Type','Subtype','Width','Height','ColorSpace','BitsPerComponent','Filter','Length','Decode','DecodeParms','SMask'}
        extra={k:v for k,v in d.items() if k not in known}
        new=base.new_image_xobject(raw,d['Width'],d['Height'],d['ColorSpace'],d['BitsPerComponent'],str(d['Filter']),decode=d.get('Decode'),smask=sm,decode_parms=d.get('DecodeParms'),extra=extra)
        nd=base.get(new);expect=dict(d)
        if sm is not None:expect['SMask']=sm
        assert nd==expect,(ref,new,d,nd)
        assert base.stream_raw(new)==raw
        copied[ref]=new;return new
    # Frozen M2 contains exactly 26 table patches plus10 literal caption images.
    for k in range(3,39):
        name='CfxPatch'+str(k);assert name in di
        ref=image_copy(di[name]);got=base.add_xobject_to_page(pi,ref,prefix='CfxPatch');assert got==name,(got,name)
        mapping.append({'name':name,'old_M2_ref':list(di[name]),'new_current_base_ref':list(ref),'raw_held':True,'dictionary_held_except_new_SMask_ref':True})
    assert [p['name'] for p in patches]==['CfxPatch39','CfxPatch40']
    for p in patches:
        sm=base.new_image_xobject(p['SMask_raw'],p['width'],p['height'],Name('DeviceGray'),8,'FlateDecode')
        im=base.new_image_xobject(p['RGB_raw'],p['width'],p['height'],Name('DeviceRGB'),8,'FlateDecode',smask=sm)
        got=base.add_xobject_to_page(pi,im,prefix='CfxPatch');assert got==p['name']
        assert base.stream_raw(im)==p['RGB_raw'] and base.stream_raw(sm)==p['SMask_raw']
        mapping.append({'name':got,'new_current_base_ref':list(im),'new_SMask_ref':list(sm),'RGB_raw_SHA256':p['RGB_raw_SHA256'],'SMask_raw_SHA256':p['SMask_raw_SHA256']})
    # Keep existing Contents Ref105/0 rather than replacing the page dictionary.
    base.set_stream(refs[pi][0],native)
    assert base.page_contents_refs(pi)==refs[pi] and base.page_content(pi)==native
    res1=[base.page_resources(p) for p in range(base.n_pages)]
    for p in range(base.n_pages):
        assert base.page_contents_refs(p)==refs[p]
        if p!=pi:
            assert base.page_dict(p)==pg0[p] and res1[p]==res0[p] and base.page_content(p)==content0[p]
    assert {k:v for k,v in res1[pi].items() if k!='XObject'}=={k:v for k,v in res0[pi].items() if k!='XObject'}
    final=base.resolve(res1[pi]['XObject']);assert set(final)==names
    for n,(d,raw) in held.items():
        assert final[n]==xr[n] and base.get(final[n])==d and base.stream_raw(final[n])==raw
    pp=base.page_dict(pi);assert {k:v for k,v in pp.items() if k!='Resources'}=={k:v for k,v in pg0[pi].items() if k!='Resources'}
    return {'status':'RAM_GRAFT_CURRENT_BASE_ONLY_NOT_SAVED_NOT_VISUAL','current_Contents_ref_held':list(refs[pi][0]),'10_other_pages_resources_dicts_and_content_exact':True,
        'existing_page10_resources_refs_raw_dicts_held':True,'native_SHA256':hashlib.sha256(native).hexdigest(),'copied_M2_image_objects':len(copied),'registered_new_names':38,'mapping':mapping,'PDF_saves':0}
