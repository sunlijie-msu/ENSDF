"""
Step 2 Java Averaging Script.
Run Java_Average.py for all 28 WILL_AVERAGE transitions.
Each entry: {'nei': Ei, 'eg': Eg, 'srcL': N, 'entries': [(val, unc, NSR), ...], 'hy02': (val, unc)}
"""
import subprocess, sys, re

def run_java(vals_uncs):
    """Run Java_Average.py with value/unc pairs. Returns stdout."""
    args = [sys.executable, r'.github\scripts\Java_Average.py']
    for v, u in vals_uncs:
        args += [str(v), str(u)]
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout

def parse_result(stdout):
    """Extract 'Suggested Adopted Result: X +/- Y' and method."""
    val, unc, method = None, None, None
    for line in stdout.splitlines():
        m = re.search(r'Suggested Adopted Result:\s*([\d.E+\-]+)\s*\+/-\s*([\d.E+\-]+)', line)
        if m:
            val, unc = m.group(1), m.group(2)
        if 'Weighted' in line and 'Suggested' not in line:
            method = 'weighted'
        if 'Unweighted' in line and 'Suggested' not in line:
            method = 'unweighted'
    return val, unc, method

def in_to_unc(ri_str, in_str):
    """Convert {In} notation to absolute uncertainty."""
    n = int(in_str)
    dec = len(ri_str.split('.')[1]) if '.' in ri_str else 0
    return n * (10**(-dec))

# 28 WILL_AVERAGE transitions
cases = [
  # Ei=1887.29
  {'ei':1887.29,'eg':1740.89,'srcL':221,
   'entries':[('66.7','33','1977Da02'),('74.2','12','1983Wa27'),('100','40','1969Gr29')],
   'hy02':('67','7')},
  # Ei=2157.9
  {'ei':2157.9,'eg':927.57,'srcL':234,
   'entries':[('9.1','15','1977Da02'),('8.54','31','1983Wa27'),('19','6','1969Gr29')],
   'hy02':('10.5','60')},
  {'ei':2157.9,'eg':2011.5,'srcL':252,
   'entries':[('21.2','15','1977Da02'),('20.1','5','1983Wa27')],
   'hy02':('19','9')},
  {'ei':2157.9,'eg':2157.9,'srcL':260,
   'entries':[('21.2','15','1977Da02'),('23.8','5','1983Wa27'),('38','14','1969Gr29')],
   'hy02':('19','5')},
  # Ei=2181.1
  {'ei':2181.1,'eg':1515.8,'srcL':275,
   'entries':[('25.5','21','1977Da02'),('24.7','14','1983Wa27')],
   'hy02':('26','12')},
  {'ei':2181.1,'eg':1719.9,'srcL':277,
   'entries':[('87','4','1977Da02'),('69.8','27','1983Wa27')],
   'hy02':('49','9')},
  # Ei=2611.03
  {'ei':2611.03,'eg':1945.73,'srcL':338,
   'entries':[('51.4','29','1977Da02'),('38.3','28','1983Wa27')],
   'hy02':('10.0','80')},
  # Ei=2721.3
  {'ei':2721.3,'eg':563.4,'srcL':350,
   'entries':[('16.3','21','1977Da02'),('14.5','11','1983Wa27')],
   'hy02':('17','7')},
  {'ei':2721.3,'eg':834.01,'srcL':352,
   'entries':[('6.1','21','1977Da02'),('4.3','4','1983Wa27')],
   'hy02':('4.3','21')},
  {'ei':2721.3,'eg':1490.97,'srcL':355,
   'entries':[('4.1','21','1977Da02'),('4.5','4','1983Wa27')],
   'hy02':('6.4','21')},
  {'ei':2721.3,'eg':2056,'srcL':358,
   'entries':[('12.2','21','1977Da02'),('16.4','11','1983Wa27')],
   'hy02':('17','7')},
  {'ei':2721.3,'eg':2574.9,'srcL':366,
   'entries':[('36.7','21','1977Da02'),('39.5','11','1983Wa27')],
   'hy02':('40','7')},
  {'ei':2721.3,'eg':2721.3,'srcL':369,
   'entries':[('28.6','21','1977Da02'),('34.1','11','1983Wa27')],
   'hy02':('28','7')},
  # Ei=3600.28
  {'ei':3600.28,'eg':878.98,'srcL':463,
   'entries':[('98','4','1977Da02'),('93.9','11','1983Wa27'),('85','13','1969Gr29')],
   'hy02':('92','11')},
  {'ei':3600.28,'eg':1224.58,'srcL':474,
   'entries':[('14.9','21','1977Da02'),('15.7','19','1983Wa27')],
   'hy02':('17','8')},
  # Ei=3631.7
  {'ei':3631.7,'eg':3485.1,'srcL':514,
   'entries':[('82','4','1977Da02'),('83.5','13','1983Wa27')],
   'hy02':('92','14')},
  # Ei=3983.0
  {'ei':3983.0,'eg':1261.7,'srcL':584,
   'entries':[('12.7','16','1977Da02'),('13.9','11','1983Wa27')],
   'hy02':('12.3','62')},
  {'ei':3983.0,'eg':1825.1,'srcL':592,
   'entries':[('46.0','32','1977Da02'),('42.3','17','1983Wa27'),('72','17','1969Gr29')],
   'hy02':('40','8')},
  # Ei=4139.7
  {'ei':4139.7,'eg':1981.7,'srcL':651,
   'entries':[('36','9','1977Da02'),('45','4','1983Wa27')],
   'hy02':('39','14')},
  # Ei=4515.7
  {'ei':4515.7,'eg':4369.0,'srcL':733,
   'entries':[('27','4','1977Da02'),('25.0','25','1983Wa27')],
   'hy02':('19','12')},
  # Ei=6169.4
  {'ei':6169.4,'eg':2568.6,'srcL':1292,
   'entries':[('23.5','24','1977Da02'),('39','22','1969Gr29')],
   'hy02':('22','13')},
  {'ei':6169.4,'eg':2623.8,'srcL':1295,
   'entries':[('14.7','74','1977Da02'),('22','11','1969Gr29')],
   'hy02':('16','6')},
  {'ei':6169.4,'eg':4938.3,'srcL':1320,
   'entries':[('11.8','59','1977Da02'),('17','8','1969Gr29')],
   'hy02':('9.4','31')},
  {'ei':6169.4,'eg':6022.0,'srcL':1330,
   'entries':[('74','8','1977Da02'),('100','17','1969Gr29')],
   'hy02':('91','22')},
  # Ei=6208.2
  {'ei':6208.2,'eg':2224.0,'srcL':1410,
   'entries':[('7.3','38','1977Da02'),('26','15','1969Gr29')],
   'hy02':('12','4')},
  {'ei':6208.2,'eg':2661.9,'srcL':1421,
   'entries':[('48','5','1977Da02'),('56','17','1969Gr29')],
   'hy02':('49','12')},
]

print("JAVA AVERAGING RESULTS")
print("="*80)
for c in cases:
    # Build value/unc pairs: convert {In} to absolute unc
    pairs = []
    for (val, in_n, nsr) in c['entries']:
        unc = in_to_unc(val, in_n)
        pairs.append((val, unc))
    # Add 1971HY02
    hy02_v, hy02_dri = c['hy02']
    hy02_unc = in_to_unc(hy02_v, hy02_dri)
    pairs.append((hy02_v, hy02_unc))
    
    stdout = run_java(pairs)
    val, unc, method = parse_result(stdout)
    print(f"\nEi={c['ei']}, Eg={c['eg']}, srcL={c['srcL']}")
    print(f"  Input: {[(v,u) for v,u in pairs]}")
    print(f"  Java suggests: {method or 'unknown'}")
    print(f"  Suggested Adopted Result: {val} +/- {unc}")
    # Show full Java output for debugging
    for line in stdout.splitlines():
        if 'Weighted' in line or 'Unweighted' in line or 'Suggested' in line:
            print(f"  >> {line.strip()}")
