#!/usr/bin/env python3
"""Audit the working-tree diff of a .ens file.

Fails if any changed line is not a comment record (col 7 = 'c', col 8 = 'L').
Reports the column count of every changed comment line so unwrapped lines are
visible rather than silently accepted.
"""
import subprocess
import sys
from pathlib import Path


def changed_lines(path: str):
    diff = subprocess.run(
        ['git', 'diff', '--unified=0', '--', path],
        capture_output=True, text=True, check=True).stdout
    for line in diff.splitlines():
        if line.startswith(('+++', '---', '@@', 'diff ', 'index ')):
            continue
        if line[:1] in ('+', '-'):
            yield line[0], line[1:]


def main() -> int:
    path = sys.argv[1]
    bad = []
    comments = []
    for kind, text in changed_lines(path):
        text = text.rstrip('\r\n')
        if text[:1] == '\\':
            continue
        is_comment = text[6:7] == 'c' and text[7:8] == 'L'
        if is_comment:
            comments.append((kind, len(text), text))
        else:
            bad.append((kind, text[:40]))

    print(f'changed comment lines: {len(comments)}')
    widths = sorted({w for _, w, _ in comments})
    print(f'comment line widths seen: {widths}')
    for kind, width, text in comments:
        flag = '' if width <= 80 else '  <-- OVER 80'
        print(f'  {kind} {width:>3}{flag} {text!r}')
    print(f'non-comment changed lines: {len(bad)}')
    for kind, text in bad[:20]:
        print('   ', kind, repr(text))
    ok = not bad
    print('RESULT:', 'comment-only diff OK' if ok else 'DATA RECORD CHANGED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
