import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

def isnum(s):
    return re.match(r"^[\d.]+", s.strip() or "")

# build level blocks with comments and gammas
blocks = []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and isnum(g(l, 10, 19)):
        cur = dict(line=i, E=g(l, 10, 19).strip(), DE=g(l, 20, 21).strip(),
                   J=g(l, 22, 39).strip(), T=g(l, 40, 49).strip(),
                   Lf=g(l, 56, 64).strip(), c77=g(l, 77, 77),
                   ms=g(l, 78, 79).strip(), q=g(l, 80, 80),
                   xref="", comments=[], gammas=[])
        blocks.append(cur)
    elif rt == "L" and c6 == "X":
        if cur: cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif rt == "L" and c6 == "F":
        if cur: cur["flags"] = g(l, 10, 80).strip()
    elif c7 == "c" and rt == "L" and c6 == " ":
        if cur: cur["comments"].append(g(l, 10, 80).rstrip())
    elif c7 == "c" and rt == "L" and c6 != " ":
        if cur: cur["comments"].append("   " + g(l, 10, 80).rstrip())
    elif rt == "G" and c7 == " " and c6 == " " and cur is not None and isnum(g(l, 10, 19)):
        cur["gammas"].append((g(l, 10, 19).strip(), g(l, 22, 29).strip(),
                              g(l, 31, 44).strip(), g(l, 41, 49).strip(),
                              g(l, 80, 80)))

out = []
for b in blocks:
    out.append(f"L{b['line']:>5} E={b['E']:<10} DE={b['DE']:<3} J={b['J']:<16} T={b['T']:<9} L={b['Lf']:<7} c77={b['c77']} ms={b['ms']:<3} q={b['q']} XREF={b['xref']}")
    for c in b["comments"]:
        out.append(f"        | {c}")
    for gm in b["gammas"]:
        out.append(f"        g {gm[0]:<10} RI={gm[1]:<8} M={gm[2]:<12} MR={gm[3]:<8} {gm[4]}")
open(r"d:/X/ND/ENSDF/.github/temp/2026-10-29_Ni58_Jpi_audit/levels.txt", "w", encoding="utf-8").write("\n".join(out))
print(len(blocks), "levels,", len(out), "lines")
