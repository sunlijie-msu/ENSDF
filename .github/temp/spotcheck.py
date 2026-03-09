import random

lines = open('A34/Cl34/raw/1977DA02_1983WA27.adp').read().splitlines()
g_records = [l for l in lines if l.startswith(' 34CL  G')]
sample = random.sample(g_records, 5)

print("\n--- 5% SPOT CHECK ---")
print("Ruler:")
print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
print('11111111112222222222333333333344444444445555555555666666666677777777778888888899')

for l in sample:
    padded = l.ljust(80)
    print(padded)
    print(f"  Col 23-29 (RI) : '{padded[22:29]}'")
    print(f"  Col 30-31 (DRI): '{padded[29:31]}'")
