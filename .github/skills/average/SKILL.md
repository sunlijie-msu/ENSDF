---
name: average
description: >
  Use this skill when calculating weighted or unweighted averages for ENSDF
  nuclear data using Java_Average.py. Enforces exact transcription of the
  Suggested Adopted Result, minimum-uncertainty rule, and lifetime
  uncertainty limit 99. Suitable for adopting measured values from multiple
  publications.
argument-hint: [VALUE1 UNC1 VALUE2 UNC2 ...]
---

# ENSDF Averaging

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

Copy the `suggested adopted result` line exactly — value and uncertainty — character-for-character. Apply to the L-record T/DT fields and cL comment.

## Gotchas

- **`[critical=X]` is display-only.** The tool decides Weighted vs. Unweighted using a hardcoded threshold of 3.5, not the displayed chi² critical value.
- **If Unweighted: both value and uncertainty change.** Never substitute the unweighted uncertainty with the weighted one (or vice versa).
- **Never recalculate.** If the suggested result looks surprising, trust the tool.
- **Lifetimes use full precision** (uncertainty limit 99): write `197 fs {I50}`, not `2.0E2 {I5}`.
- **One value per paper.** Comment mode skips any value before "average of" (it's the previous result) and stops at "Other:".
