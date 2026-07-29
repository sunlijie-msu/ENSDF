"""Generate all replacement lines for S34 beta decay revision."""
import sys
sys.path.insert(0, '.')
from build_lines import build_L, build_B, build_G

# Generate new data section starting from L 2127.4
lines = []

# L 2127.4
lines.append(build_L('2127.4', '2', '2+'))
lines.append(build_B('14.8', '20', '4.93', '6'))
lines.append((' 34S  cB IB$other: 15 {I2} (1971Wa04)').ljust(80))
lines.append(build_G('2127.3', '', '100.0', '3', 'E2'))

# L 3303.7 (new)
lines.append(build_L('3303.7', '3', ''))
lines.append(build_G('3303.5', '', '0.12', 'LT', ''))

# L 3914.2
lines.append(build_L('3914.2', '6', '0+'))
lines.append(build_B('0.045', '17', '5.98', '17'))
lines.append(build_G('1787', '1', '0.3', '1', 'E2'))

# L 4073.0
lines.append(build_L('4073.0', '10', '1+'))
lines.append(build_B('0.111', '23', '5.38', '9'))
lines.append(build_G('1947.1', '15', '0.28', '10', 'M1+E2', '+1.3', '+9-32'))
lines.append(build_G('4073.4', '15', '0.46', '6', 'D'))

# L 4114.5
lines.append(build_L('4114.5', '6', '2+'))
lines.append(build_B('0.31', '6', '4.88', '9'))
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

print('\n'.join(lines))
