#!/usr/bin/env python3
"""Read-only: compare SKILL.md error table against checker-emitted codes."""
import ast
import re
from pathlib import Path

skill = Path(r'd:\X\ND\ENSDF\.github\skills\comment-quoted-values-check\SKILL.md').read_text(encoding='utf-8')
src = Path(r'd:\X\ND\ENSDF\.github\scripts\check_quoted_values.py').read_text(encoding='utf-8')

tree = ast.parse(src)
codes = set()
for n in ast.walk(tree):
    if isinstance(n, ast.Call):
        for kw in n.keywords:
            if kw.arg == 'code' and isinstance(kw.value, ast.Constant):
                codes.add(kw.value.value)

# skill table rows: "| `CODE` | SEVERITY | ..."
tbl = {}
for line in skill.splitlines():
    m = re.match(r'\|\s*`([A-Z_]+)`\s*\|\s*(ERROR|WARNING)\s*\|', line)
    if m:
        tbl[m.group(1)] = m.group(2)

print('script codes :', sorted(codes))
print('skill table  :', sorted(tbl))
print('in script, not in skill table:', sorted(codes - set(tbl)))
print('in skill table, not in script:', sorted(set(tbl) - codes))
print()
print('skill mentions level designator:', 'designator' in skill)
print('skill mentions resonance designator:', 'resonance' in skill)
print('script accepts resonance designator:', 'resonance' in src)
print('skill exit-code lines:')
for line in skill.splitlines():
    if 'Exit codes' in line or 'exit' in line.lower():
        print('   ', line.strip())
print('script exit calls:')
for i, line in enumerate(src.splitlines(), 1):
    if 'sys.exit' in line:
        print(f'    {i}: {line.strip()}')
