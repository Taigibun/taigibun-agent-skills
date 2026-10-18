---
name: taigi-document-typesetter
description: Typesets Taigi Markdown or text into .docx (and .odt) with the GenYoMin2 TW font, the correct pandoc flags for POJ text (smart punctuation OFF), a patched reference.docx, and per-run font, language and kinsoku patching. Use whenever converting Taigi Markdown to Word, choosing pandoc options for text that contains POJ hyphens or `--` enclitics, building a reference.docx, or applying GenYoMin fonts to an existing .docx.
---

# Taigi Document Typesetter

Markdown → `.docx` that Microsoft Word lays out correctly for mixed Hanji + Roman Orthography text.

## The pandoc command

```bash
pandoc in.md -f markdown-smart-raw_tex -t docx --reference-doc=assets/reference_genyo.docx -o tmp.docx
python3 scripts/apply_fonts_to_docx.py tmp.docx out.docx
```

- **`-smart` is mandatory.** Pandoc's `smart` extension is on by default and turns `--` into an en dash, `---` into an em dash, `...` into an ellipsis and straight quotes into curly ones. POJ depends on the literal double hyphen for neutral-tone enclitics (`--ê`, `--a`, `--lah`) and on literal hyphens inside words. Never pass `--smart`, and never use a bare `-f markdown`.
- **`-raw_tex`** keeps backslashes and `\…` sequences in the source as text instead of TeX.
- YAML front matter `title:` and `author:` map to Word's built-in Title and Author styles. Emit them from the structuring step instead of a duplicate `#` heading.
- Verse belongs in pandoc line blocks (`| line`): one paragraph with soft line breaks instead of N paragraphs.

## Building the reference document

```bash
pandoc -o assets/reference.docx --print-default-data-file reference.docx
python3 scripts/patch_reference_docx.py assets/reference.docx assets/reference_genyo.docx
```

`patch_reference_docx.py` strips every `<w:rFonts>` and `<w:lang>` from `styles.xml`, then sets on **every** style and on `rPrDefault`: GenYoMin2 TW for ascii, hAnsi, eastAsia and cs; `<w:lang w:val="en-US" w:eastAsia="zh-TW"/>`; bold via `<w:b/>` on `Heading*` and `Title`; paragraph spacing (body 6pt before/after at 1.5 lines, headings 18pt/12pt); and `<w:strictFirstAndLastChars w:val="1"/>` in `settings.xml`. Without explicit per-style fonts, styles that carry no `<w:rPr>` (pandoc's `BodyText`) fall back to Calibri in some renderers. Called without arguments it uses `<script dir>/../assets/reference.docx` → `reference_genyo.docx`.

## Patching the output docx

`apply_fonts_to_docx.py in.docx out.docx` rewrites `document.xml`, `styles.xml` and `settings.xml`:

- explicit `<w:rFonts>` and `<w:lang>` on every run, including the bare runs pandoc emits with only `w:hint="eastAsia"`;
- `<w:kinsoku w:val="1"/><w:wordWrap w:val="1"/>` on every paragraph and on `Normal`, `BodyText`, `FirstParagraph` and `pPrDefault`;
- each run split at ASCII hyphens with a `<w:noBreakHyphen/>` run between the segments, so `chi̍t-ê` never breaks across lines while the text stays plain ASCII for search and copy (details in `taigi-docx-typography-expert`);
- an empty paragraph after each body paragraph, not after headings or the title block, for visual spacing.

Idempotent: a re-run strips its own earlier injections first.

## Font facts

- The family name is `GenYoMin2 TW`. Request bold with `<w:b/>`, never with a weight-suffixed face name; LibreOffice substitutes unknown face names.
- Source: https://github.com/ButTaiwan/genyo-font, release v2.100, `GenYoMin2-ttc.zip`, SIL OFL 1.1. Install the `.ttc` files into `~/Library/Fonts/` so Word finds them.
- Body: GenYoMin2 TW R. Headings: GenYoMin2 TW B, reached through bold.

## ODT copies

LibreOffice is fine for `.odt`:

```bash
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to odt out.docx
```

It is **not** fine for PDF of this font (every glyph becomes a box). Use `taigi-pdf-outliner` for PDF.

## Bundled scripts

- `scripts/patch_reference_docx.py [reference.docx] [reference_genyo.docx]`
- `scripts/apply_fonts_to_docx.py <in.docx> <out.docx>`

Both need only the Python standard library. The full stage-4 wrapper lives in `taigi-doc-pipeline/scripts/04_typeset.sh`.
