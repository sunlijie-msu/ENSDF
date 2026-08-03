"""Extract E-record fields from the 1.5266_s template file (limit records)."""
PATH = r"A34\S34\new\S34_34cl_ec_decay_1.5266_s.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

for i, line in enumerate(lines, 1):
    if len(line) >= 80 and line[6] == " " and line[7] == "E":
        print(f"L{i} len={len(line)}")
        print(f"  [1-9]=[{line[0:9]}]")
        print(f"  E(10-19)=[{line[9:19]}] DE(20-21)=[{line[19:21]}]")
        print(f"  IB(22-29)=[{line[21:29]}] DIB(30-31)=[{line[29:31]}]")
        print(f"  IE(32-39)=[{line[31:39]}] DIE(40-41)=[{line[39:41]}]")
        print(f"  LOGFT(42-49)=[{line[41:49]}] DFT(50-55)=[{line[49:55]}]")
        print(f"  TI(65-74)=[{line[64:74]}] DTI(75-76)=[{line[74:76]}] C(77)=[{line[76:77]}] Q(80)=[{line[79:80]}]")
        print()
