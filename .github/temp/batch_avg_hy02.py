"""
Batch Java_Average.py runs for 20 D-flagged G records
where 1971Hy02 values in Other: should join the 1977Da02 average.
"""
import subprocess
import sys

python = sys.executable

cases = [
  ('L6169 G2092.7',  ['14.7','7.4', '16','6']),
  ('L6169 G2185.9',  ['100','10', '100','25', '100','19']),
  ('L6169 G3447.5',  ['20.6','2.1', '25','13']),
  ('L6169 G3557.8',  ['5.9','3.0', '13','6']),
  ('L6169 G3987.7',  ['14.7','7.4', '16','6']),
  ('L6169 G4281.4',  ['8.8','4.4', '6.3','3.1']),
  ('L6208 G2130.8',  ['18.8','1.9', '14.3','8.2']),
  ('L6208 G2575.3',  ['20.8','2.1', '20','10']),
  ('L6208 G2606.7',  ['100','10', '100','20', '100','21']),
  ('L6208 G4025.7',  ['6.3','3.1', '8.2','2.1']),
  ('L6229 G1589.7',  ['3.3','1.8', '6.0','2.0']),
  ('L6229 G1712.9',  ['24.4','2.5', '22','6']),
  ('L6229 G1811.3',  ['6.7','3.3', '6.0','2.0']),
  ('L6229 G1874.4',  ['20','2', '16','6']),
  ('L6229 G2088.9',  ['13.3','1.3', '12','4']),
  ('L6229 G2454.8',  ['33.3','3.3', '26','6']),
  ('L6229 G3507.1',  ['100','10', '100','12']),
  ('L6229 G4070.5',  ['11.1','5.6', '10','4']),
  ('L6229 G5766.9',  ['4.4','2.2', '2.0','1.0']),
  ('L6229 G6228.01', ['3.3','1.8', '1.60','0.80']),
]

for label, args in cases:
    full_args = [python, '.github/scripts/Java_Average.py'] + args
    r = subprocess.run(full_args, capture_output=True, text=True)
    lines = r.stdout.strip().split('\n')
    result = [l.strip() for l in lines if 'Suggested' in l or 'Weighted' in l or 'Unweighted' in l]
    print(f"{label}:")
    for l in result[:3]:
        print(f"  {l}")
    print()
