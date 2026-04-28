---
name: taigi-legacy-encoding-converter
description: Expertise in converting legacy Taigi Pe̍h-ōe-jī (POJ) encodings, font-hacks, and number formats to modern Unicode.
---

# KonvertLegacyPOJ

## Overview

This skill specializes in recovering and converting legacy Taigi text from outdated encodings and "font-hack" formats (like `tws21.ttf`) into standard modern Unicode POJ.

## Conversion Process

1.  **Identify Encoding:** Check for characteristic character remappings (e.g., unusual accented letters in Latin-1 range, `ä` $\rightarrow$ `ā`).
2.  **Map to Unicode:** Use authoritative mapping tables (see references) to replace legacy codepoints with standard Unicode base characters + combining diacritics.
3.  **NFC Normalize:** Always normalize the output to Unicode NFC form.

## Core Capabilities

### 1. Legacy Format Conversion
- **Number Format** $\rightarrow$ **Unicode**: `a2` $\rightarrow$ `á`, `ou3` $\rightarrow$ `ò͘`.
- **TP Encoding** $\rightarrow$ **Unicode**: Handles tones 7/8 and `ou` digraphs.
- **HOTSYS 2000** $\rightarrow$ **Unicode**: A number format and font hack.
    *   **CRITICAL RULE:** Swaps tones 2 and 3 for **UPPERCASE** `OU` only (`OU2` $\rightarrow$ grave, `OU3` $\rightarrow$ acute). Lowercase `ou` is **NOT** swapped.
- **CTS Tai-lo/POJ** $\rightarrow$ **Unicode**: Formats used by SinBongAi CTS in early Taigi web forums.

### 2. Font-Hack Recovery
- **TP Font Hack** (`tws21.ttf`) $\rightarrow$ **Unicode**: Recovers text displayed using legacy font diacritic mapping (e.g., `ä` $\rightarrow$ `ā`).
- **HOTSYS Font Hack** $\rightarrow$ **Unicode**: Recovers text from HOTSYS legacy font systems.

### 3. Unicode $\rightarrow$ Number Format
- Reverse conversion from modern Unicode back to legacy number format notation (e.g., `á` $\rightarrow$ `a2`).

## Supported Mappings

- **NumberToUnicode**: 93 entries.
- **TpToUnicode**: 53 entries.
- **HotsysToUnicode**: 83 entries.
- **UnicodeToNumber**: 191 entries.
- **Font-Hack Tables**: Specialized maps for TP and HOTSYS font systems.

## Resources

### references/
- `encoding_mappings.md`: Detailed tables for TP, HOTSYS, and CTS mappings.
- `usage_examples.md`: Code snippets for different conversion directions.
