#!/usr/bin/env python3
"""Build the edit plan for appending the 2005Ma03 provenance sentence.

For each target level: last line of its cL J$ block, the id for a new
continuation line, a short unique anchor taken from the start of the following
line, and the sentence to append.

Read-only.
"""
import sys
from pathlib import Path

SENT = 'is given by 2005Ma03 in {+24}Mg({+16}O,|a2p|g).'
IDS = ' 23456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

TARGETS = [
    (8371.0, '7-'), (8503.7, '6+'), (8734.8, '6-'), (8970.6, '6-'),
    (9413.8, '6'), (10399.8, '8-'), (11374.2, '8+'), (11807.4, '8+'),
    (12985.4, '(9+)'), (13320.2, '(9-)'), (13960.5, '(10+)'), (15281.0, '(10)'),
]


def main() -> int:
    path = Path(sys.argv[1])
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    text = '\n'.join(lines)

    def anchor_for(i):
        line = lines[i]
        head = line[:9]
        rest = line[9:80]
        out = ''
        run = 0
        for ch in rest:
            if ch == ' ':
                run += 1
                if run >= 2:
                    break
            else:
                run = 0
            out += ch
        return (head + out).rstrip()

    for e, jpi in TARGETS:
        idx = None
        for i, line in enumerate(lines):
            if len(line) >= 40 and line[7:8] == 'L' and line[5:6] == ' ' \
                    and line[6:7] == ' ' and line[0:5].strip():
                try:
                    if abs(float(line[9:19]) - e) < 0.01:
                        idx = i
                        break
                except ValueError:
                    continue
        if idx is None:
            print(f'!! level {e} not found')
            continue
        # J$ block: first cL comment containing J$, plus its continuations
        start = None
        i = idx + 1
        while i < len(lines):
            line = lines[i]
            if len(line) < 10:
                break
            is_cl = line[6:7] == 'c' and line[7:8] == 'L'
            if is_cl:
                if start is None:
                    if 'J$' in line[9:]:
                        start = i
                elif line[5:6] == ' ':
                    break
                elif not (('J$' in line[9:]) or True):
                    break
            elif start is not None:
                break
            i += 1
        last = i - 1
        if start is None or last < start:
            print(f'!! level {e}: no J$ block found')
            continue
        ids = IDS
        cid = ' '
        for j in range(start, last + 1):
            cid = lines[j][5:6]
        new_id = ids[ids.index(cid) + 1] if cid in ids else '?'
        nxt = last + 1
        anchor = anchor_for(nxt)
        cnt = text.count(anchor)
        prefix = f' 34S {new_id}cL ' if new_id != ' ' else ' 34S  cL '
        body = f'{jpi} {SENT}'
        newline = prefix + body
        if len(newline) > 80:
            print(f'!! level {e}: sentence too long ({len(newline)})')
        newline = newline + ' ' * (80 - len(newline))
        print(f'=== level {e} (block lines {start + 1}..{last + 1},'
              f' last id {cid!r} -> new id {new_id!r})')
        print(f'    last line: {lines[last][:70]!r}')
        print(f'    next line {nxt + 1}: {lines[nxt][:70]!r}')
        print(f'    anchor (hits={cnt}): {anchor!r}')
        print(f'    NEW: {newline!r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
