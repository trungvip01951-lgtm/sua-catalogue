"""Backend-independent PDF access (pikepdf preferred, PyMuPDF fallback).

Only what catfix needs: page content streams, resources, form/image XObjects,
fonts, adding image XObjects, saving, rendering.

Python view of PDF objects (both backends):
    dict (keys without '/'), list, int/float, cs.Name, cs.Str (bytes), cs.Ref((num, gen)), bool, None
"""
import io
import os
import re
import struct
import zlib

import numpy as np

from . import cs
from .cs import Name, Str, Ref

try:
    import pikepdf
except Exception:  # pragma: no cover
    pikepdf = None
try:
    import pymupdf as fitz
except Exception:  # pragma: no cover
    try:
        import fitz
    except Exception:
        fitz = None


def available_backends():
    out = []
    if pikepdf is not None:
        out.append('pikepdf')
    if fitz is not None:
        out.append('fitz')
    return out


# ------------------------------------------------------------------ stream filters
def _png_unpredict(data, columns, colors=1, bpc=8):
    bpp = max(1, colors * bpc // 8)
    rowlen = (columns * colors * bpc + 7) // 8
    out = bytearray()
    prev = bytearray(rowlen)
    i = 0
    n = len(data)
    while i < n:
        ft = data[i]
        row = bytearray(data[i + 1:i + 1 + rowlen])
        i += 1 + rowlen
        if len(row) < rowlen:
            row += bytes(rowlen - len(row))
        if ft == 1:
            for k in range(bpp, rowlen):
                row[k] = (row[k] + row[k - bpp]) & 255
        elif ft == 2:
            for k in range(rowlen):
                row[k] = (row[k] + prev[k]) & 255
        elif ft == 3:
            for k in range(rowlen):
                left = row[k - bpp] if k >= bpp else 0
                row[k] = (row[k] + ((left + prev[k]) >> 1)) & 255
        elif ft == 4:
            for k in range(rowlen):
                a = row[k - bpp] if k >= bpp else 0
                b = prev[k]
                c = prev[k - bpp] if k >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[k] = (row[k] + pr) & 255
        out += row
        prev = row
    return bytes(out)


def _lzw_decode(data, early=1):
    out = bytearray()
    table = [bytes([i]) for i in range(256)] + [None, None]
    bits = 9
    buf = 0
    nbits = 0
    prev = None
    for byte in data:
        buf = (buf << 8) | byte
        nbits += 8
        while nbits >= bits:
            nbits -= bits
            code = (buf >> nbits) & ((1 << bits) - 1)
            if code == 256:
                table = table[:258]
                bits = 9
                prev = None
                continue
            if code == 257:
                return bytes(out)
            if prev is None:
                entry = table[code]
            elif code < len(table) and table[code] is not None:
                entry = table[code]
                table.append(prev + entry[:1])
            else:
                entry = prev + prev[:1]
                table.append(entry)
            out += entry
            prev = entry
            if len(table) + early >= (1 << bits) and bits < 12:
                bits += 1
    return bytes(out)


def _a85_decode(data):
    import base64
    d = data.strip()
    if d.startswith(b'<~'):
        d = d[2:]
    if not d.endswith(b'~>'):
        d = d + b'~>'
    return base64.a85decode(b'<~' + d[:-2] + b'~>', adobe=True)


IMAGE_FILTERS = ('DCTDecode', 'JPXDecode', 'CCITTFaxDecode', 'JBIG2Decode', 'DCT', 'CCF')


def decode_stream(raw, filters, parms):
    """Apply non-image filters in order. Returns (data, remaining_filters, remaining_parms)."""
    if filters is None:
        filters = []
    if not isinstance(filters, list):
        filters = [filters]
    if not isinstance(parms, list):
        parms = [parms] * len(filters) if parms else [None] * len(filters)
    data = raw
    for k, (f, p) in enumerate(zip(filters, parms)):
        f = str(f)
        p = p or {}
        if f in ('FlateDecode', 'Fl'):
            try:
                data = zlib.decompress(data)
            except zlib.error:
                d = zlib.decompressobj()
                data = d.decompress(data)
        elif f in ('LZWDecode', 'LZW'):
            data = _lzw_decode(data, p.get('EarlyChange', 1))
        elif f in ('ASCIIHexDecode', 'AHx'):
            h = re.sub(rb'[^0-9A-Fa-f]', b'', data.split(b'>')[0])
            if len(h) % 2:
                h += b'0'
            data = bytes.fromhex(h.decode())
        elif f in ('ASCII85Decode', 'A85'):
            data = _a85_decode(data)
        elif f in ('RunLengthDecode', 'RL'):
            out = bytearray()
            i = 0
            while i < len(data):
                L = data[i]
                if L == 128:
                    break
                if L < 128:
                    out += data[i + 1:i + 2 + L]
                    i += L + 2
                else:
                    out += bytes([data[i + 1]]) * (257 - L)
                    i += 2
            data = bytes(out)
        elif f in IMAGE_FILTERS:
            return data, filters[k:], parms[k:]
        else:
            raise ValueError('unsupported filter ' + f)
        pred = p.get('Predictor', 1) if isinstance(p, dict) else 1
        if pred and pred >= 10:
            data = _png_unpredict(data, p.get('Columns', 1), p.get('Colors', 1), p.get('BitsPerComponent', 8))
        elif pred == 2:
            raise ValueError('TIFF predictor not supported')
    return data, [], []


# ------------------------------------------------------------------ document
class PdfDoc(object):
    """Open with PdfDoc(path).  backend='pikepdf' | 'fitz' | None (auto)."""

    def __init__(self, path, backend=None):
        self.path = path
        if backend is None:
            backend = os.environ.get('CATFIX_BACKEND') or None
        if backend is None:
            backend = 'pikepdf' if pikepdf is not None else ('fitz' if fitz is not None else None)
        if backend is None:
            raise RuntimeError('Cần pikepdf hoặc PyMuPDF (fitz) để mở PDF')
        self.backend = backend
        if backend == 'pikepdf':
            self.pdf = pikepdf.open(path)
            self._pages = list(self.pdf.pages)
        else:
            self.doc = fitz.open(path)
        self._new_names = {}

    # -------------------------------------------------------------- basics
    @property
    def n_pages(self):
        return len(self._pages) if self.backend == 'pikepdf' else self.doc.page_count

    def page_ref(self, pi):
        if self.backend == 'pikepdf':
            return Ref(self._pages[pi].obj.objgen)
        return Ref((self.doc[pi].xref, 0))

    def get(self, ref):
        """Python view of an object (dict / list / value). ref: Ref or backend object."""
        if self.backend == 'pikepdf':
            o = ref
            if isinstance(ref, Ref):
                o = self.pdf.get_object(tuple(ref))
            return _pk_to_py(o, top=True)
        xref = ref[0] if isinstance(ref, Ref) else int(ref)
        src = self.doc.xref_object(xref, compressed=True)
        return cs.parse_object(src)

    def resolve(self, v):
        """resolve a Ref (or return v)."""
        while isinstance(v, Ref):
            v = self.get(v)
        return v

    def page_dict(self, pi):
        return self.get(self.page_ref(pi))

    def inherited(self, pi, key):
        ref = self.page_ref(pi)
        seen = 0
        while ref is not None and seen < 50:
            d = self.get(ref)
            if key in d:
                return d[key], ref
            ref = d.get('Parent')
            seen += 1
        return None, None

    def mediabox(self, pi):
        v, _ = self.inherited(pi, 'MediaBox')
        v = self.resolve(v)
        return tuple(float(self.resolve(x)) for x in v)

    def cropbox(self, pi):
        v, _ = self.inherited(pi, 'CropBox')
        if v is None:
            return self.mediabox(pi)
        v = self.resolve(v)
        return tuple(float(self.resolve(x)) for x in v)

    def rotation(self, pi):
        v, _ = self.inherited(pi, 'Rotate')
        return int(self.resolve(v) or 0)

    # -------------------------------------------------------------- streams
    def stream_raw(self, ref):
        if self.backend == 'pikepdf':
            o = self.pdf.get_object(tuple(ref)) if isinstance(ref, Ref) else ref
            return bytes(o.read_raw_bytes())
        xref = ref[0] if isinstance(ref, Ref) else int(ref)
        return self.doc.xref_stream_raw(xref)

    def stream_decoded(self, ref, stop_at_image_filter=True):
        """decoded stream bytes (+ remaining image filters). returns (data, filters_left, dict)"""
        d = self.get(ref)
        raw = self.stream_raw(ref)
        filt = self.resolve(d.get('Filter'))
        parms = self.resolve(d.get('DecodeParms'))
        if isinstance(filt, list):
            filt = [self.resolve(x) for x in filt]
        if isinstance(parms, list):
            parms = [self.resolve(x) for x in parms]
        data, left, leftp = decode_stream(raw, filt, parms)
        return data, left, d

    def page_contents_refs(self, pi):
        d = self.page_dict(pi)
        c = d.get('Contents')
        if c is None:
            return []
        if isinstance(c, Ref):
            v = self.get(c)
            if isinstance(v, list):
                return [x for x in v]
            return [c]
        if isinstance(c, list):
            return list(c)
        return []

    def page_content(self, pi):
        parts = []
        for r in self.page_contents_refs(pi):
            data, left, _ = self.stream_decoded(r)
            parts.append(data)
        return b'\n'.join(parts)

    def set_page_content(self, pi, data):
        if self.backend == 'pikepdf':
            page = self._pages[pi]
            page.obj['/Contents'] = self.pdf.make_indirect(pikepdf.Stream(self.pdf, data))
            return
        page = self.doc[pi]
        xref = self.doc.get_new_xref()
        self.doc.update_object(xref, '<<>>')
        self.doc.update_stream(xref, data, compress=True)
        page.set_contents(xref)

    def set_stream(self, ref, data):
        """replace data of an existing stream object (e.g. a form XObject); keeps its dictionary."""
        if self.backend == 'pikepdf':
            o = self.pdf.get_object(tuple(ref))
            o.write(zlib.compress(data), filter=pikepdf.Name.FlateDecode)
            if '/DecodeParms' in o:
                del o['/DecodeParms']
            return
        xref = ref[0]
        self.doc.update_stream(xref, data, compress=True)

    # -------------------------------------------------------------- resources
    def page_resources(self, pi):
        v, owner = self.inherited(pi, 'Resources')
        return self.resolve(v) or {}

    def resource(self, res, category, name):
        """value (usually Ref) of /Resources/<category>/<name> given a resources python dict."""
        cat = self.resolve(res.get(category)) if res else None
        if not cat:
            return None
        return cat.get(str(name))

    def xobject_resources_of(self, ref):
        """resources dict of a form XObject"""
        d = self.get(ref)
        return self.resolve(d.get('Resources')) or {}

    def _fresh_name(self, res, category, prefix):
        cat = self.resolve(res.get(category)) if res else None
        used = set(cat.keys()) if cat else set()
        k = 1
        while '%s%d' % (prefix, k) in used:
            k += 1
        return '%s%d' % (prefix, k)

    def add_xobject_to_page(self, pi, xref_ref, prefix='CfxIm'):
        """register an XObject (Ref) in page resources under a fresh name; returns the name."""
        res = self.page_resources(pi)
        name = self._fresh_name(res, 'XObject', prefix)
        if self.backend == 'pikepdf':
            page = self._pages[pi]
            obj = page.obj
            if '/Resources' not in obj:  # inherited -> copy onto page
                v, owner = self.inherited(pi, 'Resources')
                src = self.pdf.get_object(tuple(v)) if isinstance(v, Ref) else None
                if src is None:
                    po = self.pdf.get_object(tuple(owner))
                    src = po.Resources
                obj['/Resources'] = pikepdf.Dictionary(src)
            R = obj.Resources
            if '/XObject' not in R:
                R['/XObject'] = pikepdf.Dictionary()
            R.XObject[pikepdf.Name('/' + name)] = self.pdf.get_object(tuple(xref_ref))
            return name
        doc = self.doc
        page = doc[pi]
        kind, val = doc.xref_get_key(page.xref, 'Resources')
        if kind == 'null':
            v, owner = self.inherited(pi, 'Resources')
            if isinstance(v, Ref):
                src = doc.xref_object(v[0], compressed=True)
            else:
                k2, src = doc.xref_get_key(owner[0], 'Resources')
            doc.xref_set_key(page.xref, 'Resources', src)
        kind, val = doc.xref_get_key(page.xref, 'Resources')
        target = page.xref
        key = 'Resources/XObject/' + name
        if kind == 'xref':
            target = int(val.split()[0])
            key = 'XObject/' + name
            k3, v3 = doc.xref_get_key(target, 'XObject')
            if k3 == 'xref':
                target = int(v3.split()[0])
                key = name
        else:
            k3, v3 = doc.xref_get_key(page.xref, 'Resources/XObject')
            if k3 == 'xref':
                target = int(v3.split()[0])
                key = name
        doc.xref_set_key(target, key, '%d 0 R' % xref_ref[0])
        return name

    def new_image_xobject(self, data, width, height, colorspace, bpc, filt, decode=None, smask=None,
                          decode_parms=None, extra=None):
        """create an image XObject stream; colorspace is a python value (Name / list with Refs / Ref).
        filt: 'DCTDecode' / 'FlateDecode' / None (data already encoded accordingly). returns Ref."""
        d = {'Type': Name('XObject'), 'Subtype': Name('Image'), 'Width': int(width), 'Height': int(height),
             'ColorSpace': colorspace, 'BitsPerComponent': int(bpc)}
        if filt:
            d['Filter'] = Name(filt)
        if decode is not None:
            d['Decode'] = decode
        if decode_parms is not None:
            d['DecodeParms'] = decode_parms
        if smask is not None:
            d['SMask'] = smask
        if extra:
            d.update(extra)
        if self.backend == 'pikepdf':
            st = pikepdf.Stream(self.pdf, data)
            for k, v in d.items():
                st[pikepdf.Name('/' + k)] = _py_to_pk(self.pdf, v)
            ind = self.pdf.make_indirect(st)
            return Ref(ind.objgen)
        doc = self.doc
        xref = doc.get_new_xref()
        doc.update_object(xref, cs.fmt_obj(dict((k, v) for k, v in d.items() if k != 'Filter')).decode('latin-1'))
        doc.update_stream(xref, data, compress=False)
        if filt:
            doc.xref_set_key(xref, 'Filter', '/' + filt)
        return Ref((xref, 0))

    # -------------------------------------------------------------- save
    def save(self, path):
        from ._compat import same_file
        if same_file(path, self.path):
            raise ValueError('Không ghi đè file đầu vào - hãy lưu ra file mới')
        d = os.path.dirname(os.path.abspath(path))
        os.makedirs(d, exist_ok=True)
        try:
            if self.backend == 'pikepdf':
                self.pdf.save(path, object_stream_mode=pikepdf.ObjectStreamMode.preserve,
                              compress_streams=True, recompress_flate=False)
            else:
                self.doc.save(path, garbage=1, deflate=True)
        except PermissionError as e:
            raise PermissionError('Không ghi được %s – file đang bị mở (Windows khoá file đang mở: trình xem PDF, hoặc '
                                  'Editor/PdfDoc khác chưa close()). Đóng file đó rồi lưu lại. (%s)' % (path, e))

    def close(self):
        try:
            if self.backend == 'pikepdf':
                self.pdf.close()
            else:
                self.doc.close()
        except Exception:
            pass


# ------------------------------------------------------------------ pikepdf <-> python
def _pk_to_py(o, top=False):
    if not top and getattr(o, 'is_indirect', False):
        try:
            return Ref(o.objgen)
        except Exception:
            pass
    if isinstance(o, pikepdf.Dictionary) or isinstance(o, pikepdf.Stream):
        out = {}
        for k in o.keys():
            out[str(k)[1:]] = _pk_to_py(o.get(k))
        return out
    if isinstance(o, pikepdf.Array):
        return [_pk_to_py(x) for x in o]
    if isinstance(o, pikepdf.Name):
        return Name(str(o)[1:])
    if isinstance(o, pikepdf.String):
        return Str(bytes(o))
    if isinstance(o, bool):
        return o
    if o is None:
        return None
    try:
        tc = o._type_code
    except Exception:
        tc = None
    if isinstance(o, int):
        return int(o)
    try:
        f = float(o)
        return int(f) if f == int(f) and '.' not in str(o) else f
    except Exception:
        pass
    return o


def _py_to_pk(pdf, v):
    if isinstance(v, Ref):
        return pdf.get_object(tuple(v))
    if isinstance(v, Name):
        return pikepdf.Name('/' + str(v))
    if isinstance(v, Str):
        return pikepdf.String(bytes(v))
    if isinstance(v, (bytes, bytearray)):
        return pikepdf.String(bytes(v))
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, list):
        return pikepdf.Array([_py_to_pk(pdf, x) for x in v])
    if isinstance(v, dict):
        d = pikepdf.Dictionary()
        for k, x in v.items():
            d[pikepdf.Name('/' + k)] = _py_to_pk(pdf, x)
        return d
    if v is None:
        return None
    raise TypeError(repr(v))


# ------------------------------------------------------------------ synthetic pages
def make_single_page_pdf(path_out, mediabox, content):
    """write a 1-page PDF with the given mediabox and raw content stream (no resources needed
    for pure vector paths).  Used to OCR outlined glyphs drawn black on white."""
    if pikepdf is not None:
        pdf = pikepdf.new()
        page = pikepdf.Dictionary(Type=pikepdf.Name.Page, MediaBox=pikepdf.Array([float(v) for v in mediabox]),
                                  Resources=pikepdf.Dictionary())
        try:
            page.Contents = pdf.make_stream(content)
        except AttributeError:
            page.Contents = pdf.make_indirect(pikepdf.Stream(pdf, content))
        try:
            pdf.pages.append(pikepdf.Page(page))
        except Exception:
            pdf.pages.append(page)
        pdf.save(path_out)
        return path_out
    doc = fitz.open()
    x0, y0, x1, y1 = mediabox
    p = doc.new_page(width=x1 - x0, height=y1 - y0)
    xref = doc.get_new_xref()
    doc.update_object(xref, '<<>>')
    doc.update_stream(xref, content, compress=True)
    p.set_contents(xref)
    doc.xref_set_key(p.xref, 'MediaBox', '[%s]' % ' '.join(repr(float(v)) for v in mediabox))
    doc.save(path_out)
    return path_out


# ------------------------------------------------------------------ rendering
def render(path, pi, dpi=150, clip=None, engine=None):
    """Render page pi (0-based) to an RGB uint8 numpy array.
    clip = (x0, y0, x1, y1) in PDF page coordinates (origin bottom-left, as in content streams).
    engine: 'fitz' | 'pdftoppm' | None(auto, fitz first).  Use the SAME engine for before/after."""
    if engine is None:
        engine = os.environ.get('CATFIX_RENDER') or ('fitz' if fitz is not None else 'pdftoppm')
    if engine == 'fitz':
        doc = fitz.open(path)
        page = doc[pi]
        z = dpi / 72.0
        if clip:
            x0, y0, x1, y1 = clip
            # PDF user space (bottom-left origin) -> MuPDF page space (top-left origin)
            try:
                T = page.transformation_matrix
                p0 = fitz.Point(x0, y0) * T
                p1 = fitz.Point(x1, y1) * T
                r = fitz.Rect(min(p0.x, p1.x), min(p0.y, p1.y), max(p0.x, p1.x), max(p0.y, p1.y))
            except Exception:
                mbox = _mediabox_pdf(doc, pi)
                r = fitz.Rect(x0 - mbox[0], mbox[3] - y1, x1 - mbox[0], mbox[3] - y0)
            pix = page.get_pixmap(matrix=fitz.Matrix(z, z), clip=r, alpha=False, colorspace=fitz.csRGB)
        else:
            pix = page.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False, colorspace=fitz.csRGB)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()
        doc.close()
        return a
    import subprocess
    import tempfile
    from PIL import Image
    tmp = tempfile.mkdtemp()
    out = os.path.join(tmp, 'r')
    cmd = ['pdftoppm', '-f', str(pi + 1), '-l', str(pi + 1), '-r', str(dpi), '-png', '-singlefile']
    if clip:
        mbox = _mediabox_any(path, pi)
        x0, y0, x1, y1 = clip
        s = dpi / 72.0
        X = int(round((x0 - mbox[0]) * s))
        Y = int(round((mbox[3] - y1) * s))
        W = int(round((x1 - x0) * s))
        Hh = int(round((y1 - y0) * s))
        cmd += ['-x', str(X), '-y', str(Y), '-W', str(W), '-H', str(Hh)]
    cmd += [path, out]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    a = np.asarray(Image.open(out + '.png').convert('RGB')).copy()
    try:
        os.remove(out + '.png')
        os.rmdir(tmp)
    except Exception:
        pass
    return a


def _mediabox_pdf(doc, pi):
    try:
        k, v = doc.xref_get_key(doc[pi].xref, 'MediaBox')
        if k == 'array':
            return [float(x) for x in v.strip('[]').split()]
    except Exception:
        pass
    r = doc[pi].mediabox
    return [r.x0, r.y0, r.x1, r.y1]


def _mediabox_any(path, pi):
    d = PdfDoc(path)
    try:
        return d.mediabox(pi)
    finally:
        d.close()


def render_engines():
    out = []
    if fitz is not None:
        out.append('fitz')
    import shutil
    if shutil.which('pdftoppm'):
        out.append('pdftoppm')
    return out
