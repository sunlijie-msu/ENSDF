---
name: nds-doi-lookup
description: >
  Use this skill when looking up and verifying DOIs for the most recent
  Nuclear Data Sheets (NDS) evaluation articles by mass number A. Uses the
  NNDC EvaluationIndexServlet as ground truth, Crossref REST API for DOI
  discovery, and the Elsevier linking hub for confirmation. Inserts verified
  DOI lines in ascending A order into Data Check Report .txt files.
argument-hint: [space-separated list of mass numbers, e.g. 204 207 208 211 212]
---

# NDS DOI Lookup Skill

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Critical Rule: NNDC EvaluationIndexServlet Is the ONLY Ground Truth

**MANDATORY FIRST STEP** for any citation lookup or verification task: fetch the NNDC Evaluation Index and inspect the `citation` field.

```
fetch https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet
```

Each `MASS` entry in the returned JSON has a `citation` field with two possible forms:

| `citation` value | Meaning | Action |
|---|---|---|
| `"ENSDF"` | **Continuous internal ENSDF evaluation** -- no published journal paper is the current authoritative source. Old journal papers for this A exist but are superseded. | Set citation to `"Continuous internal ENSDF"`, blank DOI, blank or known evaluator name. **Never substitute an old Crossref paper.** |
| `"NDS vol, page (year)"` | A specific published NDS paper is the current evaluation. | Use Crossref to find the DOI for that exact citation, then record it. |

**CRITICAL:** Many mass chains (e.g., A=77, 101, 108, 117, 165, 224 as of 2025) are marked `"citation":"ENSDF"` in the NNDC index. These chains have older published papers in Crossref, but those papers are **no longer the current evaluation**. Do NOT use them. The NNDC index is the only authoritative source for which papers are current.

Always re-fetch the NNDC index live -- never rely on hardcoded or cached data, as the index is updated when new evaluations are published (e.g., A=216, 261, 265 switched from old papers to new NDS vol.209 (2026) papers during the 2025 evaluation cycle).

---

## Workflow

### 1. Retrieve Ground Truth from NNDC

```
fetch https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet
```

Parse the resulting JSON. For `type=MASS` entries, extract the `citation` field for the desired mass number(s).

- If `citation == "ENSDF"`: record as continuous internal ENSDF -- **stop here, no DOI needed**.
- If `citation` is a journal reference (`"NDS vol, page (year)"`): proceed to Step 2.

### 2. Discover DOI via Crossref

Using the exact citation details from NNDC, query Crossref with the ISSN filter for Nuclear Data Sheets (`issn:0090-3752`) and volume:

```
https://api.crossref.org/works?query.bibliographic={journal}+{volume}+{page}+{year}&rows=20&filter=issn:0090-3752
```

Extract the item whose `page` field starts with the target page number. Read off `DOI` and `author` list.

*Note: The `filter=container-title:Nuclear+Data+Sheets` syntax causes HTTP 400 errors. Use `filter=issn:0090-3752` instead. For very recent publications (current year), prefer `filter=issn:0090-3752,from-pub-date:{year-1}` to limit the result set.*

### 3. Insert into Report or Table

Insert one line per mass number in **ascending A order**:

```
Nuclear Data Sheets for A={A} https://doi.org/{DOI}
```

Match the formatting of any pre-existing entries in the file. After editing, read back the modified section to confirm all entries are present, correctly ordered, and surrounding text is intact.

---

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Using old Crossref papers for ENSDF-tagged chains | **Fatal error.** Always check NNDC `citation` field first. If `"ENSDF"`, the old paper is superseded -- never use it. |
| Hallucinated or missing A<45 masses | Never search by title alone; always use NNDC `EvaluationIndexServlet` as ground truth. |
| Stale hardcoded NNDC data | Always re-fetch live; new evaluations are published frequently (e.g., A=216,261,265 switched to NDS 209 (2026)). |
| Crossref rate limiting / silent drops | Use sequential fallback limits; handle `HTTP Error 400`; avoid aggressive multithreading. |
| `filter=container-title:` in Crossref URL | Causes HTTP 400. Use `filter=issn:0090-3752` instead. |
| URL encoding errors | Carefully encode citation strings in `query.bibliographic` requests. |
| Non-NDS journals | Light mass chains often resolve to "Nuclear Physics A" (`NP A`) rather than "Nuclear Data Sheets" (`NDS`). |
| Grouped evaluations (one paper covers multiple A) | One DOI may serve multiple A values (e.g., NDS 209, 499 covers A=261 and A=265). Both rows get the same DOI. |