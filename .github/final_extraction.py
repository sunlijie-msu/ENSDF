#!/usr/bin/env python3
"""
Final corrected extraction with proper level detection
"""

import re
import json

def final_corrected_extraction():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    levels = []  # Keep track of all levels in order
    lifetimes = {}
    
    tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
    
    for i, line in enumerate(lines):
        # Check for level records: position 7 is 'L', position 8 is space
        if len(line) > 9 and line[7] == 'L' and line[8] == ' ':
            energy_str = line[9:19].strip()
            try:
                level_energy = float(energy_str)
                levels.append((level_energy, i+1))
                print(f"Level found: {level_energy} keV at line {i+1}")
            except:
                pass
        
        # Check for lifetime comments
        elif '|t{-' in line:
            matches = re.findall(tau_pattern, line)
            if matches:
                # Find the most recent level before this comment
                current_level = None
                for level_energy, level_line in reversed(levels):
                    if level_line < i+1:  # Level must be before this comment
                        current_level = level_energy
                        break
                
                if current_level is not None:
                    if current_level not in lifetimes:
                        lifetimes[current_level] = {}
                    
                    print(f"Line {i+1}: Associating lifetime data with level {current_level} keV")
                    
                    for match in matches:
                        tau_type, value, plus_err, minus_err = match
                        lifetimes[current_level][tau_type] = {
                            'value': float(value),
                            'plus': int(plus_err) / 100.0,
                            'minus': int(minus_err) / 100.0
                        }
                        print(f"    {tau_type}: {value} +{plus_err/100:.2f}-{minus_err/100:.2f} ps")
                    print()
    
    print("\n" + "="*50)
    print("FINAL EXTRACTED LIFETIMES:")
    print("="*50)
    for level in sorted(lifetimes.keys()):
        print(f"{level} keV: {lifetimes[level]}")
    
    return lifetimes

def compare_with_json():
    """Compare extracted ENSDF data with JSON data"""
    json_file = "XUNDL/2025LAAA_CH11036_127I_lifetimes.json"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    json_lifetimes = {}
    for band in json_data['bands']:
        for transition in band['transitions']:
            energy = transition['excitation_energy_keV']
            json_lifetimes[energy] = {}
            
            for tau_type in ['GTA', 'GTB', 'Ave']:
                key = f'tau_{tau_type}_ps'
                if key in transition and transition[key] is not None:
                    tau_data = transition[key]
                    json_lifetimes[energy][tau_type] = {
                        'value': tau_data['value'],
                        'plus': tau_data['uncertainty_plus'],
                        'minus': tau_data['uncertainty_minus']
                    }
    
    ensdf_lifetimes = final_corrected_extraction()
    
    print("\n" + "="*60)
    print("COMPARISON: JSON vs ENSDF")
    print("="*60)
    
    all_perfect = True
    matches = 0
    
    for json_energy in sorted(json_lifetimes.keys()):
        # Find matching ENSDF level (within 1 keV)
        ensdf_match = None
        for ensdf_energy in ensdf_lifetimes.keys():
            if abs(json_energy - ensdf_energy) <= 1.0:
                ensdf_match = ensdf_energy
                break
        
        print(f"\nJSON Level {json_energy} keV:")
        if ensdf_match:
            print(f"  ✅ Matched ENSDF: {ensdf_match} keV")
            matches += 1
            
            json_data = json_lifetimes[json_energy]
            ensdf_data = ensdf_lifetimes[ensdf_match]
            
            level_perfect = True
            for tau_type in ['GTA', 'GTB', 'Ave']:
                if tau_type in json_data:
                    if tau_type in ensdf_data:
                        j_val = json_data[tau_type]
                        e_val = ensdf_data[tau_type]
                        
                        val_ok = abs(j_val['value'] - e_val['value']) < 0.01
                        plus_ok = abs(j_val['plus'] - e_val['plus']) < 0.01
                        minus_ok = abs(j_val['minus'] - e_val['minus']) < 0.01
                        
                        if val_ok and plus_ok and minus_ok:
                            print(f"    {tau_type}: ✅ MATCH")
                        else:
                            print(f"    {tau_type}: ❌ MISMATCH")
                            level_perfect = False
                            all_perfect = False
                    else:
                        print(f"    {tau_type}: ❌ MISSING IN ENSDF")
                        level_perfect = False
                        all_perfect = False
        else:
            print(f"  ❌ NO ENSDF MATCH FOUND")
            all_perfect = False
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {matches}/10 levels matched")
    if all_perfect and matches == 10:
        print("🎉 ✅ ALL LIFETIME DATA VERIFIED PERFECTLY!")
    else:
        print("❌ Some discrepancies found")

if __name__ == "__main__":
    compare_with_json()
