"""Scan v4: add Flag A for pure-L XREF, Flag E for pure-T XREF (L/T + optional annotation only)."""
import re

P = r"A34/S34/new/S34_adopted.ens"
txt = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = txt.split("\n")

recs = []
for i, ln in enumerate(lines):
    if len(ln) >= 8 and ln[5:8] == "  L":
        xref = ""
        for k in range(i + 1, min(i + 5, len(lines))):
            s = lines[k]
            if "XREF=" in s:
                xref = s.split("XREF=", 1)[1].strip()
                break
        clean = re.sub(r"\([^)]*\)", "", xref).strip()
        recs.append(dict(line=i + 1, e=ln[9:19].strip(), ln=ln, c77=ln[76:77] if len(ln) > 76 else "",
                         xref=xref, pureL=(clean == "L"), pureT=(clean == "T"), short=len(ln) != 80))

pairsA, pairsE, warn = [], [], []
for r in recs:
    tgt = None
    if r["pureL"] and r["c77"] != "A":
        tgt = ("A", pairsA)
    elif r["pureT"] and r["c77"] != "E":
        tgt = ("E", pairsE)
    if tgt and not r["short"]:
        if txt.count(r["ln"]) != 1:
            warn.append(f"NONUNIQUE line={r['line']} E={r['e']}")
        new = r["ln"][:76] + tgt[0] + r["ln"][77:]
        tgt[1].append(f"### E={r['e']} line={r['line']} flag={tgt[0]}")
        tgt[1].append("OLD<" + r["ln"] + ">")
        tgt[1].append("NEW<" + new + ">")

open(r".github/temp/2026-09-17_flagsA/pairsA_rest.txt", "w", encoding="utf-8").write("\n".join(pairsA) + "\n")
open(r".github/temp/2026-09-17_flagsA/pairsE.txt", "w", encoding="utf-8").write("\n".join(pairsE) + "\n")

print("remaining pure-L to flag A:", len(pairsA) // 3, [r["e"] for r in recs if r["pureL"] and r["c77"] != "A"])
print("pure-T levels:", [(r["e"], r["xref"], r["c77"]) for r in recs if r["pureT"]])
print("pure-T to flag E:", len(pairsE) // 3)
print("warnings:", warn if warn else "none")
