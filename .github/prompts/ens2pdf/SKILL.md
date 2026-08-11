---
name: ens2pdf
description: >
  Run the ens2pdf.py Python wrapper to convert ENSDF .ens files to PDF using
  the McMaster-MSU Java NDS tool. Supports single files, element-level batches,
  and glob patterns. Optionally opens the result.
argument-hint: "File name, element symbol, or glob pattern (e.g. Si35_adopted, Si, Si35_*sig)"
---

# ENSDF PDF export

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Usage

```bash
python .github/scripts/ens2pdf.py Si35_adopted
python .github/scripts/ens2pdf.py "finished/Si35/new/Si35_adopted.ens"
python .github/scripts/ens2pdf.py Si
python .github/scripts/ens2pdf.py "Si35_*sig"
python .github/scripts/ens2pdf.py Si35_adopted --open
python .github/scripts/ens2pdf.py Si35_adopted --open --system
```

## Options
- No flag: convert and save PDF without opening it.
- `--open`: open the result in VS Code after conversion.
- `--open --system`: open the result in the system default PDF viewer.

## Notes
- The script resolves partial names and glob patterns against the workspace tree.
- Multiple matches are converted sequentially.
- The Java tool must be present at `D:\X\ND\McMaster-MSU-Java-NDS\`.
