# Đọc lại 3 PDF ứng viên: (1) mọi model mới có đúng kW, HP, dãy H và bộ kích thước như so_lieu.py; (2) trang cũ không đổi ngoài số trang và các chỗ chủ ý sửa.
import pymupdf, so_lieu, lib, re
D = so_lieu.doc(); KQ = []
def spans(p): return [s for b in p.get_text('dict')['blocks'] for l in b.get('lines', []) for s in l['spans'] if s['text'].strip()]
for h in ('REDPUMP', 'PEROTAC', 'AQUARIS'):
    moi = pymupdf.open(f'{h} - Bơm trục đứng CDLF.pdf'); goc = pymupdf.open(lib.goc_cdlf(h)); n0 = goc.page_count
    SP = {i: spans(moi[i]) for i in range(n0 + 1, moi.page_count)}
    def cung_dong(ten):      # các dãy chữ nằm cùng dòng (lệch tâm ≤ 3 pt), bên phải mỗi chỗ xuất hiện tên
        out = []
        for i, ss in SP.items():
            for s in ss:
                if s['text'].strip() != ten: continue
                yc = (s['bbox'][1] + s['bbox'][3]) / 2
                r = sorted([t for t in ss if t is not s and abs((t['bbox'][1] + t['bbox'][3]) / 2 - yc) <= 3 and t['bbox'][0] > s['bbox'][2] - 1], key=lambda t: t['bbox'][0])
                out.append([t['text'].strip() for t in r])
        return out
    class _D(dict):
        def get(self, k, d=None): return cung_dong(k)
    dong = _D()
    sai = 0; dem = 0
    for dai, d in D.items():
        gop = dict(lib.gop_kich_thuoc(d['models']))
        for m in d['models']:
            dem += 1; ung = dong.get(m['ten'], [])
            can = [lib.g(m['kw']), lib.g(m['hp'])] + [lib.g(v) for v in m['h']]
            co = any([x for x in r if re.fullmatch(r'[\d.]+', x)][-len(can):] == can for r in ung)
            if not co: sai += 1; print(h, 'PERF không khớp', m['ten'], ung[:2])
        for ten, dim in gop.items():
            ung = dong.get(ten, []); 
            if not any(r[:5] == [str(v) for v in dim] for r in ung): sai += 1; print(h, 'DIM không khớp', ten, ung[:2])
    # trang cũ
    doi = []
    chen = 3 if h == 'REDPUMP' else 2      # trang cấu tạo CDLF 120/150/200 chèn ở chỉ số này
    for i in range(n0):
        j = i + (1 if i >= chen else 0)
        a = [s['text'] for s in spans(goc[i])]; b = [s['text'] for s in spans(moi[j])]
        if sorted(a) != sorted(b): doi.append((i + 1, len(set(a) ^ set(b))))
        da, db = len(goc[i].get_drawings()), len(moi[j].get_drawings()); ia, ib = len(goc[i].get_image_info()), len(moi[j].get_image_info())
        if (da, ia) != (db, ib) and i != 0: print(h, 'tr.', i + 1, 'nét/ảnh đổi', da, db, ia, ib)
    print(h, 'model đã so', dem, '| sai', sai, '| trang cũ có chữ khác (trang, số chuỗi khác):', doi)
