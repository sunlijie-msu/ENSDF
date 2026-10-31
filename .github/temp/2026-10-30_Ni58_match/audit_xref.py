import re
from collections import Counter, defaultdict

def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]

def levels(AD):
    out = []
    for i, l in enumerate(AD, 1):
        if l[5] == " " and l[6] == " " and l[7] == "L":
            out.append((i, l))
    return out

def xrefs(AD, start, stop):
    res = []
    for n in range(start + 1, stop):
        l = AD[n - 1]
        if "XREF=" in l or l[5] != " " and l[6] != "c":
            pass
    return res

def collect(AD, tag):
    """return list of (level_line, energy, j, xref_string, xref_line)"""
    lv = levels(AD)
    res = []
    for k, (ln, l) in enumerate(lv):
        nxt = lv[k + 1][0] if k + 1 < len(lv) else len(AD) + 1
        xs, xl = "", None
        for n in range(ln + 1, nxt):
            if "XREF=" in AD[n - 1]:
                xs += AD[n - 1][9:80].rstrip()
                xl = n if xl is None else xl
            if AD[n - 1][5] == " " and AD[n - 1][6] == " " and AD[n - 1][7] in "G":
                break
        res.append((ln, l[9:19].strip(), l[19:21].strip(), l[22:39].strip(), xs, xl))
    return res

def parse_labels(xs):
    """xs like 'XREF=CDK(*)' or 'XREF=C(7590)EN(7560*)'"""
    s = xs[5:] if xs.startswith("XREF=") else xs
    s = re.sub(r"XREF[+=]", "", s)
    labels = []
    i = 0
    KEY = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")
    while i < len(s):
        c = s[i]
        if c in KEY:
            lab = c; i += 1
            mod = ""
            if i < len(s) and s[i] == "(":
                j = s.find(")", i)
                if j < 0:
                    return labels, f"unclosed '(' at offset {i}"
                mod = s[i:j + 1]; i = j + 1
            labels.append(lab + mod)
        elif c == " ":
            return labels, f"embedded space at offset {i}"
        else:
            return labels, f"illegal char {c!r} at offset {i} in {s!r}"
    return labels, None

def order_key(mod):
    m = re.search(r"\(([^)]*)\)", mod)
    if not m: return (0, "")
    inner = m.group(1)
    d = re.sub(r"[^0-9.]", "", inner)
    return (1, d)

def audit(path, tag):
    AD = L(path)
    rows = collect(AD, tag)
    print(f"\n===== {tag}: {len(rows)} levels =====")

    err = defaultdict(list)
    star_count = Counter()
    plain_energy = defaultdict(list)

    for ln, e, de, j, xs, xl in rows:
        if not xs:
            continue
        labels, e2 = parse_labels(xs)
        if e2:
            err["malformed"].append((ln, xl, xs, e2))
            continue
        # letter order + duplicate label
        seen = []
        for lab in labels:
            if lab in seen:
                err["duplicate label"].append((ln, xl, xs, lab))
            seen.append(lab)
        letters = [x[0] for x in labels]
        keyf = lambda c: (c.lower(), 1 if c.islower() else 0)
        ks = [keyf(c) for c in letters]
        if ks != sorted(ks):
            err["letter order"].append((ln, xl, xs, "".join(letters)))
        if "*" in xs:
            for lab in labels:
                if "*" in lab:
                    star_count[lab] += 1
        for lab in labels:
            plain_energy[lab].append(ln)

    for k in ("malformed", "duplicate label", "letter order"):
        print(f"\n-- {k}: {len(err[k])}")
        for ln, xl, xs, why in err[k]:
            print(f"   level :{ln:<5} xref :{xl:<5} [{why}]  {xs}")

    single = {k: v for k, v in star_count.items() if v < 2}
    print(f"\n-- starred labels appearing on only ONE level: {len(single)}")
    for lab, c in sorted(single.items()):
        print(f"   {lab} (count {c})")

    dup = Counter()
    for ln, e, de, j, xs, xl in rows:
        if e:
            dup[(e, de)] += 1
    print("\n-- level records with identical E and DE:")
    for (e, de), c in dup.items():
        if c > 1:
            ls = [ln for ln, e2, d2, j, xs, xl in rows if e2 == e and d2 == de]
            print(f"   E={e} DE={de!r} x{c} at lines {ls}")

for p, t in [(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens", "58Ni"),
             (r"XUNDL/A58/Co58/new/Co58_adopted.ens", "58Co")]:
    audit(p, t)
