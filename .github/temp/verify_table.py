
import re

ensdf_path = r"d:\X\ND\ENSDF\XUNDL\2026TAAA_CLR1074_173W.ens"

data_raw = """
1453.3	424.4	424.4	Band 5
1359.8	517.9	517.9	Band 6
1114.5	763.2	763.2	Band 5
1292.8	867.2	867.2	Band 6
1009.9	867.8		Band 6
1251.7	908.3	908.3	
959.4	918.3	918.3	Band 1
1025.5	1134.5	1134.5	Band 2
743	1134.7		Band 2
956.7	1203.3	1203.3	Band 5
673.9	1203.8		Band 5
844	1316	1316	Band 6
818.4	1341.6	1341.6	
794.3	1365.7	1365.7	Band 1
617.2	1542.8	1542.8	
560.5	1599.5	1599.5	Band 2
440.9	1719.1	1719.1	
361.9	1798.1	1798.1	
351.9	1808.1	1808.1	
"""

flag_map_check = {
    'A': 'Band 5',
    'a': 'Band 6',
    'B': 'Band 1',
    'b': 'Band 2',
    'C': 'Band 3',
    'c': 'Band 4',
}

level_flags = {}
with open(ensdf_path, 'r') as f:
    for line in f:
        if line.startswith("173W   L"):
            # Ensure 80 cols
            clean_line = line.rstrip('\n')
            padded = clean_line.ljust(80)
            
            try:
                e_val = float(padded[9:19].strip())
                flag = padded[76] # Col 77 is index 76
                level_flags[int(e_val)] = flag
            except:
                pass


print("| Gamma | Final Level | Levels need to be added | Final Level's Band | Flag | Match Check |")
print("|---|---|---|---|---|---|")

for line in data_raw.strip().split('\n'):
    parts = line.split('\t')
    g = parts[0].strip()
    lvl = parts[1].strip()
    added = parts[2].strip() if len(parts)>2 else ""
    band = parts[3].strip() if len(parts)>3 else ""
    
    try:
        val = int(float(lvl))
        # Find flag with tolerance
        flag = " "
        min_d = 5.0
        for k, v in level_flags.items():
            if abs(k - val) < min_d:
                min_d = abs(k-val)
                flag = v
    except:
        flag = " "

    # Check
    expected = flag_map_check.get(flag, "")
    
    # Logic: 
    # If User Band is present, does it match Expected?
    # Strip "Band " from user string for easier check? No, map logic is consistent.
    
    norm_user = band.lower().replace(" ","")
    norm_exp = expected.lower().replace(" ","")
    
    if band == "":
        status = "-"
    elif norm_user == norm_exp:
        status = "OK"
    else:
        status = f"MISMATCH (Exp {expected})"
        
    print(f"| {g} | {lvl} | {added} | {band} | {flag} | {status} |")
