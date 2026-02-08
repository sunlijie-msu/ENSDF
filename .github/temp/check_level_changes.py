import sys

def check_level_changes(diff_file):
    try:
        with open(diff_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(diff_file, 'r', encoding='utf-16') as f:
                lines = f.readlines()
        except:
             with open(diff_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
    
    level_changes = []
    for line in lines:
        if line.startswith('+ 35CL  L') or line.startswith('- 35CL  L'):
            level_changes.append(line)
            
    if not level_changes:
        print("No level records changed.")
        return

    # Group by level energies to see what actually changed
    for i in range(0, len(level_changes), 2):
        if i+1 < len(level_changes):
            old = level_changes[i]
            new = level_changes[i+1]
            if old[0] == '-' and new[0] == '+':
                # Compare energy fields (columns 10-19)
                old_e = old[10:20]
                new_e = new[10:20]
                if old_e != new_e:
                    print(f"ENERGY CHANGE DETECTED!")
                    print(f"Old: {old.strip()}")
                    print(f"New: {new.strip()}")
                else:
                    print(f"Level {old_e.strip()} changed, but energy remains same.")
            else:
                # Handle cases where multiple lines are changed or added/removed
                print(f"Unexpected diff pattern: {line.strip()}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_level_changes(sys.argv[1])
