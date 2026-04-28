---
name: taigi-document-structurer
description: Automatically detects and applies Markdown header structure to raw Taigi text files. Identifies book titles, bylines, and chapter headings using linguistic and length-based heuristics.
---

# Taigi Document Structurer

This skill provides heuristics for transforming flat Taigi text into structured Markdown documents suitable for typesetting.

## Structural Heuristics

1.  **H1 (Book Title):** The first non-blank line of the file.
2.  **Byline (Author):** The second non-blank line of the file. Render as `*italic*`.
3.  **H2 (Chapter Heading) Candidates:**
    *   Stripped length ≤ 40 characters.
    *   Does **NOT** end with punctuation `。`, `！`, or `？`.
    *   Does **NOT** start with dashes `－`, `—`, or `--`.
4.  **H2 Promotion Rules:**
    *   **Single-line H2:** Candidate is followed by at least one blank line.
    *   **Two-line H2:** Candidate ending in `－－`, `——`, or `--` followed by another candidate line and then a blank line.
5.  **Noise Removal:** Drop lines containing pagination noise like `PAGE` or bracketed numbers `【…】`.
6.  **Safety Rule:** The very last non-blank line in a file should **NEVER** be promoted to a heading (avoids closing sentences becoming headers).

## Workflow

1.  **Extract:** Get raw text from source (e.g., via `textutil`).
2.  **Fix:** Apply `taigi-han-lo-formatter` first to ensure clean text.
3.  **Structure:** Apply the heuristics above to insert `#` and `##` headers.
