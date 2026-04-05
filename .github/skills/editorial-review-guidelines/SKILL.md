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

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Provide a rigorous editorial review of ENSDF comment text with a focus on:
- grammar and punctuation,
- technical language in nuclear physics,
- ENSDF text-notation correctness.

## Action Policy

### Default: Check-Only

- Do not edit files unless the user explicitly asks for corrections.
- Report findings only.
- Include line numbers, current text, recommended text, and rationale.

### Why this policy exists

LLM edits can introduce subtle ENSDF formatting errors. Human review in diff view is a required safety layer.

## Scope

Review comment records only:
- `c`, `cL`, `cG`, `cB`, `cN` and their continuation lines.

Do not review data-record fields for editorial issues:
- `L`, `G`, `E`, `B`, `DP` numeric/layout fields.

## High-Priority Error Classes

### 1) ENSDF Notation and Encoding Errors

- Flag malformed superscript/subscript usage. Element symbol must be **outside** braces.
  - Wrong: `{+13C}`, `{+48Ca}`, `{+208Pb}`, `{+36S}`
  - Correct: `{+13}C`, `{+48}Ca`, `{+208}Pb`, `{+36}S`
- Use regex guidance for notation scanning:
  - Correct pattern: `{+[0-9]+}[A-Z][a-z]?`
  - Flag pattern: `{+[0-9A-Z][a-z]*}` or `{-[0-9A-Za-z]*}[A-Z]`
- This error appears frequently — scan every review.
- Flag record tags accidentally leaked into comment text.
  - Wrong: `...cL all the data are justifiable` (spurious `cL` inside text)
  - Correct: Only the record identifier in columns 6–9; comment text starts at column 10.
  - Scan comment text (columns 10–80) for patterns: ` cL `, ` cG `, ` L `, ` G `, ` E `, ` B `
  - Common cause: copy-paste errors when duplicating continuation records.
- Flag accidental ENSDF symbol prefixes that change meaning.
  - Example: `|resonance` (renders as `ρesonance`) should usually be `resonance`.
- Flag inconsistent subscript notation within the same expression.
  - All angular correlation coefficients must use the same notation style.
  - Wrong: `A{-2}=0.5 A{-4}=0.1 A6=-0.1` (mixed: `A{-2}` subscripted, `A6` plain).
  - Correct: `A{-2}=0.5 A{-4}=0.1 A{-6}=-0.1`.
- Flag mid-token line breaks across continuation records.
  - Tokens like `E{-p}(lab)` must not be split at a continuation boundary.
  - Wrong: line ends `...E{-p}(la` and next continuation line starts `b)=546`.
  - Correct: reflow text so the full token appears on one line.
  - Common cause: 80-column wrap splits a compound subscript token.

### 2) Grammar and Style Errors

- Dittography (duplicate words): `the the`, `were were`, `from from`, `and and`, `in in`, `of of`.
  - Real examples found in production files: `Protons were were spatially`, `using the the CeBrA demonstrator`.
  - Systematic scan: use regex `\b(\w+)\s+\1\b`.
- Subject-verb agreement.
  - NSR key numbers (`YYYYAA##`) take singular verbs.
  - Example: `1972Hu10 measure` → `1972Hu10 measures`; `2001Nu01 report` → `2001Nu01 reports`.
- Missing auxiliary verbs in passive constructions.
  - Wrong: `spectra recorded`, `levels deduced`.
  - Correct: `spectra were recorded`, `levels were deduced`.
- Adjective/noun errors.
  - `decay to others levels` → `decay to other levels`.

### 3) Punctuation and List Logic

- Comma splice → semicolon when clauses are independent.
- Enforce Oxford comma in lists of three or more items.
- Flag duplicate `and` in lists — only the final `and` (Oxford comma position) is correct.
  - Wrong: `14.9 {I6} (Ref1), and 8.3 {I4} (Ref2), and 10.5 {I60} (Ref3)`.
  - Correct: `14.9 {I6} (Ref1), 8.3 {I4} (Ref2), and 10.5 {I60} (Ref3)`.
  - Scan for: `and [value], and` — interior `and` tokens must be removed.

### 4) Hyphenation Rules

- Hyphenate compound modifiers before nouns.
  - `4-mm-long target`, `gamma-ray spectrum`, `R-matrix analysis`.
- Do not hyphenate when not used adjectivally.
  - `the target was 4 mm long`.
- Always hyphenate: `half-life`, `L-transfer`, `L-transfers`.
- Gamma terminology:
  - Noun form: `gamma rays`.
  - Adjective form: `gamma-ray`.

### 5) Technical Terminology and Spelling

**Facility and instrument names:**
- `Van de Graaff` — three distinct error variants to flag:
  - Wrong preposition: `Van der Graaff` → `Van de Graaff`.
  - Single-f: `Van de Graaf` → `Van de Graaff`.
  - Combined preposition + single-f: `Van der Graaf` → `Van de Graaff`.
  - Character substitution: `de Craaff` → `de Graaff` (C mistyped as G).
- `Cockcroft-Walton` (NOT `Cockroft-Walton` — missing second 'c'; named after John Cockcroft).

**Nuclear-physics terms:**
- `deexciting` (NOT `deexiting`).
- `multipolarities` (NOT `multiporities`).
- `GXPF1A` (exact capitalization — shell-model interaction name).
- `granddaughter` (one word, NOT `grand-daughter`).

**Adverb/adjective modifiers:**
- `novelly designed` → `novel` is an adjective, not an adverb; reword or use `newly designed`.

**Chemical formulas and target materials:**
- Material notation is case-sensitive: `CD{-2}` (deuterated polyethylene, CD₂) ≠ `Cd{-2}` (cadmium).
- Always verify against original publication to confirm target composition.
- Common nuclear-physics targets: CD₂ (deuterated polyethylene), CH₂ (polyethylene), C, Ni, Pb.

**Common spelling errors in ENSDF comments:**
- `ohter` → `other`
- `stoped` → `stopped`
- `striped` → `stripped`
- `usign` → `using`
- `coeffcients` → `coefficients`
- `paretheses` → `parentheses`
- `deexiting` → `deexciting`
- `Cockroft-Walton` → `Cockcroft-Walton`

### 6) Logical Clarity in Scientific Statements

- Flag contradictory or ambiguous claims (e.g., "confirmed" vs "tentative" in same sentence).
- Flag unsupported conclusions missing a citation or method reference.

### 7) Text and Number Integrity

- Extra space after `=` in physics expressions.
  - Wrong: `E{-p}(lab)= 639`, `|w|g= 0.45`.
  - Correct: `E{-p}(lab)=639`, `|w|g=0.45`.
  - Scan for: `=[space][digit]` pattern in comment text.
- Accidental space within a multi-digit number.
  - Wrong: `E{-p}(lab)=54 6` (space splits "546").
  - Correct: `E{-p}(lab)=546`.
  - Common cause: line-editing error; look for spaces between consecutive digit characters.
- Content placed in the wrong comment identifier (`E$` vs `RI$`).
  - `E$` fields must contain energies only; `RI$` fields must contain intensities only.
  - Wrong: `cG RI$ weighted average of 1224.6 {I154} weighted average of 14.9 {I21}` — gamma energy `1224.6 {I154}` pasted before the actual intensity.
  - Correct: `cG RI$ weighted average of 14.9 {I21}`.
  - Check: if an energy value appears in an `RI$` field (or vice versa), flag as cross-contamination.

## Never Flag (Exclusions)

- Missing terminal periods (Java NDS may add them in PDF output).
- XREF notation or XREF alignment.
- Fixed-column spacing/layout outside comment text.
- Valid ENSDF symbols and control notation.

## ENSDF Symbols Quick Reference (Do Not Mark as Errors)

- Approximation: `|?` means approximately.
- Superscript/subscript: `{+n}`, `{-n}`.
- Common Greek letters: `|a` (alpha), `|b` (beta), `|g` (gamma), `|d` (delta), `|w` (omega).
- Common operators: `|*` (times), `|<` (less than or equal), `|>` (greater than or equal), `|+` (plus-minus), `|-` (minus-plus).

## Recommended Scan Procedure

1. Read target ENSDF file(s) and isolate comment records.
2. Apply checks in this order:
   - notation integrity,
   - grammar/agreement,
   - punctuation/list logic,
   - hyphenation,
   - terminology/spelling,
   - logical clarity.
3. Use regex where useful:
   - duplicated words: `\b(\w+)\s+\1\b`
   - suspicious leaked tags in comment text: `\s(cL|cG|\bL\b|\bG\b|\bE\b|\bB\b)\s`
4. Compile findings table.

## Workflow (Execution Standard)

1. Preparation: complete the pre-review checklist.
2. Reading: scan comment records only, including continuation comments.
3. Analysis: apply all high-priority error classes.
4. Documentation: report findings using the required table format.
5. Action policy check: keep check-only behavior unless the user explicitly asks for edits.

## Output Format (Required)

Use this exact table schema:

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