#!/usr/bin/env python3
"""Audit cL J$ quotations of a tentative E/M character form.

Rule under test (gamma-selection-rules, Conversion Precedence Rules):
a character derived from the level scheme (`|D|p=... from level scheme.`) is
circular as evidence for Jpi, so a cL J$ argument must quote the measured
assignment (D / Q / D+Q / D(+Q)), not the converted `(E1)` / `(M1)` / `(E2)`
/ `(M2)` / `(M1+E2)` / `(E1+M2)`.

Read-only: prints candidates, never edits.
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import check_quoted_values as cv  # noqa: E402

TENTATIVE = ('(', '[')


def g_comment_provenance(lines, g_line):
    """Collect the cG comment text attached to the G-record at g_line."""
    texts = []
    for i in range(g_line, len(lines)):
        line = lines[i]
        if len(line) < 8:
            break
        if line[6:7] == 'c' and line[7:8] == 'G':
            texts.append(line[9:].rstrip('\r\n').strip())
            continue
        if texts:
            break
        if line[7:8] in ('L', 'G'):
            break
    return ' '.join(texts)


def main() -> int:
    path = Path(sys.argv[1])
    refs, _ = cv.extract_quoted_refs(path)
    gammas = cv.parse_gammas(path)
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')

    found = 0
    for ref in refs:
        mult = (ref.multipolarity or '').strip()
        if not mult.startswith(TENTATIVE):
            continue
        g = cv.find_closest_gamma(gammas, ref.gamma_energy, 2.0)
        if g is None:
            continue
        prov = g_comment_provenance(lines, g.line_num)
        circular = 'from level scheme' in prov
        found += 1
        tag = 'CIRCULAR' if circular else 'ok (measured provenance)'
        print(f'[{"!" if circular else " "}] block line {ref.line_num}'
              f'  {ref.gamma_energy_str}|g quoted "{mult}"'
              f'  M field "{g.multipolarity}"')
        print(f'      -> {tag}: {prov[:150]}')
    print(f'\ntentative-character quotations found: {found}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
