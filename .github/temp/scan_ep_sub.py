raw = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

ep_sub = [(i+1, lines[i].rstrip()) for i in range(len(lines)) if 'cL $E{-p}(lab)=' in lines[i]]
print(f'Total cL $E{{-p}}(lab)= lines: {len(ep_sub)}')
print()
for ln, s in ep_sub[:5]:
    print(f'L{ln}: {s}')
print('...')
for ln, s in ep_sub[-3:]:
    print(f'L{ln}: {s}')

# For each, find the L record that precedes it
print('\n--- L records and col77 check ---')
for ln, _ in ep_sub[:5]:
    # Walk backwards to find most recent L record
    for j in range(ln-2, -1, -1):
        stripped = lines[j].rstrip()
        if len(stripped) >= 8 and stripped[7] == 'L' and stripped[5:7] == '  ':
            col77 = stripped[76] if len(stripped) >= 77 else ' '
            print(f'  cL at L{ln} -> L-rec at L{j+1}: col77={repr(col77)} len={len(stripped)}')
            print(f'    {stripped}')
            break
