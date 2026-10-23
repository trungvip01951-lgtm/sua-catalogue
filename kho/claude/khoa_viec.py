"""Khóa VIỆC theo phiên (bổ sung cho khóa catalogue của cat.py claim).
Dùng khi việc không nằm trong 25 catalogue gốc (PDF hãng mới, nhóm thiết kế lại, thư mục work, tệp quy tắc...).
  python3 claude/khoa_viec.py xem
  python3 claude/khoa_viec.py nhan <TEN_VIEC> <MA_PHIEN> "<phạm vi: tệp/trang/hãng>"
  python3 claude/khoa_viec.py nha  <TEN_VIEC> <MA_PHIEN> "<ghi chú kết quả>"
Quy ước tên: NHOM_HANG[_PHAN], ví dụ WC_PEROTAC, WC_REDPUMP_P3-5, CM_AQUARIS, QUYTAC_CLAUDE.
Khóa là một tệp tạo độc quyền (không ghi đè được). Khóa của phiên khác: KHÔNG tự chiếm, kể cả khi đã cũ; báo anh Trung.
Nhả khóa = đổi tên tệp sang khoa/da_nha/ (không cần quyền xóa).
"""
import json, os, re, sys, time
from pathlib import Path

D = Path(os.environ.get('CLAUDE_KHOA_DIR', Path(__file__).resolve().parent / 'khoa'))


def ten(s):
    t = re.sub(r'[^A-Za-z0-9_-]+', '_', s.strip()).strip('_').upper()
    if not t:
        sys.exit('Thiếu tên việc')
    return t


def now():
    return time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())


def xem():
    D.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(p.read_text(encoding='utf8')) for p in sorted(D.glob('*.lock'))]
    if not rows:
        print('Không có khóa việc nào đang giữ.')
    for r in rows:
        print(f"{r['viec']} | phiên {r['phien']} | từ {r['luc']} | {r['pham_vi']}")
    return rows


def nhan(viec, phien, pham_vi):
    D.mkdir(parents=True, exist_ok=True)
    p = D / (ten(viec) + '.lock')
    try:
        fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        r = json.loads(p.read_text(encoding='utf8'))
        sys.exit(f"ĐÃ CÓ PHIÊN GIỮ: {r['viec']} | phiên {r['phien']} | từ {r['luc']} | {r['pham_vi']} -> KHÔNG làm việc này, chọn việc khác")
    with os.fdopen(fd, 'w', encoding='utf8') as f:
        json.dump({'viec': ten(viec), 'phien': phien, 'luc': now(), 'pham_vi': pham_vi}, f, ensure_ascii=False)
    r = json.loads(p.read_text(encoding='utf8'))
    if r['phien'] != phien:
        sys.exit('Đọc lại khóa không khớp phiên -> dừng')
    print(f"ĐÃ NHẬN KHÓA {r['viec']} cho phiên {phien}")


def nha(viec, phien, ghi_chu):
    p = D / (ten(viec) + '.lock')
    if not p.exists():
        sys.exit('Không có khóa này')
    r = json.loads(p.read_text(encoding='utf8'))
    if r['phien'] != phien:
        sys.exit(f"KHÓA KHÔNG THUỘC PHIÊN NÀY (đang của {r['phien']}) -> không nhả")
    r.update({'nha_luc': now(), 'ghi_chu': ghi_chu})
    (D / 'da_nha').mkdir(exist_ok=True)
    q = D / 'da_nha' / f"{ten(viec)}.{r['nha_luc']}.json"
    q.write_text(json.dumps(r, ensure_ascii=False), encoding='utf8')
    os.replace(p, D / 'da_nha' / f"{ten(viec)}.{r['nha_luc']}.lock")
    print(f"ĐÃ NHẢ KHÓA {r['viec']}")


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['xem']:
        xem()
    elif a[:1] == ['nhan'] and len(a) == 4:
        nhan(a[1], a[2], a[3])
    elif a[:1] == ['nha'] and len(a) == 4:
        nha(a[1], a[2], a[3])
    else:
        sys.exit(__doc__)
