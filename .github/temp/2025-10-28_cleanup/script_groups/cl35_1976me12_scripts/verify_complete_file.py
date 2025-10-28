"""
Cross-verify complete file against user's original data table.
"""

# Sample verification data from user's table
verification_data = [
    (7067.5, 716.0, 1.0, 0.3, 0.1),    # First resonance
    (7839.1, 1510.2, 1.0, 4.8, 1.4),   # Middle resonance
    (8324.5, 2009.9, 1.3, 1.6, 0.5)    # Last resonance
]

with open('A35/Cl35/temp/1976ME12_COMPLETE.ens', 'r') as f:
    lines = f.readlines()

print("=" * 80)
print("CROSS-VERIFICATION AGAINST USER'S ORIGINAL DATA TABLE")
print("=" * 80)
print()

all_match = True

for ex, ep, dep, gamma_eV, unc_eV in verification_data:
    target_ex = f"{ex:.1f}"
    found = False
    
    for i, line in enumerate(lines):
        # Check for L-record with matching Ex
        if line[7:8] == 'L' and line[6:7] == ' ' and target_ex in line[9:20]:
            ex_field = line[9:19].strip()   # Cols 10-19 (Python index 9:19)
            de_field = line[19:21].strip()  # Cols 20-21 (Python index 19:21)
            ep_field = line[64:74].strip()  # Cols 65-74 (Python index 64:74)
            dep_field = line[74:76].strip() # Cols 75-76 (Python index 74:76)
            
            # Get gamma width from next line (cL comment)
            next_line = lines[i+1] if i+1 < len(lines) else ''
            gamma_str = ''
            if '\\|w|g=' in next_line:
                # Extract Γγ value between \|w|g= and ' eV'
                gamma_str = next_line.split('\\|w|g=')[1].split(' eV')[0].strip()
            
            # Expected values
            expected_de = str(int(dep * 10)) if dep * 10 < 10 else str(int(dep * 10))
            expected_ep = f"{ep:.1f}"
            expected_dep = str(int(dep * 10)) if dep * 10 < 10 else str(int(dep * 10))
            
            # Format expected gamma
            if gamma_eV >= 10:
                expected_gamma = f"{int(gamma_eV)}{{I{int(unc_eV)}}}"
            elif gamma_eV >= 1:
                unc_last = int(unc_eV * 10)
                expected_gamma = f"{gamma_eV:.1f}{{I{unc_last}}}"
            else:
                unc_last = int(unc_eV * 10)
                expected_gamma = f"{gamma_eV:.1f}{{I{unc_last}}}"
            
            print(f"Resonance Ex = {ex} keV:")
            print(f"  Expected: Ex={target_ex}, DE={expected_de}, Ep={expected_ep}, DEp={expected_dep}, Γγ={expected_gamma}")
            print(f"  Found:    Ex={ex_field}, DE={de_field}, Ep={ep_field}, DEp={dep_field}, Γγ={gamma_str}")
            
            # Check match
            match = (ex_field == target_ex and 
                    de_field == expected_de and 
                    ep_field == expected_ep and 
                    dep_field == expected_dep and
                    gamma_str == expected_gamma)
            
            print(f"  Status:   {'✓ PERFECT MATCH' if match else '✗ MISMATCH'}")
            print()
            
            if not match:
                all_match = False
            
            found = True
            break
    
    if not found:
        print(f"ERROR: Resonance Ex={ex} keV not found!")
        print()
        all_match = False

print("=" * 80)
if all_match:
    print("SUCCESS: All verified resonances match user's original data perfectly!")
else:
    print("ERROR: Some mismatches detected!")
print("=" * 80)
