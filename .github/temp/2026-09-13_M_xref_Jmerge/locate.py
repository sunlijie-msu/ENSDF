import io, sys, hashlib, os
p = sys.argv[1] if len(sys.argv) > 1 else r"A34\S34\new\S34_adopted.ens"
raw = open(p, "rb").read()
print("sha256 :", hashlib.sha256(raw).hexdigest().upper())
print("mtime  :", os.path.getmtime(p))
L = raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
if L and L[-1] == "":
    L.pop()
print("lines  :", len(L))
print("--- lines containing 1977GrZH ---")
for i, l in enumerate(L):
    if "1977GrZH" in l:
        print("%5d len=%3d |%s|" % (i + 1, len(l), l))
print("--- lines 267-285 ---")
for i in range(266, min(285, len(L))):
    print("%5d len=%3d |%s|" % (i + 1, len(L[i]), L[i]))
