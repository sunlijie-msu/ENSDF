"""Read-only scan: G-record M field (cols 33-41) parentheses vs cG M/MR comment basis.

Rules (gamma-selection-rules SKILL.md conversion table):
  D+Q measured  + 'M2 ruled out by RUL'      -> FIRM  M1+E2
  D+Q measured  + only '|D|p=no from level scheme' -> tentative (M1+E2)
  D(+Q) measured (delta ~ 0)                  -> tentative M1(+E2)
  POL-measured character (DCO/ADO + POL)      -> FIRM
"""
import sys

PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"


def main():
    L = open(PATH, "rb").read().decode("utf-8").split("\r\n")
    recs = []
    cur = None
    curl = None
    for i, s in enumerate(L, 1):
        if len(s) < 8:
            continue
        cont = s[5:6] != " "          # col 6 continuation label
        kind = s[7:8]                 # col 8 record type
        iscom = s[6:7] == "c"         # col 7 comment identifier
        if iscom:
            if cur is not None:
                cur["comment"].append(s[9:].rstrip())
            continue
        if kind == "L" and not cont:
            curl = dict(line=i, e=s[9:19].strip(), j=s[22:39].strip(),
                        t=s[39:49].strip())
            cur = None
            continue
        if kind == "G":
            if cont:                  # '2 G' / 'F G' -> same record
                continue
            cur = dict(line=i, e=s[9:19].strip(), de=s[19:21].strip(),
                       ri=s[22:29].strip(), dri=s[29:31].strip(),
                       m=s[32:41].strip(), comment=[], level=curl)
            recs.append(cur)
    print("total G records:", len(recs))
    classes = {"paren+RUL": [], "paren_noRUL": [], "firm+RUL": [],
               "firm_noRUL": [], "bracket": []}
    for r in recs:
        m = r["m"]
        c = " ".join(r["comment"])
        has_rul = "RUL" in c
        if not m:
            cls = None
        elif m.startswith("["):
            cls = "bracket"
        elif "(" in m:
            cls = "paren+RUL" if has_rul else "paren_noRUL"
        else:
            cls = "firm+RUL" if has_rul else "firm_noRUL"
        if cls:
            classes[cls].append(r)
            r["cls"] = cls
            r["pol"] = "POL" in c
            r["body"] = c
    for k in ("paren+RUL", "paren_noRUL", "firm+RUL", "bracket"):
        print("\n=== %s : %d ===" % (k, len(classes[k])))
        for r in classes[k]:
            lv = r["level"] or {}
            print("L%-5d %-10s M=%-11s Jpi=%-10s T=%-9s pol=%s" %
                  (r["line"], r["e"], r["m"], lv.get("j", "?"),
                   lv.get("t", "?"), r["pol"]))
            print("      c: %s" % r["body"][:150])
    print("\nfirm_noRUL count:", len(classes["firm_noRUL"]))


if __name__ == "__main__":
    sys.exit(main())
