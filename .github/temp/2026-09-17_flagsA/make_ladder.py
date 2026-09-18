"""Build a run-length ladder probe: 5 lines, runs of 20/30/40/50/56 spaces before 'A'."""
P = r".github/temp/2026-09-17_flagsA/probeLadder.ens"
lines = []
for run in (20, 30, 40, 50, 56):
    head = f"RUN{run:02d}"
    prefix = head + "Z" * (76 - run - len(head))
    assert len(prefix) == 76 - run, (run, len(prefix))
    line = prefix + " " * run + "A" + "   "
    assert len(line) == 80
    lines.append(line)
open(P, "w", encoding="utf-8", newline="").write("\r\n".join(lines) + "\r\n")
print("written", P)
for ln in lines:
    print(repr(ln))
