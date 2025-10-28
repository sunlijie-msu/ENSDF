#!/usr/bin/env python3
"""Find cL comment ordering violations in ENSDF file."""

import re
import sys

def check_cl_order(file_path):
    """Find all cL comment ordering violations."""
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    violations = []
    i = 0
    
    while i < len(lines):
        # Check if this is an L-record
        if re.match(r'\s*35CL\s+L\s', lines[i]):
            l_line_num = i + 1
            energy = lines[i].split()[4] if len(lines[i].split()) > 4 else '?'
            
            # Look for following cL records
            j = i + 1
            cl_blocks = []
            
            while j < len(lines):
                line = lines[j]
                
                # Stop if we hit another L, G, or DP record (not cL)
                if re.match(r'\s*35CL\s+[LGD]\s', line) and not re.match(r'\s*35CL\s+cL', line):
                    break
                
                # Continuation lines (2cL, 3cL, etc.) are part of previous block
                if re.match(r'\s*35CL\s+[2-9]cL', line):
                    j += 1
                    continue
                
                # Check for cL with identifier
                match = re.match(r'\s*35CL\s+cL\s+([EJTS])\$', line)
                if match:
                    cl_type = match.group(1)
                    cl_blocks.append((cl_type, j + 1))  # Store type and line number
                
                j += 1
            
            # Check if blocks are in wrong order (E < J < T < S)
            order_map = {'E': 0, 'J': 1, 'T': 2, 'S': 3}
            
            for k in range(len(cl_blocks) - 1):
                curr_type, curr_line = cl_blocks[k]
                next_type, next_line = cl_blocks[k + 1]
                
                curr_val = order_map.get(curr_type, -1)
                next_val = order_map.get(next_type, -1)
                
                # Violation if current > next (out of order)
                if curr_val > next_val:
                    order_str = ''.join([t for t, _ in cl_blocks])
                    violations.append({
                        'l_line': l_line_num,
                        'energy': energy,
                        'order': order_str,
                        'cl_lines': [(t, ln) for t, ln in cl_blocks],
                        'first_violation': (k, curr_type, next_type)
                    })
                    break  # Only report first violation per L-record
        
        i += 1
    
    return violations

if __name__ == '__main__':
    file_path = "d:\\X\\ND\\ENSDF\\A35\\Cl35\\new\\Cl35_34s_p_g.ens"
    
    violations = check_cl_order(file_path)
    
    if violations:
        print(f"Found {len(violations)} L-records with cL ordering violations:\n")
        for v in violations:
            print(f"Line {v['l_line']} (E={v['energy']}): {v['order']}")
            for k, (cl_type, cl_line) in enumerate(v['cl_lines']):
                print(f"  [{k}] Line {cl_line}: {cl_type}$")
            print()
    else:
        print("No cL ordering violations found!")
