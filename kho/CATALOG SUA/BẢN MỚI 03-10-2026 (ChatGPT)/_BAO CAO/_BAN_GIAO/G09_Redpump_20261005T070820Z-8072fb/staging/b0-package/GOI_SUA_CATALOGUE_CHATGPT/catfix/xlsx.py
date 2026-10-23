"""Excel (.xlsx) edits at XML level - everything else in the file (images, print setup, styles)
stays byte-identical.  No openpyxl save (openpyxl can drop images/drawings).

    X = Xlsx('in.xlsx')
    X.cells('Sheet1')                       # {'A1': 'text', ...} (shared strings resolved)
    X.set_text('Sheet1', 'A11', 'Warranty: 1 year')
    X.replace_in_cell('Sheet1', 'A8', '380 - 420V', '380 - 415V')
    X.set_number('Sheet1', 'C27', 0.45)
    X.media()                               # images inside the workbook: ['xl/media/image1.png', ...]
    X.put_media('xl/media/image2.png', png_bytes)
    X.save('out.xlsx');  diff_cells('in.xlsx', 'out.xlsx')
"""
import io
import re
import os
import zipfile
from xml.sax.saxutils import escape


def _unesc(s):
    return (s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&'))


class Xlsx(object):
    def __init__(self, path):
        self.path = path
        z = zipfile.ZipFile(path)
        self.order = [i.filename for i in z.infolist()]
        self.info = {i.filename: i for i in z.infolist()}
        self.data = {n: z.read(n) for n in self.order}
        z.close()
        self._sheets = None

    # -------------------------------------------------------------- structure
    def sheets(self):
        if self._sheets is None:
            wb = self.data['xl/workbook.xml'].decode('utf-8')
            rels = self.data['xl/_rels/workbook.xml.rels'].decode('utf-8')
            rid = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels)}
            rid.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship[^>]*Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
            out = {}
            for m in re.finditer(r'<sheet\b[^>]*?name="([^"]+)"[^>]*?r:id="([^"]+)"', wb):
                t = rid.get(m.group(2), '')
                t = t.lstrip('/')
                out[_unesc(m.group(1))] = t if t.startswith('xl/') else 'xl/' + t
            self._sheets = out
        return self._sheets

    def _ss(self):
        x = self.data.get('xl/sharedStrings.xml', b'').decode('utf-8')
        items = re.findall(r'<si>(.*?)</si>', x, re.S)
        return x, items

    @staticmethod
    def si_text(si):
        return _unesc(''.join(re.findall(r'<t(?:\s[^>]*)?>(.*?)</t>', si, re.S)))

    def cells(self, sheet):
        x = self.data[self.sheets()[sheet]].decode('utf-8')
        _, items = self._ss()
        out = {}
        for m in re.finditer(r'<c r="([A-Z]+\d+)"([^>]*?)(?:/>|>(.*?)</c>)', x, re.S):
            ref, attrs, body = m.group(1), m.group(2), m.group(3) or ''
            t = re.search(r't="(\w+)"', attrs)
            t = t.group(1) if t else None
            v = re.search(r'<v>(.*?)</v>', body, re.S)
            f = re.search(r'<f[^>]*>(.*?)</f>', body, re.S)
            if t == 's' and v:
                out[ref] = self.si_text(items[int(v.group(1))])
            elif t == 'inlineStr':
                out[ref] = _unesc(''.join(re.findall(r'<t(?:\s[^>]*)?>(.*?)</t>', body, re.S)))
            elif v:
                out[ref] = ('=' + _unesc(f.group(1)) + ' -> ' if f else '') + _unesc(v.group(1))
            elif f:
                out[ref] = '=' + _unesc(f.group(1))
        return out

    def find(self, text):
        hits = []
        for sh in self.sheets():
            for ref, val in self.cells(sh).items():
                if text in str(val):
                    hits.append((sh, ref, val))
        return hits

    # -------------------------------------------------------------- edits
    def _cell_match(self, sheet, ref):
        name = self.sheets()[sheet]
        x = self.data[name].decode('utf-8')
        m = re.search(r'<c r="%s"([^>]*?)(?:/>|>(.*?)</c>)' % ref, x, re.S)
        if not m:
            raise KeyError('Không thấy ô %s trong %s' % (ref, sheet))
        return name, x, m

    def _shared_use_count(self, idx):
        n = 0
        for sh, name in self.sheets().items():
            x = self.data[name].decode('utf-8')
            n += len(re.findall(r'<c [^>]*t="s"[^>]*>\s*<v>%d</v>' % idx, x))
        return n

    def replace_in_cell(self, sheet, ref, old, new, count=1):
        """replace text inside a cell (keeps rich-text runs / fonts).  Works for shared strings."""
        name, x, m = self._cell_match(sheet, ref)
        attrs, body = m.group(1), m.group(2) or ''
        if 't="s"' in attrs:
            idx = int(re.search(r'<v>(\d+)</v>', body).group(1))
            ssx, items = self._ss()
            si = items[idx]
            if old not in self.si_text(si):
                raise ValueError('Ô %s không chứa %r (đang là %r)' % (ref, old, self.si_text(si)))
            new_si = self._replace_in_si(si, old, new, count)
            if self._shared_use_count(idx) > 1:
                # string shared with other cells -> add a new shared string just for this cell
                ssx2 = ssx.replace('</sst>', '<si>%s</si></sst>' % new_si)
                ssx2 = re.sub(r'uniqueCount="(\d+)"', lambda mm: 'uniqueCount="%d"' % (int(mm.group(1)) + 1), ssx2, 1)
                self.data['xl/sharedStrings.xml'] = ssx2.encode('utf-8')
                new_idx = len(items)
                x2 = x[:m.start()] + m.group(0).replace('<v>%d</v>' % idx, '<v>%d</v>' % new_idx) + x[m.end():]
                self.data[name] = x2.encode('utf-8')
            else:
                parts = re.split(r'(<si>.*?</si>)', ssx, flags=re.S)
                k = -1
                for i, p in enumerate(parts):
                    if p.startswith('<si>'):
                        k += 1
                        if k == idx:
                            parts[i] = '<si>%s</si>' % new_si
                            break
                self.data['xl/sharedStrings.xml'] = ''.join(parts).encode('utf-8')
            return
        if 't="inlineStr"' in attrs:
            new_body = self._replace_in_si(body, old, new, count)
            x2 = x[:m.start()] + m.group(0).replace(body, new_body) + x[m.end():]
            self.data[name] = x2.encode('utf-8')
            return
        raise ValueError('Ô %s không phải ô chữ - dùng set_number / set_text' % ref)

    @staticmethod
    def _replace_in_si(si, old, new, count=1):
        # try inside a single <t> first (keeps formatting); else merge into the first run
        def rep(mm):
            return mm.group(1) + escape(_unesc(mm.group(2)).replace(old, new, count)) + mm.group(3)
        ts = list(re.finditer(r'(<t(?:\s[^>]*)?>)(.*?)(</t>)', si, re.S))
        for t in ts:
            if old in _unesc(t.group(2)):
                return si[:t.start()] + rep(t) + si[t.end():]
        full = ''.join(_unesc(t.group(2)) for t in ts)
        if old not in full:
            raise ValueError('không thấy %r' % old)
        newfull = full.replace(old, new, count)
        first = ts[0]
        out = si[:first.start()] + first.group(1).replace('<t>', '<t xml:space="preserve">') + escape(newfull) + '</t>'
        rest = si[first.end():]
        rest = re.sub(r'(<t(?:\s[^>]*)?>)(.*?)(</t>)', r'\1\3', rest, flags=re.S)
        return out + rest

    def set_text(self, sheet, ref, text):
        """set whole text of a text cell (keeps the cell style; first run formatting kept)."""
        cur = self.cells(sheet).get(ref)
        if cur is None:
            raise KeyError(ref)
        self.replace_in_cell(sheet, ref, cur, text)

    def _drop_calc_chain(self, sheet_name, refs):
        cc = self.data.get('xl/calcChain.xml')
        if not cc:
            return
        s = cc.decode('utf-8')
        sheets = list(self.sheets().values())
        sid = sheets.index(sheet_name) + 1 if sheet_name in sheets else None
        for r in refs:
            s = re.sub(r'<c r="%s"(?: i="%s")?[^>]*/>' % (r, sid if sid else r'\d+'), '', s)
        self.data['xl/calcChain.xml'] = s.encode('utf-8')

    def _freeze_shared_group(self, name, x, si):
        """turn every cell of shared-formula group `si` into a constant (keeps cached values)."""
        refs = []

        def fix(mm):
            refs.append(mm.group(1))
            body = re.sub(r'<f[^>]*t="shared"[^>]*si="%s"[^>]*?(?:/>|>.*?</f>)' % si, '', mm.group(3), flags=re.S)
            return '<c r="%s"%s>%s</c>' % (mm.group(1), mm.group(2), body)
        x2 = re.sub(r'<c r="([A-Z]+\d+)"([^>]*?)>((?:(?!</c>).)*?<f[^>]*t="shared"[^>]*si="%s"(?:(?!</c>).)*?)</c>' % si, fix, x, flags=re.S)
        self.data[name] = x2.encode('utf-8')
        self._drop_calc_chain(name, refs)
        return x2, refs

    def set_number(self, sheet, ref, value, keep_formula=False):
        """write a plain number.  If the cell belongs to a SHARED formula group, the whole group is
        first turned into constants (each keeps its current value) so the workbook stays valid."""
        name, x, m = self._cell_match(sheet, ref)
        body0 = m.group(2) or ''
        sh = re.search(r'<f[^>]*t="shared"[^>]*si="(\d+)"', body0)
        if sh and not keep_formula:
            x, refs = self._freeze_shared_group(name, x, sh.group(1))
            name, x, m = self._cell_match(sheet, ref)
        elif re.search(r'<f', body0) and not keep_formula:
            self._drop_calc_chain(name, [ref])
        attrs, body = m.group(1), m.group(2) or ''
        if 't="s"' in attrs or 't="inlineStr"' in attrs or 't="str"' in attrs:
            attrs2 = re.sub(r'\s*t="\w+"', '', attrs)
        else:
            attrs2 = attrs
        v = repr(float(value)) if not float(value).is_integer() else str(int(value))
        f = re.search(r'<f[^>]*>.*?</f>|<f[^>]*/>', body, re.S)
        body2 = ((f.group(0) if (f and keep_formula) else '') + '<v>%s</v>' % v)
        new = '<c r="%s"%s>%s</c>' % (ref, attrs2, body2)
        self.data[name] = (x[:m.start()] + new + x[m.end():]).encode('utf-8')

    def replace_font_name(self, old, new):
        """rename a font everywhere (styles + rich text runs), e.g. '.VnCooper' -> 'Cooper Black'."""
        n = 0
        for part in ('xl/styles.xml', 'xl/sharedStrings.xml'):
            if part in self.data:
                s = self.data[part].decode('utf-8')
                k = s.count('val="%s"' % old)
                s = s.replace('val="%s"' % old, 'val="%s"' % new)
                self.data[part] = s.encode('utf-8')
                n += k
        return n

    # -------------------------------------------------------------- media
    def media(self):
        return [n for n in self.order if n.startswith('xl/media/')]

    def get_media(self, name):
        return self.data[name]

    def put_media(self, name, data):
        if name not in self.data:
            raise KeyError(name)
        self.data[name] = data

    # -------------------------------------------------------------- save
    def save(self, path):
        from ._compat import same_file
        if same_file(path, self.path):
            raise ValueError('Không ghi đè file gốc')
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with zipfile.ZipFile(path, 'w') as z:
            for n in self.order:
                inf = self.info[n]
                zi = zipfile.ZipInfo(n, date_time=inf.date_time)
                zi.compress_type = inf.compress_type
                zi.external_attr = inf.external_attr
                z.writestr(zi, self.data[n])
        return path


def diff_cells(a, b):
    """[(sheet, cell, old, new)] for every cell whose value differs."""
    A, B = Xlsx(a), Xlsx(b)
    out = []
    for sh in A.sheets():
        ca, cb = A.cells(sh), B.cells(sh) if sh in B.sheets() else {}
        for ref in sorted(set(ca) | set(cb)):
            if ca.get(ref) != cb.get(ref):
                out.append((sh, ref, ca.get(ref), cb.get(ref)))
    return out


def diff_parts(a, b):
    """zip parts that changed (to prove nothing else was touched)."""
    A, B = Xlsx(a), Xlsx(b)
    return [n for n in sorted(set(A.data) | set(B.data)) if A.data.get(n) != B.data.get(n)]
