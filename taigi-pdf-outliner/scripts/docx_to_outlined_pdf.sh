#!/usr/bin/env bash
# docx → outlined PDF via Microsoft Word (AppleScript) + Ghostscript -dNoOutputFonts.
#
# Usage: docx_to_outlined_pdf.sh <input.docx> <output.pdf> [--keep-intermediate]
#   --keep-intermediate also writes <output>_word.pdf (Word's export, fonts embedded, searchable)
#
# LibreOffice is deliberately NOT used: its PDF export renders every GenYoMin2 TW
# glyph as the .notdef box (verified with LibreOffice 26.2 on macOS).
set -euo pipefail

[[ $# -ge 2 ]] || { echo "usage: $0 <input.docx> <output.pdf> [--keep-intermediate]" >&2; exit 1; }
[[ -f "$1" ]] || { echo "missing: $1" >&2; exit 1; }
in_docx="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
out_pdf="$2"
keep="${3:-}"
command -v gs >/dev/null || { echo "ghostscript not found (brew install ghostscript)" >&2; exit 1; }

# Word is sandboxed: it can always read and write inside its own container.
WORK="${HOME}/Library/Containers/com.microsoft.Word/Data/Documents/.outliner_stage"
mkdir -p "$WORK"
base="$(basename "${in_docx%.docx}")"
tmp_docx="${WORK}/${base}.docx"
tmp_pdf="${WORK}/${base}.pdf"
cp "$in_docx" "$tmp_docx"
rm -f "$tmp_pdf"

osascript - "$tmp_docx" "$tmp_pdf" <<'OSA'
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
[[ -s "$tmp_pdf" ]] || { echo "Word did not produce $tmp_pdf" >&2; exit 1; }

mkdir -p "$(dirname "$out_pdf")"
gs -q -o "$out_pdf" -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dNoOutputFonts "$tmp_pdf"
if [[ "$keep" == "--keep-intermediate" ]]; then
    cp "$tmp_pdf" "${out_pdf%.pdf}_word.pdf"
fi
rm -f "$tmp_docx" "$tmp_pdf"
echo "outlined → $out_pdf"
