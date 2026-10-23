"""Raster (image) editing: change the pixels of what is visible at a place, then put a small
PATCH image exactly over it.  The original image object stays untouched.

Two kinds of canvas:
  * R.canvas(im)                 - the image's own samples (same colour space; JPEG patch with the
                                   SAME quantisation tables).  Best for normal scanned pages.
  * R.render_canvas(pi, rect)    - the rendered appearance of a page area (RGB).  Use it when the
                                   image has a stencil /Mask (JBIG2), several layers, or is unusual.

    E = Editor('in.pdf'); R = Raster(E)
    im = R.image_at(pi, rect)                  # topmost image covering rect (page coords)
    cv = R.canvas(im)                          # or R.render_canvas(pi, rect, dpi=300)
    hits = R.find(cv, '1750', box=cv.box(rect))
    bank = R.glyph_bank(cv, box=cv.box(table_rect))
    R.replace_word(cv, hits[0], '175', bank, align='center')
    R.commit(cv)
    E.save('out.pdf')
"""
import io
import math
import os
import re
import tempfile
import zlib

import numpy as np
from PIL import Image

from . import cs
from .cs import Instr, Name, Ref
from .vector import apply, M
from . import ocr as _ocr

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None
try:
    from scipy import ndimage
except Exception:  # pragma: no cover
    ndimage = None

NCOMP = {'DeviceGray': 1, 'DeviceRGB': 3, 'DeviceCMYK': 4, 'CalGray': 1, 'CalRGB': 3, 'Lab': 3}


# ======================================================================= image drawings
class PageImage(object):
    """one drawing ('Do') of an image XObject on a page."""

    def __init__(self, key, index, name, ref, d, ctm, order, clip=None, textclip=False):
        self.key, self.index, self.name, self.ref, self.d, self.ctm, self.order = key, index, name, ref, d, ctm, order
        self.clip = clip
        self.textclip = textclip
        self.W = int(d.get('Width', 0))
        self.H = int(d.get('Height', 0))
        det = ctm[0, 0] * ctm[1, 1] - ctm[0, 1] * ctm[1, 0]
        self.inv = np.linalg.inv(ctm) if abs(det) > 1e-12 else None

    @property
    def page_bbox(self):
        pts = [apply(self.ctm, x, y) for x, y in ((0, 0), (1, 0), (0, 1), (1, 1))]
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def to_px(self, x, y):
        s, t = apply(self.inv, x, y)
        return s * self.W, (1.0 - t) * self.H

    def to_page(self, u, v):
        return apply(self.ctm, u / float(self.W), 1.0 - v / float(self.H))

    @property
    def dpi(self):
        b = self.page_bbox
        return self.W / max((b[2] - b[0]) / 72.0, 1e-6)

    @property
    def has_stencil_mask(self):
        return isinstance(self.d.get('Mask'), Ref)

    def __repr__(self):
        b = self.page_bbox
        extra = ' SMask' if self.d.get('SMask') is not None else ''
        extra += ' StencilMask' if self.has_stencil_mask else ''
        extra += ' TEXT-CLIPPED(chỉ hiện trong nét chữ)' if self.textclip else ''
        extra += (' clip=(%.0f,%.0f,%.0f,%.0f)' % tuple(self.clip)) if self.clip is not None else ''
        return 'PageImage(%s %dx%d page=(%.1f,%.1f,%.1f,%.1f) ~%.0fdpi%s #%d)' % (
            self.name, self.W, self.H, b[0], b[1], b[2], b[3], self.dpi, extra, self.index)


def _colorspace_n(doc, csv):
    csv = doc.resolve(csv)
    if isinstance(csv, Name):
        return NCOMP.get(str(csv), 3), str(csv)
    if isinstance(csv, list) and csv:
        kind = str(doc.resolve(csv[0]))
        if kind == 'ICCBased':
            d = doc.get(csv[1]) if isinstance(csv[1], Ref) else {}
            return int(doc.resolve(d.get('N', 3))), 'ICCBased'
        if kind in ('Indexed', 'Separation'):
            return 1, kind
        if kind == 'DeviceN':
            return len(doc.resolve(csv[1])), kind
        return NCOMP.get(kind, 3), kind
    return 3, 'DeviceRGB'


# ======================================================================= canvases
class Canvas(object):
    """editable pixel buffer `work` (H x W x C uint8) mapped to page coordinates."""
    kind = 'base'

    def box(self, rect, pad=0):
        """pixel box (u0, v0, u1, v1) covering page rect."""
        pts = [self.to_px(x, y) for x, y in ((rect[0], rect[1]), (rect[2], rect[1]), (rect[0], rect[3]), (rect[2], rect[3]))]
        u0 = int(math.floor(min(p[0] for p in pts))) - pad
        v0 = int(math.floor(min(p[1] for p in pts))) - pad
        u1 = int(math.ceil(max(p[0] for p in pts))) + pad
        v1 = int(math.ceil(max(p[1] for p in pts))) + pad
        H, W = self.work.shape[:2]
        return (max(0, u0), max(0, v0), min(W, u1), min(H, v1))

    def rect(self, box):
        """page rect of a pixel box."""
        u0, v0, u1, v1 = box
        pts = [self.to_page(u, v) for u, v in ((u0, v0), (u1, v0), (u0, v1), (u1, v1))]
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))

    def gray(self, box=None):
        a = self.work if box is None else self.work[box[1]:box[3], box[0]:box[2]]
        if a.shape[2] == 1:
            g = a[:, :, 0]
            return (255 - g) if getattr(self, 'mode', '') == 'CMYK' else g
        if getattr(self, 'mode', '') == 'CMYK':
            c, m_, y, k = [a[:, :, i].astype(np.float32) for i in range(4)]
            rgb = np.stack([(255 - c) * (255 - k) / 255, (255 - m_) * (255 - k) / 255, (255 - y) * (255 - k) / 255], 2)
            return (rgb @ np.array([0.299, 0.587, 0.114])).clip(0, 255).astype(np.uint8)
        return (a[:, :, :3].astype(np.float32) @ np.array([0.299, 0.587, 0.114])).clip(0, 255).astype(np.uint8)

    def save_png(self, path, box=None, scale=1):
        a = self.work if box is None else self.work[box[1]:box[3], box[0]:box[2]]
        if a.shape[2] == 1:
            pim = Image.fromarray(a[:, :, 0])
        elif a.shape[2] == 4:
            pim = Image.fromarray(a, 'CMYK').convert('RGB')
        else:
            pim = Image.fromarray(a[:, :, :3])
        if scale != 1:
            pim = pim.resize((pim.width * scale, pim.height * scale), Image.NEAREST)
        pim.save(path)
        return path


class ImageCanvas(Canvas):
    kind = 'image'

    def __init__(self, im, pixels, mode, jpeg, smask):
        self.im = im
        self.orig = pixels
        self.work = pixels.copy()
        self.mode = mode
        self.jpeg = jpeg
        self.smask = smask
        self.key = im.key

    def to_px(self, x, y):
        return self.im.to_px(x, y)

    def to_page(self, u, v):
        return self.im.to_page(u, v)


class RenderCanvas(Canvas):
    kind = 'render'

    def __init__(self, pi, rect, dpi, pixels, after):
        self.pi = pi
        self.key = after.key if after is not None else pi
        self.after = after          # PageImage after which the patch is drawn (None -> end of page)
        self.rect0 = rect
        self.dpi = dpi
        self.orig = pixels
        self.work = pixels.copy()
        self.mode = 'RGB'
        self.jpeg = None
        self.smask = None
        H, W = pixels.shape[:2]
        self.s = 72.0 / dpi
        self.W, self.H = W, H

    def to_px(self, x, y):
        return (x - self.rect0[0]) / self.s, (self.rect0[3] - y) / self.s

    def to_page(self, u, v):
        return self.rect0[0] + u * self.s, self.rect0[3] - v * self.s


class ArrayCanvas(Canvas):
    """canvas over a plain picture (e.g. an image inside an Excel file).  'Page' coordinates are
    pixel coordinates with y pointing UP (y = H - v), so the same helpers work."""
    kind = 'array'

    def __init__(self, pixels, mode='RGB'):
        a = np.asarray(pixels)
        if a.ndim == 2:
            a = a[:, :, None]
        self.orig = a.copy()
        self.work = a.copy()
        self.mode = mode
        self.jpeg = None
        self.smask = None
        self.key = None
        self.pi = None
        self.H, self.W = a.shape[:2]

    @classmethod
    def from_bytes(cls, data):
        pim = Image.open(io.BytesIO(data))
        info = dict(format=pim.format, qtables=getattr(pim, 'quantization', None))
        try:
            from PIL import JpegImagePlugin
            info['sampling'] = JpegImagePlugin.get_sampling(pim) if pim.format == 'JPEG' else -1
        except Exception:
            info['sampling'] = -1
        mode = pim.mode
        if mode not in ('L', 'RGB'):
            pim = pim.convert('RGB')
            mode = 'RGB'
        cv = cls(np.asarray(pim), mode)
        cv.file_info = info
        return cv

    def to_bytes(self):
        a = self.work[:, :, 0] if self.work.shape[2] == 1 else self.work
        pim = Image.fromarray(np.ascontiguousarray(a))
        buf = io.BytesIO()
        info = getattr(self, 'file_info', {}) or {}
        if info.get('format') == 'JPEG':
            kw = dict(format='JPEG', optimize=True)
            if info.get('qtables'):
                kw['qtables'] = info['qtables']
            if info.get('sampling', -1) in (0, 1, 2) and self.work.shape[2] > 1:
                kw['subsampling'] = info['sampling']
            pim.save(buf, **kw)
        else:
            pim.save(buf, format=info.get('format') or 'PNG')
        return buf.getvalue()

    def to_px(self, x, y):
        return x, self.H - y

    def to_page(self, u, v):
        return u, self.H - v


# ======================================================================= main class
class _NoLog(object):
    def __init__(self):
        self.log = []


class Raster(object):
    def __init__(self, E=None):
        self.E = E if E is not None else _NoLog()
        self.doc = getattr(E, 'doc', None)
        self.canvases = {}
        self._imgs = {}
        self.patch_count = 0

    # -------------------------------------------------------------- discovery
    def images(self, pi):
        """all image drawings on page pi (incl. inside form XObjects), in drawing order."""
        if pi in self._imgs:
            return self._imgs[pi]
        out = []
        P = self.E.page(pi)
        res = self.doc.page_resources(pi)
        xo = self.doc.resolve(res.get('XObject')) if res else None
        for ev in P.images:
            if ev['kind'] != 'Do' or not xo:
                continue
            ref = xo.get(ev['name'])
            if not isinstance(ref, Ref):
                continue
            d = self.doc.get(ref)
            sub = str(d.get('Subtype'))
            if sub == 'Image':
                pim = PageImage(pi, ev['i'], ev['name'], ref, d, ev['ctm'], len(out), ev.get('clip'), ev.get('textclip', False))
                pim.gs = ev.get('gs')
                out.append(pim)
            elif sub == 'Form':
                mtx = d.get('Matrix')
                Mf = M(*[float(self.doc.resolve(x)) for x in mtx]) if mtx else np.eye(3)
                fkey = ('form', ref)
                fp = self.E.page(fkey)
                r2 = self.doc.resolve(d.get('Resources')) or res
                xo2 = self.doc.resolve(r2.get('XObject')) if r2 else None
                for ev2 in fp.images:
                    if ev2['kind'] != 'Do' or not xo2:
                        continue
                    ref2 = xo2.get(ev2['name'])
                    if isinstance(ref2, Ref) and str(self.doc.get(ref2).get('Subtype')) == 'Image':
                        out.append(PageImage(fkey, ev2['i'], ev2['name'], ref2, self.doc.get(ref2), ev2['ctm'] @ Mf @ ev['ctm'], len(out),
                                             ev.get('clip'), ev.get('textclip', False) or ev2.get('textclip', False)))
        self._imgs[pi] = out
        return out

    def image_at(self, pi, rect):
        """topmost image whose area covers rect (page coords)."""
        best = None
        for im in self.images(pi):
            if im.W < 8 or im.H < 8 or im.textclip:
                continue
            b = im.page_bbox
            if im.clip is not None:
                c = im.clip
                b = (max(b[0], c[0]), max(b[1], c[1]), min(b[2], c[2]), min(b[3], c[3]))
            if b[0] <= rect[0] + 0.05 and b[1] <= rect[1] + 0.05 and b[2] >= rect[2] - 0.05 and b[3] >= rect[3] - 0.05:
                best = im
        if best is None:
            raise ValueError('Không có ảnh nào phủ trọn vùng %s ở trang %d' % (tuple(round(v, 1) for v in rect), pi + 1))
        return best

    # -------------------------------------------------------------- pixel decoding
    def pixels(self, im_or_ref, W=None, H=None):
        ref = im_or_ref.ref if isinstance(im_or_ref, PageImage) else im_or_ref
        data, left, d = self.doc.stream_decoded(ref)
        W = W or int(d.get('Width'))
        H = H or int(d.get('Height'))
        n, csname = _colorspace_n(self.doc, d.get('ColorSpace'))
        bpc = int(self.doc.resolve(d.get('BitsPerComponent', 8)) or 8)
        if left and str(left[0]) in ('DCTDecode', 'DCT'):
            pim = Image.open(io.BytesIO(data))
            sampling = -1
            try:
                from PIL import JpegImagePlugin
                sampling = JpegImagePlugin.get_sampling(pim)
            except Exception:
                pass
            jpeg = dict(qtables=getattr(pim, 'quantization', None), sampling=sampling, mode=pim.mode,
                        adobe=pim.info.get('adobe'))
            pim.load()
            arr = np.asarray(pim)
            if arr.ndim == 2:
                arr = arr[:, :, None]
            return arr.copy(), pim.mode, jpeg
        if left and str(left[0]) == 'JPXDecode':
            pim = Image.open(io.BytesIO(data))
            arr = np.asarray(pim)
            return (arr[:, :, None] if arr.ndim == 2 else arr).copy(), pim.mode, None
        if left:
            raise ValueError('Bộ lọc ảnh %s không giải mã được bằng Python -> dùng render_canvas' % left)
        if d.get('ImageMask'):
            n = 1
            bpc = 1
        if bpc == 8:
            arr = np.frombuffer(data, dtype=np.uint8)[:W * H * n].reshape(H, W, n)
        elif bpc == 16:
            arr = (np.frombuffer(data, dtype='>u2')[:W * H * n].reshape(H, W, n) >> 8).astype(np.uint8)
        elif bpc in (1, 2, 4):
            rowbytes = (W * n * bpc + 7) // 8
            raw = np.frombuffer(data, dtype=np.uint8)[:rowbytes * H].reshape(H, rowbytes)
            bits = np.unpackbits(raw, axis=1)[:, :W * n * bpc].reshape(H, W * n, bpc)
            v = (bits * (2 ** np.arange(bpc - 1, -1, -1))).sum(axis=2).reshape(H, W, n)
            arr = (v * (255 // (2 ** bpc - 1))).astype(np.uint8)
        else:
            raise ValueError('BitsPerComponent %d' % bpc)
        mode = {1: 'L', 3: 'RGB', 4: 'CMYK'}.get(n, 'L')
        if csname == 'Indexed':
            mode = 'P'
        return arr.copy(), mode, None

    def canvas(self, im):
        """editable canvas of the image's own samples."""
        k = ('img', im.key, im.index)
        if k not in self.canvases:
            if im.has_stencil_mask:
                raise ValueError('Ảnh %s có /Mask dạng stencil (vd JBIG2) -> dùng R.render_canvas(pi, rect)' % im.name)
            arr, mode, jpeg = self.pixels(im)
            if mode == 'P':
                raise ValueError('Ảnh %s dùng bảng màu Indexed -> dùng R.render_canvas(pi, rect)' % im.name)
            sm = None
            smref = im.d.get('SMask')
            if isinstance(smref, Ref):
                sm, _, _ = self.pixels(smref)
            self.canvases[k] = ImageCanvas(im, arr, mode, jpeg, sm)
        return self.canvases[k]

    def render_canvas(self, pi, rect, dpi=None, engine=None):
        """editable canvas of the RENDERED appearance of page rect.  dpi default: 2x the image dpi
        (>= 300).  The patch is drawn right after the topmost image covering rect."""
        from .pdfdoc import render
        try:
            after = self.image_at(pi, rect)
        except ValueError:
            after = None
        if dpi is None:
            dpi = max(300, int(round((after.dpi if after else 150) * 2)))
        # snap rect to the pixel grid of the render
        s = 72.0 / dpi
        mb = self.doc.mediabox(pi)
        x0 = mb[0] + math.floor((rect[0] - mb[0]) / s) * s
        y1 = mb[3] - math.floor((mb[3] - rect[3]) / s) * s
        x1 = x0 + math.ceil((rect[2] - x0) / s) * s
        y0 = y1 - math.ceil((y1 - rect[1]) / s) * s
        r = (x0, y0, x1, y1)
        pix = render(self.doc.path, pi, dpi=dpi, clip=r, engine=engine)
        cvs = RenderCanvas(pi, r, dpi, pix, after)
        self.canvases[('render', pi, r)] = cvs
        return cvs

    # -------------------------------------------------------------- OCR
    def ocr(self, cv, box=None, scale=2, psm=11, config=''):
        """OCR words in pixel box of canvas -> list of dict(text, box (px), conf, line)."""
        H, W = cv.work.shape[:2]
        if box is None:
            box = (0, 0, W, H)
        box = tuple(int(round(x)) for x in box)
        import hashlib
        g = cv.gray(box)
        ck = (hashlib.sha1(g.tobytes()).hexdigest(), g.shape, box, scale, psm, config)
        if not hasattr(self, '_ocr_cache'):
            self._ocr_cache = {}
        if ck in self._ocr_cache:
            return [dict(w) for w in self._ocr_cache[ck]]
        pim = Image.fromarray(g)
        if scale != 1:
            pim = pim.resize((pim.width * scale, pim.height * scale), Image.BICUBIC)
        out = []
        for w in _ocr.image_words(pim, psm=psm, config=config):
            l, t, r, b = w['box']
            out.append(dict(text=w['text'], box=(box[0] + l / scale, box[1] + t / scale, box[0] + r / scale, box[1] + b / scale),
                            conf=w['conf'], line=w['line']))
        self._ocr_cache[ck] = [dict(w) for w in out]
        return out

    def find(self, cv, text, box=None, scale=2, psm=11, regex=False):
        """find text (single line) -> list of dict(text, line_text, box (px), words)."""
        words = self.ocr(cv, box, scale, psm)
        out = []
        lines = {}
        for w in words:
            lines.setdefault(w['line'], []).append(w)
        for ln, ws in lines.items():
            ws.sort(key=lambda w: w['box'][0])
            s = ''
            spans = []
            for w in ws:
                if s:
                    s += ' '
                spans.append((len(s), len(s) + len(w['text']), w))
                s += w['text']
            pat = text if regex else re.escape(text)
            for m in re.finditer(pat, s):
                sel = [w for a, b, w in spans if b > m.start() and a < m.end()]
                if not sel:
                    continue
                bx = [min(w['box'][0] for w in sel), min(w['box'][1] for w in sel), max(w['box'][2] for w in sel), max(w['box'][3] for w in sel)]
                # partial word: cut the box proportionally (refined later by components)
                if len(sel) == 1 and (m.start() > spans[[x[2] for x in spans].index(sel[0])][0] or m.end() < spans[[x[2] for x in spans].index(sel[0])][1]):
                    a0, b0, w0 = spans[[x[2] for x in spans].index(sel[0])]
                    n = max(1, b0 - a0)
                    u0, u1 = w0['box'][0], w0['box'][2]
                    bx[0] = u0 + (u1 - u0) * (m.start() - a0) / n
                    bx[2] = u0 + (u1 - u0) * (m.end() - a0) / n
                hit = dict(text=m.group(0), line_text=s, box=tuple(bx), words=sel)
                try:
                    comps = self.components(cv, hit['box'], expect=len(hit['text'].replace(' ', '')))
                    if comps:
                        hit['box'] = (min(c['box'][0] for c in comps) - 1, min(c['box'][1] for c in comps) - 1,
                                      max(c['box'][2] for c in comps) + 1, max(c['box'][3] for c in comps) + 1)
                        hit['n_glyphs'] = len(comps)
                except Exception:
                    pass
                out.append(hit)
        return out

    # -------------------------------------------------------------- ink model
    @staticmethod
    def bg_ink(a, box, pad=3):
        u0, v0, u1, v1 = [int(round(x)) for x in box]
        H, W = a.shape[:2]
        U0, V0, U1, V1 = max(0, u0 - pad), max(0, v0 - pad), min(W, u1 + pad), min(H, v1 + pad)
        region = a[V0:V1, U0:U1].astype(np.float32)
        ring = np.ones(region.shape[:2], bool)
        ring[(v0 - V0):(v1 - V0), (u0 - U0):(u1 - U0)] = False
        if ring.sum() < 4:
            ring[:] = True
        bg = np.median(region[ring], axis=0)
        inner = region[(v0 - V0):(v1 - V0), (u0 - U0):(u1 - U0)].reshape(-1, region.shape[2])
        if len(inner) == 0:
            return bg, bg
        dist = np.abs(inner - bg).sum(axis=1)
        thr = np.percentile(dist, 92)
        ink = np.median(inner[dist >= thr], axis=0)
        return bg, ink

    @staticmethod
    def alpha_of(a, bg, ink):
        v = ink - bg
        n2 = float((v * v).sum())
        if n2 < 1e-6:
            return np.zeros(a.shape[:2], np.float32)
        return np.clip(((a.astype(np.float32) - bg) * v).sum(axis=2) / n2, 0.0, 1.0)

    def components(self, cv, box, thr=0.4, bg=None, ink=None, remove_lines=True, band=True, expect=None):
        """glyph components inside pixel box -> list of dict(box, alpha, bg, ink) sorted by x.
        Table rules (long horizontal / vertical lines) crossing the box are ignored."""
        if ndimage is None:
            raise RuntimeError('Cần scipy để tách chữ trên ảnh')
        a = cv.work
        H, W = a.shape[:2]
        u0, v0, u1, v1 = [int(round(x)) for x in box]
        u0, v0, u1, v1 = max(0, u0), max(0, v0), min(W, u1), min(H, v1)
        if bg is None or ink is None:
            bg, ink = self.bg_ink(a, (u0, v0, u1, v1))
        al = self.alpha_of(a[v0:v1, u0:u1], bg, ink)
        m = al > thr
        line_mask = np.zeros_like(m)
        if remove_lines and m.size:
            bh, bw = m.shape

            def longest_run(v):
                best = cur = 0
                for t in v:
                    cur = cur + 1 if t else 0
                    best = max(best, cur)
                return best
            if bw >= 12:
                for y in range(bh):
                    if m[y].sum() >= 0.9 * bw and longest_run(m[y]) >= 0.9 * bw:
                        line_mask[max(0, y - 1):y + 2, :] |= m[max(0, y - 1):y + 2, :] | True
            if bh >= 12:
                for x in range(bw):
                    if m[:, x].sum() >= 0.9 * bh and longest_run(m[:, x]) >= 0.9 * bh:
                        line_mask[:, max(0, x - 1):x + 2] |= True
            m = m & ~line_mask
        # keep only the main text band (OCR boxes often reach into the next table row)
        if band and m.any():
            rows = m.sum(axis=1)
            ink_rows = rows > 0
            runs = []
            y = 0
            while y < len(rows):
                if ink_rows[y]:
                    y0 = y
                    while y < len(rows) and ink_rows[y]:
                        y += 1
                    runs.append((y0, y, int(rows[y0:y].sum())))
                else:
                    y += 1
            if len(runs) > 1:
                # merge runs separated by tiny gaps (dots of i/j, colon)
                merged = [list(runs[0])]
                for r0, r1, s in runs[1:]:
                    if r0 - merged[-1][1] <= max(1, int(0.25 * (merged[-1][1] - merged[-1][0]))):
                        merged[-1][1] = r1
                        merged[-1][2] += s
                    else:
                        merged.append([r0, r1, s])
                best = max(merged, key=lambda r: r[2])
                keep = np.zeros_like(m)
                keep[best[0]:best[1], :] = True
                m = m & keep
        lab, n = ndimage.label(m, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
        comps = []
        bh, bw = m.shape
        for sl in ndimage.find_objects(lab):
            if sl is None:
                continue
            ys, xs = sl
            h, w = ys.stop - ys.start, xs.stop - xs.start
            if h * w < 2:
                continue
            if (w > 0.9 * bw and h <= 3) or (h > 0.9 * bh and w <= 3):
                continue
            comps.append([u0 + xs.start, v0 + ys.start, u0 + xs.stop, v0 + ys.stop])
        comps.sort(key=lambda b: b[0])

        def area(b):
            return max(1, (b[2] - b[0]) * (b[3] - b[1]))
        changed = True
        while changed:
            changed = False
            for i in range(len(comps)):
                for j in range(i + 1, len(comps)):
                    A, B = comps[i], comps[j]
                    ov = min(A[2], B[2]) - max(A[0], B[0])
                    gap = max(B[1] - A[3], A[1] - B[3])
                    hmax = max(A[3] - A[1], B[3] - B[1])
                    small = min(area(A), area(B)) < 0.35 * max(area(A), area(B))
                    if ov >= 0.5 * min(A[2] - A[0], B[2] - B[0]) and gap <= 0.6 * hmax and (small or gap > 0):
                        comps[i] = [min(A[0], B[0]), min(A[1], B[1]), max(A[2], B[2]), max(A[3], B[3])]
                        del comps[j]
                        changed = True
                        break
                if changed:
                    break
        # make the number of glyphs match the expected text length (split wide / merge close parts)
        if expect:
            prof_al = np.where(m, al, 0.0)
            guard = 0
            while len(comps) < expect and comps and guard < 20:
                guard += 1
                k = max(range(len(comps)), key=lambda i: comps[i][2] - comps[i][0])
                A = comps[k]
                xa, xb = A[0] - u0, A[2] - u0
                if xb - xa < 4:
                    break
                prof = prof_al[A[1] - v0:A[3] - v0, xa:xb].sum(axis=0)
                lo, hi = 2, len(prof) - 2
                if hi <= lo:
                    break
                cut = lo + int(np.argmin(prof[lo:hi]))
                comps[k:k + 1] = [[A[0], A[1], A[0] + cut, A[3]], [A[0] + cut, A[1], A[2], A[3]]]
                comps.sort(key=lambda b: b[0])
            while len(comps) > expect and len(comps) >= 2:
                gaps = [comps[i + 1][0] - comps[i][2] for i in range(len(comps) - 1)]
                i = int(np.argmin(gaps))
                A, B = comps[i], comps[i + 1]
                comps[i:i + 2] = [[min(A[0], B[0]), min(A[1], B[1]), max(A[2], B[2]), max(A[3], B[3])]]
            # tighten vertical extent of split parts
            for c in comps:
                sub = m[c[1] - v0:c[3] - v0, c[0] - u0:c[2] - u0]
                ys = np.where(sub.any(axis=1))[0]
                if len(ys):
                    c[3] = c[1] + ys[-1] + 1
                    c[1] = c[1] + ys[0]
        out = []
        full_lines = np.zeros((H, W), bool)
        full_lines[v0:v1, u0:u1] = line_mask
        for b in comps:
            b = [max(0, b[0] - 1), max(0, b[1] - 1), min(W, b[2] + 1), min(H, b[3] + 1)]
            ca = self.alpha_of(a[b[1]:b[3], b[0]:b[2]], bg, ink)
            ca[ca < 0.04] = 0
            ca[full_lines[b[1]:b[3], b[0]:b[2]]] = 0
            out.append(dict(box=tuple(b), alpha=ca, bg=bg, ink=ink))
        return out

    # -------------------------------------------------------------- glyph bank + spacing
    DESC = set('gjpqy,;')
    LOWMARK = set('.,-_~\'"°³²*')

    @staticmethod
    def _cls(ch):
        if ch.isdigit():
            return 'D'
        if ch.isupper():
            return 'U'
        if ch.islower():
            return 'L'
        return ch

    def glyph_bank(self, cv, box=None, scale=2, psm=11, words=None, pattern=r'^[A-Za-z0-9.,:;()/%+\-=°³²]+$'):
        """learn glyph pictures + spacing (centre distances, gaps) from OCR words in pixel box.
        Best: a box with text of the SAME font and size (e.g. one table / one paragraph).
        replace_word() automatically keeps only samples of the same size as the text it edits."""
        words = words if words is not None else self.ocr(cv, box, scale, psm)
        samples = []
        for w in words:
            t = w['text']
            if not re.fullmatch(pattern, t):
                continue
            comps = self.components(cv, w['box'], expect=len(t))
            if len(comps) != len(t):
                continue
            hs_ = [c['box'][3] - c['box'][1] for c in comps]
            if max(hs_) > 3.5 * max(1, np.median(hs_)):
                continue
            bottoms = [c['box'][3] for c, ch in zip(comps, t) if ch not in self.DESC and ch not in self.LOWMARK]
            if not bottoms:
                continue
            samples.append(dict(text=t, word=w, base=float(np.median(bottoms)), comps=comps,
                                size=float(np.percentile(hs_, 75))))
        return self._bank_from_samples(samples)

    def _bank_from_samples(self, samples):
        bank, boff, pair, gapc, gaps = {}, {}, {}, {}, []
        for s in samples:
            t, comps, base = s['text'], s['comps'], s['base']
            for c, ch in zip(comps, t):
                bank.setdefault(ch, []).append(c)
                boff.setdefault(ch, []).append(c['box'][3] - base)
            for (ca, a), (cb, b) in zip(zip(comps, t), list(zip(comps, t))[1:]):
                d = (cb['box'][0] + cb['box'][2]) / 2.0 - (ca['box'][0] + ca['box'][2]) / 2.0
                g = cb['box'][0] - ca['box'][2]
                pair.setdefault((a, b), []).append(d)
                gapc.setdefault((self._cls(a), self._cls(b)), []).append(g)
                gaps.append(g)
        med = lambda v: float(np.median(v))
        metrics = dict(boff={k: med(v) for k, v in boff.items()},
                       pair={k: med(v) for k, v in pair.items()}, npair={k: len(v) for k, v in pair.items()},
                       gapc={k: med(v) for k, v in gapc.items()}, ngapc={k: len(v) for k, v in gapc.items()},
                       gap=med(gaps) if gaps else 1.0,
                       width={k: med([c['box'][2] - c['box'][0] for c in v]) for k, v in bank.items()},
                       height={k: med([c['box'][3] - c['box'][1] for c in v]) for k, v in bank.items()})
        return dict(glyphs=bank, metrics=metrics if samples else None, samples=samples)

    def sub_bank(self, bank, size, tol=0.15):
        """keep only samples whose text size is within +-tol of `size` (pixels)."""
        keep = [s for s in bank['samples'] if abs(s['size'] - size) <= tol * size]
        return self._bank_from_samples(keep) if keep else bank

    def best_glyph(self, bank, ch):
        lst = bank['glyphs'].get(ch)
        if not lst:
            raise KeyError('Không có mẫu chữ %r trong vùng đã học (học thêm vùng khác CÙNG kiểu chữ)' % ch)
        ws = np.array([c['box'][2] - c['box'][0] for c in lst])
        hs = np.array([c['box'][3] - c['box'][1] for c in lst])
        k = int(np.argmin(np.abs(ws - np.median(ws)) + np.abs(hs - np.median(hs))))
        return lst[k]

    def pair_distance(self, bank, a, b):
        """centre-to-centre distance between consecutive glyphs a, b (pixels)."""
        Mx = bank['metrics']
        if (a, b) in Mx['pair'] and Mx['npair'][(a, b)] >= 1:
            return Mx['pair'][(a, b)]
        k = (self._cls(a), self._cls(b))
        if k == ('D', 'D'):
            dd = [v for (x, y), v in Mx['pair'].items() if x.isdigit() and y.isdigit()]
            if dd:
                return float(np.median(dd))      # tabular figures: constant pitch
        ga = self.best_glyph(bank, a)
        gb = self.best_glyph(bank, b)
        wa = ga['box'][2] - ga['box'][0]
        wb = gb['box'][2] - gb['box'][0]
        gap = Mx['gapc'][k] if (k in Mx['gapc'] and Mx['ngapc'][k] >= 2) else Mx['gap']
        return (wa + wb) / 2.0 + gap

    def layout(self, bank, text):
        """relative centres for text (spaces allowed)."""
        Mx = bank['metrics']
        xs = []
        x = 0.0
        prev = None
        space_w = None
        for ch in text:
            if ch == ' ':
                if space_w is None:
                    hD = Mx['height'].get('0') or np.median(list(Mx['height'].values()))
                    space_w = 0.32 * hD
                x += space_w
                continue
            if prev is not None:
                x += self.pair_distance(bank, prev, ch)
            xs.append((ch, x))
            prev = ch
        return xs

    # -------------------------------------------------------------- pixel edits
    def erase(self, cv, mask=None, box=None, method='auto', dilate=1, color=None):
        """erase mask (bool HxW) or pixel box; fill by inpainting (cv2) / ring median / colour."""
        a = cv.work
        H, W = a.shape[:2]
        if mask is None:
            mask = np.zeros((H, W), bool)
            u0, v0, u1, v1 = [int(round(x)) for x in box]
            mask[v0:v1, u0:u1] = True
        if dilate and ndimage is not None:
            mask = ndimage.binary_dilation(mask, iterations=dilate)
        if color is not None:
            a[mask] = np.asarray(color, np.float32).round().clip(0, 255).astype(np.uint8)
            return mask
        ys, xs = np.where(mask)
        if not len(ys):
            return mask
        y0, y1, x0, x1 = max(0, ys.min() - 12), min(H, ys.max() + 13), max(0, xs.min() - 12), min(W, xs.max() + 13)
        msub = mask[y0:y1, x0:x1]
        if method in ('auto', 'inpaint') and cv2 is not None and a.shape[2] in (1, 3):
            sub = np.ascontiguousarray(a[y0:y1, x0:x1] if a.shape[2] == 3 else a[y0:y1, x0:x1, 0])
            res = cv2.inpaint(sub, (msub * 255).astype(np.uint8), 3, cv2.INPAINT_TELEA)
            if a.shape[2] == 3:
                a[y0:y1, x0:x1][msub] = res[msub]
            else:
                a[y0:y1, x0:x1, 0][msub] = res[msub]
        else:
            ring = ~msub
            med = np.median(a[y0:y1, x0:x1][ring], axis=0)
            a[y0:y1, x0:x1][msub] = med.astype(np.uint8)
        return mask

    def erase_components(self, cv, comps, dilate=1, method='auto', color=None):
        H, W = cv.work.shape[:2]
        mask = np.zeros((H, W), bool)
        for c in comps:
            b = c['box']
            mask[b[1]:b[3], b[0]:b[2]] |= c['alpha'] > 0.05
        return self.erase(cv, mask=mask, dilate=dilate, method=method, color=color)

    def stamp(self, cv, comp, u, v, ink=None):
        """blend glyph alpha (comp) with top-left at (u, v) px using ink colour."""
        a = cv.work
        al = comp['alpha']
        h, w = al.shape
        u = int(round(u))
        v = int(round(v))
        H, W = a.shape[:2]
        if u < 0 or v < 0 or u + w > W or v + h > H:
            raise ValueError('chữ mới ra ngoài vùng ảnh')
        ink = np.asarray(comp['ink'] if ink is None else ink, np.float32)
        dst = a[v:v + h, u:u + w].astype(np.float32)
        a[v:v + h, u:u + w] = (dst * (1 - al[:, :, None]) + ink[None, None, :] * al[:, :, None]).round().clip(0, 255).astype(np.uint8)

    def replace_word(self, cv, match, new_text, bank, align='center', ink=None, erase_method='auto', erase_color=None,
                     prefer_copy=True):
        """erase the glyphs inside match['box'] and write new_text with glyphs cut from `bank`.
        align: 'left' | 'center' | 'right' (relative to the old text's ink extent)."""
        if bank.get('metrics') is None:
            raise ValueError('glyph_bank chưa có mẫu (cần OCR đọc được chữ trong vùng học)')
        old = match['text'].replace(' ', '')
        comps = self.components(cv, match['box'], expect=len(old))
        if not comps:
            raise ValueError('Không thấy nét chữ trong vùng %s' % (match['box'],))
        if len(comps) != len(old):
            raise ValueError('Tách được %d nét chữ nhưng chữ cũ %r có %d ký tự - kiểm lại vùng' % (len(comps), old, len(old)))
        bg, ink0 = self.bg_ink(cv.work, match['box'])
        ink = ink0 if ink is None else ink
        size = float(np.percentile([c['box'][3] - c['box'][1] for c in comps], 75))
        if bank.get('samples') and any('size' in s for s in bank['samples']):
            sb = self.sub_bank(bank, size)
            if all(ch in sb['glyphs'] for ch in new_text if ch != ' '):
                bank = sb
        Mx = bank['metrics']
        left = min(c['box'][0] for c in comps)
        right = max(c['box'][2] for c in comps)
        if len(comps) == len(old):
            bots = [c['box'][3] for c, ch in zip(comps, old) if ch not in self.DESC and ch not in self.LOWMARK]
        else:
            bots = []
        base = float(np.median(bots)) if bots else float(np.median([c['box'][3] for c in comps]))
        lay = self.layout(bank, new_text)
        if not lay:
            self.erase_components(cv, comps, method=erase_method, color=erase_color)
            return
        gl = [(ch, x, self.best_glyph(bank, ch)) for ch, x in lay]
        # an identical word already printed in the same font -> copy it as a whole (authentic spacing)
        src_word = None
        if prefer_copy and ' ' not in new_text:
            for s in bank['samples']:
                if s['text'] == new_text:
                    src_word = s
                    break
        if src_word is not None:
            c0 = (src_word['comps'][0]['box'][0] + src_word['comps'][0]['box'][2]) / 2.0
            gl = [(ch, (c['box'][0] + c['box'][2]) / 2.0 - c0, c) for ch, c in zip(new_text, src_word['comps'])]
            boff = {}
            for ch, c in zip(new_text, src_word['comps']):
                boff[id(c)] = c['box'][3] - src_word['base']
        nl = min(x - (g['box'][2] - g['box'][0]) / 2.0 for ch, x, g in gl)
        nr = max(x + (g['box'][2] - g['box'][0]) / 2.0 for ch, x, g in gl)
        if align == 'left':
            off = left - nl
        elif align == 'right':
            off = right - nr
        else:
            off = (left + right) / 2.0 - (nl + nr) / 2.0
        self.erase_components(cv, comps, method=erase_method, color=erase_color)
        for ch, x, g in gl:
            w = g['box'][2] - g['box'][0]
            h = g['box'][3] - g['box'][1]
            u = off + x - w / 2.0
            if src_word is not None:
                bottom = base + boff[id(g)]
            else:
                bottom = base + Mx['boff'].get(ch, 0.0)
            self.stamp(cv, g, u, bottom - h, ink=ink)
        pg = cv.pi if cv.kind in ('render', 'array') else cv.im.key
        self.E.log.append(dict(page=pg + 1 if isinstance(pg, int) else (str(pg) if pg is not None else 'image'), kind='raster-' + cv.kind, old=match['text'], new=new_text,
                               box_px=[int(round(v)) for v in match['box']], align=align))

    def copy_box(self, cv, src_box, dst_uv, flip_h=False, mask=None):
        """copy pixels of src_box to top-left dst_uv (same canvas). mask: bool (src box size)."""
        a = cv.work
        u0, v0, u1, v1 = src_box
        blk = a[v0:v1, u0:u1].copy()
        if flip_h:
            blk = blk[:, ::-1]
            mask = None if mask is None else mask[:, ::-1]
        du, dv = dst_uv
        h, w = blk.shape[:2]
        if mask is None:
            a[dv:dv + h, du:du + w] = blk
        else:
            a[dv:dv + h, du:du + w][mask] = blk[mask]

    # -------------------------------------------------------------- commit
    @staticmethod
    def _align(b, H, W, align=16):
        u0, v0, u1, v1 = b
        return (int(max(0, (u0 // align) * align)), int(max(0, (v0 // align) * align)),
                int(min(W, -(-u1 // align) * align)), int(min(H, -(-v1 // align) * align)))

    def changed_boxes(self, cv, merge=24):
        diff = np.any(cv.work != cv.orig, axis=2)
        if not diff.any():
            return []
        H, W = diff.shape
        if ndimage is None:
            ys, xs = np.where(diff)
            return [self._align((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1), H, W)]
        lab, n = ndimage.label(ndimage.binary_dilation(diff, iterations=merge))
        out = []
        for sl in ndimage.find_objects(lab):
            ys, xs = sl
            out.append(self._align((xs.start, ys.start, xs.stop, ys.stop), H, W))
        return out

    def commit(self, cv, encoding='auto', mode='auto'):
        """apply the canvas changes to the PDF.
        image canvas, mode 'replace' (default): the whole image is re-encoded once (JPEG with the
            SAME quantisation tables) into a NEW image object used only by this drawing -> no seams.
        mode 'patch': small patch images over the changed areas (render canvases always patch)."""
        if cv.kind == 'image' and mode in ('auto', 'replace'):
            if not np.any(cv.work != cv.orig):
                return []
            name = self._replace_image(cv, encoding)
            cv.orig = cv.work.copy()
            return [name]
        boxes = self.changed_boxes(cv)
        names = [self._write_patch(cv, b, encoding) for b in boxes]
        cv.orig = cv.work.copy()
        return names

    def _encode(self, cv, arr, encoding):
        enc = encoding
        if enc == 'auto':
            enc = 'jpeg' if (cv.kind == 'image' and cv.jpeg is not None) else 'flate'
        if enc == 'jpeg':
            a = arr[:, :, 0] if arr.shape[2] == 1 else arr
            pim = Image.fromarray(np.ascontiguousarray(a), mode={1: 'L', 3: 'RGB', 4: 'CMYK'}[arr.shape[2]])
            buf = io.BytesIO()
            kw = dict(format='JPEG', optimize=True)
            if cv.jpeg and cv.jpeg.get('qtables'):
                kw['qtables'] = cv.jpeg['qtables']
            else:
                kw['quality'] = 95
            if cv.jpeg and cv.jpeg.get('sampling', -1) in (0, 1, 2) and arr.shape[2] > 1:
                kw['subsampling'] = cv.jpeg['sampling']
            pim.save(buf, **kw)
            return buf.getvalue(), 'DCTDecode'
        return zlib.compress(np.ascontiguousarray(arr).tobytes(), 9), 'FlateDecode'

    def usage_count(self, ref):
        """how many times an image object is drawn in the whole document (pages + forms)."""
        n = 0
        for pi in range(self.doc.n_pages):
            for im in self.images(pi):
                if tuple(im.ref) == tuple(ref):
                    n += 1
        return n

    def _replace_image(self, cv, encoding='auto'):
        im = cv.im
        d = im.d
        data, filt = self._encode(cv, cv.work, encoding)
        filters = d.get('Filter')
        flate_wrap = isinstance(filters, list) and len(filters) == 2 and str(filters[0]) in ('FlateDecode', 'Fl') and filt == 'DCTDecode'
        if flate_wrap:
            data = zlib.compress(data, 9)
        if self.usage_count(im.ref) == 1:
            self._overwrite_stream(im.ref, data, ['FlateDecode', 'DCTDecode'] if flate_wrap else [filt])
            self.patch_count += 1
            return im.name
        extra = {}
        for k in ('Interpolate', 'Intent', 'Mask', 'Metadata', 'OC'):
            if d.get(k) is not None:
                extra[k] = d.get(k)
        bpc = int(self.doc.resolve(d.get('BitsPerComponent', 8)) or 8)
        ref = self.doc.new_image_xobject(data, im.W, im.H, d.get('ColorSpace'), bpc, None, decode=d.get('Decode'),
                                         smask=d.get('SMask'), extra=extra)
        self._overwrite_stream(ref, data, ['FlateDecode', 'DCTDecode'] if flate_wrap else [filt])
        name = self._register(im.key, ref)
        self.E.modify_instr(im.key, im.index, Instr([Name(name)], 'Do'))
        self.patch_count += 1
        return name

    def _overwrite_stream(self, ref, data, filters):
        doc = self.doc
        if doc.backend == 'pikepdf':
            import pikepdf
            o = doc.pdf.get_object(tuple(ref))
            fl = pikepdf.Array([pikepdf.Name('/' + f) for f in filters]) if len(filters) > 1 else pikepdf.Name('/' + filters[0])
            o.write(data, filter=fl)
            if '/DecodeParms' in o:
                del o['/DecodeParms']
            return
        xref = ref[0]
        doc.doc.update_stream(xref, data, compress=False)
        doc.doc.xref_set_key(xref, 'Filter', ('[' + ' '.join('/' + f for f in filters) + ']') if len(filters) > 1 else '/' + filters[0])
        doc.doc.xref_set_key(xref, 'DecodeParms', 'null')

    def _write_patch(self, cv, box, encoding='auto'):
        doc = self.doc
        u0, v0, u1, v1 = box
        blk = np.ascontiguousarray(cv.work[v0:v1, u0:u1])
        extra = {}
        decode = None
        if cv.kind == 'image':
            im = cv.im
            d = im.d
            csv = d.get('ColorSpace')
            for k in ('Interpolate', 'Intent'):
                if d.get(k) is not None:
                    extra[k] = d.get(k)
            decode = d.get('Decode')
            if isinstance(d.get('Mask'), list):
                extra['Mask'] = d.get('Mask')
        else:
            csv = Name('DeviceRGB')
        enc = encoding
        if enc == 'auto':
            enc = 'jpeg' if (cv.kind == 'image' and cv.jpeg is not None) else 'flate'
        if enc == 'jpeg':
            arr = blk[:, :, 0] if blk.shape[2] == 1 else blk
            pim = Image.fromarray(arr, mode={1: 'L', 3: 'RGB', 4: 'CMYK'}[blk.shape[2]])
            buf = io.BytesIO()
            kw = dict(format='JPEG', optimize=False)
            if cv.jpeg and cv.jpeg.get('qtables'):
                kw['qtables'] = cv.jpeg['qtables']
            else:
                kw['quality'] = 95
            if cv.jpeg and cv.jpeg.get('sampling', -1) in (0, 1, 2) and blk.shape[2] > 1:
                kw['subsampling'] = cv.jpeg['sampling']
            pim.save(buf, **kw)
            data, filt = buf.getvalue(), 'DCTDecode'
        else:
            data, filt = zlib.compress(blk.tobytes(), 9), 'FlateDecode'
        smask_ref = None
        if cv.kind == 'image' and cv.smask is not None:
            sm = np.ascontiguousarray(cv.smask[v0:v1, u0:u1, 0])
            if sm.min() < 255:
                smask_ref = doc.new_image_xobject(zlib.compress(sm.tobytes(), 9), u1 - u0, v1 - v0, Name('DeviceGray'), 8, 'FlateDecode')
        ref = doc.new_image_xobject(data, u1 - u0, v1 - v0, csv, 8, filt, decode=decode, smask=smask_ref, extra=extra)
        if cv.kind == 'image':
            im = cv.im
            name = self._register(im.key, ref)
            W, H = float(im.W), float(im.H)
            mtx = [cs.Num((u1 - u0) / W), 0, 0, cs.Num((v1 - v0) / H), cs.Num(u0 / W), cs.Num(1 - v1 / H)]
            instrs = [Instr([], 'q'), Instr(mtx, 'cm'), Instr([Name(name)], 'Do'), Instr([], 'Q')]
            self.E.insert_instrs(im.key, im.index, instrs, before=False)
        else:
            x0, y1 = cv.to_page(u0, v0)
            x1, y0 = cv.to_page(u1, v1)
            target = cv.after
            key = target.key if target is not None else cv.pi
            name = self._register(key, ref)
            want = np.array([[x1 - x0, 0, 0], [0, y1 - y0, 0], [x0, y0, 1.0]])
            if target is not None:
                cur = target.ctm      # CTM in force right after the image Do
                X = want @ np.linalg.inv(cur)
                idx = target.index
            else:
                P = self.E.page(cv.pi)
                X = want  # appended at page end: assume default CTM after balanced q/Q
                idx = len(P.ops) - 1
            mtx = [cs.Num(X[0, 0]), cs.Num(X[0, 1]), cs.Num(X[1, 0]), cs.Num(X[1, 1]), cs.Num(X[2, 0]), cs.Num(X[2, 1])]
            instrs = [Instr([], 'q'), Instr(mtx, 'cm'), Instr([Name(name)], 'Do'), Instr([], 'Q')]
            self.E.insert_instrs(key, idx, instrs, before=False)
        self.patch_count += 1
        return name

    def _register(self, key, ref):
        if isinstance(key, int):
            return self.doc.add_xobject_to_page(key, ref, prefix='CfxPatch')
        doc = self.doc
        form_ref = key[1]
        if doc.backend == 'pikepdf':
            import pikepdf
            fo = doc.pdf.get_object(tuple(form_ref))
            if '/Resources' not in fo:
                fo['/Resources'] = pikepdf.Dictionary()
            R = fo.Resources
            if '/XObject' not in R:
                R['/XObject'] = pikepdf.Dictionary()
            k = 1
            while pikepdf.Name('/CfxPatch%d' % k) in R.XObject:
                k += 1
            nm = 'CfxPatch%d' % k
            R.XObject[pikepdf.Name('/' + nm)] = doc.pdf.get_object(tuple(ref))
            return nm
        k = 1
        while doc.doc.xref_get_key(form_ref[0], 'Resources/XObject/CfxPatch%d' % k)[0] != 'null':
            k += 1
        nm = 'CfxPatch%d' % k
        doc.doc.xref_set_key(form_ref[0], 'Resources/XObject/' + nm, '%d 0 R' % ref[0])
        return nm

    # -------------------------------------------------------------- self test
    def noop_test(self, pi, rect=None, size=128, render_dpi=None, mode='replace'):
        """patch an UNCHANGED area and measure the visible difference (throw-away editor!)."""
        from .pdfdoc import render
        ims = [im for im in self.images(pi) if im.W >= 2 * size and im.H >= 2 * size]
        if not ims and rect is None:
            return None
        if rect is None:
            im = ims[-1]
            b = im.page_bbox
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            hw = size / im.dpi * 72 / 2
            rect = (cx - hw, cy - hw, cx + hw, cy + hw)
        im = self.image_at(pi, rect)
        try:
            cv = self.canvas(im)
            kind = 'image'
        except ValueError:
            cv = self.render_canvas(pi, rect)
            kind = 'render'
        H, W = cv.work.shape[:2]
        bx = cv.box(rect)
        bx = self._align(bx, H, W)
        if kind == 'image' and mode == 'replace':
            self._replace_image(cv)
        else:
            self._write_patch(cv, bx)
        out = os.path.join(tempfile.gettempdir(), 'catfix_noop_%d.pdf' % os.getpid())
        self.E.save(out)
        dpi = render_dpi or max(150, int(round(im.dpi)))
        r = cv.rect(bx)
        a = render(self.doc.path, pi, dpi=dpi, clip=r).astype(int)
        b = render(out, pi, dpi=dpi, clip=r).astype(int)
        h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
        dd = np.abs(a[:h, :w] - b[:h, :w])
        return dict(kind=kind, image=im.name, max_diff=int(dd.max()), mean_diff=round(float(dd.mean()), 3),
                    p99=float(np.percentile(dd, 99)), rect=tuple(round(v, 1) for v in r))
