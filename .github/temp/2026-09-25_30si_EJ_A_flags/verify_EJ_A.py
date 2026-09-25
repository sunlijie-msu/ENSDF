"""Bidirectional check: flag-A L records of the 30Si(a,g) dataset vs Adopted Levels.

Forward  : for each target flag-A record, find the adopted level with the same E text.
Reverse  : for each adopted level used as source, confirm the target carries the same
           E, DE and J text on an A-flagged record.
Read-only.
"""
import io

T = r"d:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens"
A = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"

SOURCE_LEVELS = ("0.0", "2127.558", "3304.207", "3916.40", "4074.657", "5679.925")


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


def levels(lines, flag=None):
    out = []
    for i, l in enumerate(lines):
        if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
            if flag is None or l[76] == flag:
                out.append((i + 1, l[9:19], l[19:21], l[22:39]))
    return out


tgt = levels(load(T), flag="A")
ad = {e.rstrip(): (e, de, j) for _, e, de, j in levels(load(A))}

print("target flag-A records: %d" % len(tgt))
print("FWD/RVS check (target E/DE/J  vs  adopted E/DE/J):")
ok = True
used = []
for n, e, de, j in tgt:
    a = ad.get(e.strip())
    if a is None:
        print("  line %-4d E=%-10r -> NO adopted level with this E" % (n, e.strip()))
        ok = False
        continue
    used.append(e.strip())
    same = (e == a[0]) and (de == a[1]) and (j == a[2])
    ok = ok and same
    print(
        "  line %-4d %-3s E=%-10r/%-10r DE=%-3r/%-3r J=%-14r/%-14r"
        % (n, "OK" if same else "DIFF", e, a[0], de, a[1], j, a[2])
    )

print()
print("reverse: adopted sources not present as an A-flag record:")
missing = [s for s in SOURCE_LEVELS if s not in used]
print("  ", missing if missing else "none")
print("  extra A-flag energies not in the source list:",
      [u for u in used if u not in SOURCE_LEVELS] or "none")
print()
print("ALL FIELDS MATCH ADOPTED" if ok and not missing else "PROBLEM")
