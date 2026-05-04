"""Debug block extraction near 3646.3"""
with open(r'A34\Cl34\new\Cl34_adopted.ens', encoding='utf-8') as f:
    lines = f.readlines()

cur_level_str = None
in_j = False
block_text = ''
block_start = 0
blocks = []

for i, line in enumerate(lines, 1):
    if len(line) < 10:
        if in_j:
            blocks.append((cur_level_str, block_start, block_text))
            in_j = False; block_text = ''
        continue
    col6 = line[5]; col8 = line[7]
    is_cL = (col8 == 'L' and line[6] == 'c' and col6 == ' ')
    is_data_L = (col6 == ' ' and col8 == 'L' and line[6] == ' ')

    if is_data_L:
        if in_j:
            blocks.append((cur_level_str, block_start, block_text))
            in_j = False; block_text = ''
        cur_level_str = line[9:19].strip()
    elif is_cL:
        text = line[9:80].rstrip('\n')
        if 'J$' in text:
            if in_j:
                blocks.append((cur_level_str, block_start, block_text))
            in_j = True; block_text = text; block_start = i
        elif in_j:
            block_text += ' ' + text.strip()
    else:
        if in_j:
            blocks.append((cur_level_str, block_start, block_text))
            in_j = False; block_text = ''

# Show blocks near 3646.3
for parent, bs, bt in blocks:
    if parent and '364' in parent:
        print(f'BLOCK: parent={parent!r} start_line={bs}')
        print(f'  Text: {bt[:120]}')
        print()
