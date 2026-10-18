---
name: taigi-roman-orthography-converter
description: Converts and validates Taigi Roman Orthography between POJ (Pe̍h-ōe-jī) and KPL (Kàu-io̍k Pō͘ Lô-má-jī), each in Input (tone numbers) and Unicode (diacritics) form, including tone-mark placement rules and the KonvertToPoj library API. Use whenever text like tai5-gi2, Tâi-gí, tsit8-e5 or tsi̍t-ê must be converted, checked or have its tone marks corrected, and whenever someone mentions Tâi-lô, TL, POJ, KPL, lomaji or lô-má-jī.
---

# Taigi Roman Orthography Converter

## Guidelines

- **Orthography**: always say **Roman Orthography**, never "Romanization". Prefer **Taigi Latin-script Orthography** or **Taigi Roman-script Orthography**.
- **Naming**: the language is **Taigi**. Avoid "Taiwanese Southern Min", "Holo" and "Taiwanese Hokkien". The official standard is **KPL**; do not call it Tâi-lô or TL.

## Overview

Backed by the Kotlin Multiplatform library **KonvertToPoj** (0.6.0). It handles the 12 directions between POJ/KPL × Input/Unicode, validation, and POJ normalization. Read `references/linguistic_rules.md` before any manual conversion; read `references/api_summary.md` before calling the library.

## Core capabilities

1. **Format conversion:** `POJ_INPUT ↔ POJ_UNICODE`, `KPL_INPUT ↔ KPL_UNICODE`, and POJ ↔ KPL across systems. Only syllable-shaped tokens are converted; English words pass through untouched.
2. **Normalization:** tone marks moved to the correct vowel, Han-Lo spacing and punctuation width, diacritic repair. Foreign words survive in the Hybrid variants.
3. **Validation:** whitelist-based phonotactics, strictly separated per system (`ch` is never valid KPL, `ts` never valid POJ).

## Conversion pipeline (manual or when checking the library)

1. **NFC-normalize** the input.
2. **Map the orthography:** initials, vowels and finals per the target system (`ch` → `ts`, `oa` → `ua`, `ek` → `ik`, `o͘` → `oo`, `ⁿ` → `nn`).
3. **Re-place the tone mark** by the target system's rules; POJ and KPL differ on compound vowels.
4. **Special characters:** `o͘` is o + U+0358, `ⁿ` is U+207F, tone 8 is U+030D, tone 9 is breve (POJ) or double acute (KPL).

### Quick reference

| Feature | POJ | KPL |
| :--- | :--- | :--- |
| **Initials** | `ch` / `chh` | `ts` / `tsh` |
| **Vowels** | `oa` / `oe` | `ua` / `ue` |
| **Finals** | `ek` / `eng` | `ik` / `ing` |
| **Open o** | `o͘` | `oo` |
| **Nasalization** | `ⁿ` | `nn` |

### Tone placement in one line each

- **POJ:** mark the 2nd letter from the right; if that is `i`, mark the rightmost letter instead; in a checked syllable whose 2nd-from-right is `i` or `u`, mark the 3rd (except `iuh`). `ng` counts as one letter, `ⁿ` counts as nothing, `o͘` is one unit.
- **KPL:** mark `a` if present, else the rightmost vowel (`oo` → left `o`), else the nasal.

## Things that surprise people

- `POJ_UNICODE ↔ KPL_UNICODE` is direct: digits in the text are never read as tones unless `viaInputForm = true`.
- `normalizePoj*` runs a strict KPL → POJ pre-pass: `Tsai` → `Chai`.
- A tone digit glued to a checked syllable in input form is consumed in 0.6.0: `gah1` → `gah`.
- From `POJ_INPUT`, `ou` is read as `oo`, but `ou` never validates.

## Usage patterns

- "Convert this POJ input `tai5-gi2` to Unicode."
- "Convert this POJ Unicode text to KPL."
- "Normalize the tone marks in `Ta̍i-gi̍`."
- "Is `chn̂g` a valid POJ syllable?"
- "Fix the spacing in this Han-Lo sentence: `我 是 lâng , Lí hó .`" (then also read `taigi-han-lo-formatter`)

## Resources

- `references/linguistic_rules.md`: tone placement and orthographic differences in full. **Read before complex conversions.**
- `references/api_summary.md`: every public method, `ConvertOptions`, known behaviours, Gradle wiring.
- `references/format_examples.md`: the four formats with worked conversion and normalization examples.
