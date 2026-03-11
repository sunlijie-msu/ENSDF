import re
import sys

file_path = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_5635 = False
last_eg = None

updates = {
    1843.9: ("3.7", "7 ", "2.5"),
    1975.2: ("0.3", "LT", None),
    1989.3: ("0.4", "LT", None),
    2003.9: ("0.3", "LT", None),
    2506.5: ("3.9", "4 ", "4.1"),
    2914.5: ("1.0", "3 ", "0.7"),
    3024.5: ("0.4", "LT", None),
    3055.2: ("12.2", "7 ", "14.5"),
    3259.8: ("0.3", "LT", None),
    3454.4: ("0.5", "LT", None),
    3477.6: ("0.6", "3 ", None), 
    3748.2: ("1.8", "3 ", "1.9"),
    4405.1: ("0.6", "4 ", "0.6"),
    4969.7: ("15.4", "10", "15.9"),
    5174.3: ("2.2", "7 ", "2.9"),
    5488.8: ("0.65", "LT", "<0.4"),
    5635.2: ("100", "  ", "100")
}

for i, line in enumerate(lines):
    if line.startswith(" 34CL  L 5635"):
        in_5635 = True
        new_lines.append(line)
        continue
    if in_5635 and line.startswith(" 34CL  L "):
        in_5635 = False
        new_lines.append(line)
        continue
        
    if in_5635:
        if line.startswith(" 34CL  G "):
            try:
                eg_str = line[9:19].strip()
                if eg_str:
                    eg = float(eg_str)
                    last_eg = eg
                    if eg in updates:
                        fr_ri, fr_dri, wa_ri = updates[eg]
                        fr_ri_str = fr_ri.ljust(7)
                        fr_dri_str = fr_dri.ljust(2)
                        
                        line = line[:22] + fr_ri_str + fr_dri_str + line[31:]
            except ValueError:
                pass
        
        elif line.startswith(" 34CL cG RI$other:"):
            if last_eg in updates:
                fr_ri, fr_dri, wa_ri = updates[last_eg]
                if wa_ri:
                    line = f" 34CL cG RI$other: {wa_ri}".ljust(80) + "\n"
                else: 
                    line = "" # skip it
            
    if line != "":
        new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
