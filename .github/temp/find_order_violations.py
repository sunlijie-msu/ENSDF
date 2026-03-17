import re

with open('A34/Cl34/new/Cl34_33s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Ordering ranks for identifiers
def cg_rank(ident):
    ident = ident.strip().upper()
    if ident == 'E': return 1
    if ident == 'RI': return 2
    if ident in ('M', 'M,MR'): return 3
    if ident == 'MR': return 4
    return 5  # general / other

def cl_rank(ident):
    ident = ident.strip().upper()
    if ident == 'E': return 1
    if ident == 'J': return 2
    if ident == 'T': return 3
    if ident == 'S': return 4
    return 5  # general

def get_cg_ident(line):
    m = re.match(r'.{5}.cG ([^$\n]*)\$', line)
    if m:
        return m.group(1).strip()
    # No dollar-sign: general comment
    m = re.match(r'.{5}.cG (.+)', line)
    if m:
        text = m.group(1).strip()
        # If starts with known identifier and dollar, already matched above
        # Otherwise it's a general comment with identifier = ''
        return ''
    return None

def get_cl_ident(line):
    m = re.match(r'.{5}.cL ([^$\n]*)\$', line)
    if m:
        return m.group(1).strip()
    m = re.match(r'.{5}.cL (.+)', line)
    if m:
        return ''
    return None

violations = []
i = 0
while i < len(lines):
    line = lines[i]
    if len(line) >= 9:
        rec_type = line[7:8]
        cont = line[5:6]
        if rec_type in ('G', 'L') and cont == ' ':
            block_type = rec_type
            block_start = i
            block_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if len(next_line) >= 8:
                    # Match cG or cL in cols 6-8 (0-indexed 5-7)
                    pattern = 'cG' if block_type == 'G' else 'cL'
                    # col 5 (0-indexed) can be ' ', letter, digit
                    seg = next_line[5:8] if len(next_line) > 7 else ''
                    if re.match(r'[A-Za-z2-9 ]c' + ('G' if block_type == 'G' else 'L'), seg):
                        block_lines.append((j+1, next_line))
                        j += 1
                    else:
                        break
                else:
                    break

            # Collect identifiers from first-line comments (not continuations)
            idents_seen = []
            for lineno, bline in block_lines:
                cont6 = bline[5:6]
                # Continuation: col 6 is alphanumeric (not space)
                if re.match(r'[A-Za-z2-9]', cont6):
                    continue
                if block_type == 'G':
                    ident = get_cg_ident(bline)
                else:
                    ident = get_cl_ident(bline)
                if ident is not None:
                    idents_seen.append((lineno, ident))

            # Check ordering
            prev_rank = 0
            prev_ident = ''
            for lineno, ident in idents_seen:
                r = cg_rank(ident) if block_type == 'G' else cl_rank(ident)
                if r < prev_rank:
                    violations.append((f'c{block_type}', lineno, ident, prev_ident, block_start+1))
                prev_rank = r
                prev_ident = ident
    i += 1

if violations:
    print(f'Found {len(violations)} ordering violations:')
    for v in violations:
        print(f'  Type={v[0]}, Line={v[1]}, ident="{v[2]}" comes after "{v[3]}" (record at line {v[4]})')
else:
    print('No violations found.')
