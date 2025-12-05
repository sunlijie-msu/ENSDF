---
applyTo: "**"
---
# ENSDF Averaging Rules

## CLI Tool

```bash
python .github/Java_Average.py VALUE1 UNC1 [VALUE2 UNC2 ...]
```

Algorithm: Replicates AverageTool_22January2025.jar exactly.

## Workflow

1. Collect measurements with uncertainties
2. Run: `python .github/Java_Average.py 280 50 215 70 130 60 120 65`
3. Use **EXACT** "Suggested Adopted Result" from output
4. Apply to ENSDF record

## Critical Rules

### One Value Per Paper

Use **ONE value per original paper**, NOT one value per method.

- Multiple methods in same paper → select best value
- Lower limits → adopt largest limit
- Upper limits → adopt smallest limit
- Trace back to original papers (dataset values may differ)

### Java Output Rules (Zero Tolerance)

| Rule | Action |
|------|--------|
| Suggested Adopted Result | Use EXACTLY as shown |
| Uncertainty | Use EXACTLY (includes "≥ any input" rule) |
| Weighted vs Unweighted | Use whichever Java suggests |
| Transcription | Character-for-character, no rounding |

**FORBIDDEN:** Recalculating, modifying uncertainty, substituting weighted/unweighted.

## Lifetime Uncertainty Format

Lifetimes use uncertainty limit **99** (not default 35).

| Input | Default (limit 35) | Lifetime (limit 99) |
|-------|-------------------|---------------------|
| 197±50 | `2.0E2 {I5}` ❌ | `197 fs {I50}` ✓ |


**Rationale:** Full precision preserves information; scientific notation loses it.
