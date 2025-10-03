import os

# Read file
file_path = os.path.join('A35', 'Cl35', 'temp', '1976ME12.ens')
with open(file_path, 'r') as f:
    lines = f.readlines()

resonance_start = 190
current_resonances = {}
current_ep = None
current_gammas = []

for i in range(resonance_start, min(resonance_start + 30, len(lines))):
    line = lines[i]
    if len(line) < 10:
        break
    
    print(f"Line {i}: {repr(line[:80])}")
    
    if line[7] == 'L':
        print(f"  -> L-record detected")
        # New L-record - save previous
        if current_ep is not None and current_gammas:
            print(f"  -> Saving previous Ep={current_ep} with {len(current_gammas)} gammas")
            current_resonances[current_ep] = current_gammas
        elif current_ep is not None:
            print(f"  -> Previous Ep={current_ep} has no gammas, not saving")
        
        # Extract Ep from S field (cols 65-74)
        ep_field = line[64:74].strip()
        print(f"  -> Ep field: {repr(ep_field)}")
        try:
            current_ep = float(ep_field) if ep_field else None
            print(f"  -> New current_ep = {current_ep}")
        except Exception as e:
            print(f"  -> Failed to parse Ep: {e}")
            current_ep = None
        current_gammas = []
    
    elif ' cL' in line:
        print(f"  -> cL comment, skipping")
        continue
    
    elif line[7] == 'G':
        print(f"  -> G-record detected, current_ep={current_ep}")
        if current_ep is not None:
            current_gammas.append(line)
            print(f"  -> Added to current_gammas, total now = {len(current_gammas)}")

# Save last resonance
if current_ep is not None and current_gammas:
    print(f"\nSaving last Ep={current_ep} with {len(current_gammas)} gammas")
    current_resonances[current_ep] = current_gammas

print(f"\n\nFinal: Found {len(current_resonances)} resonances")
for ep, gammas in list(current_resonances.items())[:3]:
    print(f"  Ep={ep}: {len(gammas)} gammas")
