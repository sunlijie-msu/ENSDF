---
name: level-matching
description: >
  Use this skill when matching L-records between an individual dataset (.ens)
  and the adopted dataset (adopted.ens) to identify which levels are shared and which
  are newly observed. Produces matched/unmatched/adopted-only tables.
  CHECK-ONLY — reports findings without editing files.
argument-hint: [source.ens] [adopted.ens]
---

# Level Matching: Individual Dataset vs. Adopted

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Configuration

Set before running. Adjust per dataset:

| Parameter | Default | Notes |
|:---|:---|:---|
| `BASELINE_KEV` | 15 | Min threshold; raise for high-uncertainty data (e.g., fragmentation → 50) |
| `STRONG_FACTOR` | 1.0 | Δ ≤ STRONG_FACTOR × de_source → **Strong**; else → **Possible** |

## Algorithm

### 1. Parse L-Records (both files)

Exact 0-based Python indices:
- Guard: `line[5]==' ' and line[6]==' ' and line[7]=='L' and line[8]==' '`
- E: `line[9:19].strip()` → float; DE: `line[19:21].strip()` → int (default 5 if blank)
- Jπ: `line[22:39].strip()`

### 2. Match by Energy

For each source level find the nearest adopted level within a dynamic threshold:

```python
threshold = max(BASELINE_KEV, 3 * de_source)  # see Configuration
```

Report match **confidence** based on energy difference:
- **Strong**: Δ ≤ de_source (within source uncertainty — very likely same level)
- **Possible**: de_source < Δ ≤ threshold (outside uncertainty but nearby)

### 3. Resolve One-to-One Conflicts

Two source levels → same adopted: keep the closer; demote the other to "new in source." Process in one pass.

### 4. Jπ Compatibility

Treat J (spin magnitude) and π (parity) **independently**. Flag `!!` only if **both** are incompatible.

**Parity**: incompatible only when one is unambiguously positive and the other unambiguously negative. Blank, parenthesized, or multi-valued → compatible.

**Spin**: build allowed-spin sets; incompatible only if sets are disjoint.
- Single value `3/2` → `{3/2}`
- Options `3/2,5/2` → `{3/2, 5/2}`
- Range `(1/2:9/2)` → `{1/2, 3/2, 5/2, 7/2, 9/2}`

## Output

Three sections (read-only; no file edits). Script: `.github/temp/match_levels.py`.

| Section | Columns |
|:---|:---|
| **Matched** | Source E · ±DE · Adopted E · Δ · Confidence · Jπ-OK · Source Jπ · Adopted Jπ |
| **New in source** | Source E · ±DE · Jπ · nearest adopted (Δ) |
| **Adopted-only** | Adopted E · Jπ · nearest source (Δ) |

## Interpretation

| Pattern | Likely cause |
|:---|:---|
| `!!`, strong match | Same level; Jπ in adopted needs revision from this dataset |
| `!!`, strong match, high-spin adopted | Likely doublet — two levels at same energy |
| `!!`, possible match (Δ near threshold) | Likely different levels; raise `BASELINE_KEV` or flag unmatched |
| Many new source levels in a region | Adopted incomplete for that excitation range |
| Adopted-only, high-spin or blank Jπ | Inaccessible to this reaction type, or fine-grained resonance levels |

## Pitfalls

| Issue | Fix |
|:---|:---|
| Blank DE | Default `de = 5` keV |
| Blank Jπ | Treat as compatible with any Jπ |
| Threshold too tight | Raise baseline |
| Range notation `(a:b)` | Expand to full half-integer set before spin comparison |
