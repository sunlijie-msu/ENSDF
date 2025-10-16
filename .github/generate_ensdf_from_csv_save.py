#!/usr/bin/env python3
"""
Generate ENSDF L and G records from 2001VO24.csv and save to file
"""

import csv

def read_csv(filename):
    """Read CSV and extract transition data"""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Extract Exi values from row 3 (index 2)
    exi_row = rows[2]
    exi_values = []
    exi_col_indices = []
    for col_idx in range(2, len(exi_row)):
        val = exi_row[col_idx].strip()
        if val and val != 'Exi':
            exi_values.append(int(val))
            exi_col_indices.append(col_idx)
    
    # Extract transitions
    transitions = {}
    for row_idx in range(3, len(rows)-1):
        row = rows[row_idx]
        exf_label = row[0].strip()
        exf_val = row[1].strip()
        
        if exf_label == 'Exf' and exf_val:
            exf = int(exf_val)
            
            for col_idx, exi in zip(exi_col_indices, exi_values):
                if col_idx < len(row):
                    br_str = row[col_idx].strip()
                    if br_str:
                        br = int(br_str)
                        if exi not in transitions:
                            transitions[exi] = {}
                        transitions[exi][exf] = br
    
    return transitions

def format_l_record(exi_kev):
    """Format L-record: Exi in MeV in columns 10-19, left-justified"""
    exi_mev = exi_kev / 1000.0
    e_str = f"{exi_mev:.3f}".ljust(10)
    line = f" 35CL  L {e_str}"
    line = line.ljust(80)
    return line

def format_g_record(egamma_kev, ri_value):
    """Format G-record: Egamma in columns 10-19, RI in columns 23-29, left-justified"""
    e_str = f"{egamma_kev:.1f}".ljust(10)
    ri_str = f"{ri_value}".ljust(7)
    line = f" 35CL  G {e_str} {ri_str}"
    line = line.ljust(80)
    return line

def generate_records(transitions):
    """Generate ENSDF records from transitions dictionary"""
    records = []
    
    for exi in sorted(transitions.keys()):
        # Generate L-record
        l_record = format_l_record(exi)
        records.append(l_record)
        
        # Sort gammas by energy (ascending)
        gamma_data = []
        for exf in sorted(transitions[exi].keys()):
            br = transitions[exi][exf]
            egamma = exi - exf
            gamma_data.append((egamma, br, exf))
        
        # Sort by egamma ascending
        gamma_data.sort(key=lambda x: x[0])
        
        for egamma, br, exf in gamma_data:
            g_record = format_g_record(egamma, br)
            records.append(g_record)
    
    return records

if __name__ == '__main__':
    csv_file = 'd:\\X\\ND\\ENSDF\\A35\\Cl35\\raw\\2001VO24.csv'
    ens_file = 'd:\\X\\ND\\ENSDF\\A35\\Cl35\\raw\\2001VO24_generated.txt'
    
    transitions = read_csv(csv_file)
    records = generate_records(transitions)
    
    # Save to file
    with open(ens_file, 'w') as f:
        for record in records:
            f.write(record + '\n')
    
    print(f"Generated {len(records)} records")
    print(f"  L-records: {len(transitions)}")
    print(f"  G-records: {sum(len(v) for v in transitions.values())}")
    print(f"Saved to: {ens_file}")
