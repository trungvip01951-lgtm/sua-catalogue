"""Real text (text-show operators Tj/TJ with embedded fonts): find / replace / delete / insert.

Edits keep the same font, size, colour and position - only the string bytes of the show
operator change (plus small TJ position numbers to keep the alignment).

    E  = Editor('in.pdf')           # catfix.vector.Editor (shared with outline/raster edits)
    TL = TextLayer(E)
    TL.dump(0)                      # print text lines of page 1 with positions
    m = TL.find(0, 'irrugation')    # list of TMatch
    TL.replace(m[0], 'irrigation', align='left')
    E.save('out.pdf')
"""
import math
import re

import numpy as np

from . import cs
from .cs import Instr, Name, Str, Ref
from .fonts import PdfFont
from .vector import M, apply, union


class TGlyph(object):
    __slots__ = ('run', 'k', 'elem', 'off', 'cb', 'ch', 'o', 'e', 'ts0', 'ts1')

    def __init__(self, run, k, elem, off, cb, ch, o, e, ts0, ts1):
        self.run = run      # TextRun
        self.k = k          # index of glyph inside the run
        self.elem = elem    # index of the string element inside TJ array (0 for Tj)
        self.off = off      # byte offset inside that string
        self.cb = cb        # code bytes
        self.ch = ch        # unicode (or '�')
        self.o = o          # origin (page coords)
        self.e = e          # next origin (page coords) after advance
        self.ts0 = ts0      # text-space x before / after (relative to run start)
        self.ts1 = ts1

    @property
    def bbox(self):
        r = self.run
        h = r.size_page
        x0, y0 = self.o
        x1, y1 = self.e
        return (min(x0, x1), min(y0, y1) - 0.22 * h, max(x0, x1), max(y0, y1) + 0.75 * h)

    def __repr__(self):
        return 'TG(%r %.1f,%.1f)' % (self.ch, self.o[0], self.o[1])


class TextRun(object):
    def __init__(self, key, index, op, font, fs, Tm, ctm, tc, tw, th, ts, tl, tr, fill, fill_cs, fontname, res_key):
        self.key = key
        self.index = index
        self.op = op
        self.font = font
        self.fs = fs
        self.Tm = Tm.copy()
        self.ctm = ctm.copy()
        self.tc, self.tw, self.th, self.ts, self.tl, self.tr = tc, tw, th, ts, tl, tr
        self.fill = fill
        self.fill_cs = fill_cs
        self.fontname = fontname
        self.res_key = res_key
        self.glyphs = []
        T = M(fs * th, 0, 0, fs, 0, ts) @ Tm @ ctm
        self.Trm = T
        ux, uy = T[0, 0], T[0, 1]
        n = math.hypot(ux, uy) or 1.0
        self.u = (ux / n, uy / n)
        self.size_page = math.hypot(T[1, 0], T[1, 1])
        self.scale_x = n / (fs * th) if fs * th else 1.0   # page units per text-space unit along baseline

    @property
    def text(self):
        return ''.join(g.ch for g in self.glyphs)

    def __repr__(self):
        return 'Run(p%s #%d %s %.1fpt %r)' % (self.key + 1 if isinstance(self.key, int) else self.key, self.index,
                                             self.font.basefont if self.font else '?', self.size_page, self.text[:40])


class TMatch(object):
    def __init__(self, key, glyphs, text, line):
        self.key = key
        self.glyphs = glyphs
        self.text = text
        self.line = line

    @property
    def bbox(self):
        return union(g.bbox for g in self.glyphs)

    @property
    def runs(self):
        out = []
        for g in self.glyphs:
            if g.run not in out:
                out.append(g.run)
        return out

    def __repr__(self):
        b = self.bbox
        r = self.glyphs[0].run
        return 'TMatch(%r page=%s bbox=(%.1f,%.1f,%.1f,%.1f) font=%s %.2fpt)' % (
            self.text, self.key + 1 if isinstance(self.key, int) else self.key, b[0], b[1], b[2], b[3],
            r.font.basefont if r.font else '?', r.size_page)


class TextLayer(object):
    def __init__(self, E):
        self.E = E
        self.doc = E.doc
        self._runs = {}
        self._fonts = {}
        self.end_ctm = {}

    # -------------------------------------------------------------- fonts
    def font(self, ref, name):
        k = tuple(ref) if isinstance(ref, Ref) else (name, id(ref))
        if k not in self._fonts:
            self._fonts[k] = PdfFont(self.doc, ref, name)
        return self._fonts[k]

    # -------------------------------------------------------------- interpreter
    def runs(self, pi):
        """all text runs on page pi (including inside form XObjects)."""
        if pi in self._runs:
            return self._runs[pi]
        out = []
        res = self.doc.page_resources(pi)
        self._interp(pi, pi, res, np.eye(3), out, depth=0)
        self._runs[pi] = out
        return out

    def _interp(self, page, key, res, base_ctm, out, depth):
        if depth > 6:
            return
        P = self.E.page(key)
        ops = P.ops
        ctm = base_ctm.copy()
        stack = []
        fill = ('g', (0.0,))
        fill_cs = None
        tc = tw = 0.0
        th = 1.0
        ts = 0.0
        tl = 0.0
        tr = 0
        font = None
        fontname = None
        fs = 0.0
        Tm = np.eye(3)
        Tlm = np.eye(3)
        fonts_res = self.doc.resolve(res.get('Font')) if res else None
        xo_res = self.doc.resolve(res.get('XObject')) if res else None
        seq = []
        for i, ins in enumerate(ops):
            if ins.op == '__multi__':
                for j, sub in enumerate(ins.operands):
                    seq.append((i, j, sub))
            else:
                seq.append((i, None, ins))
        for i, sub_j, ins in seq:
            op = ins.op
            v = ins.operands
            if op == 'q':
                stack.append((ctm.copy(), fill, fill_cs, tc, tw, th, ts, tl, tr, font, fontname, fs))
            elif op == 'Q':
                if stack:
                    ctm, fill, fill_cs, tc, tw, th, ts, tl, tr, font, fontname, fs = stack.pop()
            elif op == 'cm':
                ctm = M(*[float(x) for x in v]) @ ctm
            elif op in ('rg', 'g', 'k', 'sc', 'scn'):
                fill = (op, tuple(v))
                if op in ('rg', 'g', 'k'):
                    fill_cs = None
            elif op == 'cs':
                fill_cs = v[0] if v else None
            elif op == 'BT':
                Tm = np.eye(3)
                Tlm = np.eye(3)
            elif op == 'Tc':
                tc = float(v[0])
            elif op == 'Tw':
                tw = float(v[0])
            elif op == 'Tz':
                th = float(v[0]) / 100.0
            elif op == 'TL':
                tl = float(v[0])
            elif op == 'Ts':
                ts = float(v[0])
            elif op == 'Tr':
                tr = int(v[0])
            elif op == 'Tf':
                fontname = str(v[0])
                fs = float(v[1])
                ref = fonts_res.get(fontname) if fonts_res else None
                font = self.font(ref, fontname) if ref is not None else None
            elif op == 'Td':
                Tlm = M(1, 0, 0, 1, float(v[0]), float(v[1])) @ Tlm
                Tm = Tlm.copy()
            elif op == 'TD':
                tl = -float(v[1])
                Tlm = M(1, 0, 0, 1, float(v[0]), float(v[1])) @ Tlm
                Tm = Tlm.copy()
            elif op == 'Tm':
                Tlm = M(*[float(x) for x in v])
                Tm = Tlm.copy()
            elif op == 'T*':
                Tlm = M(1, 0, 0, 1, 0, -tl) @ Tlm
                Tm = Tlm.copy()
            elif op in ('Tj', 'TJ', "'", '"'):
                if op == "'":
                    Tlm = M(1, 0, 0, 1, 0, -tl) @ Tlm
                    Tm = Tlm.copy()
                    arr = [v[0]]
                elif op == '"':
                    tw = float(v[0])
                    tc = float(v[1])
                    Tlm = M(1, 0, 0, 1, 0, -tl) @ Tlm
                    Tm = Tlm.copy()
                    arr = [v[2]]
                elif op == 'Tj':
                    arr = [v[0]]
                else:
                    arr = v[0] if v and isinstance(v[0], list) else []
                run = TextRun(key, i, op, font, fs, Tm, ctm, tc, tw, th, ts, tl, tr, fill, fill_cs, fontname, key)
                run.sub = sub_j
                x = 0.0
                k = 0
                for ei, el in enumerate(arr):
                    if isinstance(el, (int, float)) and not isinstance(el, bool):
                        x += -float(el) / 1000.0 * fs * th
                        continue
                    if not isinstance(el, (bytes, bytearray)):
                        continue
                    codes = font.split_codes(el) if font else [bytes([b]) for b in el]
                    off = 0
                    for cb in codes:
                        w0 = font.width(cb) if font else 500.0
                        ch = (font.unicode_of(cb) if font else None) or '�'
                        adv = (w0 / 1000.0 * fs + tc + (tw if (len(cb) == 1 and cb == b' ') else 0.0)) * th
                        o = self._pt(run, x)
                        e = self._pt(run, x + adv)
                        run.glyphs.append(TGlyph(run, k, ei, off, cb, ch, o, e, x, x + adv))
                        x += adv
                        off += len(cb)
                        k += 1
                Tm = M(1, 0, 0, 1, x, 0) @ Tm
                out.append(run)
            elif op == 'Do' and xo_res:
                name = str(v[0])
                ref = xo_res.get(name)
                if isinstance(ref, Ref):
                    d = self.doc.get(ref)
                    if str(d.get('Subtype')) == 'Form':
                        mtx = d.get('Matrix')
                        Mf = M(*[float(self.doc.resolve(x)) for x in mtx]) if mtx else np.eye(3)
                        r2 = self.doc.resolve(d.get('Resources')) or res
                        self._interp(page, ('form', ref), r2, Mf @ ctm, out, depth + 1)
        self.end_ctm[key] = ctm

    @staticmethod
    def _pt(run, x_ts):
        # text space point (x_ts, 0) -> page.  Trm already contains fs*th scaling, so divide.
        T = M(1, 0, 0, 1, x_ts, 0) @ M(1, 0, 0, 1, 0, run.ts) @ run.Tm @ run.ctm
        return (T[2, 0], T[2, 1])

    # -------------------------------------------------------------- lines & search
    def glyphs(self, pi, rect=None, visible_only=False):
        out = []
        for r in self.runs(pi):
            if visible_only and r.tr in (3, 7):
                continue
            for g in r.glyphs:
                if rect:
                    x, y = g.o
                    if not (rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]):
                        continue
                out.append(g)
        return out

    def lines(self, pi, rect=None, visible_only=False):
        gs = self.glyphs(pi, rect, visible_only)
        groups = {}
        for g in gs:
            u = g.run.u
            ang = round(math.degrees(math.atan2(u[1], u[0])) / 2.0) * 2.0
            perp = -g.o[0] * u[1] + g.o[1] * u[0]
            groups.setdefault(ang, []).append((perp, g))
        out = []
        for ang, lst in groups.items():
            lst.sort(key=lambda t: t[0])
            cur = []
            for perp, g in lst:
                if cur and abs(perp - cur[-1][0]) > max(0.3 * g.run.size_page, 0.8):
                    out.append(cur)
                    cur = []
                cur.append((perp, g))
            if cur:
                out.append(cur)
        res = []
        for ln in out:
            u = ln[0][1].run.u
            gl = sorted((g for p, g in ln), key=lambda g: g.o[0] * u[0] + g.o[1] * u[1])
            seg = [gl[0]]
            for a, b in zip(gl, gl[1:]):
                pa = a.e[0] * u[0] + a.e[1] * u[1]
                pb = b.o[0] * u[0] + b.o[1] * u[1]
                if pb - pa > 3.0 * max(a.run.size_page, 1.0):
                    res.append(seg)
                    seg = []
                seg.append(b)
            res.append(seg)
        res.sort(key=lambda ln: (-round(ln[0].o[1], 0), ln[0].o[0]))
        return res

    def line_text(self, ln):
        if not ln:
            return ''
        out = ln[0].ch
        u = ln[0].run.u
        for a, b in zip(ln, ln[1:]):
            pa = a.e[0] * u[0] + a.e[1] * u[1]
            pb = b.o[0] * u[0] + b.o[1] * u[1]
            gap = pb - pa
            if gap > 0.22 * max(a.run.size_page, 1.0) and a.ch != ' ' and b.ch != ' ':
                out += ' '
            out += b.ch
        return out

    def text_lines(self, pi, rect=None, visible_only=False):
        return [(self.line_text(ln), ln) for ln in self.lines(pi, rect, visible_only)]

    def dump(self, pi, rect=None, visible_only=False):
        for t, ln in self.text_lines(pi, rect, visible_only):
            b = union(g.bbox for g in ln)
            r = ln[0].run
            print('(%.1f,%.1f,%.1f,%.1f) [%s %.1fpt%s] %s' % (b[0], b[1], b[2], b[3], r.font.family if r.font else '?', r.size_page,
                                                         ' Tr%d' % r.tr if r.tr else '', t))

    def find(self, pi, query, rect=None, regex=False, visible_only=True):
        out = []
        for ln in self.lines(pi, rect, visible_only):
            t = self.line_text(ln)
            idx = []
            gi = 0
            prev = None
            for ch in t:
                # inferred spaces map to no glyph
                if gi < len(ln) and ln[gi].ch == ch:
                    idx.append(gi)
                    gi += 1
                else:
                    idx.append(None)
            pat = query if regex else re.escape(query)
            for m in re.finditer(pat, t):
                gis = [idx[k] for k in range(m.start(), m.end()) if idx[k] is not None]
                if gis:
                    out.append(TMatch(pi, [ln[i] for i in gis], m.group(0), ln))
        return out

    # -------------------------------------------------------------- editing helpers
    def _cur_instr(self, run):
        P = self.E.page(run.key)
        ins = P.ops[run.index]
        if ins.op == '__multi__':
            return ins.operands[run.sub], ins
        return ins, None

    def _as_tj(self, run):
        """current array of the run's show operator (list of strings / numbers)."""
        ins, wrapper = self._cur_instr(run)
        if ins.op == 'TJ':
            return list(ins.operands[0]), ins
        if ins.op in ('Tj', "'"):
            return [ins.operands[0]], ins
        if ins.op == '"':
            return [ins.operands[2]], ins
        raise ValueError('not a show op: %s' % ins.op)

    def _write_tj(self, run, arr, orig_ins):
        """write the new array back IN PLACE (same instruction slot -> indices stay valid)."""
        E = self.E
        key = run.key
        clean = []
        for el in arr:
            if isinstance(el, (int, float)) and not isinstance(el, bool):
                if clean and isinstance(clean[-1], (int, float)) and not isinstance(clean[-1], bool):
                    clean[-1] = clean[-1] + el
                else:
                    clean.append(el)
            elif isinstance(el, (bytes, bytearray)):
                if len(el) == 0:
                    continue
                clean.append(el if isinstance(el, Str) else Str(bytes(el)))
        clean = [(round(x, 3) if isinstance(x, float) else x) for x in clean
                 if not (isinstance(x, (int, float)) and not isinstance(x, bool) and abs(x) < 1e-3)]
        if not clean:
            clean = [Str(b'')]
        tj = Instr([clean], 'TJ')
        if orig_ins.op == "'":
            new_sub = [Instr([], 'T*'), tj]
        elif orig_ins.op == '"':
            new_sub = [Instr([orig_ins.operands[0]], 'Tw'), Instr([orig_ins.operands[1]], 'Tc'), Instr([], 'T*'), tj]
        else:
            new_sub = [tj]
        P = E.page(key)
        cur = P.ops[run.index]
        if cur.op == '__multi__':
            subs = list(cur.operands)
            subs[run.sub:run.sub + 1] = new_sub
            P.ops[run.index] = Instr(subs, '__multi__')
        elif len(new_sub) == 1:
            P.ops[run.index] = new_sub[0]
        else:
            P.ops[run.index] = Instr(new_sub, '__multi__')
        E.dirty.add(key)

    def _num(self, run, delta_ts):
        """TJ number that moves the pen by delta_ts (text-space units, positive = right)."""
        if run.fs * run.th == 0:
            return 0
        return -delta_ts * 1000.0 / (run.fs * run.th)

    def _split_array(self, run, arr, g0, g1):
        """split TJ array around glyph indices [g0, g1] of the run -> (before, after) element lists."""
        glyphs = run.glyphs
        a = glyphs[g0]
        b = glyphs[g1]
        before = []
        after = []
        for ei, el in enumerate(arr):
            if isinstance(el, (int, float)) and not isinstance(el, bool):
                if ei < a.elem:
                    before.append(el)
                elif ei > b.elem:
                    after.append(el)
                # numbers between the matched glyphs are dropped
                continue
            el = bytes(el)
            if ei < a.elem:
                before.append(el)
            elif ei > b.elem:
                after.append(el)
            else:
                if ei == a.elem:
                    before.append(el[:a.off])
                if ei == b.elem:
                    after.append(el[b.off + len(b.cb):])
        return before, after

    def width_ts(self, run, text):
        """width of text in the run's font (text-space units)."""
        return run.font.text_width(text, run.fs, run.tc, run.tw, run.th)

    # -------------------------------------------------------------- public edits
    def replace(self, match, new_text, align='left', keep_rest=True, font_run=None, verbose=True):
        """replace match by new_text in the SAME font/size/colour.
        align: 'left' | 'center' | 'right' relative to the old text.
        keep_rest: text after the match inside the same operator keeps its position."""
        runs = match.runs
        r1 = runs[0]
        g_in_r1 = [g for g in match.glyphs if g.run is r1]
        g0, g1 = g_in_r1[0].k, g_in_r1[-1].k
        font = r1.font
        if font is None:
            raise ValueError('Không đọc được font của đoạn chữ')
        newb = font.encode(new_text) if new_text else b''
        Wn = self.width_ts(r1, new_text) if new_text else 0.0
        # old width measured along r1 baseline in r1 text-space
        u = r1.u
        p0 = match.glyphs[0].o
        p1 = match.glyphs[-1].e
        Wo = ((p1[0] - p0[0]) * u[0] + (p1[1] - p0[1]) * u[1]) / r1.scale_x
        if align == 'left':
            shift = 0.0
        elif align == 'center':
            shift = (Wo - Wn) / 2.0
        elif align == 'right':
            shift = Wo - Wn
        else:
            raise ValueError("align phải là 'left' | 'center' | 'right'")
        arr, orig = self._as_tj(r1)
        before, after = self._split_array(r1, arr, g0, g1)
        new_arr = list(before)
        if abs(shift) > 1e-6:
            new_arr.append(self._num(r1, shift))
        if newb:
            new_arr.append(Str(newb))
        has_rest = any(isinstance(x, (bytes, bytearray)) and len(x) for x in after)
        if len(runs) == 1:
            if keep_rest and has_rest:
                comp = Wo - (shift + Wn)
                new_arr.append(self._num(r1, comp))
            new_arr += after
            self._write_tj(r1, new_arr, orig)
        else:
            new_arr += after if g1 < len(r1.glyphs) - 1 else []
            self._write_tj(r1, new_arr, orig)
            for r in runs[1:]:
                gs = [g for g in match.glyphs if g.run is r]
                arr2, orig2 = self._as_tj(r)
                b2, a2 = self._split_array(r, arr2, gs[0].k, gs[-1].k)
                removed = gs[-1].ts1 - gs[0].ts0
                na = list(b2)
                if keep_rest and any(isinstance(x, (bytes, bytearray)) and len(x) for x in a2):
                    na.append(self._num(r, removed))
                na += a2
                self._write_tj(r, na, orig2)
        self._runs.clear()
        if verbose:
            print('p%s: %r -> %r (font %s %.1fpt, căn %s)' % (match.key + 1 if isinstance(match.key, int) else match.key,
                                                             match.text, new_text, font.family, r1.size_page, align))
        self.E.log.append(dict(page=match.key + 1 if isinstance(match.key, int) else str(match.key), kind='text',
                               old=match.text, new=new_text, align=align, bbox=[round(v, 2) for v in match.bbox]))

    def delete(self, match, keep_rest=True):
        self.replace(match, '', align='left', keep_rest=keep_rest)

    def insert_like(self, ref, text, origin, verbose=True):
        """write `text` with the same font/size/colour/rendering as reference glyph or match `ref`,
        starting at page point `origin` (baseline-left).  Appended at the end of the stream holding ref."""
        g = ref.glyphs[0] if isinstance(ref, TMatch) else ref
        r = g.run
        font = r.font
        b = font.encode(text)
        key = r.key
        # desired text matrix in page space: same orientation/scale as run, translated to origin
        TmCtm = r.Tm @ r.ctm
        # we emit:  q  cm(X)  BT  Tf Tc Tw Tz Ts Tr color Tm(Tm2) (b)Tj ET Q
        # with X = r.ctm @ inv(end_ctm(key)) so that the effective CTM == r.ctm
        if key not in self.end_ctm:
            self.runs(key if isinstance(key, int) else 0)
        endc = self.end_ctm.get(key, np.eye(3))
        X = r.ctm @ np.linalg.inv(endc)
        # Tm2: like r.Tm but translated so that its origin maps to `origin` in page space
        inv_ctm = np.linalg.inv(r.ctm)
        ox, oy = apply(inv_ctm, origin[0], origin[1])
        Tm2 = r.Tm.copy()
        Tm2[2, 0] = ox
        Tm2[2, 1] = oy
        ops = [Instr([], 'q'), Instr([round(X[0, 0], 6), round(X[0, 1], 6), round(X[1, 0], 6), round(X[1, 1], 6), round(X[2, 0], 4), round(X[2, 1], 4)], 'cm')]
        if r.fill_cs is not None:
            ops.append(Instr([r.fill_cs], 'cs'))
        fop, fv = r.fill
        ops.append(Instr(list(fv), fop))
        ops += [Instr([], 'BT'), Instr([Name(r.fontname), r.fs], 'Tf')]
        if r.tc:
            ops.append(Instr([r.tc], 'Tc'))
        if r.tw:
            ops.append(Instr([r.tw], 'Tw'))
        if r.th != 1.0:
            ops.append(Instr([r.th * 100], 'Tz'))
        if r.ts:
            ops.append(Instr([r.ts], 'Ts'))
        if r.tr:
            ops.append(Instr([r.tr], 'Tr'))
        ops.append(Instr([round(Tm2[0, 0], 6), round(Tm2[0, 1], 6), round(Tm2[1, 0], 6), round(Tm2[1, 1], 6), round(Tm2[2, 0], 4), round(Tm2[2, 1], 4)], 'Tm'))
        ops.append(Instr([Str(b)], 'Tj'))
        ops += [Instr([], 'ET'), Instr([], 'Q')]
        P = self.E.page(key)
        self.E.ins[key][len(P.ops)].extend(ops)
        self._runs.clear()
        if verbose:
            print('p%s: thêm %r tại (%.2f, %.2f) font %s %.1fpt' % (key + 1 if isinstance(key, int) else key, text, origin[0], origin[1],
                                                                   font.family, r.size_page))
        self.E.log.append(dict(page=key + 1 if isinstance(key, int) else str(key), kind='text', old='', new=text,
                               at=[round(origin[0], 2), round(origin[1], 2)]))
