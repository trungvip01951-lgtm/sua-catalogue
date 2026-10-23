"""Ready-made recipes on top of the low-level modules (what ChatGPT should normally call).

    from catfix.recipes import Job
    job = Job('in.pdf', 'out.pdf')                     # opens Editor + helpers lazily
    job.outline_replace(pages=[14, 16], old='Warranty: 1 year', new='Warranty: 2 years', align='left')
    job.text_replace(pages=[0], old='irrugation', new='irrigation', align='left')
    job.raster_replace(page=8, old='1750', new='175', align='center')
    job.save()                                          # writes out.pdf + out.log.json (or log_path)
    job.evidence('compare.png')                         # before/after crops of every edit
    job.check()                                         # diff regions vs edited boxes + structure
"""
import json
import os
import re

from .vector import Editor
from . import verify


class Job(object):
    def __init__(self, src, dst, backend=None, log_path=None):
        from ._compat import same_file
        if same_file(src, dst):
            raise ValueError('file ra phải khác file vào')
        self.src = src
        self.dst = dst
        self.log_path = log_path or (dst + '.log.json')
        self.E = Editor(src, backend)
        self._T = None
        self._TL = None
        self._R = None
        self.edits = []      # dict(page (0-based), rect, label, kind)
        self._canvases = {}

    # -------------------------------------------------------------- helpers (lazy)
    @property
    def T(self):
        if self._T is None:
            from .otext import OutlineText
            self._T = OutlineText(self.E)
        return self._T

    @property
    def TL(self):
        if self._TL is None:
            from .textlayer import TextLayer
            self._TL = TextLayer(self.E)
        return self._TL

    @property
    def R(self):
        if self._R is None:
            from .raster import Raster
            self._R = Raster(self.E)
        return self._R

    def _add(self, pi, rect, label, kind):
        self.edits.append(dict(page=pi, rect=[round(float(v), 2) for v in rect], label=label, kind=kind))

    # -------------------------------------------------------------- outlined text
    def outline_find(self, page, text, rect=None, regex=False):
        if page not in self.T.learned_pages:
            self.T.learn([page], verbose=False)
        return self.T.find(page, text, rect=rect, regex=regex)

    def outline_replace(self, pages, old, new, align='left', rect=None, expect=None, regex=False, twins='auto'):
        """replace outlined text on each page in `pages` (0-based).  expect: number of matches
        required per page (None = at least one)."""
        done = []
        for pi in ([pages] if isinstance(pages, int) else pages):
            ms = self.outline_find(pi, old, rect, regex)
            if expect is not None and len(ms) != expect:
                raise ValueError('Trang %d: thấy %d chỗ %r (cần %d): %s' % (pi + 1, len(ms), old, expect, ms))
            if not ms:
                raise ValueError('Trang %d: không thấy %r (chữ nét vẽ). Dùng job.outline_dump(%d) để xem chữ đọc được' % (pi + 1, old, pi))
            for m in ms:
                newt = re.sub(old, new, m.text) if regex else new
                self.T.replace(m, newt, align=align, twins=twins, verbose=False)
                self._add(pi, m.bbox, '%s -> %s' % (m.text, newt), 'outline')
                done.append((pi + 1, m.text, newt))
        return done

    def outline_delete(self, page, text, rect=None, close_gap=False, expect=1):
        ms = self.outline_find(page, text, rect)
        if len(ms) != expect:
            raise ValueError('Trang %d: thấy %d chỗ %r (cần %d)' % (page + 1, len(ms), text, expect))
        for m in ms:
            self.T.delete(m, close_gap=close_gap)
            self._add(page, m.bbox, 'xoá %s' % m.text, 'outline')

    def outline_dump(self, page, rect=None):
        if page not in self.T.learned_pages:
            self.T.learn([page], verbose=False)
        self.T.dump(page, rect)

    # -------------------------------------------------------------- real text
    def text_replace(self, pages, old, new, align='left', rect=None, expect=None, regex=False, keep_rest=True):
        done = []
        for pi in ([pages] if isinstance(pages, int) else pages):
            ms = self.TL.find(pi, old, rect=rect, regex=regex)
            if expect is not None and len(ms) != expect:
                raise ValueError('Trang %d: thấy %d chỗ %r (cần %d)' % (pi + 1, len(ms), old, expect))
            if not ms:
                raise ValueError('Trang %d: không thấy %r trong lớp chữ. Dùng job.TL.dump(%d)' % (pi + 1, old, pi))
            # replace from right to left so earlier matches keep their indices
            for m in sorted(ms, key=lambda m: (-m.glyphs[0].run.index, -m.glyphs[0].k)):
                newt = re.sub(old, new, m.text) if regex else new
                b = m.bbox
                self.TL.replace(m, newt, align=align, keep_rest=keep_rest, verbose=False)
                self._add(pi, b, '%s -> %s' % (m.text, newt), 'text')
                done.append((pi + 1, m.text, newt))
                self.TL._runs.clear()
        return done

    # -------------------------------------------------------------- raster
    def canvas(self, page, rect=None, render=False, dpi=None):
        mb = self.E.mediabox(page)
        r = rect or (mb[0] + 5, mb[1] + 5, mb[2] - 5, mb[3] - 5)
        if render:
            cv = self.R.render_canvas(page, r, dpi=dpi)
        else:
            im = self.R.image_at(page, r)
            k = ('img', im.key, im.index)
            cv = self._canvases.get(k) or self.R.canvas(im)
            self._canvases[k] = cv
        return cv

    def raster_replace(self, page, old, new, align='center', search_rect=None, learn_rect=None, nth=None, render=False, expect=1):
        """replace a word printed in a scanned page image.
        search_rect: page area to search (recommended);  learn_rect: area with the SAME font to learn
        glyphs from (default: a band around the word)."""
        cv = self.canvas(page, search_rect if render else None, render=render)
        box = cv.box(search_rect) if search_rect else None
        hits = self.R.find(cv, old, box=box)
        if nth is not None:
            hits = [hits[nth]]
        if expect is not None and len(hits) != expect:
            raise ValueError('Trang %d: OCR thấy %d chỗ %r (cần %d): %s' % (page + 1, len(hits), old, expect, [h['box'] for h in hits]))
        for h in hits:
            if learn_rect:
                lb = cv.box(learn_rect)
            else:
                u0, v0, u1, v1 = h['box']
                H, W = cv.work.shape[:2]
                lb = (0, max(0, int(v0 - 150)), W, min(H, int(v1 + 150)))
            bank = self.R.glyph_bank(cv, box=lb)
            rect = cv.rect([int(round(v)) for v in h['box']])
            self.R.replace_word(cv, h, new, bank, align=align)
            self._add(page, rect, '%s -> %s' % (old, new), 'raster')
        return hits

    def raster_commit(self):
        for cv in list(self._canvases.values()) + [c for k, c in self.R.canvases.items() if k[0] == 'render']:
            self.R.commit(cv)
        self._canvases = {}

    # -------------------------------------------------------------- save & checks
    def save(self):
        if self._R is not None:
            self.raster_commit()
        self.E.save(self.dst)
        d = os.path.dirname(os.path.abspath(self.log_path))
        os.makedirs(d, exist_ok=True)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(dict(src=self.src, dst=self.dst, edits=self.edits, log=self.E.log), f,
                      ensure_ascii=False, indent=1, default=str)
        return self.dst

    def close(self):
        self.E.close()

    def evidence(self, out_png, dpi=200):
        items = [(e['page'], e['rect'], e['label']) for e in self.edits]
        return verify.compare_sheet(self.src, self.dst, items, out_png, dpi=dpi) if items else None

    def check(self, extra_allowed=None, raster=False):
        """diff regions must lie inside the edited boxes (+ extra_allowed {page_no: [rects]})."""
        allowed = {}
        for e in self.edits:
            r = e['rect']
            allowed.setdefault(e['page'] + 1, []).append((r[0] - 3, r[1] - 3, r[2] + 12, r[3] + 3))
        for k, v in (extra_allowed or {}).items():
            allowed.setdefault(k, []).extend(v)
        kw = dict(thr=48, min_size=2.0) if raster else {}
        regs = verify.diff_regions(self.src, self.dst, dpi=100, **kw)
        bad = verify.outside_pixels(self.src, self.dst, allowed, dpi=100, **kw)
        miss = verify.missing(regs, {k: [(a[0] + 3, a[1] + 3, a[2] - 12, a[3] - 3) for a in v] for k, v in allowed.items()})
        st = verify.structure_check(self.src, self.dst)
        return dict(ok=not bad and not miss and st['ok'], unexpected=bad, missing=miss, structure=st, regions=regs)
