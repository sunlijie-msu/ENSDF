import re

path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")

targets = [308, 382, 384, 386, 527, 529, 531, 533, 567, 569, 572, 617, 619, 622]
print("=== STRICT 14: current col-77 state ===")
for t in targets:
    ln = lines[t - 1]
    print("line %-5d len=%-3d col77=%r  %s" % (t, len(ln), ln[76] if len(ln) > 76 else "", ln[9:19].strip()))

print()
print("=== all G-records with non-blank col 77 ===")
n = 0
for i, ln in enumerate(lines, 1):
    if len(ln) > 76 and ln[7] == "G" and ln[6] == " " and ln[76] != " ":
        n += 1
        print("line %-5d len=%-3d flag=%r E=%s" % (i, len(ln), ln[76], ln[9:19].strip()))
print("count:", n)
print()
print("any col-76 (space-78) violations:", sum(1 for ln in lines if len(ln) > 77 and ln[7] == "G" and ln[6] == " " and ln[77] != " "))
