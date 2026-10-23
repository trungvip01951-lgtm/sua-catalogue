"""Bộ kiểm thử catfix - chạy:  python tests/run_tests.py
Mỗi bài in ĐẠT / CHƯA ĐẠT kèm số đo.  Không đụng tới file catalogue thật (chỉ dùng tests/fixtures)."""
import os
import sys
import tempfile
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from catfix._compat import utf8_stdio  # noqa: E402

utf8_stdio()   # Windows: in tiếng Việt không lỗi bảng mã
FX = os.path.join(HERE, 'fixtures')
OUT = os.path.join(os.environ.get('CATFIX_CACHE', os.path.join(tempfile.gettempdir(), 'catfix_cache')), 'test_out')
os.makedirs(OUT, exist_ok=True)   # cố định -> chạy từng phần vẫn dùng chung kết quả

RESULTS = []


def check(name, cond, detail=''):
    RESULTS.append((name, bool(cond), detail))
    print('  [%s] %s %s' % ('ĐẠT' if cond else 'CHƯA ĐẠT', name, detail))
    return cond


def t_env():
    from catfix import env
    ok, verdict = env.report(verbose=True)
    for k, v in verdict:
        check('Môi trường: ' + k, v)


def t_tokenizer():
    from catfix.pdfdoc import PdfDoc
    from catfix import cs
    for f in sorted(os.listdir(FX)):
        if not f.endswith('.pdf'):
            continue
        d = PdfDoc(os.path.join(FX, f))
        data = d.page_content(0)
        t = time.time()
        ins = cs.parse(data)
        check('Đọc/ghi lại luồng nội dung không mất byte: ' + f, cs.serialize(ins) == data,
              '(%d lệnh, %.2fs)' % (len(ins), time.time() - t))


def t_outline_text():
    from catfix.vector import Editor
    from catfix.otext import OutlineText
    from catfix import verify
    src = os.path.join(FX, 'fx_vector_aquaris_sp_p9_goc.pdf')
    E = Editor(src)
    T = OutlineText(E)
    T.learn([0], verbose=False)
    m = T.find(0, '818')
    if not check('Chữ nét vẽ: tìm thấy đúng 1 chỗ "818"', len(m) == 1, str(m)):
        return
    T.replace(m[0], '815', align='center', verbose=False)
    out = os.path.join(OUT, 'vec_815.pdf')
    E.save(out)
    E2 = Editor(out)
    T2 = OutlineText(E2)
    T2.learn([0], verbose=False)
    m2 = T2.find(0, '815')
    check('Chữ nét vẽ: đọc lại thấy "815", hết "818"', len(m2) == 1 and not T2.find(0, '818'))
    exp = [(515.52, 509.328, 519.36, 515.1216), (520.7184, 509.4888, 522.78, 515.1216), (524.8469, 509.3282, 528.7013, 514.9922)]
    if m2:
        err = max(abs(a - b) for g, e in zip(m2[0].glyphs, exp) for a, b in zip(g.bbox, e))
        check('Chữ nét vẽ: vị trí chữ mới trùng bản đã kiểm duyệt (sai lệch <= 0.01pt)', err <= 0.01, 'sai lệch %.4f pt' % err)
    regs = verify.diff_regions(src, out, dpi=150)
    cell = (515.0, 508.5, 529.5, 516.0)
    bad = verify.unexpected(regs, {1: [cell]}, pad=1.5)
    check('Chữ nét vẽ: chỉ ô sửa thay đổi điểm ảnh', regs and not bad, 'vùng đổi=%s ngoài vùng=%s' % (regs, bad))


def t_textlayer():
    from catfix.vector import Editor
    from catfix.textlayer import TextLayer
    from catfix import verify
    src = os.path.join(FX, 'fx_text_wc_p1.pdf')
    E = Editor(src)
    TL = TextLayer(E)
    m1 = TL.find(0, 'irrugation')
    m2 = TL.find(0, '(KW)')
    if not check('Chữ thật: tìm thấy "irrugation" và "(KW)"', len(m1) == 1 and len(m2) == 1):
        return
    boxes = [m1[0].bbox, m2[0].bbox]
    TL.replace(m1[0], 'irrigation', align='left', verbose=False)
    TL.replace(m2[0], '(kW)', align='center', verbose=False)
    out = os.path.join(OUT, 'text.pdf')
    E.save(out)
    r1 = verify.text_check(out, 0, 'irrigation', absent='irrugation')
    r2 = verify.text_check(out, 0, '(kW)', absent='(KW)')
    check('Chữ thật: đọc lại lớp chữ đúng', r1['ok'] and r2['ok'], str((r1, r2)))
    regs = verify.diff_regions(src, out, dpi=150)
    bad = verify.unexpected(regs, {1: [(b[0] - 1, b[1] - 1, b[2] + 6, b[3] + 1) for b in boxes]}, pad=2)
    check('Chữ thật: chỉ chỗ sửa thay đổi', regs and not bad, 'vùng đổi=%s ngoài=%s' % (regs, bad))


def t_raster():
    from catfix.vector import Editor
    from catfix.raster import Raster
    from catfix import verify
    src = os.path.join(FX, 'fx_raster_perotac_sp_p9.pdf')
    E = Editor(src)
    R = Raster(E)
    mb = E.mediabox(0)
    im = R.image_at(0, (10, 10, mb[2] - 10, mb[3] - 10))
    check('Ảnh: chọn đúng ảnh đang hiển thị (không chọn lớp ảnh chỉ hiện trong nét chữ)', im.name == 'X11', repr(im))
    cv = R.canvas(im)
    hits = R.find(cv, '1750')
    if not check('Ảnh: OCR tìm thấy "1750"', len(hits) == 1, str([h['box'] for h in hits])):
        return
    h = hits[0]
    rect = cv.rect([int(round(v)) for v in h['box']])
    u0, v0, u1, v1 = h['box']
    bank = R.glyph_bank(cv, box=(0, int(v0 - 150), im.W, int(v1 + 150)))
    check('Ảnh: học được mẫu chữ số 1, 5, 7', all(c in bank['glyphs'] for c in '157'))
    R.replace_word(cv, h, '175', bank, align='center')
    R.commit(cv)
    out = os.path.join(OUT, 'raster.pdf')
    E.save(out)
    oc = verify.ocr_check(out, 0, (rect[0] - 4, rect[1] - 2, rect[2] + 4, rect[3] + 2), '175')
    check('Ảnh: OCR đọc lại "175"', oc['ok'], repr(oc['read']))
    regs = verify.diff_regions(src, out, dpi=100, thr=48, min_size=2.0)
    bad = verify.unexpected(regs, {1: [(rect[0] - 3, rect[1] - 3, rect[2] + 3, rect[3] + 3)]}, pad=3)
    check('Ảnh: thay đổi rõ rệt (>48 mức, >2pt) chỉ nằm ở ô sửa', regs and not bad, 'vùng=%s ngoài=%s' % (regs, bad))
    E3 = Editor(src)
    R3 = Raster(E3)
    res = R3.noop_test(0)
    check('Ảnh: ghi lại ảnh không sửa gì -> sai khác trung bình < 1 mức màu', res and res['mean_diff'] < 1.0, str(res))


def t_charts():
    import numpy as np
    from catfix.vector import Editor
    from catfix.otext import OutlineText
    from catfix import charts
    Ch = charts.Chart.from_ticks([(0, 100.0), (10, 200.0)], [(0, 50.0), (100, 250.0)])
    pts = [(0, 80), (2, 78), (4, 72), (6, 63), (8, 50), (10, 32)]
    path = Ch.smooth_path(pts)
    d = Ch.to_data(charts.sample_path(path))
    dev = max(abs(Ch.value_at(d, q) - h) for q, h in pts)
    check('Biểu đồ: đường cong mượt đi sát điểm bảng (đơn giản)', dev <= max(1.0, 0.02 * 80) + 1e-6, 'lệch tối đa %.3f' % dev)
    src = os.path.join(FX, 'fx_vector_aquaris_sp_p9_goc.pdf')
    E = Editor(src)
    P = E.page(0)
    T = OutlineText(E)
    T.learn([0], verbose=False)
    gx, gy = charts.gridlines(P, (205, 95, 535, 415))
    xt = charts.snap_ticks(charts.ticks_from_labels(T, 0, (200, 75, 535, 100), 'x'), gx)
    yt = charts.snap_ticks(charts.ticks_from_labels(T, 0, (180, 95, 209, 415), 'y'), gy)
    ch = charts.Chart.from_ticks(xt, yt)
    check('Biểu đồ: hiệu chỉnh trục tuyến tính', ch.warning is None and ch.residual[0] < 0.6 and ch.residual[1] < 0.6, str(ch.residual))
    cur = charts.curve_objects(P, (205, 95, 535, 415), color=(0.133, 0.365, 0.635))
    check('Biểu đồ: tìm đủ 8 đường cong', len(cur) == 8, str(cur))
    Qs = [0, 5, 10, 14, 16, 18]
    H = [170, 157, 133, 110, 90, 65]
    path = ch.smooth_path(list(zip(Qs, H)))
    E.replace_path(0, cur[0], path)
    out = os.path.join(OUT, 'chart.pdf')
    E.save(out)
    P2 = Editor(out).page(0)
    d2 = ch.to_data(charts.sample_path(P2.object_pagepath(cur[0])))
    cmp_ = ch.compare(d2, list(zip(Qs, H)), tol_abs=ch.last_fit['tol'] if ch.last_fit else 0.5)
    check('Biểu đồ: đường vẽ lại khớp bảng trong dung sai', all(c['ok'] for c in cmp_),
          str([(c['Q'], c['H_table'], c['H_curve']) for c in cmp_]) + ' %s' % (ch.last_fit,))
    o2 = P2.objs[cur[0]]
    o1 = P.objs[cur[0]]
    check('Biểu đồ: giữ nguyên màu và độ dày nét', o1['stroke'] == o2['stroke'] and abs(o1['lw'] - o2['lw']) < 1e-9)


def t_images():
    from catfix.vector import Editor
    from catfix.raster import Raster
    from catfix import images, verify
    src = os.path.join(FX, 'fx_cover_cdlf_aquaris_p1.pdf')
    E = Editor(src)
    R = Raster(E)
    ims = {im.name: im for im in R.images(0)}
    cover = [ims[n] for n in ('R13', 'R16', 'R18', 'R20', 'R22', 'R25')]
    b = ims['R13'].page_bbox
    axis = (b[0] + b[2]) / 2
    images.mirror_images(E, cover, axis)
    cb = ims['R25'].page_bbox
    slot = (2 * axis - cb[2], cb[1], 2 * axis - cb[0], cb[3])
    images.delete_image(E, ims['R25'])
    dst = images.fit_bbox(ims['R16'].page_bbox, slot, keep_aspect='height', anchor='bottom-center')
    images.clone_image(E, ims['R16'], dst, after=ims['R25'], flip_h=True)
    out = os.path.join(OUT, 'cover.pdf')
    E.save(out)
    R2 = Raster(Editor(out))
    new = [(im.name, im.page_bbox) for im in R2.images(0)]
    names = [n for n, bb in new]
    check('Ảnh bìa: xoá bơm đế gang (R25 không còn)', 'R25' not in names, str(names))
    copies = [bb for n, bb in new if n == 'R16']
    ok = len(copies) == 2 and any(max(abs(x - y) for x, y in zip(bb, dst)) < 0.01 for bb in copies)
    check('Ảnh bìa: bản sao bơm đặt đúng ô (sai lệch < 0.01pt)', ok, str(copies))
    regs = verify.diff_regions(src, out, dpi=60)
    bad = verify.unexpected(regs, {1: [b]}, pad=3)
    check('Ảnh bìa: chỉ vùng ảnh bìa thay đổi (chữ trên bìa giữ nguyên vị trí)', not bad, str(bad))


def t_xlsx():
    from catfix.xlsx import Xlsx, diff_cells, diff_parts
    src = os.path.join(FX, 'fx_dwo.xlsx')
    X = Xlsx(src)
    for r, v in [('D16', 0.5), ('D17', 1), ('D18', 1.5), ('D20', 3), ('D21', 4), ('D22', 5), ('C21', 3), ('C22', 3.7)]:
        X.set_number('Sheet1', r, v)
    X.replace_in_cell('Sheet1', 'C15', '(kw)', '(kW)')
    out = os.path.join(OUT, 'dwo.xlsx')
    X.save(out)
    d = diff_cells(src, out)
    changed = sorted(r for s, r, a, b in d)
    check('Excel: chỉ đúng các ô cần sửa thay đổi', changed == sorted(['C15', 'C21', 'C22', 'D16', 'D17', 'D18', 'D20', 'D21', 'D22']), str(changed))
    parts = diff_parts(src, out)
    check('Excel: ảnh/định dạng/in ấn không bị đụng tới', all(p in ('xl/sharedStrings.xml', 'xl/worksheets/sheet2.xml', 'xl/calcChain.xml') for p in parts), str(parts))
    try:
        import openpyxl
        wb = openpyxl.load_workbook(out)
        ws = wb['Sheet1']
        check('Excel: mở lại bằng openpyxl được, giá trị đúng', [ws['D%d' % i].value for i in range(16, 23)] == [0.5, 1, 1.5, 2, 3, 4, 5])
    except ImportError:
        check('Excel: (bỏ qua mở lại - không có openpyxl)', True)


def t_structure():
    from catfix import verify
    for f, o in (('fx_vector_aquaris_sp_p9_goc.pdf', 'vec_815.pdf'), ('fx_text_wc_p1.pdf', 'text.pdf'), ('fx_raster_perotac_sp_p9.pdf', 'raster.pdf'),
                 ('fx_cover_cdlf_aquaris_p1.pdf', 'cover.pdf')):
        p = os.path.join(OUT, o)
        if os.path.exists(p):
            r = verify.structure_check(os.path.join(FX, f), p)
            check('Cấu trúc file sau sửa hợp lệ: ' + o, r['ok'], str(r['problems']) + ' %d->%d bytes' % (r['size_before'], r['size_after']))


def t_session():
    """đường dẫn vào/ra trên máy anh Trung (giả lập cây thư mục, tên thư mục có dấu kiểu NFD) và trên máy chủ ChatGPT."""
    import shutil
    import unicodedata
    from catfix.session import Session, IN_NAME, OUT_NAME, REPORT_NAME
    from catfix.recipes import Job
    base = tempfile.mkdtemp(prefix='catfix_ses_')
    root = os.path.join(base, 'Catalog Sua')
    ind = os.path.join(root, unicodedata.normalize('NFD', IN_NAME))           # tên kiểu NFD: vẫn phải nhận ra
    wc = 'Catalog cắt rác Aquaris WC (bản mới).pdf'
    cm = 'bơm trục ngnag perotac model CM (bản mới).pdf'
    os.makedirs(os.path.join(ind, 'Nước thải'))
    os.makedirs(os.path.join(ind, 'Trục ngang'))
    shutil.copy(os.path.join(FX, 'fx_text_wc_p1.pdf'), os.path.join(ind, 'Nước thải', wc))
    shutil.copy(os.path.join(FX, 'fx_text_wc_p1.pdf'), os.path.join(ind, 'Trục ngang', cm))
    S = Session(root=root)
    out_wc = os.path.join(root, OUT_NAME, 'Nước thải', wc)
    ok = (S.mode == 'local' and S.src(wc) == os.path.join(ind, 'Nước thải', wc) and S.dst(wc) == out_wc and
          S.dst(cm, rename=cm.replace('ngnag', 'ngang')) == os.path.join(root, OUT_NAME, 'Trục ngang', cm.replace('ngnag', 'ngang')))
    check('Đường dẫn máy anh: tìm đúng file vào, file ra cùng tên khác thư mục, đổi tên #129', ok, repr(S))
    job = S.job(wc)
    job.text_replace(0, 'irrugation', 'irrigation', align='left', expect=1)
    job.save()
    job.close()
    r = job.check()
    log = os.path.join(root, OUT_NAME, REPORT_NAME, wc + '.log.json')
    check('Đường dẫn máy anh: sửa + lưu + kiểm qua S.job (nhật ký vào _BAO CAO)', os.path.isfile(out_wc) and os.path.isfile(log) and r['ok'],
          str(r['unexpected']) + str(r['missing']))
    sub = S.dst(wc, sub='G02 (gồm cả G01)')
    j2 = S.job(wc, sub='G02 (gồm cả G01)', src=S.result(wc))
    j2.close()
    check('Đường dẫn máy anh: G02 lấy đúng file đã sửa của G01, ghi ra thư mục riêng, nhật ký riêng',
          S.result(wc) == out_wc and sub != out_wc and os.path.dirname(sub).endswith('G02 (gồm cả G01)') and
          j2.src == out_wc and j2.dst == sub and j2.log_path != job.log_path, sub)
    S.progress('G08', 'XONG', '1/1 ĐẠT')
    refused = False
    try:
        Job(S.src(wc), S.src(wc))
    except ValueError:
        refused = True
    check('Đường dẫn máy anh: ghi tiến độ được, không cho ghi đè file vào', 'G08' in S.read_progress() and refused)
    data = os.path.join(base, 'data')                                    # giả lập /mnt/data của ChatGPT
    os.makedirs(os.path.join(data, 'catfix_pkg', 'x'))
    shutil.copy(os.path.join(FX, 'fx_text_wc_p1.pdf'), os.path.join(data, wc))
    shutil.copy(os.path.join(FX, 'fx_text_wc_p1.pdf'), os.path.join(data, 'catfix_pkg', 'x', wc))   # bản mồi: phải bỏ qua
    S2 = Session(root=os.path.join(base, 'khong_co'), data=data)
    check('Đường dẫn máy chủ ChatGPT: file tải lên trong /mnt/data, ra /mnt/data/out',
          S2.mode == 'sandbox' and S2.src(wc) == os.path.join(data, wc) and S2.dst(wc) == os.path.join(data, 'out', wc), repr(S2))
    shutil.rmtree(base, ignore_errors=True)


def t_windows():
    """giả lập các điểm khác của Windows: bảng mã cp1252 khi đầu ra bị chuyển hướng; tesseract không nằm trong PATH."""
    import subprocess
    from catfix._compat import tesseract_cmd
    env = dict(os.environ, PYTHONIOENCODING='cp1252', PYTHONPATH=ROOT)
    env.pop('PYTHONUTF8', None)
    r = subprocess.run([sys.executable, '-c', "import catfix; print('ĐẠT ạ ố ằ')"], cwd=ROOT, env=env, capture_output=True)
    r2 = subprocess.run([sys.executable, '-m', 'catfix.env'], cwd=ROOT, env=env, capture_output=True)
    out2 = r2.stdout.decode('utf-8', 'replace')
    check('Windows: in tiếng Việt khi đầu ra dùng bảng mã cp1252 không lỗi',
          r.returncode == 0 and r.stdout.decode('utf-8').strip() == 'ĐẠT ạ ố ằ' and r2.returncode == 0 and 'KẾT LUẬN' in out2,
          (r.stderr + r2.stderr).decode('utf-8', 'replace')[-300:])
    tess = tesseract_cmd()
    code = ("from catfix import ocr; import sys\n"
            "t = ocr.region_text(sys.argv[1], 0, (50, 50, 560, 790), dpi=150, psm=6)\n"
            "print(ocr.TESSERACT, ocr.tesseract_available(), len(t))")
    env3 = dict(os.environ, PATH=os.path.join(ROOT, 'khong_co_thu_muc_nay'), PYTHONPATH=ROOT, CATFIX_TESSERACT=tess or '',
                CATFIX_CACHE=os.path.join(OUT, 'cache_win'))
    r3 = subprocess.run([sys.executable, '-c', code, os.path.join(FX, 'fx_text_wc_p1.pdf')], cwd=ROOT, env=env3, capture_output=True)
    o3 = r3.stdout.decode('utf-8', 'replace').split()
    check('Windows: tìm được tesseract khi không có trong PATH (biến CATFIX_TESSERACT / chỗ cài mặc định) và OCR chạy',
          r3.returncode == 0 and len(o3) == 3 and o3[1] == 'True' and int(o3[2]) > 50,
          r3.stdout.decode('utf-8', 'replace')[-200:] + r3.stderr.decode('utf-8', 'replace')[-300:])


TESTS = [('Môi trường', t_env), ('Bộ đọc luồng PDF', t_tokenizer), ('Chữ nét vẽ (Aquaris SP)', t_outline_text),
         ('Chữ thật (WC)', t_textlayer), ('Ảnh quét (Perotac SP)', t_raster), ('Biểu đồ', t_charts),
         ('Ảnh bìa (CDLF)', t_images), ('Excel (DWO)', t_xlsx), ('Cấu trúc file', t_structure),
         ('Đường dẫn (máy anh / máy chủ)', t_session), ('Windows', t_windows)]

if __name__ == '__main__':
    only = sys.argv[1:]
    t0 = time.time()
    for name, fn in TESTS:
        if only and not any(o.lower() in name.lower() for o in only):
            continue
        print('== ' + name)
        t = time.time()
        try:
            fn()
        except Exception as e:
            traceback.print_exc()
            check(name + ': chạy không lỗi', False, '%s: %s' % (type(e).__name__, e))
        print('   (%.1fs)' % (time.time() - t))
    n_ok = sum(1 for r in RESULTS if r[1])
    print('\nTỔNG KẾT: %d/%d ĐẠT  (%.0fs)  - file thử nghiệm ở %s' % (n_ok, len(RESULTS), time.time() - t0, OUT))
    if n_ok != len(RESULTS):
        print('CHƯA ĐẠT:')
        for r in RESULTS:
            if not r[1]:
                print('  - %s %s' % (r[0], r[2]))
        sys.exit(1)
