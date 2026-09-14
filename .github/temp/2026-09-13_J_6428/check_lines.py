"""Report the length of each drafted cL-comment line and pad it to 80 columns.

Usage: python check_lines.py DRAFT.txt
Each non-empty line of DRAFT.txt is treated as the text to place AFTER the
11-character prefix ' 34S  cL J$' (line 1) or the 9-character prefix
' 34S 2cL ' (subsequent lines), i.e. the draft text already includes the $ form.
"""
import sys

path = sys.argv[1]
lines = open(path, 'r', encoding='utf-8').read().split('\n')
prefixes = [' 34S  cL J$', ' 34S 2cL ', ' 34S 3cL ', ' 34S 4cL ', ' 34S 5cL ', ' 34S 6cL ']
idx = 0
for ln in lines:
    if not ln.strip():
        continue
    pre = prefixes[idx]
    full = pre + ln
    status = 'OK ' if len(full) <= 80 else 'TOO LONG'
    print('%s len=%2d (text=%2d, budget=%2d) [%s]' % (status, len(full), len(ln), 80 - len(pre), ln))
    idx += 1
