"""Compact probe: locate pre-existing ordering jump and failing calibration section."""
import re
import subprocess
import sys

P = r"A34/S34/new/S34_adopted.ens"
txt = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

print("--- ordering check (consecutive L energies) ---")
prev = None
for i, ln in enumerate(txt, 1):
    if len(ln) >= 80 and ln[6:7] == " " and ln[7:8] == "L":
        e = ln[9:19].strip()
        try:
            v = float(e)
        except ValueError:
            continue
        if prev and v < prev[1]:
            print(f"DESC: line {prev[0]} E={prev[1]} -> line {i} E={v}")
        prev = (i, v)

print("--- calibration probe ---")
r = subprocess.run([sys.executable, r".github/scripts/column_calibrate.py", P],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
out = (r.stdout or "") + (r.stderr or "")
print("exit:", r.returncode)
lines = out.splitlines()
print("total output lines:", len(lines))
for j in range(0, min(60, len(lines))):
    print(f"{j:4d}| {lines[j]}")
