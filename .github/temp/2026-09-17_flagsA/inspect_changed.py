"""Inspect current bytes of the user-modified blocks (10408, 10447, 10482)."""
raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
for target in ("G 8279", "G 10406", "G 7142", "G 6407"):
    for ln in raw.split("\n"):
        if target in ln[:40]:
            print(f"{target}: len={len(ln)} flag_col77={ln[76]!r}  {ln!r}")
            break
for energy in ("10408", "10447", "10482"):
    for ln in raw.split("\n"):
        if ln.startswith(" 34S   L " + energy):
            print(f"L {energy}: len={len(ln)} flag_col77={ln[76]!r}  {ln!r}")
            break
