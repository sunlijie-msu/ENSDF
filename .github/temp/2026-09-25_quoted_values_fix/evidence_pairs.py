"""Evidence dump: verify the three quoted pairs in the Cl34 3964.1-level J$ comment
against their L records, and re-confirm the ASCII status of both adopted files."""
import io

CL = r"A34\Cl34\new\Cl34_adopted.ens"
S34 = r"A34\S34\new\S34_adopted.ens"
PAIRS = [("2+", "2157.9"), ("3+", "146.36"), ("4+", "2375.67")]


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


lines = load(CL)
print("Cl34 3964.1-level cL J$ comment, quoted pair -> L record:")
for i, l in enumerate(lines, 1):
    if "2157.9 level" in l:
        print("  comment L%d: %s" % (i, l.rstrip()))
        break
for jpi, e in PAIRS:
    hit = [(k + 1, lines[k][9:19].strip(), lines[k][22:39].strip())
           for k in range(len(lines))
           if len(lines[k]) == 80 and lines[k][5:7] == "  " and lines[k][7] == "L"
           and lines[k][9:19].strip() == e]
    for k, et, jt in hit:
        ok = (jt == jpi)
        print("   quoted %-8s %-9s  ->  L%-4d E=%-10r J=%-6r  %s"
              % (jpi, e, k, et, jt, "MATCH" if ok else "MISMATCH"))
print()
for f in (CL, S34):
    n = 0
    txt = io.open(f, newline="", encoding="utf-8").read()
    for i, l in enumerate(txt.replace("\r\n", "\n").split("\n"), 1):
        bad = [c for c in l if ord(c) > 126]
        if bad:
            n += 1
            print("%s L%d: %d non-ASCII %s" % (f.split("/")[-1], i, len(bad),
                                               " ".join("U+%04X" % ord(c) for c in bad)))
    print("%s: non-ASCII lines = %d" % (f.split("/")[-1], n))
