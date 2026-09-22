"""Run checker -> planner -> simulation verification in one shot."""
import hashlib
import re
import subprocess
import sys

ROOT = r"d:\X\ND\ENSDF"
TGT = ROOT + r"\A34\S34\new\S34_adopted.ens"
TMP = ROOT + r"\.github\temp\quoted_check"
CHK = ROOT + r"\.github\scripts\check_quoted_values.py"

sha = hashlib.sha1(open(TGT, "rb").read()).hexdigest()[:12]
print("target sha:", sha)

p = subprocess.run([sys.executable, CHK, TGT], capture_output=True, text=True)
out = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", p.stdout + p.stderr)
open(TMP + r"\errors_live.txt", "w", encoding="utf-8").write(out)
print([l for l in out.splitlines() if "ERRORS:" in l])

r = subprocess.run([sys.executable, TMP + r"\plan4.py"], capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    print(r.stderr.strip())
    sys.exit(r.returncode)

p2 = subprocess.run([sys.executable, CHK, TMP + r"\simulated.ens"], capture_output=True, text=True)
out2 = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", p2.stdout + p2.stderr)
open(TMP + r"\sim_errors.txt", "w", encoding="utf-8").write(out2)
print("SIM:", [l for l in out2.splitlines() if "ERRORS:" in l or "RESULT:" in l])
if "ERRORS: 0" not in out2:
    for m in re.finditer(r"#(\d+) \[(\w+)\]  line (\d+)\n(.*)\n(.*)", out2):
        print(f"  #{m.group(1)} {m.group(2)} line {m.group(3)}: {m.group(4).strip()} | {m.group(5).strip()}")
