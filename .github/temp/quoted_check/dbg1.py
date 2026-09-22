import collections
p = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
b = open(p, "rb").read()
print("bytes", len(b), "CRLF", b.count(b"\r\n"), "LF", b.count(b"\n"))
t = b.decode("ascii")
lines = t.split("\r\n")
print("total lines", len(lines))
c = collections.Counter()
for l in lines:
    if len(l) > 9 and l[6:7] == "c" and l[7:8] == "L":
        c[l[5:6]] += 1
print("cL col6 chars:", dict(c))
for n in [512, 160, 729, 756, 868, 901]:
    l = lines[n - 1]
    print(n, repr(l[:12]), len(l), "|", repr(l[60:]))
