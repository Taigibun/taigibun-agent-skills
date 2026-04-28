---
name: taigi-roman-orthography-converter
description: Expertise in converting Taigi Roman Orthography between POJ (Pe̍h-ōe-jī) and KPL (Kàu-io̍k Pō͘ Lô-má-jī) in both Input (tone numbers) and Unicode (diacritics) formats.
---

# KonvertToPoj

## Guidelines

- **Orthography**: Always use the term **Roman Orthography** instead of "Romanization". Prefer **Taigi Latin-script Orthography** or **Taigi Roman-script Orthography**.
- **Naming**: Refer to the language as **Taigi**. Avoid "Taiwanese Southern Min", "Holo", or "Taiwanese Hokkien".

## Overview

This skill specializes in converting and normalizing Taigi Roman Orthography using the logic from the `KonvertToPoj` library. It handles 12 conversion directions between POJ/KPL and Input/Unicode formats.

## Core Capabilities

### 1. Format Conversion
- **POJ_INPUT** $\leftrightarrow$ **POJ_UNICODE**
- **KPL_INPUT** $\leftrightarrow$ **KPL_UNICODE**
- **POJ** $\leftrightarrow$ **KPL** (Cross-system)

### 2. Normalization
- **Tone-mark Placement**: Automatically moves tone marks to the correct vowel according to linguistic rules.
- **Han-Lo Spacing**: Fixes spacing and punctuation around Hanji and Roman Orthography.
- **Punctuation Width**: Converts between half-width and full-width punctuation based on the context.

### 3. Validation
- Validates syllables against linguistically correct Taiwanese phonotactics (whitelist-based).
- Validation-aware normalization (preserves foreign words like "Tennessee").

## Conversion Pipeline

When converting text manually or verifying logic, follow these steps:
1.  **Normalization:** Ensure input text is NFC-normalized.
2.  **Orthographic Mapping:** Swap initials, vowels, and finals based on the target system (e.g., POJ `ch` → KPL `ts`).
3.  **Tone Re-placement:** Re-calculate the position of tone marks based on the rules of the target system (POJ rules differ from KPL rules for compound vowels).
4.  **Special Characters:** Ensure correct Unicode representation for system-specific markers (e.g., POJ `o͘` vs KPL `oo`).

### Quick Reference Table

| Feature | POJ | KPL |
| :--- | :--- | :--- |
| **Initials** | `ch` / `chh` | `ts` / `tsh` |
| **Vowels** | `oa` / `oe` | `ua` / `ue` |
| **Open 'o'** | `o͘` | `oo` |
| **Nasalization** | `ⁿ` | `nn` |

## Usage Patterns

- "Convert this POJ input `tai5-gi2` to Unicode."
- "Normalize the tone marks in this text: `Ta̍i-gi̍`."
- "Fix the spacing in this Han-Lo sentence: `我 是 lâng , Lí hó .`"

## Resources

### references/
- `linguistic_rules.md`: Detailed linguistic rules for tone placement and system-specific differences. **MUST** read before complex conversions.
- `api_summary.md`: Summary of methods like `convertHybrid`, `isValidSyllable`, and `normalizePojHanLo`.
- `format_examples.md`: Table of formats (Input vs Unicode).
