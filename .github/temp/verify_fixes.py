"""Verify all blank-DOI fixes and run DOI integrity scan."""
import urllib.request
import json
import re
from pathlib import Path

text = Path('ENSDF_Mass_Chain_Evaluations.md').read_text(encoding='utf-8')
lines = text.splitlines()

# Check the 7 fixed rows
fixed_targets = {76, 77, 101, 108, 117, 165, 224}
print('=== Verification of fixed rows ===')
for ln in lines:
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit() and int(p[0]) in fixed_targets:
        a, cite, doi, auth = int(p[0]), p[1], p[2], p[3]
        status = 'FIXED' if doi and doi != '' else 'STILL BLANK'
        print(f'  A={a:4d}: [{status}] doi={doi[:60]}')

# Remaining blank DOI rows
print()
print('=== Remaining blank-DOI rows ===')
for ln in lines:
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit():
        a, cite, doi, auth = int(p[0]), p[1], p[2], p[3]
        if not doi:
            print(f'  A={a:4d}: cite={cite}')

# Full DOI syntax scan
print()
print('=== Full DOI syntax scan ===')
issues = []
rows = []
for ln in lines:
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit():
        a, cite, doi, auth = int(p[0]), p[1], p[2], p[3]
        rows.append((a, doi))

for a, doi in rows:
    if not doi:
        continue
    ok_prefix = doi.startswith('https://doi.org/')
    suffix = doi.replace('https://doi.org/', '', 1)
    space_in = ' ' in doi
    paren_mismatch = suffix.count('(') != suffix.count(')')
    if not ok_prefix or space_in or paren_mismatch:
        issues.append({'A': a, 'doi': doi, 'reason': 'syntax'})

if issues:
    print(f'  SYNTAX ISSUES: {len(issues)}')
    for issue in issues:
        print(f'    A={issue["A"]}: {issue["doi"]}')
else:
    print(f'  No syntax issues found. Scanned {len([r for r in rows if r[1]])} DOIs.')
