# ENSDF {In} Uncertainty Notation - Quick Reference Card

**CRITICAL RULE**: {In} notation MUST use **INTEGERS ONLY** - decimals are FORBIDDEN!

---

## Format Rules

### Correct Format
```
{In}  where n is an INTEGER (e.g., {I1}, {I11}, {I45})
```

### FORBIDDEN Formats
```
{I0.1}   ❌ WRONG - decimal not allowed
{I1.1}   ❌ WRONG - decimal not allowed  
{I2.7}   ❌ WRONG - decimal not allowed
```

---

## Conversion Formulas

### For Values with N Decimal Places
```
uncertainty_integer = round(uncertainty_value × 10^N)
```

### Specific Cases

**1 Decimal Place** (e.g., wγ = 3.6 eV):
```
uncertainty_int = round(Δwγ × 10)

Examples:
  Δwγ = 0.1 → 0.1 × 10 = 1 → {I1}
  Δwγ = 1.1 → 1.1 × 10 = 11 → {I11}
  Δwγ = 3.0 → 3.0 × 10 = 30 → {I30}
```

**2 Decimal Places** (e.g., E = 123.45 keV):
```
uncertainty_int = round(ΔE × 100)

Examples:
  ΔE = 0.01 → 0.01 × 100 = 1 → {I1}
  ΔE = 0.45 → 0.45 × 100 = 45 → {I45}
  ΔE = 1.23 → 1.23 × 100 = 123 → {I123}
```

**3 Decimal Places** (e.g., T = 1.234 ps):
```
uncertainty_int = round(ΔT × 1000)

Examples:
  ΔT = 0.001 → 0.001 × 1000 = 1 → {I1}
  ΔT = 0.045 → 0.045 × 1000 = 45 → {I45}
  ΔT = 0.123 → 0.123 × 1000 = 123 → {I123}
```

---

## Physical Meaning

### Understanding {In} Notation

**The integer n represents uncertainty in the LAST SIGNIFICANT DIGIT**

Examples:
```
Value         | {I}   | ENSDF(n) | ± Form
--------------|-------|----------|------------------
3.6 eV        | {I11} | 3.6(11)  | 3.6 ± 1.1 eV
0.2 eV        | {I1}  | 0.2(1)   | 0.2 ± 0.1 eV
12.3 keV      | {I45} | 12.3(45) | 12.3 ± 4.5 keV
1.42 ps       | {I7}  | 1.42(7)  | 1.42 ± 0.07 ps
123.45 keV    | {I12} | 123.45(12)| 123.45 ± 0.12 keV
```

### Decimal Place Alignment

**1 decimal**: {In} means ± n × 0.1
```
3.6 eV {I11} = 3.6 ± (11 × 0.1) = 3.6 ± 1.1 eV
```

**2 decimals**: {In} means ± n × 0.01
```
12.34 keV {I56} = 12.34 ± (56 × 0.01) = 12.34 ± 0.56 keV
```

**3 decimals**: {In} means ± n × 0.001
```
1.234 ps {I78} = 1.234 ± (78 × 0.001) = 1.234 ± 0.078 ps
```

---

## Common Mistakes and Corrections

### Mistake Pattern 1: Using Decimal Format
```
WRONG:  3.6 eV {I1.1}   ❌
RIGHT:  3.6 eV {I11}    ✓

Reason: {I} notation requires integers only!
```

### Mistake Pattern 2: Missing Scale Factor
```
WRONG:  3.6 eV {I1}     ❌ (means 3.6 ± 0.1, not 3.6 ± 1.1)
RIGHT:  3.6 eV {I11}    ✓ (means 3.6 ± 1.1)

Reason: For 1-decimal values, multiply uncertainty by 10!
```

### Mistake Pattern 3: Forgetting Trailing Zero Significance
```
WRONG:  11.0 eV {I3}    ❌ (means 11.0 ± 0.3, not 11.0 ± 3.0)
RIGHT:  11.0 eV {I30}   ✓ (means 11.0 ± 3.0)

Reason: 11.0 has 1 decimal, so 3.0 → 3.0 × 10 = 30!
```

---

## Quick Conversion Table

### For wγ Values (1 Decimal Place)

| Δwγ (eV) | Calculation | {I} Notation |
|----------|-------------|--------------|
| 0.1      | 0.1 × 10 = 1 | {I1}        |
| 0.2      | 0.2 × 10 = 2 | {I2}        |
| 0.3      | 0.3 × 10 = 3 | {I3}        |
| 0.5      | 0.5 × 10 = 5 | {I5}        |
| 0.6      | 0.6 × 10 = 6 | {I6}        |
| 1.0      | 1.0 × 10 = 10 | {I10}      |
| 1.1      | 1.1 × 10 = 11 | {I11}      |
| 1.8      | 1.8 × 10 = 18 | {I18}      |
| 3.0      | 3.0 × 10 = 30 | {I30}      |

### For Energy Values (2 Decimal Places)

| ΔE (keV) | Calculation | {I} Notation |
|----------|-------------|--------------|
| 0.01     | 0.01 × 100 = 1 | {I1}      |
| 0.05     | 0.05 × 100 = 5 | {I5}      |
| 0.12     | 0.12 × 100 = 12 | {I12}    |
| 0.45     | 0.45 × 100 = 45 | {I45}    |
| 1.23     | 1.23 × 100 = 123 | {I123}  |

---

## Validation Checklist

### Before Creating {I} Notation

- [ ] Count decimal places in the value (N)
- [ ] Multiply uncertainty by 10^N
- [ ] Round result to nearest integer
- [ ] Use rounded integer in {In} notation
- [ ] Verify: does {In} correctly represent the uncertainty?

### Example Validation
```
Value: wγ = 3.6 eV (1 decimal place)
Uncertainty: Δwγ = 1.1 eV

Step 1: N = 1 (one decimal place)
Step 2: 1.1 × 10^1 = 1.1 × 10 = 11
Step 3: round(11) = 11
Step 4: {I11}
Step 5: Verify: 3.6 eV {I11} = 3.6(11) eV = 3.6 ± 1.1 eV ✓
```

---

## ENSDF Manual References

**Source**: `.github/copilot-instructions.md`

**Key Sections**:
- Lines 1135-1150: ENSDF Uncertainty Notation rules
- Lines 1629-1670: Decimal Places Conversion Table
- Lines 915-950: {In} notation format specifications

**Critical Quote**:
> "Symmetric uncertainties: {In} (e.g., {I7}, {I11}) - NO plus/minus signs"
> "NEVER use {I+n} for symmetric uncertainties - this is incorrect ENSDF format"

---

## When in Doubt

1. **Read copilot-instructions.md** sections on ENSDF uncertainty notation
2. **Count decimal places** in the value carefully
3. **Apply formula**: uncertainty_int = round(uncertainty × 10^decimals)
4. **Verify result** using ENSDF(n) notation
5. **Run validation tools** to confirm compliance

**Remember**: ENSDF systems are automated - one wrong {I} notation can cause data rejection!

---

**Created**: Phase 6 {I} Notation Correction (2025)  
**Purpose**: Quick reference for future ENSDF wγ/Δwγ comment creation  
**Status**: Validated against 103 corrected entries in 1972HU10.ens
