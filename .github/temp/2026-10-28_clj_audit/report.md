# cL J quoted-value audit — Ni58_adopted.ens

Check-only. 138 `cL J$` lines; 61 `gamma to/from Jpi` quotes; 40 dJ claims; 29 multipolarity claims.

Destination of each gamma = its own `F G FL=` continuation when present, else the level whose energy is closest to `E(level) - E(gamma)`. Quoted Jpi compared character-exact with the cols 21-39 field of that destination.

## Findings

| # | Line | Quoted | Record evidence | Verdict |
|---|------|--------|-----------------|---------|
| 1 | 1145 | `DJ=1, D+Q gamma to 7+` | `G 1752.0 D+Q`, `FL=6219.9`; that level is `(7+)` | Parentheses dropped. Line 1168 quotes the same level as `(7+)`. |
| 2 | 876 | `DJ=1, (M1+E2) gamma to 7+` | `G 537.0 (M1+E2)` to 6067.5 `(7+)`; `G 384.8` `FL=6219.9` `(7+)` | No exact `7+` destination in block. |
| 3 | 2295 | `gamma's to (13+) and (14+)` | `G 2283.0` to 13884.1 `(13+)`; `G 1062.0` to 15105.2, J field **blank** | `(14+)` not a recorded Jpi; level 15105.2 says only "suggest (12,13,14)". |
| 4 | 649 | `L(p,t)=4 for 5488 {I11}` | Level is 5472.3; no level within 5488 +/- 11 | Quoted energy off by 15.7 keV. |
| 5 | 1550 | `|p=(-) is in (p,p') is in disagreement` | Wording at 1516, 1542: `|p=(2-) in (e,e') is in disagreement` | Duplicated "is in". |
| 6 | 723 | `see comment for 5905.3 level` | 5905.3 is the energy of `G 5905.3 M1` (716); the level is 5905.6 (709) | Gamma energy labelled as a level. |
| 7 | 790, 796 | `L 6219.9 4 (7+)` vs `L 6220 10` | 0.1 keV apart, XREF=TU vs XREF=C, no comment; `G 1752.0`, `G 1854.3`, `G 384.8` all `FL=6219.9` | 6220 is left with no gamma and no Jpi. |

## Verified

| Check | Units | Pass |
|-------|-------|------|
| Quoted Jpi == destination level Jpi, character-exact | 61 | 58 (fail 1, 2) |
| Quoted Jpi exists somewhere in the scheme | 61 | 61 |
| dJ == spin difference of the quoted level pair | 40 | 40 |
| Quoted multipolarity present on that G record | 29 | 29 |
| d-pi vs explicit E1/E2/M1/M2/E3 | 14 | 14 |
| L(p,p'), L(a,a'), L(p,t) = J with natural parity | 32 | 32 |
| Quoted `N {In}` and `N gamma` values | 13 | 12 (fail 4) |

## Retracted from earlier drafts

| Line | Earlier claim | Why wrong |
|------|---------------|-----------|
| 934 | `D gamma to (5+)` implies pi=+ | Bare `D` is parity-agnostic: d-pi=yes gives E1, d-pi=no gives M1 (`gamma-selection-rules`). |
| 1960 | `2+,(4+) in (e,e')` breaks a sibling pattern | Meaning is "in (e,e') the level was 2+, tentatively 4+"; the quoted 2+ is inside the adopted `(1+,2+)`, so nothing is provably wrong. |
| 1108 | 3.3 keV gap to the 6+ level | Gamma DE is 20 keV; 3.3 keV is within 1 sigma. |
