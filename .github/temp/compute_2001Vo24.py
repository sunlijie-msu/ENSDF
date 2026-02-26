import math

factor = 9.9 / 9.5  # 1.04210526316 => divide to scale DOWN

targets = [
    (759,  '0.14', 2, 2),   # line, val_str, decimal_places, existing_Inum
    (1117, '0.7',  1, 2),
    (1499, '2.2',  1, 3),
    (2079, '4.2',  1, 8),
    (2119, '3.3',  1, 5),
    (2150, '1.0',  1, 3),
    (2311, '6.1',  1, 6),
]

print(f'Factor = {factor:.10f} (divide = scale DOWN)')
print()
print(f'{"Line":>5}  {"Old":>6}  {"Old{In}":>8}  {"Scaled":>12}  {"Rounded":>10}  Changed?')
print('-' * 65)

for line, val_str, dec_places, Inum in targets:
    old_val = float(val_str)
    new_val = old_val / factor
    rounded = round(new_val, dec_places)
    val_fmt = f'{rounded:.{dec_places}f}'
    changed = (val_fmt != val_str)
    unc_tag = '{I' + str(Inum) + '}'
    print(f'{line:>5}  {val_str:>6}  {unc_tag:>8}  {new_val:>12.6f}  {val_fmt:>10}  {"YES" if changed else "no change"}')
