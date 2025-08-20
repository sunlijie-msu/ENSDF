import json
import re

# Read final corrected JSON data
with open('1984CA14_final_corrected.json', 'r') as f:
    paper_data = json.load(f)

# Read ENSDF data and extract S field (neutron lab energy)
ensdf_data = {}
with open('../new/S35_ng_resonances.ens', 'r') as f:
    lines = f.readlines()

for line in lines:
    if len(line) >= 8 and line[7] == 'L':
        # Extract energy from columns 10-19
        energy_str = line[9:19].strip()
        if energy_str:
            try:
                energy_float = float(energy_str)
                
                # Extract Jp from columns 23-39 
                jp_str = line[22:39].strip() if len(line) > 39 else ''
                
                # Extract L-transfer from columns 56-64
                l_transfer = line[55:64].strip() if len(line) > 64 else ''
                
                # Extract neutron lab energy from S field (columns 65-74)
                s_field = line[64:74].strip() if len(line) > 74 else ''
                
                # Try to extract numeric value from S field
                neutron_energy = None
                if s_field:
                    # Remove uncertainty and extract first numeric value
                    s_clean = re.sub(r'\s+\d+\s*$', '', s_field)  # Remove trailing uncertainty
                    try:
                        neutron_energy = float(s_clean)
                    except ValueError:
                        pass
                
                ensdf_data[energy_float] = {
                    'jp': jp_str,
                    'l_transfer': l_transfer,
                    'neutron_energy': neutron_energy
                }
                
            except ValueError:
                pass

print('=== FINAL CORRECTED COMPARISON ===')
print('Paper Energy | Paper Jπ          | ENSDF Energy | ENSDF Jπ  | L-transfer | Match | Issue')
print('-' * 95)

discrepancies = []
matches = 0

for entry in paper_data:
    if entry['Jp'] is None:
        continue  # Skip entries without Jp assignments
    
    # Extract energy value
    energy_str = entry['En_keV']
    energy_clean = re.sub(r'[()]', '', energy_str).strip()
    try:
        json_energy = float(energy_clean)
    except:
        continue
    
    json_jp = entry['Jp']
    
    # Find ENSDF level with matching neutron lab energy (within 1 keV tolerance)
    matched_ensdf = None
    min_diff = float('inf')
    
    for ensdf_energy, ensdf_info in ensdf_data.items():
        if ensdf_info['neutron_energy'] is not None:
            diff = abs(json_energy - ensdf_info['neutron_energy'])
            if diff < min_diff and diff < 1.0:  # 1 keV tolerance
                min_diff = diff
                matched_ensdf = ensdf_energy

    if matched_ensdf:
        ensdf_info = ensdf_data[matched_ensdf]
        ensdf_jp = ensdf_info['jp']
        ensdf_l = ensdf_info['l_transfer']
        neutron_en = ensdf_info['neutron_energy']
        
        # Check for match
        issues = []
        if 'l=' in json_jp:
            # L-transfer assignment from paper
            if ensdf_l == '':
                issues.append('Missing L-transfer')
            elif '[' in ensdf_l:
                issues.append('L in brackets (tentative)')
        else:
            # Jp assignment from paper
            if ensdf_jp == '':
                issues.append('Missing Jp')
            else:
                # Extract J and parity from paper assignment
                paper_jp_clean = json_jp.split()[0]  # Get "3/2-", "1/2+", etc.
                if paper_jp_clean != ensdf_jp:
                    issues.append(f'Jp mismatch: expected {paper_jp_clean}, got {ensdf_jp}')
        
        is_match = len(issues) == 0
        match_status = 'YES' if is_match else 'NO'
        
        if not is_match:
            discrepancies.append({
                'paper_energy': json_energy,
                'paper_jp': json_jp,
                'ensdf_energy': matched_ensdf,
                'ensdf_jp': ensdf_jp,
                'ensdf_l': ensdf_l,
                'neutron_energy': neutron_en,
                'issues': issues
            })
        else:
            matches += 1
            
        issue_text = '; '.join(issues) if issues else ''
        print(f'{energy_str:>12} | {json_jp:<17} | {matched_ensdf:>12.2f} | {ensdf_jp:<9} | {ensdf_l:<10} | {match_status:>5} | {issue_text}')

print(f'\n=== FINAL SUMMARY ===')
print(f'Total paper assignments with Jp: {len([e for e in paper_data if e["Jp"] is not None])}')
print(f'Perfect matches: {matches}')
print(f'Issues found: {len(discrepancies)}')

if discrepancies:
    print(f'\n=== KEY ISSUES ===')
    jp_mismatches = [d for d in discrepancies if any('Jp mismatch' in issue for issue in d['issues'])]
    missing_jp = [d for d in discrepancies if any('Missing Jp' in issue for issue in d['issues'])]
    l_tentative = [d for d in discrepancies if any('tentative' in issue for issue in d['issues'])]
    
    print(f'Jp mismatches (parity missing): {len(jp_mismatches)}')
    print(f'Missing Jp assignments: {len(missing_jp)}')
    print(f'L-transfer tentative brackets: {len(l_tentative)}')
