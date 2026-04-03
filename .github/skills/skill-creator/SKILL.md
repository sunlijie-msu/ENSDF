---
name: skill-creator
description: "Creates and revises SKILL.md files for VS Code GitHub Copilot and Claude agent skills. Use when authoring a new SKILL.md, improving an existing one, diagnosing why a skill is not triggering, or packaging domain knowledge into a reusable workflow skill. Not for creating .instructions.md, .prompt.md, .agent.md, hooks, or other customization file types."
---

# Skill Creator

## Scope

This skill creates and revises **SKILL.md files only**.

For other customization file types (.instructions.md, .prompt.md, .agent.md, hooks, copilot-instructions.md), handle them directly without this skill.

---

## Project Rule: Reference, Don't Repeat

> **If a rule, standard, or convention already exists in `.github/copilot-instructions.md` or `.github/agents/FRIBND.agent.md`, reference the relevant section — do NOT copy or paraphrase it into SKILL.md.**

**Bad** — duplicates existing rules:
```markdown
## Uncertainty notation
Use {In} for symmetric uncertainties, {I+n-m} for asymmetric...
```

**Good** — points to the authoritative source:
```markdown
Follow uncertainty notation rules in `.github/copilot-instructions.md` § "ENSDF Uncertainty Notation".
```

This avoids stale duplicates and preserves the single source of truth in the instruction files.

---

## Core Principles

### 1. Concise Is Key

SKILL.md shares the context window with conversation history, system prompts, and all loaded skills.

- "Does Claude already know this?" → Remove it.
- "Is this already in `.github/copilot-instructions.md` or `.github/agents/FRIBND.agent.md`?" → Reference it.
- Body under 100 lines.

**Bad** (~150 tokens — explains what Claude already knows):
```
PDF files are common. To extract text you need a library. There are many options...
```

**Good** (~30 tokens):
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### 2. Set Appropriate Freedom

| Freedom | Use When | Style |
|---|---|---|
| High | Multiple valid approaches; context-dependent | Natural language steps |
| Medium | Preferred pattern exists; variation acceptable | Pseudocode with parameters |
| Low | Exact sequence required; fragile or error-prone | Exact commands; no variation |

### 3. Progressive Disclosure

```
skill-name/
├── SKILL.md        # overview + navigation (< 500 lines)
├── reference.md    # loaded on demand
└── scripts/
    └── validate.py # executed, not loaded into context
```

- References must be **one level deep** from SKILL.md. Never chain: `SKILL.md → a.md → b.md`.
- Reference files > 100 lines need a table of contents.
- All paths use **forward slashes**.

---

## YAML Frontmatter

```yaml
---
name: skill-name     # ≤ 64 chars; lowercase letters, numbers, hyphens only
description: "..."   # ≤ 1024 chars; third person; WHAT and WHEN; trigger keywords
---
```

- `name`: no XML tags, no reserved words (`anthropic`, `claude`), matches folder name. Prefer gerund form: `processing-pdfs`.
- `description`: third-person (`"Processes CSV files"` ✓ — `"I can help you"` ✗); colons must be quoted.
- **Silent failure causes:** unescaped colons · tabs instead of spaces · name/folder mismatch · XML tags.

---

## Common Patterns

### Task Configuration (data-entry and reconciliation skills)

For any skill that processes source data into ENSDF records, place a user-fillable **Task Configuration** block as the **first section** (before the workflow). The user fills it in at the start of every task; workflow steps remain fixed.

## Task Configuration

**User fills in this block at the start of each task. Update as needed.**

```
SOURCE:   [path to source file]
TARGET:   [path to target .ens file]

MAPPING  (source data → ENSDF data fields in records/comments)
  [Data A]  →  [record type, field name, comments]
  [Data B]  →  [record type, field name, comments]

OPERATIONS
  REPLACE   [field]  with source value   [e.g., G-record RI, DRI from source]
  KEEP      [field]  from target         [e.g., G-record M, MR, DMR; cG M$ comments]
  ADD       [field]  from source         [e.g., new G-records absent in target]
  MERGE     [field]  from both           [e.g., cG RI$ comments quoting both sources]
  AVERAGE   [field]  across sources      [e.g., weighted average of two RI datasets]

MATCHING
  Match L-records by:   [ ] exact E    [ ] E within ±[N] keV
  Match G-records by:   [ ] exact Eγ   [ ] Eγ within ±[N] keV   [ ] parent L first, then Eγ

SPECIAL HANDLING
  [ ] [specify any non-standard cases]
```

This block keeps task-specific customization at the top, separate from the fixed workflow steps. Existing skills using this pattern: `tabular-data-entry`, `reconciling-data`.

---

### Feedback Loop (quality-critical operations)

```markdown
1. Make edits
2. Run: `python scripts/validate.py`
3. Fix errors and return to step 2
4. Proceed only when validation passes
```

### Progress Checklist (multi-step workflows)

```
Task Progress:
- [ ] Step 1: Analyze input  (run analyze.py)
- [ ] Step 2: Create mapping (edit fields.json)
- [ ] Step 3: Validate       (run validate.py)
- [ ] Step 4: Execute        (run apply.py)
```

### Template Pattern

For strict output format: use `"ALWAYS use this exact template"`.
For flexible output: use `"Here is a sensible default — adjust as needed"`.

### Examples Pattern

When output quality depends on seeing examples, provide explicit input → output pairs rather than descriptions alone.

### Conditional Workflow

```markdown
1. Determine type:
   **New document?** → Follow Creation workflow below
   **Editing existing?** → Follow Editing workflow below
```

### One Default, Not Multiple Options

```
# Bad — forces a decision
"You can use pypdf, pdfplumber, PyMuPDF, or pdf2image..."

# Good — default with escape hatch
Use pdfplumber. For scanned PDFs needing OCR, use pdf2image + pytesseract instead.
```

### No Time-Sensitive Information

Use "Legacy" / "Current" sections instead of date conditionals:

```markdown
## Current method
Use v2 API: `api.example.com/v2/messages`

## Legacy (v1, deprecated)
...
```

---

## Anti-Patterns

- **Windows paths** — always use forward slashes: `scripts/helper.py` not `scripts\helper.py`
- **Too many options** — one default with escape hatch, not a menu
- **Assumed installs** — list required packages explicitly
- **Chained references** — one level deep only
- **Time-sensitive conditionals** — use "Legacy/Current" sections instead

---

## Creation Checklist

**Frontmatter**
- [ ] `name`: lowercase/hyphens only, matches folder name, no reserved words
- [ ] `description`: third person, WHAT + WHEN, trigger keywords, colons quoted

**Content**
- [ ] No rules already in `copilot-instructions.md` or `FRIBND.agent.md` — referenced instead
- [ ] Every line justifies its token cost; nothing Claude already knows
- [ ] One default per task; alternatives only for genuine edge cases
- [ ] Consistent terminology (one term per concept)
- [ ] No time-sensitive conditionals
- [ ] For data-entry/reconciliation skills: Task Configuration template is the first section

**Structure**
- [ ] Body under 100 lines
- [ ] References at most one level deep
- [ ] Reference files > 100 lines have a table of contents
- [ ] All paths use forward slashes

**Testing**
- [ ] Description triggers on expected user phrases
- [ ] Tested with a real task (not synthetic)
- [ ] Feedback loops present for quality-critical operations
