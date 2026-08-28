# Add column 77 flag 'D' to the four 1975DeZS L-records (10382, 10386, 10443, 10482)
# in S34_30si_a_g_a_n_resonances.ens. Preserves CRLF line endings.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'

with open(path, 'r', encoding='utf-8', newline='') as f:
    text = f.read()

lines = text.split('\r\n')
targets = {'10382', '10386', '10443', '10482'}
modified = []

for i, ln in enumerate(lines):
    # data L record: col6=' ', col7=' ', col8='L', col9=' '
    if len(ln) >= 77 and ln[5:9] == '  L ':
        e = ln[9:19].strip()
        if e in targets:
            # column 77 (0-based index 76) currently a space; set to 'D'
            if ln[76] == ' ':
                ln = ln[:76] + 'D' + ln[77:]
                modified.append((i + 1, e))
    lines[i] = ln

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(lines))

print('modified (line, energy):', modified)
