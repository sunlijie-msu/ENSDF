"""Scan Cl34_adopted.ens and report exact line numbers for all target content."""
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

with open(ENS_FILE, encoding='utf-8') as f:
    lines = f.readlines()

targets = [
    (' 34CL cL J$1697|g',    '1697|g'),
    (' 34CL2cL 146 level.',  '146_level_continuation_243'),
    (' 34CL cL J$3500|g',    '3500|g'),
    (' 34CL2cL level.',      'level_continuation_627'),
    (' 34CL cL J$1502|g',    '1502|g'),
    (' 34CL cL J$3330|g',    '3330|g'),
    (' 34CL cL J$725|g, M1+E2, |DJ=1 to 5+, 3646 level', '725|g_3646'),
    (' 34CL cL J$4300.0|g',  '4300|g'),
    (' 34CL cL J$1224.1|g',  '1224|g'),
    (' 34CL2cL 3+, 146 level.', '3+_146_983'),
    (' 34CL cL J$2681|g',    '2681|g'),
    (' 34CL3cL 4810.5|g',    '4810.5|g'),
    (' 34CL2cL transition 1786.6', '1786.6'),
    (' 34CL cL J$primary transition 1330|g', '1330|g'),
    (' 34CL2cL 1977.0|g',    '1977|g'),
    (' 34CL cL J$primary transitions 5762.8', '5762.8'),
    (' 34CL2cL transition 5638.6', '5638.6'),
    (' 34CL cL J$1935.0|g',  '1935|g'),
    (' 34CL cL J$2384|g',    '2384|g'),
    (' 34CL cL J$2487.4|g',  '2487.4|g'),
    (' 34CL cL J$2840|g',    '2840|g'),
    (' 34CL cL J$4077|g',    '4077|g'),
    (' 34CL cL J$3381|g',    '3381|g'),
]

for prefix, label in targets:
    found = [(i+1, lines[i].rstrip()) for i in range(len(lines)) if lines[i].startswith(prefix)]
    if found:
        for lineno, content in found:
            print(f'{label:30s} -> Line {lineno:5d}: {content[:60]}')
    else:
        print(f'{label:30s} -> NOT FOUND')
