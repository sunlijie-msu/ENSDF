---
name: ensdf-delayed-particle-record-80-column-standard
description: "Defines ENSDF delayed-particle (DP-record) 80-column fields and shared DN, DA, DD, and DT formatting. Use when checking or formatting delayed proton or related delayed-particle records."
---

# Delayed Proton Emission Record (DP-Record)

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  DP EP       DE IP     DI EI                                              
 35CL  DP 501      10 3.5    12 9022                                            
```

| Field | Columns | Description                            |
| :---- | :------ | :------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., " 35P " or " 34Cl")     |
| CONT  | 6       | Continuation label (blank)             |
| SPACE | 7       | Must be blank                          |
| RTYPE | 8       | Record type `D` for delayed particle   |
| PSYM  | 9       | Particle symbol `P` for proton         |
| SPACE | 10      | Readability space                      |
| EP    | 11–19   | Proton energy in keV                   |
| DE    | 20–21   | Energy uncertainty                     |
| SPACE | 22      | Readability space                      |
| IP    | 23–29   | Proton intensity in percent            |
| DIP   | 30–31   | Uncertainty in IP                      |
| SPACE | 32      | Readability space                      |
| EI    | 33–39   | Energy of proton-emitting level in keV |

**Critical DP Format Rules:**
- Delayed Neutron Emission Record (DN-Record), Delayed Alpha Emission Record (DA-Record), Delayed Deuteron Emission Record (DD-Record), and Delayed Triton Emission Record (DT-Record) follow the same format as DP-Records, with `D` in column 8 and `N`, `A`, `D`, or `T` in column 9, respectively.
- Readable spaces at columns 10, 22, and 32 for human readability.
- All field positioning follows standard ENSDF left-justification rules.
