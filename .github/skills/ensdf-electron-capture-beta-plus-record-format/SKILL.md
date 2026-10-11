---
name: ensdf-electron-capture-beta-plus-record-format
description: "Defines ENSDF electron-capture/beta-plus (E-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF E-record."
---

# Electron Capture and Beta Plus Decay Record (E-Record)

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  E EEEE.E    DE IB     DI IE     DI LOGFT  DFT            TI        DICUNQ
 35CL  E 1750.0    5  65.0   8  35.0   5  4.85   15             100.0     8 C1US
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)                       |
| CONT  | 6       | Continuation identifier (blank or any alphanumeric character)                   |
| SPACE | 7       | Must be blank                                                                   |
| RTYPE | 8       | Record type `E` for electron capture and beta-plus decay                        |
| PSYM  | 9       | Particle symbol must be blank                                                   |
| E     | 10–19   | Energy for electron capture to level (no need to edit)                          |
| DE    | 20–21   | Uncertainty in E                                                                |
| SPACE | 22      | Readability space                                                               |
| IB    | 23–29   | Intensity of beta-plus-decay branch                                             |
| DIB   | 30–31   | Uncertainty in IB                                                               |
| IE    | 32–39   | Intensity of electron capture branch                                            |
| DIE   | 40–41   | Uncertainty in IE                                                               |
| SPACE | 42      | Readability space                                                               |
| LOGFT | 43–49   | The log ft for (electron capture + beta-plus) transition                        |
| DFT   | 50–55   | Uncertainty in LOGFT                                                            |
| SPACE | 56–64   | Must be blank                                                                   |
| TI    | 65–74   | Total (electron capture + beta-plus) decay intensity                            |
| DTI   | 75–76   | Uncertainty in TI                                                               |
| C     | 77      | Comment flag (`C` denotes coincidence, `?` denotes probable coincidence)        |
| UN    | 78–79   | Forbiddenness classification (`1U`, `2U` for unique forbidden, blank = allowed) |
| Q     | 80      | `?` = uncertain branch, `S` = expected or assumed transition                    |

**Critical E-Record Rules:**
- Must follow LEVEL record for the level being populated in the decay.
- IE, IB and TI must be in same units.
- TI = IE + IB for total decay intensity to the level.
- Forbiddenness classification in columns 78-79 (`1U`, `2U` for first-, second-unique forbidden).
