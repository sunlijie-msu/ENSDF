---
name: averaging
description: >
  Use this skill when calculating weighted or unweighted averages for ENSDF
  nuclear data using Java_Average.py. Enforces exact transcription of the
  Suggested Adopted Result, minimum-uncertainty rule, and lifetime
  uncertainty limit 99. Suitable for adopting measured values from multiple
  publications.
argument-hint: [VALUE1 UNC1 VALUE2 UNC2 ...]
---

# ENSDF Averaging

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## When
Run `Java_Average.py` any time you need to adopt a value from 2+ measurements across different papers.

## How

**Numeric mode** — comma after each pair for readability (optional):
```bash
python .github/scripts/Java_Average.py 19.7 1.3, 22 4, 21.5 1.5
```

**Comment mode** — feed the existing cL T$ comment directly:
```bash
python .github/scripts/Java_Average.py --comment "19.7 ps {I13} (1970Br10) and 22 ps {I4} (1975Sm02)"
```

## What to adopt


When user requests code `Java_Average.py` for calculating averages, follow these rules with absolute precision and zero tolerance for deviation:

- Always use exact Java code "Suggested Adopted Result" value without recalculation or substitution
- Use exact uncertainty value provided by Java code (automatically applies rule: adopted uncertainty ≥ any individual input uncertainty)
- Check whether Java suggests weighted or unweighted average in output comments
- Use whichever method Java code explicitly recommends
- Transcribe all values character-for-character without rounding, adjustment, or omitting units
- Never recalculate averages by yourself
- Never use unrecommended uncertainty results
- Never substitute weighted/unweighted averages contrary to Java's recommendation


## Gotchas

- **`[critical=X]` is display-only.** The tool decides Weighted vs. Unweighted using a hardcoded threshold of 3.5, not the displayed chi² critical value.
- **Lifetimes use full precision** (uncertainty limit 99): write `197 fs {I50}`, not `2.0E2 {I5}`.
- **One value per paper.** Comment mode skips any value before "average of" (it's the previous result) and stops at "Other:".
