"""
Match S35 p_d levels to adopted levels.
For each p_d level, find the closest adopted level within a dynamic threshold.
"""

def parse_levels(f):
    r = []
    with open(f, encoding='utf-8') as fh:
        for ln in fh:
            if len(ln) >= 9 and ln[5] == ' ' and ln[7] == 'L' and ln[6] == ' ' and ln[8] == ' ':
                es = ln[9:19].strip()
                de = ln[19:21].strip()
                jp = ln[22:39].strip()
                try:
                    r.append((float(es), de, jp))
                except ValueError:
                    pass
    return r


adopted = parse_levels('A35/S35/new/S35_adopted.ens')
pd = parse_levels('A35/S35/new/S35_36s_p_d.ens')

print(f'Adopted levels: {len(adopted)}')
print(f'p_d levels:     {len(pd)}')
print()

THRESHOLD = 25  # keV baseline (p_d DE = 5-20 keV; adopted energies are precise)

matched_adopted = {}
results = []

for pd_tup in pd:
    pe, pde, pjp = pd_tup
    try:
        pde_val = int(pde)
    except (ValueError, TypeError):
        pde_val = 5
    threshold = max(THRESHOLD, 3 * pde_val)

    best_diff = threshold
    best = None
    best_idx = -1
    for i, (ae, ade, ajp) in enumerate(adopted):
        diff = abs(pe - ae)
        if diff < best_diff:
            best_diff = diff
            best = (ae, ade, ajp)
            best_idx = i

    if best_idx >= 0 and best_idx in matched_adopted:
        # Conflict: two p_d levels mapped to same adopted level - keep closer
        prev_r = matched_adopted[best_idx]
        if best_diff < prev_r['match_diff']:
            prev_r['match'] = None  # demote previous
            prev_r['match_diff'] = None
            results.append({
                'pd_e': pe, 'pd_de': pde, 'pd_jp': pjp,
                'match': best, 'match_diff': best_diff, 'match_idx': best_idx
            })
            matched_adopted[best_idx] = results[-1]
        else:
            results.append({
                'pd_e': pe, 'pd_de': pde, 'pd_jp': pjp,
                'match': None, 'match_diff': None, 'match_idx': -1
            })
    else:
        results.append({
            'pd_e': pe, 'pd_de': pde, 'pd_jp': pjp,
            'match': best, 'match_diff': best_diff if best else None, 'match_idx': best_idx
        })
        if best_idx >= 0:
            matched_adopted[best_idx] = results[-1]

# Print matched results
matched = [r for r in results if r['match']]
unmatched = [r for r in results if not r['match']]

print('=== MATCHED (p_d → Adopted) ===')
print(f"{'p_d E':>8}  {'±DE':>3}  {'Adpt E':>10}  {'Diff':>5}  {'p_d Jp':<22} {'Adpt Jp':<22}")
print('-' * 80)
for r in matched:
    ae, ade, ajp = r['match']
    diff = r['match_diff']
    print(f"{r['pd_e']:8.0f}  {r['pd_de']:>3}  {ae:10.3f}  {diff:5.1f}  {r['pd_jp']:<22} {ajp:<22}")

print()
print(f'=== NOT MATCHED in p_d (new levels, not yet in Adopted) [{len(unmatched)} levels] ===')
for r in unmatched:
    print(f"  p_d E = {r['pd_e']:6.0f} keV (±{r['pd_de']})  Jp = {r['pd_jp']}")

print()
print(f'Summary: {len(matched)} matched, {len(unmatched)} new in p_d, '
      f'{len(adopted)} total adopted levels')
