#!/usr/bin/env bash
# Phase 2 rerun: shallow-clone 16 (vendor, tag) source trees to Desktop/vdb_src
# Purpose: dev-reviewer-level source excerpt extraction (one excerpt per probe case).
# Designed to run in background; writes progress to clone_progress.log.
set +e
DEST="/c/Users/11428/Desktop/vdb_src"
mkdir -p "$DEST"
LOG="$DEST/clone_progress.log"
: > "$LOG"

clone() {
  local vendor="$1" url="$2" tag="$3"
  local target="$DEST/$vendor/$tag"
  if [ -d "$target/.git" ]; then
    echo "[SKIP] $vendor/$tag (exists)" | tee -a "$LOG"
    return 0
  fi
  echo "[CLONE] $vendor $tag ..." | tee -a "$LOG"
  rm -rf "$target"
  if git clone --depth 1 --branch "$tag" "$url" "$target" >>"$LOG" 2>&1; then
    local sha; sha=$(git -C "$target" rev-parse --short HEAD 2>/dev/null)
    echo "[OK] $vendor/$tag $sha" | tee -a "$LOG"
  else
    echo "[FAIL] $vendor/$tag" | tee -a "$LOG"
  fi
}

MIL=https://github.com/milvus-io/milvus
QDR=https://github.com/qdrant/qdrant
WEA=https://github.com/weaviate/weaviate

for t in v2.3.22 v2.6.10 v2.6.12 v2.6.16 v2.6.17 v2.6.19 v3.0.0; do clone milvus "$MIL" "$t"; done
for t in v1.12.1 v1.17.1 v1.18.0 v1.18.1 v1.18.2 v1.18.3; do clone qdrant "$QDR" "$t"; done
for t in v1.37.4 v1.38.0 v1.38.2; do clone weaviate "$WEA" "$t"; done

echo "=== ALL DONE ===" | tee -a "$LOG"
echo "--- sizes ---" | tee -a "$LOG"
du -sh "$DEST"/*/* 2>/dev/null | tee -a "$LOG"
