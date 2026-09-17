"""Scan S34_adopted.ens v2: Flag A only for XREF consisting of dataset L alone.

Rule (user-corrected):
  XREF == "L" or "L(<energy annotation>)" and nothing else  ->  flag A at col 77.
  XREF where L is mixed with any other dataset letter (LP, LW, LQ, L(10317)P, ...)
  -> NO flag A.

Outputs pairs2.txt with exact OLD/NEW 80-char line pairs. Check-only.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read()
txt = raw.replace("\r\n", "\n")
lines = txt.split("\n")

recs = []
n = len(lines)
for i, ln in enumerate(lines):
    if len(ln) >= 80 and ln[6:7] == " " and ln[7:8] == "L":
        e = ln[9:19].strip()
        j = ln[22:39].strip()
        c77 = ln[76:77]
        xref = ""
        for k in range(i + 1, min(i + 5, n)):
            s = lines[k]
            if "XREF=" in s:
                xref = s.split("XREF=", 1)[1].strip()
                break
            if s.strip() == "" or (len(s) >= 8 and s[7:8] in ("L", "G")):
                break
        clean = re.sub(r"\([^)]*\)", "", xref).strip()
        pure = (clean == "L")
        old = ln
        new = ln[:76] + "A" + ln[77:80]
        recs.append(dict(line=i + 1, e=e, j=j, c77=c77, xref=xref,
                         pureL=pure, needsA=(pure and c77 != "A"), old=old, new=new))

tbl = [f"{r['line']:5d} E={r['e']:9s} J={r['j']:12s} c77={r['c77']!r} "
       f"pureL={int(r['pureL'])} needsA={int(r['needsA'])} XREF={r['xref']}"
       for r in recs]
open(r".github/temp/2026-09-17_flagsA/flags_table2.txt", "w", encoding="utf-8").write("\n".join(tbl) + "\n")

pairs, warn = [], []
for r in recs:
    if r["needsA"]:
        if txt.count(r["old"]) != 1:
            warn.append(f"NONUNIQUE line={r['line']} E={r['e']}")
        pairs.append(f"### E={r['e']} line={r['line']} XREF={r['xref']}")
        pairs.append("OLD<" + r["old"] + ">")
        pairs.append("NEW<" + r["new"] + ">")
open(r".github/temp/2026-09-17_flagsA/pairs2.txt", "w", encoding="utf-8").write("\n".join(pairs) + "\n")

need = [r for r in recs if r["needsA"]]
pureA = [r for r in recs if r["pureL"] and r["c77"] == "A"]
mixedA = [r for r in recs if (not r["pureL"]) and r["c77"] == "A"]
print("pure-L levels total:", sum(1 for r in recs if r["pureL"]))
print("pure-L already A:", [r["e"] for r in pureA])
print("pure-L NEED A:", len(need), [r["e"] for r in need])
print("mixed-XREF with A (NOT touched):", [(r["e"], r["xref"]) for r in mixedA])
print("warnings:", warn if warn else "none")
