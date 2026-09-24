#!/usr/bin/env python3
"""Read-only independent enumeration of quoted level energies in cL J$ blocks.

Verification aid for the compliance audit. Writes nothing.
"""
import re
import sys
from pathlib import Path

LIVE = Path(r'd:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens')


def parse_levels(path):
    """Return list of (energy_float, e_field_str, line_no)."""
    levels = []
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if len(line) < 19:
            continue
        if line[0:5].strip() == '':
            continue
        if line[5] == ' ' and line[6] == ' ' and line[7] == 'L':
            e = line[9:19].strip()
            if not e:
                continue
            try:
                levels.append((float(e), e, i))
            except ValueError:
                pass
    return levels


def collect_cL_blocks(path):
    """Return list of (block_start_line, owner_level_line, [text,...])."""
    lines = path.read_text(encoding='utf-8').splitlines()
    blocks = []
    owner = None          # line number of nearest preceding data L-record
    cur = None
    for i, line in enumerate(lines, 1):
        if len(line) < 10:
            continue
        col6, col7, col8 = line[5], line[6], line[7]
        if col6 == ' ' and col7 == ' ' and col8 == 'L' and line[0:5].strip():
            owner = i
            continue
        is_cL = col7 == 'c' and col8 == 'L' and line[0:5].strip() != ''
        if is_cL:
            text = line[9:80]
            if 'J$' in text:
                if cur:
                    blocks.append(cur)
                cur = [i, owner, [text]]
            elif cur is not None:
                cur[2].append(text)
            else:
                pass
        else:
            if cur is not None:
                blocks.append(cur)
                cur = None
    if cur:
        blocks.append(cur)
    return blocks


QUOTE = re.compile(
    r'\b(?:to|from)\s+'
    r'(?P<jpi>[0-9/()+, \-]{1,24}?)\s*,\s*'
    r'(?P<level>g\.s\.|\d+(?:\.\d+)?)'
    r'(?:-keV)?'
    r'(?P<suffix>\s+(?:level|resonance)\b)?')


def nearest(levels, value, window=1.0):
    best = None
    bd = window
    for e, s, ln in levels:
        d = abs(e - value)
        if d <= bd:
            bd = d
            best = (e, s, ln)
    return best


def main():
    levels = parse_levels(LIVE)
    blocks = collect_cL_blocks(LIVE)
    print(f'Live file: {LIVE}')
    print(f'Parsed L-records: {len(levels)}')
    print(f'cL J$ blocks: {len(blocks)}')

    total = 0
    gs_cases = []
    mismatches = []
    no_level = []
    for start, owner, texts in blocks:
        full = re.sub(r'\s+', ' ', ' '.join(t.strip() for t in texts))
        for m in QUOTE.finditer(full):
            total += 1
            lvl = m.group('level')
            ctx = m.group(0).strip(' ,;')
            if lvl == 'g.s.':
                gs_cases.append((start, owner, ctx))
                continue
            value = float(lvl)
            hit = nearest(levels, value)
            if hit is None:
                no_level.append((start, owner, lvl, ctx))
                continue
            if hit[1] != lvl:
                mismatches.append((start, owner, lvl, hit[1], hit[2], ctx))

    print()
    print(f'TOTAL quoted level energies: {total}')
    print(f'g.s. cases: {len(gs_cases)}')
    for s, o, c in gs_cases:
        print(f'   g.s. @block line {s} (owner L line {o}): {c}')
    print()
    print(f'LEVEL_NOT_FOUND (no L within 1.0 keV): {len(no_level)}')
    for s, o, lvl, c in no_level:
        print(f'   line {s}: "{lvl}"  ctx={c}')
    print()
    print(f'STRING MISMATCHES: {len(mismatches)}')
    for s, o, lvl, actual, lno, c in mismatches:
        print(f'   block line {s}: quoted "{lvl}" vs L-E="{actual}" '
              f'(L line {lno})  ctx={c}')

    # List every quoted level energy string with its match, for evidence
    print()
    print('--- full enumeration ---')
    idx = 0
    for start, owner, texts in blocks:
        full = re.sub(r'\s+', ' ', ' '.join(t.strip() for t in texts))
        for m in QUOTE.finditer(full):
            idx += 1
            lvl = m.group('level')
            if lvl == 'g.s.':
                print(f'#{idx} blk{start} owner{owner}  "{lvl}"  OK(g.s.)  '
                      f'ctx={m.group(0).strip(" ,;")}')
            else:
                hit = nearest(levels, float(lvl))
                tag = 'OK' if (hit and hit[1] == lvl) else 'MISMATCH'
                print(f'#{idx} blk{start} owner{owner}  "{lvl}" -> '
                      f'"{hit[1] if hit else None}" [{tag}]  '
                      f'ctx={m.group(0).strip(" ,;")}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
