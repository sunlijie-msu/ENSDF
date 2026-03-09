ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
lines = open(ADP_FILE, encoding='utf-8').readlines()

# L637 spot check
print(f"L637: {repr(lines[636].rstrip())}")

# Lines with cG RI$from
from_lines = [(i+1, lines[i].rstrip()) for i in range(len(lines))
              if 'cG RI$from 1977Da02' in lines[i] or 'cG RI$from 1983Wa27' in lines[i]]

# Over 80 chars
over80 = [(ln, l) for (ln, l) in from_lines if len(l) > 80]
print(f"\nLines over 80 chars: {len(over80)}")
for lnum, l in over80[:10]:
    print(f"  L{lnum} ({len(l)} chars): {repr(l)}")

# Plain (no Other)
plain = [(ln, l) for (ln, l) in from_lines if 'Other' not in l]
print(f"\nRemaining plain cG RI$from (no Other): {len(plain)}")
for lnum, l in plain[:20]:
    print(f"  L{lnum}: {repr(l)}")

# Has Other
with_other = [(ln, l) for (ln, l) in from_lines if 'Other' in l]
print(f"\ncG RI$from lines with Other: {len(with_other)}")
print(f"Total cG RI$from lines: {len(from_lines)}")
