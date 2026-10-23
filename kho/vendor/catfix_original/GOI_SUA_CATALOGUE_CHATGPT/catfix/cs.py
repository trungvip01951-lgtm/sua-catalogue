"""Lossless PDF content-stream tokenizer / serializer (pure Python, no dependency).

Every instruction keeps its exact original bytes (`raw`), so an edited stream
re-emits untouched instructions byte-for-byte.  Only new / modified
instructions are serialized from their operands.

    instrs = parse(data)                 # list[Instr]
    data2  = serialize(instrs)           # == data when nothing changed
    Instr([1, 0, 0, 1, 10, 20], 'cm')    # new instruction (raw=None)
"""
import re

__all__ = ['Name', 'Str', 'Num', 'Instr', 'parse', 'serialize', 'fmt_num', 'fmt_obj',
           'parse_object', 'Ref']

WS = b' \t\r\n\f\x00'
DELIMS = b'()<>[]{}/%'


class Name(str):
    """PDF name without the leading slash."""
    def __repr__(self):
        return '/' + str(self)


class Str(bytes):
    """PDF string (raw decoded bytes). `.hex` tells how it was written."""
    hex = False

    def __new__(cls, value=b'', hex=False):
        o = bytes.__new__(cls, value)
        o.hex = hex
        return o


class Num(float):
    """float that is written with `nd` decimals (default 10) - for precise matrices."""
    def __new__(cls, value, nd=10):
        o = float.__new__(cls, value)
        o.nd = nd
        return o


class Ref(tuple):
    """Indirect reference (num, gen) - only appears in object syntax, not in content streams."""
    def __repr__(self):
        return '%d %d R' % self


class Instr(object):
    __slots__ = ('operands', 'op', 'raw', 'pos')

    def __init__(self, operands, op, raw=None, pos=None):
        self.operands = operands
        self.op = op
        self.raw = raw
        self.pos = pos

    def __repr__(self):
        return 'Instr(%r, %r)' % (self.operands, self.op)

    def copy(self):
        return Instr(list(self.operands), self.op, None)


_TOK = re.compile(rb'''
 (?P<ws>[ \t\r\n\f\x00]+)
|(?P<comment>%[^\r\n]*)
|(?P<name>/[^ \t\r\n\f\x00()<>\[\]{}/%]*)
|(?P<num>[+-]?(?:\d+\.?\d*|\.\d+))(?=[ \t\r\n\f\x00()<>\[\]{}/%]|\Z)
|(?P<dopen><<)
|(?P<dclose>>>)
|(?P<hex><[0-9A-Fa-f \t\r\n\f\x00]*>)
|(?P<lit>\()
|(?P<aopen>\[)
|(?P<aclose>\])
|(?P<bopen>\{)
|(?P<bclose>\})
|(?P<kw>[^ \t\r\n\f\x00()<>\[\]{}/%]+)
''', re.X)

_ESC = {ord('n'): b'\n', ord('r'): b'\r', ord('t'): b'\t', ord('b'): b'\b',
        ord('f'): b'\f', ord('('): b'(', ord(')'): b')', ord('\\'): b'\\'}


def _lit_string(data, i):
    """data[i] == '(' ; return (Str, end_index_after_closing_paren)."""
    n = len(data)
    depth = 1
    out = bytearray()
    i += 1
    while i < n:
        c = data[i]
        if c == 0x5C:  # backslash
            i += 1
            if i >= n:
                break
            c2 = data[i]
            if c2 in _ESC:
                out += _ESC[c2]
                i += 1
            elif 0x30 <= c2 <= 0x37:
                j = i
                while j < n and j < i + 3 and 0x30 <= data[j] <= 0x37:
                    j += 1
                out.append(int(data[i:j], 8) & 0xFF)
                i = j
            elif c2 == 0x0D:  # line continuation
                i += 1
                if i < n and data[i] == 0x0A:
                    i += 1
            elif c2 == 0x0A:
                i += 1
            else:
                out.append(c2)
                i += 1
            continue
        if c == 0x28:
            depth += 1
        elif c == 0x29:
            depth -= 1
            if depth == 0:
                return Str(bytes(out)), i + 1
        out.append(c)
        i += 1
    raise ValueError('unterminated string at %d' % i)


def _name(tok):
    s = tok[1:]
    if b'#' in s:
        s = re.sub(rb'#([0-9A-Fa-f]{2})', lambda m: bytes([int(m.group(1), 16)]), s)
    return Name(s.decode('latin-1'))


def _num(tok):
    if b'.' in tok:
        return float(tok)
    return int(tok)


def _hexstr(tok):
    h = re.sub(rb'[^0-9A-Fa-f]', b'', tok[1:-1])
    if len(h) % 2:
        h += b'0'
    return Str(bytes.fromhex(h.decode('ascii')), hex=True)


def _find_ei(data, start):
    """end of inline image data: position right after 'EI'."""
    n = len(data)
    pos = start
    while True:
        k = data.find(b'EI', pos)
        if k < 0:
            raise ValueError('inline image without EI')
        before_ok = k > 0 and data[k - 1] in WS
        after_ok = k + 2 >= n or data[k + 2] in WS or data[k + 2] in DELIMS
        if before_ok and after_ok:
            # sanity: following bytes should look like text operators
            tail = data[k + 2:k + 40]
            if all(32 <= b < 127 or b in WS for b in tail):
                return k + 2
        pos = k + 2


def parse(data, keep_raw=True):
    """Parse content-stream bytes into a list of Instr (lossless)."""
    instrs = []
    stack = []          # nested containers: list or ('dict', list)
    operands = []
    start = 0           # raw start of the current instruction
    i = 0
    n = len(data)
    match = _TOK.match
    while i < n:
        m = match(data, i)
        if m is None:
            raise ValueError('cannot tokenize at %d: %r' % (i, data[i:i + 20]))
        kind = m.lastgroup
        end = m.end()
        if kind == 'ws' or kind == 'comment':
            i = end
            continue
        tok = m.group(kind)
        if kind == 'num':
            val = _num(tok)
        elif kind == 'name':
            val = _name(tok)
        elif kind == 'lit':
            val, end = _lit_string(data, i)
        elif kind == 'hex':
            val = _hexstr(tok)
        elif kind == 'aopen':
            stack.append([])
            i = end
            continue
        elif kind == 'dopen':
            stack.append(('dict', []))
            i = end
            continue
        elif kind == 'aclose':
            val = stack.pop()
            if isinstance(val, tuple):
                raise ValueError('bad nesting at %d' % i)
            val = _collapse_refs(val)
        elif kind == 'dclose':
            t = stack.pop()
            items = _collapse_refs(t[1])
            val = {}
            for k in range(0, len(items) - 1, 2):
                val[str(items[k])] = items[k + 1]
        elif kind in ('bopen', 'bclose'):  # PostScript calculator braces - keep as keyword
            val = Name(tok.decode('latin-1'))
        else:  # keyword
            if tok == b'true':
                val = True
            elif tok == b'false':
                val = False
            elif tok == b'null':
                val = None
            else:
                if stack:  # keyword inside array/dict (should not happen) -> keep as name
                    val = Name(tok.decode('latin-1'))
                else:
                    op = tok.decode('latin-1')
                    if op == 'BI':
                        idk = data.find(b'ID', end)
                        # find 'ID' as a token
                        while idk >= 0 and not ((data[idk - 1] in WS) and (idk + 2 >= n or data[idk + 2] in WS)):
                            idk = data.find(b'ID', idk + 2)
                        if idk < 0:
                            raise ValueError('BI without ID')
                        dict_part = data[end:idk]
                        d0 = parse(dict_part + b' x', keep_raw=False)
                        params = d0[0].operands if d0 else []
                        dstart = idk + 3
                        e = _find_ei(data, dstart)
                        ins = Instr([params, data[dstart:e - 2]], 'BI', data[start:e] if keep_raw else None, start)
                        instrs.append(ins)
                        operands = []
                        start = e
                        i = e
                        continue
                    ins = Instr(operands, op, data[start:end] if keep_raw else None, start)
                    instrs.append(ins)
                    operands = []
                    start = end
                    i = end
                    continue
        if stack:
            top = stack[-1]
            (top[1] if isinstance(top, tuple) else top).append(val)
        else:
            operands.append(val)
        i = end
    if operands or (keep_raw and start < n):
        # trailing whitespace / comments (or malformed operands without operator): keep as tail
        instrs.append(Instr(operands, '', data[start:] if keep_raw else None, start))
    return instrs


def fmt_num(v, nd=4):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if v != v or v in (float('inf'), float('-inf')):
        raise ValueError('bad number %r' % v)
    r = round(float(v), nd)
    if r == int(r) and abs(r) < 1e15:
        return str(int(r))
    s = ('%.' + str(nd) + 'f') % r
    s = s.rstrip('0').rstrip('.')
    if s in ('-0', ''):
        s = '0'
    return s


def _esc_name(s):
    out = []
    for ch in s.encode('latin-1', 'replace'):
        if ch < 33 or ch > 126 or ch in b'()<>[]{}/%#':
            out.append('#%02X' % ch)
        else:
            out.append(chr(ch))
    return ''.join(out)


def _esc_lit(b):
    out = bytearray(b'(')
    for ch in b:
        if ch in (0x28, 0x29, 0x5C):
            out += b'\\' + bytes([ch])
        elif ch == 0x0D:
            out += b'\\r'
        elif ch == 0x0A:
            out += b'\\n'
        elif ch < 32 or ch > 126:
            out += ('\\%03o' % ch).encode()
        else:
            out.append(ch)
    out += b')'
    return bytes(out)


def fmt_obj(v, nd=4):
    if isinstance(v, Name):
        return ('/' + _esc_name(v)).encode('latin-1')
    if isinstance(v, Str):
        if v.hex:
            return _fmt_hex(v)
        return _esc_lit(v)
    if isinstance(v, (bytes, bytearray)):
        return _esc_lit(bytes(v))
    if isinstance(v, Ref):
        return ('%d %d R' % v).encode()
    if isinstance(v, bool) or v is None:
        return b'null' if v is None else (b'true' if v else b'false')
    if isinstance(v, Num):
        return fmt_num(float(v), v.nd).encode()
    if isinstance(v, (int, float)):
        return fmt_num(v, nd).encode()
    if isinstance(v, (list, tuple)):
        return b'[' + b' '.join(fmt_obj(x, nd) for x in v) + b']'
    if isinstance(v, dict):
        return b'<<' + b' '.join(fmt_obj(Name(k), nd) + b' ' + fmt_obj(x, nd) for k, x in v.items()) + b'>>'
    raise TypeError('cannot format %r' % (v,))


def _fmt_hex(v):
    return b'<' + bytes.hex(bytes(v)).upper().encode() + b'>'


def fmt_instr(ins, nd=4):
    if ins.op == '':
        return b''
    if ins.op == '__multi__':   # compound: several instructions occupying one slot
        return b'\n'.join((s.raw.strip() if s.raw is not None else fmt_instr(s, nd)) for s in ins.operands)
    if ins.op == 'BI':
        params, imgdata = ins.operands
        d = b' '.join(fmt_obj(x, nd) for x in params) if isinstance(params, list) else b''
        return b'BI ' + d + b' ID ' + imgdata + b' EI'
    parts = []
    for v in ins.operands:
        if isinstance(v, Str) and v.hex:
            parts.append(_fmt_hex(v))
        else:
            parts.append(fmt_obj(v, nd))
    parts.append(ins.op.encode('latin-1'))
    return b' '.join(parts)


def _regular(b):
    return b not in WS and b not in DELIMS


def serialize(instrs, nd=4):
    """Join instructions; untouched ones are re-emitted from their raw bytes."""
    out = bytearray()
    for ins in instrs:
        chunk = ins.raw if ins.raw is not None else b'\n' + fmt_instr(ins, nd)
        if out and chunk and _regular(out[-1]) and _regular(chunk[0]):
            out += b' '
        out += chunk
    return bytes(out)


# ---------------------------------------------------------------- object syntax
def _collapse_refs(items):
    """turn  int int R  sequences (R parsed as Name inside containers) into Ref."""
    if len(items) < 3:
        return items
    out = []
    i = 0
    while i < len(items):
        v = items[i]
        if (i + 2 < len(items) and type(v) is int and type(items[i + 1]) is int
                and isinstance(items[i + 2], Name) and items[i + 2] == 'R'):
            out.append(Ref((v, items[i + 1])))
            i += 3
            continue
        out.append(v)
        i += 1
    return out


def parse_object(data):
    """Parse one PDF object written in PDF syntax (dict, array, number, 'n g R' ...).
    Used by the PyMuPDF backend to read dictionaries."""
    if isinstance(data, str):
        data = data.encode('latin-1')
    toks = parse(data + b' __END__', keep_raw=False)
    if not toks:
        return None
    t0 = toks[0]
    if t0.op == 'R' and len(t0.operands) == 2:
        return Ref((t0.operands[0], t0.operands[1]))
    vals = _collapse_refs(t0.operands)
    return vals[0] if vals else None
