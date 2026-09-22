"""Build quoted-value substitution plan for S34_adopted.ens.

Reads checker output (errors_clean.txt), derives find->replace rules per comment
line, reflows affected comment lines to 80 columns, and writes:
  - edits.txt      : OLD visible lines / NEW exact 80-col lines per edit
  - simulated.ens  : full file with edits applied (for checker verification)
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"d:\X\ND\ENSDF")
TGT = ROOT / "A34" / "S34" / "new" / "S34_adopted.ens"
TMP = ROOT / ".github" / "temp" / "quoted_check"
ERRORS = TMP / "errors_clean.txt"

# Manual rules for NOT_FOUND (data do not exist as records; map to adopted string)
NOTFOUND = {
    (322, "3303.2"): "3304.207",
    (349, "4687.6"): "4688.96",
    (407, "3303.2"): "3304.207",
    (427, "4875.2"): "4876.839",
    (463, "4687.6"): "4688.96",
    (519, "4687.6"): "4688.96",
    (547, "4687.6"): "4688.96",
    (626, "4687.6"): "4688.96",
    (160, "1945.5"): "1947.060",
    (252, "2750.9"): "2749.24",
    (275, "4890.7"): "4889.30",
    (297, "3191.6"): "3194.74",
    (308, "3255"): "3253.21",
    (349, "1000"): "1001.5",
    (512, "5575"): "5755.871",
    (519, "4604"): "4614",
    (519, "2043"): "2053",
    (620, "1560"): "1557",
    (620, "5688"): "5690.61",
    (729, "8138.08"): "8136.98",
    (948, "9710"): "9706",
    (966, "9858"): "9867",
}

PAT = {
    "LEVEL_ENERGY_MISMATCH": r'Quoted "([^"]+)" keV, L-record has "([^"]+)"',
    "GAMMA_ENERGY_MISMATCH": r'Quoted "([^"]+)" keV, G-record has "([^"]+)"',
    "JPI_MISMATCH": r'Quoted J-pi "([^"]+)", L-record J field is "([^"]+)"',
    "MULTIPOLARITY_MISMATCH": r'Quoted "([^"]+)", G-record M field is "([^"]+)"',
}

raw = (TGT.read_bytes().decode("ascii")).split("\r\n")
lines = raw[:]  # 0-based list, last element may be ''

# ---- parse errors -----------------------------------------------------------
text = ERRORS.read_text(encoding="utf-8")
rules = []  # (line, quoted, expected, context, kind)
for chunk in text.split("\n  #")[1:]:
    kind = re.search(r"\[([A-Z_]+)\]", chunk).group(1)
    ln = int(re.search(r"line (\d+)", chunk).group(1))
    ctx = re.search(r"Context: (.+)", chunk)
    ctx = ctx.group(1).strip() if ctx else ""
    if kind in PAT:
        m = re.search(PAT[kind], chunk)
        rules.append((ln, m.group(1), m.group(2), ctx, kind))
    elif kind.endswith("NOT_FOUND"):
        q = re.search(r'of ([\d.]+) keV', chunk).group(1)
        if (ln, q) not in NOTFOUND:
            print(f"!! no manual rule for NOT_FOUND line {ln} quote {q}")
            sys.exit(2)
        rules.append((ln, q, NOTFOUND[(ln, q)], ctx, kind))

print(f"rules parsed: {len(rules)}")

# ---- apply substitutions to individual lines --------------------------------
def apply_rule(line, quoted, expected, ctx):
    """Replace the quoted token on this line, disambiguating with ctx if needed."""
    occ = [m.start() for m in re.finditer(re.escape(quoted), line)]
    if not occ:
        return None, "not-found-in-line"
    if len(occ) == 1:
        idx = 0
    else:
        # locate ctx inside line, then pick the quoted token inside ctx
        probe = ctx
        pos = line.find(probe)
        if pos < 0:
            # ctx may be the concatenation of several lines; use last sentence piece
            for piece in re.split(r"[.;] ", ctx):
                pos = line.find(piece)
                if pos >= 0:
                    probe = piece
                    break
        if pos < 0:
            return None, f"ambiguous({len(occ)}) ctx-unmatched"
        inside = [o for o in occ if pos <= o < pos + len(probe)]
        if len(inside) != 1:
            return None, f"ambiguous({len(occ)}) ctx-inside={len(inside)}"
        idx = occ.index(inside[0])
    return line[:occ[idx]] + expected + line[occ[idx] + len(quoted):], f"occ{idx}/{len(occ)}"


changed = {}   # line number -> new full line text (no padding yet)
report = []
for ln, quoted, expected, ctx, kind in rules:
    cur = lines[ln - 1]
    new, how = apply_rule(cur, quoted, expected, ctx)
    if new is None:
        print(f"FAIL line {ln}: {how} | quote={quoted} kind={kind}")
        print(f"     line: {cur}")
        print(f"     ctx : {ctx}")
        continue
    # ensure the substituted text is inside the comment text region
    if new[:9] != cur[:9]:
        print(f"FAIL line {ln}: prefix changed")
        continue
    lines[ln - 1] = new
    changed[ln] = new[:80]
    report.append((ln, kind, quoted, expected, how))

print(f"lines substituted: {len(changed)} / {len(rules)} rules")

# ---- reflow blocks whose text now exceeds 71 cols ---------------------------
def block_of(n):
    """Return list of 1-based line numbers of the cL J$ block containing line n."""
    i = n - 1
    while i >= 0:
        l = lines[i]
        if len(l) < 10:
            return None
        if l[6:7] == "c" and l[7:8] == "L" and l[0:5].strip():
            # start of a cL line; walk forward over continuations
            out = [i + 1]
            j = i + 1
            while j < len(lines) and lines[j][5:6] != " ":
                out.append(j + 1)
                j += 1
            return out
        i -= 1
    return None

CONT = "23456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
refiles = []
for ln in sorted(changed):
    txt = changed[ln][9:]
    if len(txt.rstrip()) <= 71:
        continue
    blk = block_of(ln)
    if blk is None:
        print(f"!! no block for line {ln}")
        continue
    start = blk.index(ln)
    prefixes = [lines[b - 1][:9] for b in blk]
    # rebuild tail text
    tail = " ".join(changed[b][9:].strip() for b in blk[start:])
    tail = re.sub(r"\s+", " ", tail).strip()
    words = tail.split(" ")
    wrapped, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= 71:
            cur += " " + w
        else:
            wrapped.append(cur)
            cur = w
    if cur:
        wrapped.append(cur)
    refiles.append((ln, blk[start:], wrapped, prefixes))
    print(f"reflow line {ln}: block lines {blk[start:]}, {len(words)} words -> {len(wrapped)} lines")

# ---- emit new lines ---------------------------------------------------------
def pad(txt80prefix, text):
    return txt80prefix + text + " " * (80 - 9 - len(text))

EMIT = {}
for ln, newtxt in changed.items():
    EMIT[ln] = pad(newtxt[:9], newtxt[9:].strip())
for ln, blkreflines, wrapped, prefixes in refiles:
    for k, b in enumerate(blkreflines):
        pre = prefixes[k] if k < len(prefixes) else None
        if k >= len(prefixes):
            # extra line needed: build continuation prefix from the previous one
            prev = prefixes[-1]
            ch = CONT[len(prefixes) - 1] if len(prefixes) - 1 < len(CONT) else "?"
            pre = prev[:5] + ch + prev[6:]
            print(f"!! block {ln}: adding continuation line prefix {pre!r}")
        EMIT[b] = pad(pre, wrapped[k])
    # drop lines if wrapped is shorter than the block tail
    for b in blkreflines[len(wrapped):]:
        EMIT[b] = None
        print(f"!! block {ln}: dropping line {b}")

# ---- write plan + simulated file -------------------------------------------
sim = []
plan = []
for i, l in enumerate(lines):
    n = i + 1
    if n not in changed and l == "":
        if n <= len(raw) - 1:
            sim.append(l)
        continue
    if n in EMIT:
        newv = EMIT[n]
        if newv is None:
            plan.append(f"--- DELETE line {n}: {l[:100]!r}")
            continue
        plan.append(f"--- line {n}\nOLD:{l}\nNEW:{newv}  [len={len(newv)}]")
        sim.append(newv)
    else:
        sim.append(l)

(TMP / "edits.txt").write_text("\n".join(plan), encoding="utf-8")
(TMP / "simulated.ens").write_bytes(("\r\n".join(sim)).encode("ascii"))
print("wrote edits.txt and simulated.ens")
