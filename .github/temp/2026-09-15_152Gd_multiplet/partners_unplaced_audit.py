"""Do the 348 unplaced G-records of the target provide additional multiplet partners?

Partners are searched among the 751 Table II rows AND the 348 unplaced G-records
of 2026OSAA_CT11035_152Gd.ens (lines before the first L-record).
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TBL = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd_Table_II.md")
ENS = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd.ens")
TOL = 1.0
NUM = re.compile(r"^[0-9]")


def num(s):
    s = s.strip()
    m = re.match(r"^([-+]?[0-9]*\.?[0-9]+)", s) if s else None
    return float(m.group(1)) if m else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


rows = []
with io.open(TBL, encoding="utf-8") as fh:
    for ln, raw in enumerate(fh, 1):
        line = raw.rstrip("\r\n")
        if not line.startswith("|"):
            continue
        c = cells(line)
        if len(c) < 5 or not NUM.match(c[1].strip()):
            continue
        rows.append(dict(ln=ln, eg=c[1], ig=c[2], ei=c[0], ef=c[3], E=num(c[1])))
astro = [r for r in rows if "*" in r["ig"]]
print("Table II rows: {} | asterisked: {}".format(len(rows), len(astro)))

L = [l.rstrip("\r\n") for l in io.open(ENS, encoding="ascii", errors="ignore")]
firstL = next(i for i, l in enumerate(L)
              if len(l) > 7 and l[6] == " " and l[7] == "L")
unp = []
for i, l in enumerate(L[:firstL]):
    if len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "G":
        e = num(l[9:19])
        if e is None:
            continue
        unp.append(dict(ln=i + 1, eg=l[9:19].strip(), de=l[19:21].strip(),
                        ig=l[22:29].strip(), E=e))
print("unplaced G-records: {}".format(len(unp)))

hits = {}
for r in astro:
    pu = [q for q in unp if abs(q["E"] - r["E"]) <= TOL]
    pu.sort(key=lambda q: (abs(q["E"] - r["E"]), q["ln"]))
    if pu:
        hits[r["ln"]] = pu
print("\nasterisked rows with \u22651 unplaced partner within \u00b1{:.1f} keV: {}".format(
    TOL, len(hits)))
for r in astro:
    if r["ln"] not in hits:
        continue
    print("Table II row {}  Eg={}  I={}  Ei={}".format(r["ln"], r["eg"], r["ig"], r["ei"]))
    for q in hits[r["ln"]]:
        print("    unplaced ens line {}  Eg={}  DE={}  RI={}  dE={:+.2f}".format(
            q["ln"], q["eg"], q["de"] or "-", q["ig"] or "-", q["E"] - r["E"]))

print("\n--- unplaced energies identical to a Table II row energy ---")
tblE = {(round(r["E"], 3)): r for r in rows}
same = [q for q in unp if round(q["E"], 3) in tblE]
print("count: {}".format(len(same)))
for q in same[:20]:
    print("  unplaced line {} Eg={}  == Table II E={}".format(q["ln"], q["eg"], tblE[round(q["E"], 3)]["E"]))

print("\n--- closest unplaced gamma to any asterisked row ---")
best = sorted(((abs(q["E"] - r["E"]), r["ln"], r["eg"], q["ln"], q["eg"])
               for r in astro for q in unp), key=lambda z: z[0])[:8]
for d, rln, reg, qln, qeg in best:
    print("  {:6.2f} keV | Table II row {} Eg={}  <->  unplaced line {} Eg={}".format(
        d, rln, reg, qln, qeg))
