# What textutil makes of a legacy Word .doc

Observations from converting 1990s–2000s Taigi `.doc` files with
`textutil -convert txt -encoding UTF-8`. They drive stages 1–3 of the pipeline.

## Paragraphs are soft-wrapped

Word's text export wraps long paragraphs at the window width:

- a line starting with 4 spaces or a tab **begins a paragraph**;
- a line at column 0 is **either a chapter title or a continuation** of the previous paragraph.

A title is followed by a blank line within two lines: a one-line title, or a two-line title whose
second line is also at column 0 and is then followed by a blank. Anything else at column 0 is a
soft-wrap continuation and is glued back onto the open paragraph. `PipelineFix.joinSoftWraps`
(stage 2) does this; `03_structure.py` replays the same classification over the raw text to
recover the indent depth that stage 2 strips.

## Indent depth encodes prose vs verse

| Leading whitespace | Meaning |
| :-- | :-- |
| 4 spaces | prose paragraph start |
| 5+ spaces or a tab | verse line (poem quotes; attribution lines are tab-led and right-aligned in the original) |
| none, whole document | poems appear as runs of ≥ 2 consecutive short column-0 lines bounded by blank lines |

A run of ≥ 2 verse candidates is a verse block. Stage 3 needs the stage-1 raw file for this.

## Running header/footer echo at the tail

The document title, sometimes followed by its Roman Orthography twin on the next line, is echoed
at the very end of the text together with pagination noise (`PAGE`, `【…】`). Trim from the tail
backwards: blanks, noise lines, a line equal to the canonical title, then a short line with no
Hanji right after it.

## Cover title concatenation

textutil sometimes joins the cover title and the first section title into one line
(`Pha荒ê故事` + `ê故事` → `Pha荒ê故事ê故事`). Stage 3 treats a short first line that *starts
with* the canonical title as the article H1 and keeps the canonical title in YAML.

## Big5-ETEN kana land in the Private Use Area

Hiragana ぁ..ん (U+3041..U+3093) arrive as U+F6F7..U+F749, katakana ァ..ヶ (U+30A1..U+30F6) as
U+F74A..U+F79F. Stage 2 shifts them back (`restoreLegacyKana`). Symptom before the fix: a
Japanese loanword shows only its Hanji (`流` where `流し` was written). See
`taigi-legacy-encoding-converter`.

## TP font hack

POJ diacritics appear as Latin-1 characters (`ä` = ā, `ö` = ō, `¬` = o͘, `°` = ⁿ …).
`KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode` recovers them; run it before anything else
touches the text, because the Han-Lo normalizer expects real diacritics.

## Filenames are NFD on macOS

`《Pha荒ê故事》.doc` on disk is NFD; the body text is NFC. NFC-normalize any title derived from a
filename before comparing it with text.

## Typos in the source survive

For example `gah1 句話` (a stray tone digit). KonvertToPoj 0.6.0 consumes the glued digit
(`gah句話`); older versions kept it. Decide per project whether to regenerate committed outputs
when the library changes.
