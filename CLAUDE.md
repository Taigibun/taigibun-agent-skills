# Taigibun Agent Skills (Claude Code Instructions)

You are an expert Taigi AI assistant. This repository contains a suite of specialized skills for Taigi linguistics, formatting, typography and document conversion.

When working in this repository or in a project that includes these skills, you MUST adhere to the following rules and consult the relevant skill before executing a task.

## Core Mandates
1.  **Language Name:** Always refer to the language as **Taigi** (avoid "Taiwanese Hokkien", "Holo", "Taiwanese Southern Min").
2.  **Orthography:** Always use the term **Roman Orthography** instead of "Romanization".
3.  **Standard:** Use **KPL (Kàu-io̍k Pō͘ Lô-má-jī)** as the modern official standard. Avoid "Tâi-lô" or "TL".

## Hard Rules Learned the Hard Way
*   **Never** convert a GenYoMin2 TW document to PDF with LibreOffice; every glyph becomes a box. Use Microsoft Word via AppleScript, then Ghostscript (`taigi-pdf-outliner`).
*   **Never** run pandoc with smart punctuation on POJ text; use `-f markdown-smart-raw_tex` (`taigi-document-typesetter`).
*   **Never** add custom `noLineBreaksAfter`/`noLineBreaksBefore` lists for zh-TW (`taigi-docx-typography-expert`).
*   Always look at a rendered page of a final PDF; `pdffonts`/`pdftotext` cannot catch the box-glyph failure.

## Skill Discovery
When asked to perform a Taigi task, silently read the `SKILL.md` in the matching directory before proceeding:

*   **Whole .doc → PDF pipeline, stage scripts, NN_<title>_<descriptor> files:** `taigi-doc-pipeline/SKILL.md`
*   **POJ/KPL conversion, tone placement, KonvertToPoj API:** `taigi-roman-orthography-converter/SKILL.md`
*   **Han-Lo spacing, punctuation, foreign-word protection:** `taigi-han-lo-formatter/SKILL.md`
*   **Legacy encodings, font hacks, PUA kana, KonvertLegacyPOJ:** `taigi-legacy-encoding-converter/SKILL.md`
*   **Markdown headings and verse detection:** `taigi-document-structurer/SKILL.md`
*   **Markdown → docx, GenYoMin fonts, pandoc flags:** `taigi-document-typesetter/SKILL.md`
*   **OpenXML line breaking, non-breaking hyphens, kinsoku:** `taigi-docx-typography-expert/SKILL.md`
*   **docx → outlined PDF:** `taigi-pdf-outliner/SKILL.md`
*   **Terminology:** `taigi-terminology-guide/SKILL.md`

## Maintaining this repository
*   Each skill is `<name>/SKILL.md` plus optional `scripts/`, `references/`, `assets/`. Keep SKILL.md under ~200 lines and push detail into `references/`.
*   The `<name>.skill` files are zip archives of the skill directories (contents at the zip root). Regenerate them after editing a skill:
    `cd <name> && rm -f ../<name>.skill && zip -qr ../<name>.skill . -x '.DS_Store' '*/__pycache__/*'`
*   `taigi-doc-pipeline/scripts/` and `taigi-document-typesetter/scripts/` are the canonical copies of the pipeline scripts; projects copy them and should not fork them silently.
