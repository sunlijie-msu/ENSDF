from pathlib import Path
import re
from decimal import Decimal

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_Unbound_extracttable.csv')
ens_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02.ens')

lines = csv_path.read_text().splitlines()
header = lines[1].split(',')
fixed_headers = header[:31]
ef_headers = [Decimal(x) for x in fixed_headers[2:30]]

existing_levels = []
level_text_by_value = {}
for line in ens_path.read_text().splitlines():
    if len(line) > 9 and line[6:7] == ' ' and line[7:8] == 'L':
        text = line[9:19].strip()
        if text:
            try:
                value = Decimal(text)
                existing_levels.append(value)
                level_text_by_value[value] = text
            except Exception:
                print('BAD_L_FIELD', repr(text))

pattern = re.compile(r'(\d+(?:\.\d+)?)\(([^)]*)\)')


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


def make_l_record(ei_text: str) -> str:
    return f" 34CL  L {ei_text.ljust(10)}{'':2} {'':58}"


def make_g_record(eg_text: str, ri_text: str, dri_text: str) -> str:
    return f" 34CL  G {eg_text.ljust(10)}{'':2} {ri_text.ljust(7)}{dri_text.ljust(2)}{'':49}"

rows = []
for line in lines[2:]:
    parts = line.split(',')
    fixed = parts[:30]
    tail = ','.join(parts[30:]).strip()
    eplab = fixed[0].strip()
    ei_text = fixed[1].strip()
    ei = Decimal(ei_text)
    transitions = []
    for idx, cell in enumerate(fixed[2:], start=2):
        cell = cell.strip()
        if not cell:
            continue
        ef = ef_headers[idx - 2]
        ef_text = fixed_headers[idx]
        transitions.append((ef, ef_text, cell))
    for ef_text, ig_text in pattern.findall(tail):
        ef_value = Decimal(ef_text)
        precise_ef_text = level_text_by_value.get(ef_value, ef_text)
        transitions.append((ef_value, precise_ef_text, ig_text.strip()))
    rows.append((eplab, ei, ei_text, transitions, tail))

missing = [(eplab, ei, ei_text, transitions, tail) for eplab, ei, ei_text, transitions, tail in rows if ei not in existing_levels]

print(f'fixed_headers={len(fixed_headers)}')
print(f'ef_headers={len(ef_headers)}')
print(f'rows={len(rows)}')
print(f'existing_levels={len(existing_levels)}')
print(f'missing_levels={len(missing)}')
for eplab, ei, ei_text, transitions, tail in missing[:5]:
    print('ROW', eplab, str(ei), 'transitions', len(transitions), 'tail', repr(tail))

print('LAST_MISSING', str(missing[-1][1]))
print('TOTAL_MISSING_TRANSITIONS', sum(len(item[2]) for item in missing))

# write detailed candidate output
out = Path(r'd:\X\ND\ENSDF\.github\temp\2026-03-09_unbound_candidates.txt')
with out.open('w') as f:
    for eplab, ei, ei_text, transitions, tail in missing:
        f.write(f'Ei={ei} Eplab={eplab}\n')
        for ef, ef_text, cell in transitions:
            eg = ei - ef
            f.write(f'  Ef={ef} Eg={eg} Ig={cell}\n')
        f.write('\n')
print(out)

block_lines = []
for eplab, ei, ei_text, transitions, tail in missing:
    block_lines.append(make_l_record(ei_text))
    gamma_records = []
    for ef, ef_text, cell in transitions:
        places = max(decimals_of(ei_text), decimals_of(ef_text))
        eg_text = decimal_to_text(ei - ef, places)
        ri_text, dri_text = parse_intensity(cell)
        gamma_records.append((Decimal(eg_text), make_g_record(eg_text, ri_text, dri_text)))
    gamma_records.sort(key=lambda item: item[0])
    for _, record in gamma_records:
        block_lines.append(record)

block_path = Path(r'd:\X\ND\ENSDF\.github\temp\2026-03-09_unbound_block.txt')
block_path.write_text('\n'.join(block_lines) + '\n')
print(block_path)
print('BLOCK_LINES', len(block_lines))
print('BAD_LENGTHS', sum(1 for line in block_lines if len(line) != 80))
