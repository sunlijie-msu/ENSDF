import sys

def check_gamma_changes(diff_file):
    with open(diff_file, 'r', encoding='latin-1') as f:
        lines = f.readlines()
    
    pairs = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('- 35CL  G'):
            if i+1 < len(lines) and lines[i+1].startswith('+ 35CL  G'):
                pairs.append((lines[i], lines[i+1]))
                i += 2
                continue
        i += 1
    
    print(f"Auditing {len(pairs)} Gamma record modifications...")
    energy_changes = 0
    for old, new in pairs:
        old_e = old[10:20]
        new_e = new[10:20]
        if old_e != new_e:
            print(f"ENERGY CHANGE: '{old_e}' -> '{new_e}'")
            print(f"  Old: {old.strip()}")
            print(f"  New: {new.strip()}")
            energy_changes += 1
            
    if energy_changes == 0:
        print("SUCCESS: Zero Gamma energy changes found across the entire session.")
    else:
        print(f"WARNING: Found {energy_changes} Gamma energy modifications.")

if __name__ == "__main__":
    check_gamma_changes(sys.argv[1])
