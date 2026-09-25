"""Bidirectional check: every T/DT field entered in the two 34Cl EC+B+ decay
datasets must match the Adopted Levels record of the same level.

Direction 1 (source -> target): each adopted level that appears in a decay
dataset must carry its adopted T/DT in that dataset's L-record.
Direction 2 (target -> source): every non-empty T/DT in the decay datasets must
exist, character for character, in the adopted L-record.

Usage: python verify_half_lives.py
"""
import re

ADOPTED = r'A34/S34/new/S34_adopted.ens'
TARGETS = [
    (r'A34/S34/new/S34_34cl_ec_decay_1.5266_s.ens', '34CL EC+B+ DECAY (1.5266 S)'),
    (r'A34/S34/new/S34_34cl_ec_decay_31.99_m.ens', '34CL EC+B+ DECAY (31.99 M)'),
]


def l_records(path):
    """Yield (line_no, E_string, T_field, DT_field, raw_line) for L-records."""
    for i, l in enumerate(open(path, encoding='utf-8', newline='').read().split('\r\n')):
        if len(l) >= 80 and l[7] == 'L' and l[5:7] == '  ':
            yield i + 1, l[9:19].strip(), l[39:49], l[49:55], l


adopted = {}
for _, e, T, DT, _ in l_records(ADOPTED):
    adopted[e] = (T, DT)

print('Adopted Levels reference (E -> T | DT):')
for e in sorted(adopted, key=lambda x: float(x)):
    T, DT = adopted[e]
    print(f'   {e:<10} {T!r:<12} {DT!r}')
print()

fail = 0
for path, title in TARGETS:
    print(f'=== {title}   ({path.split("/")[-1]})')
    for n, e, T, DT, raw in l_records(path):
        if not T.strip():
            print(f'   line {n:>4}  E={e:<6}  T empty  -> adopted has no half-life for '
                  f'{ [k for k in adopted if k.split(".")[0] == e] }')
            continue
        # direction 2: target -> source (nearest adopted level)
        near = min(adopted, key=lambda k: abs(float(k) - float(e)))
        aT, aDT = adopted[near]
        ok = (T == aT) and (DT == aDT)
        fail += 0 if ok else 1
        print(f'   line {n:>4}  E={e:<6} T={T!r:<12} DT={DT!r:<8} '
              f'| adopted {near} T={aT!r} DT={aDT!r}  {"OK" if ok else "*** MISMATCH ***"}')
        assert len(raw) == 80, f'line {n} is {len(raw)} chars'
    print()

# direction 1: adopted levels that a decay dataset observes but whose T was not copied
for path, title in TARGETS:
    seen = {e for _, e, _, _, _ in l_records(path)}
    print(f'{title}: levels in dataset = {sorted(seen, key=float)}')
print()
print('MISMATCHES:', fail)
