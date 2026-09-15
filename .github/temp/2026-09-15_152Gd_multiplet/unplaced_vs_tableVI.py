"""Cross-check the target's 348 UNPLACED G-records against the authors' source
table 2026OSAA_CT11035_152Gd_Table_VI_3rd.md (unidentifed/unplaced peaks), and
re-test whether any unplaced gamma can be the multiplet partner of an
asterisked Table II row (E_gamma equality, independent of the report generator).
"""
import io
import re

VI = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"
T2 = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"

sd = re.compile(r"^([-\d.]+)\s*\(\s*(\d+)\s*\)$")
x = re.compile(r"-?\d+(?:\.\d+)?")
fail = []


def parse(t):
    t = (t or "").strip()
    m = sd.match(t)
    if m:
        return m.group(1), m.group(2)
    return (t, "") if t else (None, None)


# ---- source: Table VI ------------------------------------------------------
vi = []
for i, line in enumerate(io.open(VI, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_gamma" in line:
        continue
    c = [y.strip() for y in line.strip("|").split("|")]
    if len(c) < 2 or not c[0]:
        continue
    e, de = parse(c[0])
    ri, dri = parse(c[1])
    vi.append(dict(ln=i, e=e, de=de, ri=ri, dri=dri,
                   coin="*" in (c[2] if len(c) > 2 else ""), E=float(x.search(c[0]).group(0))))
print("Table VI_3rd data rows :", len(vi))
print("  coincidence '*' rows :", sum(1 for r in vi if r["coin"]))
print("  rows with I_gamma    :", sum(1 for r in vi if r["ri"]))
print("  ascending energy     :", all(vi[i]["E"] < vi[i + 1]["E"] for i in range(len(vi) - 1)))

# ---- target: unplaced G-records -------------------------------------------
lines = [l.rstrip("\r") for l in io.open(ENS, encoding="ascii", errors="ignore")]
lines = [l.ljust(80) for l in lines]
firstL = next(i for i, l in enumerate(lines, 1) if l[6] == " " and l[7] == "L")
unp = []
for i, l in enumerate(lines[:firstL - 1], 1):
    if l[5] == " " and l[6] == " " and l[7] == "G":
        unp.append(dict(ln=i, e=l[9:19].strip(), de=l[19:21].strip(),
                        ri=l[22:29].strip(), dri=l[29:31].strip(), flag=l[76]))
print("target unplaced G recs :", len(unp), "lines {} - {}".format(unp[0]["ln"], unp[-1]["ln"]))
print("  col 77 non-blank     :", sum(1 for r in unp if r["flag"] != " "),
      sorted({r["flag"] for r in unp}))

# ---- 1:1 comparison -------------------------------------------------------
print("\n--- Table VI_3rd vs target unplaced G-records ---")
for k, (a, b) in enumerate(zip(vi, unp)):
    chk = [("E", a["e"], b["e"]), ("DE", a["de"] or "", b["de"]),
           ("RI", a["ri"] or "", b["ri"]), ("DRI", a["dri"] or "", b["dri"])]
    for name, s, t in chk:
        if s != t:
            fail.append(("VI", a["ln"], k + 1, name, s, t))
    want = "X" if a["coin"] else " "
    if b["flag"] != want:
        fail.append(("VI-flag", a["ln"], b["ln"], "col77", want, b["flag"]))
print("row-count match        :", len(vi) == len(unp), "(VI {} vs ens {})".format(len(vi), len(unp)))
print("mismatches             :", len(fail))
for f in fail[:40]:
    print("   ", f)
flagmap = sum(1 for a, b in zip(vi, unp) if b["flag"] == ("X" if a["coin"] else " "))
print("coincidence->col77 X rows matched 1:1 :", flagmap, "/", len(vi))

# ---- partner test: unplaced as partner of asterisked Table II rows --------
t2 = []
for i, line in enumerate(io.open(T2, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [y.strip() for y in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    t2.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3],
                   E=float(x.search(c[1]).group(0)), ast="*" in c[2]))
ast = [r for r in t2 if r["ast"]]
print("\n--- unplaced gamma as partner of an asterisked Table II row ---")
print("asterisked rows        :", len(ast))
buckets = {"0.005": 0, "0.1": 0, "0.5": 0, "1.0": 0, "2.0": 0}
best = []
for r in ast:
    d, q = min(((abs(u["E"] - r["E"]), u) for u in vi), key=lambda t: t[0])
    best.append((d, r, q))
    for k in buckets:
        if d <= float(k):
            buckets[k] += 1
for k in ["0.005", "0.1", "0.5", "1.0", "2.0"]:
    print("  asterisked rows with unplaced partner within {:>5} keV : {}".format(k, buckets[k]))
best.sort(key=lambda t: -t[0])
print("  closest overall      : {:.3f} keV  ({} vs unplaced {})".format(
    best[0][0], best[0][1]["eg"], best[0][2]["e"]))
print("  nearest-distance range: {:.2f} - {:.2f} keV".format(
    min(d for d, _, _ in best), max(d for d, _, _ in best)))

print("\n--- unplaced internal duplicates (same E_gamma twice) ---")
dup = [(a["e"], b["e"]) for i, a in enumerate(vi) for b in vi[i + 1:]
       if abs(a["E"] - b["E"]) < 0.005]
print("  unplaced pairs with identical E_gamma:", len(dup), dup)

print("\nFAILS:", len(fail))
