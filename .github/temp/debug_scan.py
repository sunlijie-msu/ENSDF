import re

filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Test specific known violations
test_lines = [2605, 2820]  # L 8844.3 and L 9081.5

for test_line in test_lines:
    print(f"\nTesting around line {test_line+1}:")
    
    i = test_line
    line = lines[i]
    
    if line[6:9] == '  L':
        level_energy = line[10:19].strip()
        print(f"  Found L-record: L {level_energy}")
        
        i += 1
        comments = []
        
        while i < len(lines):
            current = lines[i]
            
            if len(current) > 6 and current[6] in 'X0123456789':
                print(f"    Line {i+1}: Skip (XREF/ISPIN)")
                i += 1
                continue
            
            if len(current) > 9 and current[6:9] == ' cL':
                ctype = None
                if ' E$' in current:
                    ctype = 'E$'
                elif ' J$' in current:
                    ctype = 'J$'
                elif ' T$' in current:
                    ctype = 'T$'
                else:
                    ctype = 'general'
                
                comments.append({'line': i+1, 'type': ctype})
                print(f"    Line {i+1}: Found {ctype} comment")
                
                i += 1
                while i < len(lines) and len(lines[i]) > 9 and lines[i][6].isdigit() and lines[i][7:9] == 'cL':
                    print(f"    Line {i+1}: Skip (continuation)")
                    i += 1
                continue
            
            print(f"    Line {i+1}: Stop (different record)")
            break
        
        print(f"  Comments found: {[c['type'] for c in comments]}")
        
        # Check for violation
        types = [c['type'] for c in comments]
        violation = False
        for j, t in enumerate(types):
            if t == 'T$':
                for k in range(j+1, len(types)):
                    if types[k] in ['E$', 'J$']:
                        violation = True
                        break
        
        print(f"  Violation: {violation}")
