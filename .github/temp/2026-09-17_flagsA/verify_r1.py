"""Verify R1: the 9 lines are clean (no A, len 80) and no '@' remains file-wide."""
raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
print("'@' occurrences:", raw.count("@"))
for lev in ("10447", "10528", "10617", "10869", "10895", "10917", "11180", "11194", "11289"):
    for ln in raw.split("\n"):
        if ln.startswith(" 34S   L " + lev):
            ok = len(ln) == 80 and ln[76] == " "
            print(("OK  " if ok else "BAD ") + f"{lev}: len={len(ln)} col77={ln[76]!r}")
            break
