"""Tương thích Windows / Linux (chỉ dùng thư viện chuẩn – env.py dùng được cả khi thiếu numpy).

utf8_stdio()     : in tiếng Việt không lỗi khi chạy trên Windows (đầu ra bị chuyển hướng dùng bảng mã cp125x)
tesseract_cmd()  : tìm chương trình OCR tesseract (PATH, biến môi trường, chỗ cài mặc định trên Windows)
same_file(a, b)  : hai đường dẫn có trỏ cùng một file không (Windows không phân biệt hoa/thường)
"""
import os
import shutil
import sys


def utf8_stdio():
    for s in (sys.stdout, sys.stderr):
        try:
            enc = (getattr(s, 'encoding', None) or '').lower().replace('-', '').replace('_', '')
            if enc != 'utf8' and hasattr(s, 'reconfigure'):
                s.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass


def tesseract_cmd():
    """đường dẫn chạy được của tesseract, hoặc None."""
    cands = [os.environ.get('CATFIX_TESSERACT'), os.environ.get('TESSERACT_CMD'), shutil.which('tesseract')]
    if os.name == 'nt':
        bases = [os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)'), os.environ.get('ProgramW6432'),
                 r'C:\Program Files', r'C:\Program Files (x86)']
        la = os.environ.get('LOCALAPPDATA')
        if la:
            bases += [os.path.join(la, 'Programs'), la]
        for b in bases:
            if b:
                cands.append(os.path.join(b, 'Tesseract-OCR', 'tesseract.exe'))
    for c in cands:
        if not c:
            continue
        if os.path.isfile(c):
            return c
        w = shutil.which(c)
        if w:
            return w
    return None


def same_file(a, b):
    try:
        if os.path.exists(a) and os.path.exists(b):
            return os.path.samefile(a, b)
    except Exception:
        pass
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))
