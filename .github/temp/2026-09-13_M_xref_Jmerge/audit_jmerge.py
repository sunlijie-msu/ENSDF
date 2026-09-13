import re, sys, io

SNAP = r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\snapshot_audited.ens"
ADOPT = sys.argv[1] if len(sys.argv) > 1 else SNAP
SRC   = r"d:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens"
BEFORE= r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\head_adopted_before.txt"

TARGETS = ["2127.564","3304.212","3916.407","4074.666","4114.81","4624.404",
           "4688.97","4876.842","4889.76","5228.175","5318.8","5380.99",
           "5679.928","5690.8","5998.10"]

SRCTARGETS = {"2127.564":"2127.0","3304.212":"3303.2","3916.407":"3913.0",
              "4074.666":"4071.8","4114.81":"4114.0","4624.404":"4622.4",
              "4688.97":"4687.6","4876.842":"4875.2","4889.76":"4891.1",
              "5228.175":"5225","5318.8":"5318.8","5380.99":"5382",
              "5679.928":"5679","5690.8":"5688","5998.10":"5993"}

def readlines(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return [l.rstrip("\n").rstrip("\r") for l in f]

def is_L(l):
    return len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "L"

def is_G(l):
    return len(l) > 7 and l[5] == " " and l[6] == " " and l[7] == "G"

def is_cL(l):
    return len(l) > 7 and l[6] == "c" and l[7] == "L"

def is_cG(l):
    return len(l) > 7 and l[6] == "c" and l[7] == "G"

def is_cont_L(l):  # continuation of L record, e.g. " 34S 2 L ..." or XREF " 34S X L ..."
    return len(l) > 7 and l[6] != "c" and l[7] == "L" and l[5] != " "

def is_cont_cL(l):
    return len(l) > 7 and l[5] != " " and l[6] == "c" and l[7] == "L"

def energy_of_L(l):
    return l[9:19].strip()

def blocks(lines, want_type):
    """yield (lineno0, Lline, [ (lineno0, line) for comment lines ])"""
    n = len(lines)
    for i, l in enumerate(lines):
        if is_L(l) and energy_of_L(l) == want_type:
            out = []
            j = i + 1
            while j < n and not is_L(lines[j]):
                if is_cL(lines[j]) or is_cont_cL(lines[j]):
                    out.append((j, lines[j]))
                j += 1
            yield i, l, out

def jblock(cmt):
    """given comment lines list, return J$ group lines"""
    res = []
    inside = False
    for ln, txt in cmt:
        body = txt[9:]
        if txt[7] == "L":
            pass
        # identifier = text after col 9 up to $
        m = re.match(r"^([A-Za-z]*)\$", body)
        ident = m.group(1) if m else None
        if ident == "J":
            inside = True
            res.append((ln, txt))
        elif inside:
            # continuation only
            if txt[5] != " " and is_cont_cL(txt):
                res.append((ln, txt))
            else:
                inside = False
    return res

def jblock2(cmt):
    """sequential parse: a block starts at first cL with J$ and continues
    through continuation lines (2cL,3cL...) ; stop at next cL that is a new ident."""
    res = []
    n = len(cmt)
    k = 0
    while k < n:
        ln, txt = cmt[k]
        ident = ident_of(txt)
        if ident == "J":
            res.append((ln, txt))
            k += 1
            while k < n:
                ln2, t2 = cmt[k]
                if t2[5] != " ":
                    res.append((ln2, t2))
                    k += 1
                else:
                    break
        else:
            k += 1
    return res

def ident_of(txt):
    body = txt[9:]
    m = re.match(r"^([A-Za-z][A-Za-z]?)\$", body)
    return m.group(1) if m else None

def main():
    A = readlines(ADOPT)
    S = readlines(SRC)
    print("=" * 100)
    print("PART A: ADOPTED BLOCK STRUCTURE")
    print("=" * 100)
    for t in TARGETS:
        for i, L, cmt in blocks(A, t):
            print("-" * 100)
            print("ADOPTED level %s  L-record line %d" % (t, i + 1))
            print("  L   : %r" % L)
            for ln, txt in cmt:
                print("  c%d@%-4d len=%3d %r" % (ln + 1, ln + 1, len(txt), txt))
            # order check
            idents = []
            for ln, txt in cmt:
                if txt[5] == " ":
                    idents.append((ident_of(txt), ln + 1))
            print("  ORDER OF BLOCK STARTERS:", idents)
            jb = jblock2(cmt)
            if jb:
                print("  J$ BLOCK:")
                for ln, txt in jb:
                    print("    line %d len=%d cont=%r  %r" % (ln + 1, len(txt), txt[5], txt))
                bad = [(ln + 1, len(txt)) for ln, txt in jb if len(txt) != 80]
                print("  J-BLOCK LONG-LINES:", bad if bad else "none (all 80)")
                for key in ["1970Mo09","1971Mu03","1972Jo10","1974Gr06","1971Gr26","1979Ba54"]:
                    for ln, txt in jb:
                        if key in txt:
                            print("  !!! FORBIDDEN NSR IN J-BLOCK: %s at line %d" % (key, ln + 1))
                # continuation integrity
                labels = [txt[5] for ln, txt in jb]
                print("  CONT LABELS:", labels)
            else:
                print("  NO J$ BLOCK FOUND")

    print()
    print("=" * 100)
    print("PART B: SOURCE BLOCK STRUCTURE")
    print("=" * 100)
    for t in TARGETS:
        st = SRCTARGETS[t]
        found = False
        for i, L, cmt in blocks(S, st):
            found = True
            print("-" * 100)
            print("SOURCE level %s (for adopted %s) L-record line %d" % (st, t, i + 1))
            print("  L   : %r" % L)
            for ln, txt in cmt:
                print("  c%d@%-4d len=%3d %r" % (ln + 1, ln + 1, len(txt), txt))
            jb = jblock2(cmt)
            for ln, txt in jb:
                print("  SRC-J: line %d %r" % (ln + 1, txt))
        if not found:
            print("-" * 100)
            print("SOURCE level %s NOT FOUND (for adopted %s)" % (st, t))

main()
