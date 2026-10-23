"""catfix - sửa catalogue PDF "vô hình": cùng font, cùng màu, cùng vị trí; file gốc không đụng tới.

Modules
  cs          content-stream tokenizer (lossless)          pdfdoc   PDF access (pikepdf / PyMuPDF), render
  vector      paths, glyph groups, Editor (all edits)      otext    OUTLINED text: learn / find / replace
  textlayer   REAL text (Tj/TJ): find / replace / insert    fonts    font encodings, widths
  raster      IMAGE pages: canvas, OCR, glyph bank, replace, patch/replace image
  images      image placement: delete / clone / mirror      charts   axes, curves, smooth redraw
  verify      diff regions, unexpected changes, sheets, OCR/text read-back, report
  inspect_pdf page types, what_is_at(rect)                  xlsx     Excel edits at XML level
  env         environment check  (python -m catfix.env)
  session     đường dẫn file vào/ra: máy anh Trung (Windows) hoặc máy chủ ChatGPT (/mnt/data)
"""
__version__ = '1.1.0'

from ._compat import utf8_stdio as _utf8_stdio

_utf8_stdio()   # Windows: in tiếng Việt không lỗi bảng mã


def __getattr__(name):          # nạp chậm: `python -m catfix.env` chạy được cả khi thiếu numpy
    if name == 'Editor':
        from .vector import Editor
        return Editor
    if name == 'Session':
        from .session import Session
        return Session
    raise AttributeError(name)
