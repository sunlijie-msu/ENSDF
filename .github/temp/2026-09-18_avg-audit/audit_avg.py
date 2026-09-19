"""Audit every arithmetic average statement in an ENSDF file.

Parses comment blocks (cL/cG + continuations), finds "average of <v1> {Iu1} from <s1>, ...",
recomputes unweighted/weighted mean (with chi2 scale factor when chi2>n-1),
and compares with the owning L/G record field and with the comment's own first value.
"""
import math
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"

lines = open(PATH, encoding="utf-8", errors="replace").read().split("\n")
if lines and lines[-1] == "":
    lines.pop()


def is_data(l):
    return len(l) > 8 and l[5] == " " and l[6] == " " and l[7] in "LG" and l[8] == " "


def cmt_start(l):
    return len(l) > 7 and l[5] == " " and l[6] == "c"


def cmt_cont(l):
    return len(l) > 7 and l[5] != " " and l[6] == "c"


# --- collect blocks: each cmt_start begins a block, following cmt_cont lines continue it
blocks = []
i = 0
while i < len(lines):
    if cmt_start(lines[i]):
        j = i + 1
        while j < len(lines) and cmt_cont(lines[j]):
            j += 1
        blocks.append((i + 1, j - 1, [lines[k][8:].rstrip() for k in range(i, j)]))
        i = j
    else:
        i += 1

NUM = r"(\d+(?:\.\d+)?)"
UNC = r"\{I([+-]?\d+)(?:-(\d+))?\}"
ITEM = re.compile(NUM + r"\s+" + UNC)


def owner_of(start):
    for k in range(start - 2, -1, -1):
        if is_data(lines[k]):
            return k + 1, lines[k]
    return None, None


def rec_fields(l, kind):
    """Return dict of numeric fields from an L or G record."""
    if kind == "L":
        e = l[9:19].strip()
        de = l[19:21].strip()
        t = l[39:49].strip()
        dt = l[49:55].strip()
        return {"E": e, "DE": de, "T": t, "DT": dt}
    e = l[9:19].strip()
    de = l[19:21].strip()
    ri = l[22:29].strip()
    dri = l[29:31].strip()
    return {"E": e, "DE": de, "RI": ri, "DRI": dri}


def fmt(x, nd=None):
    return ("%%.%df" % nd) % x if nd is not None else repr(x)


report = []
for start, end, body in blocks:
    text = " ".join(t.strip() for t in body)
    if not re.search(r"averag", text, re.I):
        continue
    oline, orec = owner_of(start)
    kind = orec[7] if orec else "?"
    ident = body[0].split("$")[0].strip() if "$" in body[0] else ""
    # window: from "average of" up to end of the value/source list
    m = re.search(r"(un)?(weighted )?average of", text, re.I)
    if not m:
        report.append(dict(start=start, end=end, owner=oline, kind=kind, ident=ident,
                           status="NO-AVG-PHRASE", text=text))
        continue
    mom = re.match(r"(un)?weighted ", m.group(0), re.I)
    weighted = not (m.group(1) and m.group(1).lower() == "un")
    tail = text[m.end():]
    # stop list at end of sentence / next comment identifier
    items = []
    pos = 0
    for mm in ITEM.finditer(tail):
        gap = tail[pos:mm.start()]
        # a new sentence/identifier boundary -> stop collecting
        if items and re.search(r"\.\s|;\s|\$\s*$", gap):
            break
        v = float(mm.group(1))
        u = float(mm.group(2)) if not mm.group(3) else float(mm.group(2) + "." + mm.group(3))
        items.append((v, u, mm.group(0)))
        pos = mm.end()
    period_end = re.search(r"[.;]", tail[pos:])
    srcs = tail[pos:pos + period_end.start()] if period_end else tail[pos:]
    srcs = " ".join(srcs.split())
    report.append(dict(start=start, end=end, owner=oline, kind=kind, ident=ident,
                       weighted=weighted, items=items, srcs=srcs,
                       rec=rec_fields(orec, kind) if orec else {}, text=text))

print("PATH", PATH)
print("blocks with 'average':", len(report))
for r in report:
    print("=" * 100)
    print("CMT %d-%d  owner L%d %s  ident=%r  %s" % (
        r["start"], r["end"], r.get("owner") or 0, r.get("kind"), r.get("ident"),
        "weighted" if r.get("weighted") else "unweighted"))
    if "items" not in r:
        print("  !!", r["status"])
        print("  ", r["text"])
        continue
    items = r["items"]
    print("  rec :", r["rec"])
    print("  n=%d inputs:" % len(items), items)
    print("  srcs:", r["srcs"][:200])
    if len(items) < 2:
        print("  -> fewer than 2 inputs; skip")
        continue
    vals = [v for v, _, _ in items]
    uncs = [u for _, u, _ in items]
    if any(u <= 0 for u in uncs):
        print("  -> zero/negative unc; skip")
        continue
    if r["weighted"]:
        w = [1.0 / u ** 2 for u in uncs]
        sw = sum(w)
        mean = sum(wi * v for wi, v in zip(w, vals)) / sw
        sig = math.sqrt(1.0 / sw)
        chi2 = sum(((v - mean) / u) ** 2 for v, u in zip(vals, uncs))
        dof = len(vals) - 1
        sf = math.sqrt(chi2 / dof) if chi2 > dof else 1.0
        sigs = sig * sf
    else:
        mean = sum(vals) / len(vals)
        sig = math.sqrt(sum(u ** 2 for u in uncs)) / len(vals)
        chi2 = float("nan")
        sf = 1.0
        sigs = sig
    print("  mean=%.3f  sigma=%.3f  scaled_sigma=%.3f  chi2=%.3f  dof=%d  SF=%.2f" % (
        mean, sig, sigs, chi2, dof, sf))
    print("  rec E=%r DE=%r | T=%r DT=%r | RI=%r DRI=%r" % (
        r["rec"].get("E"), r["rec"].get("DE"), r["rec"].get("T"), r["rec"].get("DT"),
        r["rec"].get("RI"), r["rec"].get("DRI")))
