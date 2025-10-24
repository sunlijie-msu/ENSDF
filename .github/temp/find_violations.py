import re

filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

violations = []
i = 830  # Start from line 831 (0-based index)

while i < len(lines):
    line = lines[i]
    
    # Look for L-record
    if re.match(r'^ \d{1,3}[A-Z][a-z]?  L ', line):
        level_line_num = i + 1
        level_energy = line[10:19].strip()
        
        # Collect all cL comments for this level
        i += 1
        comment_blocks = []
        
        while i < len(lines):
            current = lines[i]
            
            # Skip XREF, ISPIN lines
            if re.match(r'^ \d{1,3}[A-Z][a-z]?[X\d] L ', current):
                i += 1
                continue
            
            # Found a cL comment line
            if re.match(r'^ \d{1,3}[A-Z][a-z]? cL ', current):
                comment_line = i + 1
                
                # Determine type
                ctype = None
                if ' E$' in current or ' E,' in current:
                    ctype = 'E$'
                elif ' J$' in current or ' J,' in current:
                    ctype = 'J$'
                elif ' T$' in current or ' T,' in current:
                    ctype = 'T$'
                elif ' S$' in current:
                    ctype = 'S$'
                else:
                    ctype = 'general'
                
                comment_blocks.append({
                    'line': comment_line,
                    'type': ctype
                })
                
                i += 1
                # Skip continuation lines
                while i < len(lines) and re.match(r'^ \d{1,3}[A-Z][a-z]?\dcL ', lines[i]):
                    i += 1
                continue
            
            # Hit a non-comment record, stop
            break
        
        # Check ordering: T$ should NOT appear before E$ or J$
        if len(comment_blocks) >= 2:
            types = [c['type'] for c in comment_blocks]
            
            # Find T$ positions
            for j, t in enumerate(types):
                if t == 'T$':
                    # Check if E$ or J$ comes AFTER T$
                    for k in range(j + 1, len(types)):
                        if types[k] in ['E$', 'J$']:
                            violations.append({
                                'level': level_energy,
                                'line': level_line_num,
                                'order': '  '.join(types),
                                'comments': comment_blocks
                            })
                            break
                    break
        
        continue
    
    i += 1

# Print results
print("=" * 80)
print(f"COMMENT ORDERING VIOLATION SCAN: Cl35_adopted.ens")
print(f"Search scope: Lines 831 to end of file")
print(f"Rule: cL comments must follow order E$  J$  T$  S$  general")
print("=" * 80)
print()

if violations:
    print(f" FOUND {len(violations)} VIOLATION(S):\n")
    for idx, v in enumerate(violations, 1):
        print(f"Violation #{idx}: L {v['level']} (line {v['line']})")
        print(f"  Current order: {v['order']}")
        print(f"  Details:")
        for c in v['comments']:
            print(f"    Line {c['line']:5d}: {c['type']}")
        print()
else:
    print(" NO VIOLATIONS FOUND!\n")

print("=" * 80)
print(f"Total violations found: {len(violations)}")
