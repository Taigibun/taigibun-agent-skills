# Formats and conversion examples

## The four formats

| Format | Example | Description |
| :-- | :-- | :-- |
| `POJ_INPUT` | `chit8-e5` | POJ with tone numbers, ASCII-safe (`oo` for `o͘`, `nn` for `ⁿ`) |
| `POJ_UNICODE` | `chi̍t-ê` | POJ with tone diacritics (`o͘` = o + U+0358, `ⁿ` = U+207F) |
| `KPL_INPUT` | `tsit8-e5` | KPL with tone numbers |
| `KPL_UNICODE` | `tsi̍t-ê` | KPL with tone diacritics |

Tone digits: `2 3 5 7 8 9`; tone 1 and 4 are unmarked (`1`/`4` typed are dropped). Tones 4 and 8 require a final `p t k h`. Tone 9 is `ă` (breve) in POJ and `a̋` (double acute) in KPL.

## Conversions

```kotlin
import tw.poj.kesi.konverttopoj.KonvertToPoj
import tw.poj.kesi.konverttopoj.LomajiFormat.*

KonvertToPoj.convert("tai5-gi2", POJ_INPUT, POJ_UNICODE)        // → "Tâi-gí"
KonvertToPoj.convert("Tâi-gí", POJ_UNICODE, POJ_INPUT)          // → "tai5-gi2"
KonvertToPoj.convert("chit8-e5", POJ_INPUT, KPL_INPUT)          // → "tsit8-e5"
KonvertToPoj.convert("goo2-kong7 e7-hiau2 oh8 tai5-gi2", POJ_INPUT, KPL_UNICODE)
                                                                // → "góo-kōng ē-hiáu o̍h tâi-gí"
KonvertToPoj.convert("connecting chi̍t", POJ_UNICODE, KPL_UNICODE)
                                                                // → "connecting tsi̍t"
KonvertToPoj.convert("hōe goa2", POJ_UNICODE, KPL_UNICODE)      // → "huē goa2"   (digits ignored)
KonvertToPoj.convert("hōe goa2", POJ_UNICODE, KPL_UNICODE, ConvertOptions(viaInputForm = true))
                                                                // → "huē guá"
KonvertToPoj.convert("annh8", POJ_INPUT, POJ_UNICODE, ConvertOptions(traditionalNasal = true))
                                                                // → "a̍hⁿ"
```

## Hybrid text

```kotlin
KonvertToPoj.convertHybrid("1. tai5-oan5 2. tiong1-kok4", POJ_INPUT, POJ_UNICODE)
// → "1. tâi-oân 2. tiong-kok"
KonvertToPoj.convertHybrid("koe2(漳)/kor2(泉)", POJ_INPUT, POJ_UNICODE, ConvertOptions(haikau = true))
// → "kóe(漳)/kó̤(泉)"
```

## Han-Lo normalization

```kotlin
val text = "  góa   sī\tlâng ， 真 好 。"
KonvertToPoj.normalizePojHanLoForceUsingFullwidthPunctuation(text)
// → "góa sī lâng，真好。"
KonvertToPoj.normalizePojHanLoForceUsingFullwidthPunctuation(text, ConvertOptions(aggressiveWhitespace = false))
// → "  góa   sī\tlâng，真好。"
KonvertToPoj.normalizePoj("Ta̍i-gi̍")                            // → "Tâi-gí"  (tone marks re-placed)
```

## Orthographic differences at a glance

| Feature | POJ | KPL |
| :-- | :-- | :-- |
| Initials | `ch` / `chh` | `ts` / `tsh` |
| Vowels | `oa` / `oe` | `ua` / `ue` |
| Finals | `ek` / `eng` | `ik` / `ing` |
| Open o | `o͘` | `oo` |
| Nasalization | `ⁿ` | `nn` |
| Coastal vowels | `ur` / `or` (`ṳ` / `o̤`) | `ir` / `er` |
| Tone 9 | `ă` | `a̋` |
