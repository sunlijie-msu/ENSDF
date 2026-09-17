"""Scan S34_adopted.ens: levels whose XREF contains dataset L, and emit exact edit pairs.

Outputs:
  flags_table.txt  - every L-record: line, E, J, col77 char, cols78-80, XREF, hasL, needsA
  pairs.txt        - OLD/NEW 80-char line pairs for every level needing 'A' at col 77
Check-only: never writes the .ens file.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read()
txt = raw.replace("\r\n", "\n")
lines = txt.split("\n")

recs = []
n = len(lines)
for i, ln in enumerate(lines):
    if len(ln) >= 80 and ln[7:8] == "L" and ln[6:7] == " ":
        e = ln[9:19].strip()
        j = ln[22:39].strip()
        c77 = ln[76:77]
        tail = ln[77:80]
        xref = ""
        for k in range(i + 1, min(i + 5, n)):
            s = lines[k]
            if "XREF=" in s:
                xref = s.split("XREF=", 1)[1].strip()
                # continuation XREF lines (col6 alnum, col8 L, XREF text continues)
                m = k + 1
                while m < n and len(lines[m]) >= 9 and lines[m][6:7] not in (" ", ""):
                    nxt = lines[m]
                    if nxt[8:9] in ("L", " ") and "XREF" not in nxt and len(nxt) < 12:
                        break
                    # only extend when the following line starts with XREF continuation text
                    if "XREF=" in nxt:
                        xref += " " + nxt.split("XREF=", 1)[1].strip()
                        m += 1
                        continue
                    break
                break
            if s.strip() == "":
                break
            # stop scan if a new L record or comment/G encountered before XREF
            if len(s) >= 8 and s[7:8] in ("L", "G"):
                break
        clean = re.sub(r"\([^)]*\)", "", xref)
        hasL = "L" in clean
        old = ln
        new = ln[:76] + "A" + ln[77:80]
        recs.append(dict(line=i + 1, e=e, j=j, c77=c77, tail=tail, xref=xref,
                         hasL=hasL, needsA=(hasL and c77 != "A"), old=old, new=new))

tbl = []
for r in recs:
    tbl.append(f"{r['line']:5d} E={r['e']:9s} J={r['j']:12s} c77={r['c77']!r} "
               f"t789={r['tail']!r} hasL={int(r['hasL'])} needsA={int(r['needsA'])} "
               f"XREF={r['xref']}")
open(r".github/temp/2026-09-17_flagsA/flags_table.txt", "w", encoding="utf-8").write("\n".join(tbl) + "\n")

pairs = []
warn = []
for r in recs:
    if r["needsA"]:
        cnt = txt.count(r["old"])
        if cnt != 1:
            warn.append(f"NONUNIQUE OLD count={cnt} line={r['line']} E={r['e']}")
        pairs.append(f"### E={r['e']} line={r['line']} XREF={r['xref']}")
        pairs.append("OLD<" + r["old"] + ">")
        pairs.append("NEW<" + r["new"] + ">")
open(r".github/temp/2026-09-17_flagsA/pairs.txt", "w", encoding="utf-8").write("\n".join(pairs) + "\n")

need = [r for r in recs if r["needsA"]]
hasA_L = [r for r in recs if r["hasL"] and r["c77"] == "A"]
A_noL = [r for r in recs if (not r["hasL"]) and r["c77"] == "A"]
otherflag = [r for r in recs if r["needsA"] and r["c77"].strip() not in ("", "A")]
print("level records:", len(recs))
print("XREF contains L:", sum(1 for r in recs if r["hasL"]))
print("need flag A:", len(need))
print("already A with L:", len(hasA_L), [r["e"] for r in hasA_L])
print("A without L (untouched):", len(A_noL), [(r["e"], r["tail"] or "col78-80:" + repr(r["tail"])) for r in A_noL])
print("needsA with other c77 letter:", [(r["e"], r["c77"]) for r in otherflag])
print("warnings:", warn if warn else "none")
print("need E list:", [r["e"] for r in need])
