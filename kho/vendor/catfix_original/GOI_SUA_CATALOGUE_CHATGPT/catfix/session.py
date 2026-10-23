"""Đường dẫn làm việc – tự nhận đang chạy ở đâu:
  * MÁY ANH TRUNG  : có thư mục  C:\\Users\\H2\\Desktop\\Catalog Sua\\BẢN MỚI 01-10-2026  (code chạy thẳng trên Windows)
  * MÁY CHỦ CHATGPT: file anh tải lên nằm trong /mnt/data

    from catfix.session import Session
    S = Session(); print(S)
    job = S.job('Catalog cắt rác Aquaris WC (bản mới).pdf')    # Job(file vào, file ra): ra CÙNG TÊN, KHÁC THƯ MỤC
    S.src(tên)                      # đường dẫn file vào (BẢN MỚI 01-10-2026\\<thư mục con>\\tên  hoặc /mnt/data/.../tên)
    S.dst(tên, rename=None, sub=None)   # file ra: BẢN MỚI 03-10-2026 (ChatGPT)\\<cùng thư mục con>\\tên  (/mnt/data/out/...)
    S.result(tên)                   # file ĐÃ SỬA của nhóm trước (vd G02 dùng kết quả G01)
    S.report('BAO CAO G08.md')      # đường dẫn trong thư mục _BAO CAO
    S.progress('G08', 'XONG', '12/12 ĐẠT');  print(S.read_progress())
Không bao giờ trả về đường dẫn ghi đè file vào.
"""
import datetime
import os
import unicodedata

from ._compat import same_file

ROOT_WIN = r'C:\Users\H2\Desktop\Catalog Sua'
ROOTS = (ROOT_WIN, '/mnt/c/Users/H2/Desktop/Catalog Sua')      # Windows; WSL (Linux chạy trong Windows)
IN_NAME = 'BẢN MỚI 01-10-2026'
OUT_NAME = 'BẢN MỚI 03-10-2026 (ChatGPT)'
REPORT_NAME = '_BAO CAO'
SANDBOX = '/mnt/data'


def nfc(s):
    return unicodedata.normalize('NFC', s)


def child(parent, name):
    """parent/name – chấp nhận tên có dấu tiếng Việt mã hoá kiểu khác (NFC/NFD)."""
    try:
        for e in os.listdir(parent):
            if nfc(e) == nfc(name):
                return os.path.join(parent, e)
    except OSError:
        pass
    return os.path.join(parent, name)


def _under(p, top):
    p, top = os.path.normcase(os.path.abspath(p)), os.path.normcase(os.path.abspath(top))
    return p == top or p.startswith(top.rstrip('\\/') + os.sep)


class Session(object):
    def __init__(self, root=None, data=None):
        cands = [root] if root else ([os.environ['CATFIX_ROOT']] if os.environ.get('CATFIX_ROOT') else list(ROOTS))
        root, in_dir = cands[0], child(cands[0], IN_NAME)
        for c in cands:
            if os.path.isdir(child(c, IN_NAME)):
                root, in_dir = c, child(c, IN_NAME)
                break
        if os.path.isdir(in_dir):
            self.mode = 'local'
            self.root = root
            self.in_dir = in_dir
            self.out_dir = child(root, OUT_NAME)
            self.skip = [self.out_dir]
        else:
            base = data or os.environ.get('CATFIX_DATA') or SANDBOX
            self.mode = 'sandbox'
            self.root = base
            self.in_dir = base
            self.out_dir = os.path.join(base, 'out')
            self.skip = [self.out_dir, os.path.join(base, 'catfix_pkg'), os.path.join(base, 'catfix_cache')]
        self.report_dir = os.path.join(self.out_dir, REPORT_NAME)

    def __repr__(self):
        where = ('MÁY ANH TRUNG (code chạy thẳng trên máy anh, đọc/ghi file trong thư mục của anh)' if self.mode == 'local'
                 else 'MÁY CHỦ CHATGPT (file anh tải lên trong %s)' % self.in_dir)
        return 'Session – %s\n  file vào : %s\n  file ra  : %s\n  báo cáo  : %s' % (where, self.in_dir, self.out_dir, self.report_dir)

    # ------------------------------------------------------------ tìm file
    def _files(self, top, skip):
        for dp, dn, fn in os.walk(top):
            dn[:] = sorted(d for d in dn if not any(_under(os.path.join(dp, d), s) for s in skip))
            for f in sorted(fn):
                yield os.path.join(dp, f)

    def src(self, name):
        """đường dẫn file vào có tên `name` (tìm trong thư mục vào và các thư mục con)."""
        hits = [p for p in self._files(self.in_dir, self.skip) if nfc(os.path.basename(p)) == nfc(name)]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise FileNotFoundError('Không thấy file vào %r trong %s%s' % (
                name, self.in_dir, '' if self.mode == 'local' else ' – anh cần tải file này lên (đính kèm vào cuộc trò chuyện)'))
        raise ValueError('Thấy %d file cùng tên %r: %s – dùng đúng một file' % (len(hits), name, hits))

    def _mirror(self, name, rename=None, sub=None):
        s = self.src(name)
        rel = os.path.relpath(os.path.dirname(s), self.in_dir)
        d = self.out_dir if rel in ('.', '') else os.path.join(self.out_dir, rel)
        if sub:
            d = os.path.join(d, sub)
        return s, os.path.join(d, rename or os.path.basename(s))

    def dst(self, name, rename=None, sub=None):
        """file ra: cùng tên (hoặc `rename`), trong thư mục ra, cùng thư mục con với file vào (+ `sub`)."""
        s, out = self._mirror(name, rename, sub)
        if same_file(out, s) or (self.mode == 'local' and _under(out, self.in_dir)):
            raise ValueError('Đường dẫn ra trùng / nằm trong thư mục vào: %s' % out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        return out

    def result(self, name, sub=None):
        """file ĐÃ SỬA ở nhóm trước (vd G02 dùng file ra của G01)."""
        s, out = self._mirror(name, None, sub)
        if os.path.isfile(out):
            return out
        if self.mode == 'sandbox':
            print('Chú ý: không có %s trong phiên này -> dùng file anh tải lên %s (phải là file ĐÃ SỬA của nhóm trước)' % (out, s))
            return s
        raise FileNotFoundError('Chưa có file đã sửa %s – nhóm trước chưa làm xong?' % out)

    def report(self, name):
        os.makedirs(self.report_dir, exist_ok=True)
        return os.path.join(self.report_dir, name)

    def check_inputs(self, names):
        """in đường dẫn từng file vào; trả False nếu thiếu file nào."""
        ok = True
        for n in names:
            try:
                print('  CÓ    %s' % self.src(n))
            except Exception as e:
                ok = False
                print('  THIẾU %s – %s' % (n, e))
        return ok

    # ------------------------------------------------------------ Job, tiến độ
    def job(self, name, rename=None, sub=None, src=None, backend=None):
        """Job(file vào, file ra) – nhật ký .log.json lưu vào thư mục _BAO CAO."""
        from .recipes import Job
        s = src or self.src(name)
        d = self.dst(name, rename=rename, sub=sub)
        log = (sub + ' - ' if sub else '') + os.path.basename(d) + '.log.json'      # G01 và G02 không ghi đè nhật ký của nhau
        return Job(s, d, backend=backend, log_path=self.report(log))

    def progress(self, group, status, note=''):
        """ghi 1 dòng vào _BAO CAO/TIEN DO.md (để làm tiếp nếu cuộc trò chuyện bị ngắt)."""
        p = self.report('TIEN DO.md')
        new = not os.path.exists(p)
        with open(p, 'a', encoding='utf-8') as f:
            if new:
                f.write('# TIẾN ĐỘ SỬA CATALOGUE (ChatGPT)\n\n| Thời điểm | Nhóm | Trạng thái | Ghi chú |\n|---|---|---|---|\n')
            f.write('| %s | %s | %s | %s |\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), group, status,
                                              str(note).replace('|', '/').replace('\n', ' ')))
        return p

    def read_progress(self):
        p = os.path.join(self.report_dir, 'TIEN DO.md')
        if not os.path.exists(p):
            return '(chưa có tiến độ – bắt đầu từ đầu)'
        with open(p, encoding='utf-8') as f:
            return f.read()
