#!/usr/bin/env python3
"""
Lifetime Verification Script - Compare Image Data with ENSDF Comments
====================================================================

This script extracts lifetime data from ENSDF comments and compares them
with the lifetime values provided in the image table.

Author: Nuclear Data Verification System
Date: September 2025
"""

# Image data for the 10 levels with their lifetime measurements
image_data = {
    3957.9: {  # Ex = 3958.7 keV in image
        'gamma': 982.1,
        'image_lifetimes': {
            'GTA': '1.32+0.12-0.13',
            'Ave': '1.32+0.12-0.13'
        }
    },
    2976.1: {  # Ex = 2976.6 keV in image
        'gamma': 431.2,
        'image_lifetimes': {
            'GTA': '2.02+0.22-0.23',
            'GTB': '1.97+0.10-0.18',
            'Ave': '2.00+0.29-0.20'
        }
    },
    2545.13: {  # Ex = 2545.4 keV in image
        'gamma': 651.5,
        'image_lifetimes': {
            'GTA': '1.66+0.14-0.12',
            'GTB': '1.80+0.17-0.16',
            'Ave': '1.73+0.22-0.20'
        }
    },
    1893.64: {  # Ex = 1893.9 keV in image
        'gamma': 658.7,
        'image_lifetimes': {
            'GTA': '0.88+0.07-0.07',
            'GTB': '1.14+0.10-0.12',
            'Ave': '1.01+0.12-0.14'
        }
    },
    1235.13: {  # Ex = 1235.2 keV in image
        'gamma': 490.3,
        'image_lifetimes': {
            'GTA': '1.10+0.08-0.09',
            'GTB': '0.71+0.08-0.07',
            'Ave': '0.91+0.11-0.11'
        }
    },
    2356.75: {  # Ex = 2356.7 keV in image
        'gamma': 877.0,
        'image_lifetimes': {
            'GTB': '1.02+0.24-0.23',
            'Ave': '1.02+0.24-0.23'
        }
    },
    1876.02: {  # Ex = 1876.2 keV in image
        'gamma': 610.0,
        'image_lifetimes': {
            'GTB': '1.34+0.17-0.20',
            'Ave': '1.34+0.17-0.20'
        }
    },
    1479.75: {  # Ex = 1479.7 keV in image
        'gamma': 763.3,
        'image_lifetimes': {
            'GTA': '0.86+0.05-0.07',
            'GTB': '0.72+0.03-0.06',
            'Ave': '0.79+0.06-0.09'
        }
    },
    716.48: {  # Ex = 716.4 keV in image
        'gamma': 659.0,
        'image_lifetimes': {
            'GTA': '1.42+0.10-0.11',
            'Ave': '1.42+0.10-0.11'
        }
    },
    744.76: {  # Ex = 744.9 keV in image
        'gamma': 744.9,
        'image_lifetimes': {
            'GTA': '2.41+0.27-0.33',
            'Ave': '2.41+0.27-0.33'
        }
    }
}

# ENSDF lifetime data extracted from comments
ensdf_lifetimes = {
    3957.9: {},  # No lifetime comment found
    2976.1: {},  # No lifetime comment found - need to check
    2545.13: {},  # No lifetime comment found - need to check  
    1893.64: {
        'Ave': '1.01+12-14',
        'GTA': '0.88+7-7', 
        'GTB': '1.14+10-12'
    },
    1235.13: {
        'Ave': '0.91+11-11',
        'GTA': '1.10+8-9',
        'GTB': '0.71+8-7'
    },
    2356.75: {},  # No lifetime comment found - need to check
    1876.02: {
        'Ave': '1.34+17-20',
        'GTB': '1.34+17-20'
    },
    1479.75: {
        'Ave': '0.79+6-9',
        'GTA': '0.86+5-7',
        'GTB': '0.72+3-6'
    },
    716.48: {
        'Ave': '1.42+10-11',
        'GTA': '1.42+10-11'
    },
    744.76: {
        'Ave': '2.41+27-33',
        'GTA': '2.41+27-33'
    }
}

def parse_lifetime_value(lifetime_str):
    """Parse lifetime string like '1.42+10-11' to extract central value and uncertainties"""
    if not lifetime_str:
        return None, None, None
    
    # Handle format like '1.42+10-11' 
    if '+' in lifetime_str and '-' in lifetime_str:
        parts = lifetime_str.split('+')
        central = float(parts[0])
        uncertainty_part = parts[1]
        if '-' in uncertainty_part:
            up_parts = uncertainty_part.split('-')
            up_err = float(up_parts[0]) / 100  # Convert to same decimal places
            down_err = float(up_parts[1]) / 100
            return central, up_err, down_err
    
    return None, None, None

def compare_lifetimes():
    """Compare image and ENSDF lifetime data"""
    
    print("LIFETIME VERIFICATION - Image vs ENSDF")
    print("=" * 60)
    
    all_match = True
    
    for level_energy in sorted(image_data.keys()):
        gamma_energy = image_data[level_energy]['gamma']
        print(f"\nLevel {level_energy} keV (γ = {gamma_energy} keV):")
        print("-" * 40)
        
        image_lifetimes = image_data[level_energy]['image_lifetimes']
        ensdf_lifetimes_level = ensdf_lifetimes.get(level_energy, {})
        
        # Check each lifetime type
        for lifetime_type in ['GTA', 'GTB', 'Ave']:
            if lifetime_type in image_lifetimes:
                image_val = image_lifetimes[lifetime_type]
                ensdf_val = ensdf_lifetimes_level.get(lifetime_type, 'NOT FOUND')
                
                print(f"  {lifetime_type}:")
                print(f"    Image:  τ = {image_val} ps")
                print(f"    ENSDF:  τ = {ensdf_val} ps")
                
                if ensdf_val == 'NOT FOUND':
                    print(f"    ❌ MISMATCH: {lifetime_type} not found in ENSDF")
                    all_match = False
                else:
                    # Parse and compare values
                    img_central, img_up, img_down = parse_lifetime_value(image_val.replace('+', '+').replace('-', '-'))
                    ensdf_central, ensdf_up, ensdf_down = parse_lifetime_value(ensdf_val)
                    
                    if img_central and ensdf_central:
                        central_match = abs(img_central - ensdf_central) < 0.01
                        if central_match:
                            print(f"    ✅ MATCH: Central values agree")
                        else:
                            print(f"    ❌ MISMATCH: Central values differ")
                            all_match = False
                    else:
                        print(f"    ⚠️  Could not parse values for comparison")
                        all_match = False
    
    print("\n" + "=" * 60)
    if all_match:
        print("✅ ALL LIFETIME VALUES MATCH")
    else:
        print("❌ SOME LIFETIME VALUES DO NOT MATCH")
    
    return all_match

if __name__ == "__main__":
    compare_lifetimes()
