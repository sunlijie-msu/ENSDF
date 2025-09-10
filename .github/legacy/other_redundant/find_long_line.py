with open('A35/Cl35/new/Cl35_34s_3he_d.ens', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    line_content = line.rstrip('\n\r')
    if len(line_content) > 80:
        print(f'Line {i}: {len(line_content)} characters')
        print(f'Content: |{line_content}|')
        print('Exact char positions:')
        for j in range(0, len(line_content), 10):
            chunk = line_content[j:j+10]
            print(f'{j:2d}-{j+9:2d}: |{chunk}|')
        print('---')
        break
else:
    print("No lines found exceeding 80 characters!")
