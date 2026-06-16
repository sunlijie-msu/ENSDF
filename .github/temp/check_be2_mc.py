"""Extract both MIN/MAX and MC BE2(DOWN) from ruler.rpt for 17 gammas"""
import re

with open(r'D:\X\ND\Files\ruler.rpt', 'r', encoding='utf-8') as f:
    rpt = f.read()

md_data = [
    (486.7, '0.46 +0.04/-0.04', 0, 'QB1'),
    (792.4, '0.30 +0.02/-0.02', 0, 'QB1'),
    (1044.0, '0.22 +0.02/-0.02', 0, 'QB1'),
    (1239.5, '0.09 +0.01/-0.01', 0, 'QB1'),
    (1468.0, '>0.02', 1, 'QB1'),
    (1205.2, '>0.05', 1, 'QB1'),
    (457.2, '0.48 +0.08/-0.07', 0, 'QB2'),
    (748.2, '0.47 +0.04/-0.04', 0, 'QB2'),
    (841.4, '0.42 +0.05/-0.05', 0, 'QB2'),
    (938.3, '0.35 +0.03/-0.03', 0, 'QB2'),
    (1040.2, '0.26 +0.03/-0.02', 0, 'QB2'),
    (1164.1, '>0.17', 1, 'QB2'),
    (679.9, '0.25 +0.04/-0.03', 0, 'QB3'),
    (783.7, '0.27 +0.04/-0.03', 0, 'QB3'),
    (918.8, '0.26 +0.03/-0.03', 0, 'QB3'),
    (1108.5, '0.24 +0.03/-0.03', 0, 'QB3'),
    (1328.4, '>0.20', 1, 'QB3'),
]

sections = re.split(r'--->gamma#', rpt)
print(f'{"Eg":>8} {"Band":>4} {"MD_BE2":>16} {"MINMAX_BE2DOWN":>22} {"MC_BE2DOWN":>22}')
print('-' * 90)

for sec in sections[1:]:
    eg_m = re.search(r'EG=([\d.]+)', sec)
    if not eg_m:
        continue
    eg = float(eg_m.group(1))
    md = None
    for m in md_data:
        if abs(m[0] - eg) < 0.5:
            md = m
            break
    if not md:
        continue

    v_str, lim, band = md[1], md[2], md[3]

    # MIN/MAX section
    idx2 = sec.find('MINIMUM and MAXIMUM')
    mm = sec[idx2:].split('<3>')[0] if idx2 >= 0 else ''

    # MC section
    idx3 = sec.find('<3> Use uncertainties from <MONTE-CARLO>')
    mc = sec[idx3:].split('####')[0] if idx3 >= 0 else ''

    is_limit = ('T1/2 is limit' in mc) or ('limit' in mc and 'not suitable' in mc) or lim

    # Extract MIN/MAX BE2(DOWN)
    bd_mm = re.search(r'BE2\(DOWN\)\s*=\s*([\d.]+)\s+([+-]\d+)\s*([+-]\d+)?', mm)
    mm_str = ''
    if bd_mm:
        v_mm = bd_mm.group(1)
        dp = bd_mm.group(2)
        dm = bd_mm.group(3) if bd_mm.lastindex and bd_mm.lastindex >= 3 else dp
        mm_str = f'{v_mm}{dp}{dm}'

    if is_limit:
        mc_str = 'MC not suitable (limit)'
        print(f'{eg:>8.1f} {band:>4} {v_str:>16} {mm_str:>22} {mc_str:>22}')
        continue

    # Extract MC BE2(DOWN) - handle both symmetric (value N) and asymmetric (value+N-M) formats
    bd_mc = re.search(r'BE2\(DOWN\)\s*=\s*([\d.]+)\s+([+-]\d+)\s*([+-]\d+)?', mc)
    mc_str = ''
    if bd_mc:
        v_mc = bd_mc.group(1)
        dp = bd_mc.group(2)
        dm = bd_mc.group(3) if bd_mc.lastindex and bd_mc.lastindex >= 3 else dp
        mc_str = f'{v_mc}{dp}{dm}'
    else:
        # Try symmetric format: "BE2(DOWN)=0.3016 156"
        bd_mc_sym = re.search(r'BE2\(DOWN\)\s*=\s*([\d.]+)\s+(\d+)', mc)
        if bd_mc_sym:
            v_mc = bd_mc_sym.group(1)
            d_mc = bd_mc_sym.group(2)
            mc_str = f'{v_mc}+{d_mc}-{d_mc}'
        else:
            mc_str = 'NOT FOUND'

    print(f'{eg:>8.1f} {band:>4} {v_str:>16} {mm_str:>22} {mc_str:>22}')

print()
print('Note: 4 gammas omitted from MC column -- T1/2 is limit, MC not suitable.')
print('Method: MINIMUM and MAXIMUM (col 3) and MONTE-CARLO (col 4) from ruler.rpt.')
