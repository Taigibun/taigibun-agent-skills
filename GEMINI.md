# GEMINI.md

## User Preferences
- **Language Reference**: Always refer to the language as **Taigi**. Avoid "Taiwanese Southern Min", "Holo", or "Taiwanese Hokkien".
- **Terminology**: Use the term **Roman Orthography** (or "roman orthography") instead of "Romanization" or "romanization".
- **Orthography Names**:
  - Taigi Latin-script Orthography
  - Taigi Roman-script Orthography
  - Use **KPL (Kàu-io̍k Pō͘ Lô-má-jī)**. Avoid: Taiwanese Romanization, TL, Tâi-lô.

## Agent Skills
This repository contains packaged `.skill` files for Gemini CLI. If you need to perform Taigi conversions, formatting, typesetting or the full .doc → PDF pipeline, ensure you have the relevant `.skill` installed via the `gemini skills install` command and reloaded.

Hard rules: never produce the PDF with LibreOffice for GenYoMin2 TW documents (use Microsoft Word + Ghostscript, see `taigi-pdf-outliner`), and never let pandoc apply smart punctuation to POJ text (`-f markdown-smart-raw_tex`, see `taigi-document-typesetter`).
