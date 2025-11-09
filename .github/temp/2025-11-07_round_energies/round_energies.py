from decimal import Decimal, ROUND_HALF_UP
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: round_energies.py <path-to-ens-file>")
    sys.exit(2)

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8').splitlines(True)  # keep line endings

changed = []
new_lines = []
for idx, line in enumerate(text, start=1):
    if len(line) == 0:
        new_lines.append(line)
        continue
    # Only process data records with L or G in col 8
    if len(line) >= 9 and line[7] in ('L', 'G') and (len(line) >= 19):
        # E field is columns 10-19 (1-based) -> indices [9:19)
        field = line[9:19]
        raw = field.strip()
        if raw:
            try:
                val = Decimal(raw)
                ival = int(val.quantize(Decimal('1'), rounding=ROUND_HALF_UP))
                new_field = f"{ival:<10}"
                if new_field != field:
                    new_line = line[:9] + new_field + line[19:]
                    changed.append((idx, field, new_field, line.rstrip('\n'), new_line.rstrip('\n')))
                    line = new_line
            except Exception:
                pass
    new_lines.append(line)

# Write back
path.write_text(''.join(new_lines), encoding='utf-8')

# Report
print(f"Lines changed: {len(changed)}")
for (i, oldf, newf, oldline, newline) in changed:
    print(f"{i:4d} E-field: '{oldf}' -> '{newf}'")
    # show a compact diff context
    print(f"OLD: {oldline}")
    print(f"NEW: {newline}")
