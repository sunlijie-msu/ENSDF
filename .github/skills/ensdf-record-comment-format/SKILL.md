---
name: ensdf-record-comment-format
description: "Defines ENSDF record-comment fields, SYM$ identifiers, continuation rules, and record association. Use when checking, interpreting, or formatting comments attached to L, G, B, E, A, or DP records."
---

# Record Comment

| Field | Columns | Description                                                       |
| :---- | :------ | :---------------------------------------------------------------- |
| NUCID | 1–5     | Nuclide identification (e.g., ` 35P `, ` 76AS`, `127I `, `152GD`) |
| CONT  | 6       | Blank, or an alphanumeric continuation identifier other than `1`  |
| C     | 7       | Comment identifier: `c`                                           |
| RTYPE | 8       | Record type being commented on                                    |
| PSYM  | 9       | Blank, or Particle symbol `N` or `P`                              |
| SYM   | 10–80   | `$`, `SYM$`, `SYM,SYM$`, `SYM,SYM,SYM$`                           |
| CTEXT | 10–80   | Comment text follows the `$`delimiter                             |

## Notes

1. `$` delimiter cannot be omitted.
2. A record comment following `$` applies to that `RTYPE` record in general.
 - Example: 
```
 34S   L 2127.561  15 2+               0.315 PS  12                         Z   
 34S  cL $|b{-2}(p,p')=0.28 {I1} (1985Al03).                                    
```
3. `SYM` can be any data field of the L, G, B, E, A, or DP record (e.g., `E`, `J`, `T`, `S`, `RI`, `M`, `MR`, etc).
4. A record comment following a `SYM$` applies to that `SYM` field of that `RTYPE` record.
- Example:
```
 34S   L 2127.561  15 2+               0.315 PS  12                         Z   
 34S  cL J$spin=2 from p|g(|q) in {+31}P(|a,p|g). |p=+ from 2127.498|g, E2 to   
 34S 2cL 0+, g.s.                                                               

```
5. On continuation comment records, `CTEXT` may start in column 10, and `SYM` or `SYM`s are not repeated.

