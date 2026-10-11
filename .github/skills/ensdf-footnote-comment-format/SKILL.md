---
name: ensdf-footnote-comment-format
description: "Defines ENSDF footnote comment 80-column fields, SYM(FLAG)$ identifiers, FLAG rules, BAND, and field relabeling. Use when checking, interpreting, or formatting footnote comments that precede L, G, B, E, A, and DP records."
---

# Footnote Comment

| Field | Columns | Description                                                            |
| :---- | :------ | :--------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)              |
| CONT  | 6       | Continuation identifier: Blank or any alphanumeric character (not `1`) |
| C     | 7       | Comment Identifier: `c`                                                |
| RTYPE | 8       | Blank or record type of records to which the comment pertains          |
| PSYM  | 9       | Blank or particle symbol: `N`/`P`                                      |
| SYM   | 10–80   | `SYM$`, `SYM,SYM$`, `SYM(FLAG)$`, `SYM(FLAG),SYM(FLAG)$`               |
| CTEXT | 10–80   | Text of comment follows the `$`delimiter                               |

## Notes

Footnote comments must precede all L, G, B, E, A, and DP data records.

1. `SYM` can be any data field of the L, G, B, E, A, or DP record (e.g., `E`, `J`, `T`, `S`, `RI`, `M`, `MR`, etc), or `BAND`: requires a FLAG. Text after `$` is the band label in drawings.
2. Without `(FLAG)`: applies to that `SYM` field of all records of the `RTYPE` in the dataset.
   1. Example: ` 34S  cL E$From a least-squares fit to |g-ray energies.` applies to all `E` fields of `L` records in the dataset.
3. With `(FLAG)`: applies only to that `SYM` field of records carrying the `FLAG`.
4. Example: ` 34S  cL E(A),J(A)$From {+30}Si(|a,|g):resonances.` applies only to `E` and `J` fields of `L` records carrying the `A` flag.
4. `FLAG` is placed in column 77 of the record (single character), or assigned in a `FLAG=` continuation record (character string).
5. `LABEL=name` replaces the standard heading of a field in the output table. Keep `name` short.
