# Đối chiếu số đọc bằng mắt (so_lieu.py) với OCR tesseract (đọc cả bảng, bỏ nét kẻ), so theo từng dòng số. In dòng không khớp để soi lại.
import re, pymupdf, pytesseract, numpy as np, cv2
from PIL import Image
import so_lieu
D = so_lieu.doc(); doc = pymupdf.open('nguon_CDL.pdf'); khong = []; tong = 0
def dong_so(pn, clip):
    pm = doc[pn - 1].get_pixmap(dpi=300, clip=clip); im = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width, pm.n)[..., :3]
    g = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY); bw = (g < 140).astype(np.uint8)
    hl = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((1, 150), np.uint8)); vl = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((60, 1), np.uint8))
    g[cv2.dilate(hl | vl, np.ones((3, 3), np.uint8)) > 0] = 255
    t = pytesseract.image_to_string(Image.fromarray(g), config='--psm 6 -c tessedit_char_whitelist=0123456789. ')
    return [[float(x) for x in re.findall(r'\d+(?:\.\d+)?', l)] for l in t.splitlines() if l.strip()]
for dai, d in D.items():
    r = doc[d['trang'] - 1].rect
    for loai, clip, lay in (('perf', pymupdf.Rect(r.width * 0.435, 165, r.width - 25, r.height * 0.535), lambda m: m['h']),
                            ('dim', pymupdf.Rect(r.width * 0.565, r.height * 0.555, r.width * 0.822, r.height - 95), lambda m: m['dim'])):
        ocr = dong_so(d['trang'], clip)
        for m in d['models']:
            tong += 1; v = [float(x) for x in lay(m)]
            if v not in ocr:
                gan = max(ocr, key=lambda o: sum(a == b for a, b in zip(o, v)) - abs(len(o) - len(v)), default=[])
                khong.append(f'{dai} {loai} {m["nguon"]}: mắt {v} | OCR gần nhất {gan}')
print('\n'.join(khong)); print('dòng đã so', tong, '| không có dòng OCR trùng hệt', len(khong))
