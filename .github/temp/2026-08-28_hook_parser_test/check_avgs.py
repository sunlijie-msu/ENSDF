import subprocess, re, sys

PY = r'C:\Users\sun\AppData\Local\Programs\Python\Python311\python.exe'
AVG = r'd:\X\ND\ENSDF\.github\scripts\Java_Average.py'

# (label, file_level, file_de, pair_string)
cases = [
    ('L3304.9', '3304.9', '20', '3305 2 3302 10'),
    ('L4118',   '4118',   '4',  '4118 4 4120 10'),
    ('L4627',   '4627',   '4',  '4627 5 4629 10'),
    ('L5384',   '5384',   '5',  '5384 6 5384 10'),
    ('L6174',   '6174',   '6',  '6174 8 6173 10'),
    ('L6254',   '6254',   '6',  '6256 8 6251 10'),
    ('L6345',   '6345',   '6',  '6346 8 6344 10'),
    ('L6482',   '6482',   '7',  '6483 8 6480 14'),
    ('L6640',   '6640',   '7',  '6644 9 6634 10'),
    ('L6690',   '6690',   '7',  '6690 9 6690 10'),
    ('L6959',   '6959',   '7',  '6959 10 6959 10'),
    ('L7114',   '7114',   '7',  '7115 10 7112 10'),
    ('L7393',   '7393',   '10', '7388 14 7398 14'),
    ('L7632',   '7632',   '7',  '7633 11 7631 10'),
    ('L7753',   '7753',   '9',  '7755 11 7750 14'),
    ('L7783',   '7783',   '9',  '7785 11 7783 14'),
]

print(f"{'file level':10} {'file (DE)':10} {'computed':24} {'method':16} match?")
for label, fle, fde, pair in cases:
    r = subprocess.run([PY, AVG] + pair.split(), capture_output=True, text=True)
    out = r.stdout + r.stderr
    m = re.search(r'suggested adopted result:\s*([\d.]+)\((\d+)\)', out)
    meth = re.search(r'\((Weighted-Of-All|Unweighted[^)]*)\)', out)
    comp = f"{m.group(1)}({m.group(2)})" if m else '??'
    method = meth.group(1) if meth else '?'
    # compare: file value/unc vs computed (same decimal digits)
    match = '??'
    if m:
        cv, cu = float(m.group(1)), int(m.group(2))
        fv, fd = float(fle), int(fde)
        # normalize: compare with tolerance based on decimals
        tol = 10**(-len(m.group(1).split('.')[-1])) if '.' in m.group(1) else 1.0
        same_val = abs(cv - fv) <= tol
        same_unc = cu == fd
        match = 'OK' if (same_val and same_unc) else 'MISMATCH'
    print(f"{label:10} {fle+' '+fde:10} {comp:24} {method:16} {match}")
    if match == 'MISMATCH':
        # show detail
        for line in out.splitlines():
            if 'suggested' in line or 'adopted' in line or 'weighted average' in line or 'unweighted' in line:
                print('     ', line.strip())
