import re, math
from collections import Counter, defaultdict
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    if not e: return None, None
    m = re.match(r"^([0-9.]+)", e)
    if not m: return None, None
    E = float(m.group(1))
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    return E, (int(d) * 10.0**-dec if d.isdigit() else 0.0)

def parse_J(rec):
    a = rec[22:39].strip(); b = rec[21:39].strip()
    if b and (b[0].isdigit() or b[0] in "(+-"):
        a = b
    return a

def jset(txt):
    if not txt: return set()
    out = set()
    for tok in re.split(r"[,\s]+", txt.strip()):
        if not tok: continue
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        nums = re.findall(r"\d+", tok)
        if not nums: out.add((None, par))
        for n in nums: out.add((int(n), par))
    return out

def jcmp(a, b):
    sa, sb = jset(a), jset(b)
    if not sa or not sb: return "?"
    for ja, pa in sa:
        for jb, pb in sb:
            if ja is not None and jb is not None and ja != jb: continue
            if pa is not None and pb is not None and pa != pb: continue
            return "ok"
    return "X"

ds = []
for l in C:
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s = parse_E(l)
        if E is not None: ds.append(dict(E=E, s=s, J=parse_J(l)))
lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ad = []
for k, i in enumerate(lv):
    l = AD[i-1]; E, s = parse_E(l)
    if E is None: continue
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]: xs += re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    ad.append(dict(E=E, s=s, J=parse_J(l), X=xs))

def cclaim(x):
    if not x: return None
    m = re.search(r"C(?:\(([^)]*)\))?", x)
    if not m: return None
    return m.group(1) if m.group(1) else ""

def tol(a, b): return max(3.0, 3.0*math.sqrt(a["s"]**2 + b["s"]**2))

# assign: each adopted level citing C -> C peak
used = Counter()
rows = []
for a in ad:
    cl = cclaim(a["X"])
    if cl is None: continue
    par = None
    m = re.match(r"^([0-9.]+)", cl)
    if m: par = float(m.group(1))
    if par is not None:
        cand = sorted(ds, key=lambda d: abs(d["E"]-par))
        rep = cand[0]
        status = "par" if abs(rep["E"]-par) <= 2.0 else "DANGLING"
    else:
        cand = sorted(ds, key=lambda d: abs(d["E"]-a["E"]))
        rep = cand[0]
        status = "nearest"
    dE = abs(rep["E"]-a["E"]); t = tol(a, rep)
    jc = jcmp(a["J"], rep["J"])
    used[(rep["E"], rep["s"])] += 1
    v = status
    if status != "DANGLING":
        if jc == "X": v = "J-MISMATCH"
        elif dE > t: v = "FAR"
        else: v = "ok"
    rows.append((a, rep, dE, t, jc, v, status, par))

print("verdict counts:")
for k, n in Counter(r[5] for r in rows).most_common(): print(f"   {k:<12}{n}")

print("\n--- multiple adopted levels claiming the SAME C peak ---")
byc = defaultdict(list)
for a, rep, dE, t, jc, v, st, par in rows: byc[(rep["E"], rep["s"])].append((a, rep, dE, v))
for k, lst in byc.items():
    if len(lst) > 1:
        print(f"   C peak {k[0]}+-{k[1]} claimed by {len(lst)} adopted levels: "
              + ", ".join(f"{a['E']}+-{a['s']}({a['J']}) dE={dE:.1f}[{v}]" for a, rep, dE, v in lst))

print("\n--- adopted citing C but J mismatch / FAR / dangling ---")
for a, rep, dE, t, jc, v, st, par in rows:
    if v in ("J-MISMATCH", "FAR", "DANGLING"):
        print(f"   ad {a['E']}+-{a['s']} J={a['J']:<10} claim={cclaim(a['X'])!r:<12} -> "
              f"C {rep['E']}+-{rep['s']} J={rep['J']:<10} dE={dE:5.1f} tol={t:5.1f} [{v}]")

print("\n--- C peaks never used by any citing adopted level ---")
for d in ds:
    if used[(d["E"], d["s"])] == 0:
        near = sorted(ad, key=lambda a: abs(a["E"]-d["E"]))[0]
        print(f"   C {d['E']}+-{d['s']:<4} J={d['J']:<10} nearest ad {near['E']}+-{near['s']} "
              f"J={near['J']:<10} dE={abs(near['E']-d['E']):5.1f} tol={tol(near,d):5.1f} "
              f"Ccited={'C' in near['X']} J={jcmp(near['J'],d['J'])}")
