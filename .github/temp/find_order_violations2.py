import re

with open('A34/Cl34/new/Cl34_33s_p_g.ens', 'r') as f:
    lines = f.readlines()

def cg_rank(ident):
    u = ident.strip().upper()
    # E$ or E,RI$ - E alone or E-only variants
    if u == 'E': return 1
    if u.startswith('RI'): return 2
    if u in ('M', 'M,MR'): return 3
    if u == 'MR': return 4
    return 5

def cl_rank(ident):
    u = ident.strip().upper()
    if u == 'E': return 1
    if u.startswith('J'): return 2
    if u.startswith('T'): return 3
    if u.startswith('S') and not u.startswith('S,'): return 4
    return 5

def get_ident(line, rec_type):
    # Content starts at col 9 (0-indexed)
    content = line[9:] if len(line) > 9 else ''
    m = re.match(r'([^$]+)\$', content)
    if m:
        return m.group(1).rstrip()
    return ''

violations = []
i = 0
while i < len(lines):
    line = lines[i]
    if len(line) < 9:
        i += 1
        continue
    # Primary G or L record: col[5]=' '(blank cont), col[6]=' ', col[7] in 'GL'
    if line[5] == ' ' and line[6] == ' ' and line[7] in ('G', 'L'):
        rec_type = line[7]
        block_start = i
        j = i + 1
        block = []
        # Collect all cG/cL lines belonging to this record
        while j < len(lines):
            nl = lines[j]
            if len(nl) < 8:
                break
            # Primary cG/cL: col[6]='c', col[7]=rec_type
            # Continuation cG/cL: col[5] != ' ', col[6]='c', col[7]=rec_type
            if nl[6] == 'c' and nl[7] == rec_type:
                block.append((j + 1, nl))
                j += 1
            else:
                break
        # Get identifiers from PRIMARY (non-continuation) comment lines only (col[5]==' ')
        idents = []
        for lineno, bl in block:
            if len(bl) > 5 and bl[5] == ' ':
                ident = get_ident(bl, rec_type)
                idents.append((lineno, ident))
        # Check ordering
        rank_fn = cg_rank if rec_type == 'G' else cl_rank
        prev_r = 0
        prev_id = ''
        for lineno, ident in idents:
            r = rank_fn(ident)
            if r < prev_r:
                violations.append((rec_type, lineno, ident, prev_id, block_start + 1))
            prev_r = r
            prev_id = ident
    i += 1

for v in violations:
    print(f'Line {v[1]:4d}: c{v[0]} identifier="{v[2]}" comes after "{v[3]}" (record at line {v[4]})')
print(f'\nTotal: {len(violations)} violations')
