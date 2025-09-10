#!/usr/bin/env python3
"""
Final Comprehensive Verification - ALL Lifetime Data
===================================================

Verify that all 10 levels from JSON have their lifetime data correctly
represented in the ENSDF file.
"""

import json
import re

def extract_all_ensdf_lifetimes():
    """Extract ALL lifetime data from ENSDF file"""
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    lifetimes = {}
    current_level = None
    
    for i, line in enumerate(lines):
        # Check for level records
        if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
            except:
                current_level = None
        
        # Check for lifetime comments with τ values
        elif '|t{-' in line and 'ps' in line:
            if current_level is not None:
                if current_level not in lifetimes:
                    lifetimes[current_level] = {}
                
                # Extract τ values using regex
                tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
                matches = re.findall(tau_pattern, line)
                
                for match in matches:
                    tau_type, value, plus_err, minus_err = match
                    lifetimes[current_level][tau_type] = {
                        'value': float(value),
                        'plus': int(plus_err) / 100.0,  # Convert to decimal
                        'minus': int(minus_err) / 100.0
                    }
    
    return lifetimes

def load_json_lifetimes():
    """Load lifetime data from JSON file"""
    json_file = "XUNDL/2025LAAA_CH11036_127I_lifetimes.json"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lifetimes = {}
    
    for band in data['bands']:
        for transition in band['transitions']:
            energy = transition['excitation_energy_keV']
            lifetimes[energy] = {}
            
            for tau_type in ['GTA', 'GTB', 'Ave']:
                key = f'tau_{tau_type}_ps'
                if key in transition and transition[key] is not None:
                    tau_data = transition[key]
                    lifetimes[energy][tau_type] = {
                        'value': tau_data['value'],
                        'plus': tau_data['uncertainty_plus'],
                        'minus': tau_data['uncertainty_minus']
                    }
    
    return lifetimes

def find_matching_level(target_energy, ensdf_levels, tolerance=1.0):
    """Find matching ENSDF level within tolerance"""
    for ensdf_energy in ensdf_levels:
        if abs(target_energy - ensdf_energy) <= tolerance:
            return ensdf_energy
    return None

def final_verification():
    """Final comprehensive verification of all lifetime data"""
    
    print("🎯 FINAL COMPREHENSIVE LIFETIME VERIFICATION")
    print("=" * 60)
    
    json_lifetimes = load_json_lifetimes()
    ensdf_lifetimes = extract_all_ensdf_lifetimes()
    
    print(f"JSON file: {len(json_lifetimes)} levels with lifetime data")
    print(f"ENSDF file: {len(ensdf_lifetimes)} levels with lifetime data")
    print()
    
    all_perfect = True
    matches_found = 0
    
    for json_energy in sorted(json_lifetimes.keys()):
        ensdf_level = find_matching_level(json_energy, ensdf_lifetimes.keys())
        
        print(f"JSON Level {json_energy} keV:")
        
        if ensdf_level is None:
            print(f"  ❌ NO MATCHING ENSDF LEVEL FOUND")
            all_perfect = False
            continue
        
        print(f"  ✅ Matched ENSDF level: {ensdf_level} keV")
        matches_found += 1
        
        json_data = json_lifetimes[json_energy]
        ensdf_data = ensdf_lifetimes[ensdf_level]
        
        # Check each lifetime type
        level_perfect = True
        for tau_type in ['GTA', 'GTB', 'Ave']:
            if tau_type in json_data:
                json_tau = json_data[tau_type]
                
                if tau_type in ensdf_data:
                    ensdf_tau = ensdf_data[tau_type]
                    
                    # Check values
                    value_match = abs(json_tau['value'] - ensdf_tau['value']) < 0.01
                    plus_match = abs(json_tau['plus'] - ensdf_tau['plus']) < 0.01
                    minus_match = abs(json_tau['minus'] - ensdf_tau['minus']) < 0.01
                    
                    print(f"    {tau_type}:")
                    print(f"      JSON:  τ = {json_tau['value']:4.2f}^{{+{json_tau['plus']:4.2f}}}_{{-{json_tau['minus']:4.2f}}} ps")
                    print(f"      ENSDF: τ = {ensdf_tau['value']:4.2f}^{{+{ensdf_tau['plus']:4.2f}}}_{{-{ensdf_tau['minus']:4.2f}}} ps")
                    
                    if value_match and plus_match and minus_match:
                        print(f"      ✅ PERFECT MATCH")
                    else:
                        print(f"      ❌ MISMATCH")
                        if not value_match:
                            print(f"         Value: {json_tau['value']} ≠ {ensdf_tau['value']}")
                        if not plus_match:
                            print(f"         Plus: {json_tau['plus']} ≠ {ensdf_tau['plus']}")
                        if not minus_match:
                            print(f"         Minus: {json_tau['minus']} ≠ {ensdf_tau['minus']}")
                        level_perfect = False
                        all_perfect = False
                else:
                    print(f"    {tau_type}: ❌ MISSING IN ENSDF")
                    level_perfect = False
                    all_perfect = False
        
        if level_perfect:
            print(f"  🎉 LEVEL COMPLETE - ALL LIFETIME VALUES MATCH")
        print()
    
    print("=" * 60)
    print(f"SUMMARY: {matches_found}/10 levels matched")
    
    if all_perfect and matches_found == 10:
        print("🎉 ✅ PERFECT! ALL 10 LIFETIME MEASUREMENTS VERIFIED!")
        print("🎯 TASK 3 VERIFICATION: 100% COMPLETE")
    else:
        print("❌ Some issues remain")
    
    return all_perfect and matches_found == 10

if __name__ == "__main__":
    final_verification()
