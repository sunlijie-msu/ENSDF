import subprocess, sys
head = subprocess.run(["git", "show", "HEAD:A34/S34/new/S34_adopted.ens"],
                      capture_output=True, text=True, encoding="ascii").stdout.split("\n")
cur = open("A34/S34/new/S34_adopted.ens", encoding="ascii").read().split("\n")
h = [l for l in head if "L 6890" in l][0]
c = [l for l in cur if "L 6890" in l][0]
print("HEAD len=%d" % len(h))
print("CUR  len=%d" % len(c))
print("HEAD repr: %r" % h)
print("CUR  repr: %r" % c)
# character-by-character alignment
i = 0
while i < min(len(h), len(c)) and h[i] == c[i]:
    i += 1
print("first difference at index %d (col %d)" % (i, i + 1))
print("HEAD tail from diff: %r" % h[i:])
print("CUR  tail from diff: %r" % c[i:])
# gaps in HEAD between 6890 and the J value
import re
m = re.search(r"6890( +)1", h)
print("HEAD gap '6890' -> '1' = %d spaces" % len(m.group(1)))
print("CUR  gap '6890' -> '1' = %d spaces" % len(re.search(r"6890( *)1", c).group(1)))
print("HEAD tail after LT spaces = %d" % (len(h) - len(h.rstrip())))
