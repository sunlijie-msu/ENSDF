# ENSDF Lifetime Comments Standardization

## Purpose

A concise standard for writing T$ (lifetime) comment lines in ENSDF files. Keep language clear, preserve all numeric and bibliographic details, and format comments as single lines.

## Format

### Single measurement

```
T$from lifetime |t=VALUE UNIT {IUNC} (NSR, METHOD)
```

### Two measurements

```
T$from lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1) and VALUE2 UNIT {IUNC2} (NSR2, METHOD2).
```

### Three or more measurements

```
T$from lifetime |t=ADOPTED UNIT {IUNC}: average of VALUE1 UNIT {IUNC1} (NSR1, METHOD1), VALUE2 UNIT {IUNC2} (NSR2, METHOD2), and VALUE3 UNIT {IUNC3} (NSR3, METHOD3).
```

> Note: Keep the entire T$ comment on one logical line. Do not insert manual line breaks—80-column wrapping is handled externally.

## Examples

- Single (fs): `T$from lifetime |t=115 fs {I35} (1973Ca15, DSAM)`
- Single (ps): `T$from lifetime |t=1.3 ps {I10} (1973Ca15, DSAM)`
- Single (ns): `T$from lifetime |t=45 ns {I5} (1973Ca15, DSAM)`
- Single limit: `T$from lifetime |t>2 ps (1973Ca15, DSAM)`
- Asymmetric uncertainty: `T$from lifetime |t=1.3 ps {I+17-6} (1973Ca15, DSAM)`
- Two measurements: `T$from lifetime |t=1670 fs {I730}: average of 2400 fs {I1300} (1973Ca15, DSAM) and 940 fs {I400} (1970Br11).`
- Three measurements: `T$from lifetime |t=0.172 ps {I20}: average of 0.29 ps {I4} (1973Wa10, DSAM), 0.21 ps {I+10-8} (1969In04, DSAM), and 80 fs {I40} (1971Wi13, RDM).`
- Asymmetric average: `T$from lifetime |t=462 fs {I+120-80}: average of 600 fs {I150} (1973Ca15, DSAM) and 400 fs {I100} (1970Br11).`

## Rules (quick reference)

- ✅ **Do not wrap lines.** Keep T$ comments on a single line; do not insert manual breaks. Leave T$ comments as single lines; the user will use an existing VS Code extension to handle 80-column wrapping manually.
- ✅ **Preserve scientific accuracy.** Do not change values, uncertainties, or NSR keynumbers.
- ✅ **Units & notation.** Use `fs`, `ps`, `ns` etc.; use `{I+n-m}` for asymmetric uncertainties.
- ✅ **Method tags.** Use standard abbreviations (e.g., DSAM, RDM).
- ✅ **Ordering.** Adopted value first; list measurements in chronological order by NSR year when possible.
- ✅ **Formatting.** Use an Oxford comma in lists ("A, B, and C").
- ✅ **Limits.** Use `>` or `<` without uncertainty.
- ✅ **End punctuation.** Finish the comment with a period.

If you want, I can apply this standard to other ENSDF files or run a quick scan to identify nonconforming T$ comments.
