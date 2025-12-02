---
applyTo: "**"
---
# Evaluated Nuclear Structure Data File (ENSDF) Instructions for GitHub Copilot

## Your Role
You are an agent specializing in Evaluated Nuclear Structure Data File (ENSDF) 80-column fixed format.
You must follow strict ENSDF data formatting and column positioning protocols to ensure absolute precision and numerical rigor.

---

## 1. ENSDF Text Format Standards

### Superscripts and Subscripts
- `{+n}` → superscript (e.g., `{+3}He` displays as ³He)
- `{-n}` → subscript (e.g., `T{-1/2}` → T₁/₂)
- `{+-n}` → negative superscript (e.g., `10{+-4}` displays as 10⁻⁴)

### Greek Letters and Mathematical Symbols
**Greek lowercase:**
- `|a` → α (alpha), `|b` → β (beta), `|c` → η (eta), `|d` → δ (delta)
- `|e` → ε (varepsilon), `|f` → φ (phi), `|g` → γ (gamma), `|h` → χ (chi)
- `|i` → ι (iota), `|j` → ε (epsilon), `|k` → κ (kappa), `|l` → λ (lambda)
- `|m` → μ (mu), `|n` → ν (nu), `|p` → π (pi), `|q` → θ (theta)
- `|r` → ρ (rho), `|s` → σ (sigma), `|t` → τ (tau), `|u` → υ (upsilon)
- `|v` → ? (undefined), `|w` → ω (omega), `|x` → ξ (xi), `|y` → ψ (psi), `|z` → ζ (zeta)

**Greek uppercase:**
- `|C` → H, `|D` → Δ (Delta), `|F` → Φ (Phi), `|G` → Γ (Gamma), `|H` → X
- `|J` → ~ (sim), `|L` → Λ (Lambda), `|P` → Π (Pi), `|Q` → Θ (Theta), `|R` → P
- `|S` → Σ (Sigma), `|U` → Υ (Upsilon), `|V` → ∇ (nabla)
- `|W` → Ω (Omega), `|X` → Ξ (Xi), `|Y` → Ψ (Psi)

**Mathematical symbols:**
- `|*` → × (times), `|?` → ≈ (approx), `|<` → ≤ (leq), `|>` → ≥ (geq)
- `|'` → ° (degree), `|+` → ± (plus-minus), `|-` → ∓ (minus-plus)
- `|=` → ≠ (not equal), `|@` → ∞ (infinity), `|^` → ↑ (up arrow)
- `|_` → ↓ (down arrow), `|&` → ≡ (equiv), `|(` → ← (left arrow)
- `|)` → → (right arrow), `|.` → ∝ (proportional), `||` → | (vertical bar)

**Bracket and parenthesis symbols:**
- `|0` → ( (left parenthesis), `|1` → ) (right parenthesis)
- `|2` → [ (left bracket), `|3` → ] (right bracket)
- `|4` → ⟨ (left angle), `|5` → ⟩ (right angle)

**Mathematical operators:**
- `|7` → ∫ (integral), `|8` → ∏ (product), `|9` → ∑ (summation)

**Important Rules:**
- For approximate values, use `|?` (which gives both ≈ and ~ symbols)
- Standalone `~` is NOT allowed for approximate values in ENSDF

#### Common Examples
- `%(|e+|b{++})p` → %(ε+β⁺)p
- `{+208}Pb({+36}S,{+35}S)` → ²⁰⁸Pb(³⁶S,³⁵S)
- `|s(E({+3}He),|q)` → σ(E(³He),θ)


---

## 2. ENSDF 80-Column Format Standards

### ENSDF NUCID Field Format Rules (Columns 1-5)

**CRITICAL: EXACT COLUMN POSITIONING REQUIRED**

**Two-digit mass number + One-letter element** (e.g., 35S, 51V, 12C):
- **Format**: ` MME ` (space, mass, element, space)
- **Column 1**: Space
- **Columns 2-3**: Mass number (35, 51, 12)
- **Column 4**: One-letter element symbol (S, V, C)
- **Column 5**: Space
- **Results**: ` 35S `, ` 51V `, ` 12C `

**Two-digit mass number + Two-letter element** (e.g., 35Cl, 74Ge, 32Si):
- **Format**: ` MMEl` (space, mass, element)
- **Column 1**: Space
- **Columns 2-3**: Mass number (35, 74, 32)
- **Columns 4-5**: Two-letter element symbol (Cl, Ge, Si)
- **Results**: ` 35Cl`, ` 74Ge`, ` 32Si`

**Three-digit mass number + One-letter element** (e.g., 127I, 252C):
- **Format**: `MMME ` (mass, element, space)
- **Columns 1-3**: Mass number (127, 252)
- **Column 4**: One-letter element symbol (I, W, U)
- **Column 5**: Space
- **Results**: `127I `, `184W `

**Three-digit mass number + Two-letter element** (e.g., 120Sn, 208Pb, 252Cf):
- **Format**: `MMMEl` (mass, two-letter element)
- **Columns 1-3**: Mass number (120, 208, 252)
- **Columns 4-5**: Two-letter element symbol (Sn, Pb, Cf)
- **Results**: `120Sn`, `208Pb`, `252Cf`

**CRITICAL NUCID Rules:**
- Column positioning is EXACT (one column off breaks ENSDF parsing)
- Element symbols follow periodic table (case sensitive: Cl not CL)
- Spaces are mandatory where specified to maintain field boundaries
- Mass numbers are numeric only (no leading zeros unless 3-digit)

### Record Format Specifications

#### L-Record Format (Energy Levels)
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:
 35XX  L EEEE.E    DE JP               T         DT    L        S         DSC  Q
Example:
 35P   L 3572.0    12 3/2+,5/2+        29 FS     14    2        0.8       4 A  ?
 35CL  L 1219      5  3/2+             0.39 PS   8     2        0.43      15A  S
```

| Field | Columns | Description |
|-------|---------|-------------|
| NUCID | 1-5 | Nucleus (e.g., " 35P " or " 35Cl") |
| CONT | 6 | Continuation label |
| BLANK | 7 | Must be blank |
| TYPE | 8 | "L" |
| BLANK | 9 | Must be blank |
| E | 10-19 | Level energy |
| DE | 20-21 | Energy uncertainty |
| SPACE | 22 | Readability space |
| J | 23-39 | Spin-parity (starts at col 23) - See J-π Assignment Confidence Notation rules |
| T | 40-49 | Half-life with units |
| DT | 50-55 | Half-life uncertainty |
| L | 56-64 | Angular momentum transfer |
| S | 65-74 | Spectroscopic strength |
| DS | 75-76 | Uncertainty in S |
| C | 77 | Comment flag |
| MS | 78-79 | Metastable state, i.e., isomer, denoted by 'M ' |
| Q | 80 | Blank or '?' denotes an uncertain or questionable level or 'S' denotes a level assumed but not observed, usually near neutron, proton, or alpha separation energy. |


**CRITICAL cL Comment Line Association Rule:**
- cL comment lines apply ONLY to the immediately preceding L-record
- NEVER modify L-record data based on comment lines for other L-records
- Each L-record without a following cL line is an independent assignment

#### G-Record Format (Gamma Transitions)
```
Columns:
12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format: 
 35XX  G EEEE.E    DE II.I   DI MUL      MR      DMR   CC     DC TI       DTC  Q
Example:
 35P   G 1572.0    10 70.0   24 M1+E2    -1.23   25    0.090  20 71.0     23A  S
 35Si  G 2572.0    5  5.0    2  E2       +2.1          0.05   5  5.1      2 B  ?
```

| Field | Columns | Description |
|-------|---------|-------------|
| NUCID | 1-5 | Nucleus (e.g., " 35P " or " 35Cl") |
| CONT | 6 | Continuation label |
| BLANK | 7 | Must be blank |
| TYPE | 8 | "G" |
| BLANK | 9 | Must be blank |
| E | 10-19 | Gamma energy |
| DE | 20-21 | Energy uncertainty |
| SPACE | 22 | Readability space |
| RI | 23-29 | Relative photon intensity (starts at col 23) |
| DRI | 30-31 | Uncertainty in RI (including GT, LT markers) |
| SPACE | 32 | Readability space |
| M | 33-41 | Multipolarity |
| MR | 42-49 | Mixing ratio |
| DMR | 50-55 | Uncertainty in MR |
| CC | 56-62 | Conversion coefficient |
| DCC | 63-64 | Uncertainty in CC |
| TI | 65-74 | Total transition intensity |
| DTI | 75-76 | Uncertainty in TI |
| C | 77 | **Comment flag** (A-Z, a-z, *, &, @) - See G-Record Flag Rules below |
| BLANK | 78-79 | Must be blank |
| Q | 80 | **Additional indicator** (space, ?, S) - See G-Record Indicator Rules below |


### Critical ENSDF Formatting Rules

#### ENSDF Structural Relationships

**Level Blocks:**
1. Each L-record starts a new level block (physical level)
2. All G-records immediately after an L-record belong to that level block
3. Any G-records before the next L-record attach to the previous level (never to the next)
4. A level with no gammas is a single L-record with no following G-records
5. Preserve strict L→G grouping; parsers depend on it

**Comment Line Scope and Order:**
- cL lines: Apply only to the immediately preceding L-record (they are part of that L-record)
  - Order when multiple: E$ → J$ → T$ → S$ → general (no identifier)
- cG lines: Apply only to the immediately preceding G-record (they are part of that G-record)
  - Order when multiple: E$ → RI$ → M$ → MR$ → other identifiers

#### Left-Justification Requirement

**MANDATORY:** All values and uncertainties in all fields MUST be left-justified (NEVER right-justified or centered).

- Applies to: energies, intensities, half-lives, spin-parity, uncertainties (DE, DRI, DT, DMR, DCC, DTI, DS), special markers (GT, LT), and all other field content
- Formatting: Values start at leftmost column of field, padded with trailing spaces to fill field width

#### Energy Ordering Requirement

- L-records and G-records MUST be in ascending energy order
- Consequence: Violations break automated ENSDF parsers and database ingestion
- Common error: Inserting new levels or gammas without reordering by energy

#### G-Record Flag Rules

**Column 77 (C Field, Comment Flag):**
- A-Z, a-z: Any single letter used to refer to a specific comment record (cannot be a number)
- * (asterisk): Denotes a multiply-placed gamma ray
- & (ampersand): Denotes a multiply-placed transition with intensity not divided
- @ (at symbol): Denotes a multiply-placed transition with intensity suitably divided
- Space: No comment flag
- FORBIDDEN: Question mark (?) is NOT allowed in column 77

**Column 80 (Q Field, Additional Indicator):**
- Space: Normal, well-established gamma transition
- ?: Denotes uncertain placement of the transition in the level scheme
- S: Denotes expected or assumed, but as yet unobserved, gamma transition
- CRITICAL: Only space, ?, or S allowed in column 80

**Critical Note:** ENSDF files are parsed by automated systems requiring exact positions. One column off equals data rejection.

#### DP-Record Format (Delayed Proton Emission)
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX   DP EP       DE IP     DIP EI
Example: 35CL   DP 501      10 3.5    12 9022
```

| Field | Columns | Description |
|-------|---------|-------------|
| NUCID | 1-5 | Nucleus (e.g., " 35Cl" or " 35P ") |
| CONT | 6 | Continuation label (blank) |
| BLANK | 7 | Must be blank |
| D | 8 | "D" for delayed particle |
| P | 9 | "P" for proton |
| BLANK | 10 | Readability space |
| EP | 11-19 | Proton energy in keV |
| DE | 20-21 | Energy uncertainty |
| BLANK | 22 | Readability space |
| IP | 23-29 | Proton intensity in percent |
| DIP | 30-31 | Uncertainty in IP |
| BLANK | 32 | Readability space |
| EI | 33-39 | Energy of emitting level in keV |

**Critical DP Format Rules:**
- Readable spaces at columns 10, 22, and 32 for human readability
- All field positioning follows standard ENSDF left-justification rules

#### B-Record Format (Beta Minus Decay)
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  B EEEE.E   DE  IB     DIB          LOGFT   DFT              C   UN  Q
Example: 35P   B 1572.0    1  100.0  4            5.23    12               C   1U   
```

| Field | Columns | Description |
|-------|---------|-------------|
| NUCID | 1-5 | Nucleus (e.g., " 35P " or " 35Cl") |
| CONT | 6 | Continuation label |
| BLANK | 7 | Must be blank |
| TYPE | 8 | "B" for beta minus |
| BLANK | 9 | Must be blank |
| E | 10-19 | Endpoint energy of β⁻ in keV (given only if measured) |
| DE | 20-21 | Energy uncertainty |
| IB | 22-29 | Intensity of β⁻-decay branch |
| DIB | 30-31 | Uncertainty in IB |
| BLANK | 32-41 | Must be blank |
| LOGFT | 42-49 | The log ft for the β⁻ transition |
| DFT | 50-55 | Uncertainty in LOGFT |
| BLANK | 56-76 | Must be blank |
| C | 77 | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78-79 | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | '?' denotes uncertain or questionable beta minus decay |

**Critical B-Record Rules:**
- Must follow LEVEL record for the level which is fed by the beta minus decay
- E field given only if measured (endpoint energy of beta minus transition)
- IB intensity in same units as other intensity fields in file
- LOGFT for uniqueness classification (col 78-79)
- Blank signifies allowed transition for forbiddenness field

#### E-Record Format (Electron Capture and Beta Plus Decay)
```
Columns: 12345678901234567890123456789012345678901234567890123456789012345678901234567890
Format:  35XX  E EEEE.E   DE  IB     DIB IE     DIE LOGFT   DFT    TI       DTI C UN  Q
Example: 35CL  E 1750.0    5  65.0   8   35.0   5   4.85    15     100.0    8   C 1U  S
```

| Field | Columns | Description |
|-------|---------|-------------|
| NUCID | 1-5 | Nucleus (e.g., " 35Cl" or " 35P ") |
| CONT | 6 | Continuation label |
| BLANK | 7 | Must be blank |
| TYPE | 8 | "E" for electron capture |
| BLANK | 9 | Must be blank |
| E | 10-19 | Energy for electron capture to level (if measured or deduced) |
| DE | 20-21 | Uncertainty in E |
| IB | 22-29 | Intensity of β⁺-decay branch |
| DIB | 30-31 | Uncertainty in IB |
| IE | 32-39 | Intensity of electron capture branch |
| DIE | 40-41 | Uncertainty in IE |
| LOGFT | 42-49 | The log ft for (ε + β⁺) transition |
| DFT | 50-55 | Uncertainty in LOGFT |
| BLANK | 56-64 | Must be blank |
| TI | 65-74 | Total (ε + β⁺) decay intensity |
| DTI | 75-76 | Uncertainty in TI |
| C | 77 | Comment flag ('C' denotes coincidence, '?' denotes probable coincidence) |
| UN | 78-79 | Forbiddenness classification ('1U', '2U' for unique forbidden, blank = allowed) |
| Q | 80 | '?' = uncertain branch, 'S' = expected or assumed transition |

**Critical E-Record Rules:**
- Must follow LEVEL record for the level being populated in the decay
- IE, IB and TI must be in same units (see NORMALIZATION record)
- Energy field given only if measured or deduced from measured beta plus end-point energy
- TI = IE + IB for total decay intensity to the level
- Forbiddenness classification in columns 78-79 ('1U', '2U' for first-, second-unique forbidden)
- Additional indicator in column 80 for uncertain ('?') or assumed ('S') transitions

#### LOG FT Format Rules (Critical for B and E Records)

**MANDATORY LOG FT FORMATTING IN ENSDF**

Records (LOGFT field, columns 42-49):
- **Format**: Decimal notation (e.g., `4.85`, `6.2`)
- **Precision**: 1-2 decimal places typically
- **Uncertainty**: DFT field (columns 50-55) contains uncertainty in last digits
- **Special notations**:
  - Greater than: `>8.5` (blank DFT)
  - Less than: `<3.2` (blank DFT)
  - Approximate: `|?4.8`
  - Systematic: `4.85 SY` (SY in DFT)

**Comments:**
- **Use italic notation**: `log {Ift}` (NOT `log ft`)
- **Examples**: "Deduced levels, J, π, decay branching ratios, log {Ift}, and partial decay widths"

**Examples:**
```
LOGFT     DFT
4.85      15     → log ft = 4.85(15)
>8.5             → log ft > 8.5
|?5.1            → log ft ≈ 5.1
```

---

## 3. ENSDF Uncertainty Standards

### Uncertainty Format in Data Record Fields

#### Standard 2-Column Uncertainty Fields (Limited to 1-2 Digits Maximum)

- DE field (cols 20-21): 1-2 digits with space padding
  - Single digit: `"5 "` (digit + space), Double digits: `"15"` (two digits)
- DRI field (cols 30-31): 1-2 digits OR special markers
  - Single digit: `"7 "` (digit + space), Double digits: `"24"`, Markers: `"GT"`, `"LT"`
- DCC field (cols 63-64): 1-2 digits with space padding
  - Single digit: `"3 "` (digit + space), Double digits: `"18"` (two digits)
- DTI field (cols 75-76): 1-2 digits with space padding
  - Single digit: `"9 "` (digit + space), Double digits: `"42"` (two digits)
- DS field (cols 75-76): 1-2 digits with space padding
  - Single digit: `"2 "` (digit + space), Double digits: `"35"` (two digits)

#### Extended Uncertainty Fields (Up to 6 Characters for Asymmetric Uncertainties)

- DT field (cols 50-55): Half-life uncertainties, supports asymmetric format
  - Symmetric: `"14    "` (digits + spaces), Asymmetric: `"+3-4  "`, `"+19-3 "`, `"+13-28"`
- DMR field (cols 50-55): Mixing ratio uncertainties, supports asymmetric format
  - Symmetric: `"25    "` (value + spaces), Asymmetric: `"+5-3 "`, `"+21-18"`

**Critical Formatting Rules:**
- Single digits in 2-column fields: MUST be padded with trailing space
- Double digits in 2-column fields: Fill both columns completely
- Asymmetric uncertainties: Use +X-Y format in 6-character fields (DT, DMR)
- FORBIDDEN: "123" in 2-column fields (corrupts adjacent data)

#### Scientific Notation Format

For intensities and other values in scientific notation:
- Standard format: `(5.6±1.0)×10^-4` becomes `5.6E-4 10` in ENSDF
- Value field: `5.6E-4` (scientific notation with E)
- Uncertainty field: `10` (represents ±1.0 in the last significant digit)
- Examples:
  - `(1.1±0.3)×10^-6` → Value: `1.1E-6`, Uncertainty: `3`
  - `(76±20)×10^-6` → Value: `76E-6`, Uncertainty: `20`
  - `(3.3±1.2)×10^-4` → Value: `3.3E-4`, Uncertainty: `12`
- NEVER use: `×10^-n` notation directly in ENSDF records
- ALWAYS use: `E-n` notation for the value, separate uncertainty field

#### GT and LT Markers in Uncertainty Fields

- LT = "Less Than" (e.g., `<1.6` becomes `1.6    LT` in DRI field)
- GT = "Greater Than" (e.g., `>5.2` becomes `5.2    GT` in DRI field)
- Format: Value in main field, GT/LT marker in uncertainty field
- Examples: 
  - `<1.6` → RI=`1.6    ` (cols 23-29), DRI=`LT` (cols 30-31)
  - `>5.2` → RI=`5.2    ` (cols 23-29), DRI=`GT` (cols 30-31)

### Uncertainty Format in Comment Lines

**CRITICAL: Uncertainties in Data Record Fields and in Comment Lines - Two Different Formats - Do Not Confuse**

#### In Data Record Fields (L, G, E, B, DP Records)

Format: Plain numbers only (NO {I} notation, NO braces)

Examples:
- Energy: `1572.0` with uncertainty `12` in DE field means 1572.0(12)
- RI: `70.0` with uncertainty `24` in DRI field means 70.0(24)
- T1/2: `2.29 PS` with uncertainty `14` in DT field means 2.29(14) PS

#### In Comment Lines (cL, cG, General Comments)

Format: Use {In} or {I+n-m} notation with braces

**CRITICAL:** n must be INTEGER ONLY (NEVER decimals like {I0.1} or {I1.1})

- Symmetric: `{In}` (e.g., `{I7}`, `{I11}`) without plus/minus signs
- Asymmetric: `{I+n-m}` (e.g., `{I+10-11}`, `{I+7-9}`) with plus/minus signs
- FORBIDDEN: `{I+n}` for symmetric uncertainties (incorrect format)

**Comment Line {In} Examples by Decimal Places:**

| Value Decimals | Comment Notation | Meaning (± format) |
|----------------|------------------|-------------------|
| 0 decimals | `1234 {I5}` | 1234 ± 5 |
| 0 decimals | `1234 {I26}` | 1234 ± 26 |
| 1 decimal | `12.3 {I6}` | 12.3 ± 0.6 |
| 1 decimal | `3.6 {I11}` | 3.6 ± 1.1 |
| 2 decimals | `1.23 {I7}` | 1.23 ± 0.07 |
| 2 decimals | `1.23 {I21}` | 1.23 ± 0.21 |

**Critical Rules for {In} in Comments:**
- `{In}` applies to the last significant digit of the value
- For 1 decimal: `{I11}` means ±11 in last digit = ±1.1
- For 2 decimals: `{I21}` means ±21 in last two digits = ±0.21
- FORBIDDEN: `{I0.1}`, `{I1.1}`, `{I2.7}` (decimals violate ENSDF rules)

**Examples in Context:**
- Data record: ` 35P   L 1572.0    12 3/2+             2.29 PS   14` (uncertainties are plain numbers)
- Comment line: ` 35CL  cL $|w|g=3.6 eV {I11} (1972Hu10)` (uncertainty uses {I11} notation)

### Nuclear Science References (NSR)

Each article in NSR has a unique 8-character key number ("key number") used to reference articles in ENSDF and other nuclear databases.

---

## 4. ENSDF File Editing Workflow

### File Protection Rules

- NEVER edit `.old` files (reference files from previous evaluation rounds)
- NEVER modify first/last line indentation or spacing in .ens files
- NEVER modify XREF lists (XREF entries with pattern `NUCID X` have their own specific formatting rules)


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

**Process**: Display 80-char ruler → Extract L/G/E/B records → Validate against ENSDF Manual → Report issues

### Mandatory Edit-Validate-Repeat Workflow

**CRITICAL: THE MOST IMPORTANT RULE**

The Sacred Workflow (MUST Follow for Every Single Edit):
```
1. EDIT   → Make ONE precise change to ONE field
2. VALIDATE → Run ruler on that exact line: python .github/ensdf_1line_ruler.py --line "your 80-char line"
3. CONFIRM → Verify exit code 0, check ruler output
4. REPEAT → Move to next edit only after confirmation
```

Forbidden Behaviors:
- NEVER edit multiple lines without validating each one
- NEVER make multiple edits then validate at the end
- NEVER assume an edit worked without checking
- NEVER skip validation "just this once"

### Validation Tools and When to Use Them

#### Before Any Edit

1. Run `python .github/column_calibrate.py "filename.ens"` (MANDATORY)
   - Validates L-field positioning (column 56), S-field left-justification (columns 65-74)
   - Verifies comment flags at column 77
   - Reports data-record line-length issues (L/G/E/B/DP records)
   
2. Run `python .github/check_gamma_ordering.py "filename.ens"` (MANDATORY)
   - Verifies ascending energy order for L-records and G-records
   
3. Manual verification: column_calibrate.py does NOT check DP, B, or E record formatting
4. Read current file state (never assume file structure)
5. Identify target line uniquely (must have 5+ lines of unique context)
6. Single field modification only (never edit multiple fields at once)

#### During Each Edit

Run ruler for each changed line: `python .github/ensdf_1line_ruler.py --line "your 80-char line"`
- MANDATORY for every line you edit
- Immediate visual ruler, length, and field validation
- Must verify exit code 0 before proceeding to next edit

#### After All Edits

Repeat validation sequence (steps 1-2 from Before Any Edit section)

### ENSDF 1-Line Ruler Tool

Usage Modes:
- Single line check: `python .github/ensdf_1line_ruler.py --line "your exact 80-char line"`  
  - Quick ruler display, length check, immediate validation feedback
  - USE THIS for every line you edit (essential AI workflow step)
  
- File scan: `python .github/ensdf_1line_ruler.py --file path/to/file.ens [--show-only-wrong]`  
  - Checks all data records (L, G, E, B, DP records); exit code 1 if any errors found
  - Use `--show-only-wrong` to quickly identify problem lines only

### Column Calibration Tool (column_calibrate.py)

Comprehensive ENSDF field validation and data-record line-length checking:
- Basic validation: `python .github/column_calibrate.py "file.ens"`
  - Prints 80-column ruler with field boundaries
  - Checks field positioning and reports line-length issues
  
- Optional auto-fix: `--fix` flag can pad/trim spaces to exactly 80-character line lengths
  - Use with extreme caution (does NOT fix field content or formatting errors)
  - May surface new issues if misused (prefer manual corrections)
  - Always re-validate after using --fix option
  
- Exit codes: 0 = all checks pass; 1 = errors found
- Limitations: DP, B, and E records require additional manual verification

### Energy Ordering Tool (check_gamma_ordering.py)

Validates ascending energy order for L-records and G-records:
- Basic check: `python .github/check_gamma_ordering.py "file.ens"`
- Multiple files: `python .github/check_gamma_ordering.py "A35/K35/new/*.ens" --summary`
- Verbose output: Add `--verbose` flag for detailed checking process
- Exit codes: 0 = correct ordering; 1 = ordering violations found

### Output Interpretation Guidelines

SUCCESS indicators:
- Exit code 0: Validation PASSED (safe to proceed)
- "SUCCESS: All ENSDF field positions appear correct!"

ERROR indicators:
- Exit code 1: Validation FAILED (MUST fix errors before proceeding)
- "DATA RECORD LINE LENGTH ISSUES DETECTED": Lines not exactly 80 characters
- "ERROR: Field positioning errors found": Field alignment problems

### Editing Methodology

1. ONE EDIT AT A TIME (never batch multiple field changes)
2. PRECISE CONTEXT MATCHING (use complete L-record + surrounding context)
3. FIELD-SPECIFIC REPLACEMENTS (target only the specific field being changed)
4. IMMEDIATE VALIDATION (check file structure after each edit)

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

**CRITICAL COLUMN RULE:** When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).

### Tools and Workflows

#### Java Format Check

```bash
python Java_FormatCheck.py Cl35_34s_p_g.ens
```

#### Run Java Program via Python Script

```bash
# Convert single file by name
python ens2pdf.py Si35_adopted

# Convert with full file path
python ens2pdf.py "finished/Si35/new/Si35_adopted.ens"

# Convert all files for an element
python ens2pdf.py Si

# Convert files matching pattern
python ens2pdf.py "Si35_*sig"

# Convert and open in VS Code (default)
python ens2pdf.py Si35_adopted --open

# Convert and open in system viewer
python ens2pdf.py Si35_adopted --open --system
```

#### PDF Generation

```powershell
# Single element
Set-Location "D:\X\ND\Files"
$element = "Al"
Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*.ens" | ForEach-Object {
    java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
}

# All elements
$elements = @("Al", "Ar", "Ca", "K", "Mg", "Na", "Ne", "P", "Si")
foreach ($element in $elements) {
    Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*adopted.ens" | ForEach-Object {
        java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
    }
}
```

---

## 5. CSV and Tabular Data Processing

**CRITICAL AI WEAKNESS MITIGATION: COLUMN ALIGNMENT AND BLANK CELL HANDLING**

### AI Frequent Failure Patterns to Avoid

- Assuming column positions without explicit mapping
- Ignoring blank cells that shift subsequent data columns
- Single-direction counting (forward only) leading to off-by-one errors
- Mismatched header-to-data column associations
- Treating blank cells as non-existent rather than positional placeholders

### Mandatory Verification Protocol

1. Column alignment: Explicitly map ALL columns including blank ones (never assume positions based on visible data alone)
2. Blank cells: Count blank cells meticulously (each blank cell shifts all subsequent column positions and can cause catastrophic data misalignment)
3. Bidirectional verification: Always cross-check both forward counting (header to data) and backward counting (data to header) to ensure accurate column-to-data mapping

### Critical Validation Steps for Tabular Data

- Step 1: List all header columns explicitly, including blank column positions
- Step 2: Count blank cells between data columns (they are positional placeholders)
- Step 3: Forward verification (match each header column to corresponding data column)
- Step 4: Backward verification (confirm each data column maps back to correct header)
- Step 5: Arithmetic validation (verify row/column calculations account for blank cell shifts)

### Example Failure Prevention

```
CSV Header Row: Name,Age,,City,Score
Data Row: John,25,,NYC,95

WRONG: Assume columns are [Name,Age,City,Score] (ignores blank column)
CORRECT: Map as [Name,Age,BLANK,City,Score] (blank shifts City to position 4)
```

**NEVER PROCEED WITHOUT COMPLETE COLUMN MAPPING VERIFICATION**

**CRITICAL COLUMN RULE:** When fixing a quantity's position to the correct columns, NEVER shift other field values to wrong columns. Only adjust spacing between fields (never move field data to incorrect columns).

### Random Spot-Check Validation

**QUALITY ASSURANCE BEST PRACTICE:** After systematic data entry or bulk corrections, perform random spot-check validation by manually verifying a few samples (5% of total) against source data. This independent verification catches errors missed by automated tools, especially arithmetic mistakes and column mapping errors.

**When to use:** After large-scale data entry, bulk corrections, arithmetic-intensive work, or before claiming task completion when extra confidence is needed.

**Verification Checklist (for each sample):**
- Arithmetic accuracy
- Values/uncertainties match source data exactly
- Mapping accuracy (correct fields)
- Row and column alignment

**If errors found:** Identify root cause immediately, analyze pattern (systematic vs isolated), correct all instances, re-validate comprehensively, perform new spot-check.

**Integration:** Use after automated validation passes (column calibration + energy ordering), document findings for reproducibility.

---

## 6. Academic Standards

### Professional English Grammar

Common corrections:
- Spelling: "stoped" to "stopped", "usign" to "using", "coeffcients" to "coefficients"
- Duplicates: "the the", "from from", etc.

### General Comment Ordering (Adopted.ens Files)

1. Isotope discovery (reference): experimental details
2. Production: production methods and studies
3. Decay measurements: half-life, decay modes
4. Radius measurement: nuclear radius determinations
5. Mass measurements: mass spectrometry, Q-values
6. Theoretical calculations: models, predictions (always last)

---


## 7. Averaging Tool Workflow

**CLI Tool:** `python .github/Java_Average.py VALUE1 UNC1 [VALUE2 UNC2 ...]`

This Python script replicates the exact algorithm from AverageTool_22January2025.jar:
- Variance formula: V = (dxp+dxm)²/4 + 0.3633802276324186*(dxp-dxm)²
- χ² test at 95% confidence → weighted or unweighted
- Ensures uncertainty ≥ minimum input uncertainty

**Workflow:**
1. Collect all measurements with uncertainties
2. Run: `python .github/Java_Average.py 280 50 215 70 130 60 120 65`
3. Use EXACT "Suggested Adopted Result" from output
4. Apply to ENSDF record with proper formatting


### Java Averaging Result Rules

When user provides ENSDF utility Java code averaging output:

1. **Use EXACT Java "Suggested Adopted Result"** - NEVER recalculate or substitute
2. **Use EXACT uncertainty** - Java applies "uncertainty ≥ any input uncertainty" rule
3. **Check weighted vs unweighted** - Use whichever Java suggests in comments
4. **Transcribe character-for-character** - No rounding or "improving"

**FORBIDDEN:** Recalculating, using different uncertainty, substituting weighted/unweighted

---

## Document Structure

This document is organized as follows:

**Main sections:**
1. ENSDF Text Format Standards: Superscripts, subscripts, Greek letters, mathematical symbols, and formatting examples
2. ENSDF 80-Column Format Standards: NUCID field rules, record format specifications (L, G, DP, B, E records), critical formatting rules (structural relationships, left-justification, energy ordering, flag rules), and LOG FT format rules
3. ENSDF Uncertainty Standards: Uncertainty format in data record fields (standard 2-column fields, extended fields, scientific notation, GT and LT markers) and uncertainty format in comment lines
4. ENSDF File Editing Workflow: File protection rules, mandatory edit-validate-repeat workflow, validation tools (before, during, and after editing), output interpretation guidelines, editing methodology, and tools and workflows
5. CSV and Tabular Data Processing: AI frequent failure patterns to avoid, mandatory verification protocol, critical validation steps, example failure prevention, and random spot-check validation
6. Academic Standards: Professional English grammar and general comment ordering for adopted.ens files
7. Java Averaging Code Rules: Mandatory rules for using Java averaging results, forbidden behaviors, and rationale

