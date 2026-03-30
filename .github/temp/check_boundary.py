"""Precisely check which FLAG=B/AB records are missing RI$From, stopping at next G-record."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# All FLAG=B (delete only) and FLAG=AB (delete only for RI$) from JSON
targets = ['204.58', '519.22', '564.67', '769.25', '1083.9', '1426.7',
           '1740.2', '927.6', '1697.6', '2011.4', '2157.8', '1145.4', '2230.1']

for energy in targets:
    for i, l in enumerate(lines):
        if '  G ' + energy in l and l[0:5].strip():
            # Collect lines only until the next data record (L or G record)
            block = []
            for j in range(i, min(len(lines), i + 15)):
                block.append(lines[j])
                if j > i and lines[j][0:5].strip() and lines[j][7:8] in ('L', 'G', 'B', 'E') and lines[j][6:7] == ' ':
                    break  # stop at next L/G data record
            blk = ''.join(block)
            has_efrom  = 'cG E$From {+32}S({+3}He' in blk
            has_rifrom = 'cG RI$From {+32}S({+3}He' in blk
            e_status  = 'HAS' if has_efrom  else 'MISSING'
            ri_status = 'HAS' if has_rifrom else 'MISSING'
            print(f'G {energy}: E$From={e_status}, RI$From={ri_status}')
            for j in range(i, min(len(lines), i + 6)):
                print(f'  {j+1}: {lines[j].rstrip()}')
            print()
            break
