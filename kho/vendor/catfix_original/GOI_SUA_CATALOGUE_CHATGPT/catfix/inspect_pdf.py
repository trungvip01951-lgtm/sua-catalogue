"""Know the file before editing: page types and what is drawn at a given place.

    print(summary('in.pdf'))              # one line per page: type, images, fonts, text ops
    what_is_at('in.pdf', 8, (505, 505, 540, 520))   # -> which tool to use for that spot
"""
import collections

from .vector import Editor, FILL_OPS, overlap
from .raster import Raster
from .textlayer import TextLayer


def page_info(E, pi, R=None, TL=None):
    P = E.page(pi)
    mb = E.mediabox(pi)
    area = (mb[2] - mb[0]) * (mb[3] - mb[1])
    R = R or Raster(E)
    ims = R.images(pi)
    big = [im for im in ims if not im.textclip and (im.page_bbox[2] - im.page_bbox[0]) * (im.page_bbox[3] - im.page_bbox[1]) >= 0.8 * area]
    fills = [o for o in P.objs if o['op'] in FILL_OPS]
    small_fills = sum(len(o['subs']) for o in fills if (o['bbox'][3] - o['bbox'][1]) < 40)
    TL = TL or TextLayer(E)
    runs = TL.runs(pi)
    vis = [r for r in runs if r.tr not in (3, 7)]
    nvis = sum(len(r.glyphs) for r in vis)
    ninv = sum(len(r.glyphs) for r in runs if r.tr in (3, 7))
    kinds = []
    if big:
        kinds.append('ẢNH CẢ TRANG')
    if nvis > 20:
        kinds.append('CHỮ THẬT')
    if small_fills > 300:
        kinds.append('CHỮ NÉT VẼ')
    if not kinds:
        kinds.append('ÍT NỘI DUNG / HÌNH')
    return dict(page=pi + 1, size=tuple(round(v, 1) for v in mb), kinds=kinds, images=len(ims),
                big_images=[(im.name, im.W, im.H, round(im.dpi)) for im in big], text_glyphs=nvis, hidden_text_glyphs=ninv,
                vector_subpaths=small_fills, fonts=sorted(set(r.font.family for r in runs if r.font)))


def summary(path):
    E = Editor(path)
    try:
        R = Raster(E)
        TL = TextLayer(E)
        lines = []
        for pi in range(E.n_pages):
            i = page_info(E, pi, R, TL)
            lines.append('Trang %2d %s | %s | ảnh=%d %s | chữ thật=%d (ẩn %d) | nét vẽ=%d | font=%s' % (
                i['page'], i['size'][2:], ' + '.join(i['kinds']), i['images'], i['big_images'] or '', i['text_glyphs'],
                i['hidden_text_glyphs'], i['vector_subpaths'], ', '.join(i['fonts'][:6])))
        return '\n'.join(lines)
    finally:
        E.close()


def what_is_at(path, pi, rect, E=None):
    """list what is drawn in rect (page coords) and recommend the editing tool."""
    own = E is None
    E = E or Editor(path)
    try:
        P = E.page(pi)
        R = Raster(E)
        TL = TextLayer(E)
        res = collections.OrderedDict()
        tg = [g for g in TL.glyphs(pi, visible_only=True) if overlap(g.bbox, rect) > 0]
        res['text_layer'] = (''.join(g.ch for g in tg)[:80], sorted(set(g.run.font.family for g in tg if g.run.font)))
        vo = [oi for oi in P.objects_in(rect) if P.objs[oi]['op'] in FILL_OPS and (P.objs[oi]['bbox'][3] - P.objs[oi]['bbox'][1]) < 40]
        res['vector_glyph_objects'] = vo[:20]
        try:
            im = R.image_at(pi, rect)
            res['image'] = repr(im)
        except ValueError:
            res['image'] = None
        if tg:
            rec = 'TextLayer (chữ thật): TL.find / TL.replace'
        elif vo:
            rec = 'OutlineText (chữ nét vẽ): T.learn([trang]); T.find / T.replace'
        elif res['image']:
            rec = 'Raster: R.canvas(image) hoặc R.render_canvas(...) rồi R.find / R.replace_word'
        else:
            rec = 'Không thấy chữ - xem lại toạ độ'
        res['recommend'] = rec
        return dict(res)
    finally:
        if own:
            E.close()
