# Taigibun Agent Skills

This repository contains a specialized suite of agent skills for Taigi language processing, literature digitization and professional typography. These skills turn general AI agents (Claude, Gemini, etc.) into Taigi-expert assistants.

## Skills Included

### Pipeline
*   **taigi-doc-pipeline**: The end-to-end orchestrator. Legacy Word `.doc` → fixed Unicode text → structured Markdown → GenYoMin2 TW `.docx` → outlined PDF, with the `NN_<title>_<descriptor>` naming convention, all five stage scripts, the stage-2 Kotlin fixer, and notes on what `textutil` does to old Word files.

### Language & Orthography
*   **taigi-roman-orthography-converter**: Conversion between POJ/KPL and Input/Unicode formats, tone placement rules, and the KonvertToPoj API.
*   **taigi-han-lo-formatter**: Han-lo spacing, hyphen and punctuation rules, plus how to protect English words, abbreviations and decimal points from the normalizer.
*   **taigi-legacy-encoding-converter**: Recovery of legacy Taigi encodings: number formats, font hacks (TP tws21.ttf, HOTSYS, CTS) and Big5-era kana stranded in the Private Use Area.

### Document & Typography
*   **taigi-document-structurer**: Heuristics and a script that turn flat Taigi text into Markdown with YAML title/author, part and chapter headings, and verse line blocks.
*   **taigi-document-typesetter**: The correct pandoc invocation for POJ text (smart punctuation off), a GenYoMin2 TW reference.docx builder, and per-run font/kinsoku patching.
*   **taigi-docx-typography-expert**: OpenXML line breaking for mixed-script text: native non-breaking hyphens, kinsoku, element-order traps.
*   **taigi-pdf-outliner**: docx → font-independent PDF through Microsoft Word (AppleScript) and Ghostscript outlining. Explains why LibreOffice must not be used for this font.

### Reference
*   **taigi-terminology-guide**: Standardized Taigi technical and linguistic terms.

## Installation

### Claude (Claude Code)

#### Option 1: Plugin Install (Recommended)

Install the entire skill suite as a plugin directly from the repository:
```bash
/plugin install https://github.com/Taigibun/taigibun-agent-skills
```

Skills are namespaced automatically (e.g., `/taigibun-agent-skills:taigi-roman-orthography-converter`). To update:
```bash
/plugin update taigibun-agent-skills
```

#### Option 2: User-Level (Global)

Install individual skills for all projects by copying them into your home directory:
```bash
cp -r taigi-roman-orthography-converter/ ~/.claude/skills/taigi-roman-orthography-converter/
```

#### Option 3: Project-Level

Install individual skills for a specific project by copying them into the project directory:
```bash
cp -r taigi-roman-orthography-converter/ .claude/skills/taigi-roman-orthography-converter/
```

#### Option 4: CLI Flags (Development / Testing)

Load the plugin from a local directory or remote archive without installing:
```bash
claude --plugin-dir ./taigibun-agent-skills
claude --plugin-url https://example.com/taigibun-agent-skills.zip
```

For Options 2 and 3, you can optionally reference the skills in your `CLAUDE.md`:
```markdown
I have Taigi language skills in `.claude/skills/`.
Always refer to these for translation, Roman Orthography, or typesetting tasks.
```

### Gemini CLI

#### Option 1: Install from Git (Recommended)

Install the entire skill suite directly from the repository:
```bash
gemini skills install https://github.com/Taigibun/taigibun-agent-skills.git --scope user
```

Install a single skill from the repo using `--path`:
```bash
gemini skills install https://github.com/Taigibun/taigibun-agent-skills.git --path taigi-roman-orthography-converter --scope user
```

Use `--scope workspace` instead of `--scope user` to install for the current project only (stored in `.gemini/skills/`).

#### Option 2: Install from Local Directory

After cloning the repository:
```bash
gemini skills install ./taigi-roman-orthography-converter --scope user
```

#### Option 3: Symlink for Development

For active skill development, use `link` so changes are reflected immediately:
```bash
gemini skills link ./taigi-roman-orthography-converter --scope user
```

#### Option 4: Manual Placement

Copy skill directories directly to the Gemini skills directory:
```bash
cp -r taigi-roman-orthography-converter/ ~/.gemini/skills/taigi-roman-orthography-converter/
```

After any installation method, reload skills in your session:
```
/skills reload
```

### Cross-Agent Install

This project follows the open [Agent Skills](https://agentskills.io) standard (`SKILL.md`). You can use the cross-agent skills CLI to install for multiple agents at once.

**Global** (available in all projects — installs to `~/.agents/skills/` with symlinks to each agent):
```bash
cd ~ && npx skills install github.com/Taigibun/taigibun-agent-skills
```

**Project-level** (available only in the current project — installs to `.agents/skills/`):
```bash
npx skills install github.com/Taigibun/taigibun-agent-skills
```

This works with Claude Code, Gemini CLI, Codex CLI, and other compatible agents.

## Workflow Example: Publishing a Taigi Book

`taigi-doc-pipeline` runs these in order; each stage has its own skill with the detailed rules:

1.  **Extract**: `textutil` turns the legacy `.doc` into UTF-8 text (`01_<title>_raw.txt`).
2.  **Fix**: `taigi-legacy-encoding-converter` recovers font-hack text and PUA kana; `taigi-han-lo-formatter` normalizes tone marks, Han-lo spacing and punctuation (`02_<title>_fixed.txt`).
3.  **Structure**: `taigi-document-structurer` inserts YAML title/author, headings and verse blocks (`03_<title>_structured.md`).
4.  **Typeset**: `taigi-document-typesetter` and `taigi-docx-typography-expert` produce a Word document with GenYoMin2 TW, non-breaking hyphens and kinsoku (`04_<title>_typeset.docx`).
5.  **Outline**: `taigi-pdf-outliner` exports through Microsoft Word and vectorizes every glyph with Ghostscript, so the PDF renders without the font installed (`05_<title>_outlined.pdf`).

## Prerequisites

*   **macOS** for stages 1 and 5: `textutil` (built in) and **Microsoft Word for Mac** driven by AppleScript (first run asks for Automation permission).
*   **pandoc** and **Ghostscript**: `brew install pandoc ghostscript`. **poppler** for rendering checks: `brew install poppler`.
*   **Python 3** (standard library only) for the structurer and typesetter scripts.
*   **JDK 17 or 21** for the stage-2 Kotlin fixer, with the `KonvertToPOJ` and `KonvertLegacyPOJ` repositories as git submodules (they are not on Maven Central).
*   **GenYoMin2 TW** fonts from https://github.com/ButTaiwan/genyo-font installed in `~/Library/Fonts/`.
*   **LibreOffice** only if you want `.odt` copies. Do not use it for PDF.

## Contributing

We welcome contributions! Please submit a pull request or open an issue to suggest improvements or add new skills.
