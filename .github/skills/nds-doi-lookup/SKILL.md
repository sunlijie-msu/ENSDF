---
name: nds-doi-lookup
description: Look up and verify DOIs for the most recent Nuclear Data Sheets (NDS) evaluation articles by mass number A. Uses the Crossref REST API for discovery and the Elsevier linking hub for per-DOI identity confirmation. Inserts verified DOI lines (ascending A order) into Data Check Report .txt files. Use when a Data Check Report needs to cite NDS evaluations as traceability references.
argument-hint: [space-separated list of mass numbers, e.g. 204 207 208 211 212]
---

# NDS DOI Lookup Skill

## Workflow

### 1. Discover via Crossref

Query all mass numbers in a **single parallel** `fetch_webpage` call:

```
https://api.crossref.org/works?query.title=Nuclear+Data+Sheets+for+A%3D{A}&rows=5&select=DOI,title,author,volume,published-print,page
```

Select the result whose title matches `"Nuclear Data Sheets for A = {A}"` (case-insensitive) with the **most recent** publication year. Reject non-matching titles (e.g., "Symbols and Abbreviations", update articles, or articles whose volume number coincidentally equals A).

### 2. Verify via Elsevier Linking Hub

For each candidate DOI, follow the redirect chain and confirm `articleName` matches:

```
fetch https://doi.org/{DOI}
  → redirect to https://linkinghub.elsevier.com/retrieve/pii/{PII}
  → confirm:  articleName : 'Nuclear Data Sheets for A = {A}'
```

Issue all verification fetches in a single parallel call. A DOI is accepted only after this confirmation.

### 3. Insert into Report

Insert one line per mass number in **ascending A order**:

```
Nuclear Data Sheets for A={A} https://doi.org/{DOI}
```

Match the formatting of any pre-existing entries in the file. After editing, read back the modified section to confirm all entries are present, correctly ordered, and surrounding text is intact.

---

## Pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Crossref volume number equals A | Match on title text, not volume |
| Older edition returned first | Sort by year; take latest |
| `query.bibliographic` causes token overflow | Always use `query.title` + `select=` |
| DOI resolves to wrong article | Verify `articleName` at linking hub before accepting |
