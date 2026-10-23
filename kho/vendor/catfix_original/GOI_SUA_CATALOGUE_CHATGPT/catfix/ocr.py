"""OCR helpers (tesseract via pytesseract or the tesseract command line).

All boxes returned in PDF page coordinates (points, origin bottom-left) unless stated.
"""
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image

from .pdfdoc import render, PdfDoc
from ._compat import tesseract_cmd

try:
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None

CACHE_DIR = os.environ.get('CATFIX_CACHE', os.path.join(tempfile.gettempdir(), 'catfix_cache'))
TESSERACT = tesseract_cmd()          # Windows: tự tìm C:\Program Files\Tesseract-OCR\tesseract.exe
if pytesseract is not None and TESSERACT:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT


def _tess():
    if not TESSERACT:
        raise RuntimeError('Không tìm thấy tesseract (OCR - chương trình đọc chữ trong ảnh). Cài Tesseract-OCR '
                           '(Windows: bản UB Mannheim, có tiếng Anh) hoặc đặt biến môi trường CATFIX_TESSERACT = đường dẫn tesseract.exe')
    return TESSERACT


def tesseract_available():
    if pytesseract is not None and TESSERACT:
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            pass
    return TESSERACT is not None


def _file_key(path):
    st = os.stat(path)
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        h.update(f.read(1 << 20))
    h.update(str(st.st_size).encode())
    return h.hexdigest()[:16]


def _tsv_from_image(img, psm=11, lang='eng', config=''):
    """run tesseract on a PIL image; return list of dict rows (TSV)."""
    if pytesseract is not None:
        try:
            txt = pytesseract.image_to_data(img, lang=lang, config='--psm %d %s' % (psm, config))
            return list(csv.DictReader(io.StringIO(txt), delimiter='\t', quoting=csv.QUOTE_NONE))
        except Exception:
            pass
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, 'i.png')
    img.save(p)
    cmd = [_tess(), p, os.path.join(tmp, 'o'), '-l', lang, '--psm', str(psm)] + (config.split() if config else []) + ['tsv']
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with open(os.path.join(tmp, 'o.tsv'), encoding='utf-8', errors='replace') as f:
        rows = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
    shutil.rmtree(tmp, ignore_errors=True)
    return rows


def _boxes_from_image(img, psm=7, lang='eng', config=''):
    """character boxes (tesseract 'makebox'); image coords with origin bottom-left."""
    if pytesseract is not None:
        try:
            txt = pytesseract.image_to_boxes(img, lang=lang, config='--psm %d %s' % (psm, config))
            out = []
            for line in txt.splitlines():
                parts = line.split(' ')
                if len(parts) >= 5:
                    out.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])))
            return out
        except Exception:
            pass
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, 'i.png')
    img.save(p)
    subprocess.run([_tess(), p, os.path.join(tmp, 'o'), '-l', lang, '--psm', str(psm)] + (config.split() if config else []) +
                   ['makebox'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    out = []
    with open(os.path.join(tmp, 'o.box'), encoding='utf-8', errors='replace') as f:
        for line in f:
            parts = line.rstrip('\n').split(' ')
            if len(parts) >= 5:
                out.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])))
    shutil.rmtree(tmp, ignore_errors=True)
    return out


def image_words(img, psm=11, lang='eng', config='', min_conf=-1):
    """OCR a numpy/PIL image -> list of dict(text, box=(l, t, r, b) pixel coords top-left origin, conf)."""
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)
    out = []
    for r in _tsv_from_image(img, psm, lang, config):
        tx = (r.get('text') or '').strip()
        if not tx:
            continue
        conf = float(r.get('conf', -1))
        if conf < min_conf:
            continue
        l, t, w, h = int(r['left']), int(r['top']), int(r['width']), int(r['height'])
        out.append(dict(text=tx, box=(l, t, l + w, t + h), conf=conf,
                        line=(int(r.get('block_num', 0)), int(r.get('par_num', 0)), int(r.get('line_num', 0)))))
    return out


def page_words(path, pi, rect=None, dpi=600, psm=11, lang='eng', config='', gray=True, cache=True, engine=None):
    """OCR words of a PDF page (or of rect=(x0,y0,x1,y1) page coords) -> list of
    dict(text, bbox=(x0,y0,x1,y1) page coords, conf, line).  Results are cached on disk."""
    key = None
    if cache:
        key = hashlib.sha1(json.dumps([_file_key(path), pi, rect, dpi, psm, lang, config, gray]).encode()).hexdigest()[:20]
        cp = os.path.join(CACHE_DIR, 'ocr_' + key + '.json')
        if os.path.exists(cp):
            try:
                with open(cp, encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass                      # bộ nhớ đệm hỏng -> đọc lại
    doc = PdfDoc(path)
    mb = doc.mediabox(pi)
    doc.close()
    a = render(path, pi, dpi=dpi, clip=rect, engine=engine)
    if gray:
        a = (a.astype(np.float32) @ np.array([0.299, 0.587, 0.114])).round().clip(0, 255).astype(np.uint8)
    s = 72.0 / dpi
    if rect:
        ox, oy_top = rect[0], rect[3]
    else:
        ox, oy_top = mb[0], mb[3]
    out = []
    for w in image_words(a, psm, lang, config):
        l, t, r, b = w['box']
        out.append(dict(text=w['text'], bbox=(ox + l * s, oy_top - b * s, ox + r * s, oy_top - t * s), conf=w['conf'], line=w['line']))
    if cache:
        os.makedirs(CACHE_DIR, exist_ok=True)
        tmpf = cp + '.%d.tmp' % os.getpid()
        with open(tmpf, 'w', encoding='utf-8') as f:
            json.dump(out, f)
        os.replace(tmpf, cp)
    return out


def region_text(path, pi, rect, dpi=600, psm=6, lang='eng', config='', engine=None):
    """plain OCR text of a page region (for read-back verification)."""
    a = render(path, pi, dpi=dpi, clip=rect, engine=engine)
    img = Image.fromarray(a).convert('L')
    if pytesseract is not None:
        try:
            return pytesseract.image_to_string(img, lang=lang, config='--psm %d %s' % (psm, config)).strip()
        except Exception:
            pass
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, 'i.png')
    img.save(p)
    subprocess.run([_tess(), p, os.path.join(tmp, 'o'), '-l', lang, '--psm', str(psm)] + (config.split() if config else []),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with open(os.path.join(tmp, 'o.txt'), encoding='utf-8', errors='replace') as f:
        t = f.read().strip()
    shutil.rmtree(tmp, ignore_errors=True)
    return t
