"""Independent check: can the 348 UNPLACED G-records of the target .ens be the
multiplet partner of any of the 53 asterisked Table II rows?

Parses Table II (E_i | E_g | I_g | E_f | Jpi_f) and the .ens directly.
No imports from the report generator.
"""
import io
import re

SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"

num = re.compile(r"-?\d+(?:\.\d+)?")


def f(t):
    m = num.search(t or "")
    return float(m.group(0)) if m else None


tab = []
for i, line in enumerate(io.open(SRC, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or "E_i" in line or line.startswith("| :"):
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    tab.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3],
                    E=f(c[1]), ast="*" in c[2] or "\u2217" in c[2]))
lines = io.open(ENS, encoding="ascii", errors="ignore").read().split("\n")
lines = [l.rstrip("\r") for l in lines]
Lrec = [i for i, l in enumerate(lines, 1)
        if len(l.ljust(80)) > 7 and l.ljust(80)[5] == " " and l.ljust(80)[6] == " "
        and l.ljust(80)[7] == "L"]
firstL = Lrec[0]
unp = []
for i, raw in enumerate(lines, 1):
    if i >= firstL:
        break
    l = raw.ljust(80)
    if l[5] == " " and l[6] == " " and l[7] == "G":
        unp.append(dict(ln=i, E=f(l[9:19]), c76=l[76], c80=l[79], raw=raw))
plc = []
for i, raw in enumerate(lines, 1):
    if i <= firstL:
        continue
    l = raw.ljust(80)
    if l[5] == " " and l[6] == " " and l[7] == "G":
        plc.append(dict(ln=i, E=f(l[9:19]), c76=l[76], c80=l[79]))
ast = [r for r in tab if r["ast"]]

print("Table II rows           :", len(tab))
print("asterisked rows         :", len(ast))
print("first L-record line     :", firstL)
print("unplaced G-records      :", len(unp), "lines", unp[0]["ln"], "-", unp[-1]["ln"])
print("placed  G-records       :", len(plc), "lines", plc[0]["ln"], "-", plc[-1]["ln"])
print("placed col77 flags      :", {})
tal = {}
for p in plc:
    if p["c76"] != " ":
        tal[p["c76"]] = tal.get(p["c76"], 0) + 1
print("  ", tal)
talu = {}
for p in unp:
    talu[p["c76"]] = talu.get(p["c76"], 0) + 1
print("unplaced col77 char tally:", talu)

print("\n--- nearest unplaced gamma to each asterisked row ---")
worst = (0, None, None)
buckets = {0.1: 0, 0.5: 0, 1.0: 0, 2.0: 0, 5.0: 0}
for r in ast:
    ds = sorted(((abs(u["E"] - r["E"]), u["ln"], u) for u in unp), key=lambda t: (t[0], t[1]))
    d, _, u = ds[0]
    for k in buckets:
        if d <= k:
            buckets[k] += 1
    if d > worst[0]:
        worst = (d, r, u)
print("counts of asterisked rows with an unplaced gamma within:")
for k in sorted(buckets):
    print("   <= {:.1f} keV : {}".format(k, buckets[k]))
print("closest overall: {:.3f} keV  ({}  vs unplaced {})".format(
    worst[0], worst[1]["eg"], worst[2]["raw"][9:19].strip()))
for r in ast:
    ds = sorted(((abs(u["E"] - r["E"]), u["ln"], u) for u in unp), key=lambda t: (t[0], t[1]))
    print("   {:>10}  nearest {}".format(r["eg"], " ".join(
        "{:.2f}({})".format(d, u["ln"]) for d, _, u in ds[:3])))

print("\n--- exact / near energy coincidences ---")
ex = [(r["eg"], u["ln"], u["raw"][9:19].strip())
      for r in ast for u in unp if abs(u["E"] - r["E"]) < 0.005]
print("asterisked vs unplaced, |dE| < 0.005 keV :", len(ex), ex)
ex2 = [(r["eg"], u["ln"]) for r in tab for u in unp if abs(u["E"] - r["E"]) < 0.005]
print("all Table II vs unplaced, |dE| < 0.005   :", len(ex2))

print("\n--- internal structure of the unplaced set ---")
dup = [(a["ln"], a["E"], b["ln"], b["E"]) for i, a in enumerate(unp) for b in unp[i + 1:]
       if abs(a["E"] - b["E"]) < 0.05]
print("unplaced pairs within 0.05 keV of each other:", len(dup), dup[:10])
d15 = [(a["ln"], a["E"], b["ln"], b["E"]) for i, a in enumerate(unp) for b in unp[i + 1:]
       if 0.05 <= abs(a["E"] - b["E"]) <= 1.0]
print("unplaced pairs 0.05-1.0 keV apart          :", len(d15), d15[:10])

print("\n--- unplaced col80 markers ---")
x80 = [u for u in unp if u["c80"] != " "]
print("unplaced records with non-blank col80:", len(x80), {u["c80"] for u in x80})
