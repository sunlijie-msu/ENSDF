---
name: nds-doi-lookup
description: Look up and verify DOIs for the most recent Nuclear Data Sheets (NDS) evaluation articles by mass number A. Uses the Crossref REST API for discovery and the Elsevier linking hub for per-DOI identity confirmation. Inserts verified DOI lines (ascending A order) into Data Check Report .txt files. Use when a Data Check Report needs to cite NDS evaluations as traceability references.
argument-hint: [space-separated list of mass numbers, e.g. 204 207 208 211 212]
---

# NDS DOI Lookup Skill

## Workflow

### 1. Retrieve Ground Truth from NNDC

Never rely on raw Crossref title searches (e.g., "Nuclear Data Sheets for A={A}"), as this hallucinates or misses grouped evaluations (especially A < 45). Instead, query the official NNDC Evaluation Index as the golden source:

```
fetch https://www.nndc.bnl.gov/ensdf/EvaluationIndexServlet
```

Parse the resulting JSON to extract the exact `journal`, `volume`, `page`, and `year` for the desired mass chain.

### 2. Discover DOI via Crossref

Using the exact citation details obtained from NNDC, build a precise bibliographic query for Crossref. Use **sequential, rate-limited** requests to avoid silent API drops.

```
https://api.crossref.org/works?query.bibliographic={journal}+{volume}+{page}+{year}&select=DOI,title,author,volume,published-print,page&rows=5
```

*Note: Ensure proper URL encoding for spaces and special characters. Avoid concurrent API flooding which causes missed records.*

Extract the DOI and Author list matching the exact volume and page.

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
| Hallucinated or Missing A<45 Masses | Never search by title alone; always use NNDC `EvaluationIndexServlet` as ground truth. |
| Crossref Rate Limiting/Silent Drops | Use sequential fallback limits and handle exceptions (`HTTP Error 400`); avoid aggressive multithreading. |
| URL Encoding Errors | Carefully encode citation strings in `query.bibliographic` requests to avoid HTTP 400 Bad Request errors. |
| Non-NDS Journals | Light mass chains often resolve to "Nuclear Physics A" (`NP A`) rather than "Nuclear Data Sheets" (`NDS`). |
