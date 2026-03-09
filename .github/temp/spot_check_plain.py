ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

lines = open(ADP_FILE, encoding='utf-8').readlines()

# For each plain cG RI$from line, find the preceding G record and show the mrg context
plain_idxs = [i for i in range(len(lines))
              if ('cG RI$from 1977Da02' in lines[i] or 'cG RI$from 1983Wa27' in lines[i])
              and 'Other' not in lines[i]]

print(f"Checking {len(plain_idxs)} plain lines...\n")

# For each, find preceding G record
mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()

def find_prev_G(lines, i):
    """Find preceding G record energy."""
    for j in range(i-1, max(i-10, -1), -1):
        l = lines[j]
        if len(l) >= 8 and l[5] == ' ' and l[6] == ' ' and l[7] == 'G':
            return l[9:19].strip()
    return None

def find_in_mrg(mrg_lines, e_str, source_letter):
    """Check if mrg has the gamma and what datasets have RI."""
    try:
        adp_e = float(e_str)
    except:
        return None
    # Find GAMMA block within 2.0 keV
    current_e = None
    current_ds = {}
    for ml in mrg_lines:
        l = ml.rstrip('\n')
        if l.startswith(' GAMMA-'):
            idx = l.find(' 34CL  G')
            if idx >= 0:
                e_start = idx + 9
                try:
                    ce = float(l[e_start:e_start+10].strip())
                    if abs(ce - adp_e) < 2.0:
                        current_e = ce
                        current_ds = {}
                except:
                    pass
        elif l.startswith(' LEVEL') or l.startswith('-----'):
            if current_e is not None:
                # save and reset
                current_e = None
                current_ds = {}
        else:
            if current_e is not None and len(l) > 47 and l[39:47] == ' 34CL  G':
                tag = l[22:35]
                if '--->A' in tag:
                    ri = l[60:68].strip()
                    dri = l[68:70].strip()
                    current_ds['A'] = (ri, dri)
                elif '--->B' in tag:
                    ri = l[60:68].strip()
                    dri = l[68:70].strip()
                    current_ds['B'] = (ri, dri)
    return None  # didn't find it nearby

# Sample first 15 plain lines
for i in plain_idxs[:15]:
    g_e = find_prev_G(lines, i)
    other = 'B' if '1977Da02' in lines[i] else 'A'
    # Check mrg
    # simplified: just show the G energy and the line
    print(f"  ADP L{i+1}: G={g_e}  [{lines[i].rstrip()}]")
