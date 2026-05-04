"""Extract all L-records and their cL J$ comment lines for levels below a given energy."""

import sys

ADOPTED_PATH = r'A34\Cl34\new\Cl34_adopted.ens'
THRESHOLD = 5200.0

with open(ADOPTED_PATH, 'r') as f:
    lines = f.readlines()

current_level_block = None
current_E = None
current_line = None
in_scope = False
results = []
collecting_J = False  # True when last cL comment had J$

for i, line in enumerate(lines, 1):
    raw = line.rstrip('\n')
    # L-record detection: col8 (0-indexed: 7) == 'L', col6==col7==' '
    if len(raw) >= 9 and raw[7] == 'L' and raw[5] == ' ' and raw[6] == ' ':
        # Save previous block
        if current_level_block is not None and in_scope:
            results.append((current_line, current_E, current_level_block))
        # Start new block
        e_str = raw[9:19].strip()
        try:
            E = float(e_str)
        except ValueError:
            E = None
        current_E = E
        current_line = i
        in_scope = (E is not None and E < THRESHOLD)
        collecting_J = False
        current_level_block = []
        if in_scope:
            current_level_block = [(i, raw)]
    elif in_scope and current_level_block is not None and len(raw) >= 9:
        col6 = raw[5]   # 0-indexed index 5 = ENSDF col 6 (CONT)
        col7 = raw[6]   # 0-indexed index 6 = ENSDF col 7
        col8 = raw[7]   # 0-indexed index 7 = ENSDF col 8 (TYPE)
        # cL comment: ENSDF col7='c', col8='L' → raw[6]=='c', raw[7]=='L'
        if col7 == 'c' and col8 == 'L':
            rest = raw[9:].strip()
            if rest.startswith('J$'):
                current_level_block.append((i, raw))
                collecting_J = True
            else:
                collecting_J = False
        # 2cL, 3cL etc: col6 in '23456789', col7='c', col8='L'
        elif col6 in '23456789' and col7 == 'c' and col8 == 'L':
            if collecting_J:
                current_level_block.append((i, raw))
        else:
            # Non-comment line resets J$ continuation
            if col8 in ('G', 'B', 'E', 'A'):
                collecting_J = False

# Save last block
if current_level_block is not None and in_scope:
    results.append((current_line, current_E, current_level_block))

# Report
print(f"Total L-records below {THRESHOLD} keV: {len(results)}")
with_J = [(ln, E, blk) for ln, E, blk in results if len(blk) > 1]
print(f"L-records with cL J$ comments: {len(with_J)}")
print()

for linenum, E, block in with_J:
    print(f"=== Level E={E} keV (adopted line {linenum}) ===")
    for i, raw in block:
        print(f"  L{i:4d}: {raw}")
    print()
