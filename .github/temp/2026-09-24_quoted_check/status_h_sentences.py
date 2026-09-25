#!/usr/bin/env python3
"""Per-level status of the '2005Ma03' provenance sentence (read-only).

For each H-flagged level (XREF contains H) report: adopted E, adopted J|p,
source E, source J|p, the sentence's quoted J|p (if any), and whether it equals
the source J|p.
"""
import re
import sys
from pathlib import Path

MARK = 'is given by 2005Ma03'


def records(path):
    out = []
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    for i, line in enumerate(lines):
        if len(line) >= 23 and line[7:8] == 'L' and line[5:6] == ' ' \
                and line[6:7] == ' ' and line[0:5].strip():
            try:
                e = float(line[9:19].strip())
            except ValueError:
                continue
            out.append({'line': i + 1, 'E': e, 'J': line[22:40].strip()})
    return out


def h_levels(path):
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    xref, cur = {}, None
    for line in lines:
        if len(line) >= 23 and line[7:8] == 'L' and line[5:6] == ' ' \
                and line[6:7] == ' ' and line[0:5].strip():
            try:
                cur = float(line[9:19].strip())
            except ValueError:
                cur = None
        elif 'XREF=' in line and line[5:6] == 'X' and line[7:8] == 'L':
            body = line.split('XREF=', 1)[1].strip()
            if re.search(r'H(?![a-z])', body) and cur is not None:
                xref[cur] = body
    return xref


def sentences(path):
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    out = {}
    for i, line in enumerate(lines):
        if MARK not in line:
            continue
        tok = line[:line.find(MARK)].rstrip().split()[-1]
        j = i
        while j >= 0:
            if len(lines[j]) >= 23 and lines[j][7:8] == 'L' \
                    and lines[j][5:6] == ' ' and lines[j][6:7] == ' ':
                break
            j -= 1
        try:
            e = float(lines[j][9:19].strip())
        except (ValueError, IndexError):
            continue
        out[e] = (tok, i + 1)
    return out


def main() -> int:
    adopted, source = Path(sys.argv[1]), Path(sys.argv[2])
    hx, sent = h_levels(adopted), sentences(adopted)
    src = records(source)
    adop = {r['E']: r['J'] for r in records(adopted)}
    print(f'{"AdoptedE":>9}  {"AdopJpi":<12} {"SrcE":>8} {"SrcJpi":<8} '
          f'{"SENT":<7} {"OK":<5} ln')
    bad = 0
    for e in sorted(hx):
        near = min(src, key=lambda r: abs(r['E'] - e))
        tok, ln = sent.get(e, ('-', '-'))
        if tok == '-':
            flag = 'none'
        elif near['J'] == tok:
            flag = 'ok'
        else:
            flag = 'DIFF'
            bad += 1
        print(f'{e:9.1f}  {adop.get(e, "-"):<12} {near["E"]:8.1f} '
              f'{near["J"]:<8} {tok:<7} {flag:<5} {ln}')
    print(f'\nH levels: {len(hx)}   sentences: {len(sent)}   mismatches: {bad}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
