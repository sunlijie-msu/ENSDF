import re

TMP = r"d:\X\ND\ENSDF\.github\temp\quoted_check"
rules = {}
# rebuild rule list by re-running planner logic is complex; instead diff OLD vs NEW per block
plan = open(TMP + r"\edits.txt", encoding="utf-8").read()
blocks = re.split(r"### block at line (\d+)\nOLD:\n", plan)[1:]
out = []
for i in range(0, len(blocks), 2):
    ln = int(blocks[i])
    body = blocks[i + 1]
    old, new = body.split("\nNEW:\n")
    oldl = old.split("\n")
    newl = new.split("\n")
    out.append(f"== block {ln} ({len(oldl)} lines -> {len(newl)} lines)")
    for a in oldl:
        out.append("  OLD|" + a)
    for b in newl:
        pad = len(b) - len(b.rstrip())
        out.append(f"  NEW|{b.rstrip()}|pad={pad}")
open(TMP + r"\review.txt", "w", encoding="utf-8").write("\n".join(out))
print("blocks:", len(blocks) // 2, "-> review.txt lines:", len(out))
