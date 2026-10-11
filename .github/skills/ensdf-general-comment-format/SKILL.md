---
name: ensdf-general-comment-format
description: "Defines ENSDF general comment 80-column fields, c identifiers, and scope. Use when checking, interpreting, or formatting general comments that precede L, G, B, E, A, and DP records."
---

# General Comment


| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`) |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`  |
| C     | 7       | Comment identifier: `c`                                           |
| RTYPE | 8       | Blank, or record type to which the comment applies                |
| PSYM  | 9       | Blank, or particle symbol such as `N` or `P`                      |
| CTEXT | 10–80   | Comment text                                                      |

## Notes

1. General comments must precede all L, G, B, E, A, and DP data records.
2. A general comment with a specified `RTYPE` applies all records of that `RTYPE`.
3. If columns 8 and 9 are blank, the general comment applies to the entire dataset.
