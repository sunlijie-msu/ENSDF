"""Read-only audit: for every G record carrying an M/M,MR cG comment, compare the
field's firmness against the evidence cited in the comment (RUL / POL / level scheme)."""
PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
OUT = r"d:\X\ND\ENSDF\.github\temp\2026-09-21_mfield-parens-scan\audit_mfield.txt"


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
                cur["comment"].append(s[9:].rstrip())
            continue
        if kind == "L" and not cont:
            lv = dict(line=i, e=s[9:19].strip(), j=s[22:39].strip(),
                      t=s[39:49].strip())
            cur = None
            continue
        if kind == "G":
            if cont:
                continue
            cur = dict(line=i, e=s[9:19].strip(), m=s[32:41].strip(),
                       mr=s[41:49].strip(), flag=s[76:77], q=s[79:80],
                       comment=[], level=lv)
            recs.append(cur)

    def cls(m):
        if "[" in m:
            return "bracket"
        if "(" in m:
            return "paren"
        return "firm"

    rows = []
    for r in recs:
        txt = " ".join(r["comment"])
        base = ("M$" in txt) or ("M,MR$" in txt)
        rul = "RUL" in txt
        pol = "POL" in txt or "pol" in txt
        ruled = "ruled out" in txt or "excluded" in txt
        rows.append((cls(r["m"]), r, base, rul, pol, ruled, txt))

    out = []
    for c in ("paren", "bracket", "firm"):
        sel = [x for x in rows if x[0] == c]
        out.append("### %s: %d records (%d with M-basis comment)"
                   % (c, len(sel), len([x for x in sel if x[2]])))
    out.append("")
    out.append("=== MISMATCH CANDIDATE 1: tentative/bracket field citing RUL/POL ===")
    bad = [x for x in rows if x[0] in ("paren", "bracket")
           and (x[3] or x[4] or x[5])]
    for c, r, base, rul, pol, ruled, txt in bad:
        out.append("%-7s L%-5d E=%-10s M=%-11s flag=%r RUL=%s POL=%s"
                   % (c, r["line"], r["e"], r["m"], r["flag"], rul, pol))
        out.append("        %s" % txt)
    out.append("count=%d" % len(bad))
    out.append("")
    out.append("=== MISMATCH CANDIDATE 2: firm field, M-basis comment, no RUL/POL ===")
    bad2 = [x for x in rows if x[0] == "firm" and x[2] and not (x[3] or x[4]
                                                              or x[5])]
    for c, r, base, rul, pol, ruled, txt in bad2:
        out.append("%-7s L%-5d E=%-10s M=%-11s MR=%-8s flag=%r L(Jpi)=%s"
                   % (c, r["line"], r["e"], r["m"], r["mr"], r["flag"],
                      (r["level"] or {}).get("j")))
        out.append("        %s" % txt)
    out.append("count=%d" % len(bad2))
    out.append("")
    out.append("=== ALL records with M-basis comment: field class tally ===")
    for c, r, base, rul, pol, ruled, txt in rows:
        if not base:
            continue
        out.append("%-7s L%-5d E=%-10s M=%-11s flag=%r RUL=%s POL=%s | %s"
                   % (c, r["line"], r["e"], r["m"], r["flag"], rul, pol,
                      txt[:95]))
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out[:4]))
    print("cand1=%d cand2=%d -> %s" % (len(bad), len(bad2), OUT))


main()
