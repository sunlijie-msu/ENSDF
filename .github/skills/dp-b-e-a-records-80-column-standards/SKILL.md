---
name: dp-b-e-a-records-80-column-standards
description: "ENSDF DP (Delayed Proton), B (Beta Minus), E (Electron Capture/Beta Plus), and A (Alpha) record 80-column format specifications and field definitions."
---

# DP, B, E, and A Record 80-Column Standards

Use this skill when checking or writing delayed proton, beta minus, electron capture/beta plus, or alpha decay records in ENSDF files.

## Record Standards

### Delayed Proton Emission Record (DP-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  DP EP       DE IP     DI EI                                              
 35CL  DP 501      10 3.5    12 9022                                            
```

| Field | Columns | Description                            |
| :---- | :------ | :------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., " 35Cl" or " 35P ")     |
| CONT  | 6       | Continuation label (blank)             |
| SPACE | 7       | Must be blank                          |
| D     | 8       | "D" for delayed particle               |
| P     | 9       | "P" for proton                         |
| SPACE | 10      | Readability space                      |
| EP    | 11–19   | Proton energy in keV                   |
| DE    | 20–21   | Energy uncertainty                     |
| SPACE | 22      | Readability space                      |
| IP    | 23–29   | Proton intensity in percent            |
| DIP   | 30–31   | Uncertainty in IP                      |
| SPACE | 32      | Readability space                      |
| EI    | 33–39   | Energy of proton-emitting level in keV |

**Critical DP Format Rules:**
- Delayed Neutron Emission Record (DN-Record), Delayed Alpha Emission Record (DA-Record), Delayed Deuteron Emission Record (DD-Record), and Delayed Triton Emission Record (DT-Record) follow the same format as DP-Records, with "D" in column 8 and "N", "A", "D", or "T" in column 9, respectively.
- Readable spaces at columns 10, 22, and 32 for human readability.
- All field positioning follows standard ENSDF left-justification rules.

### Beta Minus Decay Record (B-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  B EEEE.E    DE IB     DI           LOGFT  DFT                        CUNQ
 35P   B 1572.0    1  100.0  4            5.23   12                         C1U 
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nucleus (e.g., " 35P " or " 35Cl")                                              |
| CONT  | 6       | Continuation label                                                              |
| SPACE | 7       | Must be blank                                                                   |
| TYPE  | 8       | "B" for beta minus                                                              |
| SPACE | 9       | Must be blank                                                                   |
| E     | 10–19   | Endpoint energy of β⁻ in keV (no need to edit)                                  |
| DE    | 20–21   | Energy uncertainty                                                              |
| SPACE | 22      | Readability space                                                               |
| IB    | 23–29   | Intensity of β⁻-decay branch                                                    |
| DIB   | 30–31   | Uncertainty in IB                                                               |
| SPACE | 32–41   | Must be blank                                                                   |
| SPACE | 42      | Readability space                                                               |
| LOGFT | 43–49   | The log ft for the β⁻ transition                                                |
| DFT   | 50–55   | Uncertainty in LOGFT                                                            |
| SPACE | 56–76   | Must be blank                                                                   |
| C     | 77      | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence)        |
| UN    | 78–79   | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q     | 80      | '?' denotes uncertain or questionable beta minus decay                          |

**Critical B-Record Rules:**
- Must follow LEVEL record for the level which is fed by the beta minus decay.
- IB intensity in same units as other intensity fields in file.
- LOGFT for uniqueness classification (col 78-79).
- Blank signifies allowed transition for forbiddenness field.

### Electron Capture and Beta Plus Decay Record (E-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  E EEEE.E    DE IB     DI IE     DI LOGFT  DFT            TI        DICUNQ
 35CL  E 1750.0    5  65.0   8  35.0   5  4.85   15             100.0     8 C1US
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nucleus (e.g., " 35Cl" or " 35P ")                                              |
| CONT  | 6       | Continuation label                                                              |
| SPACE | 7       | Must be blank                                                                   |
| TYPE  | 8       | "E" for electron capture                                                        |
| SPACE | 9       | Must be blank                                                                   |
| E     | 10–19   | Energy for electron capture to level (no need to edit)                          |
| DE    | 20–21   | Uncertainty in E                                                                |
| SPACE | 22      | Readability space                                                               |
| IB    | 23–29   | Intensity of β⁺-decay branch                                                    |
| DIB   | 30–31   | Uncertainty in IB                                                               |
| IE    | 32–39   | Intensity of electron capture branch                                            |
| DIE   | 40–41   | Uncertainty in IE                                                               |
| SPACE | 42      | Readability space                                                               |
| LOGFT | 43–49   | The log ft for (ε + β⁺) transition                                              |
| DFT   | 50–55   | Uncertainty in LOGFT                                                            |
| SPACE | 56–64   | Must be blank                                                                   |
| TI    | 65–74   | Total (ε + β⁺) decay intensity                                                  |
| DTI   | 75–76   | Uncertainty in TI                                                               |
| C     | 77      | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence)        |
| UN    | 78–79   | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q     | 80      | '?' = uncertain branch, 'S' = expected or assumed transition                    |

**Critical E-Record Rules:**
- Must follow LEVEL record for the level being populated in the decay.
- IE, IB and TI must be in same units.
- TI = IE + IB for total decay intensity to the level.
- Forbiddenness classification in columns 78-79 ('1U', '2U' for first-, second-unique forbidden).

### Alpha Decay Record (A-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
235XX  A EEEE.E    DE IA     DI HF     DHF                                  C  Q
204AT  A 6632      6  100    5  1.5    3                                    C  ?
```

| Field | Columns | Description                                                                    |
| :---- | :------ | :----------------------------------------------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., " 35P " or "204AT")                                             |
| CONT  | 6       | Continuation label                                                             |
| SPACE | 7       | Must be blank                                                                  |
| TYPE  | 8       | "A" for alpha decay                                                            |
| SPACE | 9       | Must be blank                                                                  |
| E     | 10–19   | Alpha energy in keV                                                            |
| DE    | 20–21   | Standard uncertainty in E                                                      |
| SPACE | 22      | Readability space                                                              |
| IA    | 23–29   | Intensity of α-decay branch in percent of the total α decay                    |
| DIA   | 30–31   | Standard uncertainty in IA                                                     |
| SPACE | 32      | Readability space                                                              |
| HF    | 33–39   | Hindrance factor for α decay                                                   |
| DHF   | 40–41   | Standard uncertainty in HF                                                     |
| SPACE | 42–76   | Must be blank                                                                  |
| C     | 77      | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence)       |
| SPACE | 78–79   | Must be blank                                                                  |
| Q     | 80      | '?' = uncertain or questionable α branch, 'S' = expected or predicted α branch |

**Critical A-Record Rules:**
- Must follow the daughter LEVEL record for the level being populated in the α decay.
