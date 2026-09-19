"""Audit averages v3: compact verdict table (record field vs recomputed mean).

Handles ENSDF last-digit uncertainties, tau->T1/2 (ln 2) for cL T$ lifetime blocks,
and unit conversion of T fields (FS/PS/NS/S incl. mantissa scientific notation).
"""
import math
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
LN2 = math.log(2.0)

lines = open(PATH, encoding="utf-8", errors="replace").read().split("\n")
if lines and lines[-1] == "":
    lines.pop()


def is_data(l):
    return len(l) > 8 and l[5] == " " and l[6] == " " and l[7] in "LG" and l[8] == " "


blocks = []
i = 0
while i < len(lines):
    if len(lines[i]) > 7 and lines[i][5] == " " and lines[i][6] == "c":
        j = i + 1
        while j < len(lines) and len(lines[j]) > 7 and lines[j][5] != " " and lines[j][6] == "c":
            j += 1
        blocks.append((i + 1, j, " ".join(lines[k][8:].strip() for k in range(i, j))))
        i = j
    else:
        i += 1

ITEM = re.compile(r"(\d+(?:\.\d+)?)\s*(fs|ns|ps|s|eV|keV|MeV)?\s*\{I([+-]?\d+)(?:-(\d+))?\}")
TUNIT = {"fs": 1.0, "ps": 1e3, "ns": 1e6, "s": 1e15}


def dec(s):
    return len(s.split(".")[1]) if "." in s else 0


def sig_lastdigits(vstr, up, dn):
    s = 10.0 ** (-dec(vstr))
    if dn is None:
        return abs(float(up)) * s
    return (abs(float(up)) + abs(float(dn))) / 2.0 * s


def parse_Tfield(tstr, dtstr):
    """-> (value_in_fs, sigma_in_fs) or (None, None)."""
    if not tstr:
        return None, None
    m = re.match(r"^([\d.]+(?:E[+-]?\d+)?)\s*([A-Za-z]+)?$", tstr)
    if not m:
        return None, None
    num, unit = m.group(1), (m.group(2) or "").lower()
    if unit not in TUNIT:
        return None, None
    val = float(num) * TUNIT[unit]
    mant = num.split("E")[0]
    sig = float(dtstr) * 10.0 ** (-dec(mant)) * TUNIT[unit] if dtstr and dtstr[0].isdigit() else None
    return val, sig


def fmt(x, nd=3):
    if x is None:
        return "-"
    return ("%%.%df" % nd) % x


rows = []
for start, end, text in blocks:
    if not re.search(r"averag", text, re.I):
        continue
    oidx = None
    for k in range(start - 2, -1, -1):
        if is_data(lines[k]):
            oidx = k
            break
    if oidx is None:
        continue
    orec = lines[oidx]
    kind = orec[7]
    ident = text.split("$")[0].strip()
    m = re.search(r"(un)?(weighted )?average of", text, re.I)
    if not m:
        continue
    weighted = not (m.group(1) and m.group(1).lower() == "un")
    tail = text[m.end():]
    items, pos = [], 0
    for mm in ITEM.finditer(tail):
        gap = tail[pos:mm.start()]
        if items and re.search(r"\.\s|;\s", gap):
            break
        items.append((float(mm.group(1)), sig_lastdigits(mm.group(1), mm.group(3), mm.group(4))))
        pos = mm.end()
    if len(items) < 1:
        continue
    vals = [v for v, _ in items]
    sigs = [s for _, s in items]
    if any(s <= 0 for s in sigs):
        continue
    if weighted and len(items) > 1:
        w = [1.0 / s ** 2 for s in sigs]
        sw = sum(w)
        mean = sum(wi * v for wi, v in zip(w, vals)) / sw
        sig = math.sqrt(1.0 / sw)
        chi2 = sum(((v - mean) / s) ** 2 for v, s in zip(vals, sigs))
        dof = len(vals) - 1
        sf = math.sqrt(chi2 / dof) if chi2 > dof else 1.0
    else:
        mean = sum(vals) / len(vals)
        sig = math.sqrt(sum(s ** 2 for s in sigs)) / len(vals)
        chi2, dof, sf = float("nan"), len(vals) - 1, 1.0
    sigs_scaled = sig * sf

    recE, recDE = orec[9:19].strip(), orec[19:21].strip()
    recT, recDT = orec[39:49].strip(), orec[49:55].strip()
    recRI, recDRI = orec[22:29].strip(), orec[29:31].strip()

    if kind == "G" and ident in ("E", "RI"):
        field, fdigits, func = (recE, recDE, 1.0) if ident == "E" else (recRI, recDRI, 1.0)
        if not field:
            continue
        rv = float(field)
        rsig = float(fdigits) * 10.0 ** (-dec(field)) if fdigits and fdigits[0].isdigit() else None
        delta = mean - rv
        verdict = ""
        if rsig:
            n = abs(delta) / math.hypot(rsig, sigs_scaled)
            verdict = "OK" if n < 1.5 else ("MINOR" if n < 3 else "MISMATCH")
        rows.append((start, end, oidx + 1, kind + ident, field + "(" + (fdigits or "-") + ")",
                     mean, sigs_scaled, delta, verdict, len(items), sf))
    elif kind == "L" and ident == "E":
        rv = float(recE)
        rsig = float(recDE) * 10.0 ** (-dec(recE)) if recDE and recDE[0].isdigit() else None
        delta = mean - rv
        verdict = ""
        if rsig:
            n = abs(delta) / math.hypot(rsig, sigs_scaled)
            verdict = "OK" if n < 1.5 else ("MINOR" if n < 3 else "MISMATCH")
        rows.append((start, end, oidx + 1, kind + ident, recE + "(" + (recDE or "-") + ")",
                     mean, sigs_scaled, delta, verdict, len(items), sf))
    elif kind == "L" and ident in ("T", "Tr"):
        mt = re.search(r"\|t\s*=\s*(\d+(?:\.\d+)?)\s*(fs|ns|ps)?\s*\{I([+-]?\d+)(?:-(\d+))?\}", text)
        if not mt:
            continue
        tval = float(mt.group(1)) * TUNIT[(mt.group(2) or "fs").lower()]
        tsig = sig_lastdigits(mt.group(1), mt.group(3), mt.group(4)) * TUNIT[(mt.group(2) or "fs").lower()]
        rv, rsig = parse_Tfield(recT, recDT)
        half, halfsig = tval * LN2, tsig * LN2
        verdict = "OK"
        if rv:
            n = abs(half - rv) / math.hypot(rsig or 0, halfsig)
            verdict = "OK" if n < 1.5 else ("MINOR" if n < 3 else "MISMATCH")
        rows.append((start, end, oidx + 1, kind + ident, recT + " " + recDT,
                     half, halfsig, (half - rv) if rv else None, verdict, len(items), sf))
    else:
        rows.append((start, end, oidx + 1, kind + ident, "-", mean, sigs_scaled, None, "NO-FIELD", len(items), sf))

hdr = "%-9s %-6s %-5s %-18s %-14s %-14s %-11s %-9s %-3s %-5s" % (
    "cmt", "owner", "id", "record", "mean", "sig(scaled)", "delta", "verdict", "n", "SF")
print(hdr)
print("-" * len(hdr))
for r in rows:
    print("%-9s %-6d %-5s %-18s %-14s %-14s %-11s %-9s %-3d %-5.2f" % (
        "%d-%d" % (r[0], r[1]), r[2], r[3], r[4], fmt(r[5], 5), fmt(r[6], 5),
        fmt(r[7], 5), r[8], r[9], r[10]))
print()
print("total average blocks audited:", len(rows))
from collections import Counter
print(Counter(r[8] for r in rows))
