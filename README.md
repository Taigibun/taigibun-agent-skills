# Taigibun Agent Skills

This repository contains a specialized suite of agent skills for Taigi (Taiwanese) language processing, literature analysis, and professional typography. These skills transform general AI agents (Claude, Gemini, etc.) into Taigi-expert assistants.

## Skills Included

### Language & Orthography
*   **taigi-roman-orthography-converter**: High-performance conversion between POJ/KPL and Input/Unicode formats, including procedural rules and tone placement.
*   **taigi-han-lo-formatter**: Automatically formats mixed Hanji and Roman script (Han-lo) with correct spacing and punctuation.
*   **taigi-legacy-encoding-converter**: Tool-oriented recovery of legacy Taigi encodings, "font-hack" (e.g., tws21.ttf), and number-format texts.

### Document & Typography
*   **taigi-document-structurer**: Heuristics to transform raw Taigi text into structured Markdown (Titles, Bylines, Chapters).
*   **taigi-document-typesetter**: Python scripts to apply professional Taigi fonts (GenYoMin) to DOCX files.
*   **taigi-docx-typography-expert**: Manages complex OpenXML typography (non-breaking hyphens, East Asian Kinsoku).
*   **taigi-pdf-outliner**: Automated PDF vectorization/outlining to ensure font fidelity across all devices.

### Reference
*   **taigi-terminology-guide**: Centralized rules for standardized Taigi technical and linguistic terms.

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

These skills are designed to be used in sequence:
1.  **Recovery**: Use `taigi-legacy-encoding-converter` to turn an old 1990s text file into Unicode.
2.  **Formatting**: Use `taigi-han-lo-formatter` to fix Han-lo spacing and punctuation.
3.  **Structuring**: Use `taigi-document-structurer` to automatically insert Markdown headers.
4.  **Typesetting**: Use `taigi-document-typesetter` and `taigi-docx-typography-expert` to generate a professional Word document with correct fonts and non-breaking hyphens.
5.  **Finalizing**: Use `taigi-pdf-outliner` to create a print-ready PDF that works even if the printer doesn't have Taigi fonts.

## Prerequisites

*   **Python 3.x**: Required for `taigi-document-typesetter` scripts.
*   **Ghostscript**: Required for `taigi-pdf-outliner` (`brew install ghostscript`).

## Contributing

We welcome contributions! Please submit a pull request or open an issue to suggest improvements or add new skills.
