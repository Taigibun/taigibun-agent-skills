---
name: taigi-pdf-outliner
description: Produces a font-independent PDF from a typeset Taigi .docx (GenYoMin2 TW) by exporting through Microsoft Word via AppleScript and then outlining every glyph into vector paths with Ghostscript -dNoOutputFonts. Use whenever a Taigi document must be distributed or printed as PDF, whenever a PDF of GenYoMin text shows boxes or tofu, and whenever someone proposes LibreOffice or soffice for the PDF step, which must not be used with this font.
---

# Taigi PDF Outliner

Final publishing step: `.docx` → PDF → outlined PDF that renders identically everywhere, with no font installed on the reader's machine.

## Workflow

```bash
scripts/docx_to_outlined_pdf.sh 04_<title>_typeset.docx 05_<title>_outlined.pdf
```

The script does three things:

1. **DOCX → PDF with Microsoft Word.** Word is the renderer the docx typography targets (`<w:kinsoku>`, `<w:noBreakHyphen/>`, `strictFirstAndLastChars`), and its Quartz export embeds GenYoMin2 TW correctly. Word is sandboxed, so the docx is staged inside Word's container (`~/Library/Containers/com.microsoft.Word/Data/Documents/`) and Word writes the PDF next to it via `osascript` (`save as … file format format PDF`). The first run prompts for Automation permission (Terminal → Microsoft Word).
2. **Outline with Ghostscript.**
   ```bash
   gs -q -o out.pdf -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dNoOutputFonts in.pdf
   ```
   All text becomes vector paths. Visual fidelity is exact; text search and copy are lost by design.
3. Cleans up the staged files.

## Always look at a rendered page

`pdffonts` and `pdftotext` cannot detect the failure below: the ToUnicode map is intact while every glyph is a box. Render one page and view it:

```bash
pdftoppm -png -r 60 -f 3 -l 3 out.pdf /tmp/page     # then open /tmp/page-3.png
```

## Never LibreOffice for this font

`soffice --headless --convert-to pdf` emits the `.notdef` box glyph for **every** GenYoMin2 TW character (verified with LibreOffice 26.2 on macOS; PingFang TC, Songti TC and Arial Unicode MS export fine, so it is font-specific). Ghostscript then faithfully outlines the boxes, so the result passes every "fonts embedded / outlined" check and is unreadable. LibreOffice remains fine for producing `.odt` copies of the docx.

## Fallbacks when Word automation is unavailable

Typst or XeLaTeX with the GenYoMin2 TW faces, then the same Ghostscript pass. Not LibreOffice.

## Dependencies

- Microsoft Word for Mac (Automation permission on first run)
- Ghostscript: `brew install ghostscript`
- Poppler for the rendering check: `brew install poppler`
