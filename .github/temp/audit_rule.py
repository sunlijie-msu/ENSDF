import re
p = r"A34\S34\new\S34_adopted.ens"
L = open(p, newline="").read().split("\r\n")
LIMIT = 8025.0
levels = []   # (line_idx, E, DE, Jstr, comment_lines[], gamma_lines[])
cur = None
for i, s in enumerate(L):
    if len(s) >= 8 and s[5] == " " and s[6] == " " and s[7] == "L":
        e = s[9:19].strip()
        de = s[19:21].strip()
        try:
            ev = float(e)
        except ValueError:
            ev = None
        cur = {"line": i + 1, "E": e, "DE": de, "Ev": ev, "comments": [], "gammas": []}
        levels.append(cur)
    elif len(s) >= 8 and s[7] == "G" and cur is not None:
        ge = s[9:19].strip()
        gde = s[19:21].strip()
        cur["gammas"].append((ge, gde, i + 1))
    elif len(s) >= 7 and s[6] == "c" and s[7] == "L" and cur is not None:
        cur["comments"].append((i + 1, s[9:].rstrip()))

def has_eg_de(g):
    return g[0] != "" and g[1] != ""

print("LEVELS BELOW 8025 -- rule audit")
for lv in levels:
    if lv["Ev"] is None or lv["Ev"] >= LIMIT:
        continue
    n_with = sum(1 for g in lv["gammas"] if has_eg_de(g))
    ecom = [c for c in lv["comments"] if any(k.strip() == "E" for k in c[1].split("$")[0].split(","))]
    tag = ""
    if n_with > 0 and ecom:
        tag = "RULE1-REDUNDANT?"
    if n_with == 0 and not ecom and lv["Ev"] != 0.0:
        tag = "RULE2-MISSING"
    if tag:
        print(f"{tag}  line={lv['line']} E={lv['E']} DE={lv['DE']} gammas={lv['gammas']}")
        for c in lv["comments"]:
            print("      c", c)
