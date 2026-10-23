"""ROOT gate for the second and last SP77 candidate. No PDF mutation."""
from pathlib import Path
import json
import root_SP77_gate_prepare_20261006 as G
R=G.R
OLD=R/'ROOT8SP77 ACTUAL1 GATE 20261005T185041Z-35d2a5/02 ROOT ONE CATFIX CANDIDATE GATE.json'
PLAN=R/'ROOT8SP77 FINAL SAMPLE2 STATIC INSET GRID LABEL HOLES/01 EXPLICIT LAST2 STATIC NO PDF.json'
QA=R/'INDEPENDENT SP77 LAST2 INSET GRID CLIP READONLY 20261005T190603Z/01 OWN LAST2 STATIC70 PEN15 GRID15 CLIP SOURCE HELD.json'
LOC=R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE1/LOCALIZED KEEPER READONLY/01 EXACT KEEPER DELTA LOCALIZATION NO PDF.json'
TABLE=R/'SOL SP77 SAVED TABLE135 SCOPED READONLY 20261005T185624Z/03 FINAL SAVED135 TABLE7 NUMERIC VISUAL SCOPED NO ADOPT.json'
MARGINS=R/'SOL SP77 FOUR SOURCE MARGINS READONLY 20261005T190135Z/02 FOUR MARGINS FINAL VISUAL READONLY NO CLIP DECISION.json'
def main():
 assert G.sha(OLD)=='0d93f8604966e2dcefec5052f4fa918e2e4943d52dd41c030dcd6e8dea1a40b9'
 assert G.sha(PLAN)=='052e8f8954ce15b4192d997724de3a15a875cf8c64220148aa89bb381729fc9d'
 assert G.sha(QA)=='93819e4142bca3a484fc05e6067212c18618ffe5b5bbe617d77aaf5a77c7d22d'
 old=G.rd(OLD);p=G.rd(PLAN);q=G.rd(QA)
 assert p['second_last_same_method']is True and p['actual_same_method_attempts']==1 and p['next_actual_ordinal']==2
 assert not p['obstacles']and all(v['PASS_positive_gap']for v in p['gaps225'])
 for path,h in p['guards'].items():assert G.sha(path)==h,('INPUT_CHANGED',path)
 writer=Path(__file__).with_name('root_SP77_final2_one_candidate_20261006.py')
 guards={str(PLAN):G.sha(PLAN),str(QA):G.sha(QA),str(writer):G.sha(writer),str(__file__):G.sha(__file__)}
 for path in(LOC,TABLE,MARGINS,Path(old['marker_path'])):guards[str(path)]=G.sha(path)
 for receipt in old['font_style_receipts']:guards[receipt['path']]=receipt['SHA256'];assert G.sha(receipt['path'])==receipt['SHA256']
 out=PLAN.parent/'02 ROOT LAST2 AUTHORING GATE.json'
 z={'allow_one_candidate':True,'canonical':False,'maximum_Save_calls':1,'actual_ordinal':2,'maximum_same_method_samples':2,
  'plan':str(PLAN),'plan_SHA256':G.sha(PLAN),'writer':str(writer),'writer_SHA256':G.sha(writer),
  'marker_success':True,'marker_path':old['marker_path'],'marker_SHA256':old['marker_SHA256'],'marker_already_once_not_repeated':True,
  'ROOT_font_style_scoped_selected':True,'font_style_receipts':old['font_style_receipts'],
  'independent_static_QA':G.rec(QA),'independent_static_status':q.get('status'),'guards':guards,
  'ROOT_actual1_diagnosis':'Title visible before/saved; keeper differences at shared boundary. Source bitmap fringe remains; font identity and phase UNKNOWN. Layout Q24 through word gap failed.',
  'ROOT_last2_selection':'Inset original BODY, grid knockout full words via clip only. All frozen curve/table/font/style/anchor bytes held; same method second/last sample. No canonical adoption.',
  'finite_failure_rule':'Any actual2 failure closes this method2/2. No automatic retry, no widened keeper/threshold/ROI.',
  'source_table135_prior_scoped_PASS':G.rec(TABLE),'source_margin_scoped_read':G.rec(MARGINS)}
 print(json.dumps(G.write(out,z),ensure_ascii=False))
if __name__=='__main__':main()
