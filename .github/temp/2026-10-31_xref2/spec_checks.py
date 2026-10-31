import io, os, re
from collections import Counter

BASE = "XUNDL/A58/Ni58/new/"
ADOPTED = "Ni58_adopted.ens"
KEYCH = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")


def lines(p):
    return [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]


def is_L(r):
    return r[5] == " " and r[6] == " " and r[7] == "L"


norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())


def val(txt):
    m = re.match(r"^([0-9]+\.?[0-9]*)(?:E([+-]?\d+))?$", txt.replace(" ", ""))
    return float(m.group(1)) * 10.0 ** (int(m.group(2)) if m.group(2) else 0) if m else None


AD = lines(BASE + ADOPTED)
keys = {r[8]: norm(r[9:39]) for r in AD if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
files = {}
for fn in os.listdir(BASE):
    if fn.endswith(".ens") and fn != ADOPTED:
        files.setdefault(norm(lines(BASE + fn)[0][9:39]), []).append(fn)
LF = {k: files[v][0] for k, v in keys.items() if len(files.get(v, [])) == 1}

TXT, NUM = {}, {}
for k, fn in LF.items():
    t = [r[9:19].strip() for r in lines(BASE + fn) if is_L(r) and r[9:19].strip()]
    TXT[k] = set(t)
    NUM[k] = sorted(v for v in (val(x) for x in t) if v is not None)

idx = [i for i, r in enumerate(AD) if is_L(r)]
exact = textdiff = missing = 0
bad, bare_star, plain = [], 0, 0
comment_before_xref = []
for n, i in enumerate(idx):
    end = idx[n + 1] if n + 1 < len(idx) else len(AD)
    xs, first_x, saw_comment = "", None, False
    for j in range(i + 1, end):
        r = AD[j]
        if r[5] != " " and r[7] == "L" and r[9:].lstrip().startswith("XREF"):
            xs += re.sub(r"^XREF(?:\+=|=)", "", r[9:80].strip())
            if first_x is None:
                first_x = j
        elif first_x is None and r[6] == "c":
            saw_comment = True
    if saw_comment and first_x is not None:
        comment_before_xref.append(AD[i][9:50].strip())
    s = xs
    m = re.match(r"^-\(([^)]*)\)(.*)$", s)
    if m:
        s = m.group(2)
    p = 0
    while p < len(s):
        c = s[p]
        if c in KEYCH:
            lab = c; p += 1; mod = ""
            if p < len(s) and s[p] == "(":
                q = s.find(")", p)
                if q < 0:
                    break
                mod = s[p + 1:q]; p = q + 1
            if lab not in LF:
                continue
            if mod == "*":
                bare_star += 1
            nm = re.match(r"^(\d+(?:\.\d+)?)[*?]*$", mod)
            if nm:
                txt = nm.group(1)
                if txt in TXT[lab]:
                    exact += 1
                elif any(abs(v - float(txt)) < 1e-6 for v in NUM[lab]):
                    textdiff += 1
                    bad.append((AD[i][9:50].strip(), lab + "(" + mod + ")", "same value, different text"))
                else:
                    missing += 1
                    near = min(NUM[lab], key=lambda v: abs(v - float(txt)))
                    bad.append((AD[i][9:50].strip(), lab + "(" + mod + ")", "no such level; nearest %g" % near))
            elif mod == "":
                plain += 1
        else:
            p += 1

print("datasets mapped:", len(LF))
print("labels with numeric energy: exact text match %d | same value, other text %d | no such level %d" % (exact, textdiff, missing))
for x in bad:
    print("   ", x)
print("bare (*) labels (recommended form is (energy*)):", bare_star)
print("plain labels:", plain)
print("levels with a comment line between L-record and XREF record:", len(comment_before_xref), "of", len(idx))
