---
name: ensdf-footnote-comment-format
description: "Defines ENSDF footnote comment 80-column fields, SYM(FLAG)$ identifiers, FLAG rules, BAND, and field relabeling. Use when checking, interpreting, or formatting footnote comments that precede L, G, B, E, A, and DP records."
---

# Footnote Comment

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

Footnote comments must precede L, G, B, E, A, and DP records. Columns 1–9 are the same as in record comments: `.github/skills/ensdf-record-comment-format/SKILL.md`.

| Field | Columns | Description                                                                                                                                                                               | Reference |
| :---- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- |
| SYM   | 10–80   | `SYM$`, `SYM,SYM,...,$`, `SYM(FLAG)$`, `SYM(FLAG),$`, or `SYM(FLAG),...,$`. See Note 1. FLAG is any ASCII alphanumeric character or string of alphanumeric characters. Field must end with `$`. See Note 1 on record comments for the exception | V.8       |
| CTEXT | 10–80   | Text of comment follows `$`. On continuation comment records, SYM or SYM(FLAG) are not repeated. See ENSDF Translation Dictionary (Appendix F)                                            | V.7       |

## Notes

1. SYM can only be one of the following:
   - The fields defined in formatted L, G, B, E, A, DP records.
   - `BAND`. This SYM must be accompanied by a FLAG. Text following the `$` delimiter, or in columns 20–80 in the old format, appears as the band label in some drawings. Give any other information on that band on continuation records.
2. Footnote types:
   - Footnote without FLAG:
     - Refers to all records of the specified RTYPE in the data set.
     - Normally appears only in the table for that RTYPE in the output. Example: a footnote on levels (`L` in column 8) appears only in the level properties table.
   - Footnote with FLAG:
     - Only those records are footnoted for which footnote flags are given; see Note 3.
     - Only those data values of data types specified by SYM that are associated with a given FLAG are footnoted.
3. Footnote FLAG must be either a single character placed in column 77 of the formatted record, or a string of characters assigned to a special data type called FLAG on the following continuation record. Examples of flags on a continuation record:

   ```text
   152EU2 G FLAG=ABCD$
   156GD2 L FLAG=KMP$
   ```

4. No footnotes are allowed for records of RTYPE: `N`, `P`, or `Q`.
5. To change the standard label heading of a formatted field, e.g., S to C2S for L records, CTEXT must have the form `LABEL=name`, where `name` is the new label desired. Keep the new label as short as possible. FLAG cannot be specified with relabeling. Any other comment on the relabeled field must appear on a different record. Examples of field relabel:

   ```text
   156GD CL S$LABEL=C2S
   156GD CL S$LABEL=DSIGMA/DOMEGA (45 DEG)
   ```
