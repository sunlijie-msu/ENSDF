---
name: ensdf-beta-minus-record-format
description: "Defines ENSDF beta-minus (B-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF B-record."
---

# Beta-Minus Decay Record (B-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  B EEEE.E    DE IB     DI           LOGFT  DFT                        CUNQ
 35P   B 1572.0    1  100.0  4            5.23   12                         C1U 
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`)               |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`                |
| SPACE | 7       | Must be blank                                                                   |
| RTYPE | 8       | Record type `B` for beta minus                                                  |
| PSYM  | 9       | Particle symbol must be blank                                                   |
| E     | 10–19   | Beta-decay endpoint energy in keV                                               |
| DE    | 20–21   | Energy uncertainty                                                              |
| SPACE | 22      | Readability space                                                               |
| IB    | 23–29   | Intensity of beta minus decay branch                                            |
| DIB   | 30–31   | Uncertainty in IB                                                               |
| SPACE | 32–41   | Must be blank                                                                   |
| SPACE | 42      | Readability space                                                               |
| LOGFT | 43–49   | The log ft for the beta minus transition                                        |
| DFT   | 50–55   | Uncertainty in LOGFT                                                            |
| SPACE | 56–76   | Must be blank                                                                   |
| C     | 77      | Comment flag (`C` denotes coincidence, `?` denotes probable coincidence)        |
| UN    | 78–79   | Forbiddenness classification (`1U`, `2U` for unique forbidden, blank = allowed) |
| Q     | 80      | `?` denotes uncertain or questionable beta minus decay                          |

**Critical B-Record Rules:**
- Must follow the L record populated by beta-minus decay.
- `IB` uses the same units as the other intensity fields in the dataset.
- `LOGFT` is the log of the comparative half-life, log ft.
- `UN` (columns 78–79) gives the forbiddenness classification; blank denotes an allowed transition.
