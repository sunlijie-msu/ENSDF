"""Generate the exact new block for level 6723.7 in Cl34_33s_p_g.ens"""

def g_line(energy, ri, dri=''):
    """Build an 80-char G record line.  dri='' -> blank DRI (2 spaces)."""
    nucid = ' 34CL  G '
    e_field = energy.ljust(10)
    de = '  '
    sep = ' '
    ri_field = ri.ljust(7)
    dri_field = dri.ljust(2)
    rest = ' ' * 49
    line = nucid + e_field + de + sep + ri_field + dri_field + rest
    assert len(line) == 80, f"G line len={len(line)}: {repr(line)}"
    return line

def cg_line(content):
    prefix = ' 34CL cG '
    line = (prefix + content).ljust(80)
    assert len(line) == 80, f"cG line len={len(line)}: {repr(line)}"
    return line

# New block lines
new_lines = [
    g_line('1899.2', '100'),
    cg_line('RI$100 {I11} (1977Da02)'),
    g_line('2027.9', '20'),
    cg_line('RI$18 {I9} (1977Da02)'),
    g_line('2759.5', '4.8'),           # unchanged (Wa27 only)
    g_line('3077.3', '33'),
    cg_line('RI$31.6 {I32} (1977Da02)'),
    g_line('3340.2', '1.6'),           # unchanged (Wa27 only)
    g_line('4112.4', '72'),
    cg_line('RI$91 {I9} (1977Da02)'),
    g_line('4347.7', '92'),
    cg_line('RI$118 {I12} (1977Da02)'),
    g_line('4542.3', '5.6'),
    cg_line('RI$9 {I5} (1977Da02)'),
    g_line('4565.5', '7.6'),
    cg_line('RI$14 {I7} (1977Da02)'),
    g_line('6057.8', '1.2', 'LT'),    # unchanged LT limit
    g_line('6261.9', '2',   'LT'),    # unchanged LT limit
    g_line('6576.6', '64'),
    cg_line('RI$73 {I7} (1977Da02)'),
    g_line('6723.0', '0.8', 'LT'),    # unchanged LT limit
]

print("=== New block ===")
for i, line in enumerate(new_lines):
    print(f"{i+1:2d}: {repr(line)}")

print()
print("=== Block as text (for visual check) ===")
for line in new_lines:
    print(line)
