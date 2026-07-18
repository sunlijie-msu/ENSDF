"""15% random spot-check for level energy cross-check."""
import re, random

random.seed(42)

# Get T1 data
t1_levels = {}
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_I.md', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or 'none' in line or '---' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 11:
            continue
        ei = parts[1]
        if ei and ei != '0':
            try:
                key = round(float(ei.split('(')[0]))
                if key not in t1_levels:
                    t1_levels[key] = ei
            except:
                pass

# Get ENSDF data
ensdf = {}
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if len(l) >= 9 and l[5:6] == ' ' and l[6:7] == ' ' and l[7:8] == 'L':
        e = l[9:19].strip()
        de = l[19:21].strip()
        if e:
            try:
                key = round(float(e))
                ensdf[key] = (e, de, i + 1)
            except:
                pass

# Pick 30 random samples
t1_list = [(k, t1_levels[k]) for k in sorted(t1_levels)]
sample = random.sample(t1_list, min(30, len(t1_list)))
sample.sort()

print("SPOT-CHECK RESULTS (30 samples, 15%):")
print(f"{'Key':>5s}  {'T1 E':<16s}  {'ENSDF E':<12s}  {'DE':>4s}  {'Line':>5s}  Result")
print("-" * 70)
all_ok = 0
issues = 0

for key, t1e in sample:
    if key in ensdf:
        ee, de, ln = ensdf[key]
        m = re.match(r'([\d.]+)\s*\((\d+)\)', t1e)
        t1v = float(m.group(1)) if m else None
        t1u = int(m.group(2)) if m else None
        t1dp = len(m.group(1).split('.')[1]) if m and '.' in m.group(1) else 0

        ev = float(ee)
        edp = len(ee.split('.')[1]) if '.' in ee else 0
        eu = int(de) if de else None

        ok = True
        msgs = []
        if t1v is not None and abs(t1v - ev) > 0.02:
            msgs.append("VAL:{}vs{}".format(t1v, ev))
            ok = False
        if t1u != eu:
            msgs.append("UNC:{}vs{}".format(t1u, eu))
            ok = False
        if t1dp != edp:
            msgs.append("DP:{}vs{}".format(t1dp, edp))
            ok = False

        if ok:
            all_ok += 1
            print("{:5d}  {:<16s}  {:<12s}  {:>4s}  L{:<5d}  OK".format(key, t1e, ee, de, ln))
        else:
            issues += 1
            print("{:5d}  {:<16s}  {:<12s}  {:>4s}  L{:<5d}  MISMATCH: {}".format(key, t1e, ee, de, ln, "; ".join(msgs)))
    else:
        print("{:5d}  {:<16s}  NOT IN ENSDF".format(key, t1e))

print()
print("Results: {} OK, {} issues out of {}".format(all_ok, issues, len(sample)))
