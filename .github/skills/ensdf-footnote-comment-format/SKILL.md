---
name: ensdf-footnote-comment-format
description: "Defines ENSDF footnote-comment fields, SYM(FLAG)$ syntax, FLAG rules, BAND labels, and field relabeling. Use when checking or formatting footnote comments for L, G, B, E, A, and DP records."
---

# Footnote Comment

| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`) |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`  |
| C     | 7       | Comment identifier: `c`                                           |
| RTYPE | 8       | Blank, or Record type being commented on                          |
| PSYM  | 9       | Blank, or Particle symbol `N` or `P`                              |
| SYM   | 10–80   | `SYM$`, `SYM,SYM$`, `SYM(FLAG)$`, `SYM(FLAG),SYM(FLAG)$`          |
| CTEXT | 10–80   | Comment text follows the `$` delimiter                            |

## Notes

1. Footnote comments must precede all L, G, B, E, A, and DP data records.
2. `SYM` can be any data field of the L, G, B, E, A, or DP record (e.g., `E`, `J`, `T`, `S`, `RI`, `M`, `MR`, etc).
3. Without `(FLAG)`: applies to the `SYM` field of all `RTYPE` records in the dataset.
   - Example: ` 34S  cL E$From a least-squares fit to |g-ray energies.` applies to the `E` field of all `L` records in the dataset.
4. With `(FLAG)`: applies to the `SYM` field of the `RTYPE` records that carry the `FLAG`.
   - Example: ` 34S  cL E(A),J(A)$From {+30}Si(|a,|g):resonances.` applies to the `E` and `J` fields of the `L` records that carry the `A` flag.
5. `FLAG` is placed in column 77 of the record (single character), or assigned in a `FLAG=` continuation record (character string).
6. `LABEL=name` replaces the standard heading of a field in the output table. Keep `name` short.
