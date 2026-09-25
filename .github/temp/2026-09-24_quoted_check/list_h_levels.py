#!/usr/bin/env python3
"""List adopted levels whose XREF contains H, with source (2005Ma03) J-pi.

Read-only. Prints one row per H-flagged level:
  adopted line, E(level), adopted J-pi, source J-pi, cL J$ block text,
  whether the block already cites 2005Ma03.
"""
import re
import sys
from pathlib import Path


def levels(path):
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    out = []
    for i, line in enumerate(lines):
        if len(line) >= 40 and line[7:8] == 'L' and line[5:6] == ' ' \
                and line[6:7] == ' ' and line[0:5].strip():
            try:
                e = float(line[9:19])
            except ValueError:
                continue
            xref = ''
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j][7:8] == 'L' and lines[j][5:6] == 'X':
                    xref = lines[j][9:].rstrip()
                    break
            out.append({'line': i + 1, 'e': e, 'jpi': line[22:39].strip(),
                        'xref': xref, 'idx': i})
    return lines, out


def j_block(lines, idx):
    """Return the cL J$ block text following the L-record at index idx."""
    texts = []
    for j in range(idx + 1, len(lines)):
        line = lines[j]
        if len(line) < 10:
            break
        if line[6:7] == 'c' and line[7:8] == 'L':
            text = line[9:]
            if texts or 'J$' in text:
                if 'J$' in text or line[5:6] != ' ':
                    texts.append(text.strip())
                    continue
            break
        if line[7:8] in 'LG' and line[6:7] in ' X' and line[5:6] in ' XdF':
            break
        if texts and line[7:8] != 'c':
            break
    return ' '.join(texts)


def main() -> int:
    adopted = Path(sys.argv[1])
    source = Path(sys.argv[2])
    a_lines, a_levels = levels(adopted)
    _, s_levels = levels(source)

    src = {round(l['e'], 1): l['jpi'] for l in s_levels}
    src_by_100 = {round(l['e'], 0): l['jpi'] for l in s_levels}

    rows = []
    for lv in a_levels:
        if 'H' not in lv['xref'] or not re.search(r'\bH', lv['xref']):
            continue
        block = j_block(a_lines, lv['idx'])
        s = src.get(round(lv['e'], 1), src_by_100.get(round(lv['e'], 0), ''))
        rows.append((lv, s, block))

    print(f'H-flagged adopted levels: {len(rows)}')
    print(f'{"ln":>5} {"E(level)":>10}  {"adopted":<12} {"source(2005Ma03)":<16}'
          f' {"cL J$?":<7} {"cites 2005Ma03?":<16}')
    for lv, s, block in rows:
        print(f'{lv["line"]:>5} {lv["e"]:>10}  {lv["jpi"]:<12} {s:<16}'
              f' {"yes" if block else "NO":<7}'
              f' {"yes" if "2005Ma03" in block else "no":<16}')
    print()
    for lv, s, block in rows:
        print(f'--- line {lv["line"]}  E={lv["e"]}  adopted={lv["jpi"]!r}'
              f'  source={s!r}  XREF={lv["xref"][:60]}')
        print(f'    {block}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
