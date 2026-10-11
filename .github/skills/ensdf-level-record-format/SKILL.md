---
name: ensdf-level-record-format
description: "Defines ENSDF level (L-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF L-record."
---

# Energy Level Record (L-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q
 35P   L 3572.0    12 3/2+,5/2+        29 FS     14    2        0.8       4 A  ?
 34CL  L 1230      5  1-               0.39 PS   8     1        0.50      15B  S
```

| Field | Columns | Description                                                        |
| :---- | :------ | :----------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`)  |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`   |
| SPACE | 7       | Must be blank.                                                     |
| RTYPE | 8       | Record type: `L` (Level).                                          |
| PSYM  | 9       | Particle symbol must be blank.                                     |
| E     | 10–19   | Level energy.                                                      |
| DE    | 20–21   | Energy uncertainty.                                                |
| SPACE | 22      | Readability space.                                                 |
| J     | 23–39   | Spin `J` and parity `π`                                            |
| T     | 40–49   | Half-life (FS, PS, NS, MS, S, H, D) or level width (EV, KEV, MEV). |
| DT    | 50–55   | Half-life uncertainty.                                             |
| L     | 56–64   | Angular momentum transfer (L-transfer).                            |
| S     | 65–74   | Spectroscopic strength.                                            |
| DS    | 75–76   | Uncertainty in S.                                                  |
| C     | 77      | Comment flag.                                                      |
| MS    | 78–79   | `M` isomer; `R` resonance; `C` PN comment (uncommon)               |
| Q     | 80      | `?` questionable/uncertain; `S` assumed/at separation energy.      |


J field: For multiple J-π values separated by commas, no spaces after commas.
Critical: Be sure to distinguish comment flags (col 77), MS labels (col 78–79), and `?` (col 80).
