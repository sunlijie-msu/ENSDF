# ENSDF Lifetime Comments Standardization

## Objective

Standardize all T$ (half-life) comments in ENSDF files to a consistent, evaluator-friendly format that clearly specifies measurement values, methods, and adopted values.

---

## Standard Format Patterns

### Single Measurement
```
T$from lifetime |t=VALUE UNIT {IUNCERTAINTY} (NSR, METHOD)
```
Examples: `T$from lifetime |t=115 fs {I35} (1973Ca15, DSAM)`, `T$from lifetime |t>2 ps (1973Ca15, DSAM)`

### Multiple Measurements
```
T$from lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).
```
Example: `T$from lifetime |t=0.172 ps {I20}: average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 80 fs {I40} (1971Wi13, RDM).`


---

## Field Specifications

| Field | Format | Notes |
|-------|--------|-------|
| Value | Exact number | No rounding; preserve decimal places |
| Unit | fs, ps, ns, μs, ms | Always after value |
| Uncertainty | {IUNC} or {I+n-m} | Asymmetric format for >0 or <0 ranges; limits use > or < |
| NSR | 8-char code | Format: YYYYAa## (e.g., 1973Ca15) |
| Method | Abbreviation | DSAM, RDM, etc. |
| Adopted value | First in sequence | State adopted value before measurements |

---

## Practical Examples

- **Single:** `T$from lifetime |t=115 fs {I35} (1973Ca15, DSAM)`
- **Dominant measurement:** `T$from lifetime |t=19.4 ps {I14}: average of 19.4 ps {I14} (1971Sn01, DSAM) and >14 ps (1970Br10).`
- **Multiple:** `T$from lifetime |t=1670 fs {I730}: average of 2400 fs {I1300} (1973Ca15, DSAM) and 940 fs {I400} (1970Br11).`
- **Limits:** `T$from lifetime |t>2 ps (1973Ca15, DSAM)` or `T$from lifetime |t<50 fs (1973Ca15, DSAM)`
- **Asymmetric uncertainty:** `T$from lifetime |t=1.3 ps {I+17-6} (1973Ca15, DSAM)`

---

## Workflow

1. Find all T$ comments: `grep "cL T\$" filename.ens`
2. For each level, determine: single measurement or multiple
3. Extract: adopted value, all measurements, NSR, method
4. Format: adopted value first, then individual measurements with NSR and method
5. Verify: all comments follow identical structure, NSR keynumbers correct

---

## Special Cases

- **Limits:** Use `>` or `<` without uncertainty notation
- **Asymmetric uncertainty:** Use `{I+n-m}` format
- **Mixed units:** List all measurements as reported; evaluator handles conversion logic

---

## Verification Checklist

- All T$ comments start with `T$from lifetime |t=`
- Single measurements: VALUE UNIT {IUNC} (NSR, METHOD)
- Multiple measurements: adopted value listed first
- All measurements include NSR and method
- Sentence ends with period
- No line wrapping (80-column formatting handled externally)

---

## Tools and Validation

### Finding T$ Comments
```bash
grep "cL T\$" filename.ens
```

### Visual Inspection
After editing, spot-check representative examples:
- One single-measurement case
- One multi-measurement weighted average
- One multi-measurement unweighted average
- One with asymmetric uncertainty
- One with limit (> or <)

---

## Notes

- **Do not wrap lines**: Leave T$ comments as single lines; external VS Code extension handles 80-column wrapping
- **Preserve scientific accuracy**: Never alter measurement values, uncertainties, or NSR keynumbers
- **Method abbreviations**: Use standard ENSDF abbreviations (DSAM, RDM, etc.)
- **Chronological ordering**: List measurements by NSR keynumber year when possible
