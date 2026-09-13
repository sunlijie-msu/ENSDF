import io, re, sys

SNAP = r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\snapshot_audited.ens"
ADOPT = sys.argv[1] if len(sys.argv) > 1 else SNAP
SRC   = r"d:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens"

PAIRS = [
    ("2127.564", "2127.0"), ("3304.212", "3303.2"), ("3916.407", "3913.0"),
    ("4074.666", "4071.8"), ("4114.81", "4114.0"), ("4624.404", "4622.4"),
    ("4688.97", "4687.6"), ("4876.842", "4875.2"), ("4889.76", "4891.1"),
    ("5228.175", "5225"), ("5318.8", "5318.8"), ("5380.99", "5382"),
    ("5679.928", "5679"), ("5690.8", "5688"), ("5998.10", "5993"),
]

def rd(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return [l.rstrip("\n").rstrip("\r") for l in f]

def is_L(l):
    return len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "L"

def ec(l):
    return l[9:19].strip()

def jtext(lines, energy):
    n = len(lines)
    for i, l in enumerate(lines):
        if is_L(l) and ec(l) == energy:
            j = i + 1
            out = []
            started = False
            while j < n and not is_L(lines[j]):
                t = lines[j]
                if len(t) > 7 and t[6:8] == "cL":
                    body = t[9:]
                    m = re.match(r"^([A-Za-z][A-Za-z]?)\$", body)
                    ident = m.group(1) if m else None
                    if t[5] == " ":
                        if ident == "J":
                            started = True
                            out.append(body[len("J$"):])
                        else:
                            started = False
                    elif started:
                        out.append(body)
                j += 1
            return " ".join(x.strip() for x in out).strip(), i + 1
    return None, None

A = rd(ADOPT)
S = rd(SRC)

num = re.compile(r"\d+(?:\.\d+)?")

print("%-10s %-10s %s" % ("ADOPTED", "SOURCE", "COMPARISON"))
print("=" * 120)
for a, s in PAIRS:
    at, al = jtext(A, a)
    st, sl = jtext(S, s)
    print("-" * 120)
    print("ADOPTED level %-9s (L line %s)  J$ start" % (a, al))
    print("  A: %s" % at)
    print("SOURCE  level %-9s (L line %s)" % (s, sl))
    print("  S: %s" % st)
    an = sorted(set(num.findall(at)))
    sn = sorted(set(num.findall(st)))
    print("  numbers adopted:", an)
    print("  numbers source :", sn)
    print("  only-in-source:", [x for x in sn if x not in an])
    print("  only-in-adopted:", [x for x in an if x not in sn])
    for k in ["1970Mo09", "1971Mu03", "1972Jo10", "1974Gr06", "1971Gr26", "1979Ba54"]:
        if k in at:
            print("  !!! adopted J$ still contains %s" % k)
