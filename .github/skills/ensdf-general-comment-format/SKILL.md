---
name: ensdf-general-comment-format
description: "Defines ENSDF general comment 80-column fields, C/D/T/c/t identifiers, and scope notes. Use when checking, interpreting, or formatting general comments that precede L, G, B, E, A, and DP records."
---

# General Comment

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

General comments must precede all L, G, B, E, A, and DP records.

| Field | Columns | Description                                                                   |
| :---- | :------ | :---------------------------------------------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., " 35P ", " 76AS")                                  |
| CONT  | 6       | Blank, or any alphanumeric character other than `1` for continuation records  |
| C     | 7       | Letter `C`, `D`, or `T` is required. See Notes 3–5 below                      |
| RTYPE | 8       | Blank, or record type of records to which the comment pertains                |
| PSYM  | 9       | Blank, or symbol for a (delayed-)particle, e.g., `N`, `P`                     |
| CTEXT | 10–80   | Text of the comment. See ENSDF Translation Dictionary (Appendix F)            |

## Notes

1. The comment refers only to records of the specified RTYPE given in that data set. The comment normally appears only in the table for that RTYPE in the output. Example: a comment on levels (`L` in column 8) appears only in the level properties table.
2. If columns 8 and 9 are blank, the comment refers to the whole data set. These general comments precede formatted level or radiation records. See Appendix B for use of comment records in the COMMENTS data set.
3. Letter `T` in place of `C` in column 7 indicates to the output programs that the record is reproduced as is, and blanks in the record are not squeezed out.
4. Letter `D` in place of `C` in column 7 indicates a documentation record. Output programs and analysis programs ignore it.
5. Lower-case letters `c` and `t` in column 7 indicate that CTEXT is not translated. It appears as written in Nuclear Data Sheets. Write special characters directly, for example, `jg` for γ, `f+238gPu` for ²³⁸Pu. See Appendix A for the list of special characters.
