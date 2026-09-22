import re, os, random, sys
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, BASE, letter_to_file, parse_adopted, parse_dataset, parse_xref, num, dec_places
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
A = {}
cur = 0
for i, l in enumerate(L, 1):
    if len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "L":
        A[i] = (l[9:19], l[19:21], l[78:80] if len(l) > 79 else "", l[79] if len(l) > 79 else "")
ad = parse_adopted(ADOPTED)
ds = {k: parse_dataset(os.path.join(BASE, v)) for k, v in letter_to_file.items()}
rows = []
for a in ad:
    if a["lineno"] == 73: continue
    xr = parse_xref(a["xref"] or "")
    Ead = num(a["E_str"]); DEad = (a["DE_str"] or "").strip(); d = dec_places(a["E_str"])
    B = [x[0] for x in xr for rec in ds.get(x[0], []) if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == d and (rec["DE_str"] or "").strip() == DEad]
    if len(B) == 1 and a["nG_with_DE"] == 0:
        rows.append((a["lineno"], a["E_str"], DEad, B[0], a["xref"] or ""))
print("class-A candidates with no gamma carrying DE:", len(rows))
random.seed(20260925)
sample = random.sample(rows, max(1, int(round(0.15 * len(rows)))))
bad = 0
for ln, E, DE, src, xref in sample:
    txt = open(os.path.join(BASE, letter_to_file[src]), encoding="utf-8", errors="replace").read().split("\n")
    hits = []
    for j, l in enumerate(txt, 1):
        if len(l) > 20 and l[5] == " " and l[7] == "L" and l[9:19] == E and l[19:21] == DE:
            hits.append(j)
    plain = [x[0] for x in parse_xref(xref) if x[1] is None]
    ok = len(hits) == 1 and src in plain
    if not ok: bad += 1
    print("line %4d E=%-10s DE=%-3s xref=%-24s -> %s line %s  rawE=%r rawDE=%r  %s" % (ln, E, DE or "-", xref[:24], src, hits, E, DE, "PASS" if ok else "FAIL"))
print("SPOT CHECK: %d sampled, %d FAIL" % (len(sample), bad))
