---
applyTo: "**"
---
# Evaluated Nuclear Structure Data File (ENSDF) Instructions for GitHub Copilot

## Your Role

You are an AI Agent specializing in the Evaluated Nuclear Structure Data File (ENSDF) 80-column fixed format. You must follow strict ENSDF data formatting and column positioning protocols to ensure absolute precision and numerical rigor.

---

## 1. ENSDF Comment Text Format Standards

### Superscripts and Subscripts

- `{+n}`: Superscript (e.g., `{+3}He` displays as ³He)
- `{-n}`: Subscript (e.g., `T{-1/2}` → T₁/₂, `CO{-2}` → CO₂)
- `{+-n}`: Negative superscript (e.g., `10{+-4}` displays as 10⁻⁴)

### Greek Letters and Mathematical Symbols

**Greek Lowercase:**

- `|a` → α (alpha), `|b` → β (beta), `|c` → η (eta), `|d` → δ (delta)
- `|e` → ε (varepsilon), `|f` → φ (phi), `|g` → γ (gamma), `|h` → χ (chi)
- `|i` → ι (iota), `|j` → ε (epsilon), `|k` → κ (kappa), `|l` → λ (lambda)
- `|m` → μ (mu), `|n` → ν (nu), `|p` → π (pi), `|q` → θ (theta)
- `|r` → ρ (rho), `|s` → σ (sigma), `|t` → τ (tau), `|u` → υ (upsilon)
- `|v` → ? (undefined), `|w` → ω (omega), `|x` → ξ (xi), `|y` → ψ (psi), `|z` → ζ (zeta)

**Greek Uppercase:**

- `|C` → H, `|D` → Δ (Delta), `|F` → Φ (Phi), `|G` → Γ (Gamma), `|H` → X
- `|J` → ~ (sim), `|L` → Λ (Lambda), `|P` → Π (Pi), `|Q` → Θ (Theta), `|R` → P
- `|S` → Σ (Sigma), `|U` → Υ (Upsilon), `|V` → ∇ (nabla)
- `|W` → Ω (Omega), `|X` → Ξ (Xi), `|Y` → Ψ (Psi)

**Mathematical Symbols:**

- `|*` → × (times), `|?` → ≈ (approximate/tilde), `|<` → ≤ (leq), `|>` → ≥ (geq)
- `|'` → ° (degree), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|=` → ≠ (not equal), `|@` → ∞ (infinity), `|^` → ↑ (up arrow)
- `|_` → ↓ (down arrow), `|&` → ≡ (equivalent), `|(` → ← (left arrow)
- `|)` → → (right arrow), `|.` → ∝ (proportional), `||` → | (vertical bar)
- `~#` → ⊗ (tensor product)

**Brackets and Parentheses:**

- `|0` → ( (left parenthesis), `|1` → ) (right parenthesis)
- `|2` → [ (left bracket), `|3` → ] (right bracket)
- `|4` → ⟨ (left angle bracket), `|5` → ⟩ (right angle bracket)

**Mathematical Operators:**

- `|7` → ∫ (integral), `|8` → ∏ (product), `|9` → ∑ (summation)

**Important Rules:**

- Use `|?` for approximate values (renders as ≈).
- Standalone `~` is prohibited for approximate values in ENSDF.

#### Common Examples

- `%(|e+|b{++})p` decay → %(ε+β⁺)p decay
- `{+208}Pb({+36}S,{+35}S)` reaction → ²⁰⁸Pb(³⁶S,³⁵S) reaction
- `{+32}S({+3}He,p|g){+34}Cl` reaction → ³²S(³He,pγ)³⁴Cl reaction
- `{+nat}Ni` means natural nickel
- `|s(E({+3}He),|q)` → σ(E(³He),θ)
- `Zn{-3}P{-2}` → Zn₃P₂
- `log {Ift}` → log <i>ft</i> (italicize "ft")

#### General Language Style

Use telegraphic phrasing in comment text.

### Nuclear Science References (NSR)

-   Each article in NSR has a unique 8-character key number (the "key number").
-   ENSDF uses this key number to reference published articles.

**Format:** `YYYYAA##` (e.g., `1970Br10`, `1974ClZK`).

**Capitalization rules:**
-   Author initials: First letter uppercase, rest lowercase (e.g., `Ba`, not `BA`; `Br`, not `BR`).
-   Letter suffixes: All uppercase (e.g., `ClZK`, not `Clzk`; `UmZZ`, not `Umzz`).

**Citation lists:** Use comma-separated values with spaces (e.g., `2021Vl03, 2015Vl01, 1974ClZK`).

---

## 2. ENSDF 80-Column Format Standards

### ENSDF NUCID Field Format Rules (Columns 1–5)

**CRITICAL: Exact Column Positioning Required**

**Two-digit mass number + single-letter element** (e.g., 35S, 51V, 12C):
- **Format:** ` MME ` (space, mass, element, space).
- **Column 1:** Space.
- **Columns 2–3:** Mass number (35, 51, 12).
- **Column 4:** One-letter element symbol (S, V, C).
- **Column 5:** Space.
- **Results:** ` 35S `, ` 51V `, ` 12C `.

**Two-digit mass number + two-letter element** (e.g., 35Cl, 74Ge, 32Si):
- **Format:** ` MMEl` (space, mass, element).
- **Column 1:** Space.
- **Columns 2–3:** Mass number (35, 74, 32).
- **Columns 4–5:** Two-letter element symbol (Cl, Ge, Si).
- **Results:** ` 35Cl`, ` 74Ge`, ` 32Si`.

**Three-digit mass number + single-letter element** (e.g., 127I, 232U):
- **Format:** `MMME ` (mass, element, space).
- **Columns 1–3:** Mass number (127, 232).
- **Column 4:** One-letter element symbol (I, W, U).
- **Column 5:** Space.
- **Results:** `127I `, `184W `.

**Three-digit mass number + two-letter element** (e.g., 120Sn, 208Pb, 252Cf):
- **Format:** `MMMEl` (mass, two-letter element).
- **Columns 1–3:** Mass number (120, 208, 252).
- **Columns 4–5:** Two-letter element symbol (Sn, Pb, Cf).
- **Results:** `120Sn`, `208Pb`, `252Cf`.

**CRITICAL NUCID RULES:**
- Column positioning is **EXACT**; being one column off will break the ENSDF parser.
- Element symbols are case-sensitive and must follow the official ENSDF style (e.g., antimony is `SB`, not `Sb`).
- Spaces are mandatory where specified to maintain field boundaries.
- Mass numbers must be numeric only.

### Record Format Specifications

#### Energy Level Record (L-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q
 35P   L 3572.0    12 3/2+,5/2+        29 FS     14    2        0.8       4 A  ?
 35CL  L 1219      5  3/2+             0.39 PS   8     2        0.43      15A  S
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35P " or " 35Cl"). |
| CONT | 6 | Continuation label. |
| Space | 7 | Must be blank. |
| TYPE | 8 | "L" (Level). |
| Space | 9 | Must be blank. |
| E | 10–19 | Level energy. |
| DE | 20–21 | Energy uncertainty. |
| Space | 22 | Readability space. |
| J | 23–39 | Spin-parity. |
| T | 40–49 | Half-life with units (e.g., MEV, FS, PS, S, H, D). |
| DT | 50–55 | Half-life uncertainty. |
| L | 56–64 | Angular momentum transfer. |
| S | 65–74 | Spectroscopic strength. |
| DS | 75–76 | Uncertainty in S. |
| C | 77 | Comment flag. |
| MS | 78–79 | Metastable state (isomer), denoted by 'M '. |
| Q | 80 | '?' for uncertain/questionable; 'S' for assumed but not observed. |


For multiple J-π values separated by commas, no spaces after commas.

**CRITICAL: Comment Line Association**
- `cL` comment lines apply **only** to the immediately preceding L-record.
- Do not modify L-record data based on comments for other levels.
- Each L-record with or without a following `cL` line is an independent record.

#### Gamma Transition Record (G-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q
 35P   G 1572.0    10 70.0   24 M1+E2    -1.23   25    0.090  20 71.0     23A  S
 35Si  G 2572.0    5  5.0    2  E2       +2.1          0.05   5  5.1      6 B  ?
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35P " or " 35Cl") |
| CONT | 6 | Continuation label |
| SPACE | 7 | Must be blank |
| TYPE | 8 | "G" |
| SPACE | 9 | Must be blank |
| E | 10–19 | Gamma energy |
| DE | 20–21 | Energy uncertainty |
| SPACE | 22 | Readability space |
| RI | 23–29 | Relative photon intensity (starts at col 23) |
| DRI | 30–31 | Uncertainty in RI (including GT, LT markers) |
| SPACE | 32 | Readability space |
| M | 33–41 | Multipolarity |
| MR | 42–49 | Mixing ratio |
| DMR | 50–55 | Uncertainty in MR |
| CC | 56–62 | Conversion coefficient |
| DCC | 63–64 | Uncertainty in CC |
| TI | 65–74 | Total transition intensity |
| DTI | 75–76 | Uncertainty in TI |
| C | 77 | **Comment flag** (A-Z, a-z, *, &, @) - See G-Record Flag Rules below |
| SPACE | 78–79 | Must be blank |
| Q | 80 | **Additional indicator** (space, ?, S) - See G-Record Indicator Rules below |

### Critical ENSDF Formatting Rules

#### ENSDF Structural Relationships

**Level Blocks or Level Units**

1. Each L-record starts a new level block (physical level).
2. All G-records immediately following an L-record belong to that level block.
3. Any G-records that appear before the next L-record attach to the previous level, never to the next level.
4. A level with no gamma rays consists of a single L-record with no following G-records.
5. Preserve strict L→G grouping; ENSDF parsers depend on it.

**Comment Line Scope and Order**

- **cL lines:** Apply only to the immediately preceding L-record and are an optional part of that L-record.
- **cL, 2cL, 3cL lines:** Form a unified comment block for that L-record.
- When multiple L-comment identifiers are present, order them as follows: `E$ → J$ → T$ → S$ → general` (no identifier).
- **cG lines:** Apply only to the immediately preceding G-record and are an optional part of that G-record.
- **cG, 2cG, 3cG lines:** Form a unified comment block for that G-record.
- When multiple G-comment identifiers are present, order them as follows: `E$ → RI$ → M$ → MR$ → other identifiers`.

**Continuation Records and Comments (Column 6)**

- Column 6 contains the continuation marker: blank for the first record and alphanumeric for continuation records.
- Common continuation records include `2 L` and `F L` for L-records, and `2 G` and `B G` for G-records.
- Common continuation comments include `2cL` and `3cL` for L-comment lines, and `2cG` and `3cG` for G-comment lines.
- Continuation records must remain attached to, and apply only to, the immediately preceding record type (L or G).
- Continuation comments must remain attached to the immediately preceding comment line.
- `2cL` must follow `cL`, and `3cL` must follow `2cL`, etc.
- `2cG` must follow `cG`, and `3cG` must follow `2cG`, etc.
- Continuation records have their own text-format standards. Do not use comment text format in continuation records. Example: `35CA2 L %EC+%B+=100$%ECP=95.8 3$%EC2P=4.2 3`.
- Less common: FLAG markers (for example, `FLAG=A`) are placed in continuation records following the record (L or G) that they describe.

#### Left-Justification Requirement

**MANDATORY:** All values and uncertainties in all fields MUST be left-justified (NEVER right-justified or centered).

-   **Applies to:** energies, intensities, half-lives, spin-parity, uncertainties (DE, DRI, DT, DMR, DCC, DTI, DS), special markers (GT, LT), and all other field content.
-   **Formatting:** Values start at the leftmost column of the field, padded with trailing spaces to fill field width.

#### Energy Ordering Requirement
**Requirement:**

-   L-records and G-records MUST be in ascending energy order.
-   **Consequence:** Violations break automated ENSDF parsers and database ingestion.
-   **Common error:** Inserting new levels or gammas without reordering by energy.

#### G-Record Flag Rules

**Column 77 (C Field, Comment Flag):**
-   `A-Z`, `a-z`: Any single letter used to refer to a specific comment record (cannot be a number).
-   `*` (asterisk): Denotes a multiply-placed gamma ray.
-   `&` (ampersand): Denotes a multiply-placed transition with intensity not divided.
-   `@` (at symbol): Denotes a multiply-placed transition with intensity suitably divided.
Note: Multiple identical gamma energies appearing in multiple level blocks should be flagged with either `*`, `&`, or `@`.
-   `Space`: No comment flag.
-   **FORBIDDEN:** Question mark (`?`) is NOT allowed in column 77.

**Column 80 (Q Field, Additional Indicator):**
-   `Space`: Normal, well-established gamma transition.
-   `?`: Denotes uncertain placement of the transition in the level scheme.
-   `S`: Denotes expected or assumed, but as yet unobserved, gamma transition.
-   **CRITICAL:** Only space, `?`, or `S` allowed in column 80.

**Critical Note:** ENSDF files require exact positioning. One column off equals data rejection.

#### Delayed Proton Emission Record (DP-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  DP EP       DE IP     DI EI                                              
 35CL  DP 501      10 3.5    12 9022                                            
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35Cl" or " 35P ") |
| CONT | 6 | Continuation label (blank) |
| SPACE | 7 | Must be blank |
| D | 8 | "D" for delayed particle |
| P | 9 | "P" for proton |
| SPACE | 10 | Readability space |
| EP | 11–19 | Proton energy in keV |
| DE | 20–21 | Energy uncertainty |
| SPACE | 22 | Readability space |
| IP | 23–29 | Proton intensity in percent |
| DIP | 30–31 | Uncertainty in IP |
| SPACE | 32 | Readability space |
| EI | 33–39 | Energy of emitting level in keV |

**Critical DP Format Rules:**
-   Readable spaces at columns 10, 22, and 32 for human readability.
-   All field positioning follows standard ENSDF left-justification rules.

#### Beta Minus Decay Record (B-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  B EEEE.E    DE IB     DI           LOGFT  DFT                        CUNQ
 35P   B 1572.0    1  100.0  4            5.23   12                         C1U 
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35P " or " 35Cl") |
| CONT | 6 | Continuation label |
| SPACE | 7 | Must be blank |
| TYPE | 8 | "B" for beta minus |
| SPACE | 9 | Must be blank |
| E | 10–19 | Endpoint energy of β⁻ in keV (given only if measured) |
| DE | 20–21 | Energy uncertainty |
| SPACE | 22 | Readability space |
| IB | 23–29 | Intensity of β⁻-decay branch |
| DIB | 30–31 | Uncertainty in IB |
| SPACE | 32–41 | Must be blank |
| SPACE | 42 | Readability space |
| LOGFT | 43–49 | The log ft for the β⁻ transition |
| DFT | 50–55 | Uncertainty in LOGFT |
| SPACE | 56–76 | Must be blank |
| C | 77 | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78–79 | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | '?' denotes uncertain or questionable beta minus decay |

**Critical B-Record Rules:**
-   Must follow LEVEL record for the level which is fed by the beta minus decay.
-   E field given only if measured (endpoint energy of beta minus transition).
-   IB intensity in same units as other intensity fields in file.
-   LOGFT for uniqueness classification (col 78-79).
-   Blank signifies allowed transition for forbiddenness field.

#### Electron Capture and Beta Plus Decay Record (E-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
 35XX  E EEEE.E    DE IB     DI IE     DI LOGFT  DFT            TI        DICUNQ
 35CL  E 1750.0    5  65.0   8  35.0   5  4.85   15             100.0     8 C1US
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35Cl" or " 35P ") |
| CONT | 6 | Continuation label |
| SPACE | 7 | Must be blank |
| TYPE | 8 | "E" for electron capture |
| SPACE | 9 | Must be blank |
| E | 10–19 | Energy for electron capture to level (if measured or deduced) |
| DE | 20–21 | Uncertainty in E |
| SPACE | 22 | Readability space |
| IB | 23–29 | Intensity of β⁺-decay branch |
| DIB | 30–31 | Uncertainty in IB |
| IE | 32–39 | Intensity of electron capture branch |
| DIE | 40–41 | Uncertainty in IE |
| SPACE | 42 | Readability space |
| LOGFT | 43–49 | The log ft for (ε + β⁺) transition |
| DFT | 50–55 | Uncertainty in LOGFT |
| SPACE | 56–64 | Must be blank |
| TI | 65–74 | Total (ε + β⁺) decay intensity |
| DTI | 75–76 | Uncertainty in TI |
| C | 77 | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78–79 | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | '?' = uncertain branch, 'S' = expected or assumed transition |

**Critical E-Record Rules:**
-   Must follow LEVEL record for the level being populated in the decay.
-   IE, IB and TI must be in same units.
-   TI = IE + IB for total decay intensity to the level.
-   Forbiddenness classification in columns 78-79 ('1U', '2U' for first-, second-unique forbidden).

#### Alpha Decay Record (A-Record)

```text
Example:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
235XX  A EEEE.E    DE IA     DI HF     DHF                                  C  Q
204AT  A 6632      6  100    5  1.5    3                                    C  ?
```

| Field | Columns | Description |
| :--- | :--- | :--- |
| NUCID | 1–5 | Nucleus (e.g., " 35P " or "204AT") |
| CONT | 6 | Continuation label |
| SPACE | 7 | Must be blank |
| TYPE | 8 | "A" for alpha decay |
| SPACE | 9 | Must be blank |
| E | 10–19 | Alpha energy in keV |
| DE | 20–21 | Standard uncertainty in E |
| SPACE | 22 | Readability space |
| IA | 23–29 | Intensity of α-decay branch in percent of the total α decay |
| DIA | 30–31 | Standard uncertainty in IA |
| SPACE | 32 | Readability space |
| HF | 33–39 | Hindrance factor for α decay |
| DHF | 40–41 | Standard uncertainty in HF |
| SPACE | 42–76 | Must be blank |
| C | 77 | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| SPACE | 78–79 | Must be blank |
| Q | 80 | '?' = uncertain or questionable α branch, 'S' = expected or predicted α branch |

**Critical A-Record Rules:**
-   Must follow the daughter LEVEL record for the level being populated in the α decay.


### XREF Notation Rules

Only in the Adopted Datasets: XREF (cross-reference) entries immediately following an L-record indicate which datasets observe this level.

| Notation | Meaning | Example |
| :--- | :--- | :--- |
| Plain letter | Dataset level energies match the Adopted level within uncertainties. | `XREF=FH` — Datasets F and H report this level with energies consistent with the Adopted value. |
| Letter(energy) | Dataset reports an energy outside the uncertainty range but still matches the same physical level. | `XREF=H(4865)` — Dataset H reports a level at 4866±3 keV (outside Adopted 4860±2). |
| Letter(*) | Ambiguous matching; dataset level may correspond to two or more Adopted levels. | `XREF=I(*)` — The level from dataset I has ambiguous doublet/multiplet matching. |
| Letter(?) | Questionable or uncertain match. | `XREF=J(?)` — Dataset J reports a questionable level that possibly matches the Adopted level. |

---

## 3. ENSDF Uncertainty Notation Rules

### General Rules

**CRITICAL:** Uncertainties in data record fields and comment lines use DIFFERENT formats, but both follow an "uncertainty-in-last-digits" notation. Ensure that the number of decimal places in the main value exactly matches the decimal place represented by the final digit of the uncertainty.

- Physics publications typically allow 1 or 2 digits for uncertainties.
- The uncertainty applies to the last significant digit of the value.
- Rounding threshold for uncertainty: 4-up, 3-down.
- One significant figure (leading 2 digits of uncertainty 35–99) → 1-digit uncertainties, e.g., 1.2333±0.3680 → 1.2(4).
- Two significant figures (leading 2 digits of uncertainty 10–34) → 2-digit uncertainties, e.g., 1.2333±0.3220 → 1.23(32).
- Special case: for half-lives or lifetimes, two significant figures with leading 2 digits of uncertainty 35–99 are allowed.

**Examples by Decimal Places:**

| Value Decimals | Field Notation | Comment Notation | Meaning (± format) |
| :--- | :--- | :--- | :--- |
| 0 decimals | `1234  5 ` | `1234 {I5}` | 1234 ± 5 |
| 0 decimals | `1234  26` | `1234 {I26}` | 1234 ± 26 |
| 1 decimal | `12.3  6 ` | `12.3 {I6}` | 12.3 ± 0.6 |
| 1 decimal | `3.6  11 ` | `3.6 {I11}` | 3.6 ± 1.1 |
| 2 decimals | `1.23  7` | `1.23 {I7}` | 1.23 ± 0.07 |
| 2 decimals | `1.23  21` | `1.23 {I21}` | 1.23 ± 0.21 |
| 4 decimals | `0.0060  6` | `0.0060 {I6}` | 0.0060 ± 0.0006 |
| 4 decimals | `0.0060  24` | `0.0060 {I24}` | 0.0060 ± 0.0024 |

### Uncertainty Format in Data Record Fields

#### General Format

Format: Plain integers only (NO `{I}` notation, NO parentheses).

**Examples:**
- Energy: `1572.0` with uncertainty `12` in DE field means 1572.0(12).
- RI: `70.0` with uncertainty `24` in DRI field means 70.0(24).
- T1/2: `2.29 PS` with uncertainty `14` in DT field means 2.29(14) PS.

#### Standard 2-Column Uncertainty Fields (DE, DRI, DIP, DCC, DTI, DS)

- **Field:** 1–2 digits with space padding.
    - Single digit: `"5 "` (digit + space).
    - Double digits: `"15"` (two digits).
    - Limit markers: `"GT"`, `"LT"` (two letters).


#### Extended 6-Column Uncertainty Fields (DT, DMR)

- **Field** (cols 50–55): 6 characters, left-justified, with space padding if fewer than 6 characters.
    - Symmetric: `"14    "` (1 or 2 digits + 5 or 4 spaces).
    - Asymmetric: `"+3-4  "` (2 spaces), `"+19-8 "` (1 space), `"+13-28"` (no spaces).
    - Limit markers: `"GT    "`, `"LT    "` (two letters + 4 spaces).
- For source data using the Rose and Brink (1967) sign convention, reverse the sign of the mixing ratio value before entering it into ENSDF. Reverse the asymmetric uncertainty order at the same time so the ENSDF value keeps the correct upper and lower bounds. Example: -0.27$_{-0.04}^{+0.03}$ becomes +0.27$_{+0.04}^{-0.03}$ in ENSDF.


**Critical Formatting Rules:**
- Single digits in 2-column fields: MUST be padded with trailing space.
- Double digits in 2-column fields: Fill both columns completely.
- Asymmetric uncertainties: Use +X-Y format in 6-character fields (DT, DMR).
- **FORBIDDEN:** `123` is not allowed in either 2-column fields (corrupts adjacent data) or in 6-column fields.


#### Scientific Notation Format

For intensities and other values in scientific notation:
- **Standard format:** `(5.6±1.0)×10^-4` becomes `5.6E-4 10` in ENSDF.
- **Value field:** Use `E-n` notation (e.g., `5.6E-4`).
- **Uncertainty field:** Use digits representing the last significant digit (e.g., `10` for ±1.0 if the value has one decimal place).
- **Examples:**
    - `(1.1±0.3)×10^-6` → Value: `1.1E-6`, Uncertainty: `3`.
    - `(76±20)×10^-6` → Value: `76E-6`, Uncertainty: `20`.
    - `(3.3±1.2)×10^-4` → Value: `3.3E-4`, Uncertainty: `12`.
- **NEVER use:** `×10^-n` notation directly in ENSDF records.
- **ALWAYS use:** `E-n` notation for the value with a separate uncertainty field.

#### GT and LT Markers in Uncertainty Fields

- **LT** = "Less Than" (e.g., `<1.6 ps` becomes `1.6 PS    LT` in T and DT fields).
- **GT** = "Greater Than" (e.g., `>5.2 fs` becomes `5.2 FS   GT` in T and DT fields).
- **Format:** Place the value in the main field and the GT/LT marker in the uncertainty field.
- **Examples for RI and DRI:**
    - `<1.6` → RI=`1.6    ` (cols 23–29), DRI=`LT` (cols 30–31).
    - `>5.2` → RI=`5.2    ` (cols 23–29), DRI=`GT` (cols 30–31).

### Uncertainty Format in Comment Lines

#### General Format

Format: Use `{In}` or `{I+n-m}` notation with braces.

**CRITICAL:** n must be INTEGER ONLY (NEVER decimals like `{I0.1}` or `{I1.1}`).

- **Symmetric:** `{In}` (e.g., `{I7}`, `{I11}`) without plus/minus signs.
- **Asymmetric:** `{I+n-m}` (e.g., `{I+10-11}`, `{I+7-9}`) with plus/minus signs.

#### Scientific Notation Format

In comment lines, scientific notation uses `{In}` for uncertainties:

- **Example 1:** `(5.6±1.0)×10^-4` becomes `5.6|*10{+-4} {I10}` in comments.
    - **Value:** `5.6E-4`
    - **Uncertainty:** `{I10}` (±1.0 in last digit).
- **Example 2:** `(1.1±0.3)×10^6` becomes `1.1|*10{+6} {I3}` in comments.
    - **Value:** `1.1E6`
    - **Uncertainty:** `{I3}` (±0.3 in last digit).

#### Uncertainty Notation with Units

Units are placed after the value before the uncertainty:

```text
 35CL  cL $|w|g=3.6 eV {I11} (1972Hu10)
 34S   cL $|t=54 fs {I+18-11} (1980Be15)
```


**Examples in Context:**
- Data record: ` 35P   L 1572.0    12 3/2+             2.29 PS   14` (uncertainties are plain numbers).
- Comment line: ` 35CL  cL $|w|g=3.6 eV {I11} (1972Hu10)` (uncertainty uses `{I11}` notation).

---

## 4. ENSDF File Editing Workflow

### File Protection Rules

-   **NEVER** edit `.old` files (reference files from previous evaluation rounds).
-   **NEVER** modify first/last line indentation or spacing in `.ens` files.
-   **NEVER** modify XREF lists (XREF entries with pattern `NUCID X` have their own specific formatting rules).

### Debugging Technique

**CRITICAL 80-Column Debugging Technique**:
When dealing with ENSDF alignment issues, ALWAYS use the visual ruler method:

```python
python -c "
header='[paste actual header line here]'
print('ENSDF 80-Column Ruler:')
print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')  
print('Header:', header)
print('Length:', len(header))
"
```

**Process**:
1.  Display 80-char ruler.
2.  Extract L/G/E/B records.
3.  Validate against ENSDF Manual.
4.  Report issues.

### Mandatory Edit-Validate-Repeat Workflow

**CRITICAL: THE MOST IMPORTANT RULE**

**The Sacred Workflow** (MUST Follow for Every Single Edit):
1.  **EDIT** → Make ONE precise change to ONE field.
2.  **VALIDATE** → Run ruler on that exact line: `python .github/scripts/ensdf_1line_ruler.py --line "your 80-char line"`.
3.  **CONFIRM** → Verify exit code 0 and check ruler output.
4.  **REPEAT** → Move to next edit only after confirmation.

**Forbidden Behaviors:**
-   **NEVER** edit multiple lines without validating each one.
-   **NEVER** make multiple edits then validate at the end.
-   **NEVER** assume an edit worked without checking.
-   **NEVER** skip validation "just this once".

### Validation Tools and When to Use Them

#### Before Any Edit

1.  Run `python .github/scripts/column_calibrate.py "filename.ens"` (MANDATORY).
    -   Validates L-field positioning (column 56), S-field left-justification (columns 65-74).
    -   Verifies comment flags at column 77.
    -   Reports data-record line-length issues (L/G/E/B/DP records).
2.  Run `python .github/scripts/check_gamma_ordering.py "filename.ens"` (MANDATORY).
    -   Verifies ascending energy order for L-records and G-records.
3.  Manual verification: `column_calibrate.py` does NOT check DP, B, or E record formatting.
4.  Read current file state (never assume file structure).
5.  Identify target line uniquely (must have 5+ lines of unique context).
6.  Single field modification only (never edit multiple fields at once).

#### During Each Edit

Run ruler for each changed line: `python .github/scripts/ensdf_1line_ruler.py --line "your 80-char line"`
-   MANDATORY for every line you edit.
-   Immediate visual ruler, length, and field validation.
-   Must verify exit code 0 before proceeding to next edit.

#### After All Edits

Repeat validation sequence (steps 1-2 from "Before Any Edit" section).

### ENSDF 1-Line Ruler Tool

**Usage Modes:**
-   **Single line check:** `python .github/scripts/ensdf_1line_ruler.py --line "your exact 80-char line"`
    -   Quick ruler display, length check, immediate validation feedback.
    -   USE THIS for every line you edit (essential AI workflow step).
-   **File scan:** `python .github/scripts/ensdf_1line_ruler.py --file path/to/file.ens [--show-only-wrong]`
    -   Checks all data records (L, G, E, B, DP records); exit code 1 if any errors found.
    -   Use `--show-only-wrong` to quickly identify problem lines only.

### Column Calibration Tool (column_calibrate.py)

Comprehensive ENSDF field validation and data-record line-length checking:
-   **Basic validation:** `python .github/scripts/column_calibrate.py "file.ens"`
    -   Prints 80-column ruler with field boundaries.
    -   Checks field positioning and reports line-length issues.
-   **Optional auto-fix:** `--fix` flag can pad/trim spaces to exactly 80-character line lengths.
    -   Use with extreme caution (does NOT fix field content or formatting errors).
    -   May surface new issues if misused (prefer manual corrections).
    -   Always re-validate after using `--fix` option.
-   **Exit codes:** 0 = all checks pass; 1 = errors found.
-   **Limitations:** DP, B, and E records require additional manual verification.

### Energy Ordering Tool (check_gamma_ordering.py)

Validates ascending energy order for L-records and G-records:
-   **Basic check:** `python .github/scripts/check_gamma_ordering.py "file.ens"`
-   **Multiple files:** `python .github/scripts/check_gamma_ordering.py "A35/K35/new/*.ens" --summary`
-   **Verbose output:** Add `--verbose` flag for detailed checking process.
-   **Exit codes:** 0 = correct ordering; 1 = ordering violations found.

### Output Interpretation Guidelines

**SUCCESS indicators:**
-   Exit code 0: Validation PASSED (safe to proceed).
-   "SUCCESS: All ENSDF field positions appear correct!"

**ERROR indicators:**
-   Exit code 1: Validation FAILED (MUST fix errors before proceeding).
-   "DATA RECORD LINE LENGTH ISSUES DETECTED": Lines not exactly 80 characters.
-   "ERROR: Field positioning errors found": Field alignment problems.

### Editing Methodology

1.  **ONE EDIT AT A TIME** (never batch multiple field changes).
2.  **PRECISE CONTEXT MATCHING** (use complete L-record + surrounding context).
3.  **FIELD-SPECIFIC REPLACEMENTS** (target only the specific field being changed).
4.  **IMMEDIATE VALIDATION** (check file structure after each edit).

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

**CRITICAL COLUMN RULE:** When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).



## 5. Data Extraction and Entry Quality Assurance

**CRITICAL REQUIREMENT:** For ALL numerical data extraction/entry tasks, you MUST execute BOTH quality assurance checks before claiming task completion: Bidirectional Positional Check and Random Spot Check.

### Mandatory Random Spot-Check Protocol

**NON-NEGOTIABLE REQUIREMENT:** After ANY large-scale data entry task, you MUST perform random spot-check validation before claiming completion. This is NOT optional.

#### Execution Requirements

-   **Minimum sample size:** 15% of total entries (absolute minimum: 10 samples).
-   **Selection method:** Random sampling (neither sequential nor cherry-picked).
-   **Evidence required:** Generate a verification script showing:
    -   Total entry count.
    -   Sample size calculation (e.g., "200 entries → 15% = 30 samples").
    -   Randomly selected entered data.
    -   Trace back to source data for each sample.
    -   Verification results (PASS/FAIL per sample).

#### Verification Checklist (100% Pass Rate Required)

-    Arithmetic accuracy (no calculation errors).
-    Values match source data exactly (character-for-character).
-    Uncertainties match source data exactly.
-    Mapping accuracy (correct ENSDF fields used).
-    Positional alignment (no off-by-one errors).

#### Procedures for Error Discovery

If any errors are found:
1.  **Stop immediately** and do not claim completion.
2.  Identify the root cause (systematic vs. isolated error).
3.  Analyze the error pattern across all entries.
4.  Correct all instances of the identified error type.
5.  Re-run automated validation (`column_calibrate.py` and `check_gamma_ordering.py`).
6.  Perform a new random spot-check with different samples.
7.  Repeat until a 100% pass rate is achieved.

#### Workflow Integration

-   Execute after automated validation passes (`column_calibrate.py` and `check_gamma_ordering.py`).
-   Execute after the Bidirectional Positional Check and Random Spot Check pass with 100% accuracy.
-   Execute before claiming "task completed successfully."
-   Document findings in the compliance checklist for user verification.

#### Zero-Tolerance Enforcement

-   Tasks are incomplete until the spot-check passes with zero errors.
-   No exceptions for "simple" or "small" data entry tasks.
-   Failure to execute constitutes failure to complete the assigned task.

---

## 6. Academic Standards

### Professional English Grammar

**Common corrections:**
-   **Spelling:** "other" (not "ohter"), "stopped" (not "stoped"), "using" (not "usign"), "coefficients" (not "coeffcients"), "deexciting" (not "deexiting"), "multipolarities" (not "multiporities"), "parentheses" (not "paretheses").
-   **Dittography:** Remove duplicated words (e.g., "the the").
-   **Hyphenation Rule:** [Number]-[Unit]-[Descriptor] [Noun]. Hyphenate compound adjectives occurring before a noun (e.g., "x-ray diffraction," "4-mm-long gas cell," "R-matrix theory"). Do not hyphenate when they are not adjectives before nouns (e.g., "emitted by x rays," "was 4 mm long").
-   **Consistency:** Always hyphenate "L-transfers" and "half-life."

---

## Document Structure

This document consists of six main sections:

1. **ENSDF Comment Text Format Standards:** Superscripts, subscripts, Greek letters, mathematical symbols, and NSR citation format.
2. **ENSDF 80-Column Format Standards:** NUCID field rules, L/G/B/E/A/DP record specifications, and critical formatting rules.
3. **ENSDF Uncertainty Notation:** Data record fields (plain numbers) and comment lines ({In} notation).
4. **ENSDF File Editing Workflow:** File protection, edit-validate-repeat workflow, validation tools, and editing methodology.
5. **Data Extraction and Data Entry Quality Assurance:** Trigger conditions, bidirectional positional checks, random spot-check validation, and error discovery procedures.
6. **Academic Standards:** Professional English grammar and text formatting conventions.
