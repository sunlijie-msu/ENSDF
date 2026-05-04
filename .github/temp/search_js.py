"""Find all cL/2cL lines containing wrong quoted values"""
with open(r'A34\Cl34\new\Cl34_adopted.ens', encoding='utf-8') as f:
    lines = f.readlines()

# Wrong values to find (exact substrings)
wrong_values = [
    '1697|g',    # should be 1697.5|g
    '461 level',  # should be 461.01 level
    '1502|g',    # should be 1502.1|g
    '2157 level', # should be 2157.9 level
    '3330|g',    # should be 3330.5|g
    '3646 level', # should be 3646.3 level
    '146 level',  # should be 146.36 level
    '4371 level', # should be 4371.5 level  (in 2cL: '4371 ' at end or 'level' in next)
    '3600 level', # should be 3600.14 level
    '2181.9 level', # should be 2181.09 level
    '1330|g',    # should be 1330.1|g
    '6870 level',  # should be 6871.18 level
    '5315.4 level', # should be 5314.95 level
    '2487.4|g',  # should be 2486.2|g
    '7250.1 level', # should be 7250.0 level
]

print("Lines containing wrong quoted values:")
for i, line in enumerate(lines, 1):
    for w in wrong_values:
        if w in line:
            col6 = line[5] if len(line) > 5 else '?'
            col8 = line[7] if len(line) > 7 else '?'
            print(f'  Line {i:5d} (col6={col6!r},col8={col8!r}): found {w!r}')
            print(f'          {repr(line.rstrip()[:80])}')
            break
