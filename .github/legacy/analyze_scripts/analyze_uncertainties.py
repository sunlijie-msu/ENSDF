#!/usr/bin/env python3
"""
Analyze JSON data to identify symmetric uncertainties that should use {I+n} format
"""

import json

def analyze_symmetric_uncertainties():
    json_file = "XUNDL/2025LAAA_CH11036_127I_lifetimes.json"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("LIFETIME UNCERTAINTY ANALYSIS")
    print("=" * 50)
    print("Identifying values with symmetric vs asymmetric uncertainties")
    print("=" * 50)
    
    for band in data['bands']:
        for transition in band['transitions']:
            energy = transition['excitation_energy_keV']
            gamma = transition['gamma_energy_keV']
            
            print(f"\nLevel {energy} keV (γ = {gamma} keV):")
            
            for tau_type in ['GTA', 'GTB', 'Ave']:
                key = f'tau_{tau_type}_ps'
                if key in transition and transition[key] is not None:
                    tau_data = transition[key]
                    value = tau_data['value']
                    plus = tau_data['uncertainty_plus']
                    minus = tau_data['uncertainty_minus']
                    
                    is_symmetric = abs(plus - minus) < 0.001  # Very small tolerance
                    
                    # Convert to ENSDF format (multiply by 100 for uncertainty digits)
                    plus_ensdf = int(round(plus * 100))
                    minus_ensdf = int(round(minus * 100))
                    
                    if is_symmetric:
                        ensdf_format = f"{{I+{plus_ensdf}}}"
                        print(f"  {tau_type}: τ = {value} ps ±{plus:.3f} → {ensdf_format} (SYMMETRIC)")
                    else:
                        ensdf_format = f"{{I+{plus_ensdf}-{minus_ensdf}}}"
                        print(f"  {tau_type}: τ = {value} ps +{plus:.3f}-{minus:.3f} → {ensdf_format} (ASYMMETRIC)")

if __name__ == "__main__":
    analyze_symmetric_uncertainties()
