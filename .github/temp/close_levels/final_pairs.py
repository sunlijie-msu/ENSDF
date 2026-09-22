"""All level pairs with dE <= 5 keV, compact, with Jpi and XREF."""
import re
from pathlib import Path

TARGET = Path(r"D:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens")
raw = TARGET.read_text(encoding="utf-8").split("\n")

lv = []          # dicts
for i, ln in enumerate(raw):
    if len(ln) > 79 and ln[5] == " " and ln[6] == " " and ln[7] == "L":
        e = ln[9:19].strip()
        de = ln[19:21].strip()
        j = ln[22:39].strip()
        t = ln[39:49].strip()
        lv.append(dict(line=i + 1, e=e, de=de, j=j, t=t, xref="", ng=0))

bymap = {d["line"]: d for d in lv}
cur = None
for i, ln in enumerate(raw):
    if len(ln) < 8:
        continue
    if ln[5] == " " and ln[6] == " " and ln[7] in "LG":
        cur = bymap.get(i + 1)
        if cur is not None and ln[7] == "G":
            cur["ng"] += 1
    elif ln[7] == "L" and "XREF=" in ln:
        if cur is not None:
            cur["xref"] = ln.split("XREF=")[1].strip()


def sigma(d):
    if d["de"] == "":
        return None
    dec = 0
    if "." in d["e"]:
        dec = len(d["e"].split(".")[1])
    return int(d["de"]) * 10.0 ** (-dec)


pairs = []
for a in range(len(lv)):
    for b in range(a + 1, len(lv)):
        try:
            d1, d2 = float(lv[a]["e"]), float(lv[b]["e"])
        except ValueError:
            continue
        de = abs(d2 - d1)
        if de <= 2.0:
            pairs.append((de, lv[a], lv[b]))

pairs.sort(key=lambda p: p[0])
print(f"total levels={len(lv)}  pairs dE<=2 keV: {len(pairs)}")
print(f"{'E1':>10} {'E2':>10} {'dE':>6} {'sig':>7} {'Jpi1':>14} {'Jpi2':>14} {'T1':>10} {'T2':>10}  XREF")
for de, a, b in pairs:
    s1, s2 = sigma(a), sigma(b)
    sig = "-" if (s1 is None or s2 is None) else round((s1 * s1 + s2 * s2) ** 0.5, 3)
    print(f"{a['e']:>10} {b['e']:>10} {de:>6} {str(sig):>7} {a['j'][:14]:>14} "
          f"{b['j'][:14]:>14} {a['t'][:10]:>10} {b['t'][:10]:>10}  {a['xref']} | {b['xref']}")
