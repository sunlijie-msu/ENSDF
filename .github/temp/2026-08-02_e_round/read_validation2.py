"""Extract validation summary for Cl34 file from latest terminal output."""
import glob, os, re
files = sorted(glob.glob(r"c:\Users\sun\AppData\Roaming\Code\copilot-terminal-output\copilot-terminal-output-*.txt"), key=os.path.getmtime)
p = files[-1]
t = open(p, encoding="utf-8", errors="replace").read()
print("latest:", p)
for pat in [r"EXIT_CODES[^\n]*", r"Summary: [^\n]*", r"SUCCESS: [^\n]*", r"ERROR[^\n]*"]:
    for m in re.findall(pat, t):
        print(m)
