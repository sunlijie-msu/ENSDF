# Verify all proposed new G-record lines for the 9157.1 level

def make_g(energy, ri, dri, m="", mr="", dmr="", cc="", dcc=""):
    """Build an exact 80-char G-record for 35CL."""
    prefix = " 35CL  G "       # cols 1-9 (9 chars)
    e_field = energy.ljust(10)   # cols 10-19 (10 chars)
    de_field = "  "              # cols 20-21 (2 chars, DE blank)
    sp22 = " "                   # col 22
    ri_field = ri.ljust(7)       # cols 23-29 (7 chars)
    dri_field = dri.ljust(2)     # cols 30-31 (2 chars)
    sp32 = " "                   # col 32
    m_field   = m.ljust(9)       # cols 33-41 (9 chars)
    mr_field  = mr.ljust(8)      # cols 42-49 (8 chars)
    dmr_field = dmr.ljust(6)     # cols 50-55 (6 chars)
    cc_field  = cc.ljust(7)      # cols 56-62 (7 chars)
    dcc_field = dcc.ljust(2)     # cols 63-64 (2 chars)
    tail = " " * 16              # cols 65-80 (16 chars)
    line = prefix + e_field + de_field + sp22 + ri_field + dri_field + sp32 + m_field + mr_field + dmr_field + cc_field + dcc_field + tail
    return line

lines = {
    "G 3942.4":    make_g("3942.4",  "17",  "5"),
    "G 4386.9":    make_g("4386.9",  "16",  "4"),
    "G 4978.8 LT": make_g("4978.8",  "37",  "LT"),
    "G 4983.3 LT": make_g("4983.3",  "37",  "LT"),
    "G 6153.9":    make_g("6153.9",  "20",  "5"),
    "G 6462.5":    make_g("6462.5",  "3",   "2"),
    "G 6510.8":    make_g("6510.8",  "7",   "4"),
    "G 7393.1":    make_g("7393.1",  "17",  "5"),
}

# G 5993.7: has full fields
lines["G 5993.7"] = make_g("5993.7", "22", "6", m="M1+E2", mr="+0.10", dmr="2", cc="1.59E-3", dcc=" 2")
# G 9155.8: has (E1) in M field
lines["G 9155.8"] = make_g("9155.8", "100", "9", m="(E1)")

print("Verification of new lines:")
print("=" * 90)
all_ok = True
for name, line in sorted(lines.items()):
    length = len(line)
    ok = "✅" if length == 80 else "❌"
    if length != 80:
        all_ok = False
    # Verify key field positions
    ri_val = line[22:29].rstrip()
    dri_val = line[29:31].rstrip()
    print(f"{ok} {name:15} len={length} | RI[23-29]='{line[22:29]}' DRI[30-31]='{line[29:31]}' | '{line}'")

print()
if all_ok:
    print("✅ All lines are 80 chars")
else:
    print("❌ Some lines have wrong length!")
    
print()
print("Full lines for file edit:")
print("-"*90)
for name, line in sorted(lines.items()):
    print(f"# {name}")
    print(repr(line))
