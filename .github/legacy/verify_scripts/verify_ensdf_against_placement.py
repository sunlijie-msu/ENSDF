#!/usr/bin/env python3
"""
Comprehensive verification of 2025LAAA_CH11036_127I.ens using validated placement table
"""

def parse_placement_table(filename):
    """Parse the validated placement table to get correct gamma-to-level assignments"""
    placements = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if '|' in line and 'keV' not in line and 'ELI' not in line and '---' not in line and 'FINAL' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                try:
                    eli = float(parts[0])
                    ji = parts[1].strip()
                    elf = float(parts[2])
                    jf = parts[3].strip()
                    eg_2012 = float(parts[4])
                    ri_2012 = parts[5].strip()
                    eg_2025 = parts[6].strip()
                    
                    if eg_2025 != 'TBD' and eg_2025:
                        energy_2025 = float(eg_2025)
                        placements[energy_2025] = {
                            'initial_level': eli,
                            'initial_jp': ji,
                            'final_level': elf,
                            'final_jp': jf,
                            'gamma_energy': energy_2025
                        }
                except (ValueError, IndexError):
                    continue
    
    return placements

def parse_ensdf_file(filename):
    """Parse ENSDF file to extract current level and gamma structure"""
    levels = {}
    gammas = {}
    current_level = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if len(line) > 8 and line[7] == 'L':  # Level record
            try:
                # Extract level energy and J-π
                energy_str = line[9:19].strip()
                jp_str = line[21:39].strip()
                
                if energy_str:
                    energy = float(energy_str)
                    levels[energy] = {
                        'jp': jp_str,
                        'line_number': i + 1,
                        'gammas': []
                    }
                    current_level = energy
            except (ValueError, IndexError):
                continue
                
        elif len(line) > 8 and line[7] == 'G' and current_level is not None:  # Gamma record
            try:
                # Extract gamma energy
                gamma_energy_str = line[9:19].strip()
                if gamma_energy_str:
                    gamma_energy = float(gamma_energy_str)
                    gammas[gamma_energy] = {
                        'placed_under_level': current_level,
                        'placed_under_jp': levels[current_level]['jp'],
                        'line_number': i + 1
                    }
                    levels[current_level]['gammas'].append(gamma_energy)
            except (ValueError, IndexError):
                continue
    
    return levels, gammas

def find_discrepancies(placement_data, ensdf_levels, ensdf_gammas):
    """Find all discrepancies between placement table and ENSDF file"""
    
    print("COMPREHENSIVE DISCREPANCY ANALYSIS:")
    print("=" * 80)
    
    errors = []
    
    # Check each gamma in placement table
    for gamma_energy, correct_placement in placement_data.items():
        correct_initial = correct_placement['initial_level']
        correct_initial_jp = correct_placement['initial_jp']
        correct_final = correct_placement['final_level']
        correct_final_jp = correct_placement['final_jp']
        
        if gamma_energy in ensdf_gammas:
            # Gamma exists in ENSDF - check if it's placed correctly
            current_placement = ensdf_gammas[gamma_energy]
            current_level = current_placement['placed_under_level']
            current_jp = current_placement['placed_under_jp']
            
            # Check if placed under correct initial level
            if abs(current_level - correct_initial) > 0.1:
                errors.append({
                    'type': 'wrong_level_placement',
                    'gamma': gamma_energy,
                    'current_level': current_level,
                    'current_jp': current_jp,
                    'correct_level': correct_initial,
                    'correct_jp': correct_initial_jp,
                    'line_number': current_placement['line_number']
                })
            
            # Check if initial level exists with correct J-π
            if correct_initial in ensdf_levels:
                ensdf_jp = ensdf_levels[correct_initial]['jp']
                if ensdf_jp != correct_initial_jp:
                    errors.append({
                        'type': 'wrong_jp_assignment',
                        'level': correct_initial,
                        'current_jp': ensdf_jp,
                        'correct_jp': correct_initial_jp,
                        'line_number': ensdf_levels[correct_initial]['line_number']
                    })
            else:
                errors.append({
                    'type': 'missing_initial_level',
                    'gamma': gamma_energy,
                    'missing_level': correct_initial,
                    'missing_jp': correct_initial_jp
                })
            
            # Check if final level exists with correct J-π
            if correct_final in ensdf_levels:
                ensdf_jp = ensdf_levels[correct_final]['jp']
                if ensdf_jp != correct_final_jp:
                    errors.append({
                        'type': 'wrong_final_jp',
                        'level': correct_final,
                        'current_jp': ensdf_jp,
                        'correct_jp': correct_final_jp,
                        'line_number': ensdf_levels[correct_final]['line_number']
                    })
            else:
                errors.append({
                    'type': 'missing_final_level',
                    'gamma': gamma_energy,
                    'missing_level': correct_final,
                    'missing_jp': correct_final_jp
                })
                
        else:
            # Gamma missing from ENSDF entirely
            errors.append({
                'type': 'missing_gamma',
                'gamma': gamma_energy,
                'should_be_under_level': correct_initial,
                'should_be_under_jp': correct_initial_jp
            })
    
    return errors

def report_errors(errors):
    """Report all errors in organized categories"""
    
    # Categorize errors
    categories = {}
    for error in errors:
        error_type = error['type']
        if error_type not in categories:
            categories[error_type] = []
        categories[error_type].append(error)
    
    print(f"\nFOUND {len(errors)} TOTAL ERRORS:")
    print("=" * 80)
    
    for category, category_errors in categories.items():
        print(f"\n{category.upper().replace('_', ' ')} ({len(category_errors)} errors):")
        print("-" * 50)
        
        for error in category_errors:
            if category == 'wrong_level_placement':
                print(f"  • {error['gamma']} keV gamma:")
                print(f"    Currently under: {error['current_level']} keV ({error['current_jp']}) [Line {error['line_number']}]")
                print(f"    Should be under: {error['correct_level']} keV ({error['correct_jp']})")
                
            elif category == 'wrong_jp_assignment':
                print(f"  • Level {error['level']} keV [Line {error['line_number']}]:")
                print(f"    Current J-π: '{error['current_jp']}'")
                print(f"    Correct J-π: '{error['correct_jp']}'")
                
            elif category == 'missing_initial_level':
                print(f"  • Gamma {error['gamma']} keV needs initial level:")
                print(f"    Missing level: {error['missing_level']} keV ({error['missing_jp']})")
                
            elif category == 'missing_final_level':
                print(f"  • Gamma {error['gamma']} keV needs final level:")
                print(f"    Missing level: {error['missing_level']} keV ({error['missing_jp']})")
                
            elif category == 'missing_gamma':
                print(f"  • Missing gamma: {error['gamma']} keV")
                print(f"    Should be under: {error['should_be_under_level']} keV ({error['should_be_under_jp']})")
                
            elif category == 'wrong_final_jp':
                print(f"  • Final level {error['level']} keV [Line {error['line_number']}]:")
                print(f"    Current J-π: '{error['current_jp']}'")
                print(f"    Correct J-π: '{error['correct_jp']}'")
    
    return categories

def create_correction_plan(categories):
    """Create detailed correction plan"""
    
    print("\n" + "=" * 80)
    print("CORRECTION PLAN:")
    print("=" * 80)
    
    plan = []
    
    # Priority 1: Add missing levels
    if 'missing_initial_level' in categories or 'missing_final_level' in categories:
        missing_levels = set()
        for error in categories.get('missing_initial_level', []):
            missing_levels.add((error['missing_level'], error['missing_jp']))
        for error in categories.get('missing_final_level', []):
            missing_levels.add((error['missing_level'], error['missing_jp']))
        
        plan.append({
            'priority': 1,
            'action': 'Add missing levels',
            'details': list(missing_levels)
        })
    
    # Priority 2: Correct J-π assignments
    if 'wrong_jp_assignment' in categories or 'wrong_final_jp' in categories:
        jp_corrections = []
        for error in categories.get('wrong_jp_assignment', []):
            jp_corrections.append((error['level'], error['current_jp'], error['correct_jp'], error['line_number']))
        for error in categories.get('wrong_final_jp', []):
            jp_corrections.append((error['level'], error['current_jp'], error['correct_jp'], error['line_number']))
        
        plan.append({
            'priority': 2,
            'action': 'Correct J-π assignments',
            'details': jp_corrections
        })
    
    # Priority 3: Move misplaced gammas
    if 'wrong_level_placement' in categories:
        gamma_moves = []
        for error in categories['wrong_level_placement']:
            gamma_moves.append((error['gamma'], error['current_level'], error['correct_level'], error['line_number']))
        
        plan.append({
            'priority': 3,
            'action': 'Move misplaced gammas',
            'details': gamma_moves
        })
    
    # Priority 4: Add missing gammas
    if 'missing_gamma' in categories:
        missing_gammas = []
        for error in categories['missing_gamma']:
            missing_gammas.append((error['gamma'], error['should_be_under_level'], error['should_be_under_jp']))
        
        plan.append({
            'priority': 4,
            'action': 'Add missing gammas',
            'details': missing_gammas
        })
    
    for step in plan:
        print(f"\nPriority {step['priority']}: {step['action']}")
        for detail in step['details']:
            print(f"  • {detail}")
    
    return plan

if __name__ == "__main__":
    placement_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    print("Loading validated placement table...")
    placement_data = parse_placement_table(placement_file)
    print(f"Found {len(placement_data)} gamma placements")
    
    print("Parsing ENSDF file structure...")
    ensdf_levels, ensdf_gammas = parse_ensdf_file(ensdf_file)
    print(f"Found {len(ensdf_levels)} levels and {len(ensdf_gammas)} gammas in ENSDF file")
    
    print("\nAnalyzing discrepancies...")
    errors = find_discrepancies(placement_data, ensdf_levels, ensdf_gammas)
    
    categories = report_errors(errors)
    correction_plan = create_correction_plan(categories)
    
    if errors:
        print(f"\n🚨 CRITICAL: {len(errors)} errors found in ENSDF file!")
        print("The ENSDF file requires systematic correction using the validated placement table.")
    else:
        print("\n✅ No errors found - ENSDF file matches placement table perfectly!")
