"""Inspect pre-existing data-record alignment at lines 58 and 70."""
PATH = r"A34\Cl34\new\Cl34_34cl_it_decay_31.99_m.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

print("RULER")
print("11111111112222222222333333333344444444445555555555666666666677777777778888888889")
print("12345678901234567890123456789012345678901234567890123456789012345678901234567890")

for no in (58, 70):
    ln = lines[no - 1]
    print(f"\nL{no} len={len(ln)}")
    print(ln)
    # field slices
    if ln[7] == "L":
        print(f"  E(10-19)=[{ln[9:19]}] DE(20-21)=[{ln[19:21]}]")
        print(f"  J(23-39)=[{ln[22:39]}] T(40-49)=[{ln[39:49]}] DT(50-55)=[{ln[49:55]}]")
        print(f"  C(77)=[{ln[76:77]}] MS(78-79)=[{ln[77:79]}] Q(80)=[{ln[79:80]}]")
    if ln[7] == "G":
        print(f"  E(10-19)=[{ln[9:19]}] DE(20-21)=[{ln[19:21]}]")
        print(f"  RI(23-29)=[{ln[22:29]}] DRI(30-31)=[{ln[29:31]}] M(33-41)=[{ln[32:41]}]")
        print(f"  MR(42-49)=[{ln[41:49]}] DMR(50-55)=[{ln[49:55]}] CC(56-62)=[{ln[55:62]}]")
        print(f"  DCC(63-64)=[{ln[62:64]}] TI(65-74)=[{ln[64:74]}] DTI(75-76)=[{ln[74:76]}]")
        print(f"  C(77)=[{ln[76:77]}] Q(80)=[{ln[79:80]}]")
