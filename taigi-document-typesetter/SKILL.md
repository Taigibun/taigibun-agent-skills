---
name: taigi-document-typesetter
description: Typesets Taigi documents in DOCX and ODT formats. Applies Taigi-specific fonts (GenYoMin2 TW), handles Pandoc conversion workflows, and ensures proper heading and body styling for publishing.
---

# Taigi Document Typesetter

This skill automates the typesetting of Taigi literary works into professional DOCX and ODT formats.

## Typesetting Workflow

1.  **Preparation:** Ensure the source text (usually Markdown) is properly formatted using the `taigi-han-lo-formatter`.
2.  **Pandoc Conversion:** Convert Markdown to DOCX using Pandoc with a reference document.
    ```bash
    pandoc source.md -o output.docx --reference-doc=reference.docx --smart
    ```
3.  **Font Application:** Taigi text requires specific fonts to display diacritics and Hanji correctly. The preferred font is **GenYoMin2 TW** (Regular for body, Bold for headings).
4.  **Reference Patching:** Use the bundled scripts to automate the application of fonts and styles to the DOCX files.

## Bundled Scripts

-   **`apply_fonts_to_docx.py`**: Directly modifies a DOCX file to set the font of all runs to GenYoMin2 TW.
-   **`patch_reference_docx.py`**: Patches a Pandoc reference DOCX file to ensure future conversions use the correct fonts.

## Fonts Knowledge

-   **GenYoMin2 TW R**: Standard weight for body text.
-   **GenYoMin2 TW B**: Bold weight for titles and headers (H1, H2, H3).
-   **Full-width spacing:** Ensure the document uses appropriate margins and line spacing for readability in Taigi publications.
