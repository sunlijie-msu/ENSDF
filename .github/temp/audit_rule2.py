p = r"A34\S34\new\S34_adopted.ens"
L = open(p, newline="").read().split("\r\n")
LIMIT = 8025.0
levels = []
cur = None
for i, s in enumerate(L):
    if len(s) >= 8 and s[5] == " " and s[6] == " " and s[7] == "L":
        try:
            ev = float(s[9:19].strip())
        except ValueError:
            ev = None
        cur = {"line": i + 1, "E": s[9:19].strip(), "DE": s[19:21].strip(), "Ev": ev, "comments": [], "gammas": []}
        levels.append(cur)
    elif len(s) >= 8 and s[5] == " " and s[6] == " " and s[7] == "G" and cur is not None:
        cur["gammas"].append((s[9:19].strip(), s[19:21].strip(), i + 1))
    elif len(s) >= 8 and s[6] == "c" and s[7] == "L" and cur is not None:
        cur["comments"].append((i + 1, s[9:].rstrip()))

bad1, bad2 = [], []
for lv in levels:
    if lv["Ev"] is None or lv["Ev"] >= LIMIT:
        continue
    n_with = sum(1 for g in lv["gammas"] if g[0] != "" and g[1] != "")
    ecom = [c for c in lv["comments"] if "E" in [k.strip() for k in c[1].split("$")[0].split(",")]]
    if n_with > 0 and ecom:
        bad1.append((lv, n_with, ecom))
    if n_with == 0 and not ecom and lv["Ev"] != 0.0:
        bad2.append((lv, n_with, ecom))
print("=== RULE1: cL E$ present but level has G with E+DE (unnecessary) ===")
for lv, n, e in bad1:
    print(f"line={lv['line']} E={lv['E']} DE={lv['DE']} ngam={len(lv['gammas'])} n_with_E+DE={n}")
    for c in e:
        print("     c", c[0], c[1])
print("=== RULE2: no G with E+DE and no cL E$ ===")
for lv, n, e in bad2:
    print(f"line={lv['line']} E={lv['E']} DE={lv['DE']} ngam={len(lv['gammas'])}")
    for c in lv["comments"]:
        print("     c", c[0], c[1])
