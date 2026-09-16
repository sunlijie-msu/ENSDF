from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " "


for n in range(1208, 1213):
    s = L[n - 1]
    print(n, repr(s[:14]), "| s5:", repr(s[5:6]), "s6:8:", repr(s[6:8]), "s7:8:", repr(s[7:8]), "is_lrec:", is_lrec(s))
