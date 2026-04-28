#!/usr/bin/env python3
"""Force every text run in a docx body to carry an explicit GenYoMin2 TW font.

Pandoc emits body content with empty <w:rFonts w:hint="eastAsia"/> tags and
many bare runs (no rPr at all). Even if the reference.docx styles set fonts,
some renderers (LibreOffice in particular) don't always inherit through the
style chain. We inject explicit fonts inline so every glyph is locked to
GenYoMin2 TW regardless of style inheritance behavior.

Usage: apply_fonts_to_docx.py <input.docx> <output.docx>
"""
import re
import sys
import zipfile
from pathlib import Path

FONT_FAMILY = "GenYoMin2 TW"
BODY_FONT = FONT_FAMILY
HEADING_FONT = FONT_FAMILY  # Bold via <w:b/> in style; no separate face name.
LANG_XML = '<w:lang w:val="en-US" w:eastAsia="zh-TW"/>'

# 避頭尾 (kinsoku) line-break rules. Each character set is matched against
# the script-appropriate language of the surrounding run:
#   "-" is Latin script  → matched against w:val=en-US
#   Chinese punctuation is East Asian → matched against w:eastAsia=zh-TW
#
# 行頭 (no-start-line) — closing punctuation, dashes, ellipsis cannot
# begin a wrapped line; they stay attached to the preceding text.
# 行尾 (no-end-line) — opening punctuation cannot end a line.
# LibreOffice ignores Latin chars in en-US kinsoku lists, but it scans
# the entire char list of the East Asian rule against every char in the
# document. So we put "-" inside the zh-TW list to get it treated as a
# kinsoku-protected character without changing the underlying Unicode.
NO_START_LINE_LATIN = ""
NO_START_LINE_CJK   = "，。、；：？！）」』】〕》〉．-"
NO_END_LINE_LATIN   = ""
NO_END_LINE_CJK     = "（「『【〔《〈-"

def _rule(elem: str, lang: str, chars: str) -> str:
    return f'<w:{elem} w:lang="{lang}" w:val="{chars}"/>' if chars else ""


LINE_BREAK_RULES = (
    '<w:strictFirstAndLastChars w:val="1"/>'
)


def patch_settings(xml: str) -> str:
    # Drop our own previous injections (idempotent).
    xml = re.sub(r'<w:strictFirstAndLastChars[^>]*/>', '', xml)
    xml = re.sub(r'<w:noLineBreaks(After|Before)[^/]*/>', '', xml)
    # <w:kinsoku> is a paragraph property, not a setting. LINE_BREAK_RULES 
    # defines the custom line break characters for the document.
    # We must insert them before savePreviewPicture, rsids, mathPr to satisfy schema.
    match = re.search(r'<(w:savePreviewPicture|w:rsids|m:mathPr|w:themeFontLang|w:clrSchemeMapping|w:doNotValidateBeforeSave|w:decimalSymbol|w:listSeparator|w:smartTagType)[ />]', xml)
    if match:
        return xml[:match.start()] + LINE_BREAK_RULES + xml[match.start():]
    return xml.replace('</w:settings>',
                       f'{LINE_BREAK_RULES}</w:settings>', 1)


def font_xml(font: str) -> str:
    return (f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" '
            f'w:eastAsia="{font}" w:cs="{font}"/>')


EMPTY_PARAGRAPH = '<w:p/>'

def patch_styles(xml: str) -> str:
    WORD_WRAP_ON = '<w:kinsoku w:val="1"/><w:wordWrap w:val="1"/>'
    
    def inject(m: re.Match) -> str:
        block = m.group(0)
        # Sequence: wordWrap comes before spacing, ind, jc, rPr.
        # In the reference docx, Normal and pPrDefault always have <w:spacing.
        # We put wordWrap just before it.
        if "<w:spacing" in block:
            return block.replace("<w:spacing", f"{WORD_WRAP_ON}<w:spacing", 1)
        elif "<w:ind" in block:
            return block.replace("<w:ind", f"{WORD_WRAP_ON}<w:ind", 1)
        elif "<w:jc" in block:
            return block.replace("<w:jc", f"{WORD_WRAP_ON}<w:jc", 1)
        elif "<w:rPr" in block:
            return block.replace("<w:rPr", f"{WORD_WRAP_ON}<w:rPr", 1)
        return block.replace("</w:pPr>", f"{WORD_WRAP_ON}</w:pPr>", 1)

    xml = re.sub(r'<w:style [^>]*w:styleId="Normal"[^>]*>.*?</w:style>', inject, xml, flags=re.DOTALL)
    xml = re.sub(r'<w:pPrDefault>.*?</w:pPrDefault>', inject, xml, flags=re.DOTALL)
    
    # Also inject into FirstParagraph and BodyText styles since Pandoc explicitly uses them
    xml = re.sub(r'<w:style [^>]*w:styleId="FirstParagraph"[^>]*>.*?</w:style>', inject, xml, flags=re.DOTALL)
    xml = re.sub(r'<w:style [^>]*w:styleId="BodyText"[^>]*>.*?</w:style>', inject, xml, flags=re.DOTALL)
    return xml



# Styles after which we do NOT add a trailing empty paragraph (headings,
# title block, etc. have their own spacing in styles.xml).
NO_TRAILING_EMPTY = re.compile(r'w:pStyle\s+w:val="(Heading|Title|Author|Subtitle|Date|Abstract)')


def patch_document(xml: str) -> str:
    """Walk every <w:p> and rewrite its runs to use the right font.
       Also insert an empty paragraph after each body content paragraph."""

    def in_heading(p_block: str) -> bool:
        return bool(re.search(r'w:pStyle\s+w:val="(Heading|Title)', p_block))

    def patch_paragraph(p_match: re.Match) -> str:
        p_block = p_match.group(0)
        font = HEADING_FONT if in_heading(p_block) else BODY_FONT
        rprops = font_xml(font)

        WORD_WRAP_ON = '<w:kinsoku w:val="1"/><w:wordWrap w:val="1"/>'
        # Strip any existing wordWrap/kinsoku first
        p_block = re.sub(r"<w:wordWrap[^/]*/>", "", p_block)
        p_block = re.sub(r"<w:kinsoku[^/]*/>", "", p_block)

        def inject_ppr(m: re.Match) -> str:
            block = m.group(0)
            if "<w:spacing" in block:
                return block.replace("<w:spacing", f"{WORD_WRAP_ON}<w:spacing", 1)
            elif "<w:ind" in block:
                return block.replace("<w:ind", f"{WORD_WRAP_ON}<w:ind", 1)
            elif "<w:jc" in block:
                return block.replace("<w:jc", f"{WORD_WRAP_ON}<w:jc", 1)
            elif "<w:rPr" in block:
                return block.replace("<w:rPr", f"{WORD_WRAP_ON}<w:rPr", 1)
            return block.replace("</w:pPr>", f"{WORD_WRAP_ON}</w:pPr>", 1)

        if "<w:pPr>" in p_block or "<w:pPr " in p_block or "<w:pPr/>" in p_block:
            p_block = re.sub(r"<w:pPr(?:\s[^>]*)?>.*?</w:pPr>", inject_ppr, p_block, flags=re.DOTALL)
            p_block = re.sub(r"<w:pPr\s*/>", f"<w:pPr>{WORD_WRAP_ON}</w:pPr>", p_block, flags=re.DOTALL)
        else:
            # No pPr at all — insert before first <w:r>
            p_block = re.sub(r"(<w:p[ >][^>]*>)", rf"\1<w:pPr>{WORD_WRAP_ON}</w:pPr>", p_block, count=1)

        def patch_run(r_match: re.Match) -> str:
            r_block = r_match.group(0)
            # Strip any existing rFonts (incl. the empty hint-only ones) and lang
            r_block = re.sub(r"<w:rFonts[^/]*/>", "", r_block)
            r_block = re.sub(r"<w:lang[^/]*/>", "", r_block)
            full_rprops = rprops + LANG_XML

            if "<w:rPr>" in r_block:
                r_block = r_block.replace("<w:rPr>", f"<w:rPr>{full_rprops}", 1)
            elif "<w:rPr/>" in r_block:
                r_block = r_block.replace("<w:rPr/>", f"<w:rPr>{full_rprops}</w:rPr>")
            else:
                # Bare <w:r> with no run properties — give it some.
                r_block = r_block.replace("<w:r>", f"<w:r><w:rPr>{full_rprops}</w:rPr>", 1)

            if "-" not in r_block:
                return r_block

            prefix_match = re.match(r"^(<w:r(?: [^>]*)?>.*?<w:rPr>.*?</w:rPr>)", r_block, flags=re.DOTALL)
            prefix = prefix_match.group(1) if prefix_match else f"<w:r><w:rPr>{full_rprops}</w:rPr>"

            def split_text(m: re.Match) -> str:
                t_open, text, t_close = m.group(1), m.group(2), m.group(3)
                if "-" not in text:
                    return m.group(0)
                
                parts = text.split("-")
                runs = []
                for i, p in enumerate(parts):
                    if p:
                        runs.append(f"{t_open}{p}{t_close}")
                    if i < len(parts) - 1:
                        runs.append(f"</w:r>{prefix}<w:noBreakHyphen/></w:r>{prefix}")
                
                return "".join(runs)

            r_block = re.sub(r"(<w:t(?: [^>]*)?>)(.*?)(</w:t>)", split_text, r_block, flags=re.DOTALL)
            # Clean up empty runs created by hyphens at the edges or adjacent hyphens
            r_block = r_block.replace(f"{prefix}</w:r>", "")
            return r_block

        patched = re.sub(r"<w:r(?: [^>]*)?>.*?</w:r>", patch_run, p_block, flags=re.DOTALL)

        # Trailing empty paragraph for body content only.
        if not NO_TRAILING_EMPTY.search(p_block):
            patched += EMPTY_PARAGRAPH
        return patched

    return re.sub(r"<w:p[ >].*?</w:p>", patch_paragraph, xml, flags=re.DOTALL)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: apply_fonts_to_docx.py <input.docx> <output.docx>", file=sys.stderr)
        return 1
    src, dst = Path(argv[1]), Path(argv[2])

    with zipfile.ZipFile(src, "r") as zin:
        document = zin.read("word/document.xml").decode("utf-8")
        settings = zin.read("word/settings.xml").decode("utf-8")
        styles = zin.read("word/styles.xml").decode("utf-8")
    patched_doc = patch_document(document)
    patched_settings = patch_settings(settings)
    patched_styles = patch_styles(styles)

    if dst.exists():
        dst.unlink()
    with zipfile.ZipFile(src, "r") as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            if item == "word/document.xml":
                data = patched_doc.encode("utf-8")
            elif item == "word/settings.xml":
                data = patched_settings.encode("utf-8")
            elif item == "word/styles.xml":
                data = patched_styles.encode("utf-8")
            else:
                data = zin.read(item)
            zout.writestr(item, data)
    print(f"applied fonts → {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
