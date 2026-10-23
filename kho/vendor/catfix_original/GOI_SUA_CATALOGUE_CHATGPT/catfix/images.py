"""Image PLACEMENT edits (no pixel change): delete a drawn image, draw a copy of an image at
another place (optionally mirrored), mirror a group of images about a vertical axis.
Typical use: catalogue covers composed of several cut-out photos (CDLF covers).

    E = Editor('in.pdf'); R = Raster(E)
    ims = R.images(0)                         # list of PageImage with .name, .page_bbox
    delete_image(E, ims[5])
    clone_image(E, src=ims[2], dst_bbox=(289, 144, 343, 302), after=ims[4], keep_aspect='height')
    mirror_images(E, [ims[0], ims[1], ...], axis_x=308.5)
    E.save('out.pdf')
"""
import numpy as np

from . import cs
from .cs import Instr, Name


def _cm(Mx):
    return Instr([cs.Num(Mx[0, 0]), cs.Num(Mx[0, 1]), cs.Num(Mx[1, 0]), cs.Num(Mx[1, 1]), cs.Num(Mx[2, 0]), cs.Num(Mx[2, 1])], 'cm')


def delete_image(E, im):
    """remove one drawing of an image (its 'Do' and the clip/state block that only serves it)."""
    P = E.page(im.key)
    a, b = P.enclosing_block(im.index)
    E.delete_instrs(im.key, list(range(a, b + 1)))
    E.log.append(dict(page=im.key + 1 if isinstance(im.key, int) else str(im.key), kind='image-delete', image=im.name,
                      bbox=[round(v, 2) for v in im.page_bbox]))


def placement_matrix(dst_bbox, flip_h=False):
    """unit-square -> page matrix for an image filling dst_bbox (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = dst_bbox
    if flip_h:
        return np.array([[-(x1 - x0), 0, 0], [0, y1 - y0, 0], [x1, y0, 1.0]])
    return np.array([[x1 - x0, 0, 0], [0, y1 - y0, 0], [x0, y0, 1.0]])


def fit_bbox(src_bbox, target_bbox, keep_aspect='height', anchor='bottom-center'):
    """bbox for a copy of an image of size src_bbox placed into target_bbox.
    keep_aspect: 'height' (copy gets target height), 'width', or None (stretch).
    anchor: 'bottom-center' (feet on the same ground line), 'bottom-left', 'bottom-right', 'center'."""
    sw = src_bbox[2] - src_bbox[0]
    sh = src_bbox[3] - src_bbox[1]
    tx0, ty0, tx1, ty1 = target_bbox
    tw, th = tx1 - tx0, ty1 - ty0
    if keep_aspect == 'height':
        h = th
        w = sw * th / sh
    elif keep_aspect == 'width':
        w = tw
        h = sh * tw / sw
    else:
        w, h = tw, th
    if anchor == 'bottom-center':
        cx = (tx0 + tx1) / 2.0
        return (cx - w / 2.0, ty0, cx + w / 2.0, ty0 + h)
    if anchor == 'bottom-left':
        return (tx0, ty0, tx0 + w, ty0 + h)
    if anchor == 'bottom-right':
        return (tx1 - w, ty0, tx1, ty0 + h)
    cx, cy = (tx0 + tx1) / 2.0, (ty0 + ty1) / 2.0
    return (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)


def clone_image(E, src, dst_bbox, after=None, flip_h=None):
    """draw image `src` (PageImage) again so that it fills dst_bbox (no clipping).
    after: PageImage after whose block the copy is inserted (z-order); default: right after src.
    flip_h: None -> same orientation as the source drawing; True/False -> force."""
    after = after or src
    if after.key != src.key:
        raise ValueError('ảnh nguồn và vị trí chèn phải cùng một luồng nội dung')
    if flip_h is None:
        flip_h = src.ctm[0, 0] < 0
    P = E.page(after.key)
    a, b = P.enclosing_block(after.index)
    cur = P.ctm_at(b + 1)                 # CTM in force after the whole block
    want = placement_matrix(dst_bbox, flip_h)
    X = want @ np.linalg.inv(cur)
    instrs = [Instr([], 'q')]
    if getattr(src, 'gs', None):
        instrs.append(Instr([Name(src.gs)], 'gs'))     # same transparency / blend state as the source
    instrs += [_cm(X), Instr([Name(src.name)], 'Do'), Instr([], 'Q')]
    E.ins[after.key][b + 1].extend(instrs)
    E.log.append(dict(page=src.key + 1 if isinstance(src.key, int) else str(src.key), kind='image-clone', image=src.name,
                      dst=[round(v, 2) for v in dst_bbox], flip_h=bool(flip_h)))


def mirror_images(E, ims, axis_x):
    """mirror each image drawing (WITH its clip block) about the vertical line x = axis_x.
    Pictures are flipped and their positions mirrored - like flipping a photo collage.
    Vector text drawn outside these blocks is NOT touched."""
    F = np.array([[-1.0, 0, 0], [0, 1.0, 0], [2.0 * axis_x, 0, 1.0]])
    for im in ims:
        P = E.page(im.key)
        a, b = P.enclosing_block(im.index)
        C = P.ctm_at(a)
        X = C @ F @ np.linalg.inv(C)        # page-space mirror expressed in the local space at a
        E.ins[im.key][a].extend([Instr([], 'q'), _cm(X)])
        E.ins[im.key][b + 1][0:0] = [Instr([], 'Q')]
    E.log.append(dict(kind='image-mirror', images=[im.name for im in ims], axis_x=round(axis_x, 2)))
