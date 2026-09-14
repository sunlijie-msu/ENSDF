import re

path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")

def blocks(i):
    out = []
    j = i
    while j + 1 < len(lines):
        nx = lines[j + 1]
        if len(nx) > 7 and nx[6] in ("c", "S", "d") and nx[7] == "G":
            out.append(nx)
            j += 1
        else:
            break
    return out

def idents(bl):
    out = []
    for b in bl:
        body = b[9:] if len(b) > 9 else ""
        m = re.match(r"^([A-Za-z]{1,2}(?:,[A-Za-z]{1,2})*)\$(.*)$", body)
        out.append((m.group(1) if m else None, m.group(2) if m else body))
    return out

recs = []
cur = None
for i, ln in enumerate(lines):
    if len(ln) > 7 and ln[7] == "G" and ln[6] == " ":
        cur = i
        recs.append(i)
    elif cur is not None and not (len(ln) > 6 and ln[6] in ("c", "S", "d")):
        cur = None

cats = {"a: RI$other(s)+31P": [], "b: RI$other(s) no31P": [], "c: RI$from 31P": [],
        "d: RI$from other": [], "e: no RI note": []}
for i in recs:
    bl = blocks(i)
    ids = idents(bl)
    ri = [(k, t) for k, t in ids if k and "RI" in k.split(",")]
    flag = lines[i][76] if len(lines[i]) > 76 else " "
    e = lines[i][9:19].strip()
    rec = (i + 1, e, flag, " | ".join("%s$%s" % (k, t[:70]) for k, t in ri))
    if not ri:
        cats["e: no RI note"].append(rec)
    else:
        body = " ".join(t for k, t in ri).replace(" ", "")
        if "31}P(" in body:
            if "RI$other" in "".join(b[9:14] for b in bl) or "other" in " ".join(t for k, t in ri).lower():
                cats["a: RI$other(s)+31P"].append(rec)
            else:
                cats["c: RI$from 31P"].append(rec)
        else:
            if "other" in " ".join(t for k, t in ri).lower():
                cats["b: RI$other(s) no31P"].append(rec)
            else:
                cats["d: RI$from other"].append(rec)

for k in sorted(cats):
    v = cats[k]
    fl = [r for r in v if r[2] != " "]
    print("=== %s : %d records, %d already flagged ===" % (k, len(v), len(fl)))
    if k.startswith("a") or k.startswith("c") or k.startswith("d"):
        for r in v:
            print("   line %-5d E=%-10s flag=%r  %s" % (r[0], r[1], r[2], r[3][:110]))
    else:
        for r in fl:
            print("   line %-5d E=%-10s flag=%r  %s" % (r[0], r[1], r[2], r[3][:110]))
    print()
