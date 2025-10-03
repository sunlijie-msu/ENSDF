#!/usr/bin/env python3
"""
Process "Other final levels" column from CSV and generate additional ENSDF G-records.

This script extracts gamma transitions to final levels specified in MeV in the 
"Other final levels" column, converts them to keV, and generates G-records.
"""

import re
import sys

# Manually extracted data from CSV "Other final levels" column
# Format: Exi_keV: [(Exf_MeV, BR), ...]
MANUAL_DATA = {
    7175: [('6.10', '4')],
    7192: [('4.85', '2'), ('5.01', '1')],
    7223: [('5.21', '6'), ('5.40', '1'), ('5.85', '1'), ('5.68', '2'), ('6.10', '3')],
    7269: [('4.84', '1'), ('5.01', '1.5'), ('5.40', '0.5'), ('5.75', '1.5')],
    7358: [('4.84', '1'), ('5.01', '0.5'), ('5.65', '0.5')],
    7392: [('4.35', '10')],
    7500: [('6.10', '10')],
    7517: [('4.35', '2'), ('5.59', '3'), ('5.60', '2')],
    7546: [('4.77', '1.5'), ('5.59', '0.2'), ('5.64', '0.5')],  # Fixed 564 -> 5.64
    7616: [('5.21', '3')],
    7653: [('4.84', '3'), ('5.65', '1'), ('5.68', '1'), ('6.10', '3')],
    7669: [('4.35', '6'), ('4.88', '1'), ('5.16', '4')],
    7683: [('5.21', '0.5'), ('5.40', '2'), ('5.60', '2'), ('5.75', '0.5')],
    7691: [('5.60', '1')],
    7704: [('4.84', '1'), ('5.65', '4')],
    7743: [('4.77', '1'), ('4.88', '19')],
    7775: [('4.77', '2'), ('4.84', '2')],
    7780: [('4.35', '2'), ('4.77', '7'), ('5.21', '1'), ('5.40', '1'), ('5.59', '1')],
    7795: [('4.85', '0.5'), ('5.01', '2'), ('5.40', '2'), ('5.65', '1'), ('5.75', '0.5')],
    7834: [('5.21', '1'), ('6.10', '1')],
    7866: [('5.01', '4')],
    7878: [('4.63', '1'), ('4.84', '3'), ('5.65', '9')],
    7968: [('4.35', '8'), ('4.77', '6'), ('4.88', '9'), ('5.21', '3'), ('5.59', '2'), ('5.64', '3')],
    7985: [('5.65', '1'), ('6.10', '1')],
    7993: [('5.40', '3')],
    7999: [('4.77', '8'), ('5.64', '3')],
    8033: [('5.80', '6')],
    8073: [('4.77', '4'), ('4.88', '2'), ('5.16', '1'), ('5.21', '7'), ('5.59', '11'), ('5.64', '10')],
    8093: [('4.77', '1'), ('4.84', '3'), ('5.16', '2'), ('5.21', '1'), ('5.60', '6'), ('5.64', '5'), ('5.80', '1')],
    8104: [('4.84', '0.5'), ('4.85', '0.5'), ('5.60', '0.5')],
    8111: [('5.60', '3'), ('6.49', '6')],
    8144: [('5.01', '2'), ('5.68', '1')],
    8154: [('5.21', '8'), ('5.59', '7'), ('5.64', '3')],
    8177: [('4.63', '9')],
}

def mev_to_kev(mev_str):
    """Convert MeV string to keV, preserving exact format."""
    mev_val = float(mev_str)
    kev_val = mev_val * 1000
    
    # Preserve integer format if result is whole number
    if kev_val == int(kev_val):
        return str(int(kev_val))
    else:
        # Round to 1 decimal place for keV energies
        return str(round(kev_val, 1))

def calculate_gamma_energy(exi, exf_kev):
    """Calculate gamma energy: Eg = Exi - Exf"""
    exi_val = float(exi)
    exf_val = float(exf_kev)
    eg = exi_val - exf_val
    
    # Format with 1 decimal place
    return f"{eg:.1f}"

def process_data():
    """Process manual data and generate additional G-records for each level."""
    
    all_additional_gammas = []
    
    for exi, transitions in sorted(MANUAL_DATA.items()):
        level_gammas = []
        
        for exf_mev, br in transitions:
            exf_kev = mev_to_kev(exf_mev)
            eg = calculate_gamma_energy(str(exi), exf_kev)
            
            level_gammas.append({
                'exf_mev': exf_mev,
                'exf_kev': exf_kev,
                'eg': eg,
                'br': br
            })
        
        all_additional_gammas.append({
            'exi': str(exi),
            'gammas': sorted(level_gammas, key=lambda x: float(x['eg']))  # Sort by ascending Eg
        })
    
    return all_additional_gammas

def generate_ensdf_output(additional_gammas):
    """Generate ENSDF G-records for additional gamma transitions."""
    
    print("\n[Additional Gamma Transitions from 'Other final levels']")
    print("=" * 80)
    
    for level_data in additional_gammas:
        exi = level_data['exi']
        print(f"\nLevel Exi = {exi} keV:")
        print(f"Additional G-records to insert (in ascending energy order):")
        
        for gamma in level_data['gammas']:
            exf_kev = gamma['exf_kev']
            eg = gamma['eg']
            br = gamma['br']
            
            # Format ENSDF G-record (80 columns)
            ensdf_line = f" 35CL  G {eg:<10} {br}"
            padding = ' ' * (80 - len(ensdf_line))
            ensdf_line_full = ensdf_line + padding
            
            print(f"  {ensdf_line_full[:60]}... (Exf={exf_kev} keV from {gamma['exf_mev']} MeV)")
    
    print("\n" + "=" * 80)
    total_gammas = sum(len(ld['gammas']) for ld in additional_gammas)
    print(f"[Summary] Found {total_gammas} additional gamma transitions")
    print(f"          across {len(additional_gammas)} levels")

if __name__ == "__main__":
    additional_gammas = process_data()
    generate_ensdf_output(additional_gammas)
