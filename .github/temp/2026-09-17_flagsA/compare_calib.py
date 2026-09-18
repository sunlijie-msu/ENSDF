"""Compare column_calibrate ERROR/detail items: git HEAD vs current working file."""
import re
import subprocess
import sys

def calib(path):
    r = subprocess.run([sys.executable, r".github/scripts/column_calibrate.py", path],
                       capture_output=True)
    out = (r.stdout or b"").decode("gbk", errors="replace")
    items = []
    for ln in out.split("\n"):
        if ("ERROR" in ln or "LINE " in ln or "WARN" in ln) and "USE --fix" not in ln:
            items.append(ln.strip())
    return r.returncode, items

head = subprocess.run(["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
                      capture_output=True)
tmp = r".github/temp/2026-09-17_flagsA/head_copy.ens"
open(tmp, "wb").write(head.stdout)

rc_old, old_items = calib(tmp)
rc_new, new_items = calib(r"A34/S34/new/S34_adopted.ens")
print("HEAD rc:", rc_old, "| current rc:", rc_new)
print("\n=== items ONLY in HEAD ===")
for x in old_items:
    if x not in new_items:
        print(x)
print("\n=== items ONLY in current ===")
for x in new_items:
    if x not in old_items:
        print(x)
print("\nHEAD items:", len(old_items), " current items:", len(new_items))
