"""Audit averages v4: strict ENSDF rounding comparison with candidate-error list.

For each block: expected value/uncertainty computed from the comment's own listed
inputs (last-digit uncertainties, chi2 scaling), rounded per ENSDF rules, compared
with the owning record field. Flags rows where strict rounding disagrees.
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


def sig_ld(vstr, up, dn):
    s = 10.0 ** (-dec(vstr))
    if dn is None:
        return abs(float(up)) * s
    return (abs(float(up)) + abs(float(dn))) / 2.0 * s


def round_half_up(x, nd):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def ensdf_unc(sig, step, allow2=False):
    """Return (digits_string) for sigma expressed in units of `step` (last digit)."""
    d = sig / step
    # 1 sig fig, 4-up rule
    import math as _m
    e = _m.floor(_m.log10(d)) if d > 0 else 0
    base = 10.0 ** e
    q = d / base
    up = 4.0  # 4-up: round up when next digit >= 4
    if q < 1.5:
        q2 = 1.0 if (q - 1.0) < 0.4 else 2.0
    elif q < 2.5:
        q2 = 2.0
    else:
        q2 = float(round(q + 0.0001))
    return q2 * base


def parse_Tfield(tstr, dtstr):
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


print("%-9s %-5s %-5s %-20s %-24s %-14s %s" % ("cmt", "owner", "id", "record", "recomputed", "delta", "flag"))
print("-" * 118)
cand = []
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
        items.append((float(mm.group(1)), sig_ld(mm.group(1), mm.group(3), mm.group(4))))
        pos = mm.end()
    if len(items) < 2:
        continue
    vals = [v for v, _ in items]
    sigs = [s for _, s in items]
    if any(s <= 0 for s in sigs):
        continue
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
        sf = 1.0
    sig *= sf

    if kind in "GL" and ident == "E" and orec[9:19].strip():
        rv_s, ru_s = orec[9:19].strip(), orec[19:21].strip()
        rv = float(rv_s)
        nd = dec(rv_s)
        step = 10.0 ** (-nd)
        exp_v = round_half_up(mean, nd)
        exp_unc = ensdf_unc(sig, step)
        flag = ""
        if abs(exp_v - rv) > 1e-9:
            flag += "VALUE"
        if ru_s and ru_s.isdigit() and abs(exp_unc - float(ru_s)) > 1e-9:
            flag += "+UNC"
        print("%-9s %-5d %-5s %-20s %-24s %-14s %s" % (
            "%d-%d" % (start, end), oidx + 1, kind + ident, rv_s + "(" + (ru_s or "-") + ")",
            ("%.4f(%.3g)" % (mean, sig)), "%.4f" % (exp_v - rv), flag))
        if "VALUE" in flag:
            cand.append((start, end, oidx + 1, kind + ident, rv_s, ru_s, mean, sig))
    elif kind == "G" and ident == "RI" and orec[22:29].strip():
        rv_s, ru_s = orec[22:29].strip(), orec[29:31].strip()
        rv = float(rv_s)
        nd = dec(rv_s)
        step = 10.0 ** (-nd)
        exp_v = round_half_up(mean, nd)
        flag = "" if abs(exp_v - rv) <= 1e-9 else "VALUE"
        print("%-9s %-5d %-5s %-20s %-24s %-14s %s" % (
            "%d-%d" % (start, end), oidx + 1, "GRI", rv_s + "(" + (ru_s or "-") + ")",
            ("%.4f(%.3g)" % (mean, sig)), "%.4f" % (exp_v - rv), flag))
        if flag:
            cand.append((start, end, oidx + 1, "GRI", rv_s, ru_s, mean, sig))
    elif kind == "L" and ident == "T":
        mt = re.search(r"\|t\s*=\s*(\d+(?:\.\d+)?)\s*(fs|ns|ps)?\s*\{I([+-]?\d+)(?:-(\d+))?\}", text)
        if not mt:
            continue
        fact = TUNIT[(mt.group(2) or "fs").lower()]
        tval = float(mt.group(1)) * fact
        tsig = sig_ld(mt.group(1), mt.group(3), mt.group(4)) * fact
        rv, rsig = parse_Tfield(orec[39:49].strip(), orec[49:55].strip())
        if rv is None:
            continue
        # expected T1/2 = ln2 * mean(tau); compare in fs at record precision
        ts = orec[39:49].strip()
        mnum = re.match(r"^([\d.]+(?:E[+-]?\d+)?)", ts)
        mant = mnum.group(1)
        exp_half = LN2 * (mean * 0 + tval) if False else LN2 * tval
        nd = dec(mant)
        step = 10.0 ** (-nd) * TUNIT[(re.match(r"^[\d.]+(?:E[+-]?\d+)?\s*([A-Za-z]+)", ts).group(1) or "fs").lower()]
        exp_v = round_half_up(LN2 * tval, nd)
        rec_disp = float(mant) if "E" not in mant else float(mant.split("E")[0])
        flag = "" if abs(exp_v - rec_disp) <= 1e-9 else "VALUE"
        print("%-9s %-5d %-5s %-20s %-24s %-14s %s" % (
            "%d-%d" % (start, end), oidx + 1, "LT", ts + " " + orec[49:55].strip(),
            ("taus=%.4g(%.3g) -> T=%.4f(%.3g)" % (tval, tsig, LN2 * tval, LN2 * tsig)),
            "%.4f" % (exp_v - rec_disp), flag))
        if flag:
            cand.append((start, end, oidx + 1, "LT", ts, orec[49:55].strip(), LN2 * tval, LN2 * tsig))

print()
print("VALUE-level candidates (strict rounding disagreement):")
for c in cand:
    print("  cmt %d-%d owner %d %s rec=%s(%s) recomputed=%.4f(%.4g)" % c)
