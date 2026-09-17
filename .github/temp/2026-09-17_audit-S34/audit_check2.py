p = r"A34\S34\new\S34_34s_e_eP.ens"
lines = open(p, "rb").read().split(b"\r\n")
if lines and lines[-1] == b"":
    lines = lines[:-1]
caret_total = 0
bad_caret = []
for i, l in enumerate(lines, 1):
    for idx, c in enumerate(l):
        if c == ord("^"):
            caret_total += 1
            if l[idx - 1:idx] != b"|":
                bad_caret.append((i, idx + 1, l[max(0, idx - 12):idx + 6]))
print("total '^':", caret_total)
print("caret NOT preceded by '|':", bad_caret)
print("count |^ sequences:", sum(l.count(b"|^") for l in lines))
print("count |' sequences:", sum(l.count(b"|'") for l in lines))
print("count {+2} tokens:", sum(l.count(b"{+2}") for l in lines))
print("count R{-tr} tokens:", sum(l.count(b"R{-tr}") for l in lines))
print("count B(M|L,q) tokens:", sum(l.count(b"B(M|L,q)") for l in lines))
print("count |L=1 tokens:", sum(l.count(b"|L=1") for l in lines))
for i, l in enumerate(lines, 1):
    if b"|^" in l or b"|'" in l:
        print("notion line", i, ":", l.decode("ascii").rstrip()[:78])
