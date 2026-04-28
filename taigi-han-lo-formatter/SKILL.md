---
name: taigi-han-lo-formatter
description: Formats mixed Hanji (Traditional Chinese) and Roman Orthography text according to strict Han-Lo spacing and punctuation rules. Use when processing Taigi text to ensure proper hyphenation, whitespace, and full-width punctuation.
---

# Taigi Han-Lo Formatter

This skill applies strict Han-Lo (Hàn-Lô) formatting rules to Taigi text. Han-Lo is a mixed writing system combining Hanji (漢字/Traditional Chinese) and Roman Orthography (like POJ or KPL).

## Core Principle

In pure Roman Orthography, words are separated by spaces, and syllables within a word are connected by hyphens (e.g., `Tâi-oân-lâng`).
However, when formatting Han-Lo text, you must systematically remove spaces and hyphens adjacent to Hanji characters, while preserving them between romanized words/syllables.

## Formatting Rules (Apply in Order)

When processing text, apply the following 13 post-processing steps:

1. **Wrong Diacritic Substitution:** Fix common errors (tilde `~` → macron `¯`, caron `ˇ` → circumflex `^`, etc.).
2. **Duplicate Combining Mark Removal:** Remove duplicated diacritics on a single vowel.
3. **NFC Renormalization:** Ensure all text is Unicode NFC-normalized.
4. **Vietnamese Character Fix:** Convert Vietnamese precomposed characters to POJ forms (`ớ` → `ó͘`, `ờ` → `ò͘`).
5. **Triple-h Fix:** Remove redundant `h` characters (e.g., `chhhoā` → `chhoā`).
6. **Hyphen Spacing Fix:** Remove whitespace around hyphens (e.g., `tiûⁿ -ló` → `tiûⁿ-ló`).
7. **ts→ch Normalization (POJ Mode Only):** If the target orthography is POJ, convert `ts`/`tsh` to `ch`/`chh`.
8. **Nasalization Cleanup:** Remove trailing `ⁿ` from syllables that already start with an `n` initial.
9. **Nasal Geminate Tone Fix:** Fix incorrect nasal tone placement (e.g., `n̄ng` → `nn̄g`).
10. **Diphthong Tone Placement Fix:** Correct common misplacements (e.g., `hoá` → `hóa`, `chîa` → `chiâ`).
11. **Entering Tone Correction:** Ensure tones 4 and 8 are only applied to checked syllables (ending in `p`, `t`, `k`, `h`). If an invalid tone mark is found on a checked syllable, default it to tone 8.
12. **DELETE Spaces and Hyphens Adjacent to Hanji:**
    *   **DELETE** space between two Hanji: `台灣 人` → `台灣人`
    *   **DELETE** space between Hanji and Roman Orthography: `我 ê` → `我ê`, `ê 人` → `ê人`
    *   **DELETE** hyphen between two Hanji: `台-灣` → `台灣`
    *   **DELETE** hyphen between Hanji and Roman Orthography: `台灣-ê` → `台灣ê`
    *   **KEEP** space between two Romanized words: `chin hó` stays `chin hó`
    *   **KEEP** hyphen within Romanized words: `chin-chiàⁿ` stays `chin-chiàⁿ`
13. **Full-Width Punctuation:** Convert ASCII punctuation to full-width equivalents (`, . ? ! : ; ( )` → `，。？！：；（）`).

## Crucial Hanji Knowledge

*   **The word `ê`:** The possessive/adjectival particle `ê` should generally **NOT** be transcribed to the Hanji `的`. Keep it as `ê`.
*   **Common Hanji:** Use common Hanji only. Rare or obscure characters should remain in their romanized form.

## Example

*   **Input:** `Góa chin ài Tâi-oân .` (Assume user wants Han-Lo conversion where Tâi-oân = 台灣 and Góa = 我)
*   **Intermediate:** `我 chin ài 台灣 .`
*   **Result:** `我chin愛台灣。`
