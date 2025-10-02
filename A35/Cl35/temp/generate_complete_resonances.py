import csv, re

# MeV to keV mapping
level_map = {
    '4.35': 4347.2, '4.62': 4624.2, '4.77': 4766.9, '4.84': 4841.7,
    '4.86': 4855.7, '4.89': 4885.0, '5.01': 5010.4, '5.17': 5166.7,
    '5.22': 5216.2, '5.40': 5403.6, '5.59': 5586.0, '5.60': 5600.1,
    '5.64': 5646.0, '5.65': 5646.0, '5.66': 5656.0, '5.68': 5683.0,
    '5.76': 5759.0, '5.81': 5806.0, '6.10': 6107.2, '6.11': 6107.2, '6.18': 6181.0
}

# Ef_keV header values
ef_header = [0, 1219.3, 1763.4, 2644.7, 2694.7, 3003.7, 3163.9, 3920.7, 
             3944.1, 3979, 4059.4, 4114, 4174.7, 4180.1]

# Read CSV
with open('A35/Cl35/temp/1976ME12_Branching_Ratios.csv', 'r') as f:
    data = list(csv.reader(f))

output = []
total_resonances = 0
total_gammas = 0

# Process all 47 resonances
for row_idx in range(2, len(data)):
    row = data[row_idx]
    ep = row[0].strip()
    ei_str = row[1].strip()
    
    if not ep or not ei_str:
        continue
    
    ei = float(ei_str)
    total_resonances += 1
    
    # L-record: Ex at cols 10-19, Ep at cols 65-74
    ex_str = f'{ei:.1f}' if ei == int(ei) else str(ei)
    l_line = f' 35CL  L {ex_str:<10}' + ' ' * 45 + f'{ep:<10}'
    l_line = l_line[:80].ljust(80)  # Ensure exactly 80 chars
    output.append(l_line)
    
    # cL comment
    cl_line = f' 35CL cL $\\|w|g (1976Me12,Ep={ep} keV)'
    cl_line = cl_line[:80].ljust(80)  # Ensure exactly 80 chars
    output.append(cl_line)
    
    # Collect ALL gammas
    all_gammas = []
    
    # (1) Regular Ef_keV gammas (columns 2-15)
    for idx, br_value in enumerate(row[2:16]):
        if not br_value.strip():
            continue
        ef_val = ef_header[idx]
        eg = ei - ef_val
        
        br_clean = br_value.strip()
        is_limit = br_clean.startswith('<')
        if is_limit:
            br_clean = br_clean[1:]
        
        all_gammas.append((eg, br_clean, is_limit))
    
    # (2) 'Other final levels' gammas (columns 16+)
    for col in row[16:]:
        if not col.strip():
            continue
        # Parse all MeV(BR) in this cell
        matches = re.findall(r'([0-9.]+)\(([0-9.<>]+)\)', col)
        for mev_str, br_str in matches:
            if mev_str in level_map:
                ef_kev = level_map[mev_str]
                eg = ei - ef_kev
                
                is_limit = br_str.startswith('<')
                br_clean = br_str[1:] if is_limit else br_str
                
                all_gammas.append((eg, br_clean, is_limit))
    
    # Sort by ascending Egamma
    all_gammas.sort(key=lambda x: x[0])
    total_gammas += len(all_gammas)
    
    # Generate G-records
    for eg, br_str, is_limit in all_gammas:
        # Eg at cols 10-19
        eg_str = f'{eg:.1f}' if eg != int(eg) else str(int(eg))
        g_line = f' 35CL  G {eg_str:<10}'
        
        # RI at cols 23-29 (LEFT-JUSTIFIED)
        g_line += ' ' * 3 + br_str[:7].ljust(7)
        
        # DRI at cols 30-31
        if is_limit:
            g_line += 'LT'
        else:
            g_line += '  '
        
        # Pad to 80 chars
        g_line = g_line[:80].ljust(80)  # Ensure exactly 80 chars
        output.append(g_line)

# Write output - preserve trailing spaces by writing lines individually
with open('A35/Cl35/temp/1976ME12_COMPLETE_RESONANCES.txt', 'w') as f:
    for line in output:
        f.write(line + '\n')

print(f'COMPLETE resonance generation:')
print(f'  Resonances processed: {total_resonances}')
print(f'  Total gamma transitions: {total_gammas}')
print(f'  Output lines: {len(output)}')
print(f'  File: 1976ME12_COMPLETE_RESONANCES.txt')
