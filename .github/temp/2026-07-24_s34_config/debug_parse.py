with open(r'A34\S34\new\S34_32s_t_p.ens','r') as f: lines=f.readlines()

current_l_idx = None
for i, line in enumerate(lines):
    if len(line) < 10: continue
    if line[7] == 'L' and line[8] == ' ':
        e = line[9:19].strip()
        print(f'Line {i+1}: L-record E={e}, set current_l_idx={i}')
        current_l_idx = i
        continue
    if current_l_idx is not None and 'N=' in line:
        c7 = line[6] if len(line) > 6 else '?'
        print(f'Line {i+1}: FOUND N= in line, col7=[{c7}]')
        if len(line) > 7 and line[6] == 'c':
            print(f'  CAPTURED for L idx {current_l_idx}')
        else:
            print(f'  NOT cL: col7=[{c7}]')

print('\n--- First data lines ---')
for i in range(18, 28):
    l = lines[i]
    tag = ''
    if len(l) >= 10:
        if l[7] == 'L' and l[8] == ' ': tag = 'L'
        elif 'N=' in l: tag = 'N='
        elif l[6] == 'c': tag = 'c'
    print(f'  {i+1}: [{tag}] [{l.rstrip()[:70]}]')
