#!/usr/bin/env bash
# Stage 4: 03_*_structured.md → 04_*_typeset.docx
# pandoc with a GenYoMin2 TW reference.docx, then per-run font/kinsoku patching.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
DST_DIR="${ROOT}/doc_result"
ASSETS="${ROOT}/assets"
REF_BASE="${ASSETS}/reference.docx"
REF="${ASSETS}/reference_genyo.docx"

# The two docx helpers live next to this script in a project checkout, or in
# the sibling taigi-document-typesetter skill when run from the skills repo.
find_helper() {
    local name="$1" cand
    for cand in "${HERE}/${name}" "${HERE}/../../taigi-document-typesetter/scripts/${name}"; do
        [[ -f "$cand" ]] && { echo "$cand"; return 0; }
    done
    echo "missing helper ${name}: copy it from taigi-document-typesetter/scripts/ into ${HERE}/" >&2
    return 1
}
PATCH_REF="$(find_helper patch_reference_docx.py)"
APPLY_FONTS="$(find_helper apply_fonts_to_docx.py)"

mkdir -p "$ASSETS"
# pandoc's stock reference.docx is the base that patch_reference_docx.py edits.
[[ -f "$REF_BASE" ]] || pandoc -o "$REF_BASE" --print-default-data-file reference.docx
# Build the GenYoMin2 TW reference.docx if missing/stale
if [[ ! -f "$REF" || "$PATCH_REF" -nt "$REF" ]]; then
    python3 "$PATCH_REF" "$REF_BASE" "$REF"
fi

if [[ $# -ge 1 ]]; then
    titles=("$@")
else
    titles=()
    while IFS= read -r f; do
        b="$(basename "$f")"
        b="${b#03_}"
        b="${b%_structured.md}"
        titles+=("$b")
    done < <(find "$DST_DIR" -maxdepth 1 -name '03_*_structured.md')
fi

for title in "${titles[@]}"; do
    in="${DST_DIR}/03_${title}_structured.md"
    out="${DST_DIR}/04_${title}_typeset.docx"
    tmp="${DST_DIR}/.04_${title}_typeset.raw.docx"
    [[ -f "$in" ]] || { echo "missing: $in" >&2; exit 1; }
    # -smart disables: "--" → en-dash, "---" → em-dash, "..." → ellipsis, smart quotes.
    # POJ depends on literal "--" (neutral-tone enclitics: --ê, --a, --lah), so smart MUST be off.
    # -raw_tex keeps backslash sequences as text.
    pandoc "$in" -f markdown-smart-raw_tex -t docx --reference-doc="$REF" -o "$tmp"
    python3 "$APPLY_FONTS" "$tmp" "$out"
    rm -f "$tmp"
    echo "stage 4 → $out"
done
