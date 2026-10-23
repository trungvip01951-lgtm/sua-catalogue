"""Outlined text (text converted to vector shapes) - decode, find, replace, insert, delete.

Principle (proven on "Aquaris SP"): every glyph of the same font+size is the SAME outline,
only translated.  So:
  1. OCR labels some glyph groups (words whose glyph count == letter count).
  2. Identical shapes are clustered; the majority OCR vote gives each cluster its character.
  3. Glyph metrics (left side bearing lsb, advance adv, bottom offset bot) are fitted by least
     squares from labelled sequences inside one paint object (residual ~0.001 pt).
  4. New text = copies of existing glyph outlines of the same style, placed with the metrics,
     inserted into the paint object of the old text (=> identical colour, same object).

    T = OutlineText(E)                 # E = vector.Editor
    T.learn([3, 4, 5])                 # OCR + clustering + metrics (pages 0-based)
    m = T.find(4, '4SP2-40')           # -> list of Match
    T.replace(m[0], '4SP2-4', align='left')
    E.save('out.pdf')

Rotated / differently-sized glyphs are handled through similarity transforms (Procrustes)
against the learned prototypes (see find_rotated / replace on such matches).
"""
import collections
import math
import re

import numpy as np

from .vector import union, overlap, FILL_OPS, apply
from . import ocr as _ocr


# ------------------------------------------------------------------ shape helpers
def shape_of(E, key, oi, g):
    path = E.glyph_pagepath(key, oi, g)
    pts = np.array([p for op, ps in path for p in ps], dtype=float)
    ops = ''.join(op for op, ps in path)
    return ops, pts


def norm(pts):
    return pts - pts.min(axis=0)


def procrustes(A, B, allow_rotation=True, allow_scale=True):
    """best similarity transform  B ~ s * A @ R.T + t.  returns (s, R, t, max_residual)."""
    ma = A.mean(0)
    mb = B.mean(0)
    A0 = A - ma
    B0 = B - mb
    if allow_rotation:
        U, S, Vt = np.linalg.svd(A0.T @ B0)
        d = np.sign(np.linalg.det(U @ Vt))
        D = np.diag([1.0, d])
        R = (U @ D @ Vt).T
        s = (S * np.diag(D)).sum() / max((A0 ** 2).sum(), 1e-12) if allow_scale else 1.0
    else:
        R = np.eye(2)
        s = (A0 * B0).sum() / max((A0 ** 2).sum(), 1e-12) if allow_scale else 1.0
    t = mb - s * ma @ R.T
    res = float(np.abs(s * A @ R.T + t - B).max())
    return float(s), R, t, res


class Sim(object):
    """similarity transform p -> s * R p + t  (2D)."""

    def __init__(self, s=1.0, R=None, t=(0.0, 0.0)):
        self.s = float(s)
        self.R = np.eye(2) if R is None else np.asarray(R, float)
        self.t = np.asarray(t, float)

    def __call__(self, p):
        p = np.asarray(p, float)
        return self.s * p @ self.R.T + self.t

    def vec(self, v):
        return self.s * np.asarray(v, float) @ self.R.T

    @property
    def angle(self):
        return math.degrees(math.atan2(self.R[1, 0], self.R[0, 0]))

    def compose_inv_of(self, other):
        """returns transform X with X(other(p)) = self(p)  i.e. self o other^-1"""
        Ri = other.R.T
        si = 1.0 / other.s
        # other^-1(q) = si * (q - t_o) @ Ri.T
        s = self.s * si
        R = self.R @ Ri
        t = self.t - s * other.t @ R.T
        return Sim(s, R, t)

    def matrix3(self):
        a, b = self.s * self.R[0, 0], self.s * self.R[1, 0]
        c, d = self.s * self.R[0, 1], self.s * self.R[1, 1]
        return np.array([[a, b, 0.0], [c, d, 0.0], [self.t[0], self.t[1], 1.0]])


# ------------------------------------------------------------------ data classes
class Glyph(object):
    __slots__ = ('key', 'oi', 'g', 'bbox', 'ops', 'pts', 'cl', 'char', 'style', 'T')

    def __init__(self, key, oi, g, ops, pts):
        self.key = key
        self.oi = oi
        self.g = g
        self.bbox = g['bbox']
        self.ops = ops
        self.pts = pts
        self.cl = None
        self.char = '?'
        self.style = None
        self.T = None   # Sim: style prototype space -> page

    def __repr__(self):
        return 'G(%r p%s o%d x=%.2f)' % (self.char, self.key if not isinstance(self.key, int) else self.key + 1, self.oi, self.bbox[0])


class Match(object):
    """a run of glyphs on one visual line that spells `text`."""

    def __init__(self, key, glyphs, text, line):
        self.key = key
        self.glyphs = glyphs
        self.text = text
        self.line = line

    @property
    def bbox(self):
        return union(g.bbox for g in self.glyphs)

    def __repr__(self):
        b = self.bbox
        return 'Match(%r page=%s bbox=(%.1f,%.1f,%.1f,%.1f) objs=%s)' % (
            self.text, self.key + 1 if isinstance(self.key, int) else self.key, b[0], b[1], b[2], b[3],
            sorted(set(g.oi for g in self.glyphs)))


# ------------------------------------------------------------------ metrics fit
def fit_metrics(samples, ref=None):
    """samples: list of dict(chars=str (may contain ' '), boxes=[bbox per non-space char]).
    model: x0_i = o_n + sum(adv of previous chars incl. spaces) + lsb(c_i);  y0_i = b_n + bot(c_i)
    returns dict(lsb, adv, bot, rms_x, max_x, rms_y, max_y, n)."""
    chars = sorted(set(c for s in samples for c in s['chars'] if c != ' '))
    advs = sorted(set(c for s in samples for c in s['chars'][:-1]))
    if not chars:
        raise ValueError('no samples')
    ref = ref if ref in chars else chars[0]
    cols = ['o%d' % n for n in range(len(samples))] + ['adv_' + a for a in advs] + ['lsb_' + c for c in chars if c != ref]
    idx = {k: i for i, k in enumerate(cols)}
    A = []
    bx = []
    for n, s in enumerate(samples):
        bi = 0
        for i, c in enumerate(s['chars']):
            if c == ' ':
                continue
            row = np.zeros(len(cols))
            row[idx['o%d' % n]] = 1
            for cp in s['chars'][:i]:
                row[idx['adv_' + cp]] += 1
            if c != ref:
                row[idx['lsb_' + c]] = 1
            A.append(row)
            bx.append(s['boxes'][bi][0])
            bi += 1
    A = np.array(A)
    bx = np.array(bx)
    sol = np.linalg.lstsq(A, bx, rcond=None)[0]
    resid = A @ sol - bx
    lsb = {ref: 0.0}
    lsb.update({c: float(sol[idx['lsb_' + c]]) for c in chars if c != ref})
    adv = {a: float(sol[idx['adv_' + a]]) for a in advs}
    colsy = ['b%d' % n for n in range(len(samples))] + ['bot_' + c for c in chars if c != ref]
    idy = {k: i for i, k in enumerate(colsy)}
    Ay = []
    by = []
    for n, s in enumerate(samples):
        bi = 0
        for c in s['chars']:
            if c == ' ':
                continue
            row = np.zeros(len(colsy))
            row[idy['b%d' % n]] = 1
            if c != ref:
                row[idy['bot_' + c]] = 1
            Ay.append(row)
            by.append(s['boxes'][bi][1])
            bi += 1
    Ay = np.array(Ay)
    by = np.array(by)
    soly = np.linalg.lstsq(Ay, by, rcond=None)[0]
    residy = Ay @ soly - by
    bot = {ref: 0.0}
    bot.update({c: float(soly[idy['bot_' + c]]) for c in chars if c != ref})
    # identifiability: adv only determined for chars followed by something
    return dict(lsb=lsb, adv=adv, bot=bot, ref=ref, rms_x=float(np.sqrt((resid ** 2).mean())), max_x=float(np.abs(resid).max()),
                rms_y=float(np.sqrt((residy ** 2).mean())), max_y=float(np.abs(residy).max()), n=len(samples))


def robust_fit(samples, thr=0.05, iters=8, ref=None):
    S = list(samples)
    F = None
    for it in range(iters):
        F = fit_metrics(S, ref)
        bad = set()
        for n, s in enumerate(S):
            x = None
            bi = 0
            for c in s['chars']:
                if c == ' ':
                    x += F['adv'][' ']
                    continue
                b = s['boxes'][bi]
                bi += 1
                if x is None:
                    x = b[0] - F['lsb'][c]
                elif abs(b[0] - (x + F['lsb'][c])) > thr:
                    bad.add(n)
                x += F['adv'].get(c, 0.0)
        if not bad:
            break
        S2 = [s for n, s in enumerate(S) if n not in bad]
        if len(S2) < 2:
            break
        S = S2
    F = fit_metrics(S, ref)
    F['samples'] = S
    F['iters'] = it
    return F



# ------------------------------------------------------------------ grouping helpers
def make_bands(items, box):
    """group items into text-line bands by vertical overlap (tall items first)."""
    items = sorted(items, key=lambda it: -(box(it)[3] - box(it)[1]))
    bands = []   # [y0, y1, hmax, members]
    for it in items:
        b = box(it)
        y0, y1 = b[1], b[3]
        h = y1 - y0
        best = None
        bestov = 0.0
        for bd in bands:
            ov = min(y1, bd[1]) - max(y0, bd[0])
            need = 0.5 * min(max(h, 0.05), bd[1] - bd[0])
            if ov >= need and ov > bestov:
                best, bestov = bd, ov
        if best is None:
            bands.append([y0, y1, h, [it]])
        else:
            best[3].append(it)
    return [bd[3] for bd in sorted(bands, key=lambda bd: -bd[1])]


def merge_stacked(groups):
    """merge vertically stacked parts of ONE glyph inside one paint object:
    dot + stem (i, j, !, ?), accent + letter, the two dots of ':' / the dot+comma of ';'.
    Parts of different text lines are not merged (gap limits)."""
    gs = [dict(g, subs=list(g['subs'])) for g in groups]
    changed = True
    while changed:
        changed = False
        gs.sort(key=lambda g: g['bbox'][0])
        for a in range(len(gs)):
            A = gs[a]['bbox']
            for b in range(a + 1, len(gs)):
                B = gs[b]['bbox']
                if B[0] > A[2]:
                    break
                ox = min(A[2], B[2]) - max(A[0], B[0])
                wmin = min(A[2] - A[0], B[2] - B[0])
                if ox < 0.6 * wmin:
                    # strongly overlapping parts of one glyph (e.g. a 'W' drawn as two 'V' contours)
                    oy = min(A[3], B[3]) - max(A[1], B[1])
                    if ox > 0 and oy > 0:
                        inter = ox * oy
                        amin = min((A[2] - A[0]) * (A[3] - A[1]), (B[2] - B[0]) * (B[3] - B[1]))
                        if amin > 0 and inter >= 0.5 * amin and abs((A[3] - A[1]) - (B[3] - B[1])) <= 0.15 * max(A[3] - A[1], B[3] - B[1]):
                            gs[a]['subs'] += gs[b]['subs']
                            gs[a]['bbox'] = union([A, B])
                            del gs[b]
                            changed = True
                            break
                    continue
                if not (A[3] <= B[1] + 0.05 or B[3] <= A[1] + 0.05):
                    continue
                gap = max(B[1] - A[3], A[1] - B[3])
                hA, hB = A[3] - A[1], B[3] - B[1]
                big, small = max(hA, hB), min(hA, hB)
                ok = (small <= 0.5 * big and gap <= 0.45 * big) or \
                     (abs(hA - hB) <= 0.35 * big and big <= 3.0 * max(wmin, 0.1) and gap <= 3.0 * big)
                if ok:
                    gs[a]['subs'] += gs[b]['subs']
                    gs[a]['bbox'] = union([A, B])
                    del gs[b]
                    changed = True
                    break
            if changed:
                break
    gs.sort(key=lambda g: g['bbox'][0])
    return gs


# ------------------------------------------------------------------ main class
class OutlineText(object):
    def __init__(self, E, tol=0.03, max_glyph_h=40.0):
        self.E = E
        self.tol = tol
        self.max_glyph_h = max_glyph_h
        self.glyphs = {}        # key -> list[Glyph]
        self.samples = []       # labelled sequences
        self.clusters = []      # dict(ops, pts, votes, members, label, style)
        self._buckets = collections.defaultdict(list)
        self.styles = {}        # style id -> dict(clusters, metrics, src, space)
        self.learned_pages = set()

    # -------------------------------------------------------------- glyph collection
    def page_glyphs(self, key):
        if key in self.glyphs:
            return self.glyphs[key]
        P = self.E.page(key)
        out = []
        for oi, o in enumerate(P.objs):
            if o['op'] not in FILL_OPS:
                continue
            b = o['bbox']
            if (b[3] - b[1]) > self.max_glyph_h and len(o['subs']) < 3:
                continue
            for g in merge_stacked(P.glyphs(oi)):
                gb = g['bbox']
                h = gb[3] - gb[1]
                w = gb[2] - gb[0]
                if h > self.max_glyph_h or w > self.max_glyph_h * 1.5 or (h <= 0 and w <= 0):
                    continue
                try:
                    ops, pts = shape_of(self.E, key, oi, g)
                except ValueError:
                    continue
                out.append(Glyph(key, oi, g, ops, pts))
        self.glyphs[key] = out
        for gl in out:
            self._assign_cluster(gl)
        return out

    def _bucket_key(self, ops, pts):
        n = norm(pts)
        mx = n.max(axis=0)
        return (ops, len(pts), round(float(mx[0]), 1), round(float(mx[1]), 1)), n

    def _assign_cluster(self, gl):
        bk, n = self._bucket_key(gl.ops, gl.pts)
        cands = []
        for dx in (-0.1, 0.0, 0.1):
            for dy in (-0.1, 0.0, 0.1):
                cands += self._buckets.get((bk[0], bk[1], round(bk[2] + dx, 1), round(bk[3] + dy, 1)), [])
        for ci in cands:
            cl = self.clusters[ci]
            if cl['pts'].shape == n.shape and np.abs(cl['pts'] - n).max() < self.tol:
                gl.cl = ci
                cl['members'].append(gl)
                return ci
        ci = len(self.clusters)
        self.clusters.append(dict(ops=gl.ops, pts=n, votes=collections.Counter(), members=[gl], label='?', style=None))
        self._buckets[bk].append(ci)
        gl.cl = ci
        return ci

    # -------------------------------------------------------------- lines
    def lines(self, key, rect=None, by_object=False):
        """group glyphs into visual lines -> list of lists of Glyph (sorted by x).
        by_object=True: lines never mix paint objects."""
        gs = self.page_glyphs(key)
        if rect:
            gs = [g for g in gs if rect[0] <= (g.bbox[0] + g.bbox[2]) / 2 <= rect[2] and rect[1] <= (g.bbox[1] + g.bbox[3]) / 2 <= rect[3]]
        groups = collections.defaultdict(list)
        if by_object:
            for g in gs:
                groups[g.oi].append(g)
        else:
            groups[0] = gs
        out = []
        for k in sorted(groups):
            for band in make_bands(groups[k], lambda g: g.bbox):
                band.sort(key=lambda g: g.bbox[0])
                seg = [band[0]]
                for a, b in zip(band, band[1:]):
                    h = max(a.bbox[3] - a.bbox[1], b.bbox[3] - b.bbox[1], 1.0)
                    if b.bbox[0] - a.bbox[2] > 3.0 * h:
                        out.append(seg)
                        seg = []
                    seg.append(b)
                out.append(seg)
        out.sort(key=lambda ln: (-round(ln[0].bbox[3], 0), ln[0].bbox[0]))
        return out

    # -------------------------------------------------------------- learning
    def learn(self, pages, rect=None, dpi=600, psm=11, pattern=r"^[A-Za-z0-9()/.,:;%#'\"+*=&\-]+$", verbose=True, synthetic=True):
        """OCR-label the given pages (0-based list), cluster shapes, build styles + metrics."""
        if isinstance(pages, int):
            pages = [pages]
        path = self.E.doc.path
        added = 0
        g_pos = {}
        for pi in pages:
            if pi in self.learned_pages:
                continue
            gs = self.page_glyphs(pi)
            W = self.ocr_words(pi, rect=rect, dpi=dpi, psm=psm, synthetic=synthetic)
            lines_obj = self.lines(pi, rect, by_object=True)
            for li, ln in enumerate(lines_obj):
                for k, g in enumerate(ln):
                    g_pos[id(g)] = (li, k)
            vis_lines = self.lines(pi, rect, by_object=False)
            for w in W:
                t = w['text']
                t = re.sub(r'[®©@]', '', t)
                t = t.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
                if not t or not re.fullmatch(pattern, t):
                    continue
                wb = w['bbox']
                pad = 0.6
                for ln in vis_lines:
                    mine = [g for g in ln if wb[0] - pad <= (g.bbox[0] + g.bbox[2]) / 2 <= wb[2] + pad and
                            wb[1] - 0.8 <= (g.bbox[1] + g.bbox[3]) / 2 <= wb[3] + 0.8]
                    if not mine:
                        continue
                    mine.sort(key=lambda g: g.bbox[0])
                    if len(mine) != len(t):
                        break
                    # votes for every glyph (word may span several paint objects)
                    for g, c in zip(mine, t):
                        self.clusters[g.cl]['votes'][c] += 1
                    added += 1
                    # metric samples: maximal runs inside ONE object and consecutive in its line
                    run = [(mine[0], t[0])]
                    for (g, c) in zip(mine[1:], t[1:]):
                        pg = g_pos.get(id(run[-1][0]))
                        pc = g_pos.get(id(g))
                        if g.oi == run[-1][0].oi and pg and pc and pg[0] == pc[0] and pc[1] == pg[1] + 1:
                            run.append((g, c))
                        else:
                            self._push_sample(pi, run, g_pos)
                            run = [(g, c)]
                    self._push_sample(pi, run, g_pos)
                    break
            self.learned_pages.add(pi)
        self._relabel()
        self._build_styles()
        if verbose:
            print('learn: +%d mẫu (tổng %d), %d cụm hình, %d kiểu chữ' % (added, len(self.samples), len(self.clusters), len(self.styles)))
        return self

    def ocr_words(self, key, rect=None, dpi=600, psm=11, synthetic=True):
        """OCR words of a page.  synthetic=True: OCR a temporary page that contains ONLY the glyph
        outlines painted black on white (works for white-on-blue headers, coloured text, text on
        photos, and ignores table lines)."""
        if not synthetic:
            return _ocr.page_words(self.E.doc.path, key, rect=rect, dpi=dpi, psm=psm)
        import hashlib, os, tempfile
        from . import cs as _cs
        from .cs import Instr
        from .pdfdoc import make_single_page_pdf
        gs = self.page_glyphs(key)
        mb = self.E.mediabox(key)
        out = [Instr([], 'q'), Instr([0], 'g')]
        for g in gs:
            if rect and not (rect[0] <= (g.bbox[0] + g.bbox[2]) / 2 <= rect[2] and rect[1] <= (g.bbox[1] + g.bbox[3]) / 2 <= rect[3]):
                continue
            for op, pts in self.E.glyph_pagepath(g.key, g.oi, g.g):
                out.append(Instr([round(float(c), 4) for p in pts for c in p], op))
            out.append(Instr([], 'f*' if self.E.page(g.key).objs[g.oi]['op'] in ('f*', 'B*', 'b*') else 'f'))
        out.append(Instr([], 'Q'))
        data = _cs.serialize(out)
        h = hashlib.sha1(data).hexdigest()[:16]
        tmp = os.path.join(_ocr.CACHE_DIR, 'glyphs_%s.pdf' % h)
        os.makedirs(_ocr.CACHE_DIR, exist_ok=True)
        if not os.path.exists(tmp):
            make_single_page_pdf(tmp, mb, data)
        return _ocr.page_words(tmp, 0, rect=rect, dpi=dpi, psm=psm)

    def _push_sample(self, pi, run, g_pos):
        if len(run) < 1:
            return
        gl = [g for g, c in run]
        p0 = g_pos.get(id(gl[0]))
        p1 = g_pos.get(id(gl[-1]))
        if p0 is None or p1 is None:
            return
        self.samples.append(dict(key=pi, glyphs=gl, chars=''.join(c for g, c in run), line=(pi, p0[0]), k0=p0[1], k1=p1[1]))

    def teach(self, key, rect, text, weight=5):
        """tell the decoder what the text inside rect says (one line, spaces ignored) when OCR could
        not read some glyphs (e.g. '?' in dump()).  Glyph count must equal the number of non-space
        characters.  Labels spread to every identical glyph in the file."""
        lines = self.lines(key, rect)
        gl = [g for ln in lines for g in ln]
        gl.sort(key=lambda g: g.bbox[0])
        chars = [c for c in text if c != ' ']
        if len(gl) != len(chars):
            raise ValueError('Vùng có %d nét chữ nhưng chữ dạy có %d ký tự: %s' % (len(gl), len(chars), self.line_text(gl)))
        for g, c in zip(gl, chars):
            self.clusters[g.cl]['votes'][c] += weight
        self._relabel()
        self._build_styles()
        return self.line_text(gl)

    def set_label(self, cluster_id, char):
        self.clusters[cluster_id]['votes'].clear()
        self.clusters[cluster_id]['votes'][char] = 100
        self._relabel()
        self._build_styles()

    def _relabel(self):
        for cl in self.clusters:
            if cl['votes']:
                lab, n = cl['votes'].most_common(1)[0]
                cl['label'] = lab
                cl['conf'] = n / float(sum(cl['votes'].values()))
            else:
                cl['label'] = '?'
                cl['conf'] = 0.0
            for g in cl['members']:
                g.char = cl['label']

    def _build_styles(self):
        # union-find over clusters that co-occur in the same object-line (same paint object, adjacent)
        parent = list(range(len(self.clusters)))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def unite(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for key, gs in self.glyphs.items():
            for ln in self.lines(key, by_object=True):
                for a, b in zip(ln, ln[1:]):
                    h = max(a.bbox[3] - a.bbox[1], b.bbox[3] - b.bbox[1])
                    if b.bbox[0] - a.bbox[2] < 1.5 * h:
                        unite(a.cl, b.cl)
        comp = collections.defaultdict(list)
        for ci in range(len(self.clusters)):
            comp[find(ci)].append(ci)
        self.styles = {}
        for sid, (root, cls) in enumerate(sorted(comp.items(), key=lambda kv: -sum(len(self.clusters[c]['members']) for c in kv[1]))):
            for ci in cls:
                self.clusters[ci]['style'] = sid
                for g in self.clusters[ci]['members']:
                    g.style = sid
            self.styles[sid] = dict(clusters=cls, metrics=None)
        # metrics per style from labelled samples: consecutive OCR words of the same object-line
        # (no unlabelled glyph between them) are joined with one space
        per_style = collections.defaultdict(list)
        byline = collections.defaultdict(list)
        for s in self.samples:
            byline[s['line']].append(s)
        for k, lst in byline.items():
            lst.sort(key=lambda s: s['k0'])
            seq_chars, seq_glyphs, prev = '', [], None
            for s in lst:
                labels = ''.join(self.clusters[g.cl]['label'] for g in s['glyphs'])
                if '?' in labels:
                    if seq_glyphs:
                        self._add_seq(per_style, seq_chars, seq_glyphs)
                    seq_chars, seq_glyphs, prev = '', [], None
                    continue
                if prev is not None and s['k0'] == prev['k1'] + 1:
                    seq_chars += ' ' + labels
                else:
                    if seq_glyphs:
                        self._add_seq(per_style, seq_chars, seq_glyphs)
                    seq_chars, seq_glyphs = labels, []
                seq_glyphs += s['glyphs']
                prev = s
            if seq_glyphs:
                self._add_seq(per_style, seq_chars, seq_glyphs)
        for sid, S in per_style.items():
            if len(S) < 2:
                continue
            try:
                F = robust_fit(S)
            except Exception as e:  # pragma: no cover
                continue
            st = self.styles[sid]
            st['metrics'] = F
            sp = F['adv'].get(' ')
            st['space'] = sp
        # source glyph per char per style (the most frequent cluster with that label)
        for sid, st in self.styles.items():
            src = {}
            for ci in st['clusters']:
                cl = self.clusters[ci]
                lab = cl['label']
                if lab == '?':
                    continue
                if lab not in src or len(cl['members']) > len(self.clusters[src[lab]]['members']):
                    src[lab] = ci
            st['src'] = src
        # transforms for horizontal glyphs: T = translation to bbox-min (scale 1)
        for key, gs in self.glyphs.items():
            for g in gs:
                g.T = None

    def _add_seq(self, per_style, chars, glyphs):
        sids = collections.Counter(g.style for g in glyphs)
        sid = sids.most_common(1)[0][0]
        if len(sids) > 1:
            return
        per_style[sid].append(dict(chars=chars, boxes=[g.bbox for g in glyphs]))

    # -------------------------------------------------------------- metrics access
    def metrics(self, sid):
        st = self.styles.get(sid)
        if not st or not st.get('metrics'):
            raise KeyError('kiểu chữ %s chưa đủ mẫu để đo khoảng cách chữ (cần learn thêm trang)' % sid)
        return st['metrics']

    def has_char(self, sid, c):
        F = self.styles[sid].get('metrics') or {}
        return c in self.styles[sid].get('src', {}) and c in F.get('lsb', {})

    def adv(self, sid, c, nxt=None):
        F = self.metrics(sid)
        if c in F['adv']:
            return F['adv'][c]
        if c.isdigit():
            ds = [F['adv'][d] for d in '0123456789' if d in F['adv']]
            if ds and max(ds) - min(ds) < 0.02:
                return float(np.median(ds))
        if c == ' ' and F['adv'].get(' ') is None:
            raise KeyError('chưa đo được độ rộng dấu cách của kiểu chữ %s' % sid)
        raise KeyError('chưa đo được độ rộng ký tự %r của kiểu chữ %s' % (c, sid))

    def describe_styles(self, top=12):
        rows = []
        for sid, st in list(self.styles.items())[:top]:
            F = st.get('metrics')
            chars = ''.join(sorted(st.get('src', {}).keys()))
            n = sum(len(self.clusters[c]['members']) for c in st['clusters'])
            rows.append('style %d: %d glyphs, chars=%r, fit=%s' % (
                sid, n, chars, ('n=%d rms=%.4f max=%.4f' % (F['n'], F['rms_x'], F['max_x'])) if F else 'NONE'))
        return '\n'.join(rows)

    # -------------------------------------------------------------- decoding
    def line_text(self, ln, with_spaces=True):
        """text of a list of glyphs; word spaces inferred from INK gaps with a per-line threshold
        (robust to kerning and to fonts whose metrics could not be fitted)."""
        if not ln:
            return ''
        if len(ln) == 1:
            return ln[0].char
        hs = sorted(g.bbox[3] - g.bbox[1] for g in ln)
        H = float(np.median(hs[len(hs) // 2:])) if hs else 1.0
        gaps = [b.bbox[0] - a.bbox[2] for a, b in zip(ln, ln[1:])]
        base = float(np.median(gaps)) if gaps else 0.0
        base = min(max(base, 0.0), 0.25 * H)
        thr = max(base + 0.25 * H, 0.3 * H)
        out = ln[0].char
        for (a, b), gap in zip(zip(ln, ln[1:]), gaps):
            if with_spaces and gap > thr:
                out += ' '
            out += b.char
        return out

    def _space_guess(self, sid):
        st = self.styles.get(sid) or {}
        if st.get('space'):
            return st['space']
        F = st.get('metrics')
        if F and F['adv']:
            return 0.55 * float(np.median(list(F['adv'].values())))
        return 2.5

    def text_lines(self, key, rect=None):
        """[(text, glyphs)] for all visual lines on the page (or in rect)."""
        return [(self.line_text(ln), ln) for ln in self.lines(key, rect)]

    def dump(self, key, rect=None):
        for t, ln in self.text_lines(key, rect):
            b = union(g.bbox for g in ln)
            print('(%.1f,%.1f,%.1f,%.1f) %s' % (b[0], b[1], b[2], b[3], t))

    def find(self, key, query, rect=None, regex=False, ignore_spaces=False):
        """find text on page `key` -> list of Match. query: plain text (or regex if regex=True)."""
        out = []
        for ln in self.lines(key, rect):
            t = self.line_text(ln)
            # map text index -> glyph index
            idx = []
            gi = 0
            for ch in t:
                if ch == ' ':
                    idx.append(None)
                else:
                    idx.append(gi)
                    gi += 1
            hay = t
            if ignore_spaces:
                hay = t.replace(' ', '')
                idx = [i for i in idx if i is not None]
            pat = query if regex else re.escape(query)
            for m in re.finditer(pat, hay):
                gis = [idx[k] for k in range(m.start(), m.end()) if idx[k] is not None]
                if not gis:
                    continue
                out.append(Match(key, [ln[i] for i in gis], m.group(0), ln))
        return out

    # -------------------------------------------------------------- geometry of a match
    def origin(self, g):
        F = self.metrics(g.style)
        if g.char not in F['lsb']:
            raise KeyError('ký tự %r chưa có số đo (style %s)' % (g.char, g.style))
        return np.array([g.bbox[0] - F['lsb'][g.char], g.bbox[1] - F['bot'][g.char]])

    def run_extent(self, glyphs):
        """(start_x, end_x, baseline) of a horizontal run in page coords."""
        sid = glyphs[0].style
        o0 = self.origin(glyphs[0])
        ol = self.origin(glyphs[-1])
        end = ol[0] + self.adv(sid, glyphs[-1].char)
        base = float(np.median([self.origin(g)[1] for g in glyphs]))
        return float(o0[0]), float(end), base

    def text_width(self, sid, text):
        w = 0.0
        for c in text:
            w += self.adv(sid, c)
        return w

    def guess_align(self, match, rows=4):
        """look at neighbouring lines in the same column: 'left' | 'right' | 'center'."""
        b = match.bbox
        h = b[3] - b[1]
        cands = []
        for t, ln in self.text_lines(match.key):
            lb = union(g.bbox for g in ln)
            if ln is match.line or abs(((lb[1] + lb[3]) / 2) - ((b[1] + b[3]) / 2)) < 0.5 * h:
                continue
            if overlap((lb[0], 0, lb[2], 1), (b[0], 0, b[2], 1)) > 0 and abs(((lb[1] + lb[3]) / 2) - ((b[1] + b[3]) / 2)) < rows * 3 * h:
                cands.append(lb)
        if not cands:
            return 'left'
        L = np.std([c[0] for c in cands] + [b[0]])
        R = np.std([c[2] for c in cands] + [b[2]])
        C = np.std([(c[0] + c[2]) / 2 for c in cands] + [(b[0] + b[2]) / 2])
        return ['left', 'right', 'center'][int(np.argmin([L, R, C]))]

    # -------------------------------------------------------------- editing
    def _source(self, sid, c):
        """(glyph instance to copy, scale factor, metrics-style) for char c in style sid."""
        st = self.styles[sid]
        if c in st.get('src', {}) and st.get('metrics') and c in st['metrics']['lsb']:
            ci = st['src'][c]
            return self.clusters[ci]['members'][0], 1.0, sid
        # same font at another size?
        for sid2, st2 in self.styles.items():
            if sid2 == sid or c not in st2.get('src', {}) or not st2.get('metrics') or c not in st2['metrics']['lsb']:
                continue
            s = self.style_scale(sid, sid2)
            if s is None:
                continue
            ci = st2['src'][c]
            return self.clusters[ci]['members'][0], s, sid2
        raise KeyError('Không có chữ %r cùng kiểu chữ trong file (style %s) - không tự thay kiểu chữ khác' % (c, sid))

    def style_scale(self, sid_target, sid_src, max_res=0.02):
        """scale factor s with  shape_target = s * shape_src  if both styles are the same font; else None."""
        k = ('scale', sid_target, sid_src)
        if not hasattr(self, '_scales'):
            self._scales = {}
        if k in self._scales:
            return self._scales[k]
        A = self.styles[sid_target].get('src', {})
        B = self.styles[sid_src].get('src', {})
        common = [c for c in A if c in B]
        ss = []
        ok = True
        for c in common:
            ca = self.clusters[A[c]]
            cb = self.clusters[B[c]]
            if ca['ops'] != cb['ops'] or ca['pts'].shape != cb['pts'].shape:
                ok = False
                break
            s, R, t, res = procrustes(cb['pts'], ca['pts'], allow_rotation=False)
            if res > max_res * max(1.0, s) * 3:
                ok = False
                break
            ss.append(s)
        val = None
        if ok and len(ss) >= 2 and (max(ss) - min(ss)) / np.mean(ss) < 0.01:
            val = float(np.mean(ss))
        self._scales[k] = val
        return val

    def char_metrics(self, sid, c):
        """(lsb, adv, bot) of char c expressed in style sid (imports scaled metrics if needed)."""
        F = self.metrics(sid)
        if c in F['lsb'] and (c in F['adv'] or c.isdigit()):
            try:
                a = self.adv(sid, c)
            except KeyError:
                a = None
            if a is not None:
                return F['lsb'][c], a, F['bot'][c]
        # import from another style of the same font
        for sid2, st2 in self.styles.items():
            if sid2 == sid or not st2.get('metrics'):
                continue
            F2 = st2['metrics']
            if c not in F2['lsb'] or c not in F2['adv']:
                continue
            s = self.style_scale(sid, sid2)
            if s is None:
                continue
            common = [k for k in F['lsb'] if k in F2['lsb']]
            if not common:
                continue
            k = common[0]
            lsb = F['lsb'][k] + s * (F2['lsb'][c] - F2['lsb'][k])
            bot = F['bot'][k] + s * (F2['bot'][c] - F2['bot'][k])
            return lsb, s * F2['adv'][c], bot
        raise KeyError('Không đo được ký tự %r cho style %s' % (c, sid))

    def _place_glyph(self, key, target_oi, sid, c, x_origin, baseline, twins=()):
        """copy outline of char c (style sid) so that its origin = (x_origin, baseline)."""
        src, s, sid2 = self._source(sid, c)
        lsb, a, bot = self.char_metrics(sid, c)
        tx = x_origin + lsb
        ty = baseline + bot
        path = self.E.glyph_pagepath(src.key, src.oi, src.g)
        sx0, sy0 = src.bbox[0], src.bbox[1]
        if s == 1.0:
            dx, dy = tx - sx0, ty - sy0
            self.E.insert_path(key, target_oi, path, dx, dy)
            for t in twins:
                self.E.insert_path(key, t, path, dx, dy)
        else:
            Mx = np.array([[s, 0, 0], [0, s, 0], [tx - s * sx0, ty - s * sy0, 1.0]])
            self.E.insert_path(key, target_oi, path, Mx=Mx)
            for t in twins:
                self.E.insert_path(key, t, path, Mx=Mx)
        return a

    def twins_of(self, key, glyphs, tol=0.02):
        """other paint objects having glyphs at exactly the same place (white halo copies etc.)."""
        P = self.E.page(key)
        oi0 = glyphs[0].oi
        res = set()
        for oi, o in enumerate(P.objs):
            if oi == oi0 or overlap(o['bbox'], glyphs[0].bbox) <= 0:
                continue
            gs = P.merged_glyphs(oi)
            ok = True
            for g in glyphs:
                if not any(max(abs(a - b) for a, b in zip(g.bbox, h['bbox'])) < tol + 0.6 for h in gs):
                    ok = False
                    break
            if ok:
                res.add(oi)
        return sorted(res)

    def _twin_groups(self, key, twin_oi, glyphs, tol=0.7):
        P = self.E.page(key)
        gs = P.merged_glyphs(twin_oi)
        out = []
        for g in glyphs:
            best = min(gs, key=lambda h: sum(abs(((a[0] + a[2]) / 2) - ((b[0] + b[2]) / 2)) + abs(((a[1] + a[3]) / 2) - ((b[1] + b[3]) / 2))
                                             for a, b in [(g.bbox, h['bbox'])]))
            out.append(best)
        return out

    def replace(self, match, new_text, align='left', keep_same=True, twins='auto', dry_run=False, verbose=True):
        """replace the glyphs of `match` by `new_text` (same style, same paint object).
        align: 'left' (keep start), 'right' (keep end), 'center' (keep centre).
        twins: 'auto' -> also edit objects that duplicate these glyphs (halo/outline copies)."""
        key = match.key
        gl = match.glyphs
        sid = gl[0].style
        if any(g.style != sid for g in gl):
            raise ValueError('Đoạn chữ cũ gồm nhiều kiểu chữ khác nhau - tách nhỏ yêu cầu')
        start, end, base = self.run_extent(gl)
        Wnew = sum(self.char_metrics(sid, c)[1] for c in new_text) if new_text else 0.0
        if new_text and new_text[-1] != ' ':
            pass
        if align == 'left':
            x0 = start
        elif align == 'right':
            x0 = end - Wnew
        elif align == 'center':
            x0 = (start + end) / 2 - Wnew / 2
        else:
            raise ValueError("align phải là 'left' | 'right' | 'center'")
        target = gl[0].oi
        tw = self.twins_of(key, gl) if twins == 'auto' else list(twins or [])
        # old glyph positions (origins) for keep_same
        old = [(g, self.origin(g)) for g in gl]
        plan = []
        x = x0
        keep = set()
        for c in new_text:
            lsb, a, bot = self.char_metrics(sid, c)
            if c != ' ':
                kept = False
                if keep_same:
                    for j, (g, o) in enumerate(old):
                        if j not in keep and g.char == c and abs(o[0] - x) < 0.002 and abs(o[1] - base) < 0.01:
                            keep.add(j)
                            kept = True
                            break
                if not kept:
                    plan.append((c, x))
            x += a
        if dry_run:
            return dict(start=start, end=end, base=base, x0=x0, plan=plan, keep=sorted(keep), twins=tw)
        twin_groups = {t: self._twin_groups(key, t, gl) for t in tw}
        for j, (g, o) in enumerate(old):
            if j in keep:
                continue
            self.E.delete_group(key, g.oi, g.g)
            for t in tw:
                self.E.delete_group(key, t, twin_groups[t][j])
        for c, xo in plan:
            self._place_glyph(key, target, sid, c, xo, base, twins=tw)
        if verbose:
            print('p%s: %r -> %r  (căn %s, %d chữ mới, giữ %d, bản sao %s)' % (
                key + 1 if isinstance(key, int) else key, match.text, new_text, align, len(plan), len(keep), tw))
        self.E.log.append(dict(page=key + 1 if isinstance(key, int) else str(key), old=match.text, new=new_text, align=align,
                               bbox=[round(v, 2) for v in match.bbox], objects=sorted(set(g.oi for g in gl)), twins=tw))
        return plan

    def delete(self, match, close_gap=False, twins='auto'):
        """delete the glyphs of a match. close_gap=True shifts the rest of the same line left."""
        key = match.key
        gl = match.glyphs
        tw = self.twins_of(key, gl) if twins == 'auto' else list(twins or [])
        twin_groups = {t: self._twin_groups(key, t, gl) for t in tw}
        for j, g in enumerate(gl):
            self.E.delete_group(key, g.oi, g.g)
            for t in tw:
                self.E.delete_group(key, t, twin_groups[t][j])
        if close_gap:
            start, end, base = self.run_extent(gl)
            # also eat one space after the deleted run
            rest = [g for g in match.line if g.bbox[0] > gl[-1].bbox[0] and g not in gl]
            if rest:
                nxt = self.origin(rest[0])[0]
                shift = nxt - start
                for g in rest:
                    self.E.move_group(key, g.oi, g.g, -shift, 0.0)
        self.E.log.append(dict(page=key + 1 if isinstance(key, int) else str(key), old=match.text, new='', bbox=[round(v, 2) for v in match.bbox]))

    def insert(self, key, text, x_origin, baseline, sid, target_oi, twins=()):
        """write `text` (style sid) starting at origin (x_origin, baseline), into paint object target_oi."""
        x = x_origin
        for c in text:
            lsb, a, bot = self.char_metrics(sid, c)
            if c != ' ':
                self._place_glyph(key, target_oi, sid, c, x, baseline, twins=twins)
            x += a
        self.E.log.append(dict(page=key + 1 if isinstance(key, int) else str(key), old='', new=text, at=[round(x_origin, 2), round(baseline, 2)]))
        return x

    def move(self, match, dx, dy, twins='auto'):
        key = match.key
        tw = self.twins_of(key, match.glyphs) if twins == 'auto' else list(twins or [])
        tg = {t: self._twin_groups(key, t, match.glyphs) for t in tw}
        for j, g in enumerate(match.glyphs):
            self.E.move_group(key, g.oi, g.g, dx, dy)
            for t in tw:
                self.E.move_group(key, t, tg[t][j], dx, dy)

    # -------------------------------------------------------------- rotated / scaled text
    def similarity_decode(self, key, rect, max_res=0.03, allow_rotation=True):
        """decode glyphs in rect that are rotated/scaled copies of learned prototypes.
        returns list of (Glyph, char, Sim(style-proto-normalized -> page), style, residual)."""
        out = []
        protos = [(ci, cl) for ci, cl in enumerate(self.clusters) if cl['label'] != '?' and len(cl['members']) >= 2]
        for g in self.page_glyphs(key):
            cx = (g.bbox[0] + g.bbox[2]) / 2
            cy = (g.bbox[1] + g.bbox[3]) / 2
            if not (rect[0] <= cx <= rect[2] and rect[1] <= cy <= rect[3]):
                continue
            best = None
            for ci, cl in protos:
                if cl['ops'] != g.ops or cl['pts'].shape != g.pts.shape:
                    continue
                s, R, t, res = procrustes(cl['pts'], g.pts, allow_rotation=allow_rotation)
                rel = res / max(s, 1e-6)
                if rel < max_res and (best is None or rel < best[0]):
                    best = (rel, cl['label'], Sim(s, R, t), cl['style'])
            if best:
                out.append((g, best[1], best[2], best[3], best[0]))
        return out
