import re

def find_comment_violations(filename, start_line=831):
    """Find comment ordering violations after specified line."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    violations = []
    i = start_line - 1  # Convert to 0-based index
    
    while i < len(lines):
        line = lines[i]
        
        # Look for L-record (nuclear level record)
        if re.match(r'^ \d{1,3}[A-Z][a-z]?  L ', line):
            level_line = i + 1  # 1-based line number
            level_energy = line[10:19].strip()
            
            # Skip to find comment lines for this level
            i += 1
            comments = []
            
            while i < len(lines):
                current_line = lines[i]
                
                # Skip XREF line
                if re.match(r'^ \d{1,3}[A-Z][a-z]?X L ', current_line):
                    i += 1
                    continue
                
                # Check for ISPIN line or blank line (skip)
                if re.match(r'^ \d{1,3}[A-Z][a-z]?\d L ', current_line):
                    i += 1
                    continue
                
                # Check if this is a cL comment line
                if re.match(r'^ \d{1,3}[A-Z][a-z]? cL ', current_line):
                    # Determine comment type
                    comment_type = None
                    if ' E$' in current_line:
                        comment_type = 'E$'
                    elif ' J$' in current_line:
                        comment_type = 'J$'
                    elif ' J,' in current_line:
                        # Handle combined J,T$
                        comment_type = 'J,T$'
                    elif ' T$' in current_line:
                        comment_type = 'T$'
                    elif ' S$' in current_line:
                        comment_type = 'S$'
                    else:
                        comment_type = 'general'
                    
                    comments.append({
                        'line': i + 1,
                        'type': comment_type,
                        'text': current_line[:70]  # Truncate for display
                    })
                    i += 1
                    
                    # Skip continuation lines for this comment
                    while i < len(lines) and re.match(r'^ \d{1,3}[A-Z][a-z]?\dcL ', lines[i]):
                        i += 1
                    continue
                
                # If we hit a different record type, stop processing this level
                if re.match(r'^ \d{1,3}[A-Z][a-z]?  [GDBE]', current_line) or \
                   re.match(r'^ \d{1,3}[A-Z][a-z]? d', current_line):
                    break
                
                i += 1
            
            # Check comment ordering for this level
            if len(comments) >= 2:
                comment_types = [c['type'] for c in comments]
                
                # Check if T$ appears before E$ or J$
                for j, ctype in enumerate(comment_types):
                    if ctype == 'T$':
                        # Check if E$ or J$ appears AFTER T$
                        for k in range(j + 1, len(comment_types)):
                            if comment_types[k] in ['E$', 'J$']:
                                violations.append({
                                    'level_line': level_line,
                                    'level_energy': level_energy,
                                    'current_order': '  '.join(comment_types),
                                    'comments': comments
                                })
                                break
                        if violations and violations[-1]['level_line'] == level_line:
                            break
            continue
        
        i += 1
    
    return violations

if __name__ == '__main__':
    filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'
    
    print("Scanning Cl35_adopted.ens for comment ordering violations...")
    print("Starting from L 6106.2 (line 831)")
    print("=" * 80)
    
    violations = find_comment_violations(filename, start_line=831)
    
    if violations:
        print(f"\n FOUND {len(violations)} VIOLATION(S):\n")
        for idx, v in enumerate(violations, 1):
            print(f"Violation #{idx}: L {v['level_energy']} (line {v['level_line']})")
            print(f"  Current order: {v['current_order']}")
            print(f"  Comment details:")
            for c in v['comments']:
                print(f"    Line {c['line']:4d}: {c['type']:8s} - {c['text'].strip()[:60]}")
            print()
    else:
        print("\n NO VIOLATIONS FOUND after line 831!")
    
    print("=" * 80)
    print(f"Scan complete. Total violations: {len(violations)}")
