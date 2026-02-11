import re

text = 'J$1986|g to 1572, 1/2+ and 1566.7|g to 1991, 7/2-.'
pattern = r'(\d+\.?\d*)\|g\s+(?:[^,]+?\s+)?to\s+(\d+\.?\d*),\s*([^\s.,;]+(?:\s*\([^)]*\))?[^\s.,;]*?)(?:\s+level|,\s*\d+\.?\d*\|g|and|;|\s*$)'

matches = list(re.finditer(pattern, text))
print(f'Found {len(matches)} matches')
for i, m in enumerate(matches):
    print(f'Match {i+1}:')
    print(f'  Gamma energy: {m.group(1)}')
    print(f'  Level energy: {m.group(2)}')
    print(f'  J-pi: {m.group(3)!r}')
    print(f'  Full match: {m.group(0)!r}')
