import json
import subprocess
from pathlib import Path

PY = r"C:\Users\sun\AppData\Local\Programs\Python\Python311\python.exe"
JAVA = r".github\scripts\Java_Average.py"

recs = json.loads(Path('.github/temp/2026-04-27_cl34_t_checks/cl34_t_blocks.json').read_text(encoding='utf-8'))
for rec in recs:
    l = rec.get('L')
    if not l or l['line'] != 374:
        continue

    payload = ' '.join(x['text'][9:].rstrip() for x in rec['block'])
    print('PAYLOAD:')
    print(payload)
    print('-' * 100)

    proc = subprocess.run([PY, JAVA, '--comment', payload], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('RETURN:', proc.returncode)
    print(proc.stdout)
    if proc.stderr.strip():
        print('STDERR:')
        print(proc.stderr)
