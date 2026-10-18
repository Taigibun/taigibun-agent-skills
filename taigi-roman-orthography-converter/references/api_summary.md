# KonvertToPoj API summary (0.6.0)

Package `tw.poj.kesi.konverttopoj`, object `KonvertToPoj`. Every method also exists as a `String` extension (`"tai5-gi2".convertLomaji(POJ_INPUT, POJ_UNICODE)`). Zero dependencies; JVM, JS, Wasm, iOS.

## Formats (`LomajiFormat`)

`POJ_INPUT`, `POJ_UNICODE`, `KPL_INPUT`, `KPL_UNICODE`. See `format_examples.md`.

## Conversion

| Method | Behaviour |
| :-- | :-- |
| `convert(text, from, to, options)` | Any of the 12 directions. Only tokens that pass the **syllable-shape gate** are converted (`[onset] + 1–3 vowels + [nasal] + [coda] + [tone]`, or `[onset] + m/ng + [h] + [tone]`); everything else passes through, so `connecting` is never touched. |
| `convertHybrid(text, from, to, options)` | For Roman Orthography embedded in Hanji, numbering or annotations. Validates each token against the rhyme whitelist first; foreign words such as `Tennessee` survive. |

`POJ_UNICODE ↔ KPL_UNICODE` is **direct** by default: the tone is read off the diacritic, the letters are converted, the tone is re-placed by the target rules. Digits are never read as tones on that path. `ConvertOptions(viaInputForm = true)` restores the route through input form, where a trailing digit is a tone number.

From `POJ_INPUT`, `ou` is normalized to `oo` automatically (`gou2` → `gó͘`); validation does **not** accept `ou`.

## Validation

| Method | Behaviour |
| :-- | :-- |
| `isValidSyllable(syllable, format, options)` | Whitelist-based (initials + rhymes), strict per system: `ch`/`chh`/`oa`/`oe`/`ek`/`eng` are rejected as KPL, `ts`/`tsh`/`ua`/`ue`/`ik`/`ing` as POJ. |
| `isValidText(text, format, options)` | Every token must validate. The document pipeline uses it to decide which ASCII words are foreign. |

## Normalization (POJ)

| Method | Behaviour |
| :-- | :-- |
| `normalizePoj(text, options)` | Strict KPL → POJ pre-pass, then a Unicode → input → Unicode round trip that fixes tone placement and diacritic errors. |
| `normalizePojHybrid(text, options)` | Same, validation-gated for mixed text. |
| `normalizePojHanLoForceUsingFullwidthPunctuation(text, options)` | + Han-Lo spacing/hyphen rules, punctuation always full-width. |
| `normalizePojHanLoAutoChoanLoOrHanLoPunctuation(text, options)` | + Han-Lo rules; full-width punctuation in Han-Lo lines, half-width in all-Roman (Choân-Lô) lines. |
| `normalizePojHybridHanLoForceUsingFullwidthPunctuation(text, options)` | Hybrid variant of the above. |
| `normalizePojHybridHanLoAutoChoanLoOrHanLoPunctuation(text, options)` | Hybrid variant; the one the document pipeline calls. |

## `ConvertOptions`

| Option | Default | Effect |
| :-- | :-- | :-- |
| `traditionalNasal` | `false` | Accept `ⁿh` for `hⁿ` and `oⁿ` for `o͘ⁿ`; normalize to standard form. |
| `haikau` | `false` | Validate coastal-dialect vowels `ur`/`or` (POJ) and `ir`/`er` (KPL). `convert()` handles them regardless. |
| `aggressiveWhitespace` | `true` | HanLo methods only: rebuild canonical spacing (`true`) or keep the author's spacing except where rules forbid it (`false`). |
| `viaInputForm` | `false` | `POJ_UNICODE ↔ KPL_UNICODE` only: route through input form; trailing digits become tones. |

## Known behaviours to plan for

- `normalizePoj("Tsai")` → `"Chai"`: a token that is strictly valid KPL and not POJ is converted. Shield proper nouns.
- An input-form digit glued to a checked syllable is consumed: `gah1` → `gah`. A typed `1` or `4` is tolerated and dropped.
- Two conflicting tone marks on one syllable → left as-is.
- After a nasal onset (`m n ng`) the nasal marker is never written: `niû`, not `niûⁿ`.

## Gradle

`tw.poj.kesi:konvert-to-poj:0.6.0` (JVM-only artifact `konvert-to-poj-jvm`) is **not on Maven Central** (checked 2026-10). Add https://github.com/PehoejiKesi/KonvertToPOJ as a git submodule and use `includeBuild("KonvertToPOJ") { dependencySubstitution { substitute(module("tw.poj.kesi:konvert-to-poj")).using(project(":lib")) } }`. Requires JDK 17+.

Online converter covering every method: https://kesi.poj.tw/KonvertToPOJ/
