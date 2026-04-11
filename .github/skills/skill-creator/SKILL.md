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

> **If a rule, standard, or convention already exists in `.github/copilot-instructions.md` or `.github/agents/ENSDF-Agent.agent.md`, reference the relevant section — do NOT copy or paraphrase it into SKILL.md.**

**Every ENSDF skill body must begin with this reference line (right after the `#` heading):**

> ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

This avoids stale duplicates and preserves the single source of truth in the instruction files.

---

## Core Principles

### 1. Concise Is Key

SKILL.md shares the context window with conversation history, system prompts, and all loaded skills.

- "Does Claude already know this?" → Remove it.
- "Is this already in `.github/copilot-instructions.md` or `.github/agents/ENSDF-Agent.agent.md`?" → Reference it.
- Body under 90 lines.


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

### Task Customization and Configuration (data-entry and reconciliation skills)

For any skill that processes source data into ENSDF records, place a user-fillable **Task Customization & Configuration** block as the **first section** (before the workflow). The user fills it in at the start of every task; workflow steps remain fixed. Existing skills using this pattern: `tabular-data-entry`, `reconciling-data`.

**Template (copy verbatim as the first section in the new skill):**

~~~markdown
## Task Customization & Configuration

> Fill in before starting task. Update as needed.

### Files
- Source: `[path to source .mrg/.adp/.ens/.md/.csv file]`
- Target: `[path to target .ens file]`

### Field Mapping *(source → ENS)*
- `[Data A]` → `[record type]` `[field name]`
- `[Data B]` → `[record type]` `[field name]`

### Operations
- **Keep** `[field]` from target (e.g., M, MR, DMR; cG M$ comments)
- **Replace/Update** `[field]` with source value (e.g., RI, DRI)
- **Add/Insert** `[field]` from source (e.g., new G-records absent in target)
- **Merge/Combine** `[field]` from both (e.g., cG RI$ comments quoting both)
- **Average** `[field]` across sources (e.g., weighted average of RI)

### Matching
- L-records: `[ ]` exact E  `[ ]` E within ±[N] keV
- G-records: `[ ]` exact Eγ  `[ ]` Eγ within ±[N] keV  `[ ]` parent L first, then Eγ

### Special Handling
- `[ ]` [describe non-standard cases]
~~~

---

### Recommended Operating Procedures


---

## Anti-Patterns

- **Windows paths** — always use forward slashes: `scripts/helper.py` not `scripts\helper.py`
- **Too many options** — one default with escape hatch, not a menu
- **Assumed installs** — list required packages explicitly
- **Unqualified MCP tool names** — always use `ServerName:tool_name` format; bare names cause "tool not found" errors
- **Chained references** — one level deep only
- **Time-sensitive conditionals** — use "Legacy/Current" sections instead

---

## Creation Checklist

**Frontmatter**
- [ ] `name`: lowercase/hyphens only, matches folder name, no reserved words
- [ ] `description`: third person, WHAT + WHEN, trigger keywords, colons quoted

**Content**
- [ ] No rules already in `copilot-instructions.md` or `ENSDF-Agent.agent.md` — referenced instead
- [ ] Every line justifies its token cost; nothing Claude already knows
- [ ] One default per task; alternatives only for genuine edge cases
- [ ] Consistent terminology (one term per concept)
- [ ] No time-sensitive conditionals
- [ ] For data-entry/reconciliation skills: Task Configuration template is the first section

**Structure**
- [ ] Body under 90 lines
- [ ] References at most one level deep
- [ ] Reference files > 100 lines have a table of contents
- [ ] All paths use forward slashes

**Testing**
- [ ] Description triggers on expected user phrases
- [ ] Build ≥3 real-failure evaluations before writing extensive documentation
- [ ] Tested with a real task (not synthetic)
- [ ] Tested with Haiku and Sonnet (Opus may need less guidance than smaller models)
- [ ] Feedback loops present for quality-critical operations
