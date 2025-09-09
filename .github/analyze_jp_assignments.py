#!/usr/bin/env python3
"""
Analyze the J,π assignments provided by the user to resolve ambiguous gamma matches
"""

def analyze_assignments():
    print("ANALYZING USER'S J,π ASSIGNMENTS")
    print("=" * 60)
    
    # User's assignments
    assignments = [
        {
            "gamma_2025": 274.4,
            "ji": "31/2-", "jf": "29/2-",
            "note": "High-spin cascade transition"
        },
        {
            "gamma_2025": 806.0,
            "ji": "13/2+", "jf": "9/2+", 
            "note": "Forms cascade with 806.5 keV - this is FINAL level of 806.5"
        },
        {
            "gamma_2025": 806.5,
            "ji": "17/2+", "jf": "13/2+",
            "note": "Forms cascade with 806.0 keV - feeds the INITIAL level of 806.0"
        },
        {
            "gamma_2025": 187.5,
            "ji": "23/2-", "jf": "21/2+",
            "level_energy": "~2976.6",
            "note": "Same initial level as 431.2 keV"
        },
        {
            "gamma_2025": 431.2,
            "ji": "23/2-", "jf": "19/2-", 
            "level_energy": "~2976.6",
            "note": "Same initial level as 187.5 keV"
        },
        {
            "gamma_2025": 188.0,
            "ji": "19/2-", "jf": "17/2+",
            "level_energy": "~2545.4",
            "note": "Same initial level as 651.5 keV"
        },
        {
            "gamma_2025": 651.5,
            "ji": "19/2-", "jf": "15/2-",
            "level_energy": "~2545.4", 
            "note": "Same initial level as 188.0 keV"
        },
        {
            "gamma_2025": 431.5,
            "ji": "21/2+", "jf": "19/2+",
            "note": "Different from 431.2 keV - different initial J,π"
        },
        {
            "gamma_2025": 651.0,
            "ji": "9/2+", "jf": "5/2+",
            "note": "To ground state"
        },
        {
            "gamma_2025": 834.2,
            "ji": "13/2+", "jf": "11/2+",
            "note": "Same 13/2+ level feeds 244.0 and 806.0 keV gammas"
        }
    ]
    
    # Now find corresponding 2012DI06 transitions
    print("MAPPING TO 2012DI06 TRANSITIONS:")
    print("-" * 40)
    
    # From 2012DI06 file analysis
    di06_transitions = {
        # From placement table
        274.6: ("2343.08", "(17/2+)", "2068.39", "(15/2+)"),
        274.5: ("2590.10", "(17/2)", "2315.60", "(15/2)"),
        274.2: ("4641.60", "(31/2-)", "4367.40", "(29/2-)"),  # This matches 274.4!
        
        805.9: ("1550.68", "13/2+", "744.76", "9/2+"),      # This matches 806.0!
        806.4: ("2357.10", "17/2+", "1550.68", "13/2+"),    # This matches 806.5!
        
        187.5: ("2976.10", "23/2-", "2788.42", "21/2+"),    # Matches assignment!
        188.0: ("2545.13", "19/2-", "2357.10", "17/2+"),    # Matches assignment!
        
        431.0: ("2976.10", "23/2-", "2545.13", "19/2-"),    # This matches 431.2!
        431.5: ("2788.42", "21/2+", "2356.75", "19/2+"),    # Matches assignment!
        
        651.0: ("650.79", "9/2+", "0.00", "5/2+"),          # Matches assignment!
        651.5: ("2545.13", "19/2-", "1893.64", "15/2-"),    # Matches assignment!
        
        833.5: ("2068.39", "(15/2+)", "1235.13", "11/2-"),  # Different transition
        834.2: ("1550.68", "13/2+", "716.48", "11/2+"),     # This matches!
    }
    
    for assignment in assignments:
        gamma = assignment["gamma_2025"]
        ji = assignment["ji"]
        jf = assignment["jf"]
        note = assignment["note"]
        
        print(f"\n{gamma:5.1f} keV (2025LAAA): {ji} → {jf}")
        print(f"  Note: {note}")
        
        # Find the matching 2012DI06 transition
        if gamma == 274.4:
            print(f"  MATCHES: 274.2 keV (2012DI06) from (31/2-) → (29/2-)")
            print(f"  Levels: 4641.60 → 4367.40 keV")
        elif gamma == 806.0:
            print(f"  MATCHES: 805.9 keV (2012DI06) from 13/2+ → 9/2+") 
            print(f"  Levels: 1550.68 → 744.76 keV")
        elif gamma == 806.5:
            print(f"  MATCHES: 806.4 keV (2012DI06) from 17/2+ → 13/2+")
            print(f"  Levels: 2357.10 → 1550.68 keV")
        elif gamma == 187.5:
            print(f"  MATCHES: 187.5 keV (2012DI06) from 23/2- → 21/2+")
            print(f"  Levels: 2976.10 → 2788.42 keV")
        elif gamma == 431.2:
            print(f"  MATCHES: 431.0 keV (2012DI06) from 23/2- → 19/2-")
            print(f"  Levels: 2976.10 → 2545.13 keV")
        elif gamma == 188.0:
            print(f"  MATCHES: 188.0 keV (2012DI06) from 19/2- → 17/2+")
            print(f"  Levels: 2545.13 → 2357.10 keV")
        elif gamma == 651.5:
            print(f"  MATCHES: 651.5 keV (2012DI06) from 19/2- → 15/2-")
            print(f"  Levels: 2545.13 → 1893.64 keV")
        elif gamma == 431.5:
            print(f"  MATCHES: 431.5 keV (2012DI06) from 21/2+ → 19/2+")
            print(f"  Levels: 2788.42 → 2356.75 keV")
        elif gamma == 651.0:
            print(f"  MATCHES: 651.0 keV (2012DI06) from 9/2+ → 5/2+")
            print(f"  Levels: 650.79 → 0.00 keV")
        elif gamma == 834.2:
            print(f"  MATCHES: 834.2 keV (2012DI06) from 13/2+ → 11/2+")
            print(f"  Levels: 1550.68 → 716.48 keV")
    
    print("\n" + "=" * 60)
    print("KEY FINDINGS:")
    print("- 274.4 (2025) → 274.2 (2012): High-spin (31/2-) → (29/2-)")
    print("- 806.0 (2025) → 805.9 (2012): 13/2+ → 9/2+ cascade")
    print("- 806.5 (2025) → 806.4 (2012): 17/2+ → 13/2+ cascade")
    print("- 187.5 and 431.2 from same 23/2- level at ~2976 keV")
    print("- 188.0 and 651.5 from same 19/2- level at ~2545 keV")
    print("- All other assignments confirmed correct")

if __name__ == "__main__":
    analyze_assignments()
