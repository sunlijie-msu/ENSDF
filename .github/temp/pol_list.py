import re
lines = open(r'XUNDL/2026LIAA_CV10930_71As.ens', encoding='utf-8').read().splitlines()
gammas = []
cur = None
for l in lines:
    if len(l) < 41:
        continue
    if l[7] == 'L' and l[5:7] == '  ':
        cur = float(l[9:19].strip())
    elif l[7] == 'G' and l[5:7] == '  ':
        gammas.append({'Ei': cur, 'Eg': float(l[9:19].strip()), 'M': l[32:41].strip(), 'ado': None, 'pol': None})
    elif l[6] == 'c' and l[7] == 'G' and gammas and gammas[-1]['Ei'] == cur and gammas[-1]['ado'] is None:
        txt = l[9:].strip()
        if txt.startswith('$') and 'R{-ADO}' in txt or 'POL=' in txt:
            m = re.search(r'R\{-ADO\}=([\d.]+) \{I(\d+)\}', txt)
            if m and gammas[-1]['ado'] is None:
                gammas[-1]['ado'] = float(m.group(1))
            m2 = re.search(r'POL=([+-])([\d.]+) \{I(\d+)\}', txt)
            if m2 and gammas[-1]['pol'] is None:
                gammas[-1]['pol'] = (m2.group(1), float(m2.group(2)))
    elif l[6] == 'c' and l[7] == 'G':
        txt = l[9:].strip()
        if 'POL=' in txt and gammas and gammas[-1]['pol'] is None:
            m2 = re.search(r'POL=([+-])([\d.]+) \{I(\d+)\}', txt)
            if m2:
                gammas[-1]['pol'] = (m2.group(1), float(m2.group(2)))
        if 'R{-ADO}' in txt and gammas and gammas[-1]['ado'] is None:
            m = re.search(r'R\{-ADO\}=([\d.]+) \{I(\d+)\}', txt)
            if m:
                gammas[-1]['ado'] = float(m.group(1))

# print all POL entries with M and level info
print('=== ALL TRANSITIONS WITH POL ===')
for i, g in enumerate(gammas, 1):
    if g['pol']:
        print('gamma#%3d Ei=%7s Eg=%7s M=%-9s POL=%s%s ADO=%s' % (
            i, g['Ei'], g['Eg'], g['M'], g['pol'][0], g['pol'][1], g['ado']))
