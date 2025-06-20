#!/usr/bin/env python3
"""
ENSDF Average Verification Script
Check weighted vs unweighted averages in Ar35 file
"""

import re
import math

def extract_value_uncertainty(text):
    """Extract value and uncertainty from text like '1179 {I10}'"""
    match = re.search(r'(\d+(?:\.\d+)?)\s*\{I(\d+(?:\.\d+)?)\}', text)
    if match:
        value = float(match.group(1))
        uncertainty = float(match.group(2))
        return value, uncertainty
    return None, None

def weighted_average(values_uncertainties):
    """Calculate weighted average and uncertainty"""
    if len(values_uncertainties) < 2:
        return None, None
    
    weights = []
    weighted_sum = 0
    weight_sum = 0
    
    for value, uncertainty in values_uncertainties:
        if uncertainty > 0:
            weight = 1.0 / (uncertainty ** 2)
            weights.append(weight)
            weighted_sum += weight * value
            weight_sum += weight
        else:
            return None, None  # Can't do weighted average with zero uncertainty
    
    if weight_sum == 0:
        return None, None
    
    avg = weighted_sum / weight_sum
    avg_uncertainty = math.sqrt(1.0 / weight_sum)
    
    return avg, avg_uncertainty

def unweighted_average(values_uncertainties):
    """Calculate unweighted (simple) average"""
    if len(values_uncertainties) < 2:
        return None, None
    
    values = [v[0] for v in values_uncertainties]
    avg = sum(values) / len(values)
    
    # For unweighted average, uncertainty is typically the larger of the individual uncertainties
    # or calculated from the spread of values
    uncertainties = [v[1] for v in values_uncertainties]
    max_unc = max(uncertainties)
    
    # Calculate spread-based uncertainty
    if len(values) == 2:
        spread_unc = abs(values[0] - values[1]) / 2
        # Use the larger of max individual uncertainty or half the spread
        avg_uncertainty = max(max_unc, spread_unc)
    else:
        avg_uncertainty = max_unc
    
    return avg, avg_uncertainty

def analyze_file(filename):
    """Analyze the Ar35 file for averaging calculations"""
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    print("=== ENSDF Average Verification ===")
    print(f"Analyzing: {filename}")
    print()
    
    i = 0
    issues = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for L-records with energy values
        if re.match(r'^\s*35AR\s+L\s+(\d+(?:\.\d+)?)\s+(\d+)', line):
            # Extract the adopted energy and uncertainty
            l_match = re.match(r'^\s*35AR\s+L\s+(\d+(?:\.\d+)?)\s+(\d+)', line)
            adopted_energy = float(l_match.group(1))
            adopted_uncertainty = float(l_match.group(2))
            
            # Look for the corresponding comment line with the averaging info
            if i + 1 < len(lines):
                comment_line = lines[i + 1].strip()
                
                if 'weighted average' in comment_line or 'unweighted average' in comment_line:
                    print(f"Checking energy level: {adopted_energy} ± {adopted_uncertainty}")
                    print(f"L-record: {line}")
                    print(f"Comment:  {comment_line}")
                    
                    # Extract the original values
                    # Pattern: "value {I uncertainty} (reference)"
                    values_1973 = extract_value_uncertainty(comment_line.split('(1973Be26)')[0])
                    values_1998 = extract_value_uncertainty(comment_line.split('(1998VoAA)')[0].split('and')[1])
                    
                    if values_1973[0] is not None and values_1998[0] is not None:
                        original_data = [values_1973, values_1998]
                        
                        print(f"  1973Be26: {values_1973[0]} ± {values_1973[1]}")
                        print(f"  1998VoAA: {values_1998[0]} ± {values_1998[1]}")
                        
                        # Calculate both types of averages
                        weighted_avg, weighted_unc = weighted_average(original_data)
                        unweighted_avg, unweighted_unc = unweighted_average(original_data)
                        
                        if weighted_avg is not None:
                            print(f"  Calculated weighted average: {weighted_avg:.1f} ± {weighted_unc:.1f}")
                        if unweighted_avg is not None:
                            print(f"  Calculated unweighted average: {unweighted_avg:.1f} ± {unweighted_unc:.1f}")
                        
                        print(f"  Adopted value: {adopted_energy} ± {adopted_uncertainty}")
                          # Check which method was claimed to be used
                        is_unweighted = 'unweighted average' in comment_line
                        is_weighted = 'weighted average' in comment_line and not is_unweighted
                        
                        # Verify the calculation
                        tolerance = 0.6  # Allow some rounding tolerance
                        
                        if is_weighted and weighted_avg is not None:
                            if abs(adopted_energy - weighted_avg) > tolerance:
                                issues.append(f"ERROR: Energy {adopted_energy} claims weighted average but calculated {weighted_avg:.1f}")
                                print(f"  ❌ MISMATCH: Claimed weighted, calculated {weighted_avg:.1f}")
                            else:
                                print(f"  ✅ Weighted average calculation correct")
                                
                            # Check if unweighted would be better choice
                            if unweighted_avg is not None:
                                if abs(adopted_energy - unweighted_avg) < abs(adopted_energy - weighted_avg):
                                    issues.append(f"SUGGESTION: Energy {adopted_energy} uses weighted but unweighted ({unweighted_avg:.1f}) might be closer")
                        
                        elif is_unweighted and unweighted_avg is not None:
                            if abs(adopted_energy - unweighted_avg) > tolerance:
                                issues.append(f"ERROR: Energy {adopted_energy} claims unweighted average but calculated {unweighted_avg:.1f}")
                                print(f"  ❌ MISMATCH: Claimed unweighted, calculated {unweighted_avg:.1f}")
                            else:
                                print(f"  ✅ Unweighted average calculation correct")
                                
                            # Check if weighted would be better choice
                            if weighted_avg is not None:
                                if abs(adopted_energy - weighted_avg) < abs(adopted_energy - unweighted_avg):
                                    issues.append(f"SUGGESTION: Energy {adopted_energy} uses unweighted but weighted ({weighted_avg:.1f}) might be closer")
                        
                        # Check uncertainty
                        if is_weighted and weighted_unc is not None:
                            if abs(adopted_uncertainty - weighted_unc) > 1.0:
                                issues.append(f"WARNING: Energy {adopted_energy} uncertainty {adopted_uncertainty} vs calculated {weighted_unc:.1f}")
                        elif is_unweighted and unweighted_unc is not None:
                            if abs(adopted_uncertainty - unweighted_unc) > 1.0:
                                issues.append(f"WARNING: Energy {adopted_energy} uncertainty {adopted_uncertainty} vs calculated {unweighted_unc:.1f}")
                        
                        print()
                    else:
                        print(f"  ⚠️ Could not extract original values")
                        print()
        
        i += 1
    
    print("=== SUMMARY ===")
    if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ All averaging calculations appear correct")
    
    return issues

if __name__ == "__main__":
    issues = analyze_file("../finished/Ar35/new/Ar35_36ar_3he_a.ens")
