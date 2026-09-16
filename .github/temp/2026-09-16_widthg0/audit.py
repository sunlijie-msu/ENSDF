"""Independent re-audit: random 15% source trace of the converted width values (check-only)."""
import random
import re
from pathlib import Path

WORK = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()
SRC_L = Path("A34/S34/new/S34_30si_a_g_a_n_resonances.ens").read_text(encoding="utf-8")
SRC_Q = Path("A34/S34/new/S34_33s_n_g_n_n_resonances.ens").read_text(encoding="utf-8")
L_ENERGIES = {"10494", "10587", "10625", "10670", "10790", "11088", "11142", "11165", "11220", "11233",
              "11315", "11323", "11358", "11372", "11381", "11420", "11545", "11643"}


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


levels = {}
for i, s in enumerate(WORK, 1):
    if is_lrec(s):
        level = s[9:19].strip()
        block = []
        for j in range(i + 1, len(WORK) + 1):
            t = WORK[j - 1]
            if is_lrec(t):
                break
            if t[6:8] == "cL" and "|G{" in t:
                block.append(t.rstrip())
        if block:
            levels[level] = block

random.seed(7781)
sample = random.sample(sorted(levels), 6)
print("random sample (15%):", sample)
all_ok = True
for lev in sample:
    src = SRC_L if lev in L_ENERGIES else SRC_Q
    mine = " ".join(levels[lev])
    values = re.findall(r"=([\d.]+)|>([\d.]+)|<([\d.]+)|, \|G\S+?=([\d.]+)", mine)
    tokens = [t for group in values for t in group if t]
    missing = [t for t in tokens if t not in src]
    ok = not missing
    all_ok &= ok
    print(f"{'PASS' if ok else 'FAIL'} {lev:9s} values={tokens} missing={missing}")
    print(f"     adopted: {mine[:110]}")
print("source trace:", "all sampled values found in source datasets" if all_ok else "MISMATCH")
