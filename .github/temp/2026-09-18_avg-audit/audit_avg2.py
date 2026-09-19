"""Audit every arithmetic average statement in an ENSDF adopted file (v2).

Fixes vs v1: {In} is interpreted in last-digits notation (absolute sigma from the
value's own decimal places); optional unit token allowed between value and {In};
lifetime comments compared after tau -> T1/2 (ln 2) conversion.
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


def cmt_start(l):
    return len(l) > 7 and l[5] == " " and l[6] == "c"


def cmt_cont(l):
    return len(l) > 7 and l[5] != " " and l[6] == "c"


blocks = []
i = 0
while i < len(lines):
    if cmt_start(lines[i]):
        j = i + 1
        while j < len(lines) and cmt_cont(lines[j]):
            j += 1
        blocks.append((i + 1, j, [lines[k][8:].rstrip() for k in range(i, j)]))
        i = j
    else:
        i += 1

ITEM = re.compile(r"(\d+(?:\.\d+)?)\s*(fs|ns|ps|s|eV|keV|MeV)?\s*\{I([+-]?\d+)(?:-(\d+))?\}")


def dec_places(s):
    return len(s.split(".")[1]) if "." in s else 0


def sig_of(vstr, up, dn):
    d = dec_places(vstr)
    scale = 10.0 ** (-d)
    if dn is None:
        return abs(float(up)) * scale
    a, b = abs(float(up)) * scale, abs(float(dn)) * scale
    return (a + b) / 2.0


def owner_of(start0):
    for k in range(start0 - 1 - 1, -1, -1):
        if is_data(lines[k]):
            return k, lines[k]
    return None, None


def t_to_fs(val, unit):
    if not unit:
        return None
    mult = {"fs": 1.0, "ps": 1e3, "ns": 1e6, "s": 1e15}
    return val * mult.get(unit.lower(), 1.0)


rows = []
for start, end, body in blocks:
    text = " ".join(t.strip() for t in body)
    if not re.search(r"averag", text, re.I):
        continue
    oidx, orec = owner_of(start)
    kind = orec[7] if orec else "?"
    ident = body[0].split("$")[0].strip() if "$" in body[0] else ""
    m = re.search(r"(un)?(weighted )?average of", text, re.I)
    if not m:
        rows.append((start, end, oidx, kind, ident, "NO-AVG-PHRASE", text, None, None, None, None))
        continue
    weighted = not (m.group(1) and m.group(1).lower() == "un")
    tail = text[m.end():]
    items = []
    pos = 0
    for mm in ITEM.finditer(tail):
        gap = tail[pos:mm.start()]
        if items and re.search(r"\.\s|;\s", gap):
            break
        items.append((float(mm.group(1)), sig_of(mm.group(1), mm.group(3), mm.group(4)),
                      mm.group(0), mm.group(2)))
        pos = mm.end()
    # record fields
    if kind == "L":
        recE, recDE = orec[9:19].strip(), orec[19:21].strip()
        recT, recDT = orec[39:49].strip(), orec[49:55].strip()
        recRI = recDRI = None
    else:
        recE, recDE = orec[9:19].strip(), orec[19:21].strip()
        recRI, recDRI = orec[22:29].strip(), orec[29:31].strip()
        recT = recDT = None
    comment_result = None
    mt = re.search(r"\|t\s*=\s*(\d+(?:\.\d+)?)\s*(fs|ns|ps)?\s*\{I([+-]?\d+)(?:-(\d+))?\}", text)
    if mt:
        comment_result = (float(mt.group(1)), sig_of(mt.group(1), mt.group(3), mt.group(4)), mt.group(2) or "fs")
    rows.append((start, end, oidx, kind, ident, "", text, items, (recE, recDE, recT, recDT, recRI, recDRI),
                 comment_result, weighted))

# ---- report
print("file:", PATH)
print("average blocks:", len(rows))
for start, end, oidx, kind, ident, st, text, items, rec, cresult, weighted in rows:
    print("=" * 104)
    print("CMT %d-%d | owner %d | %s | id=%r | %s" % (
        start, end, (oidx or 0) + 1, kind, ident, "weighted" if weighted else "unweighted"))
    print("  record:", lines[oidx])
    if st:
        print("  !!", st, "->", text[:160])
        continue
    print("  inputs (%d):" % len(items), [(v, s) for v, s, _, _ in items])
    if cresult:
        print("  comment |t = %s %s {I%s}" % (cresult[0], cresult[2], cresult[1]))
    if len(items) < 2:
        print("  -> <2 inputs")
        continue
    vals = [v for v, _, _, _ in items]
    sigs = [s for _, s, _, _ in items]
    if any(s <= 0 for s in sigs):
        print("  -> bad sigma")
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
        chi2, dof, sf = float("nan"), len(vals) - 1, 1.0
    print("  mean=%.5g  sig=%.5g  SF=%.3f  scaled_sig=%.5g  chi2=%.3f dof=%d" % (
        mean, sig, sf, sig * sf, chi2, dof))
