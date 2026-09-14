"""Print length, trailing-blank count and content of lines matching a regex.

Usage: python measure.py FILE REGEX
"""
import re
import sys

raw = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
pat = re.compile(sys.argv[2])
for i, ln in enumerate(raw.split('\n'), 1):
    if pat.search(ln):
        print('line %-5d len=%-4d pad=%-3d |%s|'
              % (i, len(ln), len(ln) - len(ln.rstrip()), ln.rstrip()))
