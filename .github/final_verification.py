#!/usr/bin/env python3
"""
Final comprehensive verification that L records exactly match ELI energies.
"""

def final_verification():
    """Perform final verification of L records against ELI energies."""
    
    # Required energies from comparison file
    required_energies = [
        0.0,   # Ground state
        57.46, 628.51, 650.79, 716.48, 744.76, 1235.13, 1266.29, 1306.54, 
        1479.75, 1550.68, 1876.02, 1893.64, 1973.80, 2356.75, 2357.10, 
        2545.13, 2788.42, 2829.60, 2976.10, 3207.30, 3442.60, 3557.20, 
        3600.80, 3957.90, 3988.50, 4367.40, 4641.60, 5242.60
    ]
    
    # Extract current L records
    current_energies = []
    with open("XUNDL/2025LAAA_CH11036_127I.ens", 'r') as f:
        for line in f:
            if len(line) >= 8 and line[7] == 'L':
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        energy = float(energy_str)
                        current_energies.append(energy)
                    except ValueError:
                        pass
    
    current_energies.sort()
    required_energies.sort()
    
    print("FINAL VERIFICATION:")
    print("=" * 60)
    print(f"Required energies: {len(required_energies)}")
    print(f"Current energies:  {len(current_energies)}")
    
    # Check exact match
    perfect_match = True
    for i, (req, curr) in enumerate(zip(required_energies, current_energies)):
        match = abs(req - curr) < 0.01
        status = "✅" if match else "❌"
        print(f"{i+1:2d}. {req:8.2f} vs {curr:8.2f} keV {status}")
        if not match:
            perfect_match = False
    
    if len(required_energies) != len(current_energies):
        perfect_match = False
        print(f"\n❌ Count mismatch: {len(required_energies)} required vs {len(current_energies)} current")
    
    print("\n" + "=" * 60)
    if perfect_match:
        print("🎯 PERFECT MATCH! All L records correspond exactly to ELI energies.")
        print("✅ TASK COMPLETED SUCCESSFULLY")
    else:
        print("❌ Mismatch detected - further correction needed")
    
    return perfect_match

if __name__ == "__main__":
    final_verification()
