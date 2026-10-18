---
name: taigi-docx-typography-expert
description: Controls line breaking and typography in Microsoft Word (OpenXML) documents for Taigi mixed-script text (Hanji + Roman Orthography): native non-breaking hyphens via <w:noBreakHyphen/>, East Asian kinsoku rules, run splitting, settings.xml element order, and the traps of custom line-break character lists. Use whenever POJ hyphens break at line ends, punctuation lands at the start of a line, or any OpenXML patching of a Taigi .docx is planned.
---

# Taigi DOCX Typography Expert

Precise solutions for line breaking in Taigi `.docx` files through direct OpenXML manipulation. Verified target: Microsoft Word for Mac (Microsoft 365) on macOS.

## Core principles

1. **Preserve encoding.** Never swap ASCII hyphens for `U+2011` or glue words with `U+2060` when search and copy-paste must keep working.
2. **Use native tags.** Prefer OpenXML elements over invisible Unicode characters.
3. **Respect the property hierarchy.** Settings vs. styles vs. paragraph properties vs. run properties; put each rule at the level Word reads it from.

## Hyphenation control (Roman Orthography)

To stop `chi̍t-ê` or `m̄-koh` from breaking at the hyphen:

- **DON'T** leave the ASCII hyphen `-` (`U+002D`) alone; Word breaks after it.
- **DON'T** use the non-breaking hyphen `‑` (`U+2011`) unless copy-paste fidelity is irrelevant.
- **DO** emit the native `<w:noBreakHyphen/>` element.

### Implementation pattern

Split the run at every hyphen. For `<w:r><w:rPr>…</w:rPr><w:t>m̄-koh</w:t></w:r>`:

```xml
<w:r><w:rPr>…</w:rPr><w:t>m̄</w:t></w:r>
<w:r><w:rPr>…</w:rPr><w:noBreakHyphen/></w:r>
<w:r><w:rPr>…</w:rPr><w:t>koh</w:t></w:r>
```

- Copy the original `<w:rPr>` into every segment run **and** the hyphen run, or fonts and language reset to the style default.
- Remove the empty runs produced by a hyphen at a run edge or by consecutive hyphens (`--ê`).
- Make the pass idempotent: strip earlier injected `<w:rFonts>`, `<w:lang>`, `<w:kinsoku>` and `<w:wordWrap>` before injecting again.

## Kinsoku (East Asian line breaking)

1. **Settings:** `word/settings.xml` carries `<w:strictFirstAndLastChars w:val="1"/>`.
2. **Paragraphs:** every `<w:p>` carries `<w:kinsoku w:val="1"/>` and `<w:wordWrap w:val="1"/>` in its `<w:pPr>`; set the same on `Normal`, `BodyText`, `FirstParagraph` and `pPrDefault` in `styles.xml`, because pandoc assigns those styles explicitly.
3. **Language:** `<w:lang w:val="en-US" w:eastAsia="zh-TW"/>` on every run. OpenXML looks up line-break rules by the script-appropriate language, so Hanji use the zh-TW rules while Latin runs use en-US.

## Do NOT define custom line-break character lists

Do not add `<w:noLineBreaksAfter>` or `<w:noLineBreaksBefore>` for `zh-TW` unless you list the **entire** punctuation set. Word treats a custom list as a replacement for its built-in dictionary: defining a single character (for example the hyphen) silently disables the standard rules for `，。」` and everything else. `strictFirstAndLastChars` plus the per-paragraph `kinsoku` flag is sufficient for Hanji punctuation; the hyphen is handled by `<w:noBreakHyphen/>`.

## Element order traps (schema)

OpenXML types are ordered sequences. Word discards or rejects out-of-order children.

- In `settings.xml`, `<w:strictFirstAndLastChars/>` (and any `noLineBreaks*`) must come **before** `w:savePreviewPicture`, `w:rsids`, `m:mathPr`, `w:themeFontLang`, `w:clrSchemeMapping`, `w:doNotValidateBeforeSave`, `w:decimalSymbol`, `w:listSeparator` and `w:smartTagType`.
- In `<w:pPr>`, `<w:kinsoku/>` and `<w:wordWrap/>` come **before** `<w:spacing>`, `<w:ind>`, `<w:jc>` and `<w:rPr>`.

## Renderer notes

- Microsoft Word for Mac honours all of the above and embeds GenYoMin2 TW correctly on PDF export.
- LibreOffice ignores Latin characters in en-US kinsoku lists but scans the zh-TW list against every character in the document. It still cannot export GenYoMin2 TW to PDF (boxes), so use it only for `.odt` copies.

## Interaction with Han-Lo text

Keep the word-wrapping engine on (`<w:wordWrap w:val="1"/>`); otherwise Word breaks Latin words character by character inside Han-Lo paragraphs. Spacing and hyphen rules for the text itself belong to `taigi-han-lo-formatter`; this skill only concerns the rendered layout. `taigi-document-typesetter/scripts/apply_fonts_to_docx.py` implements everything above.
