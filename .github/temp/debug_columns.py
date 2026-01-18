with open('d:\\X\\ND\\ENSDF\\A34\\Cl34\\new\\Cl34_31p_a_ng.ens', 'r') as f:
    lines = f.readlines()
    for i in [38, 40, 46, 48, 51]:
        line = lines[i].rstrip('\n')
        print("Line", i+1, "len=", len(line))
        print("  Cols 70-80:", repr(line[69:80]))
        print("  Col 77:", repr(line[76]) if len(line) > 76 else "MISSING")
        print("  Col 78:", repr(line[77]) if len(line) > 77 else "MISSING")
        print("  Col 79:", repr(line[78]) if len(line) > 78 else "MISSING")
        print("  Col 80:", repr(line[79]) if len(line) > 79 else "MISSING")
        print()
