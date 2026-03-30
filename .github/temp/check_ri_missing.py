"""Check all FLAG=B and FLAG=AB delete-only G-records for missing RI$From."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# All FLAG=B (delete only) and FLAG=AB (delete only for RI$) from the JSON
# FLAG=AB: G 204.58, G 519.22, G 564.67, G 769.25, G 1083.9, G 1426.7
# FLAG=B:  G 1740.2, G 927.6, G 1697.6, G 2011.4, G 2157.8, G 1145.4, G 2230.1

targets = ['204.58', '519.22', '564.67', '769.25', '1083.9', '1426.7',
           '1740.2', '927.6', '1697.6', '2011.4', '2157.8', '1145.4', '2230.1']

for energy in targets:
    for i, l in enumerate(lines):
        if '  G ' + energy in l and l[0:5].strip():
            blk = ''.join(lines[i:i+10])
            has_ri_from = 'RI$From {+32}S({+3}He' in blk
            status = 'HAS RI$From' if has_ri_from else 'MISSING RI$From'
            print(f'G {energy} (line {i+1}): {status}')
            for j in range(i, min(len(lines), i+7)):
                print(f'  {j+1}: {repr(lines[j].rstrip())}')
            print()
            break
