#!/usr/bin/env python3
line = ' 35CL  G 7067.3       48     12  (D)'
print('Line:', repr(line))
print('Length:', len(line))
print()

for i in range(min(45, len(line))):
    print(f'Col {i+1:2d} (idx {i:2d}): {repr(line[i])}')
