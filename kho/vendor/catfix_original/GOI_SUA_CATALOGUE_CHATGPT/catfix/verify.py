"""Acceptance checks: what changed, where, does it read right, is the file healthy.

    regs = diff_regions('before.pdf', 'after.pdf')                  # {page_no: [rect, ...]} (1-based pages)
    bad  = unexpected(regs, allowed={9: [(505, 505, 540, 520)]})     # changes outside the allowed boxes
    structure_check('before.pdf', 'after.pdf')                      # page count/sizes, untouched pages
    compare_sheet('before.pdf', 'after.pdf', [(8, rect, 'label'), ...], 'compare.png')
    ocr_check('after.pdf', 8, rect, '815')
"""
import hashlib
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .pdfdoc import render, PdfDoc

try:
    from scipy import ndimage
except Exception:  # pragma: no cover
    ndimage = None


def _font(size=18):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf',
              '/Library/Fonts/Arial.ttf', 'C:/Windows/Fonts/arial.ttf'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def diff_regions(before, after, pages=None, dpi=100, merge=6, engine=None, thr=0, min_size=0.0):
    """{page_no (1-based): [(x0, y0, x1, y1), ...]} of visibly changed areas (page coordinates).
    thr: ignore colour differences <= thr (0-255).  min_size: drop regions smaller than this (pt) in both directions
    (use thr=48, min_size=2 for re-encoded scanned pages: JPEG re-encoding moves a few isolated pixels)."""
    db, da = PdfDoc(before), PdfDoc(after)
    n = db.n_pages
    if da.n_pages != n:
        raise AssertionError('Số trang khác nhau: %d -> %d' % (n, da.n_pages))
    out = {}
    pages = range(n) if pages is None else pages
    for pi in pages:
        A = render(before, pi, dpi, engine=engine).astype(np.int16)
        B = render(after, pi, dpi, engine=engine).astype(np.int16)
        if A.shape != B.shape:
            out[pi + 1] = [('SIZE', A.shape, B.shape)]
            continue
        d = np.abs(A - B).max(axis=2) > thr
        if not d.any():
            continue
        mb = db.mediabox(pi)
        H = A.shape[0]
        s = 72.0 / dpi
        if ndimage is not None:
            lab, k = ndimage.label(ndimage.binary_dilation(d, iterations=merge))
            R = []
            for idx, sl in enumerate(ndimage.find_objects(lab), 1):
                ys, xs = sl
                sub = d[sl] & (lab[sl] == idx)          # tight box of the really changed pixels
                yy, xx = np.where(sub)
                y0, y1 = ys.start + yy.min(), ys.start + yy.max() + 1
                x0, x1 = xs.start + xx.min(), xs.start + xx.max() + 1
                R.append((round(mb[0] + x0 * s, 1), round(mb[3] - y1 * s, 1), round(mb[0] + x1 * s, 1), round(mb[3] - y0 * s, 1)))
        else:
            ys, xs = np.where(d)
            R = [(round(mb[0] + xs.min() * s, 1), round(mb[3] - (ys.max() + 1) * s, 1), round(mb[0] + (xs.max() + 1) * s, 1), round(mb[3] - ys.min() * s, 1))]
        if min_size:
            R = [r for r in R if (r[2] - r[0]) >= min_size or (r[3] - r[1]) >= min_size]
        if R:
            out[pi + 1] = sorted(R, key=lambda r: (-r[3], r[0]))
    db.close()
    da.close()
    return out


def _inside(r, a, pad):
    return r[0] >= a[0] - pad and r[1] >= a[1] - pad and r[2] <= a[2] + pad and r[3] <= a[3] + pad


def unexpected(regions, allowed, pad=4.0):
    """changed areas NOT inside any allowed rect.  allowed: {page_no: [rect, ...]} (1-based pages)."""
    bad = {}
    for pg, rects in regions.items():
        ok = allowed.get(pg, [])
        for r in rects:
            if r and r[0] == 'SIZE':
                bad.setdefault(pg, []).append(r)
                continue
            if not any(_inside(r, a, pad) for a in ok):
                bad.setdefault(pg, []).append(r)
    return bad


def outside_pixels(before, after, allowed, pages=None, dpi=100, thr=0, min_size=0.0, pad=2.0, merge=4, engine=None):
    """pixel-exact check: changed pixels that are NOT inside the union of allowed rects.
    allowed: {page_no: [rect, ...]}.  returns {page_no: [rect, ...]} of offending areas (empty = OK)."""
    db = PdfDoc(before)
    n = db.n_pages
    out = {}
    for pi in (range(n) if pages is None else pages):
        A = render(before, pi, dpi, engine=engine).astype(np.int16)
        B = render(after, pi, dpi, engine=engine).astype(np.int16)
        if A.shape != B.shape:
            out[pi + 1] = [('SIZE', A.shape, B.shape)]
            continue
        d = np.abs(A - B).max(axis=2) > thr
        if not d.any():
            continue
        mb = db.mediabox(pi)
        s = dpi / 72.0
        H, W = d.shape
        okm = np.zeros_like(d)
        for r in allowed.get(pi + 1, []):
            x0 = int(max(0, np.floor((r[0] - pad - mb[0]) * s)))
            x1 = int(min(W, np.ceil((r[2] + pad - mb[0]) * s)))
            y0 = int(max(0, np.floor((mb[3] - r[3] - pad) * s)))
            y1 = int(min(H, np.ceil((mb[3] - r[1] + pad) * s)))
            okm[y0:y1, x0:x1] = True
        bad = d & ~okm
        if not bad.any():
            continue
        R = []
        if ndimage is not None:
            lab, k = ndimage.label(ndimage.binary_dilation(bad, iterations=merge))
            for idx, sl in enumerate(ndimage.find_objects(lab), 1):
                sub = bad[sl] & (lab[sl] == idx)
                yy, xx = np.where(sub)
                y0, y1 = sl[0].start + yy.min(), sl[0].start + yy.max() + 1
                x0, x1 = sl[1].start + xx.min(), sl[1].start + xx.max() + 1
                R.append((round(mb[0] + x0 / s, 1), round(mb[3] - y1 / s, 1), round(mb[0] + x1 / s, 1), round(mb[3] - y0 / s, 1)))
        else:
            ys, xs = np.where(bad)
            R.append((round(mb[0] + xs.min() / s, 1), round(mb[3] - (ys.max() + 1) / s, 1), round(mb[0] + (xs.max() + 1) / s, 1), round(mb[3] - ys.min() / s, 1)))
        if min_size:
            R = [r for r in R if (r[2] - r[0]) >= min_size or (r[3] - r[1]) >= min_size]
        if R:
            out[pi + 1] = R
    db.close()
    return out


def missing(regions, expected, pad=4.0):
    """expected edit areas where NOTHING changed (edit forgotten / failed)."""
    miss = {}
    for pg, rects in expected.items():
        got = regions.get(pg, [])
        for a in rects:
            if not any(not (r[2] < a[0] - pad or r[0] > a[2] + pad or r[3] < a[1] - pad or r[1] > a[3] + pad) for r in got if r and r[0] != 'SIZE'):
                miss.setdefault(pg, []).append(a)
    return miss


def page_hashes(path):
    d = PdfDoc(path)
    out = [hashlib.sha1(d.page_content(pi)).hexdigest()[:16] for pi in range(d.n_pages)]
    d.close()
    return out


def structure_check(before, after):
    """basic health: opens with every available backend, same page count & sizes; lists pages whose
    content stream changed.  returns dict(ok, problems, changed_pages, size_before, size_after)."""
    from .pdfdoc import available_backends
    problems = []
    for be in available_backends():
        try:
            d = PdfDoc(after, be)
            _ = [d.page_content(pi) for pi in range(d.n_pages)]
            d.close()
        except Exception as e:
            problems.append('Không mở được bằng %s: %s' % (be, e))
    db, da = PdfDoc(before), PdfDoc(after)
    if db.n_pages != da.n_pages:
        problems.append('Số trang %d -> %d' % (db.n_pages, da.n_pages))
    for pi in range(min(db.n_pages, da.n_pages)):
        if [round(v, 2) for v in db.mediabox(pi)] != [round(v, 2) for v in da.mediabox(pi)]:
            problems.append('Trang %d đổi khổ giấy' % (pi + 1))
    hb, ha = page_hashes(before), page_hashes(after)
    changed = [i + 1 for i, (a, b) in enumerate(zip(hb, ha)) if a != b]
    try:
        import shutil, subprocess
        if shutil.which('qpdf'):
            r = subprocess.run(['qpdf', '--check', after], capture_output=True, encoding='utf-8', errors='replace')
            if r.returncode not in (0, 3):
                problems.append('qpdf --check báo lỗi: ' + (r.stdout + r.stderr)[-300:])
    except Exception:
        pass
    sb, sa = os.path.getsize(before), os.path.getsize(after)
    if sa > 3 * sb + 2000000:
        problems.append('File phình to bất thường: %d -> %d bytes' % (sb, sa))
    db.close()
    da.close()
    return dict(ok=not problems, problems=problems, changed_pages=changed, size_before=sb, size_after=sa)


def crop(path, pi, rect, dpi=200, engine=None):
    return Image.fromarray(render(path, pi, dpi, clip=rect, engine=engine))


def compare_sheet(before, after, items, out_png, dpi=200, pad=(14, 6), engine=None, max_width=2400):
    """side-by-side crops: items = [(page_index0, rect, label), ...] -> PNG (before | after)."""
    font = _font(20)
    tiles = []
    for pi, rect, label in items:
        r = (rect[0] - pad[0], rect[1] - pad[1], rect[2] + pad[0], rect[3] + pad[1])
        a = crop(before, pi, r, dpi, engine)
        b = crop(after, pi, r, dpi, engine)
        w, h = a.size
        t = Image.new('RGB', (w * 2 + 40, h + 34), 'white')
        d = ImageDraw.Draw(t)
        d.text((4, 2), 'Trang %d: %s' % (pi + 1, label), fill=(0, 0, 0), font=font)
        t.paste(a, (0, 32))
        t.paste(b, (w + 40, 32))
        d.text((w + 8, 32 + h // 2 - 12), '->', fill=(200, 0, 0), font=font)
        tiles.append(t)
    if not tiles:
        return None
    W = min(max(t.width for t in tiles), max_width)
    scaled = []
    for t in tiles:
        if t.width > W:
            t = t.resize((W, int(t.height * W / t.width)))
        scaled.append(t)
    Ht = sum(t.height + 10 for t in scaled)
    C = Image.new('RGB', (W, Ht), 'white')
    y = 0
    for t in scaled:
        C.paste(t, (0, y))
        y += t.height + 10
    C.save(out_png)
    return out_png


def page_overview(before, after, pi, out_png, dpi=60, regions=None, engine=None):
    """whole page before | after, changed areas boxed in red."""
    a = Image.fromarray(render(before, pi, dpi, engine=engine))
    b = Image.fromarray(render(after, pi, dpi, engine=engine))
    if regions is None:
        regions = diff_regions(before, after, pages=[pi], dpi=dpi, engine=engine).get(pi + 1, [])
    d = PdfDoc(before)
    mb = d.mediabox(pi)
    d.close()
    s = dpi / 72.0
    dr = ImageDraw.Draw(b)
    for r in regions:
        if r and r[0] == 'SIZE':
            continue
        dr.rectangle([(r[0] - mb[0]) * s - 2, (mb[3] - r[3]) * s - 2, (r[2] - mb[0]) * s + 2, (mb[3] - r[1]) * s + 2], outline=(255, 0, 0), width=2)
    C = Image.new('RGB', (a.width + b.width + 20, max(a.height, b.height)), 'white')
    C.paste(a, (0, 0))
    C.paste(b, (a.width + 20, 0))
    C.save(out_png)
    return out_png


def _norm(s):
    return ''.join(ch for ch in s.lower() if ch.isalnum() or ch in '.,-/()%')


def _remove_rules(g):
    """whiten long horizontal / vertical dark runs (table lines) in a gray image."""
    a = g.copy()
    dark = a < 160
    H, W = a.shape
    for y in range(H):
        if dark[y].sum() > 0.7 * W:
            a[max(0, y - 1):y + 2, :] = 255
    for x in range(W):
        if dark[:, x].sum() > 0.7 * H:
            a[:, max(0, x - 1):x + 2] = 255
    return a


def ocr_check(path, pi, rect, expected, dpi=None, psm=7):
    """OCR the area and compare with expected text (ignoring spaces/case).  -> dict(ok, read).
    Tries several resolutions / page-segmentation modes, with and without table lines."""
    from .ocr import image_words, pytesseract
    from .pdfdoc import render as _render
    import subprocess, tempfile, shutil
    reads = []
    want = _norm(expected)
    for pad in (2, 5):
        r = (rect[0] - pad, rect[1] - pad, rect[2] + pad, rect[3] + pad)
        for d in ([dpi] if dpi else [300, 450, 600]):
            img = _render(path, pi, d, clip=r)
            g = (img.astype(np.float32) @ np.array([0.299, 0.587, 0.114])).clip(0, 255).astype(np.uint8)
            for variant in (g, _remove_rules(g)):
                for p in (psm, 8, 6, 13):
                    try:
                        words = image_words(Image.fromarray(variant), psm=p)
                    except Exception:
                        continue
                    txt = ' '.join(w['text'] for w in words)
                    reads.append(txt)
                    if want and want in _norm(txt):
                        return dict(ok=True, read=txt)
    return dict(ok=False, read=' | '.join(sorted(set(reads)))[:300])


def text_check(path, pi, expected, absent=None):
    """text-layer read-back with PyMuPDF (if installed) or catfix TextLayer."""
    txt = None
    try:
        try:
            import pymupdf as fitz
        except Exception:
            import fitz
        doc = fitz.open(path)
        txt = doc[pi].get_text()
        doc.close()
    except Exception:
        from .vector import Editor
        from .textlayer import TextLayer
        E = Editor(path)
        try:
            TL = TextLayer(E)
            txt = '\n'.join(t for t, ln in TL.text_lines(pi))
        finally:
            E.close()
    res = dict(found=expected in txt)
    if absent:
        res['absent_ok'] = absent not in txt
    res['ok'] = res['found'] and res.get('absent_ok', True)
    return res


def write_report(rows, out_md, title='BÁO CÁO NGHIỆM THU'):
    """rows: list of dict(stt, file, page, item, old, new, result ('ĐẠT'|'CHƯA ĐẠT'|'CHƯA THỂ XÁC MINH'), evidence)."""
    lines = ['# ' + title, '', '| STT | File | Trang | Việc | Cũ | Mới | Kết quả | Bằng chứng |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %s |' % tuple(str(r.get(k, '')).replace('|', '/') for k in
                                                                     ('stt', 'file', 'page', 'item', 'old', 'new', 'result', 'evidence')))
    n_ok = sum(1 for r in rows if r.get('result') == 'ĐẠT')
    lines += ['', 'Tổng: %d việc, ĐẠT %d, còn lại %d.' % (len(rows), n_ok, len(rows) - n_ok)]
    open(out_md, 'w', encoding='utf-8').write('\n'.join(lines))
    json.dump(rows, open(out_md.rsplit('.', 1)[0] + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return out_md
