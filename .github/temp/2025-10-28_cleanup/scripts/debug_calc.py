#!/usr/bin/env python3
"""Debug script to trace E(level) calculations."""

FACTOR = 0.9711849866847
SP = 6370.81

filename = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'

with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check line 1439 specifically (L 7782.1)
print("Checking line 1439 (L 7782.1):")
line = lines[1438]  # 0-indexed
print(f"Line: {repr(line)}")
print(f"Length: {len(line)}")

e_str = line[9:19].strip()
de_str = line[19:21].strip()
s_str = line[64:74].strip()
ds_str = line[74:76].strip() if len(line) > 75 else ''

print(f"E field (cols 10-19): '{e_str}'")
print(f"DE field (cols 20-21): '{de_str}'")
print(f"S field (cols 65-74): '{s_str}'")
print(f"DS field (cols 75-76): '{ds_str}'")

if s_str:
    s_parts = s_str.split()
    print(f"S parts: {s_parts}")
    print(f"Number of S parts: {len(s_parts)}")
    
    if len(s_parts) >= 2:
        print("Processing S parts...")
        s_val = float(s_parts[0])
        ds_val = s_parts[1]
        
        e_calc = s_val * FACTOR + SP
        decimals = len(s_parts[0].split('.')[1]) if '.' in s_parts[0] else 0
        e_correct = round(e_calc, decimals)
        
        print(f"\nS value: {s_val}")
        print(f"DS value: {ds_val}")
        print(f"E calculated: {e_calc:.10f}")
        print(f"Decimals: {decimals}")
        print(f"E correct (rounded): {e_correct}")
        print(f"E current (from file): {float(e_str)}")
        print(f"Difference: {abs(float(e_str) - e_correct):.6f}")
        print(f"Mismatch? {abs(float(e_str) - e_correct) > 0.01}")
