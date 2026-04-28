#!/usr/bin/env python3
"""Inject GenYoMin2 TW font into a pandoc reference.docx.

Pandoc's --reference-doc inherits styles from this file. We need EVERY style
to carry an explicit <w:rFonts> set, otherwise body content using styles like
BodyText (which by default has no <w:rPr>) falls back to Calibri instead of
inheriting from rPrDefault under some renderers.
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "reference.docx"
DST = ROOT / "assets" / "reference_genyo.docx"

FONT_FAMILY = "GenYoMin2 TW"  # Use family name only — LibreOffice substitutes
                              # if a weight-suffixed face name is supplied.
BODY_FONT = FONT_FAMILY
HEADING_FONT = FONT_FAMILY    # Bold weight is requested via <w:b/> in the
                              # style's <w:rPr>, not via a separate face name.

# Paragraph spacing applied to every style's <w:pPr>.
# w:before/after = 120 twentieths-of-a-point ≈ 6pt above/below each paragraph.
# w:line = 360 + lineRule=auto → 1.5× line height (240 = single, 360 = 1.5×).
BODY_SPACING_XML = '<w:spacing w:before="120" w:after="120" w:line="360" w:lineRule="auto"/>'
HEADING_SPACING_XML = '<w:spacing w:before="360" w:after="240" w:line="360" w:lineRule="auto"/>'


# Mixed language tagging:
#   w:val      → language of LATIN runs (POJ, ASCII "-")
#   w:eastAsia → language of EAST ASIAN runs (Hanji)
# OOXML's noLineBreaksAfter/Before rules look up by the script-appropriate
# language: ASCII "-" matches against `w:val=en-US`, so the en-US kinsoku
# rule engages. Hanji uses zh-TW for typography decisions.
LANG_XML = '<w:lang w:val="en-US" w:eastAsia="zh-TW"/>'


def font_xml(font: str) -> str:
    return (f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" '
            f'w:eastAsia="{font}" w:cs="{font}"/>')


def patch_styles(xml: str) -> str:
    # Strip pre-existing rFonts and lang so we own those choices.
    xml = re.sub(r"<w:rFonts[^/]*/>", "", xml)
    xml = re.sub(r"<w:lang[^/]*/>", "", xml)

    # Ensure rPrDefault carries the body font + language tag.
    default_rpr = f"{font_xml(BODY_FONT)}{LANG_XML}"
    if "<w:rPrDefault>" in xml:
        if re.search(r"<w:rPrDefault>\s*<w:rPr>", xml):
            xml = re.sub(r"<w:rPrDefault>\s*<w:rPr>",
                         f"<w:rPrDefault><w:rPr>{default_rpr}",
                         xml, count=1)
        else:
            xml = xml.replace("<w:rPrDefault/>",
                              f"<w:rPrDefault><w:rPr>{default_rpr}</w:rPr></w:rPrDefault>")

    def patch_style(match: re.Match) -> str:
        block = match.group(0)
        sid_match = re.search(r'w:styleId="([^"]+)"', block)
        sid = sid_match.group(1) if sid_match else ""
        is_heading = sid.startswith("Heading") or sid == "Title"
        font = HEADING_FONT if is_heading else BODY_FONT
        rprops = font_xml(font) + ("<w:b/><w:bCs/>" if is_heading else "") + LANG_XML
        spacing = HEADING_SPACING_XML if is_heading else BODY_SPACING_XML

        # Drop any pre-existing spacing so we own paragraph spacing.
        block = re.sub(r"<w:spacing[^/]*/>", "", block)

        # rPr (font + optional bold)
        if re.search(r"<w:rPr\s*>", block):
            block = re.sub(r"<w:rPr\s*>", f"<w:rPr>{rprops}", block, count=1)
        elif "<w:rPr/>" in block:
            block = block.replace("<w:rPr/>", f"<w:rPr>{rprops}</w:rPr>")
        else:
            block = block.replace("</w:style>",
                                  f"<w:rPr>{rprops}</w:rPr></w:style>", 1)

        # pPr (spacing) — inject into existing or create new before <w:rPr>
        if re.search(r"<w:pPr\s*>", block):
            block = re.sub(r"<w:pPr\s*>", f"<w:pPr>{spacing}", block, count=1)
        elif "<w:pPr/>" in block:
            block = block.replace("<w:pPr/>", f"<w:pPr>{spacing}</w:pPr>")
        else:
            block = block.replace("<w:rPr>",
                                  f"<w:pPr>{spacing}</w:pPr><w:rPr>", 1)
        return block

    xml = re.sub(r"<w:style [^>]*>.*?</w:style>", patch_style, xml, flags=re.DOTALL)
    return xml


NO_START_LINE_CJK = "，。、；：？！）」』】〕》〉．-"
NO_END_LINE_CJK   = "（「『【〔《〈-"

LINE_BREAK_RULES = (
    '<w:strictFirstAndLastChars w:val="1"/>'
)


def patch_settings(xml: str) -> str:
    # Drop any prior rules we own.
    xml = re.sub(r'<w:strictFirstAndLastChars[^>]*/>', '', xml)
    xml = re.sub(r'<w:noLineBreaks(After|Before)[^/]*/>', '', xml)
    
    # OpenXML requires CT_Settings elements to be in a very specific sequence.
    # The Kinsoku elements must appear BEFORE savePreviewPicture, rsids, mathPr, etc.
    match = re.search(r'<(w:savePreviewPicture|w:rsids|m:mathPr|w:themeFontLang|w:clrSchemeMapping|w:doNotValidateBeforeSave|w:decimalSymbol|w:listSeparator|w:smartTagType)[ />]', xml)
    if match:
        return xml[:match.start()] + LINE_BREAK_RULES + xml[match.start():]
    return xml.replace('</w:settings>', f'{LINE_BREAK_RULES}</w:settings>', 1)


def main() -> int:
    if DST.exists():
        DST.unlink()
    shutil.copy(SRC, DST)

    with zipfile.ZipFile(DST, "r") as z:
        styles = z.read("word/styles.xml").decode("utf-8")
        settings = z.read("word/settings.xml").decode("utf-8")
    patched_styles = patch_styles(styles)
    patched_settings = patch_settings(settings)

    tmp = DST.with_suffix(".tmp.docx")
    with zipfile.ZipFile(DST, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.namelist():
            if item == "word/styles.xml":
                data = patched_styles.encode("utf-8")
            elif item == "word/settings.xml":
                data = patched_settings.encode("utf-8")
            else:
                data = zin.read(item)
            zout.writestr(item, data)
    tmp.replace(DST)
    print(f"patched → {DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
