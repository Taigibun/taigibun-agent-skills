#!/usr/bin/env bash
# Stage 1: extract .doc → 01_<title>_raw.txt
# Uses macOS textutil to convert binary .doc into UTF-8 plain text.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${ROOT}/doc_original"
DST_DIR="${ROOT}/doc_result"
mkdir -p "$DST_DIR"

if [[ $# -ge 1 ]]; then
    titles=("$@")
else
    titles=()
    while IFS= read -r f; do titles+=("$(basename "${f%.doc}")"); done < <(find "$SRC_DIR" -maxdepth 1 -name '*.doc')
fi

for title in "${titles[@]}"; do
    in="${SRC_DIR}/${title}.doc"
    out="${DST_DIR}/01_${title}_raw.txt"
    [[ -f "$in" ]] || { echo "missing: $in" >&2; exit 1; }
    textutil -convert txt -encoding UTF-8 -output "$out" "$in"
    echo "stage 1 → $out"
done
