import re, sys, os, json, collections
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, BASE, letter_to_file, parse_adopted, parse_dataset, parse_xref, num, dec_places
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
ad = parse_adopted(ADOPTED)
ID_RE = re.compile(r"^\s*([A-Za-z0-9()]+(?:\s*,\s*[A-Za-z0-9()]+)*)\s*\$")
com = collections.defaultdict(list); cur = 0
for i, l in enumerate(L, 1):
    if len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "L": cur = i
    elif len(l) > 7 and l[6] == "c" and l[7] == "L": com[cur].append((i, l[9:80].rstrip()))
def e_ids(t):
    m = ID_RE.match(t); return [x.strip() for x in m.group(1).split(",")] if m else []
qual = set()
for ln, t in com[0]:
    for tok in e_ids(t):
        q = re.fullmatch(r"E\(([A-Za-z])\)", tok)
        if q: qual.add(q.group(1))
def own_note(lineno):
    for i, t in com.get(lineno, []):
        if any(re.fullmatch(r"E(\([A-Za-z]\))?", x) for x in e_ids(t)): return i
    return None
ds = {k: parse_dataset(os.path.join(BASE, v)) for k, v in letter_to_file.items()}

cls = collections.Counter(); rows = []
for a in ad:
    if a["lineno"] == 73: continue
    raw = L[a["lineno"]-1]
    Ead = num(a["E_str"]); DEad = (a["DE_str"] or "").strip()
    step = 10.0 ** (-dec_places(a["E_str"]))
    tol = (int(DEad) * step) if DEad.isdigit() else 0.0
    xr = parse_xref(a["xref"] or "")
    plain = [x[0] for x in xr if x[1] is None]
    P_in = sorted({x for x in plain for rec in ds.get(x, []) if abs(num(rec["E_str"]) - Ead) <= tol + 1e-12})
    B = sorted({x[0] for x in xr for rec in ds.get(x[0], [])
                if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == dec_places(a["E_str"])
                and (rec["DE_str"] or "").strip() == DEad})
    fit = a["nG_with_DE"] > 0
    note = own_note(a["lineno"]); flag = raw[76]
    doc = fit or note is not None or flag in qual
    if len(B) == 1 and B[0] in plain and len(P_in) == 1: c = "A unambiguous (1 plain letter, byte-exact)"
    elif len(B) == 1 and B[0] in plain: c = "B byte-exact unique, other plain letters within DE"
    elif len(B) > 1: c = "C several byte-exact datasets"
    elif doc: c = "D no byte-exact, documented (note/flag/fit)"
    else: c = "E NEEDS REVISION"
    cls[c] += 1
    rows.append(dict(line=a["lineno"], E=a["E_str"], DE=a["DE_str"], xref=a["xref"] or "", nG=a["nG"],
                     plain=plain, P_in=P_in, B=B, fit=fit, note=note, flag=flag, c=c))
print("=== whole file classification (368 L records, g.s. excluded from revision logic) ===")
for k, v in sorted(cls.items()): print("  %-48s %d" % (k, v))
print()
print("--- B bucket (fit-impossible without note, i.e. the '194' set members) ---")
for r in rows:
    if r["c"].startswith("B") and not r["fit"] and r["note"] is None and r["flag"] not in qual:
        print("   line %4d E=%-10s DE=%-3s plain=%s inDE=%s byteexact=%s xref=%s" % (r["line"], r["E"], r["DE"] or "-", r["plain"], r["P_in"], r["B"], r["xref"]))
print()
print("--- E bucket (needs revision) ---")
for r in rows:
    if r["c"].startswith("E"):
        print("   line %4d E=%-10s DE=%-3s xref=%s plain=%s inDE=%s note=%s flag=%r" % (r["line"], r["E"], r["DE"] or "-", r["xref"], r["plain"], r["P_in"], r["note"], r["flag"]))
print()
print("--- C bucket ---")
for r in rows:
    if r["c"].startswith("C"): print("   line %4d E=%-10s DE=%-3s byteexact=%s fit=%s note=%s xref=%s" % (r["line"], r["E"], r["DE"] or "-", r["B"], r["fit"], r["note"], r["xref"]))
print()
print("--- D bucket (documented, no byte-exact source) ---")
for r in rows:
    if r["c"].startswith("D"): print("   line %4d E=%-10s DE=%-3s xref=%-24s note=%s flag=%r fit=%s" % (r["line"], r["E"], r["DE"] or "-", r["xref"][:24], r["note"], r["flag"], r["fit"]))
