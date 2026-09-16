"""Print HEAD version of selected line range (read-only) for block reconstruction."""
import subprocess
from pathlib import Path

out = subprocess.run(
    ["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
    capture_output=True, text=True, encoding="utf-8",
).stdout.splitlines()

with open(".github/temp/2026-09-16_widthg0/head_block.txt", "w", encoding="utf-8") as fh:
    for i in range(1515, 1528):
        s = out[i - 1]
        line = f"{i:5d} len={len(s):3d} clen={len(s.rstrip()):3d} pad={len(s)-len(s.rstrip()):3d} {s.rstrip()!r}"
        print(line)
        fh.write(line + "\n")
