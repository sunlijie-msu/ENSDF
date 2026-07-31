#!/usr/bin/env python3
"""Debug script to see what quoted refs are extracted from J$ comments."""
import sys
import re
sys.path.insert(0, r'd:\X\ND\ENSDF\.github\scripts')
from check_quoted_values import extract_quoted_refs, parse_levels, parse_gammas, verify, find_closest_level, find_closest_gamma
from pathlib import Path

fp = Path(r"d:\X\ND\ENSDF\XUNDL\A58\Fe58\old\Fe58_adopted.ens")

# Parse data
levels = parse_levels(fp)
gammas = parse_gammas(fp)
print(f"Levels: {len(levels)}, Gammas: {len(gammas)}")

# Extract refs
refs = extract_quoted_refs(fp)
print(f"\nExtracted {len(refs)} quoted references:\n")

for i, ref in enumerate(refs, 1):
    print(f"--- Ref #{i} (line {ref.line_num}) ---")
    print(f"  Gamma:      {ref.gamma_energy_str} keV")
    print(f"  MULT:       {ref.multipolarity}")
    print(f"  Direction:  {ref.direction}")
    print(f"  Level:      {ref.level_energy_str} keV = {ref.level_energy}")
    print(f"  Jpi:        '{ref.jpi}'")
    print(f"  Context:    {ref.context}")
    print()

# Verify
findings = verify(refs, levels, gammas, 1.0)
print(f"\nFindings: {len(findings)}")
for f in findings:
    print(f"  [{f.code}] line {f.line}: {f.message}")
    print(f"    Context: {f.context}")
