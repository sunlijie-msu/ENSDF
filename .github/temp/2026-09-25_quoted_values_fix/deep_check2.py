"""Comprehensive quoted-level cross-check: extracts EVERY 'J-pi, ENERGY level' pair in
comment blocks (including items in comma-separated lists), then verifies the energy text
and the J-pi text against the L records character-for-character. Read-only."""
import io
import os
import re

FILES = [r"A34\Cl34\new\Cl34_adopted.ens", r"A34\S34\new\S34_adopted.ens"]

# candidate pair: <jpi>, <energy> [level|resonance]
CAND = re.compile(
    r"(?P<jpi>\([^()]{1,8}\)[+-]?|[0-9]{1,2}(?:/[0-9]{1,2})?[+-]|\([0-9,/]{1,8}\)[+-]?)"
    r"\s*,\s*(?P<e>g\.s\.|\d+(?:\.\d+)?)(?P<kev>-keV)?"
    r"(?P<suf>\s+(?:level|resonance)\b)?"
)
JPI_OK = re.compile(r"^(?:\([\d,/]{1,8}\)[+-]?|\d{1,2}(?:/\d{1,2})?[+-]?)$")


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


def blocks(lines):
    out, cur, start = [], [], None
    for i, l in enumerate(lines, 1):
        if len(l) > 6 and l[6] == "c":
            if start is None:
                start = i
            cur.append((i, l[9:].rstrip()))
            continue
        if cur:
            out.append(cur)
        cur, start = [], None
    if cur:
        out.append(cur)
    return out


def main():
    for rel in FILES:
        lines = load(rel)
        lv = {}
        for i, l in enumerate(lines):
            if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
                try:
                    lv.setdefault(l[9:19].strip(), []).append((i + 1, l[22:39].strip()))
                except Exception:
                    pass
        g_e = {}
        for i, l in enumerate(lines):
            if len(l) == 80 and l[5:7] == "  " and l[7] == "G":
                try:
                    g_e.setdefault(l[9:19].strip(), []).append(i + 1)
                except Exception:
                    pass
        print("=" * 96)
        print("FILE", os.path.basename(rel))
        print("=" * 96)
        n_q = n_bad = 0
        for blk in blocks(lines):
            for ln, txt in blk:
                # join the whole block so list items spanning lines are seen
                pass
            merged = re.sub(r"\s+", " ", " ".join(t for _, t in blk)).strip()
            first = blk[0][0]
            for m in CAND.finditer(merged):
                jpi, e, suf = m.group("jpi"), m.group("e"), m.group("suf")
                if not JPI_OK.match(jpi):
                    continue
                # skip if the number is itself a J-pi (immediately followed by +/-)
                end = m.end("e")
                if end < len(merged) and merged[end] in "+-":
                    continue
                has_dir = bool(re.search(r"\b(?:to|from)\s*$", merged[: m.start()]))
                if not (suf or has_dir):
                    continue
                n_q += 1
                if e == "g.s.":
                    rec = lv.get("0.0")
                else:
                    rec = lv.get(e)
                if rec is None:
                    n_bad += 1
                    print("  L%-5d %-14s J=%-8s  ENERGY_TEXT_NOT_FOUND   (quoted %r)" % (first, repr(e), repr(jpi), e))
                else:
                    rj = rec[0][1]
                    ok_j = jpi == rj or jpi in [p.strip() for p in rj.split(",")]
                    if not ok_j:
                        n_bad += 1
                        print("  L%-5d %-14s J=%-8s  JPI_MISMATCH: record L%d J=%r" % (first, repr(e), repr(jpi), rec[0][0], rj))
        print("  pairs checked: %d   mismatches: %d" % (n_q, n_bad))
        print()


if __name__ == "__main__":
    main()
