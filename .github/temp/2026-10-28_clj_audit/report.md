# Ni58 adopted cL J gamma-destination audit

**Scope:** Check-only. Scanned all 206 `cL J` comment records and mapped all 71 quoted gamma-destination Jpi tokens. Of these, 68 match a destination L-record exactly, 2 omit parentheses present on the destination assignment, and 1 is supported only by an explicit possible-spin inference.

**Method:** Matched each quoted destination to its specific gamma using `FL=` when present, otherwise level-energy differences; checked the clause's stated multipolarity and `DJ` before comparing Jpi, preserving parentheses.

## Confirmed mismatches

| Line | Quoted clause | Record-level evidence | Finding |
|---:|---|---|---|
| 876 | `DJ=1, (M1+E2) gamma to 7+` | `G 537.0` is `(M1+E2)` and feeds `L 6067.5 (7+)`. | Quote omits parentheses; destination assignment is tentative. |
| 1145 | `DJ=1, D+Q gamma to 7+` | `G 1752.0` is `D+Q`, `FL=6219.9`; destination is `L 6219.9 (7+)`. | Quote omits parentheses; destination assignment is tentative. |

## Qualified, not a confirmed mismatch

| Line | Quoted clause | Record-level evidence | Finding |
|---:|---|---|---|
| 2297 | `gamma's to (13+) and (14+)` | `G 2283.0` feeds `L 13884.1 (13+)`. `G 1062.0` feeds `L 15105.2`, whose J field is blank; that level's own comment says its gamma decays suggest spins 12, 13, or 14. | `(13+)` matches directly. `(14+)` is possible by inference, not a recorded destination Jpi; do not call it a proven mismatch. |

No other quoted gamma-destination Jpi mismatches found. No ENSDF data files edited. This supersedes earlier report drafts and excludes withdrawn false positives.
