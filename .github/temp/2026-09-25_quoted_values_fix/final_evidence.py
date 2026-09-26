"""Final evidence: working-tree diff of the two adopted files (comment-only proof)
plus ASCII status. Read-only."""
import io
import os
import subprocess
import sys

REPO = r"D:\X\ND\ENSDF"
FILES = [r"A34\S34\new\S34_adopted.ens", r"A34\Cl34\new\Cl34_adopted.ens"]

for f in FILES:
    print("=" * 92)
    print("FILE", os.path.basename(f))
    print("=" * 92)
    p = subprocess.run(["git", "-C", REPO, "diff", "--unified=0", "--", f.replace("\\", "/")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    changed = [l for l in (p.stdout or "").splitlines()
               if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    print("   changed lines:", len(changed))
    for l in changed[:12]:
        print("     ", l[:100])
    if len(changed) > 12:
        print("      ... (%d more)" % (len(changed) - 12))
    n = 0
    with io.open(os.path.join(REPO, f), newline="", encoding="utf-8") as fh:
        for i, line in enumerate(fh.read().replace("\r\n", "\n").split("\n"), 1):
            if any(ord(c) > 126 for c in line):
                n += 1
                print("   NON-ASCII line %d" % i)
    print("   non-ASCII lines:", n)
    print()
