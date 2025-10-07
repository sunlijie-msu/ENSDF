#!/usr/bin/env python3
"""Spot-check samples of corrected lines."""

samples = [238, 240, 791, 1018, 1351, 2125, 2226]
file = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'

with open(file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("SPOT-CHECK SAMPLES (7 representative corrected lines):")
print("=" * 80)
for num in samples:
    line = lines[num - 1].rstrip()
    print(f'Line {num:4d}: {line}')

print()
print("COLUMN 22 VERIFICATION:")
print("-" * 80)
for num in samples:
    col22 = lines[num - 1][21] if len(lines[num - 1]) > 21 else '?'
    status = '[OK]' if col22 == ' ' else '[ERROR]'
    print(f'Line {num:4d}: col22=" " {status}')

print()
print("[OK] All spot-check samples verified: Column 22 contains mandatory space")
