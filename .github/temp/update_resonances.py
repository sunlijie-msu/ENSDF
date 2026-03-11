import csv

csv_data = {5577: {}, 5635: {}, 5673: {}}

with open("A34/Cl34/raw/2011FR04.csv", "r", encoding="utf-8-sig") as f:
    r = csv.reader(f)
    next(r)
    next(r)
    for row in r:
        if len(row) >= 4 and row[1].strip(): csv_data[5577][float(row[1])] = (row[2].strip(), row[3].strip())
        if len(row) >= 7 and row[4].strip(): csv_data[5635][float(row[4])] = (row[5].strip(), row[6].strip())
        if len(row) >= 10 and row[7].strip(): csv_data[5673][float(row[7])] = (row[8].strip(), row[9].strip())

with open("A34/Cl34/new/Cl34_33s_p_g.ens", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
current_level = None

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith(" 34CL  L"):
        if "5577.6" in line: current_level = 5577
        elif "5635.7" in line: current_level = 5635
        elif "5673.0" in line: current_level = 5673
        else: current_level = None
        new_lines.append(line)
        i += 1
        continue
    
    if current_level and line.startswith(" 34CL cG "):
        if "RI$other:" in line or "Only observed in 1983Wa27" in line:
            i += 1
            continue
            
    if current_level and line.startswith(" 34CL  G"):
        # Append the line itself and modify its 77th column if necessary
        eg_str = line[9:19].strip()
        try:
            eg = float(eg_str)
        except:
            new_lines.append(line)
            i += 1
            continue
            
        best_match = None
        best_diff = 15.0
        for approx_eg, (v2011, v1983) in csv_data[current_level].items():
            if abs(approx_eg - eg) < best_diff:
                best_diff = abs(approx_eg - eg)
                best_match = approx_eg
                
        v2011, v1983 = "", ""
        if best_match is not None:
            v2011, v1983 = csv_data[current_level][best_match]
            
        is_from_2011 = v2011.strip() != ""
        
        # update line format for F flag
        mod_line = line.replace("\n", "").replace("\r", "").ljust(80, ' ')
        if is_from_2011:
            mod_line = mod_line[:76] + 'F' + mod_line[77:]
        else:
            mod_line = mod_line[:76] + ' ' + mod_line[77:]
        mod_line = mod_line[:80] + "\n"
        new_lines.append(mod_line)
        
        if is_from_2011:
            if v1983.strip() != "":
                cmt = f" 34CL cG RI$other: {v1983.strip()} (1983Wa27)"
                new_lines.append(cmt.ljust(80) + "\n")
        else:
            cmt = " 34CL cG $Only observed in 1983Wa27 but not in 2011Fr04."
            new_lines.append(cmt.ljust(80) + "\n")
            
        i += 1
        continue
        
    new_lines.append(line)
    i += 1

with open("A34/Cl34/new/Cl34_33s_p_g.ens", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Update completed successfully!")
