---
name: taigi-document-structurer
description: Turns cleaned Taigi text (the fixed output of a Word .doc extraction) into Markdown with YAML title/author front matter, H1 part markers, H2 chapter headings, footnote headings and pandoc verse line blocks, using length, punctuation, indent-depth and running-header heuristics. Use whenever flat Taigi text needs headings before typesetting, when chapter detection misfires, or when poems or verse in a Taigi document come out as separate paragraphs.
---

# Taigi Document Structurer

Flat text → Markdown that pandoc turns into a well-styled Word document. `scripts/structure_md.py` implements every rule below; run it rather than re-deriving the heuristics.

```bash
scripts/structure_md.py 02_<title>_fixed.txt -o 03_<title>_structured.md \
    --raw 01_<title>_raw.txt --title "<title>"
```

- `--raw` is optional but enables verse detection: indent depth survives only in the raw `textutil` output, because the fix stage strips leading whitespace.
- `--title` defaults to the input filename with the `NN_` prefix, `_fixed` suffix and `《》` stripped. It is NFC-normalized because macOS stores filenames in NFD while the body text is NFC.

## Output shape

```markdown
---
title: <canonical title>
author: <byline>
---

# 第1 pha：…           ← part marker (H1)

## Chapter title       ← H2

One prose line.        ← every source line becomes its own paragraph

| verse line 1         ← pandoc line block: one paragraph, soft breaks
| verse line 2
```

## Heuristics, in the order the script applies them

1. **Tail noise.** Walk backwards from the end dropping blank lines, any line containing `PAGE` or `【…】` (pagination), a line equal to the canonical title (textutil echoes the running header), and, right after such an echo, a short line with no Hanji (the Roman Orthography twin of the title).
2. **Title.** First non-blank line. Equal to the canonical title → YAML `title` only, no duplicate H1. Short and *starting with* the canonical title → textutil concatenated the cover title and the first section title: emit it as an article H1 and keep the canonical title in YAML. Otherwise the line is the title.
3. **Byline.** Next non-blank line if ≤ 20 chars, no colon, not a part marker and not starting with `♣` → YAML `author`. Pandoc maps `title`/`author` to Word's Title and Author styles.
4. **Heading candidate.** Stripped length ≤ 40, does not end in `。！？`, does not start with `－`, `—` or `--` (those are quotes or attributions).
5. **Heading level.** `第N pha` (regex `^第\s*\d+\s*pha(?![A-Za-z])`) → H1; every other heading → H2.
6. **One-line heading.** A candidate followed by a blank line.
7. **Two-line heading.** A candidate ending in `－－`, `——` or `--`, followed by another candidate and then a blank → joined with a space into one heading.
8. **Notes heading.** A candidate ending in a dash marker and directly followed by a footnote entry `（1）：…` → H2.
9. **Decorated headings.** `♣text♣` is normalized to `♣ text ♣`.
10. **Safety.** The last non-blank line of the file is never promoted; it is the closing sentence of the last chapter.
11. **Verse.** From the raw text: a 4-space indent starts a prose paragraph; a tab or ≥ 5 spaces marks a verse candidate; a run of ≥ 2 candidates is a verse block. Documents with no indent at all carry poems as runs of ≥ 2 consecutive short column-0 lines bounded by blanks that are not dialogue (`「『（`), not footnotes and not sentence-final; those are verse too, unless the pair is a two-line heading. Verse is emitted as a pandoc line block (`| line`).
12. **Prose.** Every remaining line is followed by a blank line so pandoc makes one docx paragraph per source line. Runs of blank lines collapse to one.

## Workflow position

Extract (`textutil`) → fix (`taigi-legacy-encoding-converter`, `taigi-han-lo-formatter`) → **structure** → typeset (`taigi-document-typesetter`) → outline (`taigi-pdf-outliner`). The orchestration, naming convention and the project-layout wrapper `03_structure.py` live in `taigi-doc-pipeline`.
