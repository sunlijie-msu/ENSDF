"""Plan + simulate comment-quoted-value revisions for S34_adopted.ens.

Prints, for every checker finding: nearest candidate records, the proposed
replacement op, and the resulting OLD/NEW comment blocks (exact 80-col text).
Also simulates the revised file and re-runs the checker pipeline on it.
"""
import importlib.util
import re
from pathlib import Path

ROOT = Path(r"D:\X\ND\ENSDF")
spec = importlib.util.spec_from_file_location(
    "cq", ROOT / ".github" / "scripts" / "check_quoted_values.py")
cq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cq)

TARGET = ROOT / "A34" / "S34" / "new" / "S34_adopted.ens"
WIDTH = 71          # text columns 10-80
WINDOW = 1.0

raw = TARGET.read_text(encoding="utf-8")
lines = raw.split("\n")
if lines and lines[-1] == "":
    lines = lines[:-1]

levels = cq.parse_levels(TARGET)
gammas = cq.parse_gammas(TARGET)
refs = cq.extract_quoted_refs(TARGET)
findings = cq.verify(refs, levels, gammas, WINDOW)

# --- manual decisions ------------------------------------------------------
# (line, quoted, kind) -> replacement text
OVERRIDE = {}

FIX_ARTICLE = True  # strip leading article in parse_target (script fix)


def text_of(line: str) -> str:
    return line[9:80] if len(line) >= 80 else line[9:]


def block_of(ln1: int):
    """Return (start_idx, end_idx, [line strings]) of the cL J$ block."""
    i = ln1 - 1
    j = i
    while j >= 0:
        l = lines[j]
        if len(l) >= 9 and l[6] == 'c' and l[7] == 'L':
            if l[5] == ' ':
                if 'J$' in l[9:]:
                    start = j
                    break
                return None
        j -= 1
    else:
        return None
    k = start + 1
    while k < len(lines) and len(lines[k]) >= 9 and lines[k][6] == 'c' \
            and lines[k][7] == 'L' and lines[k][5] != ' ':
        k += 1
    return (start, k - 1, lines[start:k])


def parent_level_of(ln1: int):
    """Energy string of the L-record owning this comment block."""
    for j in range(ln1 - 1, -1, -1):
        l = lines[j]
        if len(l) >= 10 and l[5] == ' ' and l[6] == ' ' and l[7] == 'L':
            return l[9:19].strip()
    return None


def near_gammas(e, n=3, win=5.0):
    cand = [g for g in gammas if abs(g.energy - e) <= win]
    cand.sort(key=lambda g: abs(g.energy - e))
    return cand[:n]


def near_levels(e, n=3, win=20.0):
    cand = [lv for lv in levels.values() if abs(lv.energy - e) <= win]
    cand.sort(key=lambda lv: abs(lv.energy - e))
    return cand[:n]


def ops_for(f):
    """Return list of (regex, repl) for one finding, or [] if unresolved."""
    if f.code == 'GAMMA_ENERGY_MISMATCH':
        return [(re.escape(f.quoted) + r'\|g', f.actual + '|g')]
    if f.code == 'LEVEL_ENERGY_MISMATCH':
        return [(r'(?<![\d.])' + re.escape(f.quoted) + r'(?![\d.])', f.actual)]
    if f.code == 'MULTIPOLARITY_MISMATCH':
        return [(r'(\|g\s*,\s*)' + re.escape(f.quoted) + r'(\s*,)',
                 r'\g<1>' + f.actual + r'\g<2>')]
    if f.code == 'JPI_MISMATCH':
        key = (f.line, f.quoted, 'jpi')
        if key in OVERRIDE:
            return [(re.escape(f.quoted), OVERRIDE[key])]
        if f.quoted.startswith('the '):
            return []
        return [(re.escape(f.quoted), f.actual)]
    key = (f.line, f.quoted, f.code)
    if key in OVERRIDE:
        rep = OVERRIDE[key]
        if f.code == 'GAMMA_NOT_FOUND':
            return [(re.escape(f.quoted) + r'\|g', rep + '|g')]
        return [(r'(?<![\d.])' + re.escape(f.quoted) + r'(?![\d.])', rep)]
    return []


out = []
out.append(f"levels={len(levels)} gammas={len(gammas)} refs={len(refs)} "
           f"findings={len(findings)}")

# --- report findings with candidates --------------------------------------
by_line = {}
for f in findings:
    by_line.setdefault(f.line, []).append(f)

for ln in sorted(by_line):
    blk = block_of(ln)
    pl = parent_level_of(ln)
    out.append("")
    out.append(f"=== line {ln}  block={blk[0]+1 if blk else '?'}"
               f"  parent_level={pl}")
    for f in by_line[ln]:
        out.append(f"  [{f.code}] quoted={f.quoted!r} actual={f.actual!r}")
        out.append(f"     ctx: {f.context}")
        if f.code == 'GAMMA_NOT_FOUND':
            for g in near_gammas(float(f.quoted)):
                out.append(f"     Gcand: E={g.energy_str} M={g.multipolarity!r}"
                           f" parent={g.parent_energy} line {g.line_num}")
        if f.code == 'LEVEL_NOT_FOUND':
            for lv in near_levels(float(f.quoted)):
                out.append(f"     Lcand: E={lv.energy_str} J={lv.jpi!r}"
                           f" line {lv.line_num}")

# --- apply ops to blocks, simulate ---------------------------------------
block_ops = {}
for ln in sorted(by_line):
    blk = block_of(ln)
    if blk is None:
        out.append(f"!! no block for line {ln}")
        continue
    ops = []
    for f in by_line[ln]:
        ops.extend(ops_for(f))
    block_ops[blk[0]] = ops

new_lines = list(lines)
shift = 0
plan_old_new = []
for start in sorted(block_ops, reverse=True):
    blk = None
    # recompute block for original index
    k = start
    while k < len(lines) and len(lines[k]) >= 9 and lines[k][6] == 'c' \
            and lines[k][7] == 'L':
        k += 1
    end = k - 1
    pref = [l[:9] for l in lines[start:end + 1]]
    parts = [text_of(l).rstrip() for l in lines[start:end + 1]]
    ops = block_ops[start]
    new_parts = []
    for p in parts:
        np_ = p
        for rx, rep in ops:
            np_ = re.sub(rx, rep, np_)
        new_parts.append(np_)
    if all(len(p) <= WIDTH for p in new_parts):
        final = new_parts
    else:
        joined = ' '.join(new_parts)
        words = joined.split(' ')
        final = []
        cur = ''
        for w in words:
            if not cur:
                cur = w
            elif len(cur) + 1 + len(w) <= WIDTH:
                cur += ' ' + w
            else:
                final.append(cur)
                cur = w
        final.append(cur)
    newblock = [pref[i] + final[i].ljust(WIDTH)
                for i in range(len(final))]
    plan_old_new.append((start, lines[start:end + 1], newblock))
    new_lines[start + shift:end + 1 + shift] = newblock
    shift += len(newblock) - (end - start + 1)

tmp = ROOT / ".github" / "temp" / "quoted_check" / "simulated.ens"
tmp.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
s_levels = cq.parse_levels(tmp)
s_gammas = cq.parse_gammas(tmp)
s_refs = cq.extract_quoted_refs(tmp)
s_find = cq.verify(s_refs, s_levels, s_gammas, WINDOW)

out.append("")
out.append(f"### SIMULATION: refs={len(s_refs)} findings={len(s_find)}")
for f in s_find:
    out.append(f"  REMAIN [{f.code}] line {f.line} quoted={f.quoted!r} "
               f"actual={f.actual!r} ctx={f.context}")

# --- energy conservation advisory ---------------------------------------
out.append("")
out.append("### ENERGY CONSERVATION (advisory, parent of block vs ref)")
for start, old, new in sorted(plan_old_new):
    pl = parent_level_of(start + 1)
    if pl is None:
        continue
    try:
        pe = float(pl)
    except ValueError:
        continue
    for rx, rep in block_ops[start]:
        pass
    txt = ' '.join(text_of(l) for l in new)
    for m in re.finditer(r'(\d+(?:\.\d+)?)\|g(?:\(\|q\))?', txt):
        ge = float(m.group(1))
        span = txt[m.end():]
        dm = re.search(r'\b(to|from)\b', span)
        if not dm:
            continue
        tgt = cq._parse_j_block([span[dm.end():]], 0)
        if not tgt:
            continue
        lv = tgt[0].level_energy
        if lv is None:
            continue
        diff = (pe - ge - lv) if dm.group(1) == 'to' else (ge - (pe - lv))
        flag = '  <== CHECK' if abs(diff) > 2.0 else ''
        out.append(f"  line {start+1} parent={pl} {m.group(1)}|g "
                   f"{dm.group(1)} {tgt[0].level_energy_str} -> resid "
                   f"{diff:+.2f}{flag}")

# --- print OLD/NEW blocks ------------------------------------------------
out.append("")
out.append("### BLOCK REWRITES (exact text incl. trailing spaces)")
for start, old, new in sorted(plan_old_new):
    out.append(f"--- block at line {start+1} "
               f"({len(old)} -> {len(new)} lines)")
    for l in old:
        out.append(f"OLD<{l}>")
    for l in new:
        out.append(f"NEW<{l}>")

(ROOT / ".github" / "temp" / "quoted_check" / "plan.txt").write_text(
    "\n".join(out), encoding="utf-8")
print(f"findings={len(findings)} blocks={len(plan_old_new)} "
      f"remaining={len(s_find)}")
