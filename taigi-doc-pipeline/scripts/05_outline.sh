#!/usr/bin/env bash
# Stage 5: 04_<title>_typeset.docx → 05_<title>_outlined.pdf
#
#   1. Microsoft Word (driven via AppleScript) renders the docx to PDF.
#      Word is the renderer the stage-4 typography targets (kinsoku rules,
#      <w:noBreakHyphen/>), and its Quartz PDF export embeds GenYoMin2 TW
#      correctly.
#      LibreOffice is deliberately NOT used here: its PDF export emits the
#      .notdef box glyph for every GenYoMin2 TW character (verified with
#      LibreOffice 26.2; other CJK fonts export fine), which silently
#      produces unreadable PDFs.
#   2. Ghostscript -dNoOutputFonts converts all text into vector paths so the
#      PDF renders identically everywhere without the font installed.
#
# Requirements: Microsoft Word for Mac (first run may ask for Automation
# permission: Terminal → Microsoft Word), Ghostscript (`brew install ghostscript`).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST_DIR="${ROOT}/doc_result"

# Word is sandboxed: it can always read and write inside its own container,
# so stage the docx there and let it write the PDF next to it.
WORK="${HOME}/Library/Containers/com.microsoft.Word/Data/Documents/.pipeline_stage5"
mkdir -p "$WORK"

if [[ $# -ge 1 ]]; then
    titles=("$@")
else
    titles=()
    while IFS= read -r f; do
        b="$(basename "$f")"
        b="${b#04_}"
        b="${b%_typeset.docx}"
        titles+=("$b")
    done < <(find "$DST_DIR" -maxdepth 1 -name '04_*_typeset.docx')
fi

word_to_pdf() {
    local in_docx="$1" out_pdf="$2"
    osascript - "$in_docx" "$out_pdf" <<'OSA'
on run argv
    set inPath to item 1 of argv
    set outPath to item 2 of argv
    with timeout of 900 seconds
        tell application "Microsoft Word"
            launch
            set display alerts to false
            open (POSIX file inPath)
            set theDoc to active document
            save as theDoc file name outPath file format format PDF
            close theDoc saving no
        end tell
    end timeout
end run
OSA
}

for title in "${titles[@]}"; do
    in="${DST_DIR}/04_${title}_typeset.docx"
    out="${DST_DIR}/05_${title}_outlined.pdf"
    [[ -f "$in" ]] || { echo "missing: $in" >&2; exit 1; }

    tmp_docx="${WORK}/${title}.docx"
    tmp_pdf="${WORK}/${title}.pdf"
    cp "$in" "$tmp_docx"
    rm -f "$tmp_pdf"

    word_to_pdf "$tmp_docx" "$tmp_pdf"
    [[ -s "$tmp_pdf" ]] || { echo "Word did not produce $tmp_pdf" >&2; exit 1; }

    gs -q -o "$out" -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dNoOutputFonts "$tmp_pdf"
    rm -f "$tmp_docx" "$tmp_pdf"
    echo "stage 5 → $out"
done
