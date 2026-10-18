---
name: taigi-legacy-encoding-converter
description: Recovers legacy Taigi Pe̍h-ōe-jī (POJ) text into modern Unicode from number formats (a2, ou3), font hacks (TP tws21.ttf, HOTSYS 2000, SinBongAi CTS) and the Big5-era Private Use Area kana that Word .doc extraction leaves behind. Use whenever Taigi text shows Latin-1 garbage such as ä ö ü ¬ ¯ ± ² ³ where tone marks belong, tone digits after syllables, or U+F6F7–U+F79F characters, and whenever the KonvertLegacyPOJ library or its mapping tables are involved.
---

# Taigi Legacy Encoding Converter

Backed by the Kotlin Multiplatform library **KonvertLegacyPOJ** (package `taibun.kesimi.poj`). The authoritative mapping tables are in `references/encoding_mappings.md`; read them before hand-converting anything.

## Recognising the encoding

| Symptom in the text | Encoding | Function |
| :-- | :-- | :-- |
| `a2`, `ou3`, `nn` after syllables | number format | `convertLegacyNumberFormatToUnicode` / `convertLegacyTpPojToUnicode` |
| `ä ë ö ü ¬ ¯ ± ² ³ ´ ° „ …` inside POJ words | TP font hack (tws21.ttf) | `convertLegacyTpFontHackToUnicode` |
| `¡ … ƒ „ † ‚ Š ˆ ‰ ˜ › ¢ Œ ‹ Ÿ` inside POJ words | HOTSYS font hack | `convertLegacyHotsysFontHackToUnicode` |
| `OU2`, `Ou3`: uppercase nasal-o with digits | HOTSYS 2000 / CTS POJ | `convertLegacyHotsysPojToUnicode`, `convertCtsPojToUnicode` |
| `OO2`, `a9` | CTS Tai-lo | `convertCtsTaiLoToUnicode` |
| `U+F6F7 … U+F79F` where Japanese belongs | Big5-ETEN kana in the PUA | `restoreLegacyKana` (below; not in the library) |

Every function with examples, plus Gradle wiring: `references/usage_examples.md`.

## Conversion process

1. Identify the encoding from the table (a document may mix number format and font hack).
2. Apply the matching converter(s) **before** any Han-Lo spacing or tone normalization; the normalizer expects real Unicode diacritics.
3. NFC-normalize the result.
4. Hand off to `taigi-han-lo-formatter`.

## Critical rules

- **HOTSYS/CTS tone swap.** Tones 2 and 3 are swapped for the nasal-o vowel in uppercase only: `OU2`/`Ou2` → `Ò͘` (grave), `OU3`/`Ou3` → `Ó͘` (acute). Lowercase `ou2`/`ou3` are **not** swapped.
- `hotsysPojToUnicodeMap` is `tpPojToUnicodeMap + OU overrides`; the overrides win.
- The library maps are plain `String.replace` passes over the whole text. Apply a font-hack map only to text that really is in that hack: `ä` in a German name would be converted too.
- Scope is Taigi only. Hakfa entries (`ii`, `ṳ`) are intentionally absent; see `hakfa-roman-orthography-converter` for Hakfa.

## Big5-ETEN kana in the Private Use Area

Legacy Word `.doc` files keep Japanese kana in the Big5-ETEN extension block. `textutil` cannot map it and emits one contiguous PUA run: hiragana ぁ..ん (U+3041..U+3093) land at U+F6F7..U+F749, katakana ァ..ヶ (U+30A1..U+30F6) at U+F74A..U+F79F. Undo the shift after the font-hack pass:

```python
def restore_legacy_kana(text: str) -> str:
    out = []
    for c in text:
        o = ord(c)
        if 0xF6F7 <= o <= 0xF749:
            out.append(chr(0x3041 + o - 0xF6F7))
        elif 0xF74A <= o <= 0xF79F:
            out.append(chr(0x30A1 + o - 0xF74A))
        else:
            out.append(c)
    return "".join(out)
```

Symptom before the fix: a Japanese loanword shows only its Hanji, such as `流` where `流し` was written. The Kotlin version is in `taigi-doc-pipeline/assets/pipeline/.../PipelineFix.kt`.

## Reverse direction

`convertUnicodeToLegacyNumberFormat` (`á` → `a2`, `ò͘` → `ou3`) exports to tools that only accept number format.

## Resources

- `references/encoding_mappings.md`: TP numeric, TP font hack, HOTSYS numeric and HOTSYS font hack tables (authoritative mirror of the library's `POJ_encoding_mappings.md`).
- `references/usage_examples.md`: all ten public functions with examples, the Gradle `includeBuild` setup, and a whole-document recipe.
