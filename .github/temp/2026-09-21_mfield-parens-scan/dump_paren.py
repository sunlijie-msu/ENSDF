"""Read-only: list G records whose M field is tentative (parenthesised) or
bracketed, with full comment block + owning level, to a UTF-8 file."""
PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
OUT = r"d:\X\ND\ENSDF\.github\temp\2026-09-21_mfield-parens-scan\paren_dump.txt"


def main():
    L = open(PATH, "rb").read().decode("utf-8").split("\r\n")
    recs = []
    cur = None
    lv = None
    for i, s in enumerate(L, 1):
        if len(s) < 8:
            continue
        cont = s[5:6] != " "
        kind = s[7:8]
        if s[6:7] == "c":
            if cur is not None:
                cur["comment"].append((i, s[9:].rstrip(), s[5:6].strip()))
            continue
        if kind == "L" and not cont:
            lv = dict(line=i, e=s[9:19].strip(), j=s[22:39].strip(),
                      t=s[39:49].strip())
            cur = None
            continue
        if kind == "G":
            if cont:
                if cur is not None:
                    cur["cont"].append((i, s.strip()))
                continue
            cur = dict(line=i, e=s[9:19].strip(), de=s[19:21].strip(),
                       ri=s[22:29].strip(), m=s[32:41].strip(),
                       mr=s[41:49].strip(), dmr=s[49:55].strip(),
                       flag=s[76:77], q=s[79:80], comment=[], cont=[],
                       level=lv)
            recs.append(cur)
    par = [r for r in recs if "(" in r["m"]]
    br = [r for r in recs if "[" in r["m"]]
    out = ["TOTAL G records: %d   parenthesised(M): %d   bracketed([]): %d"
           % (len(recs), len(par), len(br)), ""]
    out.append("=== PARENTHESISED M FIELDS ===")
    for r in par:
        l = r["level"] or {}
        out.append("G L%-5d E=%-10s DE=%-3s RI=%-7s M=%-11s MR=%-8s DMR=%-6s "
                   "flag=%r Q=%r  || L%-5s E=%-9s Jpi=%-9s T=%s"
                   % (r["line"], r["e"], r["de"], r["ri"], r["m"], r["mr"],
                      r["dmr"], r["flag"], r["q"], l.get("line"),
                      l.get("e"), l.get("j"), l.get("t")))
        for i, t, c in r["comment"]:
            out.append("         cL%-5d [%s] %s" % (i, c, t))
        for i, t in r["cont"]:
            out.append("         n L%-5d %s" % (i, t))
    out.append("")
    out.append("=== BRACKETED M FIELDS ===")
    for r in br:
        l = r["level"] or {}
        out.append("G L%-5d E=%-10s M=%-11s flag=%r  || L%-5s Jpi=%-9s T=%s"
                   % (r["line"], r["e"], r["m"], r["flag"], l.get("line"),
                      l.get("j"), l.get("t")))
        for i, t, c in r["comment"]:
            out.append("         cL%-5d [%s] %s" % (i, c, t))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("total G=%d paren=%d bracket=%d -> %s" % (len(recs), len(par),
                                                    len(br), OUT))


main()
