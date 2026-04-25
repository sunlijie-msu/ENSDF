"""Scan Cl34_adopted.ens for all cL T$ comment lines starting from L 1230.28."""

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# Find starting line
start = None
for i, line in enumerate(lines):
    if '34CL  L 1230.28' in line:
        start = i
        break

if start is None:
    print("ERROR: starting L-record not found")
else:
    print(f"Starting from line {start+1}: {repr(lines[start].rstrip())}")
    print()

    # Collect all T$ cL comment lines (and their continuation lines)
    results = []
    in_t_block = False
    current_block = []
    current_lrecord = None

    for i in range(start, len(lines)):
        raw = lines[i].rstrip()

        # Track L-records
        if len(raw) >= 8 and raw[6:8] == ' L':
            current_lrecord = (i+1, raw)
            in_t_block = False
            if current_block:
                results.append(current_block)
                current_block = []

        # First cL T$ line: col6=space, col7=c, col8=L (0-indexed: raw[5]=' ', raw[6]='c', raw[7]='L')
        if len(raw) >= 9 and raw[5] == ' ' and raw[6:8] == 'cL' and 'T$' in raw:
            in_t_block = True
            current_block = [(i+1, raw, 'T$', current_lrecord)]
        # Continuation lines (2cL, 3cL ... ) that belong to current T$ block
        elif in_t_block and len(raw) >= 8 and raw[6:8] == 'cL' and raw[5] in '23456789':
            current_block.append((i+1, raw, 'cont', current_lrecord))
        else:
            if current_block:
                results.append(current_block)
                current_block = []
            in_t_block = False

    if current_block:
        results.append(current_block)

    print(f"=== Total T$ cL comment blocks: {len(results)} ===\n")
    for block in results:
        for lineno, raw, kind, lrec in block:
            if lrec:
                print(f"  [L-record line {lrec[0]}]: {lrec[1]}")
            print(f"  Line {lineno}: {raw}")
        print()
