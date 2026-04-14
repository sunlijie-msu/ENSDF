"""
Level matching: S35_36s_p_d.ens <-> S35_adopted.ens
Adds Jp-compatibility check and reverse mapping (adopted levels with no p_d match).
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
                    r.append({'e': float(es), 'de': de, 'jp': jp})
                except ValueError:
                    pass
    return r


def jp_compatible(jp1, jp2):
    """Very permissive check: flag only clear parity opposites with no overlap."""
    if not jp1 or not jp2:
        return True
    # Strip parentheses for core parity check
    def has_plus(jp): return '+' in jp
    def has_minus(jp): return '-' in jp
    # If one is explicitly positive and other explicitly negative (no ambiguity), flag
    p1_plus = has_plus(jp1); p1_minus = has_minus(jp1)
    p2_plus = has_plus(jp2); p2_minus = has_minus(jp2)
    # If both have only one definite parity and they're opposite: incompatible
    if p1_plus and not p1_minus and p2_minus and not p2_plus:
        return False
    if p1_minus and not p1_plus and p2_plus and not p2_minus:
        return False
    return True


adopted = parse_levels('A35/S35/new/S35_adopted.ens')
pd = parse_levels('A35/S35/new/S35_36s_p_d.ens')

THRESHOLD = 25  # keV

matched_adopted_idx = {}  # adopted_idx -> result dict
results = []

for pd_lvl in pd:
    pe = pd_lvl['e']
    pde = pd_lvl['de']
    pjp = pd_lvl['jp']
    try:
        pde_val = int(pde)
    except (ValueError, TypeError):
        pde_val = 5
    threshold = max(THRESHOLD, 3 * pde_val)

    best_diff = threshold
    best = None
    best_idx = -1
    for i, alv in enumerate(adopted):
        diff = abs(pe - alv['e'])
        if diff < best_diff:
            best_diff = diff
            best = alv
            best_idx = i

    r = {
        'pd_e': pe, 'pd_de': pde, 'pd_jp': pjp,
        'match': best, 'match_diff': best_diff if best else None,
        'match_idx': best_idx,
        'jp_ok': jp_compatible(pjp, best['jp']) if best else None
    }

    # Conflict resolution: two p_d -> same adopted
    if best_idx >= 0 and best_idx in matched_adopted_idx:
        prev_r = matched_adopted_idx[best_idx]
        if best_diff < prev_r['match_diff']:
            prev_r['match'] = None
            prev_r['match_diff'] = None
            prev_r['match_idx'] = -1
            prev_r['jp_ok'] = None
            del matched_adopted_idx[best_idx]
            results.append(r)
            matched_adopted_idx[best_idx] = r
        else:
            r['match'] = None
            r['match_diff'] = None
            r['match_idx'] = -1
            r['jp_ok'] = None
            results.append(r)
    else:
        results.append(r)
        if best_idx >= 0:
            matched_adopted_idx[best_idx] = r

matched = [r for r in results if r['match']]
unmatched = [r for r in results if not r['match']]

print('=' * 100)
print('LEVEL MATCHING: S35_36s_p_d.ens → S35_adopted.ens')
print('=' * 100)
print(f"\n{'p_d E':>8}  {'±':>2}  {'Adpt E':>10}  {'Δ':>5}  {'Jp-OK':>5}  "
      f"{'p_d Jp':<22} {'Adopted Jp':<22}")
print('-' * 88)

jp_flag_count = 0
for r in matched:
    alv = r['match']
    diff = r['match_diff']
    flag = '  OK ' if r['jp_ok'] else '  !! '
    if not r['jp_ok']:
        jp_flag_count += 1
    print(f"{r['pd_e']:8.0f}  {r['pd_de']:>2}  {alv['e']:10.3f}  {diff:5.1f}  {flag}  "
          f"{r['pd_jp']:<22} {alv['jp']:<22}")

print()
print(f"Jp-compatibility warnings: {jp_flag_count}")
print()
print(f'{"="*60}')
print(f'NEW IN p_d — NOT IN ADOPTED ({len(unmatched)} levels):')
print(f'{"="*60}')
for r in unmatched:
    # Find nearest adopted for context
    nearest_diff = 999
    nearest_e = None
    for alv in adopted:
        d = abs(r['pd_e'] - alv['e'])
        if d < nearest_diff:
            nearest_diff = d
            nearest_e = alv['e']
    de_str = str(r['pd_de']) if r['pd_de'] else ''
    jp_str = str(r['pd_jp']) if r['pd_jp'] else ''
    ne_str = f"{nearest_e:.1f}" if nearest_e is not None else "N/A"
    print(f"  p_d {r['pd_e']:6.0f} (\u00b1{de_str:>2})  Jp={jp_str:<22}  "
          f"(nearest adopted: {ne_str}, \u0394={nearest_diff:.0f})")

# Reverse: adopted levels with no p_d match
matched_adpt_set = set(r['match_idx'] for r in matched)
print()
print(f'{"="*60}')
print(f'ADOPTED LEVELS WITH NO p_d MATCH ({len(adopted) - len(matched_adpt_set)} levels):')
print(f'{"="*60}')
for i, alv in enumerate(adopted):
    if i not in matched_adpt_set:
        # Find nearest p_d for context
        nearest_diff = 999
        nearest_e = None
        for pd_lvl in pd:
            d = abs(alv['e'] - pd_lvl['e'])
            if d < nearest_diff:
                nearest_diff = d
                nearest_e = pd_lvl['e']
        print(f"  Adopted {alv['e']:8.3f}  Jp={alv['jp']:<22}  "
              f"(nearest p_d: {nearest_e:.0f}, Δ={nearest_diff:.0f})")

print()
print(f'Summary: {len(pd)} p_d levels, {len(matched)} matched to adopted, '
      f'{len(unmatched)} new in p_d, {len(adopted) - len(matched_adpt_set)} adopted with no p_d match.')
