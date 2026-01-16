
import sys
filepath = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_32s_3he_pg.ens'
with open(filepath, 'r') as f:
    lines = f.readlines()

targets = [128, 136, 158, 165, 167, 169]
for t in targets:
    if t <= len(lines):
        l = lines[t-1]
        c77 = l[76] if len(l) > 76 else 'MISS'
        c80 = l[79] if len(l) > 79 else 'MISS'
        l_clean = l.replace('\r', '').replace('\n', '')
        print("Line " + str(t) + ": col 77='" + c77 + "', col 80='" + c80 + "', len=" + str(len(l_clean)))
        print("Content: |" + l_clean + "|")
