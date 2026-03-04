import os, glob

def count_ens(pattern):
    lrec = grec = lines = datasets = 0
    for fn in sorted(glob.glob(pattern, recursive=True)):
        datasets += 1
        with open(fn, encoding='utf-8', errors='ignore') as f:
            for line in f:
                lines += 1
                if len(line) >= 8:
                    t = line[7]
                    if t == 'L': lrec += 1
                    elif t == 'G': grec += 1
    return datasets, lrec, grec, lines

# A=34 new/
d, l, g, n = count_ens('A34/*/new/*.ens')
print(f'A34 new: datasets={d} L={l} G={g} lines={n}')

# Per-nuclide A=34
print('A34 per-nuclide counts:')
for el in ['Ne34','Na34','Mg34','Al34','Si34','P34','S34','Cl34','Ar34','K34','Ca34']:
    cnt = len(glob.glob(f'A34/{el}/new/*.ens'))
    print(f'  {el}: {cnt}')

# A=35 submitted
d, l, g, n = count_ens('A35/*/new/*.ens')
print(f'A35 new: datasets={d} L={l} G={g} lines={n}')
per35 = {}
for el in ['Ne35','Na35','Mg35','Al35','Si35','P35','S35','Cl35','Ar35','K35','Ca35']:
    per35[el] = len(glob.glob(f'A35/{el}/new/*.ens'))
print('A35 per-nuclide:', per35)

# A=36 new/
d36, l36, g36, n36 = count_ens('A36/*/new/*.ens')
print(f'A36 new: datasets={d36} L={l36} G={g36} lines={n36}')

# A=60 new/
d60, l60, g60, n60 = count_ens('A60/*/new/*.ens')
print(f'A60 new: datasets={d60} L={l60} G={g60} lines={n60}')
per60 = {}
for el in ['Ca60','Sc60','Ti60','V60','Cr60','Mn60','Fe60','Co60','Ni60','Cu60','Zn60','Ga60','Ge60']:
    per60[el] = len(glob.glob(f'A60/{el}/new/*.ens'))
print('A60 per-nuclide:', per60)
