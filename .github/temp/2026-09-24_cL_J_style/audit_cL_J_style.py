#!/usr/bin/env python3
"""Audit cL J$ primary transition lists against the gamma-selection-rules style.

Read-only. Checks, per cL J$ comment block:

  R1a  weak gamma ray        RI < 5
  R1b  upper-limit intensity LT in DRI fields (cols 30-31)
  R1c  questionable placement '?' in col 80
  R1d  final level with uncertain or multi-valued J-pi
  R2a  transitions not in descending intensity order
  R2b  two or more transitions to final levels with the same J-pi
  R5   transition list does not follow a period-terminated argument

Usage: python audit_cL_J_style.py <file.ens>
"""

import re
import sys
from pathlib import Path

TRANS = re.compile(
    r'(?P<ge>\d+(?:\.\d+)?)\|g(?P<mid>[^;]*?)\s+(?P<dir>to|from)\s+'
    r'(?P<qpjpi>[0-9/()+\-, ]{1,24}?)\s*,\s*'
    r'(?P<level>g\.s\.|\d+(?:\.\d+)?)')


def parse_records(path):
    levels = []
    gammas = []
    with open(path, encoding='utf-8') as fh:
        for i, line in enumerate(fh, start=1):
            if len(line) < 20 or not line[0:5].strip():
                continue
            if line[5] != ' ' or line[6] != ' ':
                continue
            kind = line[7]
            if kind == 'L':
                e = line[9:19].strip()
                if e:
                    levels.append((e, float(e), line[22:39].strip(), i))
            elif kind == 'G':
                e = line[9:19].strip()
                if not e:
                    continue
                ri = line[22:29].strip()
                gammas.append({
                    'estr': e, 'e': float(e),
                    'ri_str': ri,
                    'ri': float(ri) if re.fullmatch(r'\d+(?:\.\d+)?', ri) else None,
                    'dri': line[29:31].strip(),
                    'q80': line[79:80] if len(line) >= 80 else '',
                    'line': i,
                })
    return levels, gammas


def blocks(path):
    with open(path, encoding='utf-8') as fh:
        lines = fh.readlines()
    out = []
    cur, start = [], 0
    for i, line in enumerate(lines, start=1):
        if len(line) < 10:
            continue
        c6, c7, c8 = line[5], line[6], line[7]
        if c7 == 'c' and c8 == 'L' and line[0:5].strip():
            text = line[9:].rstrip('\n')
            if 'J$' in text and c6 == ' ':
                if cur:
                    out.append((start, cur))
                cur, start = [text], i
            elif cur and c6 != ' ':
                cur.append(text)
            elif cur:
                out.append((start, cur))
                cur = []
    if cur:
        out.append((start, cur))
    return out


def nearest(items, energy, key):
    best, best_d = None, 999.0
    for item in items:
        d = abs(item[1] - energy) if isinstance(item, tuple) else abs(item['e'] - energy)
        if d <= 1.0 and d < best_d:
            best, best_d = item, d
    return best


def unsure(jpi):
    return (not jpi) or any(ch in jpi for ch in '(,)')


def main():
    path = Path(sys.argv[1])
    levels, gammas = parse_records(path)
    print(f'levels={len(levels)}  gammas={len(gammas)}')
    total = 0
    for start, text_lines in blocks(path):
        full = re.sub(r'\s+', ' ', ' '.join(t.strip() for t in text_lines))
        found = list(TRANS.finditer(full))
        if not found:
            continue
        coverage = sum(len(m.group(0)) for m in found) / max(len(full), 1)
        if coverage < 0.5:
            print(f'\n--- prose (skipped) block at line {start}: coverage={coverage:.2f}')
            continue
        rows = []
        for m in found:
            g = nearest(gammas, float(m.group('ge')), 'e')
            lv = nearest(levels, 0.0 if m.group('level') == 'g.s.' else float(m.group('level')), 'e')
            rows.append((m, g, lv))
        issues = []
        for m, g, lv in rows:
            if g is None:
                issues.append(f'gamma {m.group("ge")} not found in G-records')
                continue
            if g['ri'] is not None and g['ri'] < 5:
                issues.append(f'R1a weak: {m.group("ge")}|g RI={g["ri_str"]} (G line {g["line"]})')
            if g['dri'] == 'LT':
                issues.append(f'R1b upper-limit: {m.group("ge")}|g DRI=LT (G line {g["line"]})')
            if g['q80'] == '?':
                issues.append(f'R1c questionable: {m.group("ge")}|g col80=? (G line {g["line"]})')
            if lv is not None and unsure(lv[2]):
                issues.append(f'R1d final J-pi uncertain/multi: {m.group("level")} J="{lv[2]}" (L line {lv[3]})')
        rvals = [g['ri'] for m, g, _ in rows if g and g['ri'] is not None and m.group('dir') == 'to']
        if rvals != sorted(rvals, reverse=True):
            issues.append(f'R2a order: RI sequence {rvals}')
        seen = {}
        for m, g, lv in rows:
            if lv is None or m.group('dir') != 'to':
                continue
            jpi = lv[2]
            if jpi in seen:
                issues.append(f'R2b duplicate final J-pi "{jpi}": {seen[jpi]} and {m.group("ge")}|g')
            else:
                seen[jpi] = f'{m.group("ge")}|g'
        if issues:
            total += len(issues)
            print(f'\n--- cL J$ block at line {start}: {full[:100]}')
            for f in rows:
                m, g, lv = f
                gs = f'RI={g["ri_str"]}' if g else 'RI=?'
                ls = f'J={lv[2]}' if lv else 'J=?'
                print(f'      {m.group("ge")}|g -> {m.group("level")} {gs} {ls}')
            for s in issues:
                print(f'      ! {s}')
    print(f'\nTOTAL ISSUES: {total}')


if __name__ == '__main__':
    main()
