import os

file_path = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens"

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "34CL cL S$0.010 {I2} for L=1, 0.017 {I" in line:
        new_lines.append(" 34CL cL S$0.010 {I2} for L=1, 0.017 {I3} for L=3 (2014Pa44).                  \n")
    elif "34CL cL S$for L=2.C{+2}S=0.0059 {I5}" in line:
        new_lines.append(" 34CL cL S$for L=2. C{+2}S=0.0059 {I5} for L=1, 0.034 {I3} for L=3.            \n")
    elif "34CL cL S$for L=1.C{+2}S=0.0095 {I7}" in line:
        new_lines.append(" 34CL cL S$for L=1. C{+2}S=0.0095 {I7} for L=0.                                \n")
    elif "34CL cL S$for L=2.C{+2}S=0.020 {I1} f" in line:
        new_lines.append(" 34CL cL S$for L=2. C{+2}S=0.020 {I1} for L=3.                                 \n")
    elif "34CL cL S$for L=3.C{+2}S=0.057 {I3} f" in line:
        new_lines.append(" 34CL cL S$for L=3. C{+2}S=0.057 {I3} for L=2.                                 \n")
    elif "34CL cL S$for L=1+3: 0.0060 {I5} for L" in line:
        new_lines.append(" 34CL cL S$for L=1+3: 0.0060 {I5} for L=1, 0.022 {I2} for L=3. C{+2}S=0.200 {I8}\n")
    elif "34CL cL S$for L=1+3: 0.0081 {I7} for L" in line:
        new_lines.append(" 34CL cL S$for L=1+3: 0.0081 {I7} for L=1, 0.054 {I2} for L=3. C{+2}S=0.247 {I4}\n")
    elif "34CL cL S$0.0028 {I6 for L=1, 0.016 {" in line:
        new_lines.append(" 34CL cL S$0.0028 {I6} for L=1, 0.016 {I1} for L=3.                            \n")
    elif "34CL cL S$0.012 {I1} for L=1, 0.039 {I" in line:
        new_lines.append(" 34CL cL S$0.012 {I1} for L=1, 0.039 {I3} for L=3.                            \n")
    else:
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)
