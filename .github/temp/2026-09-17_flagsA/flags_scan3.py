"""Clean scan v3: strict L-record match (cols 6,7 blank; col 8 'L').

Flag A target: XREF == "L" or "L(<annotation>)" only, and col 77 not already 'A'.
Emits pairs3.txt (exact OLD/NEW 80-char lines). Check-only.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
txt = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = txt.split("\n")

recs = []
for i, ln in enumerate(lines):
    if len(ln) >= 8 and ln[5:8] == "  L":  # true L-record
        e = ln[9:19].strip()
        c77 = ln[76:77] if len(ln) > 76 else ""
        short = len(ln) != 80
        xref = ""
        for k in range(i + 1, min(i + 5, len(lines))):
            s = lines[k]
            if "XREF=" in s:
                xref = s.split("XREF=", 1)[1].strip()
                break
            if len(s) >= 8 and (s[5:8] in ("  L", "  G") or s[7:8] in ("G",)):
                break
        clean = re.sub(r"\([^)]*\)", "", xref).strip()
        recs.append(dict(line=i + 1, e=e, ln=ln, c77=c77, short=short, xref=xref,
                         pureL=(clean == "L"), needsA=(clean == "L" and c77 != "A")))

pairs, warn = [], []
for r in recs:
    if r["needsA"] and not r["short"]:
        if txt.count(r["ln"]) != 1:
            warn.append(f"NONUNIQUE line={r['line']} E={r['e']}")
        new = r["ln"][:76] + "A" + r["ln"][77:]
        pairs.append(f"### E={r['e']} line={r['line']}")
        pairs.append("OLD<" + r["ln"] + ">")
        pairs.append("NEW<" + new + ">")
open(r".github/temp/2026-09-17_flagsA/pairs3.txt", "w", encoding="utf-8").write("\n".join(pairs) + "\n")

print("true L-records:", len(recs))
print("len!=80 L-records:", [(r["line"], r["e"], len(r["ln"])) for r in recs if r["short"]])
pure = [r for r in recs if r["pureL"]]
print("pure-L levels:", len(pure), [r["e"] for r in pure])
print("pure-L with A:", [r["e"] for r in pure if r["c77"] == "A"])
need = [r for r in recs if r["needsA"]]
print("NEED A:", len(need), [r["e"] for r in need])
print("short & needA:", [(r["line"], r["e"]) for r in need if r["short"]])
print("warnings:", warn if warn else "none")
