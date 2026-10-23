# Niêm phong lại các tệp quy tắc/công cụ (mandatory_controls trong manifest.json). Dùng: python -B -X utf8 tools/niem_phong.py "<lý do>"
"""Chạy đúng nhánh --seal-controls của tools/refresh_index.py (không chụp lại state/catalogues.json).
Dùng hàm gốc seal/fresh_json/replace_state; chỉ bỏ phần snapshot vì manifest trỏ đường Windows."""
import sys, json
from pathlib import Path
from datetime import datetime, timezone
import uuid
K = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(K/'tools'))
import refresh_index as ri
import catalogue as project
m = project.manifest()
control = ri.seal(m)
tag = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
prior = ri.ROOT/'state/control_manifest.json'
ri.fresh_json(ri.ROOT/'history'/('controls-before-'+tag+'.json'), json.loads(prior.read_text(encoding='utf8')))
ri.fresh_json(ri.ROOT/'history'/('controls-'+tag+'.json'), dict(control, actor='ROOT', reason=sys.argv[1]))
ri.replace_state(prior, control)
print(json.dumps({'sealed': len(control['files']), 'tag': tag, 'seal_sha256': project.digest(prior)}, ensure_ascii=False))
