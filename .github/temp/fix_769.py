with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'rb') as f:
    content = f.read()

lines = content.split(b'\r\n')

old_comment = b' 34CL cG RI$other: 100.0 {I28} (1977Da02)'
new_comment = b' 34CL cG RI$other: 97.3 {I27} (1977Da02)'

# Pad to 80 chars
old_line = old_comment + b' ' * (80 - len(old_comment))
new_line = new_comment + b' ' * (80 - len(new_comment))

print('old len=%d: |%s|' % (len(old_line), old_line.decode()))
print('new len=%d: |%s|' % (len(new_line), new_line.decode()))

assert len(old_line) == 80
assert len(new_line) == 80

count = content.count(old_line + b'\r\n')
print('Occurrences of old: %d' % count)

if count == 1:
    new_content = content.replace(old_line + b'\r\n', new_line + b'\r\n', 1)
    with open('D:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens', 'wb') as f:
        f.write(new_content)
    print('Fixed successfully.')
else:
    print('ERROR: expected 1 occurrence, found %d' % count)
