#!/usr/bin/env python3
"""
Comprehensive gamma assignment verification against 2012DI06 original data
Checks that all gamma assignments in comparison table are correct
"""

import re

def parse_2012di06_data(filepath):
    """Parse 2012DI06 original gamma data"""
    gamma_data = {}
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) >= 6 and parts[0].strip() != 'ELI':
            try:
                eli_str = parts[0].strip().split('(')[0]  # Remove uncertainty
                jpi_i = parts[1].strip()
                elf_str = parts[2].strip().split('(')[0]  # Remove uncertainty  
                jpi_f = parts[3].strip()
                eg_str = parts[4].strip().split('(')[0]   # Remove uncertainty
                ri_str = parts[5].strip()
                
                if eli_str and eg_str and eli_str.replace('.', '').isdigit() and eg_str.replace('.', '').isdigit():
                    eli = float(eli_str)
                    eg = float(eg_str)
                    elf = float(elf_str) if elf_str and elf_str.replace('.', '').isdigit() else None
                    
                    gamma_data[eg] = {
                        'initial_energy': eli,
                        'initial_jpi': jpi_i,
                        'final_energy': elf,
                        'final_jpi': jpi_f,
                        'intensity': ri_str
                    }
                    print(f"2012DI06: {eg} keV from {eli} keV ({jpi_i}) → {elf} keV ({jpi_f})")
                    
            except (ValueError, IndexError):
                continue
    
    return gamma_data

def parse_comparison_table(filepath):
    """Parse comparison table to extract gamma assignments"""
    comparison_data = {}
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    for line in lines:
        if '|' in line and 'keV' not in line and '----' not in line and 'ELI' not in line:
            parts = line.strip().split('|')
            if len(parts) >= 7:
                try:
                    eli_str = parts[0].strip()
                    jpi_i = parts[1].strip()
                    elf_str = parts[2].strip()
                    jpi_f = parts[3].strip()
                    eg_2012_str = parts[4].strip()
                    ri_2012 = parts[5].strip()
                    eg_2025_str = parts[6].strip()
                    
                    if (eli_str and elf_str and eg_2025_str and 
                        eli_str.replace('.', '').isdigit() and 
                        elf_str.replace('.', '').isdigit() and
                        eg_2025_str.replace('.', '').isdigit()):
                        
                        eli = float(eli_str)
                        elf = float(elf_str)
                        eg_2025 = float(eg_2025_str)
                        
                        comparison_data[eg_2025] = {
                            'initial_energy': eli,
                            'initial_jpi': jpi_i,
                            'final_energy': elf,
                            'final_jpi': jpi_f,
                            'eg_2012': eg_2012_str,
                            'ri_2012': ri_2012
                        }
                        print(f"Comparison: {eg_2025} keV from {eli} keV ({jpi_i}) → {elf} keV ({jpi_f})")
                        
                except (ValueError, IndexError):
                    continue
    
    return comparison_data

def verify_gamma_assignments(di06_data, comparison_data):
    """Verify that comparison table assignments match 2012DI06 original data"""
    print("\n" + "="*80)
    print("GAMMA ASSIGNMENT VERIFICATION")
    print("="*80)
    
    correct = 0
    incorrect = 0
    
    print(f"\n{'Gamma':<8} {'Status':<15} {'Comparison Assignment':<35} {'2012DI06 Assignment':<35}")
    print("-" * 95)
    
    for eg_2025, comp_data in sorted(comparison_data.items()):
        # Find corresponding gamma in 2012DI06 data
        best_match = None
        min_diff = float('inf')
        
        for eg_2012, di06_data_item in di06_data.items():
            diff = abs(eg_2025 - eg_2012)
            if diff < min_diff:
                min_diff = diff
                best_match = (eg_2012, di06_data_item)
        
        if best_match and min_diff < 0.5:  # 0.5 keV tolerance
            eg_2012, di06_info = best_match
            comp_initial = comp_data['initial_energy']
            di06_initial = di06_info['initial_energy']
            
            # Check if initial levels match
            if abs(comp_initial - di06_initial) < 0.1:
                status = "✅ CORRECT"
                correct += 1
            else:
                status = "❌ WRONG"
                incorrect += 1
                
            comp_assign = f"{comp_initial} → {comp_data['final_energy']}"
            di06_assign = f"{di06_initial} → {di06_info['final_energy']}"
            
            print(f"{eg_2025:<8.1f} {status:<15} {comp_assign:<35} {di06_assign:<35}")
            
            if status == "❌ WRONG":
                print(f"         MISMATCH: Comparison shows {comp_initial} but 2012DI06 shows {di06_initial}")
        else:
            print(f"{eg_2025:<8.1f} {'⚠️ NO MATCH':<15} {'N/A':<35} {'N/A':<35}")
            incorrect += 1
    
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY:")
    print("="*80)
    print(f"Correct assignments: {correct}")
    print(f"Incorrect assignments: {incorrect}")
    print(f"Accuracy: {correct / (correct + incorrect) * 100:.1f}%")
    
    if incorrect > 0:
        print(f"\n⚠️ Found {incorrect} incorrect gamma assignments that need fixing!")
    else:
        print("\n🎯 All gamma assignments are correct!")

def main():
    di06_file = "XUNDL/2012DI06_127I_all_gamma_transitions.xundl"
    comparison_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print("Parsing 2012DI06 original data...")
    di06_data = parse_2012di06_data(di06_file)
    print(f"\nFound {len(di06_data)} gamma transitions in 2012DI06")
    
    print("\nParsing comparison table...")
    comparison_data = parse_comparison_table(comparison_file)
    print(f"\nFound {len(comparison_data)} gamma assignments in comparison table")
    
    print("\nVerifying gamma assignments...")
    verify_gamma_assignments(di06_data, comparison_data)

if __name__ == "__main__":
    main()
