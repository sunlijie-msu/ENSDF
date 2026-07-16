import re

# Quick debug: check the cG comments for first 3 gammas
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    ens_lines = [l.rstrip('\n') for l in f.readlines()]
ens_lines = [l + ' ' * (80 - len(l)) if len(l) < 80 else l for l in ens_lines]

levels = []
current_level = None
current_gamma = None

for line_idx, line in enumerate(ens_lines):
    col7 = line[6]
    col8 = line[7]
    col6 = line[5]
    
    if col8 == 'L' and col6 == ' ' and col7 == ' ':
        if current_level is not None:
            levels.append(current_level)
        current_level = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'J': line[22:39].strip(), 'gammas': [], 'cL_comments': []
        }
        current_gamma = None
    
    elif col8 == 'G' and col6 == ' ' and col7 == ' ':
        current_gamma = {
            'line_idx': line_idx, 'line': line,
            'E': line[9:19].strip(), 'DE': line[19:21].strip(),
            'RI': line[22:29].strip(), 'DRI': line[29:31].strip(),
            'M': line[32:41].strip(), 'c_comments': []
        }
        if current_level is not None:
            current_level['gammas'].append(current_gamma)
    
    elif col7 == 'c' and col8 == 'G':
        if current_gamma is not None:
            current_gamma['c_comments'].append(line)

if current_level is not None:
    levels.append(current_level)

def normalize_unc(text):
    return re.sub(r'\{I([+]?\d+(?:[-]\d+)?)\}', r'(\1)', text)

# Check source #0: Ex ~4482, Eg ~858
for lv in levels:
    try:
        if abs(float(lv['E']) - 4482.0) < 1.0:
            print("Level: E=" + lv['E'] + " DE=" + lv['DE'])
            for g in lv['gammas']:
                try:
                    if abs(float(g['E']) - 858.1) < 0.2:
                        print("  Gamma: E=" + g['E'] + " RI=" + g['RI'])
                        for c in g['c_comments']:
                            print("    Raw cG: [" + repr(c) + "]")
                            nc = normalize_unc(c)
                            print("    Norm:   [" + nc + "]")
                        
                        cg_text = ' '.join([normalize_unc(c) for c in g['c_comments']])
                        print("  cg_text: [" + cg_text + "]")
                        
                        expected = "R{-ADO}=1.68(17)"
                        print("  Checking for: [" + expected + "]")
                        print("  Result: " + str(expected in cg_text))
                except:
                    pass
    except:
        pass
