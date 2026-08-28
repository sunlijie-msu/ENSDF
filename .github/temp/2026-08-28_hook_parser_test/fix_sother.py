# FIX: add missing cL S$other: NNNN {I5} (1965Mc07) comments for Wi01+Mc07 levels.
# Source of truth: 1967WI01_Table_1.md "Previous number (1965MC07)" column,
# cross-checked against 1965MC07_Table_1.md E_alpha(lab) values.
# Placement: after first immediate cL general ($) comment if present, else right after L-record
# (matches the 6 already-accepted S$other comments).
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'

# level_energy -> Mc07 E_alpha value
NEW_SOTHER = {
    '11444': 3993,
    '11457': 4007,
    '11473': 4024,
    '11489': 4043,
    '11505': 4058,
    '11544': 4106,
    '11618': 4160,
    '11642': 4220,
}

with open(path, 'r', encoding='utf-8', newline='') as f:
    lines = f.read().split('\r\n')

def is_L(ln):
    return len(ln) >= 9 and ln[5:9] == '  L '

def is_cL(ln):
    return len(ln) >= 9 and ln[6:9] == 'cL '

def is_general_cL(ln):
    # cL $... (general comment, identifier before $)
    return is_cL(ln) and ln[9:10] == '$'

inserted = []
i = 0
while i < len(lines):
    ln = lines[i]
    if is_L(ln):
        e = ln[9:19].strip()
        if e in NEW_SOTHER:
            # find insertion point
            j = i + 1
            if j < len(lines) and is_general_cL(lines[j]):
                j += 1
            newline = (' 34S  cL S$other: %d {I5} (1965Mc07)' % NEW_SOTHER[e]).ljust(80)
            assert len(newline) == 80, newline
            lines.insert(j, newline)
            inserted.append((e, NEW_SOTHER[e], j + 1))
            i = j + 1
            continue
    i += 1

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(lines))

print('Inserted S$other comments:')
for e, val, lineno in inserted:
    print(f'   line {lineno}: E={e} -> S$other {val}')
print('Total inserted:', len(inserted), 'expected:', len(NEW_SOTHER))
