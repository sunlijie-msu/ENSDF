#!/usr/bin/env python3
"""
Create 100% accurate 2025LAAA_vs_2012DI06.ens placement table using spin-parity evidence.
"""
import json

def parse_2012di06_data():
    """Parse 2012DI06 data into structured format."""
    transitions = []
    
    with open("XUNDL/2012DI06_127I_all_gamma_transitions.xundl", 'r') as f:
        lines = f.readlines()
    
    for line in lines[1:]:  # Skip header
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                try:
                    # Parse level energies (remove uncertainties)
                    eli_str = parts[0].split('(')[0]
                    elf_str = parts[2].split('(')[0]
                    eg_str = parts[4].split('(')[0]
                    
                    eli = float(eli_str)
                    elf = float(elf_str)
                    eg = float(eg_str)
                    
                    ji = parts[1]
                    jf = parts[3]
                    ri = parts[5] if len(parts) > 5 else ""
                    
                    transitions.append({
                        'eli': eli,
                        'ji': ji,
                        'elf': elf,
                        'jf': jf,
                        'eg': eg,
                        'ri': ri
                    })
                except (ValueError, IndexError):
                    continue
    
    return transitions

def get_json_gammas():
    """Get 2025LAAA gamma energies from JSON."""
    with open("XUNDL/2025LAAA_CH11036_127I_gamma_energies.json", 'r') as f:
        data = json.load(f)
    
    gammas = []
    for transition in data['gamma_transitions']:
        energy = transition['energy']['value']
        gammas.append(energy)
    
    return gammas

def find_matching_transition(gamma_energy, transitions, ji_constraint=None, jf_constraint=None, 
                           eli_constraint=None, elf_constraint=None, tolerance=1.0):
    """Find matching 2012DI06 transition for 2025LAAA gamma with constraints."""
    matches = []
    
    for trans in transitions:
        # Energy match within tolerance
        if abs(trans['eg'] - gamma_energy) <= tolerance:
            # Apply constraints if provided
            match = True
            
            if ji_constraint and not spin_match(trans['ji'], ji_constraint):
                match = False
            if jf_constraint and not spin_match(trans['jf'], jf_constraint):
                match = False
            if eli_constraint and abs(trans['eli'] - eli_constraint) > 2.0:
                match = False
            if elf_constraint and abs(trans['elf'] - elf_constraint) > 2.0:
                match = False
                
            if match:
                matches.append(trans)
    
    return matches

def spin_match(spin1, spin2):
    """Check if two spin-parity values match (ignoring parentheses)."""
    s1 = spin1.strip().replace('(', '').replace(')', '')
    s2 = spin2.strip().replace('(', '').replace(')', '')
    return s1 == s2

def main():
    print("Parsing 2012DI06 data...")
    transitions = parse_2012di06_data()
    print(f"Found {len(transitions)} transitions in 2012DI06")
    
    print("\nParsing 2025LAAA gamma energies...")
    gammas_2025 = get_json_gammas()
    print(f"Found {len(gammas_2025)} gamma energies in 2025LAAA")
    
    # Define spin-parity constraints based on user evidence
    constraints = {
        274.4: {'ji': '31/2-', 'jf': '29/2-'},
        653.1: {'ji': '31/2-'},  # Same initial level as 274.4
        806.0: {'ji': '13/2+', 'jf': '9/2+'},
        806.5: {'ji': '17/2+', 'jf': '13/2+'},
        187.5: {'ji': '23/2-', 'jf': '21/2+', 'eli_constraint': 2976.1},
        431.2: {'ji': '23/2-'},  # Same initial level as 187.5
        188.0: {'ji': '19/2-', 'jf': '17/2+', 'eli_constraint': 2545.13},
        651.5: {'ji': '19/2-'},  # Same initial level as 188.0
        431.5: {'ji': '21/2+', 'jf': '19/2+'},
        651.0: {'ji': '9/2+', 'jf': '5/2+'},
        834.2: {'ji': '13/2+', 'jf': '11/2+'},
        380.0: {'ji': '29/2-', 'jf': '27/2-'},
        409.9: {'ji': '29/2-'},  # Same initial level as 380.0
        # Additional specific constraints for ambiguous cases
        213.5: {'prefer_level': 1479.75},  # Choose 1479.75 level over 2477.70
        655.7: {'prefer_level': 3557.20},  # Choose 3557.20 level over 1306.54
        658.7: {'prefer_eg': 658.5},  # Choose 658.5 over 659.0 for better match
        659.0: {'prefer_eg': 659.0},  # Direct match
    }
    
    print("\n" + "="*100)
    print("CREATING ACCURATE PLACEMENT TABLE")
    print("="*100)
    
    placement_entries = []
    
    for gamma in sorted(gammas_2025):
        print(f"\nProcessing {gamma} keV gamma...")
        
        if gamma in constraints:
            # Apply constraints
            constraint = constraints[gamma]
            matches = find_matching_transition(
                gamma, transitions,
                ji_constraint=constraint.get('ji'),
                jf_constraint=constraint.get('jf'),
                eli_constraint=constraint.get('eli_constraint'),
                elf_constraint=constraint.get('elf_constraint'),
                tolerance=2.0  # Increased tolerance for constrained searches
            )
            
            # Handle special preference cases
            if 'prefer_level' in constraint and len(matches) > 1:
                preferred_level = constraint['prefer_level']
                matches = [m for m in matches if abs(m['eli'] - preferred_level) < 1.0]
            elif 'prefer_eg' in constraint and len(matches) > 1:
                preferred_eg = constraint['prefer_eg']
                matches = [m for m in matches if abs(m['eg'] - preferred_eg) < 0.5]
        else:
            # No constraints, find closest energy match
            matches = find_matching_transition(gamma, transitions, tolerance=0.5)
        
        if matches:
            if len(matches) == 1:
                match = matches[0]
                print(f"  ✅ FOUND: {match['eli']:.2f} ({match['ji']}) → {match['elf']:.2f} ({match['jf']}) | {match['eg']:.1f} keV")
                placement_entries.append({
                    'eli': match['eli'],
                    'ji': match['ji'],
                    'elf': match['elf'],
                    'jf': match['jf'],
                    'eg_2012': match['eg'],
                    'ri_2012': match['ri'],
                    'eg_2025': gamma
                })
            else:
                print(f"  ⚠️  MULTIPLE MATCHES for {gamma} keV:")
                for i, match in enumerate(matches):
                    print(f"    {i+1}. {match['eli']:.2f} ({match['ji']}) → {match['elf']:.2f} ({match['jf']}) | {match['eg']:.1f} keV")
                # Take the best match (first one for now, could add more logic)
                match = matches[0]
                placement_entries.append({
                    'eli': match['eli'],
                    'ji': match['ji'],
                    'elf': match['elf'],
                    'jf': match['jf'],
                    'eg_2012': match['eg'],
                    'ri_2012': match['ri'],
                    'eg_2025': gamma
                })
        else:
            print(f"  ❌ NO MATCH FOUND for {gamma} keV")
            # Handle new transitions
            if gamma in [635.5, 1181.2]:
                print(f"    → This is a new transition, will add as TBD")
                placement_entries.append({
                    'eli': 'TBD',
                    'ji': 'TBD',
                    'elf': 'TBD',
                    'jf': 'TBD',
                    'eg_2012': 'TBD',
                    'ri_2012': 'TBD',
                    'eg_2025': gamma
                })
    
    print("\n" + "="*100)
    print("GENERATING PLACEMENT TABLE")
    print("="*100)
    
    # Sort entries by 2025LAAA energy
    placement_entries.sort(key=lambda x: x['eg_2025'] if isinstance(x['eg_2025'], (int, float)) else 9999)
    
    # Write the placement table
    with open("XUNDL/2025LAAA_vs_2012DI06_CORRECTED.ens", 'w') as f:
        f.write("FINAL TABLE: COMBINED 2012DI06 AND 2025LAAA GAMMA RAY DATA\n")
        f.write("======================================================================\n")
        f.write("     ELI |       JI |      ELF |       JF |  EG_2012 |      RI_2012 |  EG_2025\n")
        f.write("   (keV) |          |    (keV) |          |    (keV) |              |    (keV)\n")
        f.write("----------------------------------------------------------------------\n")
        
        for entry in placement_entries:
            if entry['eli'] == 'TBD':
                f.write(f"  {entry['eli']} |     {entry['ji']}  |    {entry['elf']}   |     {entry['jf']}  |     {entry['eg_2012']}  |         {entry['ri_2012']}  |    {entry['eg_2025']:.1f}\n")
            else:
                f.write(f" {entry['eli']:7.2f} | {entry['ji']:8s} | {entry['elf']:8.2f} | {entry['jf']:8s} | {entry['eg_2012']:8.1f} | {entry['ri_2012']:>12s} | {entry['eg_2025']:8.1f}\n")
    
    print(f"\n✅ Created corrected placement table: 2025LAAA_vs_2012DI06_CORRECTED.ens")
    print(f"   Total entries: {len(placement_entries)}")

if __name__ == "__main__":
    main()
