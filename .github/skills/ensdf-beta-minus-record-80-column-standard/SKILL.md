---
name: ensdf-beta-minus-record-80-column-standard
description: "Defines ENSDF beta-minus (B-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF B-record."
---

# Beta Minus Decay Record (B-Record)

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  B EEEE.E    DE IB     DI           LOGFT  DFT                        CUNQ
 35P   B 1572.0    1  100.0  4            5.23   12                         C1U 
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nucleus (e.g., " 35P " or " 34Cl")                                              |
| CONT  | 6       | Continuation label                                                              |
| SPACE | 7       | Must be blank                                                                   |
| RTYPE | 8       | Record type `B` for beta minus                                                  |
| PSYM  | 9       | Particle symbol must be blank                                                   |
| E     | 10–19   | Endpoint energy of beta in keV (no need to edit)                                |
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
- Must follow LEVEL record for the level which is fed by the beta minus decay.
- IB intensity in same units as other intensity fields in file.
- LOGFT for uniqueness classification (col 78-79).
- Blank signifies allowed transition for forbiddenness field.
