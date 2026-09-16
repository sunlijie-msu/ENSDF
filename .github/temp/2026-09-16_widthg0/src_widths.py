"""List all WIDTH* records with their parent level energy in the two resonance datasets."""
from pathlib import Path

files = [
    "A34/S34/new/S34_30si_a_g_a_n_resonances.ens",
    "A34/S34/new/S34_33s_n_g_n_n_resonances.ens",
]


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


for f in files:
    L = Path(f).read_text(encoding="utf-8").splitlines()
    print(f"\n===== {f}  ({len(L)} lines) =====")
    for i, s in enumerate(L, 1):
        if s[7:8] == "L" and "WIDTH" in s and s[5:6] == "2":
            p = next(j for j in range(i, 0, -1) if is_lrec(L[j - 1]))
            ls = L[p - 1]
            print(f"  L{p:5d} E={ls[9:19].strip():9s} J={ls[22:39].strip():9s} T={ls[39:55].strip():12s} | rec {i:5d}: {s.rstrip()!r}")
