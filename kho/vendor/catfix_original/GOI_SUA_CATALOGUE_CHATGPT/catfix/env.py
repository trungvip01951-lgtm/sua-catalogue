"""Check what this Python environment can do.   python -m catfix.env"""
import importlib
import os
import platform
import shutil
import sys

from ._compat import tesseract_cmd, utf8_stdio

CHECKS = [
    ('numpy', 'numpy', True, 'tính toán'),
    ('PIL', 'Pillow', True, 'xử lý ảnh'),
    ('pikepdf', 'pikepdf', False, 'đọc/ghi PDF (ưu tiên)'),
    ('pymupdf', 'PyMuPDF', False, 'đọc/ghi + vẽ trang PDF (dự phòng; tên cũ "fitz")'),
    ('scipy', 'scipy', True, 'tách chữ trên ảnh, đường cong'),
    ('cv2', 'opencv-python', False, 'xoá nền ảnh đẹp hơn (inpaint)'),
    ('fontTools', 'fonttools', False, 'kiểm tra font có chữ hay không (chữ thật)'),
    ('pytesseract', 'pytesseract', False, 'gọi OCR'),
    ('openpyxl', 'openpyxl', False, 'không bắt buộc (catfix sửa Excel trực tiếp XML)'),
]


def report(verbose=True):
    ok = {}
    lines = []
    for mod, pipname, required, why in CHECKS:
        name = mod
        try:
            if mod == 'pymupdf':
                try:
                    m = importlib.import_module('pymupdf')
                except Exception:
                    m = importlib.import_module('fitz')
            else:
                m = importlib.import_module(mod)
            ver = getattr(m, '__version__', getattr(m, 'VersionBind', ''))
            ok[mod] = True
            lines.append('  [CÓ ]  %-12s %-10s %s' % (pipname, ver, why))
        except Exception:
            ok[mod] = False
            lines.append('  [THIẾU] %-12s %-10s %s%s' % (pipname, '', why, '  <-- BẮT BUỘC' if required else ''))
    for b, why in (('tesseract', 'OCR đọc chữ (bắt buộc cho file nét vẽ/ảnh)'), ('pdftoppm', 'vẽ trang (dự phòng nếu thiếu PyMuPDF)'),
                   ('qpdf', 'kiểm tra cấu trúc PDF (không bắt buộc)')):
        p = tesseract_cmd() if b == 'tesseract' else shutil.which(b)
        ok[b] = bool(p)
        lines.append('  [%s] %-12s %s%s' % ('CÓ ' if p else 'THIẾU', b, why, ('   (%s)' % p) if (p and b == 'tesseract') else ''))
    if ok.get('tesseract') and ok.get('pytesseract'):
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd()
            pytesseract.get_tesseract_version()
        except Exception as e:
            lines.append('  (pytesseract chưa gọi được tesseract: %s – catfix sẽ gọi thẳng chương trình)' % type(e).__name__)
    if ok.get('tesseract'):
        try:
            import subprocess
            r = subprocess.run([tesseract_cmd(), '--list-langs'], capture_output=True, encoding='utf-8', errors='replace', timeout=60)
            langs = (r.stdout + r.stderr).split()
            if 'eng' not in langs:
                ok['tesseract'] = False
                lines.append('  [THIẾU] tesseract chưa có dữ liệu tiếng Anh (eng)  <-- BẮT BUỘC')
        except Exception as e:
            ok['tesseract'] = False
            lines.append('  [LỖI ] chạy tesseract không được: %s' % e)
    can_pdf = ok.get('pikepdf') or ok.get('pymupdf')
    can_render = ok.get('pymupdf') or ok.get('pdftoppm')
    verdict = []
    verdict.append(('Mở/ghi PDF', can_pdf))
    verdict.append(('Vẽ trang để so sánh', can_render))
    verdict.append(('OCR (chữ nét vẽ, chữ trên ảnh)', ok.get('tesseract')))
    verdict.append(('Tách chữ trên ảnh', ok.get('scipy')))
    lines.append('KẾT LUẬN:')
    for k, v in verdict:
        lines.append('  %-34s %s' % (k, 'ĐƯỢC' if v else 'KHÔNG ĐƯỢC'))
    if not all(v for k, v in verdict):
        lines.append('CÁCH BỔ SUNG (chỉ làm khi anh Trung đồng ý):')
        lines.append('  "%s" -m pip install numpy scipy pillow pymupdf pikepdf opencv-python-headless fonttools pytesseract' % sys.executable)
        if not ok.get('tesseract'):
            lines.append('  Tesseract-OCR: ' + ('cài bản Windows của UB Mannheim (có sẵn tiếng Anh) vào C:\\Program Files\\Tesseract-OCR'
                                             if os.name == 'nt' else 'apt-get install tesseract-ocr tesseract-ocr-eng'))
    txt = 'Python %s · %s\n' % (sys.version.split()[0], platform.platform()) + '\n'.join(lines)
    if verbose:
        print(txt)
    return ok, verdict


if __name__ == '__main__':
    utf8_stdio()
    report()
