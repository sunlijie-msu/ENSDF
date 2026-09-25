"""Independent cross-check of every quoted level energy and its J-pi in comments
against the L-record fields (character-for-character). Read-only.

Detects: quoted energy vs L-record E text, quoted J-pi vs L-record J text,
missing 'level'/'resonance' designator, and J-pi lists (which quote no energy).
"""
import io
import os
import re
import sys

CONFIG = [
    r"A34\Cl34\new\Cl34_adopted.ens",
    r"A34\S34\new\S34_adopted.ens",
]

JPI_CHARS = r"[0-9/()+\-]"
# comma style:  to/from <jpi>, <E>[-keV][ level|resonance]
RE_COMMA = re.compile(
    r"\b(to|from)\s+([0-9/()+\-, ]{1,24}?)\s*,\s*(\d+(?:\.\d+)?|g\.s\.)(-keV)?"
    r"(\s+(?:level|resonance)\b)?"
)
# no-comma style:  to/from <jpi> <E>-keV [level]
RE_NOKEV = re.compile(
    r"\b(to|from)\s+([0-9/()+\-]{1,12}?)\s+(\d+(?:\.\d+)?)-keV(\s+(?:level|resonance)\b)?"
)
# no-comma style:  to/from <jpi> <E> level
RE_PLAIN = re.compile(
    r"\b(to|from)\s+([0-9/()+\-]{1,12}?)\s+(\d+(?:\.\d+)?)\s+(level|resonance)\b"
)


def is_jpi_list(text, m, eidx):
    """True when the number is really a J-pi value followed by +/- (list case)."""
    e = m.end(eidx)
    return e < len(text) and text[e] in "+-"


def load(path):
    with io.open(path, newline="") as fh:
        return fh.read().replace("\r\n", "\n").split("\n")


def comment_blocks(lines):
    """Return (first_line_no, merged_text) for each maximal run of comment lines."""
    blocks, cur, start = [], [], None
    for i, l in enumerate(lines, 1):
        if len(l) > 6 and l[6] == "c":
            if start is None:
                start = i
            cur.append(l[9:].rstrip())
            continue
        if cur:
            blocks.append((start, re.sub(r"\s+", " ", " ".join(cur)).strip()))
        cur, start = [], None
    if cur:
        blocks.append((start, re.sub(r"\s+", " ", " ".join(cur)).strip()))
    return blocks


def l_records(lines):
    by_text, by_val = {}, []
    for i, l in enumerate(lines):
        if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
            e_txt = l[9:19].strip()
            j_txt = l[22:39].strip()
            by_text.setdefault(e_txt, []).append((i + 1, j_txt))
            try:
                by_val.append((float(e_txt), i + 1, e_txt, j_txt))
            except ValueError:
                pass
    return by_text, by_val


def j_match(quoted, record_j):
    """Character match of the quoted J-pi against the L-record J field."""
    q = quoted.strip(" ,;")
    if q == record_j:
        return "EXACT"
    parts = [p.strip() for p in record_j.split(",")]
    if q in parts or any(p == q for p in parts):
        return "EXACT(token)"
    if q.replace(" ", "") == record_j.replace(" ", ""):
        return "EXACT(spacing)"
    return "DIFF"


def main():
    total = 0
    bad = 0
    for rel in CONFIG:
        lines = load(rel)
        by_text, by_val = l_records(lines)
        print("=" * 100)
        print("FILE", os.path.basename(rel), " L-records:", len(by_text))
        print("=" * 100)
        found = 0
        for ln, text in comment_blocks(lines):
            for rx, ge, gs in ((RE_COMMA, 3, 5), (RE_NOKEV, 3, 4), (RE_PLAIN, 3, None)):
                for m in rx.finditer(text):
                    direction, jpi, est = m.group(1), m.group(2), m.group(ge)
                    if is_jpi_list(text, m, ge):
                        continue          # J-pi list -> quotes no energy
                    found += 1
                    total += 1
                    has_suffix = True if gs is None else bool(m.group(gs))
                    if est == "g.s.":
                        has_suffix = True
                        rec = by_text.get("0.0")
                    else:
                        rec = by_text.get(est)
                    if rec is None:
                        near = [t for t in by_val if abs(t[0] - float(est)) <= 1.0]
                        status = "ENERGY_NOT_FOUND"
                        detail = ("closest: " + ", ".join("%s L%d J=%s" % (t[2], t[1], t[3]) for t in near)) if near else "no level within 1 keV"
                        jstat = "-"
                    else:
                        status = "ENERGY_EXACT"
                        detail = "L%d J=%s" % (rec[0][0], rec[0][1])
                        jstat = j_match(jpi, rec[0][1])
                    flag = ""
                    if status != "ENERGY_EXACT" or jstat not in ("EXACT", "EXACT(token)", "EXACT(spacing)", "-") or not has_suffix:
                        flag = "  <<< CHECK"
                    if flag:
                        bad += 1
                    print("  L%-5d %-4s %-16s J%-14s suff=%-5s %-17s %-28s%s"
                          % (ln, direction, repr(est), repr(jpi), has_suffix, status, jstat + " " + detail, flag))
        print("  quotes checked in this file:", found)
        print()
    print("TOTAL quotes checked:", total, " flagged:", bad)


if __name__ == "__main__":
    sys.exit(main())
