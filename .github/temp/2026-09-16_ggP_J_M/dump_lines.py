"""Read-only dump: exact target L/G lines, J and M field contents, plus source extents.

Usage: python .github/temp/2026-09-16_ggP_J_M/dump_lines.py
"""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")

# 1-based line numbers located by grep (L records then their G records)
L_LINES = [763, 866, 985, 1047, 1118, 1303]
G_LINES = [768, 873, 991, 1054, 1122, 1307]

rows = TARGET.read_text(encoding="utf-8").splitlines()
print("=== TARGET: L records ===")
for n in L_LINES:
    s = rows[n - 1]
    print(f"{n:5d} len={len(s):3d} J=[{s[22:39]}] E=[{s[9:19]}] DE=[{s[19:21]}] flag77=[{s[76:77]}]")
    print(f"      repr: {s!r}")

print("=== TARGET: G records ===")
for n in G_LINES:
    s = rows[n - 1]
    print(f"{n:5d} len={len(s):3d} E=[{s[9:19]}] DE=[{s[19:21]}] RI=[{s[22:29]}] DRI=[{s[29:31]}] M=[{s[32:41]}]")
    print(f"      repr: {s!r}")
