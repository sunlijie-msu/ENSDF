"""Planner v2: compute comment-text substitutions for quoted-value findings.

Writes simulated.ens, re-runs the quoted-values checker on it, and reports
per-line overflow so wrap adjustments can be chosen.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"D:\X\ND\ENSDF")
TARGET = ROOT / "A34" / "S34" / "new" / "S34_adopted.ens"
CHECK = ROOT / ".github" / "scripts" / "check_quoted_values.py"
OUT = ROOT / ".github" / "temp" / "quoted_check"

# (block start line) -> [(old fragment, new fragment), ...] applied on the
# concatenated cL-block text.  Every value matches the adopted record exactly.
SUBS = {
    80: [("2126.7|g", "2127.498|g")],
    112: [("3303.1|g", "3304.029|g")],
    157: [("1945.5|g", "1947.060|g"), ("2127.0 level", "2127.564 level")],
    182: [("4113.7|g", "4114.52|g")],
    230: [("2560.5|g", "2561.35|g"), ("2127.0 level", "2127.564 level")],
    249: [("2750.9|g", "2749.24|g"), ("2127.0 level", "2127.564 level")],
    272: [("4890.7|g", "4889.30|g")],
    294: [("3191.6|g", "3194.74|g"), ("2127.0 level", "2127.564 level")],
    305: [("3255|g", "3253.21|g"), ("2127.0 level", "2127.564 level")],
    319: [("2376|g", "2375.657|g"), ("3303.2 level", "3304.212 level")],
    346: [("1000|g", "1001.5|g"), ("4687.6 level", "4688.97 level")],
    383: [("5997|g", "5997.30|g")],
    404: [("2864|g", "2864.56|g"), ("3303.2 level", "3304.212 level")],
    424: [("1375|g", "1374.43|g"), ("4875.2 level", "4876.842 level"),
          ("5679 level", "5679.928 level")],
    460: [("1732|g", "1732.39|g"), ("4687.6 level", "4688.97 level")],
    508: [("929|g", "929.436|g"), ("5575 level", "5755.876 level")],
    514: [("2127.0 level", "2127.564 level"), ("4687.6 level", "4688.97 level")],
    541: [("4687.6 level", "4688.97 level"), ("2127.0 level", "2127.564 level")],
    601: [("7219|g", "7218.48|g")],
    612: [("5688 level", "5690.8 level")],
    618: [("4687.6 level", "4688.97 level")],
    623: [("3916 level", "3916.407 level"), ("4877 level", "4876.842 level")],
    637: [("1+, 4075,", "1+, 4074.666,"), ("2+, 5998,", "2+, 5998.10,"),
          ("1-, 6479.", "1-, 6478.770.")],
    663: [("2128 level", "2127.564 level")],
    681: [("5691 level", "5690.8 level"),
          ("to 4-, 6251.22 level.",
           "to the 4+ level at 6251.22 (E2 implies 4-, a |p discrepancy noted "
           "in J$ for 6251.22).")],
    712: [("7110 level", "7110.451 level"), ("8036.31|g", "8036.6|g")],
    721: [("8138.08|g", "8136.98|g")],
    728: [("8173|g", "8173.8|g")],
    740: [("6077|g", "6077.27|g"), ("2128 level", "2127.564 level"),
          ("3581|g", "3581.2|g"), ("4624 level", "4624.404 level")],
    748: [("6166|g", "6166.24|g"), ("2128 level", "2127.564 level")],
    754: [("2680|g", "2680.5|g"), ("5691 level", "5690.8 level"),
          ("580|g", "580.3|g"), ("D, |DJ=1 to 6-, 7791", "(M1), |DJ=1 to 6-, 7790.2")],
    779: [("2812|g", "2812.7|g"), ("D, |DJ=1 to 5-", "(E1), |DJ=1 to 5-"),
          ("5691 level", "5690.8 level")],
    799: [("to 4-, 6251.22 level", "to 4+, 6251.22 level")],
    819: [("8185 level", "8185.46 level")],
    837: [("3044|g", "3044.1|g"), ("5-, 5691.", "5-, 5690.8.")],
    844: [("8804|g", "8804.4|g")],
    850: [("4799|g", "4799.11|g"), ("1+, 4075 level", "1+, 4074.666 level"),
          ("1244|g", "1244.32|g"), ("7630 level", "7629.907 level")],
    859: [("9913 level", "9912.9 level")],
    892: [("3722|g", "3722.6|g"), ("5691 level", "5690.8 level"),
          ("8370 level", "8370.6 level")],
    954: [("9858|g", "9868|g")],
    961: [("1408|g", "1408.6|g"), ("8503 level", "8503.6 level")],
    1055: [("2608|g", "2608.6|g"), ("7791 level", "7790.2 level"),
           ("8370 level", "8370.6 level")],
    1105: [("8503 level", "8503.6 level"), ("D, |DJ=1 to 7-", "(M1), |DJ=1 to 7-"),
           ("8370 level", "8370.6 level")],
    1579: [("3436|g", "3436.1|g")],
    1634: [("9912 level", "9912.9 level")],
    1695: [("4949|g", "4949.3|g")],
    1702: [("1966|g", "1966.8|g"), ("8(+), 11374 level", "(8), 11374.3 level")],
    1727: [("3308|g", "3308.8|g"), ("8+, 10652 level", "8(+), 10651.6 level")],
    1751: [("2768|g", "2768.9|g"), ("11807 level", "11807.5 level")],
    1773: [("1902|g", "1902.7|g"), ("13341 level", "13341.7 level")],
}

WIDTH = 71  # columns 10-80
CONT = "23456789"


def read_lines():
    return TARGET.read_text(encoding="utf-8").split("\n")


def block_span(lines, start):
    """Return (first, last) 1-based line numbers of the cL block at *start*."""
    i = start - 1
    last = i
    while (last + 1 < len(lines) and len(lines[last + 1]) > 7
           and lines[last + 1][5] != ' ' and lines[last + 1][6] == 'c'):
        last += 1
    return start, last + 1


def wrap(text):
    words = text.split()
    out, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= WIDTH:
            cur += " " + w
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def main():
    lines = read_lines()
    log = []
    new_lines = list(lines)
    for start, subs in sorted(SUBS.items(), reverse=True):
        first, last = block_span(lines, start)
        block = lines[first - 1:last]
        text = " ".join(seg[9:].rstrip() for seg in block)
        assert "  " not in text, f"double space in block at {start}"
        for old, new in subs:
            n = text.count(old)
            assert n == 1, f"line {start}: {old!r} found {n} times"
            text = text.replace(old, new)
        chunks = wrap(text)
        assert len(chunks) <= len(CONT), f"line {start}: too many lines"
        rebuilt = []
        for idx, chunk in enumerate(chunks):
            cont = " " if idx == 0 else CONT[idx - 1]
            rebuilt.append(" 34S %scL %s" % (cont, chunk))
        log.append("### block at L%d (old %d lines -> new %d lines)"
                   % (first, len(block), len(rebuilt)))
        for i, seg in enumerate(block):
            over = ""
            if i < len(rebuilt):
                delta = len(rebuilt[i]) - len(rebuilt[i - 0]) if False else None
            log.append("OLD|%s" % seg.rstrip())
        for seg in rebuilt:
            log.append("NEW|%s%s" % (seg.rstrip(),
                                     "" if len(seg) <= 80 else "  <<< TOO LONG"))
        # in-place overflow analysis
        for i, seg in enumerate(block):
            if i < len(rebuilt):
                inplace = seg
                for old, new in subs:
                    inplace = inplace.replace(old, new)
                if len(inplace) > 80:
                    log.append("    overflow L%d: %d chars (+%d), trailing pad %d"
                               % (first + i, len(inplace), len(inplace) - len(seg),
                                  len(seg) - len(seg.rstrip())))
        new_lines[first - 1:last] = [s.ljust(80) for s in rebuilt]
    sim = OUT / "simulated.ens"
    sim.write_text("\n".join(new_lines), encoding="utf-8")
    log.append("")
    log.append("wrote %s" % sim)
    proc = subprocess.run([sys.executable, str(CHECK), str(sim)],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    (OUT / "sim_report.txt").write_text(
        re.sub(r'\x1b\[[0-9;]*m', '', proc.stdout), encoding="utf-8")
    tail = proc.stdout.strip().split("\n")
    log.append("checker exit=%d" % proc.returncode)
    keep = [ln for ln in tail if re.search(r'finding|summary|ERROR|EXIT', ln, re.I)]
    log.extend(keep[-25:])
    (OUT / "plan2_report.txt").write_text("\n".join(log), encoding="utf-8")
    print("exit=%d" % proc.returncode)
    print("\n".join(keep[-25:]))


if __name__ == "__main__":
    main()
