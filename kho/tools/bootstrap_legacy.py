"""Chạy nguyên BƯỚC0 đã lưu; không cài, không sửa công cụ hoặc catalogue."""
from pathlib import Path
from datetime import datetime, timezone
import contextlib
import io
import json
import runpy
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    m = json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
    original = ROOT / m['bootstrap_original_copy']
    text = io.StringIO()
    with contextlib.redirect_stdout(text):
        namespace = runpy.run_path(str(original), run_name='catfix_bootstrap')
        from catfix.env import report
        _, verdict = report(verbose=False)
    print(text.getvalue())
    if not all(bool(ok) for _, ok in verdict):
        print('CHƯA ĐẠT: môi trường thiếu; không tự cài.')
        return 2
    if '--tests' in sys.argv:
        completed = subprocess.run([sys.executable, 'tests/run_tests.py'],
                     cwd=namespace['PKG'], capture_output=True, text=True,
                     encoding='utf8', errors='replace')
        print(completed.stdout)
        print(completed.stderr)
        evidence = text.getvalue() + '\n' + completed.stdout + '\n' + completed.stderr
        filename = 'bootstrap-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8] + '.txt'
        with (ROOT/'history'/filename).open('x', encoding='utf8') as stream:
            stream.write(evidence)
        if completed.returncode or 'TỔNG KẾT: 43/43 ĐẠT' not in completed.stdout:
            print('CHƯA ĐẠT: chưa có đủ43/43 từ lần chạy thật; dừng sửa catalogue.')
            return 2
    else:
        print('Chỉ khởi động/môi trường; 43 kiểm thử CHƯA CHẠY trong lệnh này. Dùng --tests khi tiếp tục phiên bị ngắt.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
