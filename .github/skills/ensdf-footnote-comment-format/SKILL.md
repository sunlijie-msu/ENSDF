---
name: ensdf-footnote-comment-format
description: "Defines ENSDF footnote comment 80-column fields, SYM(FLAG)$ identifiers, FLAG rules, BAND, and field relabeling. Use when checking, interpreting, or formatting footnote comments that precede L, G, B, E, A, and DP records."
---

# Footnote Comment

Footnote comments must precede L, G, B, E, A, and DP records. Columns 1–9 are the same as in record comments: `.github/skills/ensdf-record-comment-format/SKILL.md`.
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

1. SYM can only be one of the following:
   - The fields defined in formatted L, G, B, E, A, DP records.
   - `BAND`. This SYM must be accompanied by a FLAG. Text following the `$` delimiter, or in columns 20–80 in the old format, appears as the band label in some drawings. Give any other information on that band on continuation records.
2. Footnote types:
   - Footnote without FLAG:
     - Refers to all records of the specified RTYPE in the data set.

   - Footnote with FLAG:
     - Only those records are footnoted for which footnote flags are given; see Note 3.
     - Only those data values of data types specified by SYM that are associated with a given FLAG are footnoted.
3. Footnote FLAG is usually a single character in column 77 of the record, or a string of characters assigned to a special data type `FLAG` on the following continuation record. Examples of flags on a continuation record:

   ```text
    34S F L FLAG=ABC$
   ```
