import sys

with open("A34/Cl34/new/Cl34_33s_p_g.ens", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
current_level = None

for line in lines:
    if line.startswith(" 34CL  L"):
        if "5577.6" in line: current_level = 5577
        elif "5635.7" in line: current_level = 5635
        elif "5673.0" in line: current_level = 5673
        else: current_level = None
        new_lines.append(line)
        continue
        
    if current_level and line.startswith(" 34CL  G"):
        mod_line = line.rstrip("\r\n").ljust(80)
        # DRI field is at cols 30-31, index 29-30.
        # But wait, because I appended an extra char, shifted everything right? No, I did:
        # mod_line = mod_line[:22] + ri_f + dri_f + mod_line[31:]
        # Which replaces index 22 to 30. (22 + 7 + 2 = 31). So it replaced exactly 9 chars.
        # But what if dri_f was 2 chars and the line originally had L T ?
        # " LT " became "LTT"?
        # Let's clean the DRI field. Cols 30-31 is index 29-30.
        # So chars 29, 30. And char 31 is col 32, which MUST be blank.
        # If char 31 is not blank, I need to fix it.
        # Let's extract col 30-32 (index 29-31).
        dri_str = mod_line[29:32]
        new_dri = dri_str[:2]
        if dri_str == 'LTT': new_dri = 'LT'
        elif dri_str.endswith('3') and dri_str[:2] == '23': new_dri = '23'
        elif dri_str.endswith('6') and dri_str[:2] == '66': new_dri = '66'
        elif dri_str.endswith('2') and dri_str[:2] == '12': new_dri = '12'
        elif dri_str.endswith('4') and dri_str[:2] == '14': new_dri = '14'
        elif dri_str.endswith('5') and dri_str[:2] == '55': new_dri = '55'
        
        # We can just recalculate the DRI. It is safer.
        ri_val = mod_line[22:29].strip()
        if "LT" in mod_line[29:33]:
            new_dri = "LT"
        else:
            # Let's just fix the trailing character at col 32 (index 31).
            # It should be ' '.
            pass
            
        mod_line = mod_line[:31] + ' ' + mod_line[32:]
        new_lines.append(mod_line[:80] + "\n")
        continue

    new_lines.append(line)

with open("A34/Cl34/new/Cl34_33s_p_g.ens", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Done")
