"""Extract E-record fields from the S34 34Clm decay file to replicate layout."""
PATH = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

for i, line in enumerate(lines, 1):
    if len(line) >= 80 and line[6] == " " and line[7] == "E":
        print(f"L{i} len={len(line)}")
        print(f"  IB(22-29)=[{line[21:29]}] DIB(30-31)=[{line[29:31]}]")
        print(f"  IE(32-39)=[{line[31:39]}] DIE(40-41)=[{line[39:41]}]")
        print(f"  LOGFT(42-49)=[{line[41:49]}] DFT(50-55)=[{line[49:55]}]")
        print(f"  TI(65-74)=[{line[64:74]}] DTI(75-76)=[{line[74:76]}]")
        print()
