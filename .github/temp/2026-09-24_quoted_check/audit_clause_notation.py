#!/usr/bin/env python3
"""Contingency table: clause notation vs J-pi firmness of the two levels.

For every `|D|p=X from level scheme.` clause, records whether the value is
written plain (`yes`) or parenthesized (`(yes)`), and whether either level's
J-pi is fully firm (no parentheses anywhere in the J field).

Read-only.
"""
import re
import sys
from collections import Counter
from pathlib import Path

CLAUSE = re.compile(r'\|D\|p=\s*(\(?\s*(?:yes|no)\s*\)?)', re.I)


def firm(jpi):
    return '(' not in jpi and ')' not in jpi


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
    table = Counter()
    detail = []
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
        hit = CLAUSE.search(' '.join(prov))
        if not hit or 'level scheme' not in ' '.join(prov):
            continue
        notation = hit.group(1).replace(' ', '')
        final = closest(own - eg)
        if final is None:
            continue
        initial_jpi = next(j for e, j, ln in levels if e == own)
        not_firm = (not firm(initial_jpi)) or (not firm(final[1]))
        table[('parenthesized' if '(' in notation else 'plain',
               'Jpi not firm' if not_firm else 'Jpi firm')] += 1
        if not_firm:
            detail.append((i + 1, eg, notation, initial_jpi, final[1]))

    print(f'== {path}')
    for key in sorted(table):
        print(f'   {key[0]:<14} {key[1]:<13} {table[key]}')
    print('   --- clauses whose level J-pi is not fully firm:')
    for ln, eg, notation, ij, fj in detail:
        print(f'       line {ln:>5}  gamma {eg:>8}  {notation:<6}'
              f'  {ij!r} -> {fj!r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
