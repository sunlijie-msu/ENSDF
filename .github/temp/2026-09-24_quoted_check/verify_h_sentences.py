#!/usr/bin/env python3
"""Verify every '2005Ma03' provenance sentence against the source H dataset.

Read-only. For each adopted level whose cL J$ block contains
'<Jpi> is given by 2005Ma03 in {+24}Mg({+16}O,|a2p|g).', compare <Jpi> with the
J|p of the nearest-energy L-record in the source dataset.
"""
import re
import sys
from pathlib import Path

SENT = re.compile(r'(\S+) is given by 2005Ma03 in \{?\+?24\}?Mg')


def levels(path):
    out = []
    for line in path.open(encoding='utf-8', newline='').read().split('\r\n'):
        if len(line) >= 23 and line[7:8] == 'L' and line[5:6] == ' ' \
                and line[6:7] == ' ' and line[0:5].strip():
            txt = line[9:19].strip()
            if not txt:
                continue
            try:
                e = float(txt)
            except ValueError:
                continue
            out.append((e, line[22:40].strip()))
    return out


def sentences(path):
    """Yield (adopted level energy, quoted Jpi, line number) for each sentence."""
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    out = []
    for i, line in enumerate(lines):
        if len(line) >= 10 and line[6:7] == 'c':
            m = SENT.search(line[9:])
            if not m:
                m = SENT.search(line[5:])
            if m:
                # nearest preceding L-record
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
                out.append((e, m.group(1), i + 1, lines[j][22:40].strip()))
    return out


def main() -> int:
    adopted = Path(sys.argv[1])
    source = Path(sys.argv[2])
    src = levels(source)
    rows = sentences(adopted)
    print(f'{"Adopted E":>10} {"Adopted Jpi":<12} {"Source E":>9} {"Src Jpi":<10} '
          f'{"Sentence Jpi":<13} {"MATCH":<6} line')
    bad = 0
    for e, jpi, ln, adjpi in sorted(rows):
        near = min(src, key=lambda t: abs(t[0] - e))
        if abs(near[0] - e) > 1.5:
            match = 'NO-SRC'
            bad += 1
        elif near[1] != jpi:
            match = 'DIFF'
            bad += 1
        else:
            match = 'ok'
        print(f'{e:10.1f} {adjpi:<12} {near[0]:9.1f} {near[1]:<10} '
              f'{jpi:<13} {match:<6} {ln}')
    print(f'\nsentences: {len(rows)}   problems: {bad}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
