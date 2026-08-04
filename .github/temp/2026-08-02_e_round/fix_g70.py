"""Fix G70 TI field shift (left-justify TI at col 65), verify 80 chars."""
PATH = r"A34\Cl34\new\Cl34_34cl_it_decay_31.99_m.ens"
with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

ln = lines[69]  # line 70
print("OLD:", repr(ln))
assert ln[7] == "G" and ln[9:19].strip() == "146.36"

# fields: prefix(1-64) + TI(65-74) + DTI(75-76) + C(77) + (78-79) + Q(80)
prefix = ln[:64]
ti_raw = ln[64:74]
rest = ln[74:80]
print(f"prefix=[{prefix}]")
print(f"TI=[{ti_raw}] DTI/C/Q rest=[{rest}]")

ti_val = ti_raw.strip()
new_ti = ti_val.ljust(10)
new = prefix + new_ti + rest
print("NEW:", repr(new))
print("len:", len(new))
assert len(new) == 80
print("TI slice:", repr(new[64:74]))
