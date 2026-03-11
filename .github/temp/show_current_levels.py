lines = open('A34/Cl34/raw/1977DA02.ens', 'r').readlines()

target_levels = {'2610.6': 36, '2721.4': 41, '3128.9': 47, '3333.9': 50}

for level, start_idx in target_levels.items():
    print(f"LEVEL {level}:")
    i = start_idx
    print(f"  {lines[i].rstrip()}")
    j = i + 1
    while j < len(lines):
        lstr = lines[j].rstrip()
        if ' 34CL  G ' in lstr:
            print(f"  {lstr}")
            j += 1
        elif ' 34CL  L ' in lstr:
            break
        else:
            j += 1
    print()
