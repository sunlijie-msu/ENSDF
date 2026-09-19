"""Audit averages v5: parse every 'average' comment block, recompute the mean,
compare with the owning record field under several ENSDF uncertainty conventions.

Outputs one row per block: record value(unc), recomputed mean(sigma_internal),
chi2/dof, and which conventions reproduce the record uncertainty.
"""
import math
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

PATH = sys.argv[1] if len(sys.argv) > 1 else r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
LN2 = math.log(2.0)
TUNIT = {"fs": 1.0, "ps": 1e3, "ns": 1e6, "s": 1e15}
lines = open(PATH, encoding="utf-8", errors="replace").read().split("\n")
if lines and lines[-1] == "":
    lines.pop()


def is_data(l):
    return len(l) > 8 and l[5] == " " and l[6] == " " and l[7] in "LG" and l[8] == " "


def dec(s):
    s = s.split("E")[0]
    return len(s.split(".")[1]) if "." in s else 0


def round_half_up(x, nd):
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def ceil_int(x):
    return math.ceil(x - 1e-9)


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

ITEM = re.compile(r"([\d.]+)\s*(fs|ps|ns|s|eV|keV|MeV)?\s*\{I([+-]?\d+)(?:-(\d+))?\}")
rows = []
for start, end, text in blocks:
    m = re.search(r"(un)?(weighted\s+)?average\s+(?:value\s+)?of", text, re.I)
    if not m:
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
    weighted = not (m.group(1) or "").lower().startswith("un") and bool(m.group(2) or True)
    weighted = weighted and not re.search(r"unweighted", text, re.I)
    tail = text[m.end():]
    items, pos = [], 0
    for mm in ITEM.finditer(tail):
        gap = tail[pos:mm.start()]
        if items and (re.search(r"\.\s", gap) or "Other:" in tail):
            break
        v = float(mm.group(1))
        unit = (mm.group(2) or "").lower()
        s = abs(float(mm.group(3))) * 10.0 ** (-dec(mm.group(1)))
        if mm.group(4):
            s = (abs(float(mm.group(3))) + abs(float(mm.group(4)))) / 2.0 * 10.0 ** (-dec(mm.group(1)))
        if unit:
            s *= TUNIT[unit]
        items.append((v * (TUNIT[unit] if unit else 1.0), s, mm.group(0)))
        pos = mm.end()
    if len(items) < 2:
        rows.append((start, end, oidx + 1, kind + ident, "PARSE-FAIL", text[:60]))
        continue
    vals = [v for v, _, _ in items]
    sigs = [s for _, s, _ in items]
    if weighted:
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
    sig_ext = sig * sf
    rows.append((start, end, oidx + 1, kind + ident, (mean, sig, sig_ext, min(sigs), chi2, dof, sf, vals, sigs), text))

print("%-9s %-5s %-4s %-22s %-26s %-9s %s" % ("cmt", "owner", "id", "record", "recomputed mean(sig)", "chi2/dof", "verdict"))
print("-" * 130)
for start, end, owner, ident, info, text in rows:
    if info == "PARSE-FAIL":
        print("%-9s %-5d %-4s %-22s %-26s %-9s %s" % ("%d-%d" % (start, end), owner, ident, "-", "PARSE FAIL", "-", text.replace("\n", " ")))
        continue
    mean, sig, sig_ext, smin, chi2, dof, sf, vals, sigs = info
    orec = lines[owner - 1]
    kind, idt = ident[0], ident[1:]
    if idt == "E" and kind in "GL":
        rv, ru = orec[9:19].strip(), orec[19:21].strip()
        nd = dec(rv)
        unit_step = 1.0
    elif idt == "RI" and kind == "G":
        rv, ru = orec[22:29].strip(), orec[29:31].strip()
        nd = dec(rv)
        unit_step = 1.0
    elif idt == "T" and kind == "L":
        mt = re.search(r"\|t\s*=\s*(\d+(?:\.\d+)?)\s*(fs|ps|ns|s)?", text)
        t = orec[39:49].strip()
        if not mt or not t:
            print("%-9s %-5d %-4s %-22s %-26s %-9s %s" % ("%d-%d" % (start, end), owner, ident, repr(t), "tau=%.4g" % (mean if mt else float('nan')), "-", "MANUAL"))
            continue
        f = TUNIT[(mt.group(2) or "fs").lower()]
        mean = mean * f  # tau in fs
        sig, sig_ext, smin = sig * f, sig_ext * f, smin * f
        tv = LN2 * mean
        tsig = LN2 * sig
        mnum = re.match(r"^([\d.]+(?:E[+-]?\d+)?)\s*([A-Za-z]+)?", t)
        mant, u = mnum.group(1), (mnum.group(2) or "fs").lower()
        uf = TUNIT.get(u, 1.0)
        nd = dec(mant)
        exp_v = round_half_up(tv / uf, nd)
        ru = orec[49:55].strip()
        sig_native = tsig / uf
        cands = {"A_round": round_half_up(sig_native / 10.0 ** (-nd), 0), "B_ceil": ceil_int(sig_native / 10.0 ** (-nd)),
                 "C_maxmin_ceil": max(ceil_int(smin / uf / 10.0 ** (-nd)), ceil_int(sig_native / 10.0 ** (-nd))),
                 "D_ceil_ext": ceil_int(LN2 * sig_ext / uf / 10.0 ** (-nd))}
        verdict = []
        if abs(exp_v - float(mant)) > 1e-9:
            verdict.append("VALUE(%g)" % exp_v)
        for k, v in cands.items():
            if ru.isdigit() and float(ru) == v:
                verdict.append("UNC=" + k)
        print("%-9s %-5d %-4s %-22s %-26s %-9s %s" % ("%d-%d" % (start, end), owner, ident,
              t + " " + ru, "tau=%.4g(%.3g)->T=%.5g(%.3g)" % (mean, sig, tv, tsig), "-", " ".join(verdict) or "UNC-MISMATCH"))
        continue
    else:
        continue
    rv_f = float(rv) if rv else None
    if rv_f is None:
        print("%-9s %-5d %-4s %-22s %-26s %-9s %s" % ("%d-%d" % (start, end), owner, ident, "(blank)", "%.5g(%.3g)" % (mean, sig), "-", "RECORD-BLANK"))
        continue
    step = 10.0 ** (-nd)
    exp_v = round_half_up(mean, nd)
    sig_native = sig / step
    cands = {"A_round": round_half_up(sig_native, 0), "B_ceil": ceil_int(sig_native),
             "C_maxmin": max(ceil_int(smin / step), ceil_int(sig_native)),
             "D_ceil_ext": ceil_int(sig_ext / step)}
    verdict = []
    if abs(exp_v - rv_f) > 1e-9:
        verdict.append("VALUE(%g)" % exp_v)
    matched = [k for k, v in cands.items() if ru.isdigit() and float(ru) == v]
    if ru and not ru.isdigit():
        matched = [ru]
    verdict.append(("UNC=" + "/".join(matched)) if matched else "UNC-MISMATCH(%s)" % "/".join("%s:%g" % (k, v) for k, v in cands.items()))
    print("%-9s %-5d %-4s %-22s %-26s %-9s %s" % ("%d-%d" % (start, end), owner, ident, rv + "(" + (ru or "-") + ")",
          "%.5g(%.3g)ext%.3g" % (mean, sig, sig_ext), "%.2f/%d" % (chi2, dof), " ".join(verdict)))
