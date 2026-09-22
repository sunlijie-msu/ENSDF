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
def own_E(lineno):
    for i, t in com.get(lineno, []):
        if any(re.fullmatch(r"E(\([A-Za-z]\))?", x) for x in e_ids(t)): return True
    return False
ds = {k: parse_dataset(os.path.join(BASE, v)) for k, v in letter_to_file.items()}

def dsval(letter):
    for rec in ds.get(letter, []):
        yield rec

cat = collections.Counter(); rows = []
for a in ad:
    raw = L[a["lineno"]-1]
    if a["nG_with_DE"] > 0 or a["lineno"] == 73: continue
    if own_E(a["lineno"]) or raw[76] in qual: continue
    Ead = num(a["E_str"]); DEad = (a["DE_str"] or "").strip()
    step = 10.0 ** (-dec_places(a["E_str"]))
    tol = (int(DEad) * step) if DEad.isdigit() else 0.0
    xr = parse_xref(a["xref"] or "")
    plain = [x[0] for x in xr if x[1] is None]
    modif = [(x[0], x[1], x[2]) for x in xr if x[1] is not None]
    inDE = []; exactE = []; exactEDE = []
    for x in xr:
        for rec in ds.get(x[0], []):
            d = abs(num(rec["E_str"]) - Ead)
            if d <= tol + 1e-12: inDE.append(x[0])
            if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == dec_places(a["E_str"]): exactE.append(x[0])
            if num(rec["E_str"]) == Ead and dec_places(rec["E_str"]) == dec_places(a["E_str"]) \
               and (rec["DE_str"] or "").strip() == DEad: exactEDE.append(x[0])
    plain_inDE = sorted(set(plain) & set(inDE)); plain_exact = sorted(set(plain) & set(exactEDE))
    if len(set(exactEDE)) == 1 and set(exactEDE) <= set(plain) and len(plain_inDE) == 1:
        c = "OK"           # source unambiguous from XREF + byte-exact value
    elif len(set(exactEDE)) == 1 and (set(exactEDE) & set(plain)) and len(plain_inDE) > 1:
        c = "TIE"          # several plain datasets inside adopted DE
    elif len(set(exactEDE)) == 1 and not (set(exactEDE) & set(plain)):
        c = "XREF-MOD"     # matching dataset carries a parenthesised (mismatched) energy
    elif len(set(exactEDE)) > 1:
        c = "MULTI"
    elif plain_inDE:
        c = "AVG"          # no byte-exact source: adopted value is an average/rounded
    elif inDE:
        c = "MODIFIED-ONLY"
    else:
        c = "NO-SUPPORT"
    cat[c] += 1
    rows.append(dict(line=a["lineno"], E=a["E_str"], DE=a["DE_str"], nG=a["nG"], xref=a["xref"],
                     cat=c, plain=plain, plain_inDE=plain_inDE, exactEDE=sorted(set(exactEDE)),
                     modif=modif, inDE=sorted(set(inDE))))
print("=== classification of the 194 fit-impossible levels with no note/flag ===")
for k, v in cat.most_common(): print("  %-14s %d" % (k, v))
json.dump(rows, open(r".github\temp\2026-09-22_s34_level_trace\xref_consistency.json", "w"), indent=0)
print()
for k in ("TIE", "XREF-MOD", "MULTI", "AVG", "MODIFIED-ONLY", "NO-SUPPORT"):
    sel = [r for r in rows if r["cat"] == k]
    if not sel: continue
    print("### %s (%d) ###" % (k, len(sel)))
    for r in sel[:15]:
        print("  line %4d E=%-10s DE=%-3s xref=%-30s plain=%s inDE=%s exactEDE=%s" %
              (r["line"], r["E"], r["DE"] or "-", r["xref"] or "-", r["plain"], r["inDE"], r["exactEDE"]))
    print()
