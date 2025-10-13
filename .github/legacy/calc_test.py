s = 1448.0
factor = 0.9711849866847
sp = 6370.81
e_calc = s * factor + sp
print(f"S={s}")
print(f"E_calc={e_calc:.10f}")
print(f"E_rounded_1dec={round(e_calc, 1)}")
print()

# Check a few more
levels = [
    (1448.0, 7777.1, 9),
    (1452.8, 7782.1, 11),
    (1468.6, 7797.1, 9),
    (1509.9, 7837.6, 10),
]

print("Checking calculations:")
for s_val, e_file, de_file in levels:
    e_calc = s_val * factor + sp
    decimals = len(str(s_val).split('.')[1]) if '.' in str(s_val) else 0
    e_correct = round(e_calc, decimals)
    match = "MATCH" if abs(e_file - e_correct) < 0.05 else "MISMATCH"
    print(f"S={s_val:7.1f} -> E_calc={e_calc:10.6f} -> E_rounded={e_correct:7.1f}, FILE={e_file:7.1f} [{match}]")
