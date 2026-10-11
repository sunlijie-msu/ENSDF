---
name: ensdf-general-comment-format
description: "Defines ENSDF general comment 80-column fields, c/t identifiers, and scope notes. Use when checking, interpreting, or formatting general comments that precede L, G, B, E, A, and DP records."
---

# General Comment


| Field | Columns | Description                                                            |
| :---- | :------ | :--------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)              |
| CONT  | 6       | Continuation identifier: Blank or any alphanumeric character (not `1`) |
| C     | 7       | Comment Identifier: `c`                                                |
| RTYPE | 8       | Blank or record type of records to which the comment pertains          |
| PSYM  | 9       | Blank or particle symbol: `N`/`P`                                      |
| CTEXT | 10–80   | Text of the comment.                                                   |

## Notes

General comments must precede all L, G, B, E, A, and DP data records.

