ei = 7069.0
ep = '716'

ex_str = f'{ei:.1f}' if ei == int(ei) else str(ei)
print(f'ex_str: [{ex_str}]')

l_line = f' 35CL  L {ex_str:<10}' + ' ' * 45 + f'{ep:<10}'
print(f'Before ljust: {len(l_line)} chars')
print(f'Line: [{l_line}]')

l_line = l_line[:80].ljust(80)
print(f'After ljust: {len(l_line)} chars')
print(f'Line: [{l_line}]')
