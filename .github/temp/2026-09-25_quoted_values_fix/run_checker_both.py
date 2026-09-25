"""Run the project quoted-values checker on both adopted files and print summaries."""
import io
import os
import subprocess
import sys

FILES = [r"A34\Cl34\new\Cl34_adopted.ens", r"A34\S34\new\S34_adopted.ens"]
PY = sys.executable
for f in FILES:
    print("=" * 90)
    print("CHECK", os.path.basename(f))
    print("=" * 90)
    p = subprocess.run([PY, r".github\scripts\check_quoted_values.py", f],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in (p.stdout or "").splitlines():
        if any(k in line for k in ("ERRORS", "RESULT", "Level quotes", "ERRORS:")):
            print("  ", line.strip())
    print("   exit code:", p.returncode)
