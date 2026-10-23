"""ROOT scoped review of actual2 and append-only corrected visual evidence.
No PDF write, candidate3, or assertion that source raster text is sharpened.
"""
import json
from pathlib import Path
import root_SP77_static15_material_20261006 as M
R=M.R;D=R/'ROOT8SP77 ONE CATFIX SOURCE SUFFIX CANDIDATE2'
E={
 D/'07 SAVED CANDIDATE RECEIPT.json':'6ae6ee8445e8a0e0886914f287b1fad913a46da89be0fdae2bceacfd03f59dd4',
 D/'08 ROOT FRESH READ27 PEN15 NO ADOPT.json':'28a337e24952f98865baa81cd60f297dafe368b117400f0a72d6e7a066b1de01',
 R/'INDEPENDENT SP77 ACTUAL2 SAVED GRAPH PIXELS READONLY 20261005T191033Z/01 OWN ACTUAL2 GRAPH225 RAW196 KEEPER6 OUTSIDE24.json':'80be122f5f580b686b24df59a6e49cab44aa71c5653d2a9ee19d3c9ddbfdbbb9',
 R/'SOL SP77 SAMPLE2 TABLE RETAINED READONLY 20261005T191041Z/01 SAMPLE2 TABLE135 RETAINED BANK11 RAW NO ADOPT.json':'e0df9737908203afab4825197572ca009b8e13c87717e7d009e9d5ca307a4d0a',
 R/'SOL SP77 ACTUAL2 GLYPH1 GRID DIAGNOSTIC READONLY 20261005T191714Z/01 SOURCE1 ACTUAL3 GRID CLIP DIAGNOSTIC NO ADOPT.json':'5baf9df7159a16a469e9843104323fbc1fb4ec4527a659b2b56140d75dc8b63a',
 R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/01 INDEPENDENT SP77 SAMPLE2 VISUAL READONLY.json':'1b0e70966c3fdd2d1cd2c318cf0cd22d750909b85f0c2a604b91cb6da4615057',
 R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/02 ADDENDUM GLYPH1 SOURCE VS GRID PIXELS.json':'7e3b5c39a67e8c00daa604150e1bc827aa19c8d97dc35a1d3999aacc3964e5df',
 R/'INDEPENDENT SP77 LAST2 INSET GRID CLIP READONLY 20261005T190603Z/01 OWN LAST2 STATIC70 PEN15 GRID15 CLIP SOURCE HELD.json':'93819e4142bca3a484fc05e6067212c18618ffe5b5bbe617d77aaf5a77c7d22d',
 R/'ROOT8SP77 FINAL SAMPLE2 STATIC INSET GRID LABEL HOLES/01 EXPLICIT LAST2 STATIC NO PDF.json':'052e8f8954ce15b4192d997724de3a15a875cf8c64220148aa89bb381729fc9d'}
def main():
 guards={str(p):h for p,h in E.items()};M.guard(guards)
 r=M.rd(D/'07 SAVED CANDIDATE RECEIPT.json');own=M.rd(D/'08 ROOT FRESH READ27 PEN15 NO ADOPT.json')
 p=M.rd(R/'ROOT8SP77 FINAL SAMPLE2 STATIC INSET GRID LABEL HOLES/01 EXPLICIT LAST2 STATIC NO PDF.json');M.guard(p['guards'])
 v=M.rd(R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/01 INDEPENDENT SP77 SAMPLE2 VISUAL READONLY.json')
 add=M.rd(R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/02 ADDENDUM GLYPH1 SOURCE VS GRID PIXELS.json')
 assert r['candidate_SHA256']=='48c8535c4c8a025991be53caf414242cbb500eb43ac59f804a2008204691a6a2'
 assert add['status'].startswith('CORRECTED_ATTRIBUTION_NO_GRIDLINE_IN_INTERDIGIT_GAP')
 assert v['capture_manifest']['opened_and_rehashed_count']==27 and own['ROOT_manually_opened_all27_saved']
 assert all(z['fresh_vs_writer_changed']==z['fresh_vs_writer_maxdelta']==0 for z in own['fresh_actual_captures27'])
 assert len(own['visible_pen15'])==15 and all(z['PASS_representative_ink']for z in own['visible_pen15'])
 assert all(z['changed_pixels']==z['maximum_delta']==0 for z in r['keepers'])and len(r['keepers'])==6
 assert all(z['strict0_pad0_pixels']==z['strict0_max_delta']==0 for z in r['outside24'])and len(r['outside24'])==24
 assert len(p['labels15'])==15 and not p['obstacles']and all(z['unique_nearest_owner']for z in p['labels15'])
 assert r['operations']['actual_same_method_attempts']==2 and r['operations']['Save_calls']==1
 for x in own['fresh_actual_captures27']:guards[x['path']]=x['SHA256']
 for k in('native','font_native','table_native','new_grid','new_curves'):
  guards[p[k]['path']]=p[k]['SHA256']
 guards[r['candidate']]=r['candidate_SHA256'];guards[str(__file__)]=M.sha(__file__)
 z={'status':'ROOT_ACCEPT_SAVED2_8SP77_P9_CURVE15_TABLE7_ORIGINAL137_HELD_SCOPED_ONLY',
  'allow_adopt_exact_saved_candidate':True,'candidate':r['candidate'],'candidate_SHA256':r['candidate_SHA256'],
  'current_before_SHA256':r['current_SHA256'],'source_SHA256':r['source_SHA256'],
  'ROOT_opened_saved27':True,'keeper6_actual_pixel0':True,'outside24_actual_pixel0':True,'visual_scoped_pass':True,
  'evidence_guards':guards,'ROOT_scope_visual':{
   'curves':'All15 smooth/strict Q increase/H decrease; literal same pen and15 actual profiles within0.12pt predefined one600pixel tolerance, range0.7684..0.7886pt.',
   'labels':'ROOT recognizes all15 suffixes2/3/4/5/6/7/8/9/10/12/14/16/18/20/22 under held8SP77 title. No visible stroke-letter collision. Source bitmap fringe remains, not claimed sharpened.',
   'table7':'39/59/79/200/240/280/38 read correctly. All7natural source parts held actual1→2; independent135table verdict carried once.',
   'preservation':'Title/axes/ETA/leftphoto held,keepers6/outside24 exact0 from independent andROOT saved reads.'},
  'visual_old_diagnostic_superseded':{'initial_receipt':str(R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/01 INDEPENDENT SP77 SAMPLE2 VISUAL READONLY.json'),
   'correction_receipt':str(R/'INDEPENDENT SP77 SAMPLE2 VISUAL READONLY 20261006-LUNA/02 ADDENDUM GLYPH1 SOURCE VS GRID PIXELS.json'),
   'reason':'Original only stated grid between digits. Appended own source1/crop coordinates and independent198 exactRGB source-centres show this attribution incorrect; actualgridholes checked. Font-sharpness UNKNOWN retained, no criterion lowered or extra PDF.',
   'adoption_decider':'ROOT on all27 direct saved views +independent curve/title/table review and corrected diagnostic. Peers do not decide canonical adoption.'},
  'scope':{'page':9,'curves':15,'table_H':135,'changed_H_integer_cells':7,'unchanged_H':128,'ends_observed_table_held':30,
   'physical_segments_C2':56,'native_paint_cubics_Q24_split_only':70,'source_RGB_glyph_paints':37,'aliases11_oldnodes_only':11,
   'full_font_identity_phase_or_sharpness_PASS':False,'full_catalogue_complete':False,'original149_accepted':137},
  'limits':['Physical manufacturer extremes/duty UNKNOWN; observed tableends held.','Source JPEG fringe, exactfontfamily/phase/sharpening UNKNOWN.','SP36/46 and remainingSP/SL/newrequirements unaccepted.'],
  'operations':{'PDF_Save':0,'new_candidate3':0,'canonical':0,'control':0,'marker':0}}
 M.guard(guards);out=D/'09 ROOT SCOPED SAVED2 ACCEPT NO PUBLICATION.json'
 with out.open('x',encoding='utf8')as f:json.dump(z,f,ensure_ascii=False,indent=2);f.write('\n')
 print(json.dumps({'path':str(out),'SHA256':M.sha(out)},ensure_ascii=False))
if __name__=='__main__':main()
