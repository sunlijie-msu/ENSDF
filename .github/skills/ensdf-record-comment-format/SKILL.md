---
name: ensdf-record-comment-format
description: "Defines ENSDF record comment 80-column fields, SYM$ identifiers, and placement rules. Use when checking, interpreting, or formatting comments attached to L, G, B, E, A, or DP records (cL, cG, 2cL, and similar)."
---

# Record Comment

| Field | Columns | Description                                                            |
| :---- | :------ | :--------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)              |
| CONT  | 6       | Continuation identifier: Blank or any alphanumeric character (not `1`) |
| C     | 7       | Comment Identifier: `c`                                                |
| RTYPE | 8       | Blank or record type of records to which the comment pertains          |
| PSYM  | 9       | Blank or particle symbol: `N`/`P`                                      |
| SYM   | 10–80   | `$` or `SYM$` or `SYM,SYM$`                                            |
| CTEXT | 10–80   | Text of comment follows the `$`delimiter                               |


## Notes

- Record comments placed following a record of the same RTYPE refer only to that one record.
- Example: a comment record with `cL` in columns 7-8 and `T$` in columns 10-11, placed following the level record for the second-excited state, refers to the half-life of only the second-excited state.

- Specified field symbol `SYM` must be followed by `$` delimiter. `SYM` can be any data field of the L, G, B, E, A, or DP record (e.g., `E`, `J`, `T`, `S`, `RI`, `M`, `MR`, etc).

- On continuation comment records, CTEXT may start in column 10, and SYM or SYMs are not repeated.
