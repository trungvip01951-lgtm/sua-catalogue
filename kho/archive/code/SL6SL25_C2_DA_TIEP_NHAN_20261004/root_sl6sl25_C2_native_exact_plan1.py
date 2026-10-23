"""Ten exact C2 cubic-spline paths fitted to already-locked120 table points.
No Editor, raster editing, PDF save or canonical mutation.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone
import uuid,json,hashlib,numpy as np
from scipy.optimize import linprog
from scipy.interpolate import BSpline
from catwork import start,HERE

def frac(v):return v if isinstance(v,F) else F(str(v))
def basis(i,k,t,knots):
    if k==0:return F(int(knots[i]<=t<knots[i+1] or t==knots[-1] and knots[i]<t==knots[i+1]))
    s=F(0);a=knots[i+k]-knots[i];b=knots[i+k+1]-knots[i+1]
    if a:s+=(t-knots[i])/a*basis(i,k-1,t,knots)
    if b:s+=(knots[i+k+1]-t)/b*basis(i+1,k-1,t,knots)
    return s
def deriv(i,k,t,knots):
    a=knots[i+k]-knots[i];b=knots[i+k+1]-knots[i+1];v=F(0)
    if a:v+=k/a*basis(i,k-1,t,knots)
    if b:v-=k/b*basis(i+1,k-1,t,knots)
    return v
def interp(value,xs,ys):
    assert xs[0]<=value<=xs[-1],(value,xs[0],xs[-1])
    if value==xs[-1]:return ys[-1]
    for x0,x1,y0,y1 in zip(xs,xs[1:],ys,ys[1:]):
        if x0<=value<=x1:return y0+(y1-y0)*(value-x0)/(x1-x0)
    raise AssertionError(value)
def bezier(c,t):return sum(c[i]*(1-t)**(3-i)*t**i*n for i,n in enumerate((1,3,3,1)))
def pack(v):return str(v)

def main():
    S,_,_=start();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text(encoding='utf8'))
    bp=Path(S.report('G04/SL6SL25 SUA BANG VA10 DUONG THEO QUY TAC MOI/UNG VIEN SUA BANG VA10 DUONG MAU2/TAO UNG VIEN MAU2 CO GUARD NGUON.json'));b=read(bp)
    guarded={str(bp):sha(bp),str(Path(__file__)):sha(Path(__file__))}
    for p,h in ((b['source'],b['source_SHA256']),(b['input'],b['input_SHA256']),(b['candidate'],b['candidate_SHA256']),(b['plan_file'],b['plan_SHA256']),(b['axes_file'],b['axes_SHA256'])):assert sha(p)==h;guarded[p]=h
    plan=read(b['plan_file']);assert plan['proposed_changed_H_cells']==26 and len(plan['proposals'])==10
    hs=list(map(frac,[a['H'] for a in b['H_local']]));ys=list(map(frac,[a['page_y'] for a in b['H_local']]));records=[]
    HtoY=lambda H:float(interp(frac(H),hs,ys))
    for r in b['model_paths']:
        proposal=next(p for p in plan['proposals'] if p['model']==r['model']);assert r['H_new']==proposal['H_integer_proposed']
        anchors=[tuple(map(frac,p)) for p in r['local_page_anchors']];xx=[p[0] for p in anchors];x0,xn=xx[0],xx[-1];y0,yn=anchors[0][1],anchors[-1][1]
        tf=[(x-x0)/(xn-x0) for x in xx];knots=[F(0)]*4+[tf[i] for i in (2,5,8)]+[F(1)]*4
        B=BSpline.design_matrix(np.array(list(map(float,tf))),np.array(list(map(float,knots))),3).toarray();Binside=B[:,1:-1];fixed=B[:,0]*float(y0)+B[:,-1]*float(yn)
        H=list(map(frac,r['H_new']));tol=[max(F(1),h/50) for h in H];mid=np.array([HtoY(h) for h in H]);lo=np.array([HtoY(h-t) for h,t in zip(H,tol)]);hi=np.array([HtoY(h+t) for h,t in zip(H,tol)])
        n=Binside.shape[1];m=np.zeros((n-1,n+1))
        for i in range(n-1):m[i,i]=-1;m[i,i+1]=1
        A=np.vstack([np.c_[Binside,-(hi-mid)],np.c_[-Binside,-(mid-lo)],m]);rhs=np.r_[mid-fixed,-mid+fixed,np.zeros(n-1)]
        sol=linprog(np.r_[np.zeros(n),1],A_ub=A,b_ub=rhs,bounds=[(float(yn),float(y0))]*n+[(0,None)],method='highs');assert sol.success and sol.x[-1]<1,(r['model'],sol)
        c=[y0]
        for z in sol.x[:-1]:
            v=frac(float(z)).limit_denominator(10**10)
            if abs(float(v-c[-1]))<1e-10:v=c[-1]
            if abs(float(v-yn))<1e-10:v=yn
            assert c[-1]>=v>=yn;c.append(v)
        c.append(yn)
        value=lambda t:sum(c[i]*basis(i,3,t,knots) for i in range(len(c)))
        slope=lambda t:sum(c[i]*deriv(i,3,t,knots) for i in range(len(c)))
        breaks=[F(0),tf[2],tf[5],tf[8],F(1)];segments=[];native=[]
        for a,z in zip(breaks,breaks[1:]):
            yy=[value(a),value(a)+(z-a)*slope(a)/3,value(z)-(z-a)*slope(z)/3,value(z)]
            xxx=[x0+(xn-x0)*(a+(z-a)*j/3) for j in range(4)]
            assert all(yy[i]>=yy[i+1] for i in range(3)) and yy[0]>yy[3]
            native.append([[xxx[j],yy[j]] for j in range(4)])
            segments.append(dict(t0=pack(a),t1=pack(z),controls_page_fraction=[[pack(x),pack(y)] for x,y in native[-1]],dy_dlocalt_controls_fraction=[pack(3*(yy[j+1]-yy[j])) for j in range(3)],strict_decrease_every_open_interval=True))
        joins=[]
        for left,right in zip(native,native[1:]):
            wl=left[3][0]-left[0][0];wr=right[3][0]-right[0][0]
            dl=3*(left[3][1]-left[2][1])/wl;dr=3*(right[1][1]-right[0][1])/wr
            ddl=6*(left[3][1]-2*left[2][1]+left[1][1])/wl**2;ddr=6*(right[2][1]-2*right[1][1]+right[0][1])/wr**2
            assert left[3]==right[0] and dl==dr and ddl==ddr
            joins.append(dict(C0_exact=True,C1_exact=True,C2_exact=True,page_x=pack(left[3][0]),dy_dx=pack(dl),d2y_dx2=pack(ddl)))
        checked=[]
        for q,h,t,x in zip(r['Q'],H,tf,xx):
            y=value(t);hh=interp(y,ys,hs);error=abs(hh-h);tolerance=max(F(1),h/50);assert error<=tolerance
            si=next(i for i,(a,z) in enumerate(zip(breaks,breaks[1:])) if a<=t<=z);a,z=breaks[si:si+2];local=(t-a)/(z-a)
            assert bezier([pt[0] for pt in native[si]],local)==x and bezier([pt[1] for pt in native[si]],local)==y
            checked.append(dict(Q=q,H_table=int(h),actual_plan_H_fraction=pack(hh),delta_H_fraction=pack(hh-h),tolerance_fraction=pack(tolerance),ratio=float(error/tolerance),segment=si,page_x=pack(x),page_y=pack(y),PASS=True))
        assert value(F(0))==anchors[0][1] and value(F(1))==anchors[-1][1]
        records.append(dict(model=r['model'],Q=r['Q'],H_source=r['H_source'],H_locked=r['H_new'],knots_fraction=list(map(pack,knots)),spline_controls_y_fraction=list(map(pack,c)),segments4=segments,C2joins3=joins,anchors12_checked=checked,
            first_last_table_endpoints_exact=True,all4_segment_derivatives_strict_inside=True,all12_H_errors_within_general6b=True,split_dashed_solid_at_exact_Q6=True,
            source_extrema_physical_not_inferred=True,LP_ratio=float(sol.x[-1]),exact_fraction_max_ratio=max(row['ratio'] for row in checked)))
    for p,h in guarded.items():assert sha(p)==h
    out=Path(S.report('G04'))/('ROOT SL6SL25 PLAN10 C2 EXACT120 '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir(exist_ok=False)
    report=dict(status='PASS_PURE_PLAN10_C2_120_ANCHORS_NO_RAM_NO_PDF',method='Cubic B-spline with common simple knots Q6/Q15/Q24; monotone controls chosen by bounded linear program, then exact rational Bezier conversion and C0/C1/C2+full derivative proofs.',
        prior_M2_manifest=str(bp),prior_M2_manifest_SHA256=sha(bp),records10=records,curve_count=10,segments_count=40,anchor_count=120,table_changed26_held94=True,all_source_style_and_glyphs_to_reuse_unchanged=b['style'],
        numeric_max_ratio=max(r['exact_fraction_max_ratio'] for r in records),original_authorized_chart_body=b['body'],
        Q0_actual_page_x=b['Q_local'][0]['page_x'],Q0_correct_native_u_live_source=1352.5,Q0_stale_axes_native_u=1353.5,
        current_old_clip_native_left=1357,head_fix_requires_separate_vector_clip_and_source_frame_validation=True,
        original_source_unchanged=True,current_unchanged=True,Editor_instances=0,PDF_saves=0,canonical_ledger_index_controls_writes=0,guarded_files=guarded,full_G04_complete=False,
        limits='This is mathematical plan acceptance only. RAM actual contents,20path geometry/styles,caption placement,source frame all changed pixels,old source-cap fragments and protected regions still require inspection. No physical manufacturer extrema or duty point invented.')
    jp=out/'01 SL10 C2 FRACTION40 SEGMENTS120 ANCHORS PLAN.json'
    with jp.open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
    assert read(jp)==report
    print(json.dumps(dict(path=str(jp),SHA256=sha(jp),max_ratio=report['numeric_max_ratio'],curves10=10,C2joins30=30,anchors120=120,no_RAM=True,no_PDF=True),ensure_ascii=False))
if __name__=='__main__':main()
