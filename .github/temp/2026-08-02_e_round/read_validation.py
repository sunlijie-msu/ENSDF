"""Read latest terminal output and show validation summary."""
import glob
import os
import re

files = sorted(
    glob.glob(r"c:\Users\sun\AppData\Roaming\Code\copilot-terminal-output\copilot-terminal-output-*.txt"),
    key=os.path.getmtime,
)
p = files[-1]
print("latest:", p)
t = open(p, encoding="utf-8", errors="replace").read()
for pat in [r"EXIT_CODES[^\n]*", r"Summary: [^\n]*", r"ERROR[^\n]*", r"SUCCESS: [^\n]*", r"Energy positioning errors: [^\n]*"]:
    for m in re.findall(pat, t):
        print(m)
