#!/usr/bin/env python3
"""Read-only scan: files containing '2128', with comment-line counts."""
import os
from pathlib import Path

ROOT = Path(r'd:\X\ND\ENSDF')
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv'}

rows = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        fp = Path(dirpath) / fn
        try:
            if fp.stat().st_size > 5_000_000:
                continue
            text = fp.read_text(encoding='utf-8', errors='strict')
        except Exception:
            continue
        if '2128' not in text:
            continue
        all_hits = 0
        comment_hits = 0
        for line in text.splitlines():
            if '2128' in line:
                all_hits += 1
                if len(line) > 7 and line[6] == 'c':
                    comment_hits += 1
        rows.append((comment_hits, all_hits, str(fp.relative_to(ROOT))))

rows.sort(reverse=True)
print(f'{"c-cols":>6} {"lines":>5}  file')
for c, a, p in rows:
    print(f'{c:>6} {a:>5}  {p}')
print()
print('total files:', len(rows))
