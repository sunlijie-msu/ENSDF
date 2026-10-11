---
name: ensdf-record-field-80-column-standards
description: "ENSDF L (Level), G (Gamma), DP (Delayed Proton), B (Beta Minus), E (Electron Capture/Beta Plus), and A (Alpha) record 80-column format specifications and field definitions."
---

# L, G, DP, B, E, and A Record 80-Column Standards

Use this skill when checking or editing level, gamma, delayed proton, beta minus, electron capture/beta plus, or alpha decay records in ENSDF files.

## Record Standards

### ENSDF Record Format Specifications

#### Energy Level Record (L-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q
 35P   L 3572.0    12 3/2+,5/2+        29 FS     14    2        0.8       4 A  ?
 34CL  L 1230      5  1-               0.39 PS   8     1        0.50      15B  S
```

| Field | Columns | Description                                                   |
| :---- | :------ | :------------------------------------------------------------ |
| NUCID | 1–5     | Nucleus (e.g., " 35P ", " 76AS").                             |
| CONT  | 6       | Continuation label.                                           |
| SPACE | 7       | Must be blank.                                                |
| RTYPE | 8       | Record type: `L` (Level).                                     |
| PSYM  | 9       | Particle symbol must be blank.                                |
| E     | 10–19   | Level energy.                                                 |
| DE    | 20–21   | Energy uncertainty.                                           |
| SPACE | 22      | Readability space.                                            |
| J     | 23–39   | Spin `J` and parity `π`                                       |
| T     | 40–49   | Half-life with units (e.g., MEV, KEV, FS, PS, NS, S, H, D).   |
| DT    | 50–55   | Half-life uncertainty.                                        |
| L     | 56–64   | Angular momentum transfer (L-transfer).                       |
| S     | 65–74   | Spectroscopic strength.                                       |
| DS    | 75–76   | Uncertainty in S.                                             |
| C     | 77      | Comment flag.                                                 |
| MS    | 78–79   | 'M ' isomer; 'R ' resonance; 'C ' PN comments (uncommon)      |
| Q     | 80      | `?` questionable/uncertain; `S` assumed/at separation energy. |

J field: For multiple J-π values separated by commas, no spaces after commas.
Critical: Be sure to distinguish comment flags (col 77), MS labels (col 78–79), and `?` (col 80).

**CRITICAL: Comment Line Association**
- `cL` comment lines apply **only** to the immediately preceding L-record.
- Each L-record with or without a following `cL` line is an independent record.

#### Gamma Transition Record (G-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q
 35P   G 1572.0    10 70.0   24 M1(+E2)  -0.1    +3-4  0.090  20 71.0     25A  ?
 34Cl  G 2572.0    5  5.0    2  D+Q      +0.85   23    0.05   5  5.1      6 B  S
```

| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., " 35P ", " 76AS")                                  |
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

#### G-Record Flag Rules

**Column 77 (C Field, Comment Flag):**
-   `A-Z`, `a-z`: Any single letter used to refer to a specific comment record (cannot be a number).
-   `*` (asterisk): Denotes a multiply-placed gamma ray.
-   `&` (ampersand): Denotes a multiply-placed gamma transition with intensity not divided.
-   `@` (at symbol): Denotes a multiply-placed gamma transition with intensity suitably divided.
Note: Multiple identical gamma energies appearing in multiple level blocks should be flagged with either `*`, `&`, or `@`.
-   `Space`: No comment flag.
-   **FORBIDDEN:** Question mark (`?`) is NOT allowed in column 77.
-   Flag definition letters are human-controlled: parenthesized letters in an identifier (`cL J(A)$`, `cL E(B)$`, `cG E(D),RI(D)$`) name the col-77 flag of the records the comment applies to.

#### G-Record Indicator Rules

**Column 80 (Q Field, Additional Indicator):**
-   `Space`: Normal, well-established gamma transition.
-   `?`: Denotes uncertain placement of the transition in the level scheme.
-   `S`: Denotes expected or assumed, but as yet unobserved, gamma transition.
-   **CRITICAL:** Only space, `?`, or `S` allowed in column 80.


### Delayed Proton Emission Record (DP-Record)

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

### Beta Minus Decay Record (B-Record)

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

### Electron Capture and Beta Plus Decay Record (E-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 MMXX  E EEEE.E    DE IB     DI IE     DI LOGFT  DFT            TI        DICUNQ
 35CL  E 1750.0    5  65.0   8  35.0   5  4.85   15             100.0     8 C1US
```

| Field | Columns | Description                                                                     |
| :---- | :------ | :------------------------------------------------------------------------------ |
| NUCID | 1–5     | Nucleus (e.g., " 35P " or " 34Cl")                                              |
| CONT  | 6       | Continuation label                                                              |
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

### Alpha Decay Record (A-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
MMMXX  A EEEE.E    DE IA     DI HF     DHF                                  C  Q
204AT  A 6632      6  100    5  1.5    3                                    C  ?
```

| Field | Columns | Description                                                                    |
| :---- | :------ | :----------------------------------------------------------------------------- |
| NUCID | 1–5     | Nucleus (e.g., "113I " or `204AT`)                                             |
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
