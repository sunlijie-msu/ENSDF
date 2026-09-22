import re
import subprocess
import sys

TMP = r"d:\X\ND\ENSDF\.github\temp\quoted_check"
ERR = TMP + r"\sim_errors.txt"

p = subprocess.run([sys.executable, r"d:\X\ND\ENSDF\.github\scripts\check_quoted_values.py",
                    TMP + r"\simulated.ens"], capture_output=True, text=True)
out = p.stdout + p.stderr
out = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", out)
open(ERR, "w", encoding="utf-8").write(out)
print("errors captured ->", ERR)

sim = open(TMP + r"\simulated.ens", "rb").read().decode("ascii").split("\r\n")
orig = open(r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens", "rb").read().decode("ascii").split("\r\n")
# map: simulated line -> original line
shift = 0
sim2orig = {}
i = j = 0
adds = {512, 756, 868, 901}
while i < len(sim) and j < len(orig):
    sim2orig[i + 1] = j + 1
    if (j + 1) in adds and sim[i][6:8] == "cL" and sim[i + 1][5:6] == "2":
        i += 2
        j += 1
        continue
    i += 1
    j += 1
print("sim lines", len(sim), "orig lines", len(orig))
for m in re.finditer(r"#(\d+) \[(\w+)\]  line (\d+)\n(.*)\n(.*)", out):
    n = int(m.group(3))
    print(f"#{m.group(1)} {m.group(2)} sim{n} orig{sim2orig.get(n)}: {m.group(4).strip()} | {m.group(5).strip()}")
