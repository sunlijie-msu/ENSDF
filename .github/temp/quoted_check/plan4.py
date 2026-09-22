"""Build quoted-value substitution plan for S34_adopted.ens.

Errors are reported at the cL J$ block start line.  We merge each block's text
(exactly as check_quoted_values.py does), apply the find->replace rules, re-wrap
to 71 text chars (cols 10-80), pad lines to 80, and emit the OLD/NEW line pairs
plus a simulated .ens for verification with the checker.
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"d:\X\ND\ENSDF")
TGT = ROOT / "A34" / "S34" / "new" / "S34_adopted.ens"
TMP = ROOT / ".github" / "temp" / "quoted_check"
ERRORS = TMP / "errors_live.txt"

NOTFOUND = {
    "1945.5": "1947.060",
    "2750.9": "2749.24",
    "4890.7": "4889.30",
    "3191.6": "3194.74",
    "3255": "3253.21",
    "3303.2": "3304.207",
    "1000": "1001.5",
    "4687.6": "4688.96",
    "4875.2": "4876.839",
    "5575": "5755.871",
    "4604": "4614",
    "2043": "2053",
    "1560": "1557",
    "5688": "5690.61",
    "8138.08": "8136.98",
    "9710": "9706",
    "9858": "9867",
}

PAT = {
    "LEVEL_ENERGY_MISMATCH": r'Quoted "([^"]+)" keV, L-record has "([^"]+)"',
    "GAMMA_ENERGY_MISMATCH": r'Quoted "([^"]+)" keV, G-record has "([^"]+)"',
    "JPI_MISMATCH": r'Quoted J-pi "([^"]+)", L-record J field is "([^"]+)"',
    "MULTIPOLARITY_MISMATCH": r'Quoted "([^"]+)", G-record M field is "([^"]+)"',
}

lines = TGT.read_bytes().decode("ascii").split("\r\n")

# record energy strings, used to sanity-check manual NOT_FOUND targets
rec = {"L": set(), "G": set()}
for l in lines:
    if len(l) >= 19 and l[5:6] == " " and l[6:7] == " " and l[7:8] in ("L", "G"):
        rec[l[7:8]].add(l[9:19].strip())

# ---- parse errors, group by block start line -------------------------------
text = ERRORS.read_text(encoding="utf-8")
blocks_rules = {}
for chunk in text.split("\n  #")[1:]:
    kind = re.search(r"\[([A-Z_]+)\]", chunk).group(1)
    ln = int(re.search(r"line (\d+)", chunk).group(1))
    ctx = re.search(r"Context: (.+)", chunk)
    ctx = ctx.group(1).strip() if ctx else ""
    if kind in PAT:
        m = re.search(PAT[kind], chunk)
        quoted, expected = m.group(1), m.group(2)
    else:
        quoted = re.search(r"of ([\d.]+) keV", chunk).group(1)
        if quoted not in NOTFOUND:
            print(f"!! no manual rule for {kind} line {ln} quote {quoted}")
            sys.exit(2)
        expected = NOTFOUND[quoted]
        want = "L" if kind.startswith("LEVEL") else "G"
        if expected not in rec[want]:
            print(f"!! manual target {expected} ({quoted}) is not an existing {want}-record")
            sys.exit(3)
    rules = blocks_rules.setdefault(ln, [])
    if (quoted, expected, kind) not in rules:
        rules.append((quoted, expected, ctx, kind))

print(f"blocks with errors: {len(blocks_rules)}  rules: {sum(len(v) for v in blocks_rules.values())}")


def block_lines(start):
    """1-based line numbers of the cL J$ block starting at `start`."""
    out = [start]
    j = start  # 0-based index of next line
    while j < len(lines) and len(lines[j]) >= 10 and lines[j][5:6] != " ":
        out.append(j + 1)
        j += 1
    return out


def locate(merged, quoted, ctx):
    occ = [m.start() for m in re.finditer(re.escape(quoted), merged)]
    if not occ:
        return None, "not-found"
    if len(occ) == 1:
        return occ[0], "unique"
    for probe in [ctx] + [p.strip() for p in re.split(r"[.;] ", ctx)]:
        if len(probe) < 4:
            continue
        pos = merged.find(probe)
        if pos < 0:
            continue
        inside = [o for o in occ if pos <= o < pos + len(probe)]
        if len(inside) == 1:
            return inside[0], f"ctx({len(occ)} occ)"
    # token-bounded occurrences (quoted token delimited by non-word characters)
    tb = [m.start() for m in re.finditer(
        r"(?<![A-Za-z0-9|_])" + re.escape(quoted) + r"(?![A-Za-z0-9|_])", merged)]
    if len(tb) == 1:
        return tb[0], f"token-bounded({len(occ)} occ)"
    return None, f"ambiguous({len(occ)} occ, token-bounded={len(tb)})"


emits = {}     # first line number of a block -> list of new 80-col lines
problems = []
added = []
for start, rules in sorted(blocks_rules.items()):
    bl = block_lines(start)
    prefixes = [lines[b - 1][:9] for b in bl]
    merged = re.sub(r"\s+", " ", " ".join(lines[b - 1][9:80].strip() for b in bl)).strip()
    for quoted, expected, ctx, kind in rules:
        pos, how = locate(merged, quoted, ctx)
        if pos is None:
            problems.append((start, quoted, expected, kind, how, ctx))
            continue
        merged = merged[:pos] + expected + merged[pos + len(quoted):]
    # greedy re-wrap at 71 chars
    words = merged.split(" ")
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
    if len(wrapped) > len(prefixes):
        # extend the block with extra continuation lines (col 6 char: 2,3,...9)
        while len(prefixes) < len(wrapped):
            last = prefixes[-1]
            ch = last[5]
            if ch == " ":
                ch = "1"
            if not (ch.isdigit() and ch < "9"):
                break
            prefixes.append(last[:5] + chr(ord(ch) + 1) + last[6:9])
        if len(wrapped) > len(prefixes):
            problems.append((start, "-", "-", "PREFIX", f"needs {len(wrapped)} lines, has {len(prefixes)}", merged[:60]))
            continue
        added.append((start, len(bl), len(wrapped)))
    newblock = []
    for k in range(len(prefixes)):
        text = wrapped[k] if k < len(wrapped) else ""
        new = prefixes[k] + text
        if len(new) > 80:
            problems.append((start, "-", "-", "OVERFLOW", f"line {bl[0] + k} len {len(new)}", new[:90]))
        newblock.append(new + " " * (80 - len(new)))
    emits[bl[0]] = newblock

print(f"problem blocks: {len(problems)}")
for p in problems:
    print("  !!", p)

# ---- write plan + simulated file -------------------------------------------
consumed = set()          # block lines that must be skipped (continuations)
for b0 in emits:
    for b in block_lines(b0)[1:]:
        consumed.add(b)

sim, plan = [], []
changed_lines = 0
for i, l in enumerate(lines):
    n = i + 1
    if n in emits:
        newblock = emits[n]
        if newblock == [l]:
            sim.append(l)
            continue
        changed_lines += len(newblock)
        oldtxt = "\n".join(x.rstrip() for x in [l] + [lines[b - 1] for b in block_lines(n)][1:])
        newtxt = "\n".join(newblock)
        plan.append(f"### block at line {n}\nOLD:\n{oldtxt}\nNEW:\n{newtxt}")
        sim.extend(newblock)
    elif n in consumed:
        continue
    else:
        sim.append(l)

(TMP / "edits.txt").write_text("\n".join(plan), encoding="utf-8")
(TMP / "simulated.ens").write_bytes("\r\n".join(sim).encode("ascii"))
print(f"changed lines: {changed_lines}; wrote edits.txt, simulated.ens")
print(f"blocks needing an added continuation line: {added}")
