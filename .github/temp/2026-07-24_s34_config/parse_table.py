"""Parse S34_32s_t_p.old text table into per-level configuration data."""
import re, json

with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

# Debug: print raw chars for each t-record
print("=== RAW t-records ===")
for i, line in enumerate(lines):
    if 's{-rel}' in line or 'E(MeV)' in line or 'Configuration' in line:
        print(f"L{i+1}: [{line[5] if len(line)>5 else '?'}][{line[6] if len(line)>6 else '?'}][{line[7] if len(line)>7 else '?'}][{line[8] if len(line)>8 else '?'}] len={len(line)} |{line.rstrip()}|")
    # Also capture lines with numbers at start
    stripped = line.rstrip()
    if len(line) >= 9:
        col6, col7, col8 = line[5] if len(line)>5 else '', line[6] if len(line)>6 else '', line[7] if len(line)>7 else ''
        text_after = line[8:].strip() if len(line)>8 else ''
        if col7 == 't' and ('0.00' in text_after or '2.13' in text_after):
            print(f"L{i+1}: col6=[{col6}] col7=[{col7}] text=[{text_after[:60]}]")

# Check all lines where col6='2'
print("\n=== Lines with col5,6,7 ===")
for i, line in enumerate(lines):
    if len(line) >= 9:
        c5 = line[4] if len(line)>4 else 'x'
        c6 = line[5] if len(line)>5 else 'x'
        c7 = line[6] if len(line)>6 else 'x'
        c8 = line[7] if len(line)>7 else 'x'
        # check for '2 t' pattern in cols 5-7
        if c6 == '2' and c7 == ' ' and c8 == 't':
            print(f"L{i+1}: col5-8=[{c5}{c6}{c7}{c8}] |{line.rstrip()[:80]}|")
        if c6 == ' ' and c7 == 't':
            print(f"L{i+1}: col5-8=[{c5}{c6}{c7}{c8}] |{line.rstrip()[:80]}|")
