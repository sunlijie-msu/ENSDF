"""Run column_calibrate and show header summary + any explicit error lines."""
import subprocess, sys

r = subprocess.run([sys.executable, r".github/scripts/column_calibrate.py",
                    r"A34/S34/new/S34_adopted.ens"],
                   capture_output=True)
out = (r.stdout or b"").decode("gbk", errors="replace") + "\n" + (r.stderr or b"").decode("gbk", errors="replace")
lines = out.split("\n")
print("exit code:", r.returncode)
print("=== first 40 lines ===")
for ln in lines[:40]:
    print(ln)
err = [ln for ln in lines if any(k in ln for k in ("ERROR", "INVALID", "WRONG"))]
print("=== explicit error lines:", len(err))
for ln in err[:30]:
    print(ln)
print("=== positioning detail ===")
for ln in lines:
    if any(k in ln for k in ("ERROR", "positioning", "LINE ", "Line:", "Column", "off by", "shift", "WARN")):
        print(ln)
