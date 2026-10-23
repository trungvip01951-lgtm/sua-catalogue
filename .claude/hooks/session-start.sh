#!/bin/bash
# Phiên Claude đám mây: cài tesseract/qpdf, nối $HOME/mnt/Sửa catalogue → kho/, cài thư viện Python (claude/dau_phien.sh env).
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
KHO="$CLAUDE_PROJECT_DIR/kho"
if ! command -v tesseract >/dev/null || ! command -v qpdf >/dev/null; then
  apt-get install -y -qq tesseract-ocr tesseract-ocr-eng qpdf >/dev/null 2>&1 || \
    { apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq tesseract-ocr tesseract-ocr-eng qpdf >/dev/null 2>&1; }
fi
mkdir -p "$HOME/mnt" && ln -sfn "$KHO" "$HOME/mnt/Sửa catalogue"
bash "$KHO/claude/dau_phien.sh" env >&2
