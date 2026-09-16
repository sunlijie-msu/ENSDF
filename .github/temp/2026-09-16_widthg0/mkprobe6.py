"""Build probe6.txt with exact padding to test the shrink/delete recipes."""
from pathlib import Path

p = Path(".github/temp/2026-09-16_widthg0/probe6.txt")
lines = [
    " 34S X L XREF=NPSW" + " " * 115,
    " 34S  cL E$weighted average of 8383 {I16} from {+32}S(t,p), 8385.41 {I6} from" + " " * 3,
    " 34S X L XREF=NPSW(8511*)" + " " * 164,
    " 34S  cL E$weighted average of 8496 {I16} from {+32}S(t,p), 8506.77 {I4} from" + " " * 3,
    " 34S 2 L WIDTHG0=3.6 EV 7" + " " * 55,
    " 34S   G 9639      4" + " " * 60,
]
p.write_text("\n".join(lines) + "\n", encoding="utf-8")
for i, s in enumerate(lines, 1):
    print(i, len(s), len(s.rstrip()), repr(s[:30]))
