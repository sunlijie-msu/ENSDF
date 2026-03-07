import json
data = json.load(open(r'd:\X\ND\ENSDF\.github\temp\ep_averages.json'))
for r in data['details']:
    print(f"L{r['line_num']:4d}:")
    print(f"  OLD: {r['old'][20:]}")
    print(f"  NEW: {r['new'][20:]}")
    print()
