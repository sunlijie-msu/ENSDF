import re

source = """
146.5 ± 0.5
461.2 ± 0.5
665.7 ± 0.5
1230.5 ± 0.3
1887.2 ± 0.3
2158.1 ± 0.3
2181.2 ± 0.5
2375.6 ± 0.5
2579.9 ± 0.5
2610.6 ± 0.5
2721.4 ± 0.7
3128.9 ± 0.5
3333.9 ± 1.0
3383.6 ± 0.6
3545.2 ± 0.8
3600.3 ± 0.8
3631.1 ± 0.8
3645.6 ± 1.5
(3659.4 ± 1.5)
3773.9 ± 1.0
3941.2 ± 1.5
(3964.2 ± 1.5)
3982.2 ± 0.5
4075.9 ± 1.0
4139.9 ± 1.5
4325.6 ± 0.5
4352.9 ± 1.0
4416.4 ± 0.5
4444.7 ± 1.5
4462.2 ± 1.5
4515.3 ± 0.5
4605.8 ± 1.0
4609.7 ± 1.5
4638.3 ± 1.5
(4695 ± 2)
4717.5 ± 1.0
4823.4 ± 1.0
(4941.4 ± 1.5)
4959 ± 2
4993 ± 2
5170 ± 2
(5383 ± 2)
5540 ± 2
"""

def format_ensdf(text):
    lines = text.strip().split('\n')
    output = []
    # Identification and History (simplified for scaffold)
    output.append(' 34CL    1977DA02      1977DA02                                 202603              ')
    output.append(' 34CL PN                                                                     7      ')
    # Ground state
    output.append(' 34CL  L 0.0                                                                        ')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        tentative = line.startswith('(') and line.endswith(')')
        if tentative:
            line = line[1:-1].strip()
            
        parts = line.split('±')
        energy = parts[0].strip()
        unc = parts[1].strip()
        
        # Uncertainty formatting
        if '.' in energy:
            dec = len(energy.split('.')[1])
            u_val = float(unc)
            u_int = int(round(u_val * (10**dec)))
            u_str = str(u_int)
        else:
            u_str = str(int(float(unc)))
            
        q = '?' if tentative else ' '
        # 1-5: NUCID (space, 34, CL)
        # 8: L
        # 10-19: Energy left-justified
        # 20-21: Uncertainty left-justified
        # 80: Q
        formatted = f' 34CL  L {energy:10}{u_str:2}'
        formatted = formatted.ljust(79) + q
        output.append(formatted)
    return output

for line in format_ensdf(source):
    print(line)
