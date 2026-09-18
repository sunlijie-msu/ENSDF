"""Print final op pairs (both ops per line) to a copy file + console summary."""
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")

def find_line(prefix):
    hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    return hits[0]

def suf_of(idx):
    return (lines[idx + 1][:24].rstrip() or lines[idx + 1][:24])

R1_LEVELS = ["10447", "10528", "10617", "10869", "10895", "10917", "11180", "11194", "11289"]
out = []
out.append("# R1: remove A (op1 inserts @, op2 cleans)")
for lev in R1_LEVELS:
    i = find_line(" 34S   L " + lev)
    ln = lines[i]
    C = ln[:76].rstrip()
    run = 76 - len(C)
    suf = suf_of(i)
    out.append(f"[R1 {lev}] line {i+1}")
    out.append("OP1_OLD>>>" + C + " " * run)
    out.append("OP1_NEW>>>" + C + " " * run + "@")
    out.append(f"OP2_OLD>>>@A   \n{suf}")
    out.append(f"OP2_NEW>>>    \n{suf}")

skip = {" 34S   G 8279", " 34S   G 10406", " 34S   G 7142", " 34S   G 6407"}
pairs = open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", encoding="utf-8").read()
out.append("\n# R2: add A")
n = 0
for m in re.finditer(r"\[R2-(\S+)\] line (\d+) level (\S+) g=(\S+)", pairs):
    kind, _, lev, g = m.groups()
    pat = re.compile(rf"^ 34S   G {re.escape(g)}\s")
    hits = [k for k, ln in enumerate(lines) if pat.match(ln)]
    assert len(hits) == 1
    i = hits[0]
    ln = lines[i]
    if ln[76] == "A" or any(ln.startswith(s) for s in skip):
        continue
    C2 = ln[:76].rstrip()
    run = 76 - len(C2)
    suf = suf_of(i)
    out.append(f"[R2 {lev} g={g}] line {i+1}")
    out.append("OP1_OLD>>>" + C2 + " " * run)
    out.append("OP1_NEW>>>" + C2 + " " * run + "@")
    out.append(f"OP2_OLD>>>@    \n{suf}")
    out.append(f"OP2_NEW>>>A   \n{suf}")
    n += 1

open(r".github/temp/2026-09-17_flagsA/final_ops.txt", "w", encoding="utf-8").write("\n".join(out))
print("R1 blocks: 9, R2 blocks:", n)
print("written final_ops.txt")
