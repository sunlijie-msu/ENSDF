import os, sys
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, BASE, letter_to_file
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
for ln in (1472, 1579, 1873):
    print("adopted line %d: %r" % (ln, L[ln-1]))
for letter, want in (("Q", "11411.33"), ("Q", "11440.4"), ("L", "12151")):
    p = os.path.join(BASE, letter_to_file[letter])
    for j, l in enumerate(open(p, encoding="utf-8", errors="replace").read().split("\n"), 1):
        if len(l) > 21 and l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].rstrip() == want:
            print("%s = %-28s line %-4d %r" % (letter, letter_to_file[letter], j, l))
