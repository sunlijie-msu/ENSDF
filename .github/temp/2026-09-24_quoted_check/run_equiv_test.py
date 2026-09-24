#!/usr/bin/env python3
"""Regression fixture for measured-vs-character multipolarity equivalence.

Builds a minimal adopted-style file whose cL J$ arguments quote the measured
form (D / D+Q) while the G-record M field holds the converted character form,
then runs the quoted-values checker over four planted cases:

  case 1  M=(E1)   comment D      -> must be ACCEPTED  (equivalent)
  case 2  M=(M1+E2) comment D+Q   -> must be ACCEPTED  (equivalent)
  case 3  M=M1+E2  comment D      -> must be ERROR     (order differs)
  case 4  M=E2     comment D      -> must be ERROR     (order differs)
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / 'equiv_test.ens'
CHECKER = HERE.parents[1] / 'scripts' / 'check_quoted_values.py'


def rec(fields):
    """Build one 80-column record from (start_col, text) pairs."""
    row = [' '] * 80
    for start, text in fields:
        row[start - 1:start - 1 + len(text)] = text
    return ''.join(row)


def l_record(nucid, energy, de, jpi):
    return rec([(1, nucid), (8, 'L'), (10, energy), (20, de), (23, jpi)])


def g_record(nucid, energy, de, ri, dri, mul):
    return rec([(1, nucid), (8, 'G'), (10, energy), (20, de), (23, ri),
                (30, dri), (33, mul)])


def cl_record(nucid, text):
    return rec([(1, nucid), (7, 'c'), (8, 'L'), (10, text)])


CASES = [
    ('(E1)', 'D', False, 'character form for a measured D'),
    ('(M1+E2)', 'D+Q', False, 'character form for a measured D+Q'),
    ('M1+E2', 'D', True, 'order differs: D vs M1+E2'),
    ('E2', 'D', True, 'order differs: D vs E2'),
]

lines = [l_record(' 34S ', '1991', '5', '7/2-')]
expected = {}
for index, (m_field, quote, is_error, label) in enumerate(CASES, start=1):
    # Own level sits one gamma energy above the final level quoted below.
    own = 1991.0 + 1824.7 + index
    gamma = round(own - 1991.0, 1)
    lines.append(l_record(' 34S ', f'{own:.1f}', '5', '9/2-'))
    lines.append(g_record(' 34S ', f'{gamma:.1f}', '5', '10.0', '5', m_field))
    lines.append(cl_record(
        ' 34S ',
        f'J$ {gamma:.1f}|g, {quote}, |DJ=1 to 7/2-, 1991 level.'))
    expected[round(gamma, 1)] = (m_field, quote, is_error, label)

FIXTURE.write_text('\n'.join(lines) + '\n', encoding='utf-8')

proc = subprocess.run([sys.executable, str(CHECKER), str(FIXTURE)],
                      capture_output=True, text=True)
out = proc.stdout

print(f'fixture: {FIXTURE}')
print(f'exit code: {proc.returncode}')
print(out)

failures = 0
for gamma, (m_field, quote, is_error, label) in expected.items():
    # Locate the finding by its quoted/actual pair instead of line numbers.
    ctx = re.search(rf'quoted "{re.escape(quote)}",?\s+G-record M field is '
                    rf'"{re.escape(m_field)}"', out, re.I)
    reported = ctx is not None
    ok = reported == is_error
    failures += 0 if ok else 1
    verdict = 'PASS' if ok else 'FAIL'
    print(f'{verdict}: M={m_field!r} quote={quote!r} expected_error={is_error} '
          f'reported={reported}  ({label})')

print(f'\n{"ALL PASS" if not failures else str(failures) + " FAILURE(S)"}')
sys.exit(1 if failures else 0)
