import os, sys, glob, zipfile, subprocess, tempfile
GOI = [g for g in (r'C:\Users\H2\Desktop\Catalog Sua\GOI CHATGPT 02-10-2026',        # máy anh (Windows)
                   '/mnt/c/Users/H2/Desktop/Catalog Sua/GOI CHATGPT 02-10-2026')      # máy anh (WSL)
       if os.path.isfile(os.path.join(g, 'GOI_SUA_CATALOGUE_CHATGPT.zip'))]
if GOI:                                            # (1) code chạy thẳng trên máy anh Trung
    ZIP = os.path.join(GOI[0], 'GOI_SUA_CATALOGUE_CHATGPT.zip')
    WORK = os.path.join(tempfile.gettempdir(), 'catfix_work')
else:                                              # (2) code chạy trên máy chủ của bạn
    z = sorted(glob.glob('/mnt/data/**/GOI_SUA_CATALOGUE_CHATGPT*.zip', recursive=True))
    assert z, 'Chưa có GOI_SUA_CATALOGUE_CHATGPT.zip trong /mnt/data – lấy từ máy anh hoặc nhờ anh tải lên'
    ZIP, WORK = z[-1], '/mnt/data'
zipfile.ZipFile(ZIP).extractall(os.path.join(WORK, 'catfix_pkg'))
PKG = os.path.join(WORK, 'catfix_pkg', 'GOI_SUA_CATALOGUE_CHATGPT')          # thư mục chứa catfix/
sys.path.insert(0, PKG); os.chdir(PKG)
os.environ.update(CATFIX_CACHE=os.path.join(WORK, 'catfix_cache'), PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
def sh(*args):                                     # chạy lệnh python trong thư mục gói, in kết quả
    r = subprocess.run([sys.executable] + list(args), cwd=PKG, capture_output=True, encoding='utf-8', errors='replace')
    print(r.stdout[-30000:], r.stderr[-5000:])
sh('-m', 'catfix.env')
from catfix.session import Session
S = Session(); print(S)                            # chỗ lấy file vào / lưu file ra / lưu báo cáo
print(S.read_progress())                           # nhóm nào đã xong (khi làm tiếp)