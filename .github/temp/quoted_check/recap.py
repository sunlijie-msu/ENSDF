import re
import subprocess
import sys

TMP = r"d:\X\ND\ENSDF\.github\temp\quoted_check"
TGT = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
b = open(TGT, "rb").read()
print("bytes:", len(b), "CRLF:", b.count(b"\r\n"), "LF:", b.count(b"\n"))
lines = b.decode("ascii").split("\r\n")
print("lines:", len(lines), " >80:", [(i + 1, len(l)) for i, l in enumerate(lines) if len(l) > 80])

p = subprocess.run([sys.executable, r"d:\X\ND\ENSDF\.github\scripts\check_quoted_values.py", TGT],
                   capture_output=True, text=True)
out = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", p.stdout + p.stderr)
open(TMP + r"\errors_clean2.txt", "w", encoding="utf-8").write(out)
tail = [l for l in out.splitlines() if "ERRORS:" in l or "RESULT:" in l]
print("\n".join(tail))
blocks = sorted(set(int(x) for x in re.findall(r"\]  line (\d+)", out)))
print("blocks with errors:", len(blocks))
print(blocks)
