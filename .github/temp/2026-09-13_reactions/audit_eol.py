#!/usr/bin/env python3
"""Definitive line-ending + content comparison (pure subprocess, no shell pipe)."""
import subprocess

REPO = r"d:\X\ND\ENSDF"
TARGET = "A34/S34/new/S34_adopted.ens"


def blob_bytes(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout


def stats(label, d):
    crlf = d.count(b"\r\n")
    lf = d.count(b"\n")
    cr = d.count(b"\r")
    print(f"{label:<28} bytes={len(d):>8}  CRLF={crlf:>6}  LF_total={lf:>6}  "
          f"LF_only={lf - crlf:>5}  CR_total={cr:>6}")


cur = open(rf"{REPO}\A34\S34\new\S34_adopted.ens", "rb").read()
head = blob_bytes("HEAD", TARGET)

print("=== Line-ending census (raw bytes) ===")
stats("WORKING TREE (current)", cur)
stats("HEAD blob", head)

print("\n=== git ls-files --eol (working dir, .ens sample) ===")
r = subprocess.run(["git", "ls-files", "--eol", "*.ens"], cwd=REPO, capture_output=True, text=True)
lines = r.stdout.splitlines()
print(f"total .ens tracked: {len(lines)}")
from collections import Counter
c = Counter(" ".join(l.split()[:2]) for l in lines)
for k, v in c.most_common():
    print(f"  {k:<22} {v}")
print("  --- sample of S34/A34 files ---")
for l in lines:
    if "S34" in l or "A34/" in l:
        print("   ", l)

print("\n=== Target file eol record ===")
r = subprocess.run(["git", "ls-files", "--eol", TARGET], cwd=REPO, capture_output=True, text=True)
print(r.stdout.strip())

print("\n=== Content comparison of the 10 L-records (cols 1-80, CR stripped) ===")
WANTED = [11506, 11712, 12460, 12660, 12985.5, 13590, 13790, 14430, 14576.5, 15244.4]


def level_map(d):
    m = {}
    for b in d.split(b"\n"):
        if len(b) >= 9 and b[6:7] == b" " and b[7:8] == b"L" and b[8:9] == b" ":
            try:
                e = round(float(b[9:19].decode().strip()), 1)
            except ValueError:
                continue
            m[e] = b
    return m


cm, hm = level_map(cur), level_map(head)
ok = True
for e in WANTED:
    k = round(e, 1)
    cb, hb = cm.get(k), hm.get(k)
    ccore = cb.rstrip(b"\r\n")
    hcore = hb.rstrip(b"\r\n")
    same_core = ccore == hcore
    has_cr = cb.endswith(b"\r")
    ok &= same_core
    print(f"E={e:<9} core_identical={same_core!s:<5} "
          f"cur_has_CR={has_cr!s:<5} cur_core_len={len(ccore)} head_core_len={len(hcore)}")
print("\nALL 10 CONTENT-CORE IDENTICAL:", ok)
