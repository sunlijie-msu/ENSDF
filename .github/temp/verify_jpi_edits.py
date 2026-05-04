"""Verify post-edit state of Cl34_adopted.ens."""
lines = open('A34/Cl34/new/Cl34_adopted.ens', encoding='utf-8').readlines()

# Find all occurrences of gives-added lines for 35Cl and 33S
print('=== All "gives" added J$ lines ===')
targets = [
    'from 3/2+ in {+33}S({+3}He,d) gives',
    'from 3/2+ in {+35}Cl({+3}He,|a) gives',
    'from 0+ in {+32}S(|a,d) gives',
    'from 0+ in {+36}Ar(d,|a),(pol d,|a) gives',
    'L=0+2,2+4 from 0+ in {+36}Ar',
    'L=1+3 gives 2-',
]
for target in targets:
    found = [(i+1, lines[i].rstrip('\n')) for i, l in enumerate(lines) if target in l]
    print(f'\n  Pattern: "{target}" ({len(found)} occurrences):')
    for n, txt in found:
        ok = 'OK' if len(txt)==80 else f'ERR({len(txt)})'
        prev = lines[n-2].rstrip('\n') if n>1 else ''
        print(f'    L{n}[{ok}]: |{txt}|')
        print(f'       prev: |{prev}|')

print()
# Check for any remaining verbose forms that should have been replaced
print('=== Verbose forms that should be gone ===')
verbose_checks = [
    ('should be gone', 'L=0 gives 1+; L=2 gives 1+,2+,3+'),
    ('should be gone', 'L=1 gives 0-,1-,2-; L=3 gives 2-,3-,4-'),
    ('should be gone (L2181)', 'L=2 gives   '),
    ('should be gone (L4786)', 'L=1 gives 0-,1-,2-'),
]
for label, check in verbose_checks:
    found = [(i+1, lines[i].rstrip('\n')) for i, l in enumerate(lines) if check in l]
    if found:
        for n, txt in found:
            print(f'  STILL EXISTS ({label}) L{n}: |{txt}|')
    else:
        print(f'  CLEAN ({label}): not found')
