"""Inventory every `2 L WIDTH*` continuation record: parent level, XREF, T field, block comments."""
from pathlib import Path

LINE = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " "


hits = [i for i, s in enumerate(LINE, 1) if s[7:8] == "L" and "WIDTH" in s]
print(f"total 2 L WIDTH* records = {len(hits)}\n")

for h in hits:
    # parent L record
    p = next(j for j in range(h, 0, -1) if is_lrec(LINE[j - 1]))
    ls = LINE[p - 1]
    # XREF line
    xr = ""
    for j in range(p + 1, h):
        if LINE[j - 1][5:6] == "X" and "XREF" in LINE[j - 1]:
            xr = LINE[j - 1].rstrip()
            break
    print(f"--- rec line {h:5d} | L {p} E={ls[9:19].strip():9s} J={ls[22:39].strip():10s} T={ls[39:49]!r} DT={ls[49:55]!r}")
    print(f"    XREF: {xr}")
    print(f"    REC : {LINE[h-1].rstrip()!r}")
    # comments of this level (c-record lines before the first G/F record)
    for j in range(p + 1, len(LINE) + 1):
        s = LINE[j - 1]
        if is_lrec(s):
            break
        if s[7:8] in ("G", "F", "S") and s[6:7] == " " or (s[6:7] != "c" and s[7:8] in ("G", "F", "S")):
            break
        if s[6:7] == "c":
            print(f"    c   {j:5d} {s.rstrip()!r}")
    print()
