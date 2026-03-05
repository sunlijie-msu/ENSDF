---
name: editorial-review-guidelines
description: Performs professional editorial review of ENSDF comment lines for grammatical precision, subject-verb agreement, hyphenation, and technical terminology in Nuclear Data Sheets manuscripts. Use for editorial checks, grammar reviews, manuscript audits, or ENSDF comment validation.
---

# ENSDF Editorial Review Skill

## Pre-Review Requirements

**MANDATORY: Read ENSDF notation rules before every review**
- Consult `.github\copilot-instructions.md` ENSDF Comment Text Format Standards section
- Verify understanding of `|?` (approximate ≈), `{+n}` (superscript), `{-n}` (subscript), Greek letters
- Never flag valid ENSDF notation as errors

## CRITICAL ACTION POLICY: CHECK-ONLY

⚠️ **DEFAULT BEHAVIOR: EDITORIAL REVIEW = CHECK-ONLY (NO EDITS)**
- **NEVER make any edits** unless user explicitly requests modification
- Review is **REPORT FINDINGS ONLY** — flag issues in tabular format
- Provide line numbers, current text, recommended correction, and rationale
- User reviews findings in VS Code diff view before accepting changes
- Only edit if user explicitly states "fix these" or "apply corrections"

**Why this rule exists**: LLMs can introduce formatting errors. Human review of diffs catches mistakes before they corrupt nuclear data files.

## Critical Notation Format Errors

**Superscript/Subscript positioning: ELEMENT SYMBOL MUST BE OUTSIDE BRACES**
- WRONG: `{+13C}`, `{+48Ca}`, `{-1/2}He` (element inside braces)
- CORRECT: `{+13}C`, `{+48}Ca`, `{-1/2}` (only number/value inside)

**Systematic scanning**:
- Search for: `{+[0-9]+}[A-Z][a-z]?` (correct pattern)
- Flag: `{+[0-9A-Z][a-z]*}` or `{-[0-9A-Za-z]*}[A-Z]` (incorrect patterns)
- Examples of errors:
  - `{+13C}` → `{+13}C`
  - `{+48Ca}` → `{+48}Ca`
  - `{+208Pb}` → `{+208}Pb`
  - `{+1/2}He` → `{+1/2}` (if standalone) OR review context

**Critical importance**: This error appears frequently in lab notebook comments and must be caught on every review

**Record identifiers leaked into comment text**
- WRONG: `58ZNccL cL all the data is justifiable` (spurious "cL" text within comment line)
- CORRECT: `58ZNccL all the data are justifiable` (record identifier only in columns 6-9)
- **Systematic scanning**: Search comment text (columns 10-80) for leaked patterns: ` cL `, ` cG `, ` L `, ` G `, ` E `, ` B `
- **Common cause**: Copy-paste errors or text editor formatting issues
- **Flag all instances**: This corrupts comment readability and may confuse parsers

**Critical importance**: This error appears when evaluators copy/edit continuation records and accidentally insert record type codes into comment text

## Core Review Patterns

### 1. Dittography (Repeated Words)

**Check for duplicated words**
- Scan for: "the the", "from from", "were were", "in in", "and and", "of of"
- Flag ALL instances of unintentional word repetition
- Examples:
  - `the the decay` → `the decay`
  - `were were shifted` → `were shifted`
  - `from from measurements` → `from measurements`

**Systematic scanning required**: Use regex `\b(\w+)\s+\1\b` to catch all repetitions

### 2. Subject-Verb Agreement

**NSR references as singular subjects**
- NSR key numbers (YYYYAA##) function as singular subjects
- Examples: `2005Ga01 predict` → `2005Ga01 predicts`
- Apply consistently: `1972Hu10 measure` → `1972Hu10 measures`

**Evaluator count verification**
- Check H record `AUT=` field for author count
- Two+ authors: use plural "evaluators"
- Single author: use singular "evaluator"
- Match throughout entire file

### 3. Hyphenation

**Compound adjectives before nouns: HYPHENATE**
- "4-mm-long gas cell", "x-ray diffraction", "R-matrix theory"
- "multi-reflection", "high-energy gamma"

**Not used as adjectives: NO HYPHEN**
- "was 4 mm in length", "emission by x rays", "energy is high"

**Always hyphenated: "L-transfers", "half-life"**

**Gamma-ray terminology**
- Noun form: "gamma rays were detected" (no hyphen)
- Adjective form: "gamma-ray spectrum" (hyphenated)

### 4. Punctuation

**Comma splices → semicolons**
- Wrong: `spectra were recorded, the latter allowed precise`
- Correct: `spectra were recorded; the latter allowed precise`

**Oxford comma in technical lists**
- Preferred: `measured curve, efficiency, and number`
- Avoid: `measured curve, efficiency and number`

### 5. Spelling

**Common misspellings**
- `striped` → `stripped`, `ohter` → `other`, `stoped` → `stopped`
- `usign` → `using`, `coeffcients` → `coefficients`
- `deexiting` → `deexciting`, `paretheses` → `parentheses`

**Discipline-specific terms**
- Verify exact spelling: "GXPF1A", facility names, detector names
- Preserve NSR key numbers, ENSDF notation, intentional abbreviations

### 6. Technical Terminology

**Single-word compounds**
- "granddaughter" (NOT "grand-daughter")

**Exact capitalization**
- Shell-model interactions: "GXPF1A" (not "gxpf1a" or "GXPF1a")

**Adverb modifiers**
- "novelly designed" (NOT "novel designed")

**Chemical formulas and target materials**
- `Cd{-2}` → `CD{-2}` when referring to deuterated carbon target (CD₂, not cadmium)
- Context check: CD₂ targets common in nuclear physics experiments (C with D₂ deuterium)
- Always verify against original publication to confirm target material composition
- Common nuclear physics targets: CD₂ (deuterated polyethylene), CH₂ (polyethylene), C, Ni, Pb, etc.
- Material notation is case-sensitive: CD ≠ Cd, CH ≠ Ch

### 7. Passive Voice

**Require auxiliary verbs**
- Correct: "spectra were recorded"
- Wrong: "spectra recorded"

## ENSDF Notation Rules (Do NOT Flag As Errors)

**Mathematical and approximation symbols**
- `|?` means ≈ (approximate/tilde) - VALID notation, not an error
- Example: `log| {Ift} |?4.9` is correct (approximate log ft value)

**Superscripts and subscripts**
- `{+n}` = superscript (e.g., `{+3}He` → ³He)
- `{-n}` = subscript (e.g., `T{-1/2}` → T₁/₂)

**Greek letters**
- `|a` → α, `|b` → β, `|g` → γ, `|d` → δ, etc.
- Consult `.github\copilot-instructions.md` for complete mappings

**Mathematical operators**
- `|*` → × (times), `|<` → ≤, `|>` → ≥, `|+` → ±, `|-` → ∓

**Verify before flagging**: Always check copilot-instructions.md before marking notation as erroneous

## Exclusions (Never Flag)

**DO NOT flag these**
- Missing terminating periods (Java NDS tool adds during PDF conversion)
- XREF notation or positioning
- Data record fields (L, G, E, B records - columns outside comment fields)
- Column positioning or spacing in fixed 80-column format
- Valid ENSDF text encoding (`|?`, `{+n}`, `{-n}`, Greek letters)

## Workflow

**Step 1: Preparation**
- Read `.github\copilot-instructions.md` ENSDF Comment Text Format Standards section
- Verify understanding of all notation symbols before starting review

**Step 2: File reading**
- Load all `.ens` files in target dataset
- Identify H record to determine author count

**Step 3: Systematic scanning**
- Review comment lines only (columns 8-9: `c`, `cL`, `cG`, `cB`, `cN`)
- Apply all 7 core review patterns in sequence
- Use regex scanning for dittography: `\b(\w+)\s+\1\b`

**Step 4: Documentation**
- Report findings in tabular format (see Output Format below)
- Provide line numbers, categories, and rationale for each finding

**Step 5: Default action policy** ⚠️
- **CHECK-ONLY by default** (see CRITICAL ACTION POLICY section above)
- **DO NOT EDIT** unless explicitly requested
- Report all findings; user decides on corrections

## Output Format

**Use this exact table structure**

```markdown
| File | Line(s) | Category | Current Text | Recommended | Rationale |
|------|---------|----------|--------------|-------------|-----------|
| filename.ens | 47 | Subject-Verb | `predict` | `predicts` | NSR key = singular subject |
| filename.ens | 89-90 | Dittography | `the the decay` | `the decay` | Duplicated word |
```