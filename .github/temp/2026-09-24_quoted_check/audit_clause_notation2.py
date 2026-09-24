#!/usr/bin/env python3
"""Clauses whose |D|p value is written plain vs parenthesized.

Correct criterion: the clause value is tentative exactly when the level-scheme
parity change is tentative, i.e. when a parity symbol (+/-) of either connected
level sits INSIDE parentheses in the J field:

    `8(+)`      parity + tentative   -> clause `(yes)` / `(no)`
    `(6+)`      parity + tentative   -> clause `(yes)` / `(no)`
    `(7)-`      parity - firm        -> clause plain `no`
    `5-`, `2+`  parity firm          -> clause plain

Read-only.
"""
import re
import sys
from pathlib import Path

CLAUSE = re.compile(r'\|D\|p=\s*(\(?\s*(?:yes|no)\s*\)?)', re.I)


def parity(jpi):
    """Return (sign, tentative) for a J-pi field, or (None, None)."""
    sign = None
    tentative = False
    depth = 0
    for ch in jpi:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        elif ch in '+-':
            if sign is not None and sign != ch:
                return None, None
            sign = ch
            if depth > 0:
                tentative = True
    return sign, tentative


def main() -> int:
    path = Path(sys.argv[1])
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')

    levels = []
    for i, line in enumerate(lines):
        if len(line) >= 40 and line[5:6] == ' ' and line[6:7] == ' ' \
                and line[7:8] == 'L' and line[0:5].strip():
            try:
                levels.append((float(line[9:19]), line[22:39].strip(), i + 1))
            except ValueError:
                pass

    def closest(target):
        best, diff = None, 1.5
        for e, jpi, ln in levels:
            if abs(e - target) <= diff:
                best, diff = (e, jpi), abs(e - target)
        return best

    own = None
    bad = 0
    for i, line in enumerate(lines):
        if len(line) >= 40 and line[7:8] == 'L' and line[5:6] == ' ' and line[6:7] == ' ':
            try:
                own = float(line[9:19])
            except ValueError:
                pass
            continue
        if line[7:8] != 'G' or line[5:6] != ' ' or line[6:7] != ' ' or own is None:
            continue
        try:
            eg = float(line[9:19])
        except ValueError:
            continue
        prov = []
        for j in range(i + 1, len(lines)):
            if len(lines[j]) >= 8 and lines[j][6:7] == 'c' and lines[j][7:8] == 'G':
                prov.append(lines[j][9:].rstrip())
                continue
            break
        text = ' '.join(prov)
        hit = CLAUSE.search(text)
        if not hit or 'level scheme' not in text:
            continue
        notation = hit.group(1).replace(' ', '')
        final = closest(own - eg)
        if final is None:
            continue
        initial_jpi = next(j for e, j, ln in levels if e == own)
        _, t0 = parity(initial_jpi)
        _, t1 = parity(final[1])
        tentative = t0 or t1
        parenthesized = '(' in notation
        ok = tentative == parenthesized
        if not ok:
            bad += 1
        if tentative or not ok:
            print(f'{"WRONG NOTATION" if not ok else "ok"}  line {i+1:>5}'
                  f'  gamma {eg:>8}  clause {notation:<6}'
                  f'  initial {initial_jpi!r} -> final {final[1]!r}'
                  f'  (parity tentative={tentative})')
    print(f'\nclauses with wrong notation: {bad}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
