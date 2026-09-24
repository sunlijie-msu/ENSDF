#!/usr/bin/env python3
"""Audit cL J$ comment quotations.

Checks that every quoted level energy is followed by the word 'level'
(or that the quotation uses 'g.s.' instead of an energy).

Read-only helper for the comment-quoted-values-check workflow.

Usage:
    python audit_cL_level_suffix.py <file.ens> [dump_line_number]
"""
import re
import sys
from pathlib import Path


def blocks(path):
    """Yield (start_line, merged_text) for each merged cL J$ comment block."""
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    out, buf, start = [], [], None
    for i, ln in enumerate(lines, 1):
        is_comment = len(ln) > 7 and ln[6] == 'c' and ln[7] == 'L'
        if not is_comment:
            if buf:
                out.append((start, ' '.join(buf)))
                buf, start = [], None
            continue
        text = ln[9:].strip()
        if ln[5] == ' ' and 'J$' in ln[:12]:          # new cL J$ block
            if buf:
                out.append((start, ' '.join(buf)))
            buf, start = [text], i
        elif buf:                                      # 2cL, 3cL, ... continuation
            buf.append(text)
    if buf:
        out.append((start, ' '.join(buf)))
    return out


# Quotation form: <direction> <J-pi>, <level energy> [level]
QPAT = re.compile(
    r'\b(to|from)\s+'
    r'(?P<jpi>[0-9/()+\-, ]{1,24}?)\s*,\s*'
    r'(?P<level>g\.s\.|[0-9][0-9.]*)'
    r'(?P<suffix>\s*(?:level|resonance|state)?)'
)


def main():
    path = sys.argv[1]
    hits = []
    for line_no, text in blocks(path):
        for m in QPAT.finditer(text):
            hits.append((line_no, m.group(1), m.group('jpi').strip(),
                         m.group('level'), m.group('suffix').strip()))

    print(f'quotations found: {len(hits)}')
    print('--- quotations whose quoted energy lacks the "level" suffix ---')
    missing = [h for h in hits if not h[4] and h[3] != 'g.s.']
    for line_no, direction, jpi, lev, _ in missing:
        print(f'  line {line_no}: {direction} {jpi}, {lev}')
    print(f'missing-suffix count: {len(missing)}')

    print('--- all quotations ---')
    for line_no, direction, jpi, lev, suffix in hits:
        tag = 'OK  ' if (suffix or lev == 'g.s.') else 'MISS'
        print(f'  {tag} line {line_no}: {direction} {jpi}, {lev} {suffix}'.rstrip())

    lines = None
    for arg in sys.argv[2:]:
        want = int(arg)
        if lines is None:
            lines = Path(path).read_text(encoding='utf-8').splitlines()
        print(f'--- raw lines around {want} ---')
        for i in range(want - 1, want + 4):
            if 0 < i <= len(lines):
                print(f'  L{i} len={len(lines[i - 1])} {lines[i - 1]!r}')


if __name__ == '__main__':
    main()
