#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-v0.1.0}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/output/releases"
ARCHIVE="$OUT_DIR/ai-color-workspace-${VERSION}-source.zip"

mkdir -p "$OUT_DIR"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: release package must be built from a git checkout" >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "error: working tree is not clean; commit release contents before packaging" >&2
  exit 1
fi

git archive \
  --format=zip \
  --output="$ARCHIVE" \
  --prefix="ai-color-workspace-${VERSION}/" \
  HEAD

echo "$ARCHIVE"
