# small_data_entry

## Goal

Use this prompt for one 1964Gl04 resonance table at a time.

- Source: `1964GL04_Ep*.md`
- Target: the matching resonance level block in the adopted ENSDF file
- Match by `E_p(lab)` in the `S` field

## Include

Enter only transitions labeled `(r) -> final level`.

- Include direct resonance decays.
- Exclude secondary decays such as `x -> y` unless explicitly requested.
- Exclude ambiguous rows unless explicitly requested.

## Core Rules

For each included row:

1. Convert `E_gamma` and its uncertainty from MeV to keV exactly.
2. Find the matching final level in the adopted file.
3. Match the transition to an existing `G` record if possible.

If a matching `G` record exists:

- Do not overwrite the existing `G` record energy or intensity fields.
- Add the 1964Gl04 intensity to `cG RI$other:`.
- If 1964Gl04 gives an energy uncertainty, add `cG E$other:`.
- Keep comment order: `E$`, then `RI$`, then general comments.

If no matching `G` record exists:

- Insert a new `G` record in ascending energy order.
- Enter `E`, `DE`, `RI`, and `DRI` from 1964Gl04.
- Put `?` in column 80.
- Add `cG E,RI$from 1964Gl04...`.
- Do not add `cG RI$other:` for the same 1964Gl04 intensity, because it is already the primary `RI` in the new `G` record.

## Comment Templates

```text
cG E$other: 3070 {I30} (1964Gl04)
cG RI$other: 8 {I2} (1964Gl04)
cG RI$other: 6.6 (1983Wa27), 8 {I2} (1964Gl04)
cG E,RI$from 1964Gl04, but not observed in later work.
```

## Safeguards

- Never shift unrelated fields.
- Never move the `T1/2` field or later columns when editing `L` records.
- Keep all data records exactly 80 characters.
- Keep the leading blank in column 1.
- Preserve ascending gamma order within the level block.

## Validation

For each new or changed data record:

```powershell
python .github/scripts/ensdf_1line_ruler.py --line "<exact 80-char line>"
```

After the block update:

```powershell
python .github/scripts/column_calibrate.py "<target-file>"
python .github/scripts/check_gamma_ordering.py "<target-file>"
```

## Done When

- Only `(r) -> final level` transitions were entered.
- Every 1964Gl04 intensity for an existing `G` record appears in `cG RI$other:`.
- Every 1964Gl04 energy with an explicit uncertainty appears in `cG E$other:` for existing records.
- Every missing transition was added as a new `G` record with `?` in column 80 and `cG E,RI$from 1964Gl04...`.
- Validation passes.