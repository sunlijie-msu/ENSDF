---
name: ensdf-footnote-comment-format
description: "Defines ENSDF footnote-comment fields, SYM(FLAG)$ syntax, FLAG rules, BAND labels, and field relabeling. Use when checking or formatting footnote comments for L, G, B, E, A, and DP records."
---

# Footnote Comment

| Field | Columns | Description                                                           |
| :---- | :------ | :-------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`)     |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`      |
| C     | 7       | Comment identifier: `c`                                               |
| RTYPE | 8       | Blank, or the record type to which the comment applies                |
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
