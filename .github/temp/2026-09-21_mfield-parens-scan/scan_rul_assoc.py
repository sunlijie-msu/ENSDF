"""Read-only: associate every RUL / POL mention in cG comments with its G record.

Association rule: a comment block (col 7 == 'c') belongs to the nearest preceding
record whose column 6 is blank (a genuine data record); continuation records
('2 G', 'F G', 'B G') keep the same owner.
"""
import sys

PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"


def main():
    L = open(PATH, "rb").read().decode("utf-8").split("\r\n")
    def owner(i):
        """index i (0-based) is a comment line -> return owning record index."""
        j = i - 1
        while j >= 0:
            s = L[j]
            if len(s) > 8 and s[6:7] == "c":
                j -= 1
                continue
            if s[5:6] == " " and s[7:8] in ("G", "L", "B", "E", "A", "D", "P"):
                return j
            j -= 1
        return None

    hits = []
    for i, s in enumerate(L):
        if len(s) > 8 and s[6:7] == "c" and ("RUL" in s or "POL" in s):
            o = owner(i)
            if o is None:
                continue
            r = L[o]
            hits.append((i + 1, s.strip(), o + 1, r[7:8], r[32:41].strip(),
                         r[9:19].strip()))
    print("comment lines citing RUL/POL:", len(hits))
    bad = []
    for cl, txt, rl, kind, m, e in hits:
        tentative = "(" in m or "[" in m
        tag = "TENTATIVE-FIELD" if tentative else ("blank-field" if not m
                                                  else "firm")
        print("c L%-5d -> %s L%-5d E=%-10s M=%-11s %s | %s" %
              (cl, kind, rl, e, m, tag, txt[:95]))
        if tentative:
            bad.append((cl, rl, e, m, txt))
    print("\nVIOLATIONS (tentative/bracket M field + RUL/POL clause):", len(bad))
    for cl, rl, e, m, txt in bad:
        print("  c L%-5d G L%-5d E=%-10s M=%-11s | %s" % (cl, rl, e, m, txt))


main()
