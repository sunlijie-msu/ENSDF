"""Build exact edit inventory for Flag A revision. READ-ONLY.

Outputs:
1. L-records with flag A but no Jpi (candidates for A removal).
2. Pure-L levels (XREF == 'L'): G-records without A (candidates for A add).
3. Mixed levels: G-comment lines mentioning 30}Si (evidence check).
4. Exact reprs of all candidate lines + uniqueness counts.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")

def field(ln, a, b):
    return ln[a - 1:b].rstrip()

levels = []
cur = None
for i, ln in enumerate(lines):
    if len(ln) < 8:
        continue
    if ln[6] == "c":          # comment line
        if cur is not None:
            cur["comments"].append(ln)
        continue
    cont, typ = ln[5], ln[7]
    if typ == "L" and cont == " ":
        cur = {"idx": i + 1, "E": field(ln, 10, 19), "J": field(ln, 23, 39),
               "flag": ln[76], "xref": "", "gs": [], "comments": []}
        levels.append(cur)
    elif typ == "L" and cont == "X" and cur is not None:
        m = re.search(r"XREF=(\S+)", ln)
        if m:
            cur["xref"] = m.group(1)
    elif typ == "G" and cont == " " and cur is not None:
        cur["gs"].append({"idx": i + 1, "E": field(ln, 10, 19),
                          "RI": field(ln, 23, 29), "flag": ln[76], "ln": ln})

print("=== E-flagged L-records (state check) ===")
for r in levels:
    if r["flag"] == "E":
        print(f"line {r['idx']} E={r['E']} J='{r['J']}' XREF={r['xref']}")

print("\n=== 1) L-records flag=A but no Jpi -> remove A ===")
remove_l = [r for r in levels if r["flag"] == "A" and not r["J"].strip()]
for r in remove_l:
    ln = lines[r["idx"] - 1]
    print(f"line {r['idx']:5d} E={r['E']:9s} count={raw.count(ln)}")
    print(f"    repr: {ln!r}")

print("\n=== 2) Pure-L levels: G-records missing A -> add A ===")
pure = [r for r in levels if r["xref"] == "L"]
add_g = []
for r in pure:
    for g in r["gs"]:
        if g["flag"] != "A":
            add_g.append((r, g))
for r, g in add_g:
    print(f"L {r['idx']:5d} E={r['E']:9s} | G line {g['idx']:5d} E={g['E']:9s} "
          f"flag='{g['flag']}' RI={g['RI']:7s} count={raw.count(g['ln'])}")
print("total G-add candidates (pure L):", len(add_g))

print("\n=== 3) Mixed levels: comments mentioning '30}Si' (RI-origin evidence) ===")
for r in levels:
    if "L" not in r["xref"] or r["xref"] == "L":
        continue
    hits = [c for c in r["comments"] if "30}Si" in c]
    if hits:
        print(f"L {r['idx']:5d} E={r['E']:10s} J='{r['J'].strip():10s}' XREF={r['xref'][:40]}")
        for c in hits[:4]:
            print(f"    {c.rstrip()}")
        for g in r["gs"]:
            print(f"    G {g['idx']:5d} E={g['E']:9s} RI={g['RI']:7s} flag='{g['flag']}'")
