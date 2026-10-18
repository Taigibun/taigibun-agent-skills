#!/usr/bin/env bash
# Master orchestrator — runs all 5 pipeline stages in order.
#
# Usage:
#   scripts/00_pipeline.sh                       # all .doc files in doc_original/
#   scripts/00_pipeline.sh "title-without-ext"   # one specific title
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ $# -ge 1 ]]; then
    titles=("$@")
else
    titles=()
    while IFS= read -r f; do
        titles+=("$(basename "${f%.doc}")")
    done < <(find "${ROOT}/doc_original" -maxdepth 1 -name '*.doc')
fi

for title in "${titles[@]}"; do
    echo "▶ pipeline: $title"
    "${ROOT}/scripts/01_extract.sh"   "$title"
    "${ROOT}/scripts/02_fix.sh"       "$title"
    "${ROOT}/scripts/03_structure.py" "$title"
    "${ROOT}/scripts/04_typeset.sh"   "$title"
    "${ROOT}/scripts/05_outline.sh"   "$title"
done
