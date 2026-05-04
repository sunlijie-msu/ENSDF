"""Cross-check L-record J-pi fields against cL J$ comment content, 200-5200 keV."""
import re

with open(r'A34\Cl34\new\Cl34_adopted.ens') as f:
    lines = f.readlines()

results = []
i = 0
while i < len(lines):
    line = lines[i].rstrip('\n')
    # L-record: col6=blank(idx5), col7=blank(idx6), col8='L'(idx7), col9=blank(idx8)
    if (len(line) >= 9 and line[7] == 'L' and line[5] == ' '
            and line[6] == ' ' and line[8] == ' '):
        e_str = line[9:19].strip()
        try:
            e_val = float(e_str)
        except ValueError:
            i += 1
            continue
        if 200 <= e_val <= 5200:
            jpi = line[21:39].strip()
            lineno = i + 1
            # Scan forward for cL J$ comment: col7='c'(idx6), col8='L'(idx7)
            j_lines = []
            in_jcomment = False
            j = i + 1
            while j < len(lines):
                cl = lines[j].rstrip('\n')
                if len(cl) < 9:
                    j += 1
                    continue
                is_cL = (cl[6] == 'c' and cl[7] == 'L')
                is_new_L = (cl[7] == 'L' and cl[5] == ' ' and cl[6] == ' ')
                if is_cL:
                    content = cl[9:].strip()
                    if not in_jcomment and content.startswith('J$'):
                        in_jcomment = True
                        j_lines.append(content[2:])
                    elif in_jcomment and not content[1:2] == '$':
                        # continuation (no identifier$)
                        j_lines.append(content)
                    elif in_jcomment:
                        # hit next identifier$ — stop J$ collection
                        break
                    j += 1
                elif is_new_L:
                    break
                else:
                    j += 1
            results.append((e_val, lineno, jpi, ' '.join(j_lines)))
    i += 1

print(f'Found {len(results)} levels 200-5200 keV\n')
for e, ln, jpi, jcomment in results:
    flag = ' <<< NO J$ COMMENT' if not jcomment else ''
    print(f'L{ln:4d} E={e:8.2f}  Jpi=|{jpi:18s}|  J$={jcomment[:100]}{flag}')
