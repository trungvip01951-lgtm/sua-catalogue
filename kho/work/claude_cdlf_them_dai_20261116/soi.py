import pymupdf, sys
def spans(p, clip=None):
    out=[]
    for b in p.get_text('dict', clip=clip)['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                if s['text'].strip(): out.append(s)
    return out
def show(ss, mx=80):
    for s in ss[:mx]: print(f"{s['bbox'][0]:6.1f} {s['bbox'][1]:6.1f} {s['bbox'][2]:6.1f} {s['bbox'][3]:6.1f} sz{s['size']:.1f} {'B' if 'Bold' in s['font'] or 'Black' in s['font'] else 'R'} #{s['color']:06x} | {s['text'][:34]}")
def fills(p, clip, mx=30):
    n=0
    for x in p.get_drawings():
        r=x['rect']
        if not r.intersects(clip): continue
        n+=1
        if n<=mx: print(x['type'], [round(v,1) for v in r], 'c',None if x.get('color') is None else '#%02x%02x%02x'%tuple(int(v*255) for v in x['color']), 'f',None if x.get('fill') is None else '#%02x%02x%02x'%tuple(int(v*255) for v in x['fill']), 'w',round(x.get('width') or 0,2))
    print('drawings',n)
