"""Comprehensive quoted-level cross-check v3.

Extracts every quoted level pair in comment blocks:
  A) '<jpi>, <E> level|resonance'   (designator present)  -- any position in a list
  B) 'to|from <jpi>, <E>'           (designator absent)   -- reported as MISSING_LEVEL_SUFFIX
and verifies energy text and J-pi text against the L records character-for-character.
Read-only.
"""
import io
import os
import re

FILES = [r"A34\Cl34\new\Cl34_adopted.ens", r"A34\S34\new\S34_adopted.ens"]

A = re.compile(r"(?P<jpi>[^,;.]{1,16}?)\s*,\s*(?P<e>g\.s\.|\d+(?:\.\d+)?)(?P<kev>-keV)?\s+(?P<des>level|resonance)\b")
B = re.compile(r"\b(?P<dir>to|from)\s+(?P<jpi>[^,;.]{1,16}?)\s*,\s*(?P<e>g\.s\.|\d+(?:\.\d+)?)(?P<kev>-keV)?(?P<des>\s+(?:level|resonance)\b)?")
SHAPE = re.compile(r"^[\d/()+\-, ]+$")


def protect(t):
    return re.sub(r"\(([^()]*)\)", lambda m: "(" + m.group(1).replace(",", "#") + ")", t)


def restore(t):
    return t.replace("#", ",")


def clean_jpi(tok):
    t = tok.strip()
    for w in ("and", "to", "from", "from ", "g.s.", "level", "levels", "resonance"):
        if t.startswith(w + " "):
            t = t[len(w) + 1:]
    return t.strip(" ,;")


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


def blocks(lines):
    out, cur = [], []
    for i, l in enumerate(lines, 1):
        if len(l) > 6 and l[6] == "c":
            cur.append(l[9:].rstrip())
            continue
        if cur:
            out.append((i - len(cur), cur))
        cur = []
    if cur:
        out.append((len(lines) - len(cur), cur))
    return out


def main():
    grand_q = grand_bad = 0
    for rel in FILES:
        lines = load(rel)
        lv, gs = {}, {}
        for i, l in enumerate(lines):
            if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
                lv.setdefault(l[9:19].strip(), []).append((i + 1, l[22:39].strip()))
        print("=" * 98)
        print("FILE", os.path.basename(rel), " L-records:", len(lv))
        print("=" * 98)
        n_q = n_bad = 0
        for first, blk in blocks(lines):
            merged = protect(re.sub(r"\s+", " ", " ".join(blk)).strip())
            seen = set()
            for m in A.finditer(merged):
                jpi, e, des = restore(clean_jpi(m.group("jpi"))), m.group("e"), m.group("des")
                if not SHAPE.match(jpi) or not re.search(r"\d", jpi):
                    continue
                key = (jpi, e)
                if key in seen:
                    continue
                seen.add(key)
                n_q += 1
                rec = lv.get("0.0") if e == "g.s." else lv.get(e)
                if rec is None:
                    n_bad += 1
                    print("  L%-5d ENERGY_TEXT_NOT_FOUND  quoted %-10r J=%-8r (%s)" % (first, e, jpi, des))
                    continue
                rj = rec[0][1]
                if not (jpi == rj or jpi in [p.strip() for p in rj.split(",")]):
                    n_bad += 1
                    print("  L%-5d JPI_MISMATCH  quoted E=%-10r J=%-8r -> record L%d E=%r J=%r"
                          % (first, e, jpi, rec[0][0], e, rj))
            for m in B.finditer(merged):
                jpi, e = restore(clean_jpi(m.group("jpi"))), m.group("e")
                if m.group("des"):
                    continue
                if not SHAPE.match(jpi) or not re.search(r"\d", jpi):
                    continue
                end = m.end("e")
                if end < len(merged) and merged[end] in "+-":
                    continue
                key = ("B", jpi, e)
                if key in seen:
                    continue
                seen.add(key)
                n_q += 1
                rec = lv.get("0.0") if e == "g.s." else lv.get(e)
                if rec is None:
                    n_bad += 1
                    print("  L%-5d NO_DESIGNATOR + ENERGY_TEXT_NOT_FOUND  quoted %-10r J=%-8r" % (first, e, jpi))
                else:
                    rj = rec[0][1]
                    bad_j = not (jpi == rj or jpi in [p.strip() for p in rj.split(",")])
                    if bad_j:
                        n_bad += 1
                    print("  L%-5d NO_DESIGNATOR  quoted %-10r J=%-8r (record L%d E=%r J=%r)%s"
                          % (first, e, jpi, rec[0][0], e, rj, "   <<< JPI_MISMATCH" if bad_j else ""))
        print("  pairs checked: %d   problems: %d" % (n_q, n_bad))
        print()
        grand_q += n_q
        grand_bad += n_bad
    print("TOTAL pairs checked: %d   problems: %d" % (grand_q, grand_bad))


if __name__ == "__main__":
    main()
