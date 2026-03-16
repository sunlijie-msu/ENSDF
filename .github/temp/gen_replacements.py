"""
Generate exact 80-char G record replacement strings for all 20 D-flagged transitions.
Also generate cG RI$ comment replacements.
"""
import re

ENS = r"D:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens"
lines = open(ENS, encoding='utf-8').readlines()

def make_g_record(nucid_5, e_field, de_field, ri_field, dri_field, m_field, mr_field, dmr_field, cc_field, dcc_field, ti_field, dti_field, flag_col77, ms_78_79, q_col80):
    """Build exactly 80-char G record."""
    nuc = nucid_5.ljust(5)[:5]
    line = nuc + " " + " " + "G" + " "  # cols 1-9
    line += e_field.ljust(10)[:10]       # cols 10-19
    line += de_field.ljust(2)[:2]        # cols 20-21
    line += " "                           # col 22
    line += ri_field.ljust(7)[:7]        # cols 23-29
    line += dri_field.ljust(2)[:2]       # cols 30-31
    line += " "                           # col 32
    line += m_field.ljust(9)[:9]         # cols 33-41
    line += mr_field.ljust(8)[:8]        # cols 42-49
    line += dmr_field.ljust(6)[:6]       # cols 50-55
    line += cc_field.ljust(7)[:7]        # cols 56-62
    line += dcc_field.ljust(2)[:2]       # cols 63-64
    line += ti_field.ljust(10)[:10]      # cols 65-74
    line += dti_field.ljust(2)[:2]       # cols 75-76
    line += flag_col77[:1]               # col 77
    line += ms_78_79.ljust(2)[:2]        # cols 78-79
    line += q_col80[:1]                  # col 80
    assert len(line) == 80, f"len={len(line)}"
    return line

def parse_g_record(line80):
    """Parse a G record from an 80-char line (no trailing newline)."""
    line = line80.rstrip('\n')
    if len(line) < 80:
        line = line.ljust(80)
    return {
        'nucid': line[0:5],
        'cont': line[5],
        'sp6': line[6],
        'type': line[7],
        'sp8': line[8],
        'E': line[9:19].rstrip(),
        'DE': line[19:21].rstrip(),
        'RI': line[22:29].rstrip(),
        'DRI': line[29:31].rstrip(),
        'M': line[32:41].rstrip(),
        'MR': line[41:49].rstrip(),
        'DMR': line[49:55].rstrip(),
        'CC': line[55:62].rstrip(),
        'DCC': line[62:64].rstrip(),
        'TI': line[64:74].rstrip(),
        'DTI': line[74:76].rstrip(),
        'C77': line[76],
        'MS': line[76:78],  # actually 77-78 in 0-indexed = cols 77-78 1-indexed? let me use correct
        'raw': line
    }

# Corrections: (gamma_energy_str, new_RI_str, new_DRI_str)
# The D flag in col 77 (0-indexed col 76) will be cleared to space for all.
# 2-way averages: (Da02 RI, Da02 DRI, Hy02 RI, Hy02 DRI, adopted_RI, adopted_DRI)
# For display: Da02 string, Hy02 string, additional_others (list of (val, ref) tuples)

corrections = {
    '2092.7':  {'new_ri': '15.5', 'new_dri': '60', 'da02': ('14.7','74'), 'hy02': ('16','6'),
                'gr29': None, 'others': [('15','1983Wa27')]},
    '2185.9':  {'new_ri': '100',  'new_dri': '10', 'da02': ('100','10'), 'hy02': ('100','19'),
                'gr29': ('100','25'), 'others': [('100','1983Wa27'),('100','1964Gl04')]},
    '3447.5':  {'new_ri': '20.7', 'new_dri': '21', 'da02': ('20.6','21'), 'hy02': ('25','13'),
                'gr29': None, 'others': [('25','1983Wa27')]},
    '3557.8':  {'new_ri': '7.3',  'new_dri': '30', 'da02': ('5.9','30'), 'hy02': ('13','6'),
                'gr29': None, 'others': [('8.8','1983Wa27')]},
    '3987.7':  {'new_ri': '15.5', 'new_dri': '60', 'da02': ('14.7','74'), 'hy02': ('16','6'),
                'gr29': None, 'others': [('15','1983Wa27')]},
    '4281.4':  {'new_ri': '7.1',  'new_dri': '31', 'da02': ('8.8','44'), 'hy02': ('6.3','31'),
                'gr29': None, 'others': [('6.4','1983Wa27'),('<8.3','1969Gr29')]},
    '2130.8':  {'new_ri': '18.6', 'new_dri': '19', 'da02': ('18.8','19'), 'hy02': ('14.3','82'),
                'gr29': None, 'others': [('18','1983Wa27')]},
    '2575.3':  {'new_ri': '20.8', 'new_dri': '21', 'da02': ('20.8','21'), 'hy02': ('20','10'),
                'gr29': None, 'others': [('19','1983Wa27')]},
    '2606.7':  {'new_ri': '100',  'new_dri': '10', 'da02': ('100','10'), 'hy02': ('100','21'),
                'gr29': ('100','20'), 'others': [('100','1983Wa27')]},
    '4025.7':  {'new_ri': '7.6',  'new_dri': '21', 'da02': ('6.3','31'), 'hy02': ('8.2','21'),
                'gr29': None, 'others': [('5.7','1983Wa27')]},
    '1589.7':  {'new_ri': '4.5',  'new_dri': '18', 'da02': ('3.3','18'), 'hy02': ('6.0','20'),
                'gr29': None, 'others': [('3.9','1983Wa27')]},
    '1712.9':  {'new_ri': '24.0', 'new_dri': '25', 'da02': ('24.4','25'), 'hy02': ('22','6'),
                'gr29': None, 'others': [('29','1983Wa27')]},
    '1811.3':  {'new_ri': '6.2',  'new_dri': '20', 'da02': ('6.7','33'), 'hy02': ('6.0','20'),
                'gr29': None, 'others': [('6.3','1983Wa27')]},
    '1874.4':  {'new_ri': '20',   'new_dri': '2',  'da02': ('20','2'),  'hy02': ('16','6'),
                'gr29': None, 'others': [('23','1983Wa27')]},
    '2088.9':  {'new_ri': '13.2', 'new_dri': '13', 'da02': ('13.3','13'), 'hy02': ('12','4'),
                'gr29': None, 'others': [('12','1983Wa27')]},
    '2454.8':  {'new_ri': '31.6', 'new_dri': '33', 'da02': ('33.3','33'), 'hy02': ('26','6'),
                'gr29': None, 'others': [('44','1983Wa27'),('71','1964Gl04')]},
    '3507.1':  {'new_ri': '100',  'new_dri': '10', 'da02': ('100','10'), 'hy02': ('100','12'),
                'gr29': None, 'others': [('100','1983Wa27'),('100','1964Gl04')]},
    '4070.5':  {'new_ri': '10.4', 'new_dri': '40', 'da02': ('11.1','56'), 'hy02': ('10','4'),
                'gr29': None, 'others': [('9.5','1983Wa27'),('29','1964Gl04')]},
    '5766.9':  {'new_ri': '2.4',  'new_dri': '10', 'da02': ('4.4','22'), 'hy02': ('2.0','10'),
                'gr29': None, 'others': [('5.1','1983Wa27')]},
    '6228.01': {'new_ri': '1.9',  'new_dri': '8',  'da02': ('3.3','18'), 'hy02': ('1.60','80'),
                'gr29': None, 'others': [('5.6','1983Wa27')]},
}

# Find each G record line in the file and show what changes are needed
print("=" * 100)
print("G RECORD CHANGES")
print("=" * 100)
for i, raw in enumerate(lines):
    line = raw.rstrip('\n').ljust(80)
    # Check if this is a G record with D flag
    if len(line) >= 77 and line[7] == 'G' and line[6] == ' ' and line[76] == 'D' and line[0:5].strip() == '34CL':
        e_str = line[9:19].strip()
        if e_str in corrections:
            c = corrections[e_str]
            # Build new G record
            old_ri = line[22:29].rstrip()
            old_dri = line[29:31].rstrip()
            
            # Construct new line
            new_line = line[:22] + c['new_ri'].ljust(7) + c['new_dri'].ljust(2) + line[31:76] + ' ' + line[77:80]
            assert len(new_line) == 80, f"new_line len={len(new_line)}"
            
            print(f"\nL{i+1} E={e_str}")
            print(f"  OLD G: {repr(line)}")
            print(f"  NEW G: {repr(new_line)}")
            print(f"  RI: {old_ri} -> {c['new_ri']}, DRI: {old_dri} -> {c['new_dri']}, D->space at col77")

print("\n\n" + "=" * 100)
print("cG RI$ COMMENT CHANGES")
print("=" * 100)

# Find cG RI$ lines for each target G record
for i, raw in enumerate(lines):
    line = raw.rstrip('\n').ljust(80)
    if len(line) >= 77 and line[7] == 'G' and line[6] == ' ' and line[76] == 'D' and line[0:5].strip() == '34CL':
        e_str = line[9:19].strip()
        if e_str in corrections:
            c = corrections[e_str]
            # Look for cG RI$ in next 3 lines
            for j in range(i+1, min(i+5, len(lines))):
                nxt = lines[j].rstrip('\n')
                if 'cG RI' in nxt:
                    # Build new comment
                    da02_ri, da02_dri = c['da02']
                    hy02_ri, hy02_dri = c['hy02']
                    gr29 = c['gr29']
                    others = c['others']
                    
                    # Build Other: part
                    other_parts = [f"{v} ({r})" for v, r in others]
                    other_str = "Other: " + ", ".join(other_parts) + "." if other_parts else ""
                    
                    # Build weighted average part
                    if gr29:
                        gr29_ri, gr29_dri = gr29
                        avg_str = (f"weighted average of {da02_ri} {{I{da02_dri}}} (1977Da02), "
                                   f"{gr29_ri} {{I{gr29_dri}}} (1969Gr29), and "
                                   f"{hy02_ri} {{I{hy02_dri}}} (1971Hy02).")
                    else:
                        avg_str = (f"weighted average of {da02_ri} {{I{da02_dri}}} (1977Da02) "
                                   f"and {hy02_ri} {{I{hy02_dri}}} (1971Hy02).")
                    
                    full_comment = avg_str + (" " + other_str if other_str else "")
                    
                    prefix1 = " 34CL cG RI$"  # 12 chars
                    prefix2 = " 34CL2cG "     # 9 chars
                    
                    # Check if it needs wrapping
                    if len(prefix1) + len(full_comment) <= 80:
                        new_cg_line = prefix1 + full_comment
                    else:
                        # Split: avg_str on line 1, other_str on line 2
                        # Try to split after avg_str
                        line1_content = avg_str
                        line2_content = other_str
                        if len(prefix1) + len(line1_content) <= 80:
                            new_cg_line = prefix1 + line1_content + "\n" + prefix2 + line2_content
                        else:
                            # Need to split within avg_str - find last ", and" before col 68
                            split_at = full_comment.rfind(", and ", 0, 80-12)
                            if split_at < 0:
                                split_at = full_comment.rfind(" and ", 0, 80-12)
                            if split_at >= 0:
                                new_cg_line = prefix1 + full_comment[:split_at+4] + "\n" + prefix2 + full_comment[split_at+4:].lstrip()
                            else:
                                new_cg_line = prefix1 + full_comment  # fallback, will be long
                    
                    # Check if next line is also a cG/2cG line to include in old string
                    old_block = nxt
                    if j+1 < len(lines) and '2cG' in lines[j+1] and '1971Hy02' in lines[j+1]:
                        old_block += "\n" + lines[j+1].rstrip('\n')
                    
                    print(f"\nL{j+1} E={e_str}")
                    print(f"  OLD cG RI$: {repr(old_block)}")
                    print(f"  NEW cG RI$: {repr(new_cg_line)}")
                    break
