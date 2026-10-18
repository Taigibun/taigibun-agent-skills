---
name: taigi-han-lo-formatter
description: Normalizes mixed Hanji + Roman Orthography (Han-Lo) Taigi text: tone-mark placement, diacritic repair, spacing and hyphen rules next to Hanji, full-width punctuation, and protection of English words, abbreviations and decimal points from the normalizer. Use whenever Taigi text has wrong spaces or hyphens beside Hanji, half-width punctuation in Han-Lo sentences, misplaced or duplicated tone marks, or when calling the KonvertToPoj normalizePoj* methods on real documents.
---

# Taigi Han-Lo Formatter

Han-Lo (Hàn-Lô) mixes Hanji (漢字) with Roman Orthography (POJ or KPL). Pure Roman Orthography separates words with spaces and syllables with hyphens (`Tâi-oân-lâng`); next to Hanji, both disappear.

## Library entry points (KonvertToPoj)

| Method | Use |
| :-- | :-- |
| `normalizePojHybridHanLoAutoChoanLoOrHanLoPunctuation(text)` | Documents. Validates tokens first so foreign words survive; full-width punctuation where the text is Han-Lo, half-width where it is all-Roman (Choân-Lô). The document pipeline uses this one. |
| `normalizePojHybridHanLoForceUsingFullwidthPunctuation(text)` | Same, but punctuation is always full-width. |
| `normalizePojHanLo…` (non-Hybrid variants) | No validation gate; converts more aggressively. Pure POJ input only. |
| `ConvertOptions(aggressiveWhitespace = false)` | Keep the author's spacing except where the rules forbid it. The default `true` rebuilds canonical spacing. |

## Formatting rules (apply in order)

1. **Wrong diacritic substitution:** tilde `~` → macron `¯`, caron `ˇ` → circumflex `^`, and similar.
2. **Duplicate combining mark removal** on a single vowel.
3. **NFC renormalization.**
4. **Vietnamese precomposed characters** → POJ forms (`ớ` → `ó͘`, `ờ` → `ò͘`).
5. **Triple-h fix:** `chhhoā` → `chhoā`.
6. **Hyphen spacing:** `tiûⁿ -ló` → `tiûⁿ-ló`.
7. **ts → ch (POJ target only):** `ts`/`tsh` → `ch`/`chh`.
8. **Nasalization cleanup:** drop trailing `ⁿ` after a nasal initial (`niûⁿ` → `niû`).
9. **Nasal geminate tone fix:** `n̄ng` → `nn̄g`.
10. **Diphthong tone placement:** `hoá` → `hóa`, `chîa` → `chiâ` (rules in `taigi-roman-orthography-converter/references/linguistic_rules.md`).
11. **Entering tone correction:** tones 4 and 8 only on syllables ending in `p t k h`; an invalid mark on a checked syllable defaults to tone 8.
12. **Spaces and hyphens next to Hanji:**
    - DELETE the space between two Hanji: `台灣 人` → `台灣人`
    - DELETE the space between Hanji and Roman Orthography: `我 ê` → `我ê`, `ê 人` → `ê人`
    - DELETE the hyphen between two Hanji: `台-灣` → `台灣`
    - DELETE the hyphen between Hanji and Roman Orthography: `台灣-ê` → `台灣ê`
    - KEEP the space between two Roman words: `chin hó`
    - KEEP the hyphen inside a Roman word: `chin-chiàⁿ`
13. **Full-width punctuation** in Han-Lo lines: `, . ? ! : ; ( )` → `，。？！：；（）`.

## Protecting non-Taigi tokens before normalizing

The normalizer treats every Latin token as a POJ candidate. Before running it on a real document, shield what is not Taigi, then restore:

1. **Dotted abbreviations:** two or more `X.` pairs (`U.S.A.`, `P.S.`) → placeholder.
2. **Foreign words and phrases:** an ASCII word of ≥ 2 letters that is not adjacent to a POJ character (letters with diacritics, `ⁿ`, `o͘`) and fails `isValidText(word, POJ_UNICODE)` → placeholder. Extend across following space-separated words with the same property, so `Nelson Mandela` is one unit.
3. **Decimal and abbreviation dots:** replace `.` with a sentinel (the pipeline uses U+FDD2) so they do not become `。`; restore afterwards.
4. Run the normalizer, then restore the placeholders.

Then **post-fix** what the round trip still gets wrong:

- `X .` → `X.` and `. X` → `.X` for Latin letters (abbreviation spacing);
- `aB` → `a B` where a lowercase letter is glued to an uppercase one;
- `」.` → `」。`.

Working code: `taigi-doc-pipeline/assets/pipeline/src/main/kotlin/taibun/pipeline/PipelineFix.kt`.

## Gotchas

- **KPL → POJ pre-pass.** Every `normalizePoj*` method converts a token that validates strictly as KPL but not as POJ: `Tsai` → `Chai`. Shield proper nouns that happen to look like KPL syllables.
- **Glued tone digits (KonvertToPoj 0.6.0).** An input-form digit on a checked syllable is consumed: `gah1句話` → `gah句話`. Shield digits that must survive.
- **Soft wraps.** Join Word's soft-wrapped lines back into paragraphs first, or the spacing rules run across false line ends (`taigi-doc-pipeline/references/word-doc-extraction-quirks.md`).
- **Order.** Legacy encoding recovery (`taigi-legacy-encoding-converter`) comes first; the normalizer needs real Unicode diacritics.

## Crucial Hanji knowledge

- The particle `ê` stays `ê`; do not transcribe it to `的`.
- Use common Hanji only; rare characters stay in Roman Orthography.

## Example

- Input: `Góa chin ài Tâi-oân .` with Tâi-oân = 台灣 and Góa = 我
- Intermediate: `我 chin ài 台灣 .`
- Result: `我chin愛台灣。`
