"""Dump a line range with lengths/pads: python block_of.py start end [start end ...]"""
import sys
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()
args = [int(a) for a in sys.argv[1:]]
for a, b in zip(args[0::2], args[1::2]):
    print(f"--- {a}-{b} ---")
    for n in range(a, b + 1):
        s = L[n - 1]
        print(f"{n:5d} len={len(s):3d} clen={len(s.rstrip()):3d} pad={len(s) - len(s.rstrip()):3d} {s.rstrip()!r}")
