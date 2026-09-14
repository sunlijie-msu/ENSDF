import re, sys

path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")

# gather G-records with their following comment block
recs = []
cur = None
for i, ln in enumerate(lines, 1):
    if len(ln) > 7 and ln[7] == "G" and (len(ln) < 7 or ln[6] == " "):
        cur = {"line": i, "text": ln, "block": []}
        recs.append(cur)
    elif cur is not None:
        if len(ln) > 6 and ln[6] in "cSd" and " c" in ln[:7] + " " or (len(ln) > 6 and ln[6].isalpha() and ln[6].islower()):
            pass
        if ln[6:7] == "c":
            cur["block"].append(ln)
        elif ln.strip() == "":
            pass
        else:
            # non-comment content line ends the block unless continuation comment
            if not (len(ln) > 6 and ln[6] in "c" and ln[7:8] in "G "):
                cur = None

def idents(block):
    out = []
    for b in block:
        body = b[9:] if len(b) > 9 else ""
        m = re.match(r"^([A-Za-z]{1,2}(?:,[A-Za-z]{1,2})*)\$(.*)$", body)
        if m:
            out.append((m.group(1), m.group(2)))
    return out

strict = []
default = []
for r in recs:
    e = r["text"][9:19].strip()
    ids = idents(r["block"])
    allbody = " ".join(x[1] for x in ids)
    ri_note = [b for k, b in ids if "RI" in k.split(",")]
    p31 = "31}P(" in " ".join(ri_note).replace(" ", "")
    rib = " ".join(ri_note)
    mixed = ("average" in rib.lower()) or ("Others:" in rib) or ("Other:" in rib) or ("|e+|b" in rib) or ("|b{+-}" in rib)
    if ri_note and p31 and not mixed:
        strict.append((e, r["line"]))
    elif not ri_note:
        default.append((e, r["line"]))

print("STRICT (RI note explicitly 31P(alpha,pgamma), single source):", len(strict))
for e, l in strict:
    print("   line %-5d E=%-10s" % (l, e))
print()
print("NO RI note at all (in general 31P default, unless otherwise noted):", len(default))
print()
print("TOTAL G-records:", len(recs))
