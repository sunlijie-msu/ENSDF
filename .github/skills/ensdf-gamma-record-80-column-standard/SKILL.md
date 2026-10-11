---
name: ensdf-gamma-record-80-column-standard
description: "Defines ENSDF gamma (G-record) 80-column fields, flags, and indicators. Use when checking, interpreting, or formatting an ENSDF G-record."
---

# Gamma Transition Record (G-Record)

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q
 35P   G 1572.0    10 70.0   24 M1(+E2)  -0.1    +3-4  0.090  20 71.0     25A  ?
 34Cl  G 2572.0    5  5.0    2  D+Q      +0.85   23    0.05   5  5.1      6 B  S
```

| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)         |
| CONT  | 6       | Continuation label                                                |
| SPACE | 7       | Must be blank                                                     |
| RTYPE | 8       | Record type: `G` (Gamma Transition).                              |
| PSYM  | 9       | Particle symbol must be blank                                     |
| E     | 10–19   | Gamma energy                                                      |
| DE    | 20–21   | Energy uncertainty                                                |
| SPACE | 22      | Readability space                                                 |
| RI    | 23–29   | Relative photon intensity (starts at col 23)                      |
| DRI   | 30–31   | Uncertainty in RI (including GT, LT markers)                      |
| SPACE | 32      | Readability space                                                 |
| M     | 33–41   | Multipolarity                                                     |
| MR    | 42–49   | Mixing ratio                                                      |
| DMR   | 50–55   | Uncertainty in MR                                                 |
| CC    | 56–62   | Conversion coefficient                                            |
| DCC   | 63–64   | Uncertainty in CC                                                 |
| TI    | 65–74   | Total transition intensity                                        |
| DTI   | 75–76   | Uncertainty in TI                                                 |
| C     | 77      | Comment flag (A-Z, a-z, *, &, @) - See G-Record Flag Rules        |
| SPACE | 78      | Usually blank; may be C to indicate coincidence (rarely used)     |
| SPACE | 79      | Usually blank; may be N to indicate use for normalization         |
| Q     | 80      | Additional indicator (space, ?, S) - See G-Record Indicator Rules |

## G-Record Flag Rules

**Column 77 (C Field, Comment Flag):**
- `A-Z`, `a-z`: Any single letter used to refer to a specific comment record (cannot be a number).
- `*` (asterisk): Denotes a multiply-placed gamma ray.
- `&` (ampersand): Denotes a multiply-placed gamma transition with intensity not divided.
- `@` (at symbol): Denotes a multiply-placed gamma transition with intensity suitably divided.
- `Space`: No comment flag.
- **FORBIDDEN:** Question mark (`?`) is NOT allowed in column 77.
- Flag definition letters are human-controlled: parenthesized letters in an identifier (`cL J(A)$`, `cL E(B)$`, `cG E(D),RI(D)$`) name the col-77 flag of the records the comment applies to.

Note: Multiple identical gamma energies appearing in multiple level blocks should be flagged with either `*`, `&`, or `@`.

## G-Record Indicator Rules

**Column 80 (Q Field, Additional Indicator):**
- `Space`: Normal, well-established gamma transition.
- `?`: Denotes uncertain placement of the transition in the level scheme.
- `S`: Denotes expected or assumed, but as yet unobserved, gamma transition.
- **CRITICAL:** Only space, `?`, or `S` allowed in column 80.
