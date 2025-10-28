import csv

# 1. Parse Eg CSV to get row numbers
eg_data = {}
eg_lines = []
with open('A35/Cl35/raw/2001VO24_Eg.csv', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            eg_lines.append(line)

eg_header = [int(x) for x in eg_lines[0].split(',')]
for row_num, row_text in enumerate(eg_lines[1:], 1):
    values = row_text.split(',')
    for col_num, eg_str in enumerate(values):
        eg_str = eg_str.strip()
        if eg_str and eg_str.lower() != 'null':
            exi = eg_header[col_num]
            eg = int(eg_str)
            eg_data[(exi, eg)] = row_num

# 2. Parse BR CSV
br_data = {}
br_lines = []
with open('A35/Cl35/raw/2001VO24_BR.csv', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            br_lines.append(line)

br_header = [int(x) for x in br_lines[0].split(',')]
for row_num, row_text in enumerate(br_lines[1:], 1):
    values = row_text.split(',')
    for col_num, br_str in enumerate(values):
        br_str = br_str.strip()
        if br_str and br_str.lower() != 'null':
            exi = br_header[col_num]
            br = int(br_str)
            br_data[(exi, row_num)] = br

# 3. Process ENSDF file and add BR values
output_lines = []
current_exi = None

with open('A35/Cl35/raw/2001VO24.ens', 'r') as f:
    for line in f:
        if len(line) < 10:
            output_lines.append(line.rstrip('\n'))
            continue
        
        record_type = line[7:8].strip()
        
        if record_type == 'L':
            # L-record: extract energy for tracking
            e_str = line[9:19].strip()
            if e_str:
                current_exi = int(float(e_str))
            output_lines.append(line.rstrip('\n'))
        
        elif record_type == 'G' and current_exi:
            # G-record: add BR in RI field (columns 23-29)
            e_str = line[9:19].strip()
            if e_str:
                eg = int(float(e_str))
                row_num = eg_data.get((current_exi, eg))
                if row_num:
                    br_key = (current_exi, row_num)
                    br = br_data.get(br_key)
                    
                    if br:
                        # Build G-record with BR in RI field
                        # Columns 1-9: NUCID, type (' 35CL  G ')
                        # Columns 10-19: Energy (Eg)
                        # Columns 20-21: DE (blank)
                        # Columns 22: Space
                        # Columns 23-29: RI (BR value, left-justified)
                        # Columns 30-80: rest (blank)
                        
                        nucid = line[0:6]  # ' 35CL '
                        space1 = line[6:7]
                        record = line[7:8]  # 'G'
                        space2 = line[8:9]  # ' '
                        energy = line[9:19]  # Energy field
                        de = line[19:22]  # DE field + space
                        
                        # Format BR in RI field (columns 23-29, left-justified)
                        br_str = str(br).ljust(7)  # Left-justify in 7-char field
                        
                        # Rest of line (columns 30-80)
                        rest = line[30:80] if len(line) >= 30 else ' ' * 50
                        
                        new_line = nucid + space1 + record + space2 + energy + de + br_str + rest
                        
                        # Ensure exactly 80 characters
                        if len(new_line) < 80:
                            new_line = new_line.ljust(80)
                        elif len(new_line) > 80:
                            new_line = new_line[:80]
                        
                        output_lines.append(new_line)
                    else:
                        output_lines.append(line.rstrip('\n'))
                else:
                    output_lines.append(line.rstrip('\n'))
        else:
            output_lines.append(line.rstrip('\n'))

# Write output file
with open('A35/Cl35/raw/2001VO24.ens', 'w') as f:
    for line in output_lines:
        f.write(line + '\n')

print('ENSDF file updated with BR values')
print(f'Total lines written: {len(output_lines)}')
