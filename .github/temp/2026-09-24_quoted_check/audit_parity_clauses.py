#!/usr/bin/env python3
"""Cross-check `|D|p=X from level scheme.` cG clauses against level parities.

For every G-record whose cG comment carries a level-scheme parity clause, the
parity change is recomputed from the L-records of the initial (owning) level and
the final level (owning level energy minus the gamma energy). A tentative parity
written as `8(+)` / `(7+)` is flagged, because a tentative parity cannot fix the
electromagnetic character.

Read-only: prints findings, never edits.
"""
import re
import sys
from pathlib import Path

CLAUSE = re.compile(r'\|D\|p=\s*\(?\s*(yes|no)\s*\)?', re.I)


def parity(jpi):
    """Return (sign, pi_tentative) for a J-pi string, or (None, None).

    Only the PARITY sign and its tentativeness matter here:
      `7-`    -> ('-', False)   `(7)-`  -> ('-', False)  tentative J, firm pi
      `8(+)`  -> ('+', True)    `(6+)`  -> ('+', True)   tentative parity
    """
    text = jpi.strip()
    if not text:
        return None, None
    if text.startswith('(') and text.endswith(')') and text.count('(') == 1:
        text = text[1:-1].strip()
    signs = set()
    tentative = False
    for part in text.split(','):
        part = part.strip()
        if not part:
            continue
        match = re.search(r'\(([+-])\)\s*$', part)
        if match:
            signs.add(match.group(1))
            tentative = True
        elif part[-1:] in ('+', '-'):
            signs.add(part[-1])
        else:
            return None, None
    if len(signs) != 1:
        return None, None
    return signs.pop(), tentative


def main() -> int:
    path = Path(sys.argv[1])
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')

    levels = []
    for i, line in enumerate(lines):
        if len(line) >= 40 and line[5:6] == ' ' and line[6:7] == ' ' \
                and line[7:8] == 'L' and line[0:5].strip():
            try:
                e = float(line[9:19])
            except ValueError:
                continue
            levels.append((e, line[22:39].strip(), i + 1))

    def closest(target):
        best, diff = None, 1.5
        for e, jpi, ln in levels:
            if abs(e - target) <= diff:
                best, diff = (e, jpi, ln), abs(e - target)
        return best

    own = None
    checked = mismatched = 0
    rows = []
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
        mfield = line[32:41].strip()
        # collect following cG comment
        prov = []
        for j in range(i + 1, len(lines)):
            if len(lines[j]) >= 8 and lines[j][6:7] == 'c' and lines[j][7:8] == 'G':
                prov.append(lines[j][9:].rstrip())
                continue
            break
        prov = ' '.join(prov)
        hit = CLAUSE.search(prov)
        if not hit:
            continue
        notation = hit.group(0)
        parenthesized = '(' in notation
        claimed = hit.group(1).lower()
        final = closest(own - eg)
        if final is None:
            continue
        initial_jpi = next(j for e, j, ln in levels if e == own)
        p0, t0 = parity(initial_jpi)
        p1, t1 = parity(final[1])
        rows.append((i + 1, eg, mfield, claimed, parenthesized, initial_jpi,
                     final[1], t0 or t1, p0, p1))
        if p0 is not None and p1 is not None:
            actual = 'yes' if p0 != p1 else 'no'
            checked += 1
            if actual != claimed:
                mismatched += 1
                print(f'MISMATCH  gamma {eg} (line {i+1})  {notation}'
                      f'  initial {initial_jpi!r} -> final {final[1]!r}'
                      f'  => actual Delta-pi = {actual}')

    print('\nline   gamma   notation            initial Jpi -> final Jpi   pi tent.')
    for ln, eg, mfield, claimed, par, ij, fj, pt, p0, p1 in rows:
        print(f'{ln:>5}  {eg:>7}  {str(par):>5} {mfield:<9}  {ij!r:>10} -> '
              f'{fj!r:<10}  {"YES" if pt else "-"}')
    print(f'\nclauses checked: {checked}   mismatches: {mismatched}\n'
          f'parenthesized notation: {sum(1 for r in rows if r[4])}'
          f'   tentative parity: {sum(1 for r in rows if r[7])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
