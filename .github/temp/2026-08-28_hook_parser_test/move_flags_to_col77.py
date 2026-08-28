# Move every 'F L FLAG=X' into column 77 of its corresponding L record,
# then delete the F L FLAG lines. Preserves CRLF line endings and 80-char lines.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'

with open(path, 'r', encoding='utf-8', newline='') as f:
    text = f.read()

lines = text.split('\r\n')
current_l_index = None
flag_ops = []   # (L-record index, flag letter)
delete_indices = set()

for i, ln in enumerate(lines):
    if len(ln) >= 20 and ln[5:9] == '  L ':
        current_l_index = i
    elif ln.startswith(' 34S F L FLAG='):
        flag = ln.strip().split('=')[-1]
        if current_l_index is None:
            raise SystemExit(f'ERROR: F L FLAG with no preceding L record at line {i+1}')
        flag_ops.append((current_l_index, flag))
        delete_indices.add(i)

# Apply column-77 flags to the L records
for l_index, flag in flag_ops:
    ln = lines[l_index]
    if len(ln) < 77:
        raise SystemExit(f'ERROR: L record at line {l_index+1} too short for col 77')
    if ln[76] != ' ':
        raise SystemExit(f'ERROR: col 77 already occupied at line {l_index+1}: {ln[76]!r}')
    lines[l_index] = ln[:76] + flag + ln[77:]

# Remove F L FLAG lines
new_lines = [ln for i, ln in enumerate(lines) if i not in delete_indices]

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(new_lines))

print('Moved flags to col 77:')
for l_index, flag in flag_ops:
    print(f'   L line {l_index+1} -> col77 {flag!r}')
print('Deleted F L FLAG lines:', len(delete_indices))
