line = ' 35CL  L 7069.0                                                 716             '
print(f'Length: {len(line)}')
print(f'Char at pos 7: {repr(line[7])}')
print(f'Char at pos 8: {repr(line[8])}')
print(f'line[8] == "L": {line[8] == "L"}')
print(f'Chars 64-74: {repr(line[64:74])}')
print(f'Stripped: {repr(line[64:74].strip())}')
