"""Build the exact edit plan for converting `2 L WIDTH*` records to cL comments."""
from pathlib import Path
import re

P = Path("A34/S34/new/S34_adopted.ens")
L = P.read_text(encoding="utf-8").splitlines()

L_SRC = "{+30}Si(|a,|g),(|a,n)"
Q_SRC = "{+33}S(n,|g),(n,n)"

# record line -> (comment text, provenance)  ; text uses |G symbols, provenance appended
PLAN = {
    1210: ("|G{-|g}=0.84 eV", L_SRC),
    1222: ("|G{-|g}>1.3 eV", L_SRC),
    1236: ("|G{-|g}>0.7 eV", L_SRC),
    1262: ("|G{-|g}=0.73 eV", L_SRC),
    1288: ("|G{-|g}=3 eV", L_SRC),
    1376: ("|G{-|g}=0.2 eV", L_SRC),
    1393: ("|G{-|g}=2.6 eV", L_SRC),
    1404: ("|G{-|g}=1.7 eV", L_SRC),
    1421: ("|G{-|g}=0.2 eV", L_SRC),
    1432: ("|G{-|g}=2.8 eV", L_SRC),
    1452: ("|G{-|g}=0.08 eV", L_SRC),
    1463: ("|G{-|g}=2.2 eV", L_SRC),
    1477: ("|G{-|g}=1.4 eV", L_SRC),
    1488: ("|G{-|g}=1.5 eV", L_SRC),
    1505: ("|G{-|g}=0.1 eV", L_SRC),
    1522: ("|G{-|g}=1.5 eV", Q_SRC),
    1620: ("|G{-|g}=4.4 eV", L_SRC),
    1786: ("|G{-|g}=2.3 eV", L_SRC),
    1720: ("|G{-|g}=1.0 eV", L_SRC),
    1631: ("|G{-n}=75.0 eV {I8}, |G{-|g}=0.21 eV {I5}, |G{-|a}=41 eV {I5}", Q_SRC),
    1635: ("|G{-n}=39.1 eV {I8}, |G{-|g}=0.90 eV {I5}", Q_SRC),
    1640: ("|G{-n}=16.0 eV {I9}, |G{-|g}=1.44 eV {I10}, |G{-|a}=2.5 eV {I3}", Q_SRC),
    1666: ("|G{-n}=275 eV {I5}, |G{-|g}=1.08 eV {I7}, |G{-|a}=0.17 keV {I5}", Q_SRC),
    1684: ("|G{-n}=507 eV {I13}, |G{-|g}=2.11 eV {I14}", Q_SRC),
    1688: ("|G{-n}=705 eV {I19}, |G{-|g}=0.94 eV {I6}, |G{-|a}=4 eV {I2}", Q_SRC),
    1692: ("|G{-n}=1.33 keV {I8}, |G{-|a}=4.0 keV {I6}", Q_SRC),
    1699: ("|G{-n}=280 eV {I20}, |G{-|g}=2.11 eV {I14}, |G{-|a}=10 eV {I5}", Q_SRC),
    1712: ("|G{-n}=1.260 keV {I25}, |G{-|g}=1.48 eV {I13}", Q_SRC),
    1716: ("|G{-n}=0.36 keV {I4}, |G{-|g}=1.4 eV {I4}, |G{-|a}=0.27 keV {I6}", Q_SRC),
    1747: ("|G{-n}=3.42 keV {I8}, |G{-|g}=2.6 eV {I3}", Q_SRC),
    1751: ("|G{-n}=0.76 keV {I4}, |G{-|g}=0.87 eV {I11}", Q_SRC),
    1755: ("|G{-n}=0.61 keV {I3}, |G{-|g}=1.33 eV {I12}", Q_SRC),
    1762: ("|G{-n}=2.09 keV {I8}, |G{-|g}=2.17 eV {I20}, |G{-|a}=14 eV {I5}", Q_SRC),
    1773: ("|G{-n}=0.69 keV {I7}, |G{-|g}=1.2 eV {I4}, |G{-|a}=55 eV {I20}", Q_SRC),
    1777: ("|G{-n}=4.4 keV {I9}, |G{-|a}=0.9 keV {I3}", Q_SRC),
    1782: ("|G{-n}=0.76 keV {I5}, |G{-|g}=0.81 eV {I13}, |G{-|a}=0.20 keV {I3}", Q_SRC),
    1797: ("|G{-n}=0.46 keV {I3}, |G{-|g}=1.82 eV {I20}", Q_SRC),
    1804: ("|G{-n}=0.67 keV {I6}, |G{-|g}=2.4 eV {I2}", Q_SRC),
    1809: ("|G{-n}=0.23 keV {I7}, |G{-|g}=2.1 eV {I3}", Q_SRC),
}


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


def wrap(text):
    """Return list of line texts (without NUCID/identifier prefix) each fitting in 71 chars."""
    words, out, cur = text.split(" "), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= 71:
            cur = cand
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    return out


out = open(".github/temp/2026-09-16_widthg0/plan.txt", "w", encoding="utf-8")


def W(*a):
    t = " ".join(str(x) for x in a)
    print(t)
    out.write(t + "\n")


for rec, (text, prov) in PLAN.items():
    p = next(j for j in range(rec, 0, -1) if is_lrec(L[j - 1]))
    ls = L[p - 1]
    prev = L[rec - 2]  # line above the record
    # existing cL lines of the level and first G/F line after them
    cls = []
    for j in range(p + 1, len(L) + 1):
        if is_lrec(L[j - 1]):
            break
        s = L[j - 1]
        if s[6:8] == "cL":
            cls.append(j)
    tail = cls[-1] if cls else None
    first = None
    for j in range((tail or p) + 1, len(L) + 1):
        s = L[j - 1]
        if is_lrec(s):
            break
        if s[7:8] in ("G", "F", "S"):
            first = j
            break
    full = "$" + text + " from " + prov + "."
    lines = wrap(full)
    W(f"### rec {rec}  L{p} E={ls[9:19].strip()}  nlines={len(lines)}")
    W(f"    prev({rec-1}) len={len(prev)} clen={len(prev.rstrip())} pad={len(prev)-len(prev.rstrip())} {prev.rstrip()!r}")
    W(f"    rec ({rec}) len={len(L[rec-1])} clen={len(L[rec-1].rstrip())} pad={len(L[rec-1])-len(L[rec-1].rstrip())} {L[rec-1].rstrip()!r}")
    for k, t in enumerate(lines):
        pref = " 34S  cL " if k == 0 else f" 34S {k+1}cL "
        W(f"    NEW[{k}] content({len(pref+t)}) pad({80-len(pref+t)}) {pref + t!r}")
    if tail:
        s = L[tail - 1]
        W(f"    tail cL({tail}) clen={len(s.rstrip())} pad={len(s)-len(s.rstrip())} {s.rstrip()!r}")
    if first:
        s = L[first - 1]
        W(f"    first G/F({first}) clen={len(s.rstrip())} pad={len(s)-len(s.rstrip())} {s.rstrip()!r}")
    W("")

out.close()
