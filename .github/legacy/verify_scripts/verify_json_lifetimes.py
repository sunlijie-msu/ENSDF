#!/usr/bin/env python3
"""
Comprehensive Lifetime Verification Script - JSON vs ENSDF
==========================================================

This script verifies that all lifetime data from the JSON file has been
correctly added to the ENSDF file with proper ENSDF format.

Author: Nuclear Data Verification System
Date: September 2025
"""

import json
import re

def extract_ensdf_lifetimes(ensdf_file):
    """Extract all lifetime data from ENSDF file"""
    lifetimes = {}
    current_level = None
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        # Check for level records
        if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
            # Extract energy from columns 10-19
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
            except:
                current_level = None
        
        # Check for lifetime comments (look for T$ comment lines)
        elif line.startswith('127I  cL T$') or line.startswith('127I 2cL'):
            if current_level is not None:
                if current_level not in lifetimes:
                    lifetimes[current_level] = {}
                
                # Extract τ values using regex - handle ENSDF special notation
                tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
                matches = re.findall(tau_pattern, line)
                
                for match in matches:
                    tau_type, value, plus_err, minus_err = match
                    lifetimes[current_level][tau_type] = {
                        'value': float(value),
                        'plus': int(plus_err),
                        'minus': int(minus_err)
                    }
    
    return lifetimes

def load_json_lifetimes(json_file):
    """Load lifetime data from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lifetimes = {}
    
    for band in data['bands']:
        for transition in band['transitions']:
            energy = transition['excitation_energy_keV']
            lifetimes[energy] = {}
            
            # Extract GTA, GTB, Ave values
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

def verify_lifetime_consistency():
    """Compare JSON and ENSDF lifetime data"""
    json_file = "XUNDL/2025LAAA_CH11036_127I_lifetimes.json"
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    print("COMPREHENSIVE LIFETIME VERIFICATION")
    print("=" * 50)
    
    json_lifetimes = load_json_lifetimes(json_file)
    ensdf_lifetimes = extract_ensdf_lifetimes(ensdf_file)
    
    print(f"JSON file contains {len(json_lifetimes)} levels with lifetime data")
    print(f"ENSDF file contains {len(ensdf_lifetimes)} levels with lifetime data")
    print()
    
    all_match = True
    
    # Check each level from JSON
    for energy in sorted(json_lifetimes.keys()):
        print(f"Level {energy} keV:")
        print("-" * 30)
        
        # Find matching ENSDF level (within 1 keV tolerance)
        ensdf_level = None
        for ensdf_energy in ensdf_lifetimes.keys():
            if abs(energy - ensdf_energy) < 1.0:
                ensdf_level = ensdf_energy
                break
        
        if ensdf_level is None:
            print(f"  ❌ ERROR: No matching level found in ENSDF")
            all_match = False
            continue
        
        print(f"  Matched ENSDF level: {ensdf_level} keV")
        
        json_data = json_lifetimes[energy]
        ensdf_data = ensdf_lifetimes[ensdf_level]
        
        # Check each lifetime type
        for tau_type in ['GTA', 'GTB', 'Ave']:
            if tau_type in json_data:
                json_tau = json_data[tau_type]
                if tau_type in ensdf_data:
                    ensdf_tau = ensdf_data[tau_type]
                    
                    # Check central value
                    value_match = abs(json_tau['value'] - ensdf_tau['value']) < 0.01
                    
                    # Convert JSON uncertainties to ENSDF format
                    json_plus = int(json_tau['plus'] * 100)
                    json_minus = int(json_tau['minus'] * 100)
                    
                    plus_match = json_plus == ensdf_tau['plus']
                    minus_match = json_minus == ensdf_tau['minus']
                    
                    print(f"    {tau_type}:")
                    print(f"      JSON:  τ = {json_tau['value']:4.2f}^{{+{json_tau['plus']:4.2f}}}_{{-{json_tau['minus']:4.2f}}} ps")
                    print(f"      ENSDF: τ = {ensdf_tau['value']:4.2f}^{{+{ensdf_tau['plus']:02d}}}_{{-{ensdf_tau['minus']:02d}}} ps (×0.01)")
                    
                    if value_match and plus_match and minus_match:
                        print(f"      ✅ PERFECT MATCH")
                    else:
                        print(f"      ❌ MISMATCH:")
                        if not value_match:
                            print(f"         Value: {json_tau['value']} ≠ {ensdf_tau['value']}")
                        if not plus_match:
                            print(f"         Plus error: {json_plus} ≠ {ensdf_tau['plus']}")
                        if not minus_match:
                            print(f"         Minus error: {json_minus} ≠ {ensdf_tau['minus']}")
                        all_match = False
                else:
                    print(f"    {tau_type}: ❌ MISSING in ENSDF")
                    all_match = False
        print()
    
    print("=" * 50)
    if all_match:
        print("✅ ALL LIFETIME VALUES MATCH PERFECTLY!")
    else:
        print("❌ SOME LIFETIME VALUES DO NOT MATCH")
    
    return all_match

if __name__ == "__main__":
    verify_lifetime_consistency()
