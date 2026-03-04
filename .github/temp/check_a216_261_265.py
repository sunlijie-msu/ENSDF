from pathlib import Path
import re

updates = {216: 'NDS 209, 409 (2026)', 261: 'NDS 209, 499 (2026)', 265: 'NDS 209, 499 (2026)'}

text = Path('ENSDF_Mass_Chain_Evaluations.md').read_text(encoding='utf-8')
for ln in text.splitlines():
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit() and int(p[0]) in updates:
        a = int(p[0])
        print(f'A={a}:')
        print(f'  Markdown:  "{p[1]}"')
        print(f'  NNDC now:  "{updates[a]}"')
        print(f'  DOI:       "{p[2]}"')
        print(f'  Authors:   "{p[3]}"')
        print()
