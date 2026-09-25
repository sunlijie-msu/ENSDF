"""v4: verify every 'J-pi, ENERGY level' pair in comments against L records (read-only).

Anchor = the required 'level' designator, so list items are covered too.
Also audits quotes of the 'to|from J-pi, ENERGY' form that lack the designator.
"""
import io
import os
import re

FILES = [r"A34\Cl34\new\Cl34_adopted.ens", r"A34\S34\new\S34_adopted.ens"]
PAIR = re.compile(r"([^,;.\s][^,;.]{0,14}?)\s*,\s*(\d+(?:\.\d+)?|g\.s\.)\s+(level|resonance)\b")
NODES = re.compile(r"\b(?:to|from)\s+([^,;.]{1,14}?)\s*,\s*(\d+(?:\.\d+)?|g\.s\.)(?![+-])\s*(?!\s*(?:level|resonance)\b)")
SHAPE = re.compile(r"^[\d/()+,\- ]+$")


def load(p):
    with io.open(p, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


def main():
    tq = tb = 0
    for rel in FILES:
        lines = load(rel)
        lv = {}
        for i, l in enumerate(lines):
            if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
                lv.setdefault(l[9:19].strip(), []).append((i + 1, l[22:39].strip()))
        # merged comment block text per block, keeping the first line number
        blocks, cur = [], []
        for i, l in enumerate(lines, 1):
            if len(l) > 6 and l[6] == "c":
                cur.append(l[9:].rstrip())
                continue
            if cur:
                blocks.append((i - len(cur), cur))
            cur = []
        if cur:
            blocks.append((len(lines) - len(cur), cur))

        print("=" * 96)
        print("FILE", os.path.basename(rel))
        print("=" * 96)
        n = bad = 0
        for first, blk in blocks:
            txt = re.sub(r"\s+", " ", " ".join(blk)).strip()
            for m in PAIR.finditer(txt):
                jpi = m.group(1).strip(" ,;")
                for w in ("and", "to", "from", "of"):
                    if jpi.startswith(w + " "):
                        jpi = jpi[len(w) + 1:]
                e = m.group(2)
                jpi = jpi.strip(" ,;")
                if not SHAPE.match(jpi) or not re.search(r"\d", jpi):
                    continue
                n += 1
                rec = lv.get("0.0") if e == "g.s." else lv.get(e)
                if rec is None:
                    bad += 1
                    print("  L%-5d ENERGY_TEXT_NOT_FOUND   quoted %-10r J=%-8r" % (first, e, jpi))
                else:
                    rj = rec[0][1]
                    if not (jpi == rj or jpi in [p.strip() for p in rj.split(",")]):
                        bad += 1
                        print("  L%-5d JPI_MISMATCH  quoted J=%-8r E=%-10r -> record L%d J=%r" % (first, jpi, e, rec[0][0], rj))
            for m in NODES.finditer(txt):
                jpi = m.group(1).strip(" ,;")
                if not SHAPE.match(jpi) or not re.search(r"\d", jpi):
                    continue
                n += 1
                bad += 1
                print("  L%-5d MISSING_LEVEL_SUFFIX    quoted %-10r J=%-8r" % (first, m.group(2), jpi))
        print("  pairs checked: %d   problems: %d" % (n, bad))
        print()
        tq += n
        tb += bad
    print("TOTAL pairs checked: %d   problems: %d" % (tq, tb))


if __name__ == "__main__":
    main()
