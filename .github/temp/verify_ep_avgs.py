"""
Spot-check verification for Ep average replacements.
1. Verify all $E(p)(lab)= cL lines now have the weighted-average format
2. Verify no remaining 'cL+2cL' pairs for Ep lines
3. Random 5% sample verification against ep_averages2.json
"""
import json, re, random

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
JSON = r'd:\X\ND\ENSDF\.github\temp\ep_averages2.json'

raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

# --- check 1: find Ep lines and verify format
avg_lines       = []
non_avg_multiep = []
ep_no_period    = []

for i, line in enumerate(lines, 1):
    if 'cL $E(p)(lab)=' not in line:
        continue
    stripped = line.rstrip()
    iunc_count = len(re.findall(r'\{I\d+\}', stripped))

    if iunc_count >= 2:
        # Should be weighted average format now
        if ': weighted average of' in stripped:
            avg_lines.append((i, stripped))
        else:
            non_avg_multiep.append((i, stripped))

    if not stripped.endswith('.'):
        ep_no_period.append((i, stripped[-60:]))

print(f'=== Ep weighted average lines: {len(avg_lines)} ===')
print(f'=== Multi-Ep lines NOT in avg format: {len(non_avg_multiep)} ===')
for ln, s in non_avg_multiep:
    print(f'  L{ln}: {s[-80:]}')
print(f'=== Ep lines missing period: {len(ep_no_period)} ===')
for ln, s in ep_no_period:
    print(f'  L{ln}: {s}')

# --- check 2: remaining spurious 2cL Ep continuation lines
print()
spurious_2cL = []
for i, line in enumerate(lines, 1):
    stripped = line.rstrip()
    if '2cL' in stripped and '$E(p)(lab)=' not in stripped:
        # Check if previous line had $E(p)(lab)=
        if i > 1 and 'cL $E(p)(lab)=' in lines[i-2]:
            spurious_2cL.append((i, stripped))
if spurious_2cL:
    print(f'=== Spurious 2cL after Ep lines: {len(spurious_2cL)} ===')
    for ln, s in spurious_2cL:
        print(f'  L{ln}: {s[:80]}')
else:
    print('=== No spurious 2cL Ep continuations. PASS. ===')

# --- check 3: random spot-check 5% of avg lines (~2 samples minimum 5)
data = json.load(open(JSON))
details = data['details']
sample_size = max(5, len(details) // 20 + 1)  # 5% of 31 = ~2, but min 5
random.seed(42)
sample = random.sample(details, min(sample_size, len(details)))

print(f'\n=== Random spot-check: {len(sample)} of {len(details)} entries ===')
all_pass = True
for r in sample:
    expected_new = r['new'].rstrip()
    # Find this line in the file
    found_in_file = False
    for i, line in enumerate(lines, 1):
        if line.rstrip() == expected_new:
            found_in_file = True
            break
    status = 'PASS' if found_in_file else 'FAIL'
    if not found_in_file:
        all_pass = False
    print(f'  [{status}] L{r["line_num"]}: avg={r["avg"]} | {expected_new[20:70]}')

if all_pass:
    print(f'\nAll {len(sample)} spot-checks PASSED.')
else:
    print(f'\nSPOT-CHECK FAILURES FOUND.')
