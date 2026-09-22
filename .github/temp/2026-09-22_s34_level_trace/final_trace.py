import re, sys, collections, json
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, parse_adopted
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
ad = parse_adopted(ADOPTED)
ID_RE = re.compile(r"^\s*([A-Za-z0-9()]+(?:\s*,\s*[A-Za-z0-9()]+)*)\s*\$")

com = collections.defaultdict(list)   # key 0 => file-level (general) comments
cur = 0
for i, l in enumerate(L, 1):
    if len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "L":   # plain L record
        cur = i
    elif len(l) > 7 and l[6] == "c" and l[7] == "L":    # cL comment line
        com[cur].append((i, l[9:80].rstrip()))

def e_ids(txt):
    m = ID_RE.match(txt)
    return [t.strip() for t in m.group(1).split(",")] if m else []

qual = collections.defaultdict(list)
for ln, txt in com[0]:
    for tok in e_ids(txt):
        q = re.fullmatch(r"E\(([A-Za-z])\)", tok)
        if q:
            qual[q.group(1)].append(ln)

print("GENERAL (file-level) cL comments before first L record:")
for ln, txt in com[0]:
    print("  %3d | %s" % (ln, txt))
print("\nE(X) qualifier notes: %s" % {k: v for k, v in sorted(qual.items())})

def own_E(lineno):
    for i, txt in com.get(lineno, []):
        if any(re.fullmatch(r"E(\([A-Za-z]\))?", t) for t in e_ids(txt)):
            return i
    return None

rows = []
for a in ad:
    l = L[a["lineno"]-1]
    flag = l[76]
    fit = a["nG_with_DE"] > 0
    noted = own_E(a["lineno"])
    if fit:
        why = "fit-basis (general cL E$ line 27)"
    elif noted:
        why = "own E note line %d" % noted
    elif flag in qual:
        why = "col-77 flag %s -> E(%s)$ line %d" % (flag, flag, qual[flag][0])
    else:
        why = None
    rows.append(dict(line=a["lineno"], E=a["E_str"], DE=a["DE_str"], nG=a["nG"],
                     nGde=a["nG_with_DE"], fit=fit, flag=flag, xref=a["xref"] or "", why=why))

gap = [r for r in rows if not r["fit"] and not r["why"] and r["line"] != 73]
print("\ntotal L records: %d" % len(rows))
print("fit-basis: %d ; fit-impossible: %d" % (sum(r["fit"] for r in rows), sum(not r["fit"] for r in rows)))
print("  fit-impossible documented by own E note: %d" % sum(1 for r in rows if not r["fit"] and r["why"] and "own" in r["why"]))
print("  fit-impossible documented by col-77 flag: %d" % sum(1 for r in rows if not r["fit"] and r["why"] and "flag" in r["why"]))
print("  g.s. excluded: 1")
print("  => UNTRACEABLE: %d" % len(gap))
print("\nflag letters among untraceable: %s" % dict(collections.Counter(r["flag"] for r in gap)))
print("  untraceable w/o G records: %d ; with G records lacking DE: %d" % (sum(r["nG"] == 0 for r in gap), sum(r["nG"] > 0 for r in gap)))
json.dump(rows, open(r".github\temp\2026-09-22_s34_level_trace\rows_true.json", "w"), indent=0)
open(r".github\temp\2026-09-22_s34_level_trace\gap_true.txt", "w", encoding="utf-8").write(
    "UNTRACEABLE E(level) entries: %d\n\n" % len(gap) +
    "".join("line %4d  E=%-10s DE=%-3s nG=%d flag=%r xref=%s\n" %
            (r["line"], r["E"], r["DE"] or "-", r["nG"], r["flag"], r["xref"]) for r in gap))
print("\nflagged-but-excluded levels (proof):")
for r in rows:
    if not r["fit"] and r["why"] and "flag" in r["why"]:
        print("  " + r["why"] + "  |  line %d E=%s DE=%s xref=%s" % (r["line"], r["E"], r["DE"] or "-", r["xref"]))
