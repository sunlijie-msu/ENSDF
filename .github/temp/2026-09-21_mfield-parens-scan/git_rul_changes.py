"""Read-only: find every commit whose diff removed or edited a comment line
mentioning RUL (i.e. RUL clauses that were stripped or added)."""
import re
import subprocess

REPO = r"d:\X\ND\ENSDF"
PATH = "A34/S34/new/S34_adopted.ens"
OUT = r"d:\X\ND\ENSDF\.github\temp\2026-09-21_mfield-parens-scan\git_rul_changes.txt"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True,
                          text=True, encoding="utf-8",
                          errors="replace").stdout


log = git("log", "--reverse", "--format=%H|%ad|%s", "--date=short", "-p",
          "--", PATH)
blocks = re.split(r"\n(?=[0-9a-f]{40}\|)", log)
out = []
for b in blocks:
    head = b.split("\n", 1)[0]
    if "|" not in head:
        continue
    h, d, subj = head.split("|", 2)
    minus = [l for l in b.split("\n") if l.startswith("-") and "RUL" in l]
    plus = [l for l in b.split("\n") if l.startswith("+") and "RUL" in l]
    if minus:
        out.append("=== %s %s %s" % (h[:8], d, subj[:70]))
        out.append("  removed RUL lines: %d   added RUL lines: %d"
                   % (len(minus), len(plus)))
        for l in minus:
            out.append("  - %s" % l[1:].rstrip())
        for l in plus:
            out.append("  + %s" % l[1:].rstrip())
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print("commit-blocks with RUL removals:", out.count("removed RUL lines") if 0
      else sum(1 for l in out if "removed RUL lines" in l))
print("->", OUT)
