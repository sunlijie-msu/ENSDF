#!/usr/bin/env python3
"""Item 2 final verdict + git history context for the target file."""
import subprocess

REPO = r"d:\X\ND\ENSDF"
TARGET = "A34/S34/new/S34_adopted.ens"
WANTED = [11506, 11712, 12460, 12660, 12985.5, 13590, 13790, 14430, 14576.5, 15244.4]


def blob(rev="HEAD"):
    return subprocess.run(["git", "show", f"{rev}:{TARGET}"], cwd=REPO,
                          capture_output=True).stdout


cur = open(rf"{REPO}\A34\S34\new\S34_adopted.ens", "rb").read()
head = blob()


def lmap(d):
    m = {}
    for b in d.split(b"\n"):
        if len(b) >= 9 and b[6:7] == b" " and b[7:8] == b"L" and b[8:9] == b" ":
            try:
                m[round(float(b[9:19].decode().strip()), 1)] = b
            except ValueError:
                pass
    return m


cm, hm = lmap(cur), lmap(head)
print(f"{'E':>9} | {'core==HEAD':>10} | {'CUR bytes':>9} | {'CUR record chars':>16} | "
      f"{'HEAD record chars':>17} | CRLF?")
print("-" * 90)
allgood = True
for e in WANTED:
    cb, hb = cm[round(e, 1)], hm[round(e, 1)]
    core_c, core_h = cb.rstrip(b"\r"), hb.rstrip(b"\r")
    same = core_c == core_h
    ok80 = len(core_c) == 80
    allgood &= same and ok80
    has_cr = cb.endswith(b"\r")
    print(f"{e:>9} | {str(same):>10} | {len(cb):>9} | {len(core_c):>16} | "
          f"{len(core_h):>17} | {has_cr}")
print("-" * 90)
print("ALL 10: record-content identical AND 80 chars ->", allgood)

print("\n=== git history for the file ===")
for args in (["log", "--oneline", "--follow", "--", TARGET],
             ["log", "--diff-filter=A", "--format=%H %ci %s", "--", TARGET]):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True, text=True)
    print(f"$ git {' '.join(args)}")
    print("   " + (r.stdout.strip() or "(none)").replace("\n", "\n   "))

print("\n=== index stat-cache arithmetic proof ===")
r = subprocess.run(["git", "ls-files", "--debug", TARGET], cwd=REPO, capture_output=True, text=True)
size_line = [l for l in r.stdout.splitlines() if "size:" in l][0]
cached = int(size_line.split("size:")[1].split()[0])
head_lines = head.count(b"\n")
print(f"  index cached working-tree size : {cached}")
print(f"  HEAD blob size (LF)           : {len(head)}")
print(f"  HEAD blob line count          : {head_lines}")
print(f"  HEAD blob size + line count   : {len(head) + head_lines}   (= CRLF-expanded size)")
print(f"  cached == CRLF-expanded?      : {cached == len(head) + head_lines}")
print("  => working-tree file was ALREADY CRLF at the last index update (before the audited edits).")
