# ENSDF Lifetime Comments Standardization

## Format

### Single Measurement
```
T$from lifetime |t=VALUE UNIT {IUNC} (NSR, METHOD)
```

### Multiple Measurements (2 items)
```
T$from lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2).
```

### Multiple Measurements (3+ items)
```
T$from lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).
```

## Examples

**Single (fs unit):** `T$from lifetime |t=115 fs {I35} (1973Ca15, DSAM)`

**Single (ps unit):** `T$from lifetime |t=1.3 ps {I10} (1973Ca15, DSAM)`

**Single (ns unit):** `T$from lifetime |t=45 ns {I5} (1973Ca15, DSAM)`

**Single with limit:** `T$from lifetime |t>2 ps (1973Ca15, DSAM)`

**Single asymmetric uncertainty:** `T$from lifetime |t=1.3 ps {I+17-6} (1973Ca15, DSAM)`

**Multiple (2):** `T$from lifetime |t=1670 fs {I730}: average of 2400 fs {I1300} (1973Ca15, DSAM) and 940 fs {I400} (1970Br11).`

**Multiple (3):** `T$from lifetime |t=0.172 ps {I20}: average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 80 fs {I40} (1971Wi13, RDM).`

**Multiple with asymmetric:** `T$from lifetime |t=462 fs {I+120-80}: average of 600 fs {I150} (1973Ca15, DSAM) and 400 fs {I100} (1970Br11).`

## Rules

- **Do not wrap lines**: Leave T$ comments as single lines; external VS Code extension handles 80-column wrapping
- **Preserve scientific accuracy**: Never alter measurement values, uncertainties, or NSR keynumbers
- **Method abbreviations**: Use standard ENSDF abbreviations (DSAM, RDM, etc.)
- **Chronological ordering**: List measurements by NSR keynumber year when possible
- Adopted value always first
- List all measurements with NSR and method
- AP/APS Style: Use Oxford comma for complex items (e.g., "A, B, and C")
- Limits (`>`, `<`) have no uncertainty
- Asymmetric: `{I+n-m}` format
- End with period
