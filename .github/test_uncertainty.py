# Test ENSDF uncertainty conversion
cases = [
    ('716', '0.7'),      # Ep=716±0.7
    ('754.1', '0.7'),    # Ep=754.1±0.7
    ('2073.5', '1.2'),   # Ep=2073.5±1.2
    ('1165', None),      # Ep=1165 (no uncertainty)
]

for ep, dep in cases:
    if dep is None:
        print(f'{ep} (no uncertainty) -> S="{ep}", DS="  "')
    else:
        dep_float = float(dep)
        if '.' in ep:
            decimals = len(ep.split('.')[1])
        else:
            decimals = 0
        
        # Method 1: Convert to integer in last digit position
        dep_int = int(round(dep_float * (10 ** decimals)))
        
        # Method 2: If Ep has no decimals but dEp < 1, add decimal to Ep
        if decimals == 0 and dep_float < 1:
            ep_decimal = ep + '.0'
            dep_int_v2 = int(round(dep_float * 10))
            print(f'{ep}±{dep} -> OPTION A: S="{ep}", DS="{dep_int}" (rounds to ±{dep_int} keV)')
            print(f'{ep}±{dep} -> OPTION B: S="{ep_decimal}", DS="{dep_int_v2}" (±{dep_float} keV)')
        else:
            print(f'{ep}±{dep} -> S="{ep}", DS="{dep_int}"')
