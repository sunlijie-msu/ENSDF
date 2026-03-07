import json
data = json.load(open(r'd:\X\ND\ENSDF\.github\temp\ep_averages2.json'))
for r in data['details']:
    extra = '(2-line)' if r['extra_line'] else '(1-line)'
    print(f"L{r['line_num']:4d} N={r['n_measured']} {extra}:")
    # show old (just content part, truncated for readability)
    old_lines = r['old'].split('\r\n')
    for ol in old_lines:
        print(f"  OLD: {ol.rstrip()}")
    print(f"  NEW: {r['new']}")
    print()
