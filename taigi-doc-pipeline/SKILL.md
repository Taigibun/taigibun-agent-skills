---
name: taigi-doc-pipeline
description: Runs or sets up the five-stage Taigi document pipeline that turns legacy Microsoft Word .doc files of Taigi (Han-Lo / POJ) literature into fixed Unicode text, structured Markdown, a GenYoMin2 TW typeset .docx and a font-independent outlined PDF. Use this whenever the user wants to digitize, convert, batch-process or republish Taigi .doc or .txt sources, mentions NN_<title>_<descriptor> stage files (raw, fixed, structured, typeset, outlined) or doc_original / doc_result folders, or wants to run, re-run, extend or debug any of the stage 1–5 scripts. It is the orchestrator and names the taigi-* skill that owns each stage.
---

# Taigi Document Pipeline

Five reproducible stages. Every stage writes `NN_<title>_<descriptor>.<ext>` into `doc_result/`, so the step that produced a file is visible in its name and files sort in pipeline order. `<title>` is the `.doc` filename without its extension, e.g. `《Pha荒ê故事》`.

```
doc_original/<title>.doc            read-only source of truth, never edited
   │  1 extract    textutil
doc_result/01_<title>_raw.txt
   │  2 fix        KonvertLegacyPOJ + KonvertToPoj through a small Kotlin app
doc_result/02_<title>_fixed.txt
   │  3 structure  03_structure.py: YAML title/author, H1/H2, verse blocks
doc_result/03_<title>_structured.md
   │  4 typeset    pandoc (smart OFF) + GenYoMin2 TW reference + run patching
doc_result/04_<title>_typeset.docx
   │  5 outline    Microsoft Word (AppleScript) → PDF → Ghostscript -dNoOutputFonts
doc_result/05_<title>_outlined.pdf
   │  publish      hand-copied as <title>.docx / .odt / .pdf
doc_result_final/
```

## Stage ownership

| Stage | Script | Skill holding the rules |
| :-- | :-- | :-- |
| 1 extract | `scripts/01_extract.sh` | this skill: `references/word-doc-extraction-quirks.md` |
| 2 fix | `scripts/02_fix.sh` → `assets/pipeline/` (Kotlin) | `taigi-legacy-encoding-converter`, `taigi-han-lo-formatter`; this skill: `references/stage2-fix-pass.md` |
| 3 structure | `scripts/03_structure.py` | `taigi-document-structurer` (its `structure_md.py` is the generic CLI of the same code) |
| 4 typeset | `scripts/04_typeset.sh` | `taigi-document-typesetter`, `taigi-docx-typography-expert` |
| 5 outline | `scripts/05_outline.sh` | `taigi-pdf-outliner` |

Read the owning skill before changing what a stage does.

## Running

```bash
scripts/00_pipeline.sh                      # every .doc in doc_original/
scripts/00_pipeline.sh "《Pha荒ê故事》"       # one title
scripts/03_structure.py "《Pha荒ê故事》"      # one stage; every script takes the title without .doc
```

Stages 1–3 are idempotent and fast; re-run them freely. Stage 2 is slow the first time because Gradle builds both libraries from source. Stages 4–5 depend on installed tools, and stage 5 opens Microsoft Word.

## Setting up a new project

1. Create `doc_original/` (sources), `doc_result/`, `doc_result_final/`, `assets/` and `scripts/`.
2. Copy `scripts/*` from this skill into `scripts/`, plus `apply_fonts_to_docx.py` and `patch_reference_docx.py` from `taigi-document-typesetter/scripts/`. (`04_typeset.sh` also finds them in the sibling skill when run from a skills checkout.)
3. Copy `assets/settings.gradle.kts`, `assets/build.gradle.kts` and `assets/pipeline/` to the project root and set `rootProject.name`. Add the libraries as submodules; they are not on Maven Central (checked 2026-10), and `settings.gradle.kts` substitutes their coordinates with `includeBuild`:
   ```bash
   git submodule add https://github.com/PehoejiKesi/KonvertLegacyPOJ KonvertLegacyPOJ
   git submodule add https://github.com/PehoejiKesi/KonvertToPOJ KonvertToPOJ
   cp -r KonvertToPOJ/gradle KonvertToPOJ/gradlew .      # or run: gradle wrapper
   ```
4. Tools: `brew install pandoc ghostscript poppler`; JDK 17 or 21 (`02_fix.sh` pins `JAVA_HOME`, Gradle 8.10 rejects JDK 25); Microsoft Word for Mac; GenYoMin2 TW `.ttc` files from https://github.com/ButTaiwan/genyo-font/releases (v2.100) installed in `~/Library/Fonts/`.
5. `.gitignore`: `build/`, `.gradle/`, `.kotlin/`, `assets/fonts/`, `assets/reference*.docx`, `**/__pycache__/`, and `doc_result/05_*_outlined.pdf` when the final copies are committed in `doc_result_final/`.
6. Run `scripts/00_pipeline.sh "<title>"` and **look at a rendered page** of the PDF: `pdftoppm -png -r 60 -f 2 -l 2 out.pdf /tmp/page`.

## Rules

- `doc_original/` is immutable. Fix problems in the pipeline, never in the source.
- Never hand-edit a `doc_result/` file; change the stage that produced it and re-run from there.
- pandoc runs with `-f markdown-smart-raw_tex`. Smart punctuation would turn POJ `--ê` into an en dash.
- Stage 5 never uses LibreOffice; its PDF export renders every GenYoMin2 TW glyph as a box. LibreOffice may produce the `.odt` copy for `doc_result_final/`.
- `pdffonts` and `pdftotext` do not prove a PDF is readable. Render a page.
- macOS filenames are NFD, the text is NFC; scripts normalize titles before comparing.
- When a library version changes, diff the regenerated `02_*_fixed.txt` against the committed one before accepting it (KonvertToPoj 0.6.0 changed `gah1` → `gah`).

## Debugging by symptom

| Symptom | Look at |
| :-- | :-- |
| `ä ö ü ¬ ¯` in `01_*_raw.txt` | expected: TP font hack; stage 2 fixes it (`taigi-legacy-encoding-converter`) |
| U+F6F7–U+F79F in `01`/`02` output | kana PUA shift; stage 2 `restoreLegacyKana` |
| English name mangled in `02` | foreign-word shielding (`references/stage2-fix-pass.md`, `taigi-han-lo-formatter`) |
| paragraph split mid-sentence in `02` | soft-wrap joining (`references/word-doc-extraction-quirks.md`) |
| chapter missed or a sentence promoted in `03` | heading heuristics (`taigi-document-structurer`) |
| poem lines as separate paragraphs in `04` | verse detection needs the `01_*_raw.txt` indent depth |
| hyphen breaks at a line end in `04` | `<w:noBreakHyphen/>` run splitting (`taigi-docx-typography-expert`) |
| `，` at the start of a line in `04`/`05` | kinsoku flags or a custom noLineBreaks list (`taigi-docx-typography-expert`) |
| PDF is rows of boxes | it was produced with LibreOffice; redo stage 5 (`taigi-pdf-outliner`) |
| Gradle: unsupported Java version | JDK 25 picked up; `02_fix.sh` pins 17/21, check `/usr/libexec/java_home -V` |
| Word hangs in stage 5 | Automation permission dialog; allow Terminal → Microsoft Word and re-run |

## Bundled files

- `scripts/00_pipeline.sh` … `05_outline.sh`: the stage scripts; project layout assumed (`ROOT` is the parent of `scripts/`).
- `assets/settings.gradle.kts`, `assets/build.gradle.kts`, `assets/pipeline/`: the composite Gradle build and the stage-2 fixer `PipelineFix.kt`.
- `references/word-doc-extraction-quirks.md`: what `textutil` does to legacy Word files and how stages 1–3 cope.
- `references/stage2-fix-pass.md`: the fix pass order and why.
