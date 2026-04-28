---
name: taigi-pdf-outliner
description: Converts DOCX/ODT documents to PDF and "outlines" the text into vector paths using Ghostscript. This ensures the PDF displays correctly on all devices without requiring specific fonts to be installed.
---

# Taigi PDF Outliner

This skill provides the workflow to generate font-independent PDF files for Taigi publications.

## Workflow

1.  **DOCX/ODT to PDF:** Use LibreOffice in headless mode to convert the document to a standard PDF.
    ```bash
    /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf input.docx
    ```
2.  **Outlining (Vectorization):** Use Ghostscript with the `-dNoOutputFonts` flag to convert all text glyphs into vector paths. This removes the font dependency entirely.
    ```bash
    gs -o output_outlined.pdf -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dNoOutputFonts input.pdf
    ```

## Dependencies

-   **LibreOffice:** Required for the initial conversion. Install via `brew install --cask libreoffice`.
-   **Ghostscript:** Required for outlining. Install via `brew install ghostscript`.

## When to Use

Use this skill when preparing final versions of documents for distribution or printing, where you cannot guarantee the recipient has the specific Taigi fonts (like GenYo) installed. Outlining ensures perfect visual fidelity at the cost of text searchability.
