"""
Extract ALL 48 resonance levels from 1976ME12_Resonance_Branching_Ratios.csv
with systematic bidirectional verification and ENSDF format output.

This script addresses CATASTROPHIC file corruption where duplicate G-records
appear at multiple levels due to copy-paste errors during original data entry.
"""

import csv
import sys
from pathlib import Path

def main():
    csv_file = Path(r"d:\X\ND\ENSDF\A35\Cl35\temp\1976ME12_Resonance_Branching_Ratios.csv")
    
    if not csv_file.exists():
        print(f"ERROR: CSV file not found: {csv_file}")
        return 1
    
    # Column mapping (0-indexed):
    # 0-1: BLANK
    # 2-15: Ef final level energies (keV)
    # 16: other final levels (MeV format with BR)
    # 17-21: BLANK
    
    final_levels = [0, 1219.3, 1763.4, 2644.7, 2694.7, 3003.7, 3163.9, 
                   3920.7, 3944.1, 3979, 4059.4, 4114, 4174.7, 4180.1]
    
    print("=" * 80)
    print("EXTRACTING 48 RESONANCE LEVELS FROM CSV")
    print("=" * 80)
    print()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Skip header rows (rows 0-1), extract data rows 2-49
    data_rows = rows[2:50]
    
    total_levels = 0
    total_gammas = 0
    
    for idx, row in enumerate(data_rows, start=1):
        # Bidirectional verification
        if len(row) < 22:
            print(f"WARNING: Row {idx} has only {len(row)} columns (expected 22)")
            continue
        
        # Extract Ep and Exi
        try:
            ep = float(row[0]) if row[0] else None
            exi = float(row[1]) if row[1] else None
        except ValueError:
            print(f"ERROR: Row {idx} - cannot parse Ep='{row[0]}' or Exi='{row[1]}'")
            continue
        
        if ep is None or exi is None:
            print(f"WARNING: Row {idx} - missing Ep or Exi")
            continue
        
        print(f"\n--- Level {idx}/48: Ep={ep} keV, Exi={exi} keV ---")
        total_levels += 1
        
        # Extract BR data from columns 2-15
        gammas = []
        for col_idx, br_str in enumerate(row[2:16], start=2):
            if not br_str or br_str.strip() == '':
                continue
            
            # Handle comparison operators
            if br_str.startswith('<'):
                br = br_str[1:].strip()
                comparison = 'LT'
            elif br_str.startswith('>'):
                br = br_str[1:].strip()
                comparison = 'GT'
            else:
                br = br_str.strip()
                comparison = None
            
            try:
                br_val = float(br)
            except ValueError:
                print(f"  WARNING: Cannot parse BR='{br_str}' at column {col_idx}")
                continue
            
            # Calculate Egamma = Exi - Exf
            exf = final_levels[col_idx - 2]
            egamma = exi - exf
            
            gammas.append({
                'energy': egamma,
                'ri': br_val,
                'comparison': comparison,
                'final_level': exf
            })
        
        # Extract "other final levels" from column 16
        other_levels_str = row[16] if len(row) > 16 else ''
        if other_levels_str and other_levels_str.strip():
            # Parse MeV format: e.g., "5.01(2), 5.60(2), 6.11(7)"
            parts = [p.strip() for p in other_levels_str.split(',')]
            for part in parts:
                if '(' not in part:
                    continue
                try:
                    # Extract Exf(BR) format
                    exf_mev_str, br_str = part.split('(')
                    exf_mev = float(exf_mev_str)
                    br_val = float(br_str.rstrip(')'))
                    
                    # Convert MeV to keV
                    exf_kev = exf_mev * 1000
                    egamma = exi - exf_kev
                    
                    gammas.append({
                        'energy': egamma,
                        'ri': br_val,
                        'comparison': None,
                        'final_level': exf_kev
                    })
                except (ValueError, IndexError):
                    print(f"  WARNING: Cannot parse other level '{part}'")
        
        # Sort gammas by energy (ascending order - ENSDF requirement)
        gammas.sort(key=lambda x: x['energy'])
        
        print(f"  Total gammas: {len(gammas)}")
        total_gammas += len(gammas)
        
        # Format ENSDF L-record
        print(f"\n  ENSDF L-record:")
        l_record = f" 35CL  L {exi:<10.1f}        {ep:<10.1f}     "
        print(f"    {l_record}")
        
        # Format ENSDF G-records
        if gammas:
            print(f"\n  ENSDF G-records (ascending energy):")
            for gamma in gammas:
                eg_str = f"{gamma['energy']:.1f}"
                ri_str = f"{gamma['ri']}"
                
                # Handle comparison operators in DRI field
                if gamma['comparison']:
                    dri_field = gamma['comparison']
                else:
                    dri_field = ''
                
                g_record = f" 35CL  G {eg_str:<10} {ri_str:<7} {dri_field:<2}"
                print(f"    {g_record}  [to {gamma['final_level']} keV]")
        else:
            print("  WARNING: No gammas found for this level!")
    
    print("\n" + "=" * 80)
    print(f"EXTRACTION COMPLETE:")
    print(f"  Total levels extracted: {total_levels}")
    print(f"  Total gamma transitions: {total_gammas}")
    print("=" * 80)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
