#!/usr/bin/env python3
"""Discriminate origin of CRLF in the target file."""
import subprocess, os, time
from collections import Counter

REPO = r"d:\X\ND\ENSDF"
TARGET = "A34/S34/new/S34_adopted.ens"


def eol_of(path):
    d = open(path, "rb").read()
    crlf = d.count(b"\r\n")
    lf = d.count(b"\n")
    return f"CRLF={crlf} LF_only={lf-crlf} -> {'CRLF' if crlf else ('LF' if lf else 'none')}"


print("=== EOL of files written by THIS session's create_file tool ===")
for f in ["audit_scope_check.py", "audit_data_integrity.py", "audit_eol.py"]:
    p = rf"{REPO}\.github\temp\2026-09-13_reactions\{f}"
    print(f"  {f:<26} {eol_of(p)}")

print("\n=== EOL of pre-existing helper script (prior session) ===")
p = rf"{REPO}\.github\temp\2026-09-13_reactions\find_bare.py"
print("  find_bare.py              ", eol_of(p))

print("\n=== Target file ===")
print("  S34_adopted.ens           ", eol_of(rf"{REPO}\A34\S34\new\S34_adopted.ens"))

print("\n=== Fresh checkout of target via checkout-index (applies autocrlf) ===")
outdir = rf"{REPO}\.github\temp\2026-09-13_reactions\headco"
os.makedirs(outdir, exist_ok=True)
r = subprocess.run(["git", "checkout-index", "-f", "--prefix", outdir + "/", "--", TARGET],
                   cwd=REPO, capture_output=True, text=True)
print("  rc=", r.returncode, r.stderr.strip())
fresh = os.path.join(outdir, TARGET)
if os.path.exists(fresh):
    print("  fresh checkout EOL        ", eol_of(fresh))

print("\n=== mtimes (local) ===")
for p in [rf"{REPO}\A34\S34\new\S34_adopted.ens",
          rf"{REPO}\A34\S34\new\S34_208pb_36s_34sg.ens",
          rf"{REPO}\A34\S34\new\S34_31p_a_pg.ens",
          rf"{REPO}\.github\copilot-instructions.md"]:
    print(f"  {os.path.getmtime(p):.0f} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))}  {os.path.basename(p)}")

print("\n=== EOL distribution in A34/S34/new (tracked) ===")
r = subprocess.run(["git", "ls-files", "--eol", "A34/S34/new/"], cwd=REPO, capture_output=True, text=True)
c = Counter(" ".join(l.split()[:2]) for l in r.stdout.splitlines() if l.strip())
for k, v in c.most_common():
    print(f"  {k:<20} {v}")

print("\n=== git stash / reflog top ===")
for cmd in [["git", "stash", "list"], ["git", "reflog", "-n", "3"]]:
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    print(f"  $ {' '.join(cmd)}")
    print("   ", (r.stdout or "(empty)").strip().replace("\n", "\n    "))
