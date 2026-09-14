"""Print the git diff hunk(s) around a search string (avoiding shell redirection issues).

Usage: python gitdiff.py FILE SEARCH
"""
import subprocess
import sys

path, search = sys.argv[1], sys.argv[2]
out = subprocess.run(['git', 'diff', '-U2', '--', path],
                     capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
lines = out.split('\n')
hits = [i for i, l in enumerate(lines) if search in l]
print('diff lines: %d, hits: %d' % (len(lines), len(hits)))
shown = set()
for h in hits:
    lo, hi = max(0, h - 6), min(len(lines), h + 7)
    if (lo, hi) in shown:
        continue
    shown.add((lo, hi))
    print('---- context around line %d ----' % (h + 1))
    for i in range(lo, hi):
        print('%4d %s' % (i + 1, lines[i]))
