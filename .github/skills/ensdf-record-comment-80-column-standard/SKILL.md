---
name: ensdf-record-comment-80-column-standard
description: "Defines ENSDF record comment 80-column fields, SYM$ identifiers, and placement rules. Use when checking, interpreting, or formatting comments attached to L, G, B, E, A, or DP records (cL, cG, 2cL, and similar)."
---

# Record Comment

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

| Field | Columns | Description                                                                                                                                                  | Reference |
| :---- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| NUCID | 1–5     | Nuclide identification                                                                                                                                       | V.1       |
| CONT  | 6       | Blank, or any alphanumeric character other than `1` for continuation records                                                                                 |           |
| C     | 7       | Letter `C` or `D` is required. See Notes 4 and 5 in the general comment standard: `.github/skills/ensdf-general-comment-record-80-column-standard/SKILL.md` |           |
| RTYPE | 8       | Record type being commented upon. Can be blank for particle records                                                                                          | V.6       |
| PSYM  | 9       | Blank, or symbol for a particle, e.g., `N`, `P`                                                                                                              |           |
| SYM   | 10–80   | `SYM$` or `SYM,SYM,...,$`: type of data being commented upon. Specified SYMs must be followed by `$`, except as in Note 1 below                              | V.8       |
| CTEXT | 10–80   | Text of comment follows the `$`. On continuation comment records, CTEXT may start in column 10, and SYM or SYMs are not repeated. See Appendix F             | V.7       |

## Notes

1. The old format, where SYM were specified in columns 10–19, is accepted without the `$` delimiter as long as column 19 is blank. In this case comment text begins in column 20.
2. Record comments placed following a record of the same RTYPE refer only to that one record. Example: a comment record with `CL` in columns 7–8 and `T$` in columns 10–11, placed following the level record for the second-excited state, refers to the half-life of only the second-excited state.
