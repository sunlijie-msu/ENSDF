# Apply E(alpha) data restructure per user rules:
#  A) Flag V (col77) on 22 Va08-only levels
#  B) Flag M (col77) on 21 Mc07-only levels (incl. former Table-4 levels, Table 4 omitted)
#  C) Replace old "cL $E(|a)(lab)=NNNN {I5}" with "cL S$other: MMMM {I5} (1965Mc07)" on 6 Wi01+Mc07 levels
#  D) Remove old "cL $E(|a)(lab)=NNNN {I5}" comments elsewhere (redundant with S field)
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'

V_LEVELS = {'9932','9981','10091','10097','10140','10169','10201','10236','10248',
            '10316','10385','10407','10447','10493','10528','10586','10616','10625',
            '10662','10670','10704','10767'}
M_LEVELS = {'10846','10868','10895','10916','10930','10994','11014','11025','11047',
            '11087','11107','11141','11165','11179','11193','11220','11233','11272',
            '11288','11314','11323'}
# Wi01+Mc07 (Rule 2): S = 1967Wi01 value (already in S field), cL S$other = 1965Mc07 value
RULE2 = {'11357': 3894, '11371': 3908, '11380': 3918,
         '11398': 3940, '11405': 3948, '11419': 3961}

with open(path, 'r', encoding='utf-8', newline='') as f:
    text = f.read()
lines = text.split('\r\n')

# --- 1) apply col-77 flags V/M ---
flag_added = []
for i, ln in enumerate(lines):
    if len(ln) >= 20 and ln[5:9] == '  L ':
        e = ln[9:19].strip()
        fl = None
        if e in V_LEVELS:
            fl = 'V'
        elif e in M_LEVELS:
            fl = 'M'
        if fl:
            if ln[76] != ' ':
                raise SystemExit(f'col77 not blank at line {i+1}: {ln[76]!r}')
            lines[i] = ln[:76] + fl + ln[77:]
            flag_added.append((i + 1, e, fl))

# --- 2) remove old E(|a) comment lines; replace with S$other on Rule-2 levels ---
current_l = None
out = []
removed = 0
replaced = []
for i, ln in enumerate(lines):
    if len(ln) >= 20 and ln[5:9] == '  L ':
        current_l = ln[9:19].strip()
        out.append(ln)
    elif current_l is not None and len(ln) >= 10 and ln[6:9] == 'cL ':
        m = re.search(r'\$E\(\|a\)\(lab\)=(\d+)', ln[9:])
        if m:
            if current_l in RULE2:
                new = (' 34S  cL S$other: %d {I5} (1965Mc07)' % RULE2[current_l]).ljust(80)
                out.append(new)
                replaced.append((i + 1, current_l, int(m.group(1)), RULE2[current_l]))
            else:
                removed += 1
            continue
        out.append(ln)
    else:
        out.append(ln)

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(out))

print('Flags added to col 77:')
for lineno, e, fl in flag_added:
    print(f'   line {lineno}: E={e} -> {fl}')
print()
print('E(|a) comment lines REMOVED:', removed)
print('E(|a) -> S$other REPLACED:')
for lineno, e, old, new in replaced:
    print(f'   line {lineno}: E={e} old={old} -> S$other {new}')
