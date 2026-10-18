# Stage 2: the fix pass

`assets/pipeline/src/main/kotlin/taibun/pipeline/PipelineFix.kt`, run by `scripts/02_fix.sh`
as `./gradlew --quiet :pipeline:run --args="<in> <out>"`.
Input `01_<title>_raw.txt`, output `02_<title>_fixed.txt`. The order matters.

| # | Pass | What and why |
| :-- | :-- | :-- |
| 1 | `joinSoftWraps` | Re-join Word's soft-wrapped lines into paragraphs (see `word-doc-extraction-quirks.md`), so spacing rules never run across false line ends. |
| 2 | `KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode` | TP font hack (tws21.ttf) → Unicode diacritics. Must precede normalization. |
| 3 | `shieldForeignWords` | Dotted abbreviations (≥ 2 `X.` pairs) and ASCII words of ≥ 2 letters that are not adjacent to a POJ letter and fail `KonvertToPoj.isValidText(word, POJ_UNICODE)` become placeholders `U+FDD0 n U+FDD1`. Following space-separated words with the same property join the same placeholder, so `Nelson Mandela` is one unit. |
| 4 | `.` → `U+FDD2` | Keeps decimal and abbreviation dots from becoming `。`. |
| 5 | `KonvertToPoj.normalizePojHybridHanLoAutoChoanLoOrHanLoPunctuation` | Tone-mark placement, Han-Lo spacing and hyphen rules, punctuation width (full-width in Han-Lo lines, half-width in all-Roman lines). |
| 6 | restore `.` | |
| 7 | `restoreLegacyKana` | PUA U+F6F7..U+F79F → hiragana/katakana. |
| 8 | `restoreForeignWords` | |
| 9 | `postFixPunctuation` | `X .` → `X.`, `. X` → `.X` (Latin letters), `aB` → `a B` (lowercase glued to uppercase), `」.` → `」。`. |

## Why a Kotlin app

Both libraries are Kotlin Multiplatform and are **not on Maven Central** (checked 2026-10). The
root `settings.gradle.kts` uses `includeBuild` on the two git submodules and substitutes the
Maven coordinates, so `:pipeline` depends on them by coordinate and Gradle builds them from
source. `02_fix.sh` pins `JAVA_HOME` to JDK 17 or 21 because Gradle 8.10 cannot parse JDK 25's
version string.

## Extending

Add new passes as pure `String → String` functions in `PipelineFix.kt` and keep the two library
calls untouched, so upstream library updates stay drop-in. Anything that is a general Taigi rule
belongs upstream in KonvertToPoj; anything specific to Word exports belongs here.
