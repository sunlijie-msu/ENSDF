import re, sys, os, json, collections
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, BASE, letter_to_file, parse_adopted, parse_dataset, parse_xref, num, dec_places
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
ad = parse_adopted(ADOPTED)
ds = {k: parse_dataset(os.path.join(BASE, v)) for k, v in letter_to_file.items()}

def classify(a):
    Ead = num(a["E_str"]); DEad = (a["DE_str"] or "").strip()
    step = 10.0 ** (-dec_places(a["E_str"]))
    tol = (int(DEad) * step) if DEad.isdigit() else 0.0
    xr = parse_xref(a["xref"] or "")
    plain = [x[0] for x in xr if x[1] is None]
    inDE, exactEDE, exactE = [], [], []
    for x in xr:
        for rec in ds.get(x[0], []):
            if abs(num(rec["E_str"]) - Ead) <= tol + 1e-12: inDE.append(x[0])
            if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == dec_places(a["E_str"]):
                exactE.append(x[0])
                if (rec["DE_str"] or "").strip() == DEad: exactEDE.append(x[0])
    return sorted(set(plain)), sorted(set(inDE)), sorted(set(exactE)), sorted(set(exactEDE)), tol

print("=== examples named by user ===")
for ln, E in ((1569, None), (1574, None), (1838, None)):
    pass
for a in ad:
    if a["E_str"] in ("11411.33", "11440.4", "12151"):
        p, i, eE, eEDE, tol = classify(a)
        print("line %4d E=%-9s DE=%-3s xref=%-26s plain=%s inDE=%s byteExactE=%s byteExactE+DE=%s" %
              (a["lineno"], a["E_str"], a["DE_str"] or "-", a["xref"], p, i, eE, eEDE))
        for letter in eEDE:
            for rec in ds[letter]:
                if num(rec["E_str"]) == num(a["E_str"]):
                    print("        %s line %d: |%s|" % (letter, rec["lineno"], open(os.path.join(BASE, letter_to_file[letter]), encoding="utf-8", errors="replace").read().split("\n")[rec["lineno"]-1]))

print("\n=== whole-file XREF/value consistency (all L records except g.s.) ===")
prob = collections.Counter(); detail = collections.defaultdict(list)
for a in ad:
    if a["lineno"] == 73: continue
    p, i, eE, eEDE, tol = classify(a)
    raw = L[a["lineno"]-1]
    if not a["xref"] or not p:
        cat = "no plain XREF letter"
    elif not i:
        cat = "no dataset level within adopted DE"
    elif len(i) > 1:
        cat = ">=2 XREF datasets within adopted DE"
    elif len(set(eEDE)) > 1:
        cat = ">=2 byte-exact E+DE matches"
    elif len(set(eEDE)) == 1 and set(eEDE) & set(p):
        cat = "unique source = plain letter (OK)"
    elif len(set(eEDE)) == 1:
        cat = "matching dataset carries parenthesised energy"
    else:
        cat = "no byte-exact match (average/rounded/other DE)"
    prob[cat] += 1; detail[cat].append(a["lineno"])
for k, v in prob.most_common(): print("  %-45s %d" % (k, v))
print()
for k in prob:
    if k.startswith("unique source") or k.startswith("no byte-exact"): continue
    print("### %s ###" % k, detail[k][:20])
