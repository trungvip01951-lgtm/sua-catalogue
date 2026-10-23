"""Vector content: paint objects, subpaths, glyph groups + an Editor that edits page content
streams losslessly (only touched instructions change).

Coordinates returned by this module are PDF page coordinates (origin bottom-left, points),
i.e. after applying the CTM.

Typical use:
    E = Editor('in.pdf')
    P = E.page(4)                 # 0-based page index
    for oi, o in enumerate(P.objs): ...
    gs = P.glyphs(oi)             # glyph groups (subpaths grouped by bbox containment)
    E.delete_group(4, oi, gs[0])
    E.insert_path(4, oi, E.glyph_pagepath(4, oi2, g2), dx, dy)
    E.save('out.pdf')
"""
import collections
import numpy as np

from . import cs
from .cs import Instr, Name
from .pdfdoc import PdfDoc

PATH_OPS = {'m', 'l', 'c', 'v', 'y', 'h', 're'}
PAINT_OPS = {'f', 'F', 'f*', 'B', 'B*', 'b', 'b*', 'S', 's', 'n'}
FILL_OPS = {'f', 'F', 'f*', 'B', 'B*', 'b', 'b*'}
STROKE_OPS = {'S', 's', 'B', 'B*', 'b', 'b*'}
COLOR_FILL = {'rg', 'g', 'k', 'sc', 'scn'}
COLOR_STROKE = {'RG', 'G', 'K', 'SC', 'SCN'}


def M(a, b, c, d, e, f):
    return np.array([[a, b, 0.0], [c, d, 0.0], [e, f, 1.0]], dtype=float)


def apply(Mx, x, y):
    return (x * Mx[0, 0] + y * Mx[1, 0] + Mx[2, 0], x * Mx[0, 1] + y * Mx[1, 1] + Mx[2, 1])


def union(bbs):
    bbs = list(bbs)
    return (min(b[0] for b in bbs), min(b[1] for b in bbs), max(b[2] for b in bbs), max(b[3] for b in bbs))


def overlap(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def _f(x):
    return float(x)


class VPage(object):
    """Parsed content of one page (or one form XObject).

    objs[k] = dict(i0, i1, op, fill, stroke, lw, dash, gs, ctm, fill_cs, stroke_cs, subs=[...], bbox)
       i0 = index of first path instruction, i1 = index of the painting instruction
       subs[j] = dict(j0, j1, pts, bbox)  instructions [j0, j1) of one subpath
    images[k] = dict(i, name, ctm)     every 'Do' (image or form) and inline image 'BI'
    """

    def __init__(self, instrs, base_ctm=None):
        self.ops = instrs
        self.base_ctm = np.eye(3) if base_ctm is None else base_ctm
        self._parse()
        self._gcache = {}

    def _parse(self):
        ops = self.ops
        ctm = self.base_ctm.copy()
        st = dict(fill=('g', (0,)), stroke=('G', (0,)), lw=1.0, dash=None, gs=None, fill_cs=None, stroke_cs=None,
                  clip=None, textclip=False)
        clip_pending = False
        tr_mode = 0
        text_used_clip = False
        stack = []
        self.objs = []
        self.images = []
        self.texts = []
        cur = None
        in_text = None
        for i, ins in enumerate(ops):
            op = ins.op
            v = ins.operands
            if op == 'q':
                stack.append((ctm.copy(), dict(st)))
            elif op == 'Q':
                if stack:
                    ctm, st = stack.pop()
            elif op == 'cm':
                ctm = M(*[_f(x) for x in v]) @ ctm
            elif op in COLOR_FILL:
                st['fill'] = (op, tuple(x if isinstance(x, Name) else _f(x) for x in v))
                if op in ('rg', 'g', 'k'):
                    st['fill_cs'] = None
            elif op in COLOR_STROKE:
                st['stroke'] = (op, tuple(x if isinstance(x, Name) else _f(x) for x in v))
                if op in ('RG', 'G', 'K'):
                    st['stroke_cs'] = None
            elif op == 'cs':
                st['fill_cs'] = str(v[0]) if v else None
            elif op == 'CS':
                st['stroke_cs'] = str(v[0]) if v else None
            elif op == 'w':
                st['lw'] = _f(v[0]) if v else 1.0
            elif op == 'd':
                st['dash'] = (v[0], v[1]) if len(v) >= 2 else None
            elif op == 'gs':
                st['gs'] = str(v[0]) if v else None
            elif op in PATH_OPS:
                if cur is None:
                    cur = dict(i0=i, subs=[], ctm=ctm.copy(), **st)
                vals = [_f(x) for x in v]
                if op in ('m', 're') or not cur['subs']:
                    cur['subs'].append(dict(j0=i, pts=[]))
                s = cur['subs'][-1]
                if op == 're':
                    x, y, w, h = vals
                    s['pts'] += [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
                elif op != 'h':
                    s['pts'] += list(zip(vals[0::2], vals[1::2]))
            elif op in PAINT_OPS:
                if cur is None:
                    clip_pending = False
                    continue
                cur['i1'] = i
                cur['op'] = op
                cur.update(st)
                subs = cur['subs']
                C = cur['ctm']
                for k, s in enumerate(subs):
                    s['j1'] = subs[k + 1]['j0'] if k + 1 < len(subs) else i
                    if s['pts']:
                        P = np.array([[x, y, 1.0] for x, y in s['pts']]) @ C
                        s['bbox'] = (P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max())
                    else:
                        s['bbox'] = (0.0, 0.0, 0.0, 0.0)
                cur['subs'] = [s for s in subs if s['pts']]
                if cur['subs']:
                    cur['bbox'] = union(s['bbox'] for s in cur['subs'])
                    if clip_pending:
                        cb = cur['bbox']
                        old = st['clip']
                        st['clip'] = cb if old is None else (max(old[0], cb[0]), max(old[1], cb[1]), min(old[2], cb[2]), min(old[3], cb[3]))
                    cur['clip'] = st['clip']
                    self.objs.append(cur)
                clip_pending = False
                cur = None
            elif op in ('W', 'W*'):
                clip_pending = True
            elif op == 'Do':
                self.images.append(dict(i=i, name=str(v[0]), ctm=ctm.copy(), kind='Do', clip=st['clip'], textclip=st['textclip'], gs=st['gs']))
            elif op == 'BI':
                self.images.append(dict(i=i, name=None, ctm=ctm.copy(), kind='BI', clip=st['clip'], textclip=st['textclip']))
            elif op == 'BT':
                in_text = i
                text_used_clip = False
            elif op == 'Tr':
                try:
                    tr_mode = int(v[0])
                except Exception:
                    tr_mode = 0
            elif op in ('Tj', 'TJ', "'", '"'):
                if tr_mode >= 4:
                    text_used_clip = True
            elif op == 'ET':
                if in_text is not None:
                    self.texts.append((in_text, i, ctm.copy()))
                if text_used_clip:
                    st['textclip'] = True
                in_text = None

    # ----------------------------------------------------------- state replay
    def ctm_at(self, index):
        """CTM in force just BEFORE instruction `index` (replays q/Q/cm)."""
        ctm = self.base_ctm.copy()
        stack = []
        for ins in self.ops[:index]:
            if ins.op == 'q':
                stack.append(ctm.copy())
            elif ins.op == 'Q':
                if stack:
                    ctm = stack.pop()
            elif ins.op == 'cm':
                ctm = M(*[_f(x) for x in ins.operands]) @ ctm
        return ctm

    def q_pairs(self):
        """{index_of_q: index_of_matching_Q}"""
        if hasattr(self, '_qp'):
            return self._qp
        st = []
        pairs = {}
        for i, ins in enumerate(self.ops):
            if ins.op == 'q':
                st.append(i)
            elif ins.op == 'Q' and st:
                pairs[st.pop()] = i
        self._qp = pairs
        return pairs

    def enclosing_block(self, index, allowed=('q', 'Q', 'cm', 're', 'm', 'l', 'c', 'v', 'y', 'h', 'W', 'W*', 'n', 'gs', 'ri', 'i')):
        """largest q...Q block around instruction `index` that contains nothing else but clipping /
        state set-up (so moving the whole block moves only that drawing, with its clip).
        returns (start, end) indices (inclusive) or (index, index)."""
        best = (index, index)
        for a, b in sorted(self.q_pairs().items()):
            if a < index < b:
                ok = all((j == index) or (self.ops[j].op in allowed) for j in range(a, b + 1))
                if ok and (b - a) > (best[1] - best[0]):
                    best = (a, b)
        # also absorb clip-only sibling blocks directly before (q re W n Q) - harmless, keep as is
        return best

    # ----------------------------------------------------------- queries
    def obj_bbox(self, oi):
        return self.objs[oi]['bbox']

    def glyphs(self, oi):
        """group subpaths of paint object oi into glyph groups by bbox containment (sorted by x)."""
        if ('g', oi) in self._gcache:
            return [dict(g, subs=list(g['subs'])) for g in self._gcache[('g', oi)]]
        o = self.objs[oi]
        subs = o['subs']
        order = sorted(range(len(subs)), key=lambda k: -(subs[k]['bbox'][2] - subs[k]['bbox'][0]) *
                       (subs[k]['bbox'][3] - subs[k]['bbox'][1]))
        groups = []
        t = 0.05
        for k in order:
            b = subs[k]['bbox']
            placed = False
            for g in groups:
                B = g['bbox']
                if b[0] >= B[0] - t and b[1] >= B[1] - t and b[2] <= B[2] + t and b[3] <= B[3] + t:
                    g['subs'].append(k)
                    placed = True
                    break
            if not placed:
                groups.append(dict(subs=[k], bbox=b, oi=oi))
        groups.sort(key=lambda g: g['bbox'][0])
        self._gcache[('g', oi)] = groups
        return [dict(g, subs=list(g['subs'])) for g in groups]

    def merged_glyphs(self, oi):
        """glyphs() + merge vertically stacked parts (i, j, :, ;, !, ?, =, accents)."""
        if ('m', oi) in self._gcache:
            return [dict(g, subs=list(g['subs'])) for g in self._gcache[('m', oi)]]
        gs = self.glyphs(oi)
        changed = True
        while changed:
            changed = False
            for a in range(len(gs)):
                for b in range(a + 1, len(gs)):
                    A = gs[a]['bbox']
                    B = gs[b]['bbox']
                    ox = min(A[2], B[2]) - max(A[0], B[0])
                    wmin = min(A[2] - A[0], B[2] - B[0])
                    vdis = A[3] <= B[1] + 0.05 or B[3] <= A[1] + 0.05
                    gap = max(B[1] - A[3], A[1] - B[3])
                    hmax = max(A[3] - A[1], B[3] - B[1])
                    if ox > 0.6 * wmin and vdis and gap < 0.8 * hmax:
                        gs[a]['subs'] += gs[b]['subs']
                        gs[a]['bbox'] = union([A, B])
                        del gs[b]
                        changed = True
                        break
                if changed:
                    break
        gs.sort(key=lambda g: g['bbox'][0])
        self._gcache[('m', oi)] = gs
        return [dict(g, subs=list(g['subs'])) for g in gs]

    def find(self, rect, center=True, ops=None):
        """subpaths (oi, si) whose bbox centre (or whole bbox) lies inside rect."""
        x0, y0, x1, y1 = rect
        out = []
        for oi, o in enumerate(self.objs):
            if ops and o['op'] not in ops:
                continue
            if overlap(o['bbox'], rect) <= 0 and not (o['bbox'][2] - o['bbox'][0] == 0 or o['bbox'][3] - o['bbox'][1] == 0):
                continue
            for si, s in enumerate(o['subs']):
                b = s['bbox']
                if center:
                    cx = (b[0] + b[2]) / 2
                    cy = (b[1] + b[3]) / 2
                    if x0 <= cx <= x1 and y0 <= cy <= y1:
                        out.append((oi, si))
                elif b[0] >= x0 and b[1] >= y0 and b[2] <= x1 and b[3] <= y1:
                    out.append((oi, si))
        return out

    def objects_in(self, rect, ops=None, full=False):
        """indices of paint objects overlapping (or fully inside, full=True) rect."""
        out = []
        for oi, o in enumerate(self.objs):
            if ops and o['op'] not in ops:
                continue
            b = o['bbox']
            if full:
                if b[0] >= rect[0] and b[1] >= rect[1] and b[2] <= rect[2] and b[3] <= rect[3]:
                    out.append(oi)
            elif overlap(b, rect) > 0 or (rect[0] <= b[0] <= rect[2] and rect[1] <= b[1] <= rect[3]):
                out.append(oi)
        return out

    def subpath_pagepath(self, oi, sub_indices):
        """list of (op, [(x, y), ...]) in page coordinates for the given subpaths of object oi."""
        o = self.objs[oi]
        C = o['ctm']
        out = []
        for k in sorted(sub_indices):
            s = o['subs'][k]
            for j in range(s['j0'], s['j1']):
                ins = self.ops[j]
                op = ins.op
                v = [_f(x) for x in ins.operands]
                if op == 're':
                    x, y, w, h = v
                    for op2, pp in (('m', (x, y)), ('l', (x + w, y)), ('l', (x + w, y + h)), ('l', (x, y + h)), ('h', ())):
                        out.append((op2, [apply(C, pp[0], pp[1])] if pp else []))
                    continue
                if op not in ('m', 'l', 'c', 'v', 'y', 'h'):
                    raise ValueError('unexpected op in path: ' + op)
                out.append((op, [apply(C, x, y) for x, y in zip(v[0::2], v[1::2])]))
        return out

    def object_pagepath(self, oi):
        return self.subpath_pagepath(oi, range(len(self.objs[oi]['subs'])))

    def color_of(self, oi, which='fill'):
        """(r, g, b) 0..1 for DeviceRGB/Gray/CMYK fills; None for other colour spaces."""
        o = self.objs[oi]
        op, vals = o[which]
        vals = [x for x in vals if not isinstance(x, Name)]
        if op in ('rg', 'RG') and len(vals) == 3:
            return tuple(vals)
        if op in ('g', 'G') and len(vals) == 1:
            return (vals[0],) * 3
        if op in ('k', 'K') and len(vals) == 4:
            c, m, y, k = vals
            return ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
        if len(vals) == 3:
            return tuple(vals)
        if len(vals) == 1:
            return (vals[0],) * 3
        if len(vals) == 4:
            c, m, y, k = vals
            return ((1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))
        return None


class Editor(object):
    """Edits page content streams of a PDF.  Changes are collected and applied in save().

    Target of every edit is a 'key': a page index (int) or ('form', Ref) for a form XObject.
    """

    def __init__(self, path, backend=None):
        self.path = path
        self.doc = PdfDoc(path, backend)
        self.pages = {}
        self.dels = collections.defaultdict(set)
        self.ins = collections.defaultdict(lambda: collections.defaultdict(list))
        self.mods = collections.defaultdict(dict)
        self.dirty = set()      # keys whose parsed instruction list was mutated in place (text edits)
        self.log = []

    # ------------------------------------------------------------ access
    def page(self, key):
        if key not in self.pages:
            if isinstance(key, tuple) and key[0] == 'form':
                data, left, d = self.doc.stream_decoded(key[1])
                self.pages[key] = VPage(cs.parse(data))
            else:
                self.pages[key] = VPage(cs.parse(self.doc.page_content(key)))
        return self.pages[key]

    P = page  # short alias

    @property
    def n_pages(self):
        return self.doc.n_pages

    def mediabox(self, pi):
        return self.doc.mediabox(pi)

    # ------------------------------------------------------------ geometry
    def glyph_pagepath(self, key, oi, g):
        return self.page(key).subpath_pagepath(oi, g['subs'])

    @staticmethod
    def transform_path(pagepath, Mx=None, dx=0.0, dy=0.0):
        out = []
        for op, pts in pagepath:
            q = []
            for x, y in pts:
                if Mx is not None:
                    x, y = apply(Mx, x, y)
                q.append((x + dx, y + dy))
            out.append((op, q))
        return out

    def _to_local(self, key, oi, pagepath):
        o = self.page(key).objs[oi]
        inv = np.linalg.inv(o['ctm'])
        instrs = []
        for op, pts in pagepath:
            loc = []
            for x, y in pts:
                lx, ly = apply(inv, x, y)
                loc += [round(float(lx), 4), round(float(ly), 4)]
            instrs.append(Instr(loc, op))
        return instrs

    # ------------------------------------------------------------ edits
    def delete_group(self, key, oi, g):
        o = self.page(key).objs[oi]
        for k in g['subs']:
            s = o['subs'][k]
            self.dels[key].update(range(s['j0'], s['j1']))

    def delete_subpaths(self, key, oi, sub_indices):
        self.delete_group(key, oi, dict(subs=list(sub_indices)))

    def delete_object(self, key, oi):
        o = self.page(key).objs[oi]
        self.dels[key].update(range(o['i0'], o['i1'] + 1))

    def delete_instrs(self, key, indices):
        self.dels[key].update(indices)

    def insert_path(self, key, oi_target, pagepath, dx=0.0, dy=0.0, Mx=None):
        """insert subpaths (page coords, optionally transformed by Mx then shifted) into the target
        object, just before its painting operator -> painted with the target's colour/state."""
        pp = self.transform_path(pagepath, Mx, dx, dy) if (Mx is not None or dx or dy) else pagepath
        o = self.page(key).objs[oi_target]
        self.ins[key][o['i1']].extend(self._to_local(key, oi_target, pp))

    def replace_path(self, key, oi, pagepath):
        """replace all path-construction instructions of object oi by pagepath (same paint op/state)."""
        o = self.page(key).objs[oi]
        P = self.page(key)
        for j in range(o['i0'], o['i1']):
            if P.ops[j].op in PATH_OPS:
                self.dels[key].add(j)
        self.ins[key][o['i1']].extend(self._to_local(key, oi, pagepath))

    def insert_object_after(self, key, oi_template, pagepath, paint_op=None):
        """draw a NEW path right after the template object's paint operator: the graphics state there
        is identical to the template's (CTM, colours, line width, dash, gs) -> same look."""
        o = self.page(key).objs[oi_template]
        instrs = self._to_local(key, oi_template, pagepath)
        instrs.append(Instr([], paint_op or o['op']))
        self.ins[key][o['i1'] + 1][0:0] = instrs

    def insert_instrs(self, key, index, instrs, before=True):
        if before:
            self.ins[key][index].extend(instrs)
        else:
            self.ins[key][index + 1][0:0] = instrs

    def modify_instr(self, key, index, new_instr):
        self.mods[key][index] = new_instr

    def move_group(self, key, oi, g, dx, dy):
        path = self.glyph_pagepath(key, oi, g)
        self.delete_group(key, oi, g)
        self.insert_path(key, oi, path, dx, dy)

    def move_object(self, key, oi, dx, dy):
        P = self.page(key)
        self.move_group(key, oi, dict(subs=list(range(len(P.objs[oi]['subs'])))), dx, dy)

    # ------------------------------------------------------------ build / save
    def touched(self):
        return sorted(set(list(self.dels.keys()) + list(self.ins.keys()) + list(self.mods.keys()) + list(self.dirty)), key=str)

    def build(self, key):
        P = self.page(key)
        out = []
        ins_map = self.ins.get(key, {})
        dels = self.dels.get(key, set())
        mods = self.mods.get(key, {})
        n = len(P.ops)
        for j, ins in enumerate(P.ops):
            if j in ins_map:
                out.extend(ins_map[j])
            if j in dels:
                continue
            out.append(mods.get(j, ins))
        if n in ins_map:
            out.extend(ins_map[n])
        return cs.serialize(out)

    def save(self, path):
        for key in self.touched():
            if not (self.dels.get(key) or self.ins.get(key) or self.mods.get(key) or key in self.dirty):
                continue
            data = self.build(key)
            if isinstance(key, tuple) and key[0] == 'form':
                self.doc.set_stream(key[1], data)
            else:
                self.doc.set_page_content(key, data)
        self.doc.save(path)
        return path

    def close(self):
        """đóng file vào (trên Windows file đang mở thì không ghi đè/xoá được)."""
        self.doc.close()

    def reset(self):
        self.dels.clear()
        self.ins.clear()
        self.mods.clear()
        self.dirty.clear()
        self.pages.clear()
