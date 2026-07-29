"""Generate complete replacement block for S34_beta_decay_12.43_s.ens
Replaces from L 2127.564 line to end of file."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def build_L(E_str, DE_str, J_str):
    line = (
        ' 34S   L ' +
        E_str.ljust(10)[:10] +
        DE_str.ljust(2)[:2] +
        ' ' +     # col 22
        J_str.ljust(17)[:17] +
        ' '*41    # cols 40-80
    )
    return line

def build_G(E_str, DE_str, RI_str, DRI_str, M_str, MR_str='', DMR_str=''):
    line = (
        ' 34S   G ' +
        E_str.ljust(10)[:10] +
        DE_str.ljust(2)[:2] +
        ' ' +     # col 22
        RI_str.ljust(7)[:7] +
        DRI_str.ljust(2)[:2] +
        ' ' +     # col 32
        M_str.ljust(9)[:9] +
        MR_str.ljust(8)[:8] +
        DMR_str.ljust(6)[:6] +
        ' '*7 +   # CC 56-62
        '  ' +    # DCC 63-64
        ' '*10 +  # TI 65-74
        '  ' +    # DTI 75-76
        ' ' +     # C 77
        '  ' +    # cols 78-79
        ' '       # Q 80
    )
    return line

# Read original B-record lines from the file
orig_file = r'd:\X\ND\ENSDF\A34\S34\S34_beta_decay_12.43_s.ens'
with open(orig_file, 'r') as f:
    orig_lines = [l.rstrip('\n') for l in f.readlines()]

# Extract B-record lines (they're at specific indices)
# Line indices (0-based): 28, 34, 36, 40 are B records in original
# Let me find them programmatically
b_lines = {}
for i, line in enumerate(orig_lines):
    if len(line) >= 8 and line[7] == 'B' and line[6] == ' ':
        # Find associated L-record energy
        # Look backward for the L record
        for j in range(i-1, -1, -1):
            if len(orig_lines[j]) >= 8 and orig_lines[j][7] == 'L':
                # Extract energy
                e_field = orig_lines[j][9:19].strip()
                b_lines[e_field] = line
                break

# Print B lines found
for e, bline in sorted(b_lines.items()):
    print(f'B for L {e}: {repr(bline)}')

# Now build the complete replacement block
lines = []

# L 2127.4
lines.append(build_L('2127.4', '2', '2+'))
# Keep existing B record but with correct column positions? 
# The original B record format is what the ruler accepts, so use it.
# But the original B lines are only ~52 chars. Need to pad to 80.
b_line = b_lines.get('2127.564', '')
if b_line:
    lines.append(b_line.ljust(80))
# cB comment
lines.append((' 34S  cB IB$other: 15 {I2} (1971Wa04)').ljust(80))
# G 2127.3
lines.append(build_G('2127.3', '', '100.0', '3', 'E2'))

# L 3303.7 (new)
lines.append(build_L('3303.7', '3', ''))
lines.append(build_G('3303.5', '', '0.12', 'LT', ''))

# L 3914.2
lines.append(build_L('3914.2', '6', '0+'))
b_line = b_lines.get('3916.408', '')
if b_line:
    lines.append(b_line.ljust(80))
lines.append(build_G('1787', '1', '0.3', '1', 'E2'))

# L 4073.0
lines.append(build_L('4073.0', '10', '1+'))
b_line = b_lines.get('4074.667', '')
if b_line:
    lines.append(b_line.ljust(80))
lines.append(build_G('1947.1', '15', '0.28', '10', 'M1+E2', '+1.3', '+9-32'))
lines.append(build_G('4073.4', '15', '0.46', '6', 'D'))

# L 4114.5
lines.append(build_L('4114.5', '6', '2+'))
b_line = b_lines.get('4114.813', '')
if b_line:
    lines.append(b_line.ljust(80))
lines.append(build_G('1987.2', '10', '1.0', '2', 'M1+E2', '-0.40', '5'))
lines.append(build_G('4114.0', '15', '1.2', '2', 'E2'))

# L 4622.2 (new)
lines.append(build_L('4622.2', '6', ''))
lines.append(build_G('1318.5', '', '0.21', 'LT', ''))

# L 4687.5 (new)
lines.append(build_L('4687.5', '6', ''))
lines.append(build_G('2560.0', '', '0.11', 'LT', ''))

# L 4875.2 (new)
lines.append(build_L('4875.2', '6', ''))
lines.append(build_G('1571.5', '', '1.0', 'LT', ''))

# L 4891 (new)
lines.append(build_L('4891', '3', ''))
lines.append(build_G('4891', '', '0.08', 'LT', ''))

# Print the output to a file
out_path = r'd:\X\ND\ENSDF\.github\temp\2026-07-29_beta_revise\replacement.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'\nGenerated {len(lines)} lines to {out_path}')
for i, line in enumerate(lines):
    print(f'  [{i}] len={len(line)} {repr(line[:60])}...' if len(line)>60 else f'  [{i}] len={len(line)} {repr(line)}')
