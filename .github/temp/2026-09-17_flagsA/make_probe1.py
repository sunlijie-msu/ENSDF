"""Create probe1.ens: a scratch copy of the exact 10447 block for pipeline tests."""
P = r".github/temp/2026-09-17_flagsA/probe1.ens"
line1 = " 34S   L 10447     5" + " " * 56 + "A   "
line2 = " 34S X L XREF=L" + " " * 65
line3 = " 34S  d" + " " * 73
assert len(line1) == 80 and len(line2) == 80 and len(line3) == 80
open(P, "w", encoding="utf-8", newline="").write(line1 + "\r\n" + line2 + "\r\n" + line3 + "\r\n")
print("written", P)
print("line1 repr:", repr(line1))
