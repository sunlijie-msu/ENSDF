from pathlib import Path
from decimal import Decimal
import random
import re
import math

ens_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens')
csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_Unbound_extracttable.csv')


def decimals_of(text: str) -> int:
    return len(text.split('.')[1]) if '.' in text else 0


def decimal_to_text(value: Decimal, places: int) -> str:
    if places == 0:
        return str(value.quantize(Decimal('1')))
    quant = Decimal('1.' + ('0' * places))
    return format(value.quantize(quant), 'f')


def parse_intensity(text: str):
    cleaned = text.strip().replace(' ', '')
    if cleaned.startswith('<'):
        return cleaned[1:], 'LT'
    if cleaned.startswith('>'):
        return cleaned[1:], 'GT'
    return cleaned, ''


# Parse ENSDF levels and gammas
levels = {}
level_texts = {}
current = None
for idx, line in enumerate(ens_path.read_text().splitlines(), start=1):
    if len(line) > 9 and line[6:7] == ' ' and line[7:8] == 'L':
        e_text = line[9:19].strip()
        current = Decimal(e_text)
        levels[current] = []
        level_texts[current] = e_text
    elif len(line) > 9 and line[6:7] == ' ' and line[7:8] == 'G' and current is not None:
        eg = line[9:19].strip()
        ri = line[22:29].strip()
        dri = line[29:31].strip()
        levels[current].append((eg, ri, dri, idx))

# Parse CSV
csv_lines = csv_path.read_text().splitlines()
headers = csv_lines[1].split(',')
fixed_headers = headers[:31]
ef_headers = fixed_headers[2:30]
pattern = re.compile(r'(\d+(?:\.\d+)?)\(([^)]*)\)')

expected = []
new_levels = []
for row_idx, line in enumerate(csv_lines[2:], start=3):
    parts = line.split(',')
    fixed = parts[:30]
    tail = ','.join(parts[30:]).strip()
    ei_text = fixed[1].strip()
    ei = Decimal(ei_text)
    new_levels.append(ei)
    for idx, cell in enumerate(fixed[2:], start=2):
        cell = cell.strip()
        if not cell:
            continue
        ef_text = fixed_headers[idx]
        ef = Decimal(ef_text)
        places = max(decimals_of(ei_text), decimals_of(ef_text))
        eg_text = decimal_to_text(ei - ef, places)
        ri_text, dri_text = parse_intensity(cell)
        expected.append((ei, eg_text, ri_text, dri_text, row_idx, ef_text, cell))
    for ef_text, ig_text in pattern.findall(tail):
        precise_ef_text = level_texts.get(Decimal(ef_text), ef_text)
        places = max(decimals_of(ei_text), decimals_of(precise_ef_text))
        eg_text = decimal_to_text(ei - Decimal(precise_ef_text), places)
        ri_text, dri_text = parse_intensity(ig_text)
        expected.append((ei, eg_text, ri_text, dri_text, row_idx, precise_ef_text, ig_text))

# Full completeness check
missing_levels = [ei for ei in new_levels if ei not in levels]
match_failures = []
for item in expected:
    ei, eg_text, ri_text, dri_text, row_idx, ef_text, source_text = item
    actual_set = {(eg, ri, dri) for eg, ri, dri, _ in levels.get(ei, [])}
    if (eg_text, ri_text, dri_text) not in actual_set:
        match_failures.append(item)

print(f'NEW_LEVELS_EXPECTED={len(new_levels)}')
print(f'NEW_LEVELS_MISSING={len(missing_levels)}')
print(f'NEW_TRANSITIONS_EXPECTED={len(expected)}')
print(f'NEW_TRANSITIONS_MISMATCHED={len(match_failures)}')

# 5% random spot-check
sample_size = max(5, math.ceil(0.05 * len(expected)))
random.seed(20260309)
indices = sorted(random.sample(range(len(expected)), sample_size))
print(f'SPOTCHECK_SEED=20260309')
print(f'SPOTCHECK_SIZE={sample_size}')

passes = 0
for sample_no, idx in enumerate(indices, start=1):
    ei, eg_text, ri_text, dri_text, row_idx, ef_text, source_text = expected[idx]
    matches = [(eg, ri, dri, line_no) for eg, ri, dri, line_no in levels[ei] if (eg, ri, dri) == (eg_text, ri_text, dri_text)]
    ok = len(matches) == 1
    if ok:
        passes += 1
        line_no = matches[0][3]
    else:
        line_no = -1
    print(
        f"SAMPLE {sample_no}: {'PASS' if ok else 'FAIL'} | row={row_idx} | Ei={ei} | Ef={ef_text} | "
        f"source={source_text} | Eg={eg_text} | RI={ri_text} | DRI={dri_text or '-'} | ens_line={line_no}"
    )

print(f'SPOTCHECK_PASS={passes}/{sample_size}')
