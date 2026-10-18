#!/usr/bin/env bash
# Stage 2: 01_*_raw.txt → 02_*_fixed.txt
# Applies:
#   1. KonvertLegacyPOJ.convertLegacyTpFontHackToUnicode (TP font-hack → Unicode POJ)
#   2. KonvertToPoj.normalizePojHanLo (Han-Lo spacing/tone normalization)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DST_DIR="${ROOT}/doc_result"

# Gradle 8.10 (used by submodules) doesn't parse JDK 25's version string;
# pin to JDK 17 if available.
if [[ -z "${JAVA_HOME:-}" ]] || ! "$JAVA_HOME/bin/java" -version 2>&1 | grep -qE 'version "1[78]\.|version "21\.'; then
    if jh="$(/usr/libexec/java_home -v 17 2>/dev/null)"; then
        export JAVA_HOME="$jh"
    elif jh="$(/usr/libexec/java_home -v 21 2>/dev/null)"; then
        export JAVA_HOME="$jh"
    fi
fi

if [[ $# -ge 1 ]]; then
    titles=("$@")
else
    titles=()
    while IFS= read -r f; do
        b="$(basename "$f")"
        b="${b#01_}"
        b="${b%_raw.txt}"
        titles+=("$b")
    done < <(find "$DST_DIR" -maxdepth 1 -name '01_*_raw.txt')
fi

for title in "${titles[@]}"; do
    in="${DST_DIR}/01_${title}_raw.txt"
    out="${DST_DIR}/02_${title}_fixed.txt"
    [[ -f "$in" ]] || { echo "missing: $in" >&2; exit 1; }
    # Use absolute paths — gradle's working dir differs from this script's
    in_abs="$(cd "$(dirname "$in")" && pwd)/$(basename "$in")"
    out_abs="$(cd "$(dirname "$out")" && pwd)/$(basename "$out")"
    (cd "$ROOT" && ./gradlew --quiet :pipeline:run --args="\"$in_abs\" \"$out_abs\"")
done
