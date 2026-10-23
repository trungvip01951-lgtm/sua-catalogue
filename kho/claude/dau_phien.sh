#!/bin/bash
# Đầu phiên Claude: cài môi trường riêng (ngoài kho), chạy BƯỚC 0 = 43 bài kiểm catfix trên BẢN SAO, rồi health.
# Dùng:  bash "$HOME/mnt/Sửa catalogue/claude/dau_phien.sh" env    (lần 1: cài, ~1 phút)
#        bash "$HOME/mnt/Sửa catalogue/claude/dau_phien.sh" test   (lần 2: 43 bài kiểm + health, ~1 phút)
# Không sửa catfix, không ghi gì vào kho ngoài claude/BUOC0_MOI_NHAT.txt.
K="$HOME/mnt/Sửa catalogue"; PY="$HOME/cfenv/bin/python"
case "$1" in
env)
  [ -x "$PY" ] || python3 -m venv --system-site-packages "$HOME/cfenv" || exit 1
  # 08/10: cài OFFLINE từ vendor/wheels (lưu sẵn trong kho, ~156 MB; tệp >25 MB tách .partNN) → vài giây, không phụ thuộc mạng chậm. Thiếu thì mới tải mạng.
  if ! "$PY" -c "import pymupdf,scipy,cv2,pikepdf,pytesseract,fontTools" 2>/dev/null; then
    WH="$K/vendor/wheels"; TW="$HOME/cfwheels"
    if [ -d "$WH" ]; then mkdir -p "$TW"; cp "$WH"/*.whl "$TW"/ 2>/dev/null
      for p in "$WH"/*.whl.part00; do [ -e "$p" ] || continue; b=$(basename "$p" .part00); cat "$WH/$b".part* > "$TW/$b"; done
      "$HOME/cfenv/bin/pip" install -q --no-input --no-index --find-links "$TW" pymupdf scipy opencv-python-headless pytesseract fonttools pikepdf 2>&1 | tail -2; fi
    "$PY" -c "import pymupdf,scipy,cv2,pikepdf,pytesseract,fontTools" 2>/dev/null || \
      "$HOME/cfenv/bin/pip" install -q --no-input pymupdf scipy opencv-python-headless pytesseract fonttools pikepdf 2>&1 | tail -2
  fi
  "$PY" -c "import pymupdf,scipy,cv2,pikepdf,numpy,sys;print('MOI TRUONG OK py',sys.version.split()[0],'pymupdf',pymupdf.__version__,'scipy',scipy.__version__,'cv2',cv2.__version__,'pikepdf',pikepdf.__version__,'numpy',numpy.__version__)" || { echo "MOI TRUONG THIEU - DUNG"; exit 2; }
  which tesseract pdftoppm qpdf ;;
test)
  rm -rf "$HOME/cftest"; mkdir -p "$HOME/cftest" && cp -r "$K/vendor/catfix_original/GOI_SUA_CATALOGUE_CHATGPT" "$HOME/cftest/pkg" || exit 1
  cd "$HOME/cftest/pkg" && "$PY" -B -X utf8 -m catfix.env > "$HOME/cftest/env.txt" 2>&1
  timeout 150 "$PY" -B -X utf8 tests/run_tests.py > "$HOME/cftest/out.txt" 2>&1
  T=$(grep -m1 "TỔNG KẾT" "$HOME/cftest/out.txt"); D=$(grep -c "ĐƯỢC" "$HOME/cftest/env.txt")
  H=$(cd "$K" && "$PY" -B -X utf8 claude/cat.py health 2>&1 | grep '"result"')
  V=$("$PY" -c "import pymupdf,scipy,cv2,pikepdf,sys;print('py',sys.version.split()[0],'pymupdf',pymupdf.__version__,'scipy',scipy.__version__,'cv2',cv2.__version__,'pikepdf',pikepdf.__version__)")
  { echo "UTC $(date -u +%Y%m%dT%H%M%SZ) | Claude/Linux | $V"; echo "Môi trường ĐƯỢC: $D/4"; echo "$T"; echo "health: $H"; } | tee "$K/claude/BUOC0_MOI_NHAT.txt"
  grep -nE "CHƯA ĐẠT|\[LỖI\]|Traceback" "$HOME/cftest/out.txt" | head
  echo "$T" | grep -q "43/43 ĐẠT" && [ "$D" = "4" ] || { echo "CHUA 43/43 HOAC THIEU MOI TRUONG - KHONG SUA CATALOGUE"; exit 2; } ;;
*) echo "dùng: env | test" ;;
esac
