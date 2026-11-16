# -*- coding: utf-8 -*-
"""Trang cấu tạo – vật liệu CDLF 120, 150, 200 + cách đọc mã CDLF 200 (nguồn nguon_CDL.pdf tr.10 và tr.6; QĐ 187).
Tên bộ phận dịch theo đúng từ đã dùng ở bảng 'MATERIALS CDLF 32, 42' đã duyệt (支架 Bracket, 泵头 Pump head, 机械密封 Mechanical seal, 支撑导叶 Support diffuser,
导叶 Diffuser, 导流器 Inducer, 进出水段 Inlet and outlet chamber, 底座 Base plate, 叶轮 Impeller, 轴 Shaft, 耐压筒 Cylinder, 联轴器 Coupling, 橡胶零件 Rubber parts);
hai từ mới: 出水体 → Discharge body, 轴套 → Shaft sleeve. Hàng 2 và 8 lấy bản CDLF (inox)."""
import pymupdf, numpy as np, cv2, lib
VL = [('1', 'Bracket', 'Cast iron', 'ASTM25B'), ('2', 'Pump head', 'Stainless steel', 'AISI304'), ('3', 'Mechanical seal', '', ''),
      ('4', 'Discharge body', 'Stainless steel', 'AISI304'), ('5', 'Support diffuser', 'Stainless steel', 'AISI304'), ('6', 'Diffuser', 'Stainless steel', 'AISI304'),
      ('7', 'Inducer', 'Stainless steel', 'AISI304'), ('8', 'Inlet and outlet chamber', 'Stainless steel', 'AISI304'), ('9', 'Base plate', 'Cast iron', 'ASTM 80-55-06'),
      ('11', 'Impeller', 'Stainless steel', 'AISI304'), ('12', 'Shaft', 'Stainless steel', 'AISI304'), ('13', 'Shaft sleeve', 'Tungsten carbide', ''),
      ('14', 'Cylinder', 'Stainless steel', 'AISI304'), ('15', 'Coupling', 'Carbon steel', ''), ('–', 'Rubber parts', 'NBR', '')]
MA = [('200', 'Rated flow (m³/h)'), ('3', 'Number of stages'), ('A', 'One small impeller, type A (2A = two)'), ('B', 'One small impeller, type B (2B = two)'), ('T', 'Three-phase 3~ 380–415 V')]
def anh(out='sec120.png'):
    pg = pymupdf.open('nguon_CDL.pdf')[9]; pm = pg.get_pixmap(dpi=300, clip=pymupdf.Rect(98, 446, 264, 712), colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width).copy(); a[a > 140] = 255      # bỏ nền ảnh mờ của trang nguồn, giữ nét vẽ
    cv2.imwrite(out, a); return out, pm.width, pm.height
def them(doc, goc, c_lop, k, st):
    """Nhân bản trang cấu tạo chỉ số k của bản gốc, chèn ngay sau, thay nội dung."""
    doc.insert_pdf(goc, from_page=k, to_page=k, start_at=k + 1); pg = doc[k + 1]
    _pe = pymupdf.open(lib.KHO + '/CATALOG SUA/CATALOGUE DA DUYET/PEROTAC/PEROTAC - Bơm trục đứng CDLF.pdf')      # câu chung 3 hãng, đọc từ bản PEROTAC đã duyệt tr.1
    cu = [s['text'].strip() for s in lib._spans(_pe[0]) if s['text'].startswith(('Light vertical multistage centrifu', 'components in stainless steel 304'))]
    cau = cu[0] if 'stainless steel 304' in cu[0] else cu[0] + ' ' + cu[1]      # câu mô tả CDLF lấy từ trang đã duyệt (không gõ lại)
    assert cau.startswith('Light vertical multistage centrifugal pump') and cau.endswith('304 or 316L'), cau
    if st.get('chu'): lib.xoa(pg, chu=st['chu'])
    lib.xoa(pg, vung=[st['vung']]); c = c_lop(pg); x = st['x']; w = st['w']; hd = st['hd']
    for viet in st.get('viet', []): c(*viet)
    def tieu_de(xx, y, t, ww):
        c(xx, y, t, hd['co'], True, hd['mau']); pg.draw_line((xx, y + hd['co'] * 1.45), (xx + ww, y + hd['co'] * 1.45), color=hd['mau'], width=0.7)
    tieu_de(x, st['y1'], 'SECTION DRAWING  CDLF 120, 150, 200', w)
    f, iw, ih = anh(); r = pymupdf.Rect(st['anh']); k_ = min(r.width / iw, r.height / ih)
    pg.insert_image(pymupdf.Rect(r.x0 + (r.width - iw * k_) / 2, r.y0, r.x0 + (r.width + iw * k_) / 2, r.y0 + ih * k_), filename=f)
    tieu_de(x, st['y2'], 'MATERIALS  CDLF 120, 150, 200', w)
    y = st['y2'] + st['bang_dy']; b = st['bang']; pg.draw_rect(pymupdf.Rect(x, y, x + w, y + 13), color=None, fill=b['nen_dau'])
    for dx, t in zip(b['cot'], ['NO.', 'NAME', 'MATERIAL', 'AISI / ASTM']): c(x + dx, y + 2.9, t, 7, True, b['chu_dau'])
    y += 13
    for i, row in enumerate(VL):
        if b.get('soc') and i % 2 == 0: pg.draw_rect(pymupdf.Rect(x, y, x + w, y + b['rh']), color=None, fill=b['soc'])
        for j, (dx, t) in enumerate(zip(b['cot'], row)):
            if t: c(x + dx, y + (b['rh'] - b['co'] * 1.117) / 2, t, b['co'], j == 0, b['chu'])
        y += b['rh']; pg.draw_line((x, y), (x + w, y), color=b['ke'], width=0.5)
    c(x, y + 4, 'Items 2, 8: CDLF version.', b.get('co_ghi', 7), False, b['ghi'])
    # cách đọc mã CDLF 200
    m = st['ma']; xm, ym = m['x'], m['y']; tieu_de(xm, ym, 'MODEL DESIGNATION', m['w']); ym += m['d0']
    c(xm, ym, 'CDLF 200', m['co_k'], True, m['mau_k']); ym += m['p'] + 0.8; c(xm, ym, 'Example:  CDLF200-3-A-BT', m['co_t'], False, m['mau_vd']); ym += m['p'] + 1.2
    c(xm, ym, 'CDLF', m['co_k'], True, m['mau_k']); dong = ''
    for tu in cau.split() + [None]:
        if tu is None or c.w((dong + ' ' + tu).strip(), m['co_t']) > m['w'] - m['dx'] - 30:
            c(xm + m['dx'], ym + 0.3, dong, m['co_t'], False, m['mau_t']); ym += m['p']; dong = tu or ''
        else: dong = (dong + ' ' + tu).strip()
    for kk, t in MA: c(xm, ym, kk, m['co_k'], True, m['mau_k']); c(xm + m['dx'], ym + 0.3, t, m['co_t'], False, m['mau_t']); ym += m['p']
    return pg
