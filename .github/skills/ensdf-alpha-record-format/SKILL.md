---
name: ensdf-alpha-record-format
description: "Defines ENSDF alpha-decay (A-record) 80-column fields and record-specific rules. Use when checking, interpreting, or formatting an ENSDF A-record."
---

# Alpha Decay Record (A-Record)

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
MMMXX  A EEEE.E    DE IA     DI HF     DHF                                  C  Q
204AT  A 6632      6  100    5  1.5    3                                    C  ?
```

| Field | Columns | Description                                                                    |
| :---- | :------ | :----------------------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS `, `152Gd`)                      |
| CONT  | 6       | Continuation label                                                             |
| SPACE | 7       | Must be blank                                                                  |
| RTYPE | 8       | Record type: `A` for alpha decay                                               |
| PSYM  | 9       | Particle symbol must be blank                                                  |
| E     | 10–19   | Alpha energy in keV                                                            |
| DE    | 20–21   | Standard uncertainty in E                                                      |
| SPACE | 22      | Readability space                                                              |
| IA    | 23–29   | Intensity of α-decay branch in percent of the total α decay                    |
| DIA   | 30–31   | Standard uncertainty in IA                                                     |
| SPACE | 32      | Readability space                                                              |
| HF    | 33–39   | Hindrance factor for α decay                                                   |
| DHF   | 40–41   | Standard uncertainty in HF                                                     |
| SPACE | 42–76   | Must be blank                                                                  |
| C     | 77      | Comment flag (`C` denotes coincidence, `?` denotes probable coincidence)       |
| SPACE | 78–79   | Must be blank                                                                  |
| Q     | 80      | `?` = uncertain or questionable α branch, `S` = expected or predicted α branch |

**Critical A-Record Rules:**
- Must follow the daughter LEVEL record for the level being populated in the α decay.
