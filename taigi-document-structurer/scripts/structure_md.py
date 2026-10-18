#!/usr/bin/env python3
"""structure_md.py — cleaned Taigi text → structured Markdown (YAML title/author,
H1/H2 headings, pandoc verse line blocks).

Usage:
  structure_md.py <fixed.txt> -o <out.md> [--raw <raw.txt>] [--title "<canonical title>"]

--raw   stage-1 textutil output; enables verse detection from indent depth
--title defaults to the input filename with NN_ prefix, _fixed/_raw/_structured
        suffix and 《》 stripped (NFC-normalized: macOS filenames are NFD)

Heuristics:
- H1: first non-blank line (book title)
- Byline: second non-blank line, rendered as italic paragraph
- H2: short (≤ 40 chars) line that does NOT end in 。！？, followed by ≥1 blank
- Two-line H2: first line ends with em-dash continuation marker (－－/—/--),
  both lines short, followed by blank
- Pagination noise (any line containing PAGE or 【…】) at the tail is dropped
- The very last non-blank line in the file is NOT promoted to H2 (avoids
  treating the closing sentence of the last chapter as a heading)
"""
import re
import sys
import unicodedata
from pathlib import Path

HEADER_MAX_LEN = 40
TERMINAL_PUNCT = "。！？"
CONTINUATION_SUFFIX = ("－－", "——", "--")
NOISE_RE = re.compile(r"PAGE|【.*】")
PART_RE = re.compile(r"^第\s*\d+\s*pha(?![A-Za-z])")   # 第N pha：… top-level part marker
FOOTNOTE_RE = re.compile(r"^[（(]\d+[）)]")             # （1）：… footnote entry
HAN_RE = re.compile(r"[\u3400-\u9fff]")
BYLINE_MAX_LEN = 20


def is_short(s: str) -> bool:
    return 0 < len(s) <= HEADER_MAX_LEN


def is_title_candidate(s: str) -> bool:
    return (
        is_short(s) and bool(s)
        and s[-1] not in TERMINAL_PUNCT
        and not s.startswith(("－", "—", "--"))  # quote/attribution prefix, not a chapter
    )


def ends_with_continuation(s: str) -> bool:
    return any(s.endswith(suffix) for suffix in CONTINUATION_SUFFIX)


def is_byline(s: str) -> bool:
    """Author line: very short, no colon, not a part/section marker."""
    return (
        0 < len(s) <= BYLINE_MAX_LEN
        and "：" not in s and ":" not in s
        and not PART_RE.match(s)
        and not s.startswith("♣")
    )


def heading_level(s: str) -> int:
    """第N pha：… parts are H1; every other detected heading is H2."""
    return 1 if PART_RE.match(s) else 2


def tidy_heading(s: str) -> str:
    """Normalize ♣-decorated section titles to `♣ text ♣`."""
    m = re.fullmatch(r"♣\s*(.*?)\s*♣", s)
    return f"♣ {m.group(1)} ♣" if m else s


def is_verse_line(s: str) -> bool:
    """A plausible poem line: short, not dialogue, not a footnote, no sentence end."""
    return (
        is_short(s)
        and not FOOTNOTE_RE.match(s)
        and not s.startswith(("「", "『", "（", "(", "－", "—", "--"))
        and s[-1] not in "。！？」』"
    )


def trim_tail_noise(lines: list[str], canonical_title: str = "") -> list[str]:
    """Drop trailing pagination noise plus textutil's running header/footer
    echo of the document title (Hanji form, and the roman-orthography twin
    that sits right next to it)."""
    end = len(lines)
    dropped_title = False
    while end > 0:
        s = lines[end - 1].strip()
        if not s or NOISE_RE.search(s):
            end -= 1
            continue
        if canonical_title and s.replace(" ", "") == canonical_title:
            end -= 1
            dropped_title = True
            continue
        if dropped_title and is_short(s) and not HAN_RE.search(s):
            end -= 1
            continue
        break
    return lines[:end]


def append_blank(out: list[str]) -> None:
    if out and out[-1] != "":
        out.append("")


def classify_raw_paragraphs(raw_text: str) -> list[str]:
    """Replay PipelineFix.joinSoftWraps over the raw .doc extraction and
    label each emitted non-blank line.

    Stage 2 strips leading whitespace, so this is the only place where the
    original indent depth is still visible. Prose paragraphs use a 4-space
    indent; verse lines (poem quotes) use 5+ spaces, with right-aligned
    attribution lines led by tab. A run of ≥2 consecutive verse-candidate
    lines is the signal for a verse block.

    Documents whose paragraphs sit at column 0 (no indent at all) carry
    their poems as runs of ≥2 consecutive short column-0 lines bounded by
    blank lines; those are tagged verse too (see is_verse_line).

    Returns one tag per non-blank line emitted to fixed.txt, in order:
    'verse' for lines belonging to a verse block, 'prose' otherwise.
    """
    lines = raw_text.split("\n")
    entries: list[str] = []
    paragraph_open = False
    verse_run_start: int | None = None
    verse_run_count = 0
    bare_run: list[tuple[int, str]] = []   # (entry index, text) of standalone column-0 lines

    def end_verse_run() -> None:
        nonlocal verse_run_start, verse_run_count
        if verse_run_count >= 2 and verse_run_start is not None:
            for k in range(verse_run_start, verse_run_start + verse_run_count):
                entries[k] = "verse"
        verse_run_start = None
        verse_run_count = 0

    def end_bare_run() -> None:
        nonlocal bare_run
        if len(bare_run) >= 2 and all(is_verse_line(t) for _, t in bare_run):
            two_line_title = len(bare_run) == 2 and ends_with_continuation(bare_run[0][1])
            if not two_line_title:
                for k, _ in bare_run:
                    entries[k] = "verse"
        bare_run = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            end_verse_run()
            end_bare_run()
            paragraph_open = False
            i += 1
            continue

        starts_tab = line.startswith("\t")
        leading_spaces = len(line) - len(line.lstrip(" "))
        is_verse_candidate = starts_tab or leading_spaces >= 5
        is_prose_indent = (not starts_tab) and leading_spaces >= 4

        if is_verse_candidate or is_prose_indent:
            end_bare_run()
            entries.append("prose")
            paragraph_open = True
            if is_verse_candidate:
                if verse_run_start is None:
                    verse_run_start = len(entries) - 1
                    verse_run_count = 1
                else:
                    verse_run_count += 1
            else:
                end_verse_run()
            i += 1
            continue

        nxt1 = lines[i + 1] if i + 1 < len(lines) else ""
        nxt2 = lines[i + 2] if i + 2 < len(lines) else ""
        is_single_title = not nxt1.strip()
        is_two_title = (
            nxt1.strip() != ""
            and not (nxt1.startswith("    ") or nxt1.startswith("\t"))
            and not nxt2.strip()
        )
        standalone = not paragraph_open   # not a soft-wrap continuation
        if is_single_title:
            end_verse_run()
            entries.append("prose")
            if standalone:
                bare_run.append((len(entries) - 1, line.strip()))
            else:
                end_bare_run()
            paragraph_open = False
            i += 1
        elif is_two_title:
            end_verse_run()
            entries.append("prose")
            entries.append("prose")
            if standalone:
                bare_run.append((len(entries) - 2, line.strip()))
                bare_run.append((len(entries) - 1, nxt1.strip()))
            else:
                end_bare_run()
            paragraph_open = False
            i += 2
        else:
            end_verse_run()
            if not paragraph_open:
                entries.append("prose")
                bare_run.append((len(entries) - 1, line.strip()))
            i += 1
    end_verse_run()
    end_bare_run()
    return entries

def structure(text: str, canonical_title: str = "", raw_text: str = "") -> str:
    lines = trim_tail_noise([l.rstrip() for l in text.split("\n")], canonical_title)
    if not lines:
        return ""

    # Index of the very last non-blank line — never promoted to a heading.
    last_content_idx = max(i for i, l in enumerate(lines) if l.strip())

    # Map fixed.txt line index → raw classification ('verse'/'prose').
    raw_classes = classify_raw_paragraphs(raw_text) if raw_text else []
    line_class: dict[int, str] = {}
    nb = 0
    for idx, l in enumerate(lines):
        if l.strip():
            if nb < len(raw_classes):
                line_class[idx] = raw_classes[nb]
            nb += 1

    out: list[str] = []
    i = 0

    # YAML metadata — pandoc maps `title` to Word's Title style and
    # `author` to Word's Author style automatically.
    title = canonical_title
    author = ""
    article_title = ""

    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        first = lines[i].strip()
        # textutil sometimes concatenates a cover title and a section title
        # into one line (e.g. canonical "Pha荒ê故事" → article "Pha荒ê故事ê故事").
        # When we know the canonical title from the filename and the first line
        # begins with it, treat that first line as the article H1 instead of
        # the YAML title; otherwise the first line IS the title.
        if canonical_title and first.replace(" ", "") == canonical_title:
            # First line IS the document title — keep it in YAML only, no duplicate H1.
            title = canonical_title
            i += 1
        elif canonical_title and is_short(first) and first.startswith(canonical_title):
            article_title = first
            i += 1
        else:
            title = first
            i += 1

    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and is_byline(lines[i].strip()):
        author = lines[i].strip()
        i += 1

    out.append("---")
    if title:
        out.append(f"title: {title}")
    if author:
        out.append(f"author: {author}")
    out.append("---")
    out.append("")
    if article_title:
        out.append(f"# {article_title}")
        out.append("")

    while i < len(lines):
        line = lines[i].strip()
        nxt1 = lines[i + 1].strip() if i + 1 < len(lines) else ""
        nxt2 = lines[i + 2].strip() if i + 2 < len(lines) else ""

        if not line:
            append_blank(out)
            i += 1
            continue

        # Verse block — consecutive lines tagged 'verse' from raw classification.
        # Emit as a Pandoc line block (`| line`) so pandoc renders one docx
        # paragraph with internal line breaks instead of N stand-alone paragraphs.
        if line_class.get(i) == "verse":
            append_blank(out)
            while i < len(lines) and lines[i].strip() and line_class.get(i) == "verse":
                out.append(f"| {lines[i].strip()}")
                i += 1
            out.append("")
            continue

        # Notes heading: short line ending in a dash marker, directly followed
        # by the first footnote entry （1）：…
        if (is_title_candidate(line) and ends_with_continuation(line)
                and FOOTNOTE_RE.match(nxt1)):
            append_blank(out)
            out.append(f"## {line}")
            out.append("")
            i += 1
            continue

        # 2-line title: first ends with em-dash continuation, both short, then blank
        if (is_title_candidate(line) and ends_with_continuation(line)
                and is_title_candidate(nxt1) and not nxt2
                and i + 1 != last_content_idx):
            append_blank(out)
            heading = tidy_heading(f"{line} {nxt1}")
            out.append(f"{'#' * heading_level(line)} {heading}")
            out.append("")
            i += 2
            continue

        # 1-line title
        if (is_title_candidate(line) and not nxt1
                and i != last_content_idx):
            append_blank(out)
            out.append(f"{'#' * heading_level(line)} {tidy_heading(line)}")
            out.append("")
            i += 1
            continue

        # Regular paragraph — emit followed by blank so pandoc treats each
        # source line as its own docx paragraph (not joined into one block).
        out.append(line)
        out.append("")
        i += 1

    # Collapse runs of blank lines
    cleaned: list[str] = []
    prev_blank = False
    for l in out:
        if not l:
            if prev_blank:
                continue
            prev_blank = True
        else:
            prev_blank = False
        cleaned.append(l)
    return "\n".join(cleaned).rstrip() + "\n"


def main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Structure cleaned Taigi text into Markdown with YAML title/author, "
                    "H1/H2 headings and verse line blocks.")
    ap.add_argument("fixed", help="cleaned text (stage-2 output)")
    ap.add_argument("-o", "--output", required=True, help="Markdown file to write")
    ap.add_argument("--raw", help="stage-1 raw textutil output; enables verse detection")
    ap.add_argument("--title", help="canonical title (default: derived from the input filename)")
    a = ap.parse_args(argv[1:])

    src = Path(a.fixed)
    if not src.exists():
        print(f"missing: {src}", file=sys.stderr)
        return 1
    title = a.title
    if title is None:
        title = re.sub(r"^\d+_", "", src.stem)
        title = re.sub(r"_(fixed|raw|structured)$", "", title)
    canonical = unicodedata.normalize("NFC", title.strip("《》"))
    raw_text = Path(a.raw).read_text(encoding="utf-8") if a.raw else ""
    out = Path(a.output)
    out.write_text(structure(src.read_text(encoding="utf-8"), canonical, raw_text),
                   encoding="utf-8")
    print(f"structured → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
