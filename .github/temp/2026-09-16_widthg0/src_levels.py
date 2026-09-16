"""Show how each resonance dataset records widths: T field + comments mentioning |G."""
from pathlib import Path

files = [
    "A34/S34/new/S34_30si_a_g_a_n_resonances.ens",
    "A34/S34/new/S34_33s_n_g_n_n_resonances.ens",
]


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


for f in files:
    L = Path(f).read_text(encoding="utf-8").splitlines()
    print(f"\n===== {f} =====")
    for i, s in enumerate(L, 1):
        if is_lrec(s):
            e, j, t, dt = s[9:19].strip(), s[22:39].strip(), s[39:49].strip(), s[49:55].strip()
            comments = []
            for k in range(i + 1, len(L) + 1):
                c = L[k - 1]
                if is_lrec(c):
                    break
                if c[6:8] in ("cL", "2c", "3c") and "|G" in c:
                    comments.append(f"{k}:{c.rstrip()[9:]}")
            show = t or dt or comments
            if show:
                print(f"  L{i:5d} E={e:9s} J={j:9s} T={t:9s} DT={dt:6s} {' || '.join(comments)}")
