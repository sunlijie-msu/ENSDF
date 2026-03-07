"""
Spot-check: verify all $E(p)(lab)= cL data lines end with period.
"""
raw = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

marker = 'cL $E(p)(lab)='

ep_missing = []
ep_ok = []
for i, line in enumerate(lines, 1):
    if marker in line:
        stripped = line.rstrip()
        if stripped.endswith('.'):
            ep_ok.append(i)
        else:
            ep_missing.append((i, stripped))

print(f'Ep cL lines WITH period:    {len(ep_ok)}')
print(f'Ep cL lines WITHOUT period: {len(ep_missing)}')
if ep_missing:
    print('\nMISSING PERIOD lines:')
    for ln, s in ep_missing:
        print(f'  L{ln}: {repr(s[-70:])}')
else:
    print('\nAll $E(p)(lab)= cL lines end with period. PASS.')

# Also check for multi-|w|g semicolons
print()
for i, line in enumerate(lines, 1):
    stripped = line.rstrip()
    if 'cL $|w|g=' in stripped and '; ' in stripped:
        print(f'L{i} MULTI-WG: {repr(stripped[-70:])}')
