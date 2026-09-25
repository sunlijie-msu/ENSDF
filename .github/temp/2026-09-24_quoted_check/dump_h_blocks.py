#!/usr/bin/env python3
"""Dump every H-flagged level block (XREF contains H) with line numbers and
lengths, so quoted values can be reconciled against the current records.
Read-only."""
import re
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    start = None
    for i, line in enumerate(lines):
        is_L = (len(line) >= 23 and line[7:8] == 'L' and line[5:6] == ' '
                and line[6:7] == ' ' and line[0:5].strip())
        if is_L:
            if start is not None:
                emit(lines, start, i - 1)
            start = i
    if start is not None:
        emit(lines, start, len(lines) - 1)
    return 0


def emit(lines, start, end):
    bloque = lines[start:end + 1]
    tiene_h = any('XREF=' in l and re.search(r'H(?![a-z])',
                   l.split('XREF=', 1)[1]) for l in bloque if 'XREF=' in l)
    if not tiene_h:
        return
    for n in range(start, end + 1):
        print(f'{n + 1:6d} {len(lines[n]):3d} |{lines[n]}|')


if __name__ == '__main__':
    sys.exit(main())
