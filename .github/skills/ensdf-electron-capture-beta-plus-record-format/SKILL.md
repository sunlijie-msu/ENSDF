---
name: ensdf-electron-capture-beta-plus-record-format
description: "Defines ENSDF electron-capture/beta-plus (E-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF E-record."
---

# Electron Capture and Beta Plus Decay Record (E-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  E EEEE.E    DE IB     DI IE     DI LOGFT  DFT            TI        DICUNQ
 35CL  E 1750.0    5  65.0   8  35.0   5  4.85   15             100.0     8 C1US
```

| Field | Columns | Description                                                              |
| :---- | :------ | :----------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`)        |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`         |
| SPACE | 7       | Must be blank                                                            |
| RTYPE | 8       | Record type `E` for electron capture and beta-plus decay                 |
| PSYM  | 9       | Particle symbol must be blank                                            |
| E     | 10–19   | Energy for electron capture to the level                                 |
| DE    | 20–21   | Uncertainty in E                                                         |
| SPACE | 22      | Readability space                                                        |
| IB    | 23–29   | Intensity of beta-plus-decay branch                                      |
| DIB   | 30–31   | Uncertainty in IB                                                        |
| IE    | 32–39   | Intensity of electron capture branch                                     |
| DIE   | 40–41   | Uncertainty in IE                                                        |
| SPACE | 42      | Readability space                                                        |
| LOGFT | 43–49   | Log ft for the combined electron-capture and beta-plus transition        |
| DFT   | 50–55   | Uncertainty in LOGFT                                                     |
| SPACE | 56–64   | Must be blank                                                            |
| TI    | 65–74   | Total (electron capture + beta-plus) decay intensity                     |
| DTI   | 75–76   | Uncertainty in TI                                                        |
| C     | 77      | Comment flag (`C` denotes coincidence, `?` denotes probable coincidence) |
| UN    | 78–79   | Forbiddenness classification                                             |
| Q     | 80      | `?` = uncertain branch, `S` = expected or assumed transition             |

**Critical E-Record Rules:**
- Must follow the L record for the level populated in the decay.
- `IE`, `IB`, and `TI` must use the same normalization reference.
- `TI` is the total decay intensity to the level: `TI = IE + IB`.
- `UN` (columns 78–79) gives the forbiddenness classification (`1U`, `2U` for first- and second-forbidden unique transitions).
