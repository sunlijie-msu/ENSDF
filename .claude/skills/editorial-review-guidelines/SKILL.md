---
name: editorial-review-guidelines
description: Performs professional editorial review of ENSDF comment lines for grammatical precision, subject-verb agreement, hyphenation, and technical terminology in Nuclear Data Sheets manuscripts. Use for editorial checks, grammar reviews, manuscript audits, or ENSDF comment validation.
---

# ENSDF Editorial Review Skill

## Core Review Patterns

### 1. Subject-Verb Agreement

**NSR References as Singular Subjects**
- NSR key numbers (YYYYAA##) act as singular subjects: `2005Ga01 predict` → `2005Ga01 predicts`
- `1972Hu10 measure` → `1972Hu10 measures`

**Evaluator Count**
- Check H record `AUT=` field for actual author count
- `AUT=B. Singh and C.D. Nesaraja` → use plural "evaluators"
- Match usage throughout file to H record count

### 2. Hyphenation Rules

**Compound Adjectives Before Nouns** (hyphenate):
- "4-mm-long gas cell", "x-ray diffraction", "R-matrix theory", "multi-reflection"

**After Nouns** (no hyphen):
- "was 4 mm in length", "emission by x rays"

**Always Hyphenated**: "L-transfers", "half-life"

**Gamma Terminology**:
- Noun: "gamma rays were detected" (no hyphen)
- Adjective: "gamma-ray spectrum" (hyphenated)

### 3. Punctuation

**Comma Splices** → Use semicolons:
- Wrong: `recorded, the latter allowed`
- Correct: `recorded; the latter allowed`

**Oxford Comma**: Preferred in technical lists (e.g., `curve, efficiency, and number`)

### 4. Spelling and Common Typos

- Correct obvious misspellings in comment text (e.g., `striped` → `stripped`, `evaluatord` → `evaluator`).
- Check discipline-specific terms and names for exact spelling (e.g., `GXPF1A`, facility names, detector names).
- Preserve intentional abbreviations, NSR key numbers, and ENSDF notation.

### 5. Technical Terminology

- "granddaughter" (single word, not "grand-daughter")
- Shell-model interactions: "GXPF1A" (exact capitalization)
- Adverb modifiers: "novelly designed" (not "novel designed")

### 6. Passive Voice

- Ensure auxiliary verbs: "spectra were recorded" (not "spectra recorded")

## Exclusions

- **Do NOT flag missing terminating periods**: Java NDS tool adds during PDF conversion
- **Do NOT modify XREF, data record fields, or column-positioning**

## Workflow

1. Read all `.ens` files in dataset
2. Review comment lines (columns 8-9: `c`, `cL`, `cG`, `cB`)
3. Apply pattern checks systematically
4. Report findings in tabular format
5. **Make NO edits** unless explicitly requested

## Output Format

```markdown
| Line(s) | Category | Current Text | Recommended | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| 47 | Subject-Verb | `predict` | `predicts` | NSR key = singular |
```