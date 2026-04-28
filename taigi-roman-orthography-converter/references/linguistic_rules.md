# Taigi Roman Orthography Linguistic Rules

These rules govern the conversion between POJ (Pe̍h-ōe-jī) and KPL (Kàu-io̍k Pō͘ Lô-má-jī) Roman Orthography.

## 1. Orthographic Differences

| Feature | POJ | KPL |
| :--- | :--- | :--- |
| **Initials** | `ch` / `chh` | `ts` / `tsh` |
| **Vowels** | `oa` / `oe` | `ua` / `ue` |
| **Finals** | `ek` / `eng` | `ik` / `ing` |
| **Open 'o'** | `o͘` (o + U+0358) | `oo` |
| **Nasalization** | `ⁿ` (U+207F) | `nn` |
| **Tone 9 mark** | `ă` (breve U+0306) | `a̋` (double acute U+030B) |

## 2. Tone Placement Rules

### POJ Rules (Section 21)
1.  **Single vowel:** Mark the vowel.
2.  **No vowel:** Mark the nasal (`m`, `n`, `ng` — treat `ng` as 1 unit).
3.  **Compound vowels:** Mark the 2nd letter from the right (skipping `ⁿ`, treating `ng` as 1 unit).
    *   **Exception 1:** If 2nd from right is `i` → mark 1st (rightmost) letter instead.
    *   **Exception 2:** Checked syllable + 2nd from right is `i`/`u` (but not `iu`/`iuh`) → mark 3rd letter.
    *   **Special:** `iuh` → mark 2nd from right.

### KPL Rules (Section 45)
1.  **If `a` is present:** Mark the `a`.
2.  **Else:** Mark the rightmost vowel (treating `oo` as a unit, mark the left `o`).
3.  **Else:** Mark the nasal (`ng` as unit, then `m`, then `n`).

## 3. Syllable Structure & Tones
*   **Standard Tones:** 1, 2, 3, 4, 5, 7, 8, 9 (Tone 6 does not exist).
*   **Checked Tones (4/8):** Syllable MUST end in `p`, `t`, `k`, or `h`. Non-checked syllables cannot have tones 4/8.
*   **Tone 8 mark:** U+030D (combining vertical line above).

## 4. Special Characters (Unicode)
*   `o͘`: `o` + U+0358 (combining dot above right).
*   `ⁿ`: U+207F (superscript n).
*   `ă`: U+0306 (breve).
*   `a̋`: U+030B (double acute accent).
