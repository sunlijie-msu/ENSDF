import re

path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")

def block(i):
    out = []
    j = i  # 0-based index of G record
    while j + 1 < len(lines) and lines[j + 1][6:7] in ("c", "S", "d"):
        out.append(lines[j + 1])
        j += 1
    return out

print("=== existing col-77 'M' records: their comment identifiers ===")
for i, ln in enumerate(lines):
    if len(ln) > 76 and ln[7] == "G" and ln[6] == " " and ln[76] == "M":
        ids = []
        for b in block(i):
            body = b[9:] if len(b) > 9 else ""
            m = re.match(r"^([A-Za-z]{1,2}(?:,[A-Za-z]{1,2})*)\$(.*)$", body)
            ids.append((m.group(1) if m else "-", (m.group(2) if m else body)[:78]))
        print("line %-5d E=%-10s" % (i + 1, ln[9:19].strip()))
        for k, t in ids:
            print("        %-10s %s" % (k, t))

print()
print("=== 14 targets: exact replacement strings ===")
for t in [308, 382, 384, 386, 527, 529, 531, 533, 567, 569, 572, 617, 619, 622]:
    ln = lines[t - 1]
    content = ln.rstrip()
    cur = "OLD len=%d pad=%d col77=%r" % (len(ln), len(ln) - len(content), ln[76] if len(ln) > 76 else "")
    new = content + " " * (76 - len(content)) + "M" + " " * 3
    print("line %-5d E=%-10s %s" % (t, ln[9:19].strip(), cur))
    print("        NEW len=%d col77=%r" % (len(new), new[76]))
    print("        nxt=%s" % (lines[t][:60] if t < len(lines) else "EOF"))
