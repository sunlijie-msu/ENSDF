#!/usr/bin/env python3
"""Work list for the H-dataset cL J$ provenance sentences.

For every adopted level whose XREF lists H (24Mg(16O,a2p)g, 2005Ma03):
  adopted line, E, adopted J-pi, source J-pi (nearest source level),
  the level's cL J$ block text, and whether it already cites 2005Ma03.

Read-only.
"""
import sys
from pathlib import Path


def read(path):
    return Path(path).open(encoding='utf-8', newline='').read().split('\r\n')


def data_l(lines, i):
    line = lines[i]
    return (len(line) >= 40 and line[7:8] == 'L' and line[5:6] in ' X'
            and line[6:7] in ' X' and line[0:5].strip())


def levels(lines):
    out = []
    for i, line in enumerate(lines):
        if len(line) >= 40 and line[7:8] == 'L' and line[5:6] == ' ' \
                and line[6:7] == ' ' and line[0:5].strip():
            try:
                e = float(line[9:19])
            except ValueError:
                continue
            xref = ''
            for j in range(i + 1, min(i + 6, len(lines))):
                if data_l(lines, j) and lines[j][5:6] == 'X':
                    xref = lines[j][9:].strip()
                    break
            out.append({'line': i + 1, 'e': e, 'jpi': line[22:39].strip(),
                        'xref': xref, 'idx': i})
    return out


def j_block(lines, idx):
    """cL J$ block text for the level at index idx, or ''."""
    cand = None
    i = idx + 1
    while i < len(lines):
        line = lines[i]
        if len(line) < 10:
            break
        is_cl = line[6:7] == 'c' and line[7:8] == 'L'
        if is_cl:
            text = line[9:].rstrip()
            if cand is None:
                if 'J$' in text:
                    cand = [text.strip()]
            elif line[5:6] != ' ':
                cand.append(text.strip())
            else:
                break
        else:
            if data_l(lines, i) and lines[i][5:6] == ' ' and lines[i][6:7] == ' ':
                break  # next level
        i += 1
    return ' '.join(cand) if cand else ''


def main() -> int:
    a_lines = read(sys.argv[1])
    s_lines = read(sys.argv[2])
    a_levels = levels(a_lines)
    s_levels = levels(s_lines)

    def source(e):
        best, diff = None, 1.6
        for lv in s_levels:
            d = abs(lv['e'] - e)
            if d < diff:
                best, diff = lv, d
        return best

    rows = []
    for lv in a_levels:
        if not lv['xref']:
            continue
        letters = lv['xref'].replace('XREF=', '')
        if not any(ch.isalpha() and ch == 'H' for ch in letters):
            continue
        src = source(lv['e'])
        rows.append((lv, src, j_block(a_lines, lv['idx'])))

    print(f'H-flagged adopted levels: {len(rows)}')
    for lv, src, block in rows:
        sj = src['jpi'] if src else '?'
        se = src['e'] if src else '?'
        has = 'yes' if '2005Ma03' in block else 'no'
        print(f'--- line {lv["line"]:>5}  E={lv["e"]:<9} adopted={lv["jpi"]:<12}'
              f' source={sj!r} @ {se}  cites2005Ma03={has}')
        print(f'    {block if block else "(no cL J$ block)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
