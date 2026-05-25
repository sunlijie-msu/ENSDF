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

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Rigorous editorial review of ENSDF comment text, focusing on:
- Grammar and punctuation
- Technical nuclear-physics language
- ENSDF text-notation correctness

## Action Policy

**Default: Check-Only.** Do not edit files unless the user explicitly requests corrections. Report findings with line numbers, current text, recommended text, and rationale. LLM edits can introduce subtle ENSDF formatting errors; human diff-view review is a required safety layer.

## Scope

Review comment records only: `c`, `cL`, `cG`, `cB`, `cN`, and their continuation lines.  
Do not review data-record fields (`L`, `G`, `E`, `B`, `DP`) for editorial issues.

## Error Classes

### 1. ENSDF Notation

- **Superscript/subscript:** Element symbol must appear **outside** braces.
  - Wrong: `{+13C}`, `{+208Pb}` → Correct: `{+13}C`, `{+208}Pb`
  - Correct regex pattern: `{+[0-9]+}[A-Z][a-z]?`
- **Number+element isotope tokens:** Plain isotope tokens are invalid in comment text.
  - Wrong: `3He`, `36S(d,3He)` → Correct: `{+3}He`, `{+36}S(d,{+3}He)`
  - Candidate scan regex: `(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b`
  - Filter rule: keep only valid element symbols; ignore ENSDF symbol constructs such as `2I|g`.
- **Uncertainty notation:** Use `{In}` notation; never use inline parenthetical uncertainties.
  - Wrong: `36(4)-mg/cm{+2}` → Correct: `36-mg/cm{+2} {I4}`
  - Wrong: `E=1234(5) keV` → Correct: `E=1234 keV {I5}`
- **Leaked record tags:** Scan columns 10–80 for spurious ` cL `, ` cG `, ` L `, ` G `, ` E `, ` B ` (common copy-paste artifact).
- **Unintended symbol prefixes:** `|resonance` renders as `ρesonance`; verify intent.
- **Unicode leakage (mandatory):** ENSDF comment text must use ENSDF symbol encoding, not raw Unicode glyphs.
  - Wrong: `μ`, `×`, `β`, `γ`, `θ`, `≈`, `≤`, `≥` in plain Unicode.
  - Correct: `|m`, `|*`, `|b`, `|g`, `|q`, `|?`, `|<`, `|>`.
  - Example: `1500-μm-thick` → `1500-|mm-thick`; `6.5×10^5` → `6.5|*10{+5}`.
- **Plain isotope tokens in prose (mandatory):** after the regex scan, manually review every remaining isotope-like token in comment text.
  - Wrong: `34Al`, `36Al`, `35Mg` in prose.
  - Correct: `{+34}Al`, `{+36}Al`, `{+35}Mg`.
- **Mixed symbol-text compounds:** reject mixed Unicode/ENSDF compounds such as `γ -ray`, `μm`, or split symbol-text forms.
  - Correct: `|g-ray`, `|mm`, `|b-delayed`.
- **Inconsistent subscript notation:** All coefficients in an expression must use the same style.
  - Wrong: `A{-2}=0.5 A{-4}=0.1 A6=-0.1` → Correct: `A{-2}=0.5 A{-4}=0.1 A{-6}=-0.1`
- **Mid-token line breaks:** Compound tokens such as `E{-p}(lab)` must not split across continuation lines.

### 2. Grammar and Style

- **Capitalization by scope:**
  - Top general comments (before first data record) start with uppercase, with or without identifier headers.
  - Record-specific comments with identifier(s) after level/gamma records (`cL E$`, `cL J$`, `cL T$`, `cG E$`, `cG RI$`, `cG M$`, `cG MR$`, etc.) start with lowercase unless first token is a numeral, symbol, isotope token (`{+34}Mg`), or required acronym.
  - **Exception (mandatory):** `cP` and `cN` identifier comments start with uppercase whether general or record-specific.
  - Examples: `cL T$from fitting ...` (record-specific L/G style), `cL E$From a least-squares fit ...` (top default block), `cP J,T$From ...`, `cN BR$Experimental ...`.
- **Dittography:** Scan with `\b(\w+)\s+\1\b` (e.g., `the the`, `were were`, `and and`).
- **Subject-verb agreement:** NSR key numbers (`YYYYAA##`) take singular verbs.
  - Wrong: `1972Hu10 measure` → Correct: `1972Hu10 measures`
- **Missing auxiliary verbs:** `spectra recorded` → `spectra were recorded`
- **Adjective/noun errors:** `decay to others levels` → `decay to other levels`

### 3. Punctuation and Lists

- Replace comma splices between independent clauses with semicolons.
- Require the Oxford comma in lists of three or more items.
- Only one `and` per list (at the final item).
- Use comma-space separators in NSR citation lists and author/date pairs in comment text.
  - Wrong: `14.9 {I6} (Ref1), and 8.3 {I4} (Ref2), and 10.5 {I60} (Ref3)`
  - Correct: `14.9 {I6} (Ref1), 8.3 {I4} (Ref2), and 10.5 {I60} (Ref3)`

### 4. Hyphenation

- Hyphenate compound modifiers before nouns: `4-mm-long target`, `gamma-ray spectrum`, `R-matrix analysis`.
- Hyphenate attributive unit phrases before nouns: `2-g/cm{+2} Pb target`, `0.93-g/cm{+2} C target`.
- Do not hyphenate predicatively: `the target was 4 mm long`.
- Always hyphenate: `half-life`, `L-transfer`, `L-transfers`.
- Gamma terminology: noun = `gamma rays`; adjective = `gamma-ray`.

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
| `ohter`, `usign`, `coeffcients`, `paretheses`, `stoped`, `striped` | `other`, `using`, `coefficients`, `parentheses`, `stopped`, `stripped` |

- `GXPF1A` — exact capitalization required (shell-model interaction name).
- **Chemical formulas:** `CD{-2}` (deuterated polyethylene) ≠ `Cd{-2}` (cadmium); always verify against the original publication.

### 6. Text and Number Integrity

- **Extra space after `=`:** `|w|g= 0.45` → `|w|g=0.45`; scan for `=[space][digit]`.
- **Space within a number:** `E{-p}(lab)=54 6` → `E{-p}(lab)=546`.
- **Field cross-contamination:** Energy values must not appear in `RI$` fields; intensity values must not appear in `E$` fields.
  - Wrong: `cG RI$ weighted average of 1224.6 {I154} weighted average of 14.9 {I21}`
  - Correct: `cG RI$ weighted average of 14.9 {I21}`

### 7. Logical Clarity

- Flag contradictory claims (e.g., "confirmed" and "tentative" in the same sentence).
- Flag unsupported conclusions lacking a citation or method reference.

## Exclusions

Do not flag:
- Missing terminal periods (PDF renderer may add them).
- XREF notation or alignment.
- Valid ENSDF symbols: `|?` (≈), `{+n}/{-n}`, `|a` (α), `|b` (β), `|g` (γ), `|d` (δ), `|w` (ω), `|*` (×), `|+` (±), `|-` (∓).

## Scan Procedure

1. Isolate all comment records, including continuation lines.
2. Apply error classes in order: notation → grammar → punctuation → hyphenation → terminology → logical clarity.
3. Useful regex patterns:
   - Dittography: `\b(\w+)\s+\1\b`
   - Leaked tags: `\s(cL|cG|\bL\b|\bG\b|\bE\b|\bB\b)\s`
  - Plain isotope token candidate: `(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b`
  - Post-filter for isotope-token scan: retain only valid element symbols and exclude tokens followed by `|` (for example, `2I|g`).
   - Extra space after `=`: `=\s[0-9]`
  - Non-ASCII scan (mandatory): `[^\x00-\x7F]`
4. Compile the findings table.
5. Perform a final symbol sweep on all edited or flagged comment lines: raw Unicode glyphs, plain isotope tokens, and mixed symbol-text compounds.

## Workflow

1. Isolate comment records from the target file.
2. Apply all error classes systematically.
3. Report findings in the required table format.
4. Do not edit unless the user explicitly requests corrections.

## Output Format

```markdown
| File | Line(s) | Category | Current Text | Recommended | Rationale |
|------|---------|----------|--------------|-------------|-----------|
| filename.ens | 47 | Subject-Verb | `predict` | `predicts` | NSR key is singular |
| filename.ens | 89-90 | Dittography | `the the decay` | `the decay` | Duplicated word |
```

## Quality Gate Before Reporting

Before finalizing:
- Confirm no valid ENSDF notation was misclassified as an error.
- Confirm each recommendation preserves scientific meaning.
- Confirm wording is concise and technically precise.