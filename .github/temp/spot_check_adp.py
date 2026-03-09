"""5% random spot-check of the 224 modified cG RI$from lines in adp.
For each sampled line, look up the mrg and verify the Other: value is correct."""

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'
import random
random.seed(42)

adp_lines = open(ADP_FILE, encoding='utf-8').readlines()
mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()

# Collect all modified lines (has Other: and is a cG RI$from line)
modified = [(i+1, adp_lines[i].rstrip()) for i in range(len(adp_lines))
            if ('cG RI$from 1977Da02' in adp_lines[i] or 'cG RI$from 1983Wa27' in adp_lines[i])
            and 'Other' in adp_lines[i]]

print(f"Total modified lines: {len(modified)}")
sample_size = max(11, int(len(modified) * 0.05))
sample = random.sample(modified, sample_size)
print(f"Spot-checking {sample_size} samples (5% = {0.05*len(modified):.1f})\n")

# Build mrg lookup: list of (adopted_E, {dataset_letter: (ri, dri)})
def build_mrg_lookup(mrg_lines):
    result = []
    current_e = None
    current_ds = {}
    for ml in mrg_lines:
        l = ml.rstrip('\n')
        if l.startswith(' GAMMA-'):
            if current_e is not None and current_ds:
                result.append((current_e, dict(current_ds)))
            current_ds = {}
            current_e = None
            idx = l.find(' 34CL  G')
            if idx >= 0:
                try:
                    current_e = float(l[idx+9:idx+19].strip())
                except:
                    pass
        elif l.startswith(' LEVEL') or l.startswith('-----'):
            if current_e is not None and current_ds:
                result.append((current_e, dict(current_ds)))
            current_e = None
            current_ds = {}
        elif current_e is not None and len(l) > 47 and l[39:47] == ' 34CL  G':
            tag = l[22:35]
            if '--->A' in tag:
                current_ds['A'] = (l[60:68].strip(), l[68:70].strip())
            elif '--->B' in tag:
                current_ds['B'] = (l[60:68].strip(), l[68:70].strip())
    if current_e is not None and current_ds:
        result.append((current_e, dict(current_ds)))
    return result

mrg_list = build_mrg_lookup(mrg_lines)

def find_best(e_float, tolerance=2.0):
    best, best_d = None, tolerance
    for (me, ds) in mrg_list:
        d = abs(me - e_float)
        if d < best_d:
            best_d = d; best = (me, ds)
    return best

def expected_other(ri, dri, name):
    if not ri:
        return None
    if dri == 'LT': return f'. Other: <{ri} ({name}).'
    if dri == 'GT': return f'. Other: >{ri} ({name}).'
    if dri:          return f'. Other: {ri} {{I{dri}}} ({name}).'
    return f'. Other: {ri} ({name}).'

def find_prev_G(adp_lines, line_idx_1based):
    for j in range(line_idx_1based-2, max(line_idx_1based-12, -1), -1):
        l = adp_lines[j]
        if len(l) >= 8 and l[5] == ' ' and l[6] == ' ' and l[7] == 'G':
            return l[9:19].strip()
    return None

pass_count = fail_count = 0
for (lnum, content) in sample:
    g_e_str = find_prev_G(adp_lines, lnum)
    if g_e_str is None:
        print(f"SKIP L{lnum}: no preceding G record found")
        continue
    try:
        g_e = float(g_e_str)
    except:
        print(f"SKIP L{lnum}: non-numeric G energy '{g_e_str}'")
        continue

    # Determine source and other
    if 'from 1977Da02' in content:
        other_letter, other_name = 'B', '1983Wa27'
    else:
        other_letter, other_name = 'A', '1977Da02'

    mrg_entry = find_best(g_e)
    if mrg_entry is None:
        print(f"FAIL L{lnum} G{g_e}: No mrg entry. Content: {content}")
        fail_count += 1
        continue
    mrg_e, ds = mrg_entry
    if other_letter not in ds:
        print(f"FAIL L{lnum} G{g_e}: Other dataset not in mrg. Content: {content}")
        fail_count += 1
        continue
    ri, dri = ds[other_letter]
    expected = expected_other(ri, dri, other_name)
    if expected is None:
        print(f"FAIL L{lnum} G{g_e}: Expected no Other but content has it. mrg RI='{ri}'. Content: {content}")
        fail_count += 1
        continue

    # Check that content ends with expected
    ok = content.endswith(expected.rstrip('.')) or content.endswith(expected)
    # extract what's in content after 'from ...'
    if 'from 1977Da02' in content:
        actual_suffix = content.split('from 1977Da02')[1]
    else:
        actual_suffix = content.split('from 1983Wa27')[1]
    expected_suffix = expected

    if actual_suffix == expected_suffix:
        print(f"PASS L{lnum} G{g_e}: {actual_suffix.strip()} [mrg_E={mrg_e}, diff={abs(g_e-mrg_e):.2f}]")
        pass_count += 1
    else:
        print(f"FAIL L{lnum} G{g_e}:")
        print(f"  Actual:   {repr(actual_suffix)}")
        print(f"  Expected: {repr(expected_suffix)}")
        fail_count += 1

print(f"\n{'='*50}")
print(f"RESULTS: {pass_count} PASS, {fail_count} FAIL out of {pass_count+fail_count}")
if fail_count == 0:
    print("ALL SPOT CHECKS PASSED ✓")
else:
    print(f"FAILURES DETECTED — investigate and fix!")
