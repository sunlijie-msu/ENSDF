import csv
import sys
import math

def parse_val_err(val_str):
    val_str = val_str.replace('< <', '<').replace('< ', '<').strip()
    if not val_str: return '', ''
    if '<' in val_str:
        return val_str.replace('<', '').strip(), 'LT'
    if '±' in val_str:
        v, e = val_str.split('±')
        v = v.strip()
        e = e.strip()
        v_parts = v.split('.')
        if len(v_parts) == 2:
            decimals = len(v_parts[1])
            try:
                err_int = str(int(round(float(e) * (10**decimals))))
            except:
                err_int = e
            return v, err_int
        else:
            return v, str(int(round(float(e))))
    return val_str, ''

mrg_1983 = {
    5577: {
        1436.2: ('0.48', ''), 1975.73: ('38', ''), 2030.93: ('100', ''),
        2854.9: ('21', ''), 2964.95: ('0.71', ''), 3200.3: ('0.95', ''),
        3688.69: ('4.8', ''), 4345.67: ('10', ''), 4910.4: ('0.71', 'LT'),
        5115.0: ('1.4', 'LT'), 5429.6: ('62', ''), 5576.0: ('0.24', 'LT')
    },
    5635: {
        996.1: ('0.44', ''), 1217.6: ('0.44', ''), 1843.3: ('2.5', ''),
        1861.16: ('1.0', ''), 2505.87: ('4.1', ''), 2913.9: ('0.73', ''),
        3054.6: ('15', ''), 3747.69: ('1.9', ''), 4404.67: ('0.58', ''),
        4969.4: ('16', ''), 5174.0: ('2.9', ''), 5488.6: ('0.44', 'LT'),
        5635.0: ('100', '')
    },
    5673: {
        1254.6: ('0.41', ''), 1317.7: ('0.81', ''), 1731.9: ('2.0', ''),
        1880.3: ('1.9', ''), 1898.16: ('0.54', ''), 2542.87: ('2.8', ''),
        3091.6: ('6.6', ''), 3514.10: ('10', ''), 3784.69: ('1.8', ''),
        5006.4: ('8.2', ''), 5211.0: ('0.54', 'LT'), 5525.6: ('0.41', 'LT'),
        5672.0: ('100', '')
    }
}

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
        if "RI$other:" in line or "Only observed in 1983Wa27" in line or "Observed in 1983Wa27" in line:
            i += 1
            continue
            
    if current_level and line.startswith(" 34CL  G"):
        eg_str = line[9:19].strip()
        try:
            eg = float(eg_str)
        except:
            new_lines.append(line)
            i += 1
            continue
            
        csv_match, csv_diff = None, 15.0
        for approx_eg, (v2011, v1983) in csv_data[current_level].items():
            if abs(approx_eg - eg) < csv_diff:
                csv_diff = abs(approx_eg - eg)
                csv_match = approx_eg
                
        is_from_2011 = False
        v2011_val, v1983_val_csv = "", ""
        if csv_match is not None:
            v2011_val, v1983_val_csv = csv_data[current_level][csv_match]
            is_from_2011 = v2011_val.strip() != ""
            
        mrg_match, mrg_diff = None, 20.0
        for mrg_eg, mrg_val in mrg_1983[current_level].items():
            if abs(mrg_eg - eg) < mrg_diff:
                mrg_diff = abs(mrg_eg - eg)
                mrg_match = mrg_eg
                
        v1983_val_mrg, v1983_err_mrg = "", ""
        if mrg_match is not None:
            v1983_val_mrg, v1983_err_mrg = mrg_1983[current_level][mrg_match]
            
        mod_line = line.replace("\n", "").replace("\r", "").ljust(80, ' ')
        
        if is_from_2011:
            ri, dri = parse_val_err(v2011_val)
            ri_f = ri[:7].strip().ljust(7)
            dri_f = dri[:2].strip().ljust(2)
            mod_line = mod_line[:22] + ri_f + " " + dri_f + mod_line[32:]
            mod_line = mod_line[:76] + 'F' + mod_line[77:]
            new_lines.append(mod_line[:80] + "\n")
            
            v1983_final = v1983_val_mrg if v1983_val_mrg else v1983_val_csv
            if v1983_final.strip() != "":
                if v1983_err_mrg == 'LT':
                    v1983_final = "<" + v1983_final
                cmt = f" 34CL cG RI$other: {v1983_final.strip()} (1983Wa27)"
                new_lines.append(cmt.ljust(80) + "\n")
        else:
            mod_line = mod_line[:76] + ' ' + mod_line[77:]
            if v1983_val_mrg.strip():
                ri_f = v1983_val_mrg[:7].strip().ljust(7)
                dri_f = v1983_err_mrg[:2].strip().ljust(2)
                mod_line = mod_line[:22] + ri_f + " " + dri_f + mod_line[32:]
            new_lines.append(mod_line[:80] + "\n")
            
            cmt = " 34CL cG $Observed in 1983Wa27 but not in 2011Fr04."
            new_lines.append(cmt.ljust(80) + "\n")
            
        i += 1
        continue
        
    new_lines.append(line)
    i += 1

with open("A34/Cl34/new/Cl34_33s_p_g.ens", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Done")