"""Dump exact bytes of the Unicode-bearing lines in S34_adopted.ens (read-only)."""
import io

F = r"A34\S34\new\S34_adopted.ens"
with io.open(F, newline="", encoding="utf-8") as fh:
    lines = fh.read().replace("\r\n", "\n").split("\n")
for n in (12, 13, 14, 15):
    l = lines[n - 1]
    print("%-3d len=%d  %s" % (n, len(l), ascii(l)))
