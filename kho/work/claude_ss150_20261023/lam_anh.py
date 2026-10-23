# Ảnh SS-150…370 PEROTAC độ phân giải cao từ ảnh anh gửi 08/10 (QĐ 116): nền nối mép → trắng 255, bỏ bóng, cắt khung 82%.
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, out, nguong = sys.argv[1], sys.argv[2], int(sys.argv[3])
a = np.asarray(Image.open(src).convert('RGB')).astype(np.int16)
sang = a.min(2) >= nguong
lab, n = ndimage.label(sang)
mep = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
nen = np.isin(lab, list(mep))
b = a.copy(); b[nen] = 255
# bóng dưới đế: lan nền vào điểm xám nhạt ít màu (min ≥ 95, max−min < 22) ở 15% đáy vật, nối liền nền
ys0, _ = np.where(~nen); yday = ys0.max() - int((ys0.max() - ys0.min()) * 0.15)
xam = (a.min(2) >= 95) & ((a.max(2) - a.min(2)) < 22); xam[:yday] = False
lab2, _ = ndimage.label(xam | nen)
giu = set(np.unique(lab2[nen])) - {0}
nen = np.isin(lab2, list(giu)); b[nen] = 255
vat = ~nen
ys, xs = np.where(vat); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
h, w = y1 - y0 + 1, x1 - x0 + 1
canh = int(round(max(h, w) / 0.82)); cw = int(round(canh * w / h)) if h >= w else canh
ch = canh if h >= w else int(round(canh * h / w))
cw = max(cw, int(w / 0.82)) if h >= w else cw
can = np.full((ch, cw, 3), 255, np.uint8)
oy, ox = (ch - h) // 2, (cw - w) // 2
can[oy:oy + h, ox:ox + w] = b[y0:y1 + 1, x0:x1 + 1].astype(np.uint8)
Image.fromarray(can).save(out, quality=92)
print('vat', w, 'x', h, 'khung', cw, 'x', ch, 'nen lam trang', round(nen.mean(), 3), 'ty le canh dai', round(h / ch, 3))
