"""Generate + simulate the final edit operations in memory.

R1 (9 lines): remove A.  op1: C+run -> C+run+'@' ; op2: '@A   \nSUF' -> '    \nSUF'
R2 (54 lines): add A.    op1: C2+run -> C2+run+'@' ; op2: '@    \nSUF' -> 'A   \nSUF'
SUF = next line prefix truncated at a non-space boundary.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
text = raw

lines = text.split("\n")

def find_line(prefix):
    hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

def suf_of(idx):
    nxt = lines[idx + 1]
    s = nxt[:24]
    s = s.rstrip() or nxt[:24]
    return s

R1_LEVELS = ["10447", "10528", "10617", "10869", "10895", "10917", "11180", "11194", "11289"]
ops = []
for lev in R1_LEVELS:
    i = find_line(" 34S   L " + lev)
    ln = lines[i]
    assert ln[76] == "A" and len(ln) == 80, (lev, ln[76], len(ln))
    C = ln[:76].rstrip()
    assert len(C) == 20, (lev, len(C))
    run = 76 - len(C)
    suf = suf_of(i)
    old1 = C + " " * run
    new1 = old1 + "@"
    old2 = "@A   \n" + suf
    new2 = "    \n" + suf
    ops.append((i + 1, old1, new1, old2, new2))

# R2 from the pairs file, excluding the 4 lines the user already did
skip = {" 34S   G 8279 ", " 34S   G 10406 ", " 34S   G 7142 ", " 34S   G 6407 "}
pairs = open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", encoding="utf-8").read()
r2_targets = []
for m in re.finditer(r"\[R2-(\S+)\] line (\d+) level (\S+) g=(\S+)", pairs):
    kind, _, lev, g = m.groups()
    r2_targets.append((lev, g, kind))

count_r1 = len(ops)
added = []
for lev, g, kind in r2_targets:
    # find the G line by energy within the level: locate by unique content start
    pat = re.compile(rf"^ 34S   G {re.escape(g)}\s")
    hits = [k for k, ln in enumerate(lines) if pat.match(ln)]
    assert len(hits) == 1, (lev, g, len(hits))
    i = hits[0]
    ln = lines[i]
    if ln[76] == "A":
        continue
    if any(ln.startswith(s) for s in skip):
        continue
    assert ln[76] == " " and len(ln) == 80, (lev, g, repr(ln[:30]), ln[76], len(ln))
    C2 = ln[:76].rstrip()
    run = 76 - len(C2)
    suf = suf_of(i)
    old1 = C2 + " " * run
    new1 = old1 + "@"
    old2 = "@    \n" + suf
    new2 = "A   \n" + suf
    assert text.count(old1) >= 1
    ops.append((i + 1, old1, new1, old2, new2))
    added.append((lev, g))

print(f"R1 ops: {count_r1} lines | R2 ops: {len(added)} lines | total lines: {len(ops)} ops calls: {len(ops)*2}")

# ---------- simulate sequentially ----------
sim = text
for (idx, old1, new1, old2, new2) in ops:
    c1 = sim.count(old1)
    if c1 != 1:
        print("SIM FAIL op1 count", c1, "line", idx, repr(old1[:40]), "len", len(old1))
        break
    sim = sim.replace(old1, new1, 1)
    c2 = sim.count(old2)
    if c2 != 1:
        print("SIM FAIL op2 count", c2, "line", idx, repr(old2[:40]))
        break
    sim = sim.replace(old2, new2, 1)
else:
    print("SIMULATION: ALL", len(ops) * 2, "ops applied cleanly")
    print("@ remaining:", sim.count("@"))
    for (idx, old1, *_) in ops:
        ln = sim.split("\n")[idx - 1]
        if len(ln) != 80 or ln[76] not in " A":
            print("POST-BAD", idx, len(ln), repr(ln[:60]))
    print("post-check done")
