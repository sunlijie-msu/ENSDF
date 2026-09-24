#!/usr/bin/env python3
"""Inventory cG M$ comment phrasings in an ENSDF file (read-only)."""
import re
import sys
from collections import Counter
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1])
    lines = path.open(encoding='utf-8', newline='').read().split('\r\n')
    variants = Counter()
    examples = {}
    for i, line in enumerate(lines, start=1):
        if line[6:7] == 'c' and line[7:8] == 'G' and 'M$' in line:
            match = re.search(r'M\$(.*?)(?:from|\.)', line[9:])
            if match:
                key = match.group(1).rstrip()
                variants[key] += 1
                examples.setdefault(key, i)
    for key, count in variants.most_common():
        print(f'{count:>3}  line {examples[key]:>5}  {key!r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
