with open(r'd:\X\ND\ENSDF\XUNDL\2026TAAA_CLR1074_173W.ens', 'r') as f:
    lines = f.readlines()
    line38 = lines[37]
    content = line38.replace('\n', '').replace('\r', '')
    print(f'Line 38 repr: {repr(line38)}')
    print(f'Line 38 content length: {len(content)}')
