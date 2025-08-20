with open('A35/S35/new/S35_ng_resonances.ens', 'r') as f:
    lines = f.readlines()

print('Current L field contents (columns 56-64):')
for i, line in enumerate(lines):
    if line.startswith(' 35S   L ') and len(line) > 64:
        s_field = line[65:75].strip().split()[0] if line[65:75].strip() else ''
        l_field = line[56:65].strip()
        if l_field:  # Only show non-empty L fields
            print(f'Energy {s_field}: L field = "{l_field}"')
