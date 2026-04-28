---
name: taigi-docx-typography-expert
description: Manages complex line-breaking and typography rules in Microsoft Word (OpenXML) documents for Taigi mixed-script (Hanji + Roman Orthography) text. Use when you need to prevent hyphens from breaking across lines or handle East Asian Kinsoku rules.
---

# Taigi DOCX Typography Expert

This skill provides precise solutions for controlling line-breaking and typography in Taigi Microsoft Word `.docx` documents via direct OpenXML manipulation.

## Core Principles

1.  **Preserve Encoding:** Never replace standard ASCII characters (like hyphens) with non-standard Unicode characters (like `U+2011`) if searchability or copy-paste integrity is a requirement.
2.  **Use Native Tags:** Prefer native OpenXML elements over invisible Unicode "glue" characters (like `U+2060` Word Joiner).
3.  **Respect Style Inheritance:** Ensure layout properties are applied at the correct level (Settings vs. Styles vs. Paragraph Properties).

## Hyphenation Control (Roman Orthography)

To prevent a word containing a hyphen (e.g., `chi̍t-ê`) from breaking at the end of a line:

*   **DON'T:** Use the ASCII hyphen `-` (`U+002D`).
*   **DON'T:** Use the Non-Breaking Hyphen `‑` (`U+2011`) unless you don't care about copy-paste.
*   **DO:** Use the native OpenXML `<w:noBreakHyphen/>` element.

### Implementation Pattern

Split the text run `<w:r>` into three parts.
For a run like `<w:r><w:t>m̄-koh</w:t></w:r>`:

1.  A run containing the first part: `<w:r><w:rPr>...</w:rPr><w:t>m̄</w:t></w:r>`
2.  A run containing the non-breaking hyphen: `<w:r><w:noBreakHyphen/></w:r>`
3.  A run containing the second part: `<w:r><w:t>koh</w:t></w:r>`

## Kinsoku (East Asian Line-Breaking)

To ensure punctuation follows standard East Asian rules (Kinsoku):

1.  **Global Settings:** Ensure `word/settings.xml` has `<w:strictFirstAndLastChars w:val="1"/>`.
2.  **Paragraph Properties:** Every paragraph (`<w:p>`) must have `<w:kinsoku w:val="1"/>` and `<w:wordWrap w:val="1"/>` in its `<w:pPr>` block.

## Interaction with Han-Lo Text

When processing Taigi Han-Lo text:
*   The `zh-TW` language tag should be applied to the `w:eastAsia` attribute in `<w:lang>`.
*   Ensure that the word-wrapping engine is enabled to prevent Word from breaking lines character-by-character (ignoring Latin word boundaries).
