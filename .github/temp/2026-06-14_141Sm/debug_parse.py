import re
lines = open('XUNDL/2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()
# Find which line has 'G' at pos 7 but non-numeric at pos 9-18
for i, line in enumerate(lines):
    if len(line) >= 9 and line[7] == 'G' and line[5] == ' ':
        eg = line[9:19].strip()
        if not eg:
            print(f'Line {i+1}: pos7=G but empty eg: [{line.rstrip()}]')
        else:
            try:
                float(eg)
            except:
                print(f'Line {i+1}: pos7=G non-numeric eg=[{eg}] line=[{line.rstrip()}]')
