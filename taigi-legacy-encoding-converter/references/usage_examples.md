# KonvertLegacyPOJ usage

Kotlin Multiplatform (JVM, JS, macOS, iOS, Linux), zero dependencies. Package `taibun.kesimi.poj`, object `KonvertLegacyPOJ`. Every public function is a pure `String → String` pass that applies one replacement map to the whole input.

## Gradle wiring

The coordinate `io.github.pehoeji:konvert-legacy-poj:0.1.0` is **not on Maven Central** (checked 2026-10). Add the repository as a git submodule and substitute the coordinate with an included build:

```kotlin
// settings.gradle.kts
includeBuild("KonvertLegacyPOJ") {
    dependencySubstitution {
        substitute(module("io.github.pehoeji:konvert-legacy-poj")).using(project(":"))
    }
}

// build.gradle.kts of the consuming module
dependencies {
    implementation("io.github.pehoeji:konvert-legacy-poj:0.1.0")
}
```

Requires JDK 17+ (Gradle 8.10 cannot parse JDK 25's version string; pin `JAVA_HOME`).

## Functions

```kotlin
import taibun.kesimi.poj.KonvertLegacyPOJ

// Number format → Unicode (93 entries)
KonvertLegacyPOJ.convertLegacyNumberFormatToUnicode("a2")        // → "á"
KonvertLegacyPOJ.convertLegacyNumberFormatToUnicode("ou3")       // → "ò͘"

// TP encoding → Unicode (tones 7/8 + ou/m/n digraphs only, 53 entries)
KonvertLegacyPOJ.convertLegacyTpEncodingToUnicode("a7")          // → "ā"
KonvertLegacyPOJ.convertLegacyTpEncodingToUnicode("ou")          // → "o͘"

// HOTSYS 2000 number format → Unicode (83 entries; OU2/OU3 swapped)
KonvertLegacyPOJ.convertLegacyHotsys2000ToUnicode("OU2")         // → "Ò͘"

// Unicode → number format (reverse, 191 entries)
KonvertLegacyPOJ.convertUnicodeToLegacyNumberFormat("á")         // → "a2"
KonvertLegacyPOJ.convertUnicodeToLegacyNumberFormat("ò͘")        // → "ou3"

// TP font hack (tws21.ttf) → Unicode
KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode("ä")           // → "ā"
KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode("²")           // → "ô͘"

// HOTSYS font hack → Unicode
KonvertLegacyPOJ.convertLegacyHotsysFontHackToUnicode("¡")       // → "á"
KonvertLegacyPOJ.convertLegacyHotsysFontHackToUnicode("¬")       // → "Ò͘"

// TP POJ format → Unicode (full coverage a2–u9, ou, nn)
KonvertLegacyPOJ.convertLegacyTpPojToUnicode("a2")               // → "á"

// HOTSYS POJ format → Unicode (TP map + OU overrides; OU2/OU3 swapped)
KonvertLegacyPOJ.convertLegacyHotsysPojToUnicode("OU2")          // → "Ò͘"
KonvertLegacyPOJ.convertLegacyHotsysPojToUnicode("OU3")          // → "Ó͘"

// CTS Tai-lo → Unicode
KonvertLegacyPOJ.convertCtsTaiLoToUnicode("OO2")                 // → "ÓO"
KonvertLegacyPOJ.convertCtsTaiLoToUnicode("a9")                  // → "ă"

// CTS POJ → Unicode (OU/Ou swapped; lowercase ou not swapped)
KonvertLegacyPOJ.convertCtsPojToUnicode("OU2")                   // → "Ò͘"
KonvertLegacyPOJ.convertCtsPojToUnicode("ou2")                   // → "ó͘"
```

## Whole-document recipe

```kotlin
val unicode = KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode(rawText)   // 1. recover diacritics
val kana    = restoreLegacyKana(unicode)                                   // 2. PUA → kana (see SKILL.md)
// 3. hand off to KonvertToPoj.normalizePojHybridHanLoAutoChoanLoOrHanLoPunctuation
```

A full working example, including the foreign-word shielding that must wrap step 3, is `taigi-doc-pipeline/assets/pipeline/src/main/kotlin/taibun/pipeline/PipelineFix.kt`.

## Library commands

```bash
./gradlew jvmTest                                                        # all tests
./gradlew jvmTest --tests "taibun.kesimi.poj.KonvertLegacyPOJTest"       # one class
./gradlew jvmTest --tests "taibun.kesimi.poj.GenerateFileTest"           # file converter demo
```
