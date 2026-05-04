"""
apply_cl34_fixes.py
Apply all exact-string comment fixes to Cl34_adopted.ens.
Uses line-number-based replacement for precision.
Lines are 1-indexed. All ENSDF lines are exactly 80 chars wide (before newline).
"""
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

# --- Replacements: (line_number_1indexed, old_content_stripped, new_content_stripped) ---
# new_content_stripped will be padded/trimmed to 80 chars before writing.
# For multi-line restructured blocks, use tuples covering both lines.

def pad80(s):
    """Pad or trim to exactly 80 chars (not counting newline)."""
    return s[:80].ljust(80)

# Each entry: (line1, old1, new1)  -- single-line replacement
# OR: (line1, line2, old1, old2, new1, new2) -- two-line block replacement
REPLACEMENTS = [
    # ── 1. Parent 2157.9 (lines 243-244): restructure line split ──────────────
    # OLD 243: ' 34CL cL J$1697|g, M1+E2, |DJ=1 |g to 1+, 461 level; 2012|g, M1+E2, |DJ=1 to 3+,'
    # OLD 244: ' 34CL2cL 146 level. L=0 from 3/2+ in {+35}Cl(p,d) gives 1+,2+.                  '
    (243, 244,
     ' 34CL cL J$1697|g, M1+E2, |DJ=1 |g to 1+, 461 level; 2012|g, M1+E2, |DJ=1 to 3+,',
     ' 34CL2cL 146 level. L=0 from 3/2+ in {+35}Cl(p,d) gives 1+,2+.',
     ' 34CL cL J$1697.5|g, M1+E2, |DJ=1 |g to 1+, 461.01 level; 2012|g, M1+E2, |DJ=1',
     ' 34CL2cL to 3+, 146.36 level. L=0 from 3/2+ in {+35}Cl(p,d) gives 1+,2+.',
    ),

    # ── 2. Parent 3646.3 (lines 627-628): restructure line split ──────────────
    # OLD 627: ' 34CL cL J$3500|g, E2, |DJ=2 to 3+, 146 level. 725|g, M1+E2, from 4+, 4371      '
    # OLD 628: ' 34CL2cL level.                                                                 '
    (627, 628,
     ' 34CL cL J$3500|g, E2, |DJ=2 to 3+, 146 level. 725|g, M1+E2, from 4+, 4371',
     ' 34CL2cL level.',
     ' 34CL cL J$3500|g, E2, |DJ=2 to 3+, 146.36 level. 725|g, M1+E2, from 4+,',
     ' 34CL2cL 4371.5 level.',
    ),

    # ── 3. Parent 3660.0 (line 639) ───────────────────────────────────────────
    # OLD: ' 34CL cL J$1502|g to 2+, 2157 level.                                            '
    (639, ' 34CL cL J$1502|g to 2+, 2157 level.',
          ' 34CL cL J$1502.1|g to 2+, 2157.9 level.'),

    # ── 4. Parent 3791.7 (line 663) ───────────────────────────────────────────
    # OLD: ' 34CL cL J$3330|g to 1+, 461 level.                                             '
    (663, ' 34CL cL J$3330|g to 1+, 461 level.',
          ' 34CL cL J$3330.5|g to 1+, 461.01 level.'),

    # ── 5. Parent 4371.5 (line 814) ───────────────────────────────────────────
    # OLD: ' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646 level.                               '
    (814, ' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646 level.',
          ' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646.3 level.'),

    # ── 6. Parent 4446.6 (line 836) ───────────────────────────────────────────
    # OLD: ' 34CL cL J$4300.0|g, D(+Q), to 3+, 146 level.                                   '
    (836, ' 34CL cL J$4300.0|g, D(+Q), to 3+, 146 level.',
          ' 34CL cL J$4300.0|g, D(+Q), to 3+, 146.36 level.'),

    # ── 7. Parent 4824.18 (lines 982-983): restructure line split ─────────────
    # OLD 982: ' 34CL cL J$1224.1|g, E1(+M2), |DJ=1 to 4-, 3600 level; 4677.4|g, E2, |DJ=2 to   '
    # OLD 983: ' 34CL2cL 3+, 146 level.                                                         '
    (982, 983,
     ' 34CL cL J$1224.1|g, E1(+M2), |DJ=1 to 4-, 3600 level; 4677.4|g, E2, |DJ=2 to',
     ' 34CL2cL 3+, 146 level.',
     ' 34CL cL J$1224.1|g, E1(+M2), |DJ=1 to 4-, 3600.14 level; 4677.4|g, E2, |DJ=2',
     ' 34CL2cL to 3+, 146.36 level.',
    ),

    # ── 8. Parent 4862.4 (line 1027) ──────────────────────────────────────────
    # OLD: ' 34CL cL J$2681|g, M2, |DJ=2 to 3+, 2181.9 level. 453|g from 7+, 5314.95 level. '
    (1027, ' 34CL cL J$2681|g, M2, |DJ=2 to 3+, 2181.9 level. 453|g from 7+, 5314.95 level.',
           ' 34CL cL J$2681|g, M2, |DJ=2 to 3+, 2181.09 level. 453|g from 7+, 5314.95 level.'),

    # ── 9. Parent ~4958 (line 1054, 3cL continuation) ─────────────────────────
    # OLD: ' 34CL3cL 4810.5|g to 3+, 146 level.                                            '
    (1054, ' 34CL3cL 4810.5|g to 3+, 146 level.',
           ' 34CL3cL 4810.8|g to 3+, 146.36 level.'),

    # ── 10. Parent ~5387 (line 1174, 2cL continuation) ───────────────────────
    # OLD: ' 34CL2cL transition 1786.6 |g to 4-, 3600 level gives (2-,3,4,5,6-).'
    (1174, ' 34CL2cL transition 1786.6 |g to 4-, 3600 level gives (2-,3,4,5,6-).',
           ' 34CL2cL transition 1786.6 |g to 4-, 3600.14 level gives (2-,3,4,5,6-).'),

    # ── 11. Parent 5541.1 (line 1209) ─────────────────────────────────────────
    # OLD: ' 34CL cL J$primary transition 1330|g, from 5-, 6870 level???                    '
    (1209, ' 34CL cL J$primary transition 1330|g, from 5-, 6870 level???',
           ' 34CL cL J$primary transition 1330.1|g, from 5-, 6871.18 level???'),

    # ── 12. Parent ~5577 (line 1223, 2cL continuation) ───────────────────────
    # OLD: ' 34CL2cL 1977.0|g to 4-, 3600 level and 3201.4|g to 4+, 2375 level give'
    (1223, ' 34CL2cL 1977.0|g to 4-, 3600 level and 3201.4|g to 4+, 2375 level give',
           ' 34CL2cL 1977.0|g to 4-, 3600.14 level and 3201.4|g to 4+, 2375.67 level give'),

    # ── 13. Parent 5763.3 (line 1310) ─────────────────────────────────────────
    # OLD: ' 34CL cL J$primary transitions 5762.8|g to 0+, g.s. and 5616.4|g to 3+, 146     '
    (1310, ' 34CL cL J$primary transitions 5762.8|g to 0+, g.s. and 5616.4|g to 3+, 146',
           ' 34CL cL J$primary transitions 5762.8|g to 0+, g.s. and 5616.4|g to 3+, 146.36'),

    # ── 14. Parent ~5785 (line 1327, 2cL continuation) ───────────────────────
    # OLD: ' 34CL2cL transition 5638.6|g to 3+, 146 level gives (1+,2,3,4,5+).'
    (1327, ' 34CL2cL transition 5638.6|g to 3+, 146 level gives (1+,2,3,4,5+).',
           ' 34CL2cL transition 5638.6|g to 3+, 146.36 level gives (1+,2,3,4,5+).'),

    # ── 15-19: Parent 7250.0, 7699.5, 7801.5, 8155.5, 9392.7 (5315.4→5314.95)
    # These use `5315.4 level` which appears in different cL lines, each unique by gamma energy.
    # Line 2273:
    (2273, ' 34CL cL J$1935.0|g, E2, |DJ=2 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).',
           ' 34CL cL J$1935.0|g, E2, |DJ=2 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).'),
    # Line 2476:
    (2476, ' 34CL cL J$2384|g, M1, |DJ=0 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).',
           ' 34CL cL J$2384|g, M1, |DJ=0 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).'),
    # Line 2517 (J$ for parent 7801.5): fix 2487.4|g → 2486.2|g AND 5315.4 → 5314.95
    (2517, ' 34CL cL J$2487.4|g, E1+M2, to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).',
           ' 34CL cL J$2486.2|g, E1+M2, to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).'),
    # Line 2683:
    (2683, ' 34CL cL J$2840|g, M1+E2, to 7+, 5315.4 level',
           ' 34CL cL J$2840|g, M1+E2, to 7+, 5314.95 level'),
    # Line 2904:
    (2904, ' 34CL cL J$4077|g, M1(+E2), |DJ=0 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).',
           ' 34CL cL J$4077|g, M1(+E2), |DJ=0 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).'),

    # ── 20. Parent 10631.7 (line 2910): 7250.1 → 7250.0 ──────────────────────
    (2910, ' 34CL cL J$3381|g, E2, |DJ=2 to 9+, 7250.1 level in {+27}Al({+12}C,|an|g).',
           ' 34CL cL J$3381|g, E2, |DJ=2 to 9+, 7250.0 level in {+27}Al({+12}C,|an|g).'),
]


def apply_fixes(path):
    with open(path, encoding='utf-8') as fh:
        lines = fh.readlines()

    # Build dict: lineno -> (old_stripped, new_stripped)
    # For two-line replacements, store both
    single = {}
    pairs = {}

    for rep in REPLACEMENTS:
        if len(rep) == 3:
            lineno, old, new = rep
            single[lineno] = (old.rstrip(), new.rstrip())
        elif len(rep) == 6:
            l1, l2, old1, old2, new1, new2 = rep
            pairs[l1] = (l2, old1.rstrip(), old2.rstrip(), new1.rstrip(), new2.rstrip())
        else:
            raise ValueError(f"Unexpected replacement tuple length: {len(rep)}")

    errors = []
    applied = []
    skip_next = set()

    for i, line in enumerate(lines):
        lineno = i + 1   # 1-indexed
        stripped = line.rstrip('\n').rstrip('\r')

        if lineno in skip_next:
            continue

        if lineno in pairs:
            l2, old1, old2, new1, new2 = pairs[lineno]
            actual1 = stripped
            actual2 = lines[l2 - 1].rstrip('\n').rstrip('\r') if l2 <= len(lines) else ''
            # Check old1 matches (strip trailing spaces for comparison)
            if actual1.rstrip() == old1.rstrip():
                if actual2.rstrip() == old2.rstrip():
                    lines[i] = pad80(new1) + '\n'
                    lines[l2 - 1] = pad80(new2) + '\n'
                    applied.append(f'Line {lineno}-{l2}: restructured')
                    skip_next.add(l2)
                else:
                    errors.append(f'Line {l2} mismatch: expected={old2!r} actual={actual2!r}')
            else:
                errors.append(f'Line {lineno} mismatch: expected={old1!r} actual={actual1!r}')

        elif lineno in single:
            old, new = single[lineno]
            if stripped.rstrip() == old.rstrip():
                lines[i] = pad80(new) + '\n'
                applied.append(f'Line {lineno}: fixed')
            else:
                errors.append(f'Line {lineno} mismatch: expected={old!r} actual={stripped!r}')

    if errors:
        print(f'\nERRORS ({len(errors)}):')
        for e in errors:
            print(f'  {e}')
        print('\nNo changes written due to errors.')
    else:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.writelines(lines)
        print(f'Successfully applied {len(applied)} fix(es):')
        for a in applied:
            print(f'  {a}')


if __name__ == '__main__':
    apply_fixes(ENS_FILE)
