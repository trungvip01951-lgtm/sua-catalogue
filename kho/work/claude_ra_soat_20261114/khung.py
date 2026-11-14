# -*- coding: utf-8 -*-
"""Khung HTML báo cáo rà soát: build(data) -> chuỗi HTML tự chứa (không tải gì từ mạng)."""
import html
e = html.escape
CSS = r'''
:root{--bg:#f6f4f1;--card:#ffffff;--ink:#22262b;--mut:#5d646d;--line:#ddd7d1;--acc:#a31a1f;--acc2:#2b2e33;--ok:#1d6b45;--okbg:#e3f1e9;--warn:#8a5a00;--warnbg:#fbf0d6;--bad:#a31a1f;--badbg:#f8e3e3;--chip:#eeeae6;--sel:#fff6f6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17191c;--card:#202328;--ink:#e9e6e2;--mut:#a6adb5;--line:#383d44;--acc:#ef7a7f;--acc2:#e9e6e2;--ok:#7fd1a5;--okbg:#1d3529;--warn:#f0c36a;--warnbg:#3a3018;--bad:#ef7a7f;--badbg:#3d2224;--chip:#2c3036;--sel:#2c2325}}
:root[data-theme="dark"]{--bg:#17191c;--card:#202328;--ink:#e9e6e2;--mut:#a6adb5;--line:#383d44;--acc:#ef7a7f;--acc2:#e9e6e2;--ok:#7fd1a5;--okbg:#1d3529;--warn:#f0c36a;--warnbg:#3a3018;--bad:#ef7a7f;--badbg:#3d2224;--chip:#2c3036;--sel:#2c2325}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;padding-bottom:120px}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px}
header{background:var(--acc2);color:#fff;padding:28px 0 22px;border-bottom:5px solid var(--acc)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) header{background:#101214;color:#e9e6e2}}
:root[data-theme="dark"] header{background:#101214;color:#e9e6e2}
header .k{font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.75}
h1{font-size:27px;line-height:1.25;margin:6px 0 8px;text-wrap:balance}
header p{margin:0;opacity:.85;max-width:70ch}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0 6px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.tile b{display:block;font-size:30px;line-height:1.1;font-variant-numeric:tabular-nums}
.tile span{color:var(--mut);font-size:13.5px}
.tile.ok b{color:var(--ok)}.tile.warn b{color:var(--warn)}.tile.bad b{color:var(--bad)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0}
nav .wrap{display:flex;gap:8px;overflow-x:auto}
nav a{white-space:nowrap;text-decoration:none;color:var(--ink);background:var(--chip);padding:6px 12px;border-radius:999px;font-size:14px}
nav a:hover{outline:2px solid var(--acc)}
h2{font-size:21px;margin:38px 0 4px;padding-top:8px;text-wrap:balance;scroll-margin-top:56px}
h2 small{font-weight:400;color:var(--mut);font-size:14px;margin-left:6px}
.lead{color:var(--mut);margin:0 0 14px;max-width:80ch}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
th,td{padding:9px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);background:var(--chip);white-space:nowrap}
tr:last-child td{border-bottom:0}
td.n{font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--mut)}
code{font:13px/1.4 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:var(--chip);padding:1px 5px;border-radius:4px;word-break:break-word}
.tag{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.tag.ok{background:var(--okbg);color:var(--ok)}.tag.warn{background:var(--warnbg);color:var(--warn)}.tag.bad{background:var(--badbg);color:var(--bad)}.tag.mut{background:var(--chip);color:var(--mut)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:14px 0}
.card h3{margin:0 0 6px;font-size:17px;line-height:1.35;text-wrap:balance}
.card h3 .id{color:var(--acc);font-variant-numeric:tabular-nums;margin-right:6px}
.card p{margin:6px 0}
.card .why{color:var(--mut);font-size:14.5px}
.opts{display:grid;gap:8px;margin-top:10px}
.opt{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:9px;padding:9px 12px;cursor:pointer}
.opt:hover{border-color:var(--acc)}
.opt input{margin-top:4px;accent-color:var(--acc);width:17px;height:17px;flex:none}
.opt:has(input:checked){border-color:var(--acc);background:var(--sel)}
.opt b{font-variant-numeric:tabular-nums}
.opt small{display:block;color:var(--mut);font-size:13.5px}
.rec{color:var(--ok);font-weight:600;font-size:12.5px;margin-left:6px;white-space:nowrap}
.bar{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:2px solid var(--acc);padding:10px 0;z-index:9}
.bar .wrap{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.bar label{font-size:13px;color:var(--mut)}
#ans{flex:1 1 320px;min-width:0;font:14px ui-monospace,Menlo,Consolas,monospace;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
button{font:600 14px system-ui,sans-serif;padding:9px 14px;border-radius:8px;border:1px solid var(--acc);background:var(--acc);color:#fff;cursor:pointer}
button.ghost{background:transparent;color:var(--acc)}
:root[data-theme="dark"] button:not(.ghost){color:#17191c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) button:not(.ghost){color:#17191c}}
.note{font-size:13.5px;color:var(--mut)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
ul.tight{margin:6px 0;padding-left:20px}ul.tight li{margin:3px 0}
@media (max-width:560px){h1{font-size:22px}body{font-size:15px}th,td{padding:7px 8px}}
@media (max-width:560px){.bar{padding:7px 0}.bar .wrap{gap:6px}.bar label{display:none}#ans{flex-basis:100%;padding:6px 8px;font-size:12.5px}.bar button{padding:7px 9px;font-size:12.5px;flex:1 1 auto}body{padding-bottom:110px}}
'''
JS = r'''
const ans=document.getElementById('ans');
function upd(){const p=[];document.querySelectorAll('.card[data-id]').forEach(c=>{const r=c.querySelector('input:checked');if(r)p.push(c.dataset.id+'.'+r.value)});ans.value=p.length?('Duyệt rà soát 14/11: '+p.join('  ')):'';try{localStorage.setItem('rs1411',JSON.stringify(p))}catch(e){}}
document.addEventListener('change',e=>{if(e.target.matches('.opt input'))upd()});
try{(JSON.parse(localStorage.getItem('rs1411')||'[]')).forEach(s=>{const i=s.lastIndexOf('.');const el=document.querySelector('.card[data-id="'+s.slice(0,i)+'"] input[value="'+s.slice(i+1)+'"]');if(el)el.checked=true})}catch(e){}
upd();
document.getElementById('rec').onclick=()=>{document.querySelectorAll('.card[data-id]').forEach(c=>{const r=c.querySelector('input[data-rec]');if(r)r.checked=true});upd()};
document.getElementById('clr').onclick=()=>{document.querySelectorAll('.opt input').forEach(r=>r.checked=false);upd()};
document.getElementById('cp').onclick=async()=>{ans.select();let ok=false;try{await navigator.clipboard.writeText(ans.value);ok=true}catch(e){try{ok=document.execCommand('copy')}catch(_){}}const b=document.getElementById('cp');b.textContent=ok?'Đã chép':'Bôi đen ô bên trái rồi chép';setTimeout(()=>b.textContent='Chép câu trả lời',2500)};
'''
def table(head, rows, cls=''):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td{" class=n" if i == 0 else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tbl {cls}"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def card(c):
    o = ''
    for i, (lab, sub) in enumerate(c['opts'], 1):
        rec = i == c.get('rec')
        o += (f'<label class="opt"><input type="radio" name="{c["id"]}" value="{i}"{" data-rec" if rec else ""}>'
              f'<span><b>{i}.</b> {lab}{"<span class=rec>em đề xuất</span>" if rec else ""}{f"<small>{sub}</small>" if sub else ""}</span></label>')
    return (f'<div class="card" data-id="{c["id"]}"><h3><span class="id">{c["id"]}</span>{c["t"]}</h3>'
            f'<p>{c["now"]}</p>' + (f'<p class="why">{c["why"]}</p>' if c.get('why') else '') + f'<div class="opts">{o}</div></div>')
def build(d):
    nav = ''.join(f'<a href="#{i}">{t}</a>' for i, t in d['nav'])
    tiles = ''.join(f'<div class="tile {k}"><b>{v}</b><span>{t}</span></div>' for k, v, t in d['tiles'])
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rà soát dự án Sửa catalogue</title><style>{CSS}</style></head><body>
<header><div class="wrap"><div class="k">{d["kicker"]}</div><h1>{d["title"]}</h1><p>{d["sub"]}</p></div></header>
<div class="wrap"><div class="tiles">{tiles}</div></div>
<nav><div class="wrap">{nav}</div></nav>
<div class="wrap">{d["body"]}</div>
<div class="bar"><div class="wrap"><label for="ans">Câu trả lời của anh</label><input id="ans" readonly placeholder="Chọn phương án ở các mục B… rồi chép dòng này gửi lại trong khung chat"><button id="cp">Chép câu trả lời</button><button class="ghost" id="rec">Chọn hết theo đề xuất</button><button class="ghost" id="clr">Bỏ chọn</button></div></div>
<script>{JS}</script></body></html>'''
