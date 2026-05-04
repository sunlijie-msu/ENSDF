"""
apply_fixes_final.py
Apply all comment-quoted-value fixes to Cl34_adopted.ens.
Uses content-based matching, not line-number-based.
"""
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

def p80(s):
    """Pad to exactly 80 chars (no newline)."""
    return s[:80].ljust(80)

def read_file():
    with open(ENS_FILE, encoding='utf-8') as f:
        return f.read()

def write_file(content):
    with open(ENS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def apply_all():
    content = read_file()
    errors = []
    applied = []

    # ------------------------------------------------------------------
    # Helper: replace exactly one occurrence of old_block with new_block
    # ------------------------------------------------------------------
    def replace_once(old_block, new_block, label):
        nonlocal content
        count = content.count(old_block)
        if count == 0:
            errors.append(f'{label}: OLD BLOCK NOT FOUND')
            return
        if count > 1:
            errors.append(f'{label}: OLD BLOCK FOUND {count} TIMES (ambiguous)')
            return
        content = content.replace(old_block, new_block, 1)
        applied.append(label)

    # ==================================================================
    # Lines 243-244: restructure
    # OLD: 1697|g -> 1697.5|g, 461 level -> 461.01 level, 146 level -> 146.36 level
    # ==================================================================
    old243 = p80(' 34CL cL J$1697|g, M1+E2, |DJ=1 |g to 1+, 461 level; 2012|g, M1+E2, |DJ=1 to 3+,') + '\n'
    old244 = p80(' 34CL2cL 146 level. L=0 from 3/2+ in {+35}Cl(p,d) gives 1+,2+.') + '\n'
    new243 = p80(' 34CL cL J$1697.5|g, M1+E2, |DJ=1 |g to 1+, 461.01 level; 2012|g, M1+E2, |DJ=1') + '\n'
    new244 = p80(' 34CL2cL to 3+, 146.36 level. L=0 from 3/2+ in {+35}Cl(p,d) gives 1+,2+.') + '\n'
    replace_once(old243 + old244, new243 + new244, 'Lines 243-244 (1697.5|g, 461.01 level, 146.36 level)')

    # ==================================================================
    # Lines 627-628: restructure
    # OLD: 146 level -> 146.36 level, 4371 -> 4371.5
    # ==================================================================
    old627 = p80(' 34CL cL J$3500|g, E2, |DJ=2 to 3+, 146 level. 725|g, M1+E2, from 4+, 4371') + '\n'
    old628 = p80(' 34CL2cL level.') + '\n'
    new627 = p80(' 34CL cL J$3500|g, E2, |DJ=2 to 3+, 146.36 level. 725|g, M1+E2, from 4+,') + '\n'
    new628 = p80(' 34CL2cL 4371.5 level.') + '\n'
    replace_once(old627 + old628, new627 + new628, 'Lines 627-628 (146.36 level, 4371.5)')

    # ==================================================================
    # Line 639: 1502|g -> 1502.1|g, 2157 level -> 2157.9 level
    # ==================================================================
    old639 = p80(' 34CL cL J$1502|g to 2+, 2157 level.') + '\n'
    new639 = p80(' 34CL cL J$1502.1|g to 2+, 2157.9 level.') + '\n'
    replace_once(old639, new639, 'Line 639 (1502.1|g, 2157.9 level)')

    # ==================================================================
    # Line 663: 3330|g -> 3330.5|g, 461 level -> 461.01 level
    # ==================================================================
    old663 = p80(' 34CL cL J$3330|g to 1+, 461 level.') + '\n'
    new663 = p80(' 34CL cL J$3330.5|g to 1+, 461.01 level.') + '\n'
    replace_once(old663, new663, 'Line 663 (3330.5|g, 461.01 level)')

    # ==================================================================
    # Line 814: 3646 level -> 3646.3 level
    # ==================================================================
    old814 = p80(' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646 level.') + '\n'
    new814 = p80(' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646.3 level.') + '\n'
    replace_once(old814, new814, 'Line 814 (3646.3 level)')

    # ==================================================================
    # Line 836: 146 level -> 146.36 level
    # ==================================================================
    old836 = p80(' 34CL cL J$4300.0|g, D(+Q), to 3+, 146 level.') + '\n'
    new836 = p80(' 34CL cL J$4300.0|g, D(+Q), to 3+, 146.36 level.') + '\n'
    replace_once(old836, new836, 'Line 836 (146.36 level)')

    # ==================================================================
    # Lines 982-983: restructure
    # OLD: 3600 level -> 3600.14 level, 146 level -> 146.36 level
    # ==================================================================
    old982 = p80(' 34CL cL J$1224.1|g, E1(+M2), |DJ=1 to 4-, 3600 level; 4677.4|g, E2, |DJ=2 to') + '\n'
    old983 = p80(' 34CL2cL 3+, 146 level.') + '\n'
    new982 = p80(' 34CL cL J$1224.1|g, E1(+M2), |DJ=1 to 4-, 3600.14 level; 4677.4|g, E2, |DJ=2') + '\n'
    new983 = p80(' 34CL2cL to 3+, 146.36 level.') + '\n'
    replace_once(old982 + old983, new982 + new983, 'Lines 982-983 (3600.14 level, 146.36 level)')

    # ==================================================================
    # Line 1027: 2181.9 level -> 2181.09 level
    # ==================================================================
    old1027 = p80(' 34CL cL J$2681|g, M2, |DJ=2 to 3+, 2181.9 level. 453|g from 7+, 5314.95 level.') + '\n'
    new1027 = p80(' 34CL cL J$2681|g, M2, |DJ=2 to 3+, 2181.09 level. 453|g from 7+, 5314.95 level.') + '\n'
    replace_once(old1027, new1027, 'Line 1027 (2181.09 level)')

    # ==================================================================
    # Line 1055: 4810.5|g -> 4810.8|g, 146 level -> 146.36 level
    # ==================================================================
    old1055 = p80(' 34CL3cL 4810.5|g to 3+, 146 level.') + '\n'
    new1055 = p80(' 34CL3cL 4810.8|g to 3+, 146.36 level.') + '\n'
    replace_once(old1055, new1055, 'Line 1055 (4810.8|g, 146.36 level)')

    # ==================================================================
    # Line 1175: 3600 level -> 3600.14 level
    # ==================================================================
    old1175 = p80(' 34CL2cL transition 1786.6 |g to 4-, 3600 level gives (2-,3,4,5,6-).') + '\n'
    new1175 = p80(' 34CL2cL transition 1786.6 |g to 4-, 3600.14 level gives (2-,3,4,5,6-).') + '\n'
    replace_once(old1175, new1175, 'Line 1175 (3600.14 level)')

    # ==================================================================
    # Line 1223: 3600 level -> 3600.14 level, 2375 level -> 2375.67 level
    # Content is 80 chars with no trailing spaces; needs to be split into 2 lines.
    # ==================================================================
    old1223 = p80(' 34CL2cL 1977.0|g to 4-, 3600 level and 3201.4|g to 4+, 2375 level give (3,4,5).') + '\n'
    new1223a = p80(' 34CL2cL 1977.0|g to 4-, 3600.14 level and 3201.4|g to 4+,') + '\n'
    new1223b = p80(' 34CL3cL 2375.67 level give (3,4,5).') + '\n'
    replace_once(old1223, new1223a + new1223b, 'Line 1223 (3600.14 level, 2375.67 level → split to 2 lines)')

    # ==================================================================
    # Lines 1308-1309: restructure
    # OLD: 146 -> 146.36 at end of line 1308
    # ==================================================================
    old1308 = p80(' 34CL cL J$primary transitions 5762.8|g to 0+, g.s. and 5616.4|g to 3+, 146') + '\n'
    old1309 = p80(' 34CL2cL level.') + '\n'
    new1308 = p80(' 34CL cL J$primary transitions 5762.8|g to 0+, g.s. and 5616.4|g') + '\n'
    new1309 = p80(' 34CL2cL to 3+, 146.36 level.') + '\n'
    replace_once(old1308 + old1309, new1308 + new1309, 'Lines 1308-1309 (146.36 level)')

    # ==================================================================
    # Line 1325: 146 level -> 146.36 level
    # ==================================================================
    old1325 = p80(' 34CL2cL transition 5638.6|g to 3+, 146 level gives (1+,2,3,4,5+).') + '\n'
    new1325 = p80(' 34CL2cL transition 5638.6|g to 3+, 146.36 level gives (1+,2,3,4,5+).') + '\n'
    replace_once(old1325, new1325, 'Line 1325 (146.36 level)')

    # ==================================================================
    # Line 2271: 5315.4 level -> 5314.95 level
    # ==================================================================
    old2271 = p80(' 34CL cL J$1935.0|g, E2, |DJ=2 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).') + '\n'
    new2271 = p80(' 34CL cL J$1935.0|g, E2, |DJ=2 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).') + '\n'
    replace_once(old2271, new2271, 'Line 2271 (5314.95 level)')

    # ==================================================================
    # Line 2474: 5315.4 level -> 5314.95 level
    # ==================================================================
    old2474 = p80(' 34CL cL J$2384|g, M1, |DJ=0 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).') + '\n'
    new2474 = p80(' 34CL cL J$2384|g, M1, |DJ=0 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).') + '\n'
    replace_once(old2474, new2474, 'Line 2474 (5314.95 level)')

    # ==================================================================
    # Line 2515: 2487.4|g -> 2486.2|g, 5315.4 level -> 5314.95 level
    # ==================================================================
    old2515 = p80(' 34CL cL J$2487.4|g, E1+M2, to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).') + '\n'
    new2515 = p80(' 34CL cL J$2486.2|g, E1+M2, to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).') + '\n'
    replace_once(old2515, new2515, 'Line 2515 (2486.2|g, 5314.95 level)')

    # ==================================================================
    # Line 2681: 5315.4 level -> 5314.95 level
    # ==================================================================
    old2681 = p80(' 34CL cL J$2840|g, M1+E2, to 7+, 5315.4 level') + '\n'
    new2681 = p80(' 34CL cL J$2840|g, M1+E2, to 7+, 5314.95 level') + '\n'
    replace_once(old2681, new2681, 'Line 2681 (5314.95 level)')

    # ==================================================================
    # Line 2902: 5315.4 level -> 5314.95 level
    # ==================================================================
    old2902 = p80(' 34CL cL J$4077|g, M1(+E2), |DJ=0 to 7+, 5315.4 level in {+27}Al({+12}C,|an|g).') + '\n'
    new2902 = p80(' 34CL cL J$4077|g, M1(+E2), |DJ=0 to 7+, 5314.95 level in {+27}Al({+12}C,|an|g).') + '\n'
    replace_once(old2902, new2902, 'Line 2902 (5314.95 level)')

    # ==================================================================
    # Line 2908: 7250.1 level -> 7250.0 level (same length, no overflow)
    # ==================================================================
    old2908 = p80(' 34CL cL J$3381|g, E2, |DJ=2 to 9+, 7250.1 level in {+27}Al({+12}C,|an|g).') + '\n'
    new2908 = p80(' 34CL cL J$3381|g, E2, |DJ=2 to 9+, 7250.0 level in {+27}Al({+12}C,|an|g).') + '\n'
    replace_once(old2908, new2908, 'Line 2908 (7250.0 level)')

    # ==================================================================
    # Report
    # ==================================================================
    if errors:
        print(f'\nERRORS ({len(errors)}):')
        for e in errors:
            print(f'  {e}')
        print('\nNo changes written due to errors.')
        return False
    else:
        write_file(content)
        print(f'Successfully applied {len(applied)} fix(es):')
        for a in applied:
            print(f'  {a}')
        return True


if __name__ == '__main__':
    success = apply_all()
    exit(0 if success else 1)
