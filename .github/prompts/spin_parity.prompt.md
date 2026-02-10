---
applyTo: "**"
---
# Evaluated Nuclear Structure Data File (ENSDF) Spin-Parity Interpretation Reference

## L-Transfer Field Positioning

### L-Transfer Field Positioning Rule

- L always starts from column 56 (EXACT rule for L transferred angular momentum fields)
- `L=1` → `1` at column 56
- `L=1+2` → `1` at column 56, `+2` at columns 57-58
- `L=1,2` → `1` at column 56, `,2` at columns 57-58
- ONLY the first L-value must be at column 56; subsequent values follow sequentially

### L-Transfer from 0+ for J-π Assignment Rules

Physics mapping (single-nucleon transfer from a 0+ even-even target):
- j = L ± 1/2
- π = (−1)^L

L-Transfer values and corresponding J-π assignments:
- L=0 → J-π: `1/2+`
- L=1 → J-π: `1/2-,3/2-`
- L=2 → J-π: `3/2+,5/2+`
- L=3 → J-π: `5/2-,7/2-`
- L=4 → J-π: `7/2+,9/2+`

---

## J-π Assignment Notation

### Fundamental Rule

**CRITICAL**: J = spin; π = parity

- **WITHOUT parentheses**: Firm, well-established assignments (e.g., `3/2+`, `7/2-`)
- **WITH parentheses**: Less certain, tentative assignments (e.g., `(3/2+)`, `(7/2-)`)
- **Parentheses indicate uncertainty in the assignment confidence, not the measurement precision**
- **With/without parentheses and the placement of parentheses are critical for conveying the confidence level of the assignment** 



- `1/2-` = firm spin, firm parity, no other possibilities
- `(9/2+)` = tentative spin-parity, other spin-parity possibilities exist
- `7/2(+)` = firm spin with tentative parity, other spin impossible; other parity possible
- `(5/2)-` = tentative spin with firm negative parity, other spin possible; positive parity impossible
- `(11/2)` = tentative spin, parity unknown or undetermined
- `+` = only positive parity determined, spin unknown
- `-` = only negative parity determined, spin unknown
- `(+)` = tentative positive parity, spin unknown
- `(-)` = tentative negative parity, spin unknown

#### Multiple Possible Assignments

- `1/2-,3/2-` = multiple spins with firm parity (both certain, comma-separated), no other spin-parity possibilities
- `(5/2+,7/2+)` = multiple tentative possibilities, other spin-parity possibilities exist
- `(1/2,3/2)+` = multiple tentative spins with firm positive parity, other spins possible; negative parity impossible
- `(7/2,9/2)-` = multiple tentative spins with firm negative parity, other spins possible; positive parity impossible
- `(1/2,3/2,5/2)-` = multiple tentative spins with firm negative parity, other spins possible; positive parity impossible
- `(3/2,5/2,7/2+)` = mixed notation: first two spins with both parities possible, last spin with firm positive parity

#### Range Assignments

- `(1/2+:7/2+)` = range of tentative spin-parity assignments 1/2+, 3/2±, 5/2±, 7/2+; other spins possible; other parities possible.
- `(1/2:7/2)+` = range of tentative spins 1/2+, 3/2+, 5/2+, 7/2+ with firm positive parity; other spins possible; other parities impossible.
- `(1/2:7/2)(+)` = range of tentative spins 1/2+, 3/2+, 5/2+, 7/2+ with tentative positive parity; other spins possible; other parities possible.
- `1/2:7/2(-)` = range of firm spins 1/2-, 3/2-, 5/2-, 7/2- with tentative negative parity; other spins impossible; other parities possible.
- `1/2+:5/2+` = range of firm spin-parity assignments 1/2+, 3/2±, 5/2+; other spins impossible; other parities impossible.
- `(1/2:7/2)` = range of tentative spins 1/2, 3/2, 5/2, 7/2 with unknown parity; other spins possible; any parities possible.

#### Mixed Confidence Patterns

- `3/2-,(5/2-)` = first assignment firm, second tentative
- `(7/2)+,9/2+` = first assignment tentative, second firm
- `1/2(+),3/2-` = first has tentative parity, second fully firm
- `(5/2)+,(7/2)-` = multiple assignments with different confidence levels

#### Special Cases

- `1/2+,3/2-` = multiple firm assignments with different parities
- `(5/2+,7/2-)` = multiple tentative assignments with different parities
- `3/2,5/2,7/2` = multiple possible spins, parity undetermined
- `(1/2,3/2,5/2)` = multiple tentative spins, parity undetermined

### Critical Formatting Rules

- **Comma separation** for multiple possibilities within same confidence level
- **Parentheses apply to the entire group** when wrapping multiple values
- **Do not include explicit parity on an item inside a grouped tentative list**; if a subset has a different parity or confidence, split it out of the group
- **Mixed notation is allowed** by splitting: e.g., `1/2,3/2,5/2+` (first two tentative, parity unspecified; last firm positive)
- **No spaces** around commas in J-π field
- **Exact reproduction required** - never modify parentheses placement without experimental justification

### Critical Parentheses Matching Rule

Spin-parity with/without parentheses are considered to be different confidence levels. When creating J$ comments or adding values to J fields from reference data sources, ensure parentheses are preserved exactly as written in the source:

- **Source shows `3/2`** → Comment: `J$3/2 from [reference]` (NO parentheses)
- **Source shows `(3/2)`** → Comment: `J$(3/2) from [reference]` (single parentheses preserved)
- **NEVER use double parentheses**: `J$((3/2))` is FORBIDDEN
- **Examples**: `(1/2+)`, `1/2(+)`, `1/2+` represent different assignment confidence levels and the placement of parentheses must be matched accurately and precisely!
  
Ranges: 1/2:7/2 expands to 1/2, 3/2, 5/2, 7/2.
Lists: 3/2, 5/2 expands to set of both.
Parity Inheritance: (1/2, 3/2)+ applies + parity to both inner items, i.e., (1/2)+, (3/2)+.
Loose Matching: Parentheses () indicate tentative values.


