import re
import sys

def find_comment_violations(filename, start_line=831):
    """
    Find comment ordering violations after specified line.
    Rule: E$  J$  T$  S$  general
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    violations = []
    i = start_line
    
    while i < len(lines):
        line = lines[i]
        
        # Look for L-record
        if re.match(r'^ \d{1,3}[A-Z][a-z]?  L ', line):
            level_line = i + 1  # 1-based line number
            level_energy = line[10:19].strip()
            
            # Find all comment lines for this level
            i += 1
            comments = []
            
            while i < len(lines):
                current_line = lines[i]
                
                # Check if this is a continuation X line (skip it)
                if re.match(r'^ \d{1,3}[A-Z][a-z]?X L ', current_line):
                    i += 1
                    continue
                
                # Check if this is a cL comment line
                if re.match(r'^ \d{1,3}[A-Z][a-z]? cL ', current_line):
                    comment_type = None
                    if ' E$' in current_line:
                        comment_type = 'E$'
                    elif ' J$' in current_line or ' J,' in current_line:
                        comment_type = 'J$'
                    elif ' T$' in current_line or ' T,' in current_line:
                        comment_type = 'T$'
                    elif ' S$' in current_line:
                        comment_type = 'S$'
                    else:
                        comment_type = 'general'
                    
                    comments.append({
                        'line': i + 1,
                        'type': comment_type,
                        'text': current_line.strip()
                    })
                    i += 1
                    
                    # Continue reading continuation lines
                    while i < len(lines) and re.match(r'^ \d{1,3}[A-Z][a-z]?\dcL ', lines[i]):
                        i += 1
                    continue
                
                # If we hit a different record type, stop processing this level
                break
            
            # Check comment ordering for this level
            if len(comments) >= 2:
                comment_types = [c['type'] for c in comments]
                
                # Check if T$ appears before E$ or J$
                for j, ctype in enumerate(comment_types):
                    if ctype == 'T$':
                        # Check if E$ or J$ appears after T$
                        remaining = comment_types[j+1:]
                        if 'E$' in remaining or 'J$' in remaining:
                            violations.append({
                                'level_line': level_line,
                                'level_energy': level_energy,
                                'current_order': '  '.join(comment_types),
                                'violation_details': f"T$ at line {comments[j]['line']}, followed by {' '.join(remaining)}",
                                'comments': comments
                            })
                            break
            continue
        
        i += 1
    
    return violations

if __name__ == '__main__':
    filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_adopted.ens'
    
    print("Scanning for comment ordering violations after L 6106.2 (line 831)...")
    print("=" * 80)
    
    violations = find_comment_violations(filename, start_line=830)
    
    if violations:
        print(f"\nFOUND {len(violations)} VIOLATION(S):\n")
        for v in violations:
            print(f"Violation at L {v['level_energy']} (line {v['level_line']})")
            print(f"  Current order: {v['current_order']}")
            print(f"  Details: {v['violation_details']}")
            print(f"  Comment lines:")
            for c in v['comments']:
                print(f"    Line {c['line']}: {c['type']}")
            print()
    else:
        print("\nNO VIOLATIONS FOUND!")
    
    print("=" * 80)
    print(f"Total violations found: {len(violations)}")
