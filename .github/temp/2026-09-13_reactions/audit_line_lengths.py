#!/usr/bin/env python3
"""Item 3: compare column_calibrate.py short/long complaints: current vs HEAD."""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(r"d:\X\ND\ENSDF")
TARGET = "A34/S34/new/S34_adopted.ens"
SCRIPT = REPO / ".github" / "scripts" / "column_calibrate.py"
TEMPDIR = REPO / ".github" / "temp" / "2026-09-13_reactions"
ISSUE_RE = re.compile(r"^\s*Line\s+(\d+):\s*(.*?)\s*\((short by|long by)\s+(\d+)\)")


def run_calibrate(path):
    r = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                       cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout + r.stderr, r.returncode


def issues(text):
    out = []
    for line in text.splitlines():
        m = ISSUE_RE.match(line)
        if m:
            out.append((int(m.group(1)), m.group(2), m.group(3), int(m.group(4)), line.strip()))
    return out


cur_path = REPO / TARGET
head_lf = TEMPDIR / "head_check_lf.ens"
head_crlf = TEMPDIR / "head_check_crlf.ens"

blob = subprocess.run(["git", "show", f"HEAD:{TARGET}"], cwd=REPO, capture_output=True).stdout
head_lf.write_bytes(blob)
head_crlf.write_bytes(blob.replace(b"\n", b"\r\n"))

cases = [("CURRENT (working tree)", cur_path),
         ("HEAD (LF, as stored in git blob)", head_lf),
         ("HEAD (CRLF, line-ending-normalized)", head_crlf)]

results = {}
for label, p in cases:
    text, rc = run_calibrate(p)
    iss = issues(text)
    results[label] = iss
    print("=" * 78)
    print(f"{label}   rc={rc}")
    print(f"  short/long issue count: {len(iss)}")
    for ln, desc, kind, n, raw in iss:
        print(f"    {raw}")

print("\n" + "=" * 78)
print("DIFF ANALYSIS: current issues vs HEAD-CRLF issues")
cur = {(d, k, n) for _, d, k, n, _ in results["CURRENT (working tree)"]}
hc = {(d, k, n) for _, d, k, n, _ in results["HEAD (CRLF, line-ending-normalized)"]}
extra = cur - hc
missing = hc - cur
print(f"  current issue signatures : {len(cur)}")
print(f"  HEAD(CRLF) signatures    : {len(hc)}")
print(f"  ADDITIONAL in current    : {len(extra)}")
for x in sorted(extra):
    print("    + ", x)
print(f"  present in HEAD not cur  : {len(missing)}")
for x in sorted(missing):
    print("    - ", x)
print()
print("RESULT:", "PASS (no additional short/long lines)" if not extra else "FAIL (additional issues present)")
