"""Lớp bọc đường dẫn cho phiên Claude: chạy tools/catalogue.py NGUYÊN BẢN,
chỉ dịch đường dẫn Windows trong manifest sang thư mục mount. Không sửa công cụ gốc.
Dùng:  python claude/cat.py health|status|context --file ...|claim ...  (tham số y như tools/catalogue.py)
"""
import importlib.util, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MNT = Path(os.environ.get('CLAUDE_MNT', Path.home() / 'mnt'))
CFG = json.loads((HERE / 'paths_linux.json').read_text(encoding='utf8'))


def to_local(p):
    if not isinstance(p, str):
        return p
    for win, rel in sorted(CFG['map'].items(), key=lambda kv: -len(kv[0])):
        if p.lower().startswith(win.lower()):
            rest = p[len(win):].replace('\\', '/').lstrip('/')
            return str(MNT / rel / rest) if rest else str(MNT / rel)
    return p


def main():
    os.environ.setdefault('CATFIX_ROOT', str(MNT / CFG['catfix_env']['CATFIX_ROOT']))
    spec = importlib.util.spec_from_file_location('catalogue_orig', ROOT / 'tools' / 'catalogue.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules['catalogue_orig'] = mod
    spec.loader.exec_module(mod)
    orig = mod.manifest

    def manifest():
        m = orig()
        m['paths'] = {k: to_local(v) for k, v in m['paths'].items()}
        return m
    mod.manifest = manifest
    return mod.main()


if __name__ == '__main__':
    sys.exit(main())
