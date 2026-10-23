"""Exclusive receipts for ROOT-selected source-word prototype; no PDF API."""
import argparse,hashlib,json,uuid
from pathlib import Path
from datetime import datetime,timezone
R=Path(r'C:\Users\H2\Desktop\Catalog Sua\BẢN MỚI 03-10-2026 (ChatGPT)\_BAO CAO\G05')
PLAN=R/'ROOT8SP77 STATIC15 20261005T183933Z-ac1b75/02 FULL STATIC15 FONT15 TABLE7 NO PDF.json'
SHA='9f0cb528c849ae85a69f1745da5557da9d60608064325d311d33aabe0d309972'
SOL=R/'SOL SP77 BANK13 COMMON STYLE READONLY 20261005T183820Z-e7a5d9/04 FINAL BANK11 STYLE COMPATIBILITY ROOT SELECTION ONLY.json'
SOLS='b8d9939fe0c1b903e33e479000dedf57383793a2aefd58aa700848fc26adabe6'
VIEWED=[R/'SP25 FONT13 TWO RECTANGLE IDENTITY CORRECTION STATIC NO SAMPLE 20261004T160409Z-294421/00 ALL13 ORIGINAL SOURCE GLYPHS CORRECTED NN12.png',
 R/'SOL SP77 BANK13 COMMON STYLE READONLY 20261005T183820Z-e7a5d9/02 COMMON4 5 6 ORIGINAL RGB NN16 COMPARISON.png',
 R/'SOL 8SP77 SOURCE15 TABLE7 MATERIAL STATIC 20261005T182619Z-2c1b5d/CONTACT15 PROPOSED SUFFIX RGB NN16 DISPLAY ONLY.png',
 R/'8SP77 P9 AXES FRAME220 READONLY PROPOSAL/CHART AXES OWN ORIGINAL NN3.png']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rd(p):return json.loads(Path(p).read_text('utf8'))
def rec(p):return {'path':str(p),'SHA256':sha(p)}
def write(p,z):
 with p.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 return rec(p)
def main(marker,qa):
 assert sha(PLAN)==SHA and sha(SOL)==SOLS;plan=rd(PLAN);q=rd(qa)
 assert plan['status']=='ROOT_SELECTED_STATIC15_LABEL15_TABLE7_NO_PDF'and not plan['obstacles']
 assert len(plan['gaps225'])==225 and all(v['PASS_positive_gap']for v in plan['gaps225'])
 assert len(plan['labelpairs105'])==105 and all(v['PASS_positive']for v in plan['labelpairs105'])
 assert len(plan['labels15'])==15 and all(v['unique_nearest_owner']for v in plan['labels15'])
 for p,h in plan['guards'].items():assert sha(p)==h,('INPUT_CHANGED',p)
 out=R/('ROOT8SP77 ACTUAL1 GATE '+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);out.mkdir()
 root=write(out/'01 ROOT SOURCE FONT PROTOTYPE SELECTED NOT FULLFONT.json',{
  'status':'ROOT_SELECTED_ORIGINAL_SAME_FILE_BANK_ALL15_NATURAL_PITCH_FOR_ONE_ACTUAL_PROTOTYPE',
  'opened_in_this_turn':[rec(p)for p in VIEWED],'source_bank':plan['fontbank'],'same_style_support':rec(SOL),
  'reason':'Four original SP77 suffixes touch old curve cores. Reuse unchanged original same-file 0..9/hyphen RGB for every suffix; uniform material, no invention/refont/resize/rotation.',
  'ROOT_visual_observation':'All used bank numerals are readable, upright/slightly slanted sans shapes compatible with original SP77 common4/5/6. Natural body sizes comparable. No source font name or exact JPEG phase claim.',
  'limits':['Font family programme identity, phase, all catalogue sharpening UNKNOWN.','Static source compatibility is not actual layout/font acceptance; saved PDF must be inspected by ROOT and independent visual reviewer.','No canonical replacement allowed by this gate.'],
  'operations':{'Job':0,'PDF_save':0,'newfont':0,'image_edit':0,'canonical':0,'control':0}})
 writer=Path(__file__).with_name('root_SP77_one_candidate_20261006.py')
 g={'allow_one_candidate':True,'canonical':False,'maximum_Save_calls':1,'actual_ordinal':1,'maximum_same_method_samples':2,
  'plan':str(PLAN),'plan_SHA256':SHA,'writer':str(writer),'writer_SHA256':sha(writer),
  'marker_success':True,'marker_path':str(marker),'marker_SHA256':sha(marker),
  'ROOT_font_style_scoped_selected':True,'font_style_receipts':[rec(SOL),root],
  'independent_static_QA':rec(qa),'independent_static_status':q.get('status'),
  'guards':{str(PLAN):SHA,str(SOL):SOLS,root['path']:root['SHA256'],str(qa):sha(qa),str(writer):sha(writer),str(marker):sha(marker)},
  'scope':'Frozen56 physical/70 painted15 paths, source37glyph paints11aliases,7integer edits, original task49 and12pages held; no full catalogue completion.',
  'resource_allowed_changes':['Existing content160 payload/Length','Existing Page12 inlineXObject dictionary11aliases to existing source glyph nodes'],
  'actual_visual_gate':'PENDING; canonical=0; no automatic retry'}
 print(json.dumps(write(out/'02 ROOT ONE CATFIX CANDIDATE GATE.json',g),ensure_ascii=False))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('marker',type=Path);a.add_argument('qa',type=Path);z=a.parse_args();main(z.marker,z.qa)
