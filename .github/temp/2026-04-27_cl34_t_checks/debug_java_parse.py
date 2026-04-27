import json
import re
import subprocess
from pathlib import Path

PY = r"C:\Users\sun\AppData\Local\Programs\Python\Python311\python.exe"
JAVA = r".github\scripts\Java_Average.py"

recs = json.loads(Path('.github/temp/2026-04-27_cl34_t_checks/cl34_t_blocks.json').read_text(encoding='utf-8'))
for rec in recs:
    l = rec.get('L')
    if not l:
        continue
    if l['line'] != 172:
        continue

    payload = ' '.join(x['text'][9:].rstrip() for x in rec['block'])
    print('PAYLOAD:')
    print(payload)
    print('-' * 80)

    p = subprocess.run([PY, JAVA, '--comment', payload], capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = p.stdout + '\n' + p.stderr
    print('RET', p.returncode)
    print(out)

    m = re.search(r'suggested adopted result:\s*(?P<v>[0-9]+(?:\.[0-9]+)?)\((?P<unc>[0-9]+)\)\s*(?P<u>[A-Za-z]+)', out, re.IGNORECASE)
    print('MATCH:', bool(m), m.groupdict() if m else None)
