---
name: editorial-review-guidelines
description: >
  Use this skill when performing editorial review of ENSDF comment lines.
  Checks grammatical precision, subject-verb agreement, hyphenation,
  technical terminology, and ENSDF text-notation correctness. Suitable for
  editorial checks, grammar reviews, manuscript audits, or ENSDF comment
  validation in Nuclear Data Sheets manuscripts.
---

# ENSDF Editorial Review Skill

Column/field rules: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

**Scope:** `c`, `cL`, `cG`, `cB`, `cE`, `cN`, `cP`, `cQ` comment records and continuation lines. Skip data-record fields (`L`, `G`, `E`, `B`, `DP`).
**Action Policy:** Check-Only. Report findings table. Do not edit unless user requests.

## Error Classes

### 1. ENSDF Notation
- **Superscript/subscript:** Symbol outside braces. Wrong: `{+13C}` → Correct: `{+13}C`. Detection regex (correct form): `{+[0-9]+}[A-Z][a-z]?`
- **Plain isotope tokens:** Wrong: `3He`, `36S(d,3He)` → Correct: `{+3}He`, `{+36}S(d,{+3}He)`. Scan: `(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b`; keep valid element symbols; exclude tokens followed by `|` (e.g., `2I|g`). **Mandatory:** after the regex scan, manually review every remaining candidate — regex misses tokens in dense prose.
- **Missing `{I}` on uncertainty:** Comment uncertainties require `{In}` or `{I+n-m}`. Three patterns:
  - Parentheses: `124(5) ps` → `124 ps {I5}`.
  - Bare `I` prefix: `|d=+0.05 I5` → `|d=+0.05 {I5}`.
  - Bare number (no `I`): `A{-2}=+0.05 5` → `A{-2}=+0.05 {I5}`.
  Scan for bare `I`: `\bI\d{1,3}\b` near values. Scan for bare numbers: lone 1-3 digit integers after `=` or after a value with space, where context suggests uncertainty.
- **Unicode leakage:** No raw Unicode glyphs. Wrong: `μ`, `×`, `β`, `γ`, `θ`, `≈`, `≤`, `≥` → Correct: `|m`, `|*`, `|b`, `|g`, `|q`, `|?`, `|<`, `|>`. Example: `1500-μm-thick` → `1500-|mm-thick`.
- **Non-ENSDF unit spellings:** `ug` → `|mg` (microgram); `cm2`, `mg/cm2` → `cm{+2}`, `mg/cm{+2}` (superscript exponent).
- **Mixed symbol-text:** Wrong: `γ-ray`, `μm`, `β-delayed`, `ug/cm2` → Correct: `|g-ray`, `|mm`, `|b-delayed`, `|mg/cm{+2}`.
- **Proper-noun exceptions:** Skip well-known instrument names (e.g., `Gamma Array` as part of INGA) — not every `Gamma` match is a symbol-text error.
- **Leaked record tags:** Scan cols 10-80 for spurious ` cL `, ` cG `, ` L `, ` G ` (copy-paste artifact).
- **Unintended symbol prefixes:** `|resonance` renders as rho+esonance; verify intent.
- **Inconsistent subscripts:** `A{-2}=0.5 A6=-0.1` → `A{-2}=0.5 A{-6}=-0.1`.
- **Mid-token line breaks:** `E{-p}(lab)` must not split across continuation lines.
- **Subscript used as negative exponent:** `10{-n}` (renders as subscript) must be `10{+-n}` (negative superscript). Scan: `10\{-\d+\}` . Applies to all scientific-notation contexts (`\|*10\{-`, `E\{-`, `×10\{-` in raw Unicode).

### 2. Grammar and Style
- **Capitalization:**
  - Top-block comments (before first data record, any type) → uppercase.
  - Record-specific comments **with** field identifier (`cL E$`, `cL J$`, `cL T$`, `cG E$`, `cG RI$`, `cG M$`, etc.) → lowercase, unless first token is numeral, symbol, isotope token, or acronym.
  - Record-specific comments **without** field identifier (`cL $`, `cG $`) → uppercase (standalone statements).
  - **Exception:** `cP` and `cN` comments always uppercase.
  - Examples (top-block, before first L/G/E/B/DP record): `cL E$From a least-squares fit` ✓; `cG E,RI$From 2017Li03` ✓; `cB IB,LOGFT$From I(|g+ce)` ✓ — all uppercase.
  - Examples (record-specific, after first data record): `cL T$from lifetime measurement` ✓ (lowercase continuation); `cL J$from the Adopted Levels` ✓; `cL J$1+ from shell model` ✓ (numeral exception).
- **NUCID case on comment lines:** Cols 1–5 must be uppercase. Wrong: `34Si cL J$` → Correct: `34SI cL J$`.
- **Extra space after `$`:** `cL J$ from ...` → `cL J$from ...`. Scan: `\$\s`.
- **Dittography:** `\b(\w+)\s+\1\b` -- flag `the the`, `were were`, etc.
- **Subject-verb agreement:** NSR keys are singular. Wrong: `1972Hu10 report` → Correct: `1972Hu10 reports`.
- **Missing auxiliary verbs:** `spectra recorded` → `spectra were recorded`.
- **Adjective/noun errors:** `others levels` → `other levels`.

### 3. Punctuation and Lists
- Comma splice between independent clauses → semicolon.
- Oxford comma required in lists of 3 or more items; only one `and` (at final item).
- Wrong: `14.9 {I6} (R1), and 8.3 {I4} (R2), and 10.5 {I60} (R3)` → Correct: `14.9 {I6} (R1), 8.3 {I4} (R2), and 10.5 {I60} (R3)`.

### 4. Hyphenation
- Compound modifier before noun: `4-mm-long target`, `gamma-ray spectrum`, `R-matrix analysis`, `2-g/cm{+2} Pb target`.
- Predicative: no hyphen (`the target was 4 mm long`).
- Always: `half-life`, `L-transfer`, `L-transfers`. Noun: `gamma rays`; adjective: `gamma-ray energy`.

### 5. Terminology and Spelling

**Facility and instrument names:**

| Wrong | Correct |
|-------|---------|
| `Van der Graaff`, `Van de Graaf`, `Van der Graaf`, `Van de Craaff` | `Van de Graaff` |
| `Cockroft-Walton` | `Cockcroft-Walton` |

**Nuclear-physics terms and spelling:**

| Wrong | Correct |
|-------|---------|
| `deexiting` | `deexciting` |
| `multiporities` | `multipolarities` |
| `grand-daughter` | `granddaughter` |
| `novelly designed` | `newly designed` |
| `ohter`, `usign`, `stoped`, `striped`, `coeffcients` | `other`, `using`, `stopped`, `stripped`, `coefficients` |

- `GXPF1A` — exact capitalization required (shell-model interaction name).
- **Chemical formulas:** `CD{-2}` (deuterated polyethylene) ≠ `Cd{-2}` (cadmium); verify against publication.

### 6. Text and Number Integrity
- **Extra space after `=`:** `|w|g= 0.45` → `|w|g=0.45`. Scan: `=\s[0-9]`.
- **Space within number:** `E{-p}(lab)=54 6` → `E{-p}(lab)=546`. Note: space between value and uncertainty is correct.
- **Field cross-contamination:** Energy in `RI$` or intensity in `E$` is an error. Wrong: `cG RI$ weighted average of 1224.6 {I154} ...` (contains energy, not intensity).

### 7. Logical Clarity
- Flag contradictory claims (confirmed and tentative in same sentence).
- Flag conclusions without citation or method reference.

## Exclusions
Missing terminal periods, XREF notation, alignment. Valid ENSDF symbols: `|?`, `{+n}`, `{-n}`, `|a`, `|b`, `|g`, `|d`, `|w`, `|*`, `|+`, `|-`.

## Procedure
1. Isolate all comment records (`c`, `cL`, `cG`, `cB`, `cE`, `cN`, `cP`, `cQ`) and their continuation lines.
2. Apply error classes: notation → grammar → punctuation → hyphenation → terminology → integrity → clarity.
3. Regex sweeps: dittography `\b(\w+)\s+\1\b`; leaked tags `\s(cL|cG|\bL\b|\bG\b)\s`; isotope tokens `(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b`; extra `=` space `=\s[0-9]`; extra `$` space `\$\s`; non-ASCII `[^\x00-\x7F]`.
4. Final symbol sweep on all flagged lines: verify no raw Unicode glyphs, plain isotope tokens, or mixed symbol-text compounds were missed.
5. Before reporting: confirm no valid ENSDF notation misclassified; each fix preserves scientific meaning. Do not edit unless user explicitly requests.

## Output Format
```
| File | Line(s) | Category | Current Text | Recommended | Rationale |
|------|---------|----------|--------------|-------------|-----------|
| f.ens | 47 | Subject-Verb | `predict` | `predicts` | NSR key is singular |
```
