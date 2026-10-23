"""PDF font handling for text-layer editing: code <-> unicode, widths, glyph availability."""
import io
import re

from .cs import Name, Str, Ref

try:
    from fontTools.ttLib import TTFont
    from fontTools.cffLib import CFFFontSet
except Exception:  # pragma: no cover
    TTFont = None
    CFFFontSet = None

# ------------------------------------------------------------------ glyph names
_AGL_EXTRA = {
    'space': ' ', 'exclam': '!', 'quotedbl': '"', 'numbersign': '#', 'dollar': '$', 'percent': '%', 'ampersand': '&',
    'quotesingle': "'", 'quoteright': '’', 'quoteleft': '‘', 'parenleft': '(', 'parenright': ')', 'asterisk': '*',
    'plus': '+', 'comma': ',', 'hyphen': '-', 'minus': '−', 'period': '.', 'slash': '/', 'zero': '0', 'one': '1',
    'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'colon': ':',
    'semicolon': ';', 'less': '<', 'equal': '=', 'greater': '>', 'question': '?', 'at': '@', 'bracketleft': '[',
    'backslash': '\\', 'bracketright': ']', 'asciicircum': '^', 'underscore': '_', 'grave': '`', 'braceleft': '{',
    'bar': '|', 'braceright': '}', 'asciitilde': '~', 'degree': '°', 'twosuperior': '²', 'threesuperior': '³',
    'mu': 'µ', 'micro': 'µ', 'plusminus': '±', 'multiply': '×', 'divide': '÷', 'endash': '–',
    'emdash': '—', 'bullet': '•', 'ellipsis': '…', 'quotedblleft': '“', 'quotedblright': '”',
    'quotesinglbase': '‚', 'quotedblbase': '„', 'copyright': '©', 'registered': '®', 'trademark': '™',
    'nbspace': ' ', 'uni00A0': ' ', 'Euro': '€', 'florin': 'ƒ', 'dagger': '†', 'daggerdbl': '‡',
    'section': '§', 'paragraph': '¶', 'periodcentered': '·', 'middot': '·', 'ordfeminine': 'ª',
    'ordmasculine': 'º', 'onehalf': '½', 'onequarter': '¼', 'threequarters': '¾', 'onesuperior': '¹',
    'fi': 'ﬁ', 'fl': 'ﬂ', 'germandbls': 'ß', 'Oslash': 'Ø', 'oslash': 'ø', 'AE': 'Æ', 'ae': 'æ',
    'OE': 'Œ', 'oe': 'œ', 'dotlessi': 'ı', 'Lslash': 'Ł', 'lslash': 'ł', 'Eth': 'Ð', 'eth': 'ð',
    'Thorn': 'Þ', 'thorn': 'þ', 'exclamdown': '¡', 'questiondown': '¿', 'guillemotleft': '«',
    'guillemotright': '»', 'guilsinglleft': '‹', 'guilsinglright': '›', 'cent': '¢', 'sterling': '£',
    'yen': '¥', 'currency': '¤', 'brokenbar': '¦', 'dieresis': '¨', 'macron': '¯', 'acute': '´',
    'cedilla': '¸', 'logicalnot': '¬', 'softhyphen': '­', 'circumflex': 'ˆ', 'tilde': '˜',
    'perthousand': '‰', 'Scaron': 'Š', 'scaron': 'š', 'Zcaron': 'Ž', 'zcaron': 'ž',
    'Ydieresis': 'Ÿ', 'phi': 'φ', 'Phi': 'Φ', 'uni03D5': 'ϕ', 'Omega': 'Ω', 'Delta': 'Δ',
    'litre': 'ℓ', 'uni2113': 'ℓ', 'minute': '′', 'second': '″',
}
_ACC = {'grave': '̀', 'acute': '́', 'circumflex': '̂', 'tilde': '̃', 'dieresis': '̈', 'ring': '̊',
        'cedilla': '̧', 'caron': '̌'}


def glyph_to_unicode(name):
    if name is None:
        return None
    name = str(name)
    if name in _AGL_EXTRA:
        return _AGL_EXTRA[name]
    if len(name) == 1:
        return name
    m = re.fullmatch(r'uni([0-9A-Fa-f]{4})+', name)
    if m:
        h = name[3:]
        return ''.join(chr(int(h[i:i + 4], 16)) for i in range(0, len(h), 4))
    m = re.fullmatch(r'u([0-9A-Fa-f]{4,6})', name)
    if m:
        return chr(int(m.group(1), 16))
    base = name.split('.')[0].split('_')[0]
    if base != name:
        return glyph_to_unicode(base)
    for acc, comb in _ACC.items():
        if name.endswith(acc) and len(name) == len(acc) + 1:
            import unicodedata
            return unicodedata.normalize('NFC', name[0] + comb)
    return None


def _cp1252(code):
    try:
        return bytes([code]).decode('cp1252')
    except Exception:
        return chr(code) if code >= 32 else None


def _pua(u):
    return any(0xE000 <= ord(ch) <= 0xF8FF for ch in u)


def _macroman(code):
    try:
        return bytes([code]).decode('mac_roman')
    except Exception:
        return None


# ------------------------------------------------------------------ CMap parsing
def parse_cmap(data):
    """ToUnicode CMap -> (dict code_bytes -> unicode str, list of codespace byte lengths)."""
    if isinstance(data, bytes):
        txt = data.decode('latin-1')
    else:
        txt = data
    out = {}
    lens = set()
    for m in re.finditer(r'begincodespacerange(.*?)endcodespacerange', txt, re.S):
        for a in re.findall(r'<([0-9A-Fa-f]+)>\s*<[0-9A-Fa-f]+>', m.group(1)):
            lens.add(len(a) // 2)

    def u16(h):
        b = bytes.fromhex(h)
        try:
            return b.decode('utf-16-be')
        except Exception:
            return ''.join(chr(x) for x in b)

    for m in re.finditer(r'beginbfchar(.*?)endbfchar', txt, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]*)>', m.group(1)):
            out[bytes.fromhex(a)] = u16(b)
    for m in re.finditer(r'beginbfrange(.*?)endbfrange', txt, re.S):
        body = m.group(1)
        for a, b, rest in re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(\[[^\]]*\]|<[0-9A-Fa-f]+>)', body):
            lo = int(a, 16)
            hi = int(b, 16)
            n = len(a) // 2
            if rest.startswith('['):
                items = re.findall(r'<([0-9A-Fa-f]*)>', rest)
                for k, h in enumerate(items):
                    if lo + k > hi:
                        break
                    out[(lo + k).to_bytes(n, 'big')] = u16(h)
            else:
                h = rest[1:-1]
                base = int(h, 16)
                L = len(h)
                for k in range(hi - lo + 1):
                    v = ('%0' + str(L) + 'X') % (base + k)
                    out[(lo + k).to_bytes(n, 'big')] = u16(v)
    if not lens and out:
        lens = set(len(k) for k in out)
    return out, sorted(lens) or [1]


# ------------------------------------------------------------------ font object
class PdfFont(object):
    """A font resource.  font = PdfFont(doc, ref_or_dict, name)"""

    def __init__(self, doc, ref, resname=''):
        self.doc = doc
        self.ref = ref if isinstance(ref, Ref) else None
        d = doc.resolve(ref)
        self.d = d
        self.resname = resname
        self.subtype = str(d.get('Subtype'))
        self.basefont = str(doc.resolve(d.get('BaseFont')) or '')
        self.family = self.basefont.split('+', 1)[-1]
        self.type0 = self.subtype == 'Type0'
        self.to_unicode = {}
        self.code_lens = [2] if self.type0 else [1]
        tu = d.get('ToUnicode')
        if tu is not None and isinstance(tu, Ref):
            try:
                data, left, _ = doc.stream_decoded(tu)
                self.to_unicode, lens = parse_cmap(data)
                if self.type0:
                    self.code_lens = lens or [2]
            except Exception:
                self.to_unicode = {}
        self.widths = {}
        self.missing_width = 0.0
        self.dw = 1000.0
        self.desc = None
        self.font_file = None
        self.font_file_kind = None
        self.differences = {}
        self.base_encoding = None
        if self.type0:
            df = doc.resolve(doc.resolve(d.get('DescendantFonts'))[0])
            self.desc = df
            self.dw = float(doc.resolve(df.get('DW', 1000)))
            W = doc.resolve(df.get('W')) or []
            W = [doc.resolve(x) for x in W]
            i = 0
            while i < len(W):
                c0 = int(W[i])
                nxt = W[i + 1] if i + 1 < len(W) else None
                if isinstance(nxt, list):
                    for k, w in enumerate(nxt):
                        self.widths[c0 + k] = float(doc.resolve(w))
                    i += 2
                else:
                    c1 = int(nxt)
                    w = float(W[i + 2])
                    for c in range(c0, c1 + 1):
                        self.widths[c] = w
                    i += 3
            fd = doc.resolve(df.get('FontDescriptor')) or {}
            self.cid_to_gid = df.get('CIDToGIDMap')
        else:
            fc = doc.resolve(d.get('FirstChar'))
            ws = doc.resolve(d.get('Widths'))
            if fc is not None and ws:
                for k, w in enumerate(ws):
                    self.widths[int(fc) + k] = float(doc.resolve(w))
            fd = doc.resolve(d.get('FontDescriptor')) or {}
            self.missing_width = float(doc.resolve(fd.get('MissingWidth', 0)) or 0)
            enc = doc.resolve(d.get('Encoding'))
            if isinstance(enc, dict):
                self.base_encoding = str(enc.get('BaseEncoding')) if enc.get('BaseEncoding') else None
                diffs = doc.resolve(enc.get('Differences')) or []
                code = 0
                for x in diffs:
                    x = doc.resolve(x)
                    if isinstance(x, (int, float)):
                        code = int(x)
                    else:
                        self.differences[code] = str(x)
                        code += 1
            elif enc is not None:
                self.base_encoding = str(enc)
        self.fd = fd
        for k in ('FontFile2', 'FontFile3', 'FontFile'):
            if fd.get(k) is not None:
                self.font_file = fd.get(k)
                self.font_file_kind = k
                break
        self._tt = None
        self._glyph_codes = None
        self._u2c = None

    # -------------------------------------------------------------- codes
    def split_codes(self, b):
        """bytes of a string operand -> list of code bytes."""
        b = bytes(b)
        if not self.type0:
            return [b[i:i + 1] for i in range(len(b))]
        n = self.code_lens[0] if len(self.code_lens) == 1 else 2
        out = []
        i = 0
        while i < len(b):
            # variable length codespace (rare): try longest that exists in ToUnicode
            if len(self.code_lens) > 1:
                for L in sorted(self.code_lens):
                    if b[i:i + L] in self.to_unicode:
                        n = L
                        break
            out.append(b[i:i + n])
            i += n
        return out

    def code_int(self, cb):
        return int.from_bytes(cb, 'big')

    def unicode_of(self, cb):
        if cb in self.to_unicode:
            return self.to_unicode[cb]
        c = self.code_int(cb)
        if self.type0:
            return None
        if c in self.differences:
            u = glyph_to_unicode(self.differences[c])
            if u is not None and not _pua(u):
                return u
        if self.base_encoding == 'MacRomanEncoding':
            return _macroman(c)
        if self.base_encoding in ('WinAnsiEncoding', 'StandardEncoding', 'PDFDocEncoding'):
            return _cp1252(c)
        name = self._builtin_glyph_name(c)
        if name:
            u = glyph_to_unicode(name)
            if u is not None and not _pua(u):
                return u
        return _cp1252(c)

    def width(self, cb):
        """glyph width in 1/1000 text space units."""
        c = self.code_int(cb)
        if self.type0:
            return self.widths.get(c, self.dw)
        return self.widths.get(c, self.missing_width)

    # -------------------------------------------------------------- embedded font program
    def _font_program(self):
        if self._tt is not None or self.font_file is None or TTFont is None:
            return self._tt
        try:
            data, left, _ = self.doc.stream_decoded(self.font_file)
            if self.font_file_kind == 'FontFile2':
                self._tt = ('tt', TTFont(io.BytesIO(data), lazy=True))
            elif self.font_file_kind == 'FontFile3':
                sub = str(self.doc.resolve(self.doc.get(self.font_file).get('Subtype')))
                if sub == 'OpenType':
                    self._tt = ('tt', TTFont(io.BytesIO(data), lazy=True))
                else:
                    cff = CFFFontSet()
                    cff.decompile(io.BytesIO(data), None)
                    self._tt = ('cff', cff[cff.fontNames[0]])
            else:
                self._tt = ('t1', None)
        except Exception:
            self._tt = ('err', None)
        return self._tt

    def _builtin_glyph_name(self, code):
        prog = self._font_program()
        if not prog or prog[0] not in ('tt', 'cff') or prog[1] is None:
            return None
        try:
            if prog[0] == 'tt':
                f = prog[1]
                cm = None
                for (pid, eid) in ((3, 0), (1, 0), (3, 1)):
                    t = f['cmap'].getcmap(pid, eid) if 'cmap' in f else None
                    if t is not None:
                        cm = (pid, eid, t.cmap)
                        break
                if cm is None:
                    return None
                pid, eid, m = cm
                g = m.get(0xF000 + code) if (pid, eid) == (3, 0) else m.get(code)
                if g is None and (pid, eid) == (3, 0):
                    g = m.get(code)
                return g if g and not g.startswith('glyph') else None
            cff = prog[1]
            enc = getattr(cff, 'Encoding', None)
            if isinstance(enc, list) and code < len(enc):
                n = enc[code]
                return None if n == '.notdef' else n
        except Exception:
            return None
        return None

    def has_glyph(self, cb):
        """True/False if decidable, None if unknown (no fontTools)."""
        c = self.code_int(cb)
        if self.type0:
            if self.to_unicode and cb not in self.to_unicode:
                # subset fonts usually map every used glyph
                pass
            prog = self._font_program()
            if prog and prog[0] == 'tt' and prog[1] is not None:
                try:
                    f = prog[1]
                    order = f.getGlyphOrder()
                    gid = c
                    if gid >= len(order):
                        return False
                    if 'glyf' in f:
                        g = f['glyf'][order[gid]]
                        return g.numberOfContours != 0 or self.unicode_of(cb) == ' '
                    return True
                except Exception:
                    return None
            return (c in self.widths) or None
        if c not in self.widths or self.widths.get(c, 0) == 0:
            if self.unicode_of(cb) != ' ':
                return False
        prog = self._font_program()
        if prog and prog[1] is not None:
            try:
                if prog[0] == 'tt':
                    f = prog[1]
                    name = None
                    for (pid, eid) in ((3, 0), (1, 0), (3, 1)):
                        t = f['cmap'].getcmap(pid, eid) if 'cmap' in f else None
                        if t is not None:
                            m = t.cmap
                            name = m.get(0xF000 + c) if (pid, eid) == (3, 0) else m.get(c)
                            if name is None and (pid, eid) == (3, 0):
                                name = m.get(c)
                            if (pid, eid) == (3, 1):
                                u = self.unicode_of(cb)
                                name = m.get(ord(u)) if u and len(u) == 1 else None
                            break
                    if name is None:
                        return False
                    if 'glyf' in f:
                        g = f['glyf'][name]
                        return g.numberOfContours != 0 or self.unicode_of(cb) == ' '
                    return True
                if prog[0] == 'cff':
                    cff = prog[1]
                    name = self.differences.get(c) or self._builtin_glyph_name(c)
                    if name is None:
                        return None
                    return name in cff.CharStrings
            except Exception:
                return None
        return True if c in self.widths and self.widths[c] > 0 else None

    def encode_char(self, u):
        """unicode char -> code bytes usable with this font (glyph must exist) or None."""
        if self._u2c is None:
            self._u2c = {}
            for cb, uu in self.to_unicode.items():
                if uu and uu not in self._u2c:
                    self._u2c[uu] = cb
            if not self.type0:
                for c in range(256):
                    cb = bytes([c])
                    uu = self.unicode_of(cb)
                    if uu and uu not in self._u2c and (c in self.widths and self.widths[c] > 0):
                        self._u2c[uu] = cb
        cb = self._u2c.get(u)
        if cb is None:
            return None
        ok = self.has_glyph(cb)
        if ok is False:
            return None
        return cb

    def encode(self, text):
        """unicode text -> bytes, or raise KeyError listing missing chars."""
        out = b''
        missing = []
        for ch in text:
            cb = self.encode_char(ch)
            if cb is None:
                missing.append(ch)
            else:
                out += cb
        if missing:
            raise KeyError('Font %s không có ký tự: %r' % (self.basefont, ''.join(sorted(set(missing)))))
        return out

    def text_width(self, text, size, tc=0.0, tw=0.0, th=1.0):
        w = 0.0
        for ch in text:
            cb = self.encode_char(ch)
            if cb is None:
                raise KeyError('Font %s không có ký tự %r' % (self.basefont, ch))
            w += (self.width(cb) / 1000.0 * size + tc + (tw if (not self.type0 and cb == b' ') else 0.0)) * th
        return w

    def __repr__(self):
        return 'PdfFont(%s %s %s)' % (self.resname, self.subtype, self.basefont)
