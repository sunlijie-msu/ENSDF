"""Probe dump: print repr of each line in probe.txt."""
from pathlib import Path

p = Path(".github/temp/2026-09-16_ggP_J_M/probe.txt")
for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
    print(f"{i}: len={len(ln):3d} {ln!r}")
