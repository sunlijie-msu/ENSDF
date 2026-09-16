"""Read-only: check HEAD values for WIDTHG0 and hunt provenance for 7781.22 and 11024.95."""
import re
import subprocess
from pathlib import Path

print("=== HEAD version WIDTHG0 records ===")
try:
    out = subprocess.run(
        ["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout
    for i, s in enumerate(out.splitlines(), 1):
        if "WIDTHG0" in s:
            print(f"HEAD {i:5d} {s.rstrip()!r}")
except Exception as exc:  # pragma: no cover
    print("git show failed:", exc)

print("\n=== individual datasets: levels 7781/7784, 11024/11025, and widths near 1.7 / 0.57 ===")
pats = [r"1102[45]", r"778[14]", r"1\.7\s*e?V", r"0\.57\s*e?V", r"57\s*e?V\b"]
for f in sorted(Path("A34/S34/new").glob("*.ens")):
    if "adopted" in f.name:
        continue
    for i, s in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for p in pats:
            if re.search(p, s, re.IGNORECASE):
                print(f"{f.name}:{i}: {s.rstrip()!r}")
                break
