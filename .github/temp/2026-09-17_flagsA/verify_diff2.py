"""List every diff pair in the adopted file with classification, align by cols 1-20."""
import subprocess

OUT = subprocess.run(
    ["git", "diff", "--no-color", "-U0", "--", "A34/S34/new/S34_adopted.ens"],
    capture_output=True, text=True, encoding="utf-8")
lines = OUT.stdout.replace("\r\n", "\n").split("\n")

hunks, minus, plus = [], [], []
def flush():
    global minus, plus
    if minus or plus:
        hunks.append((minus, plus))
    minus, plus = [], []

for ln in lines:
    if ln.startswith("---") or ln.startswith("+++"):
        continue
    if ln.startswith("@@"):
        flush()
    elif ln.startswith("-"):
        minus.append(ln[1:])
    elif ln.startswith("+"):
        plus.append(ln[1:])
flush()

kinds = {}
allpairs, orphan_m, orphan_p = [], [], []
for minus, plus in hunks:
    mlist = list(minus)
    for p in plus:
        key = p[:20]
        hit = next((m for m in mlist if m[:20] == key), None)
        if hit is not None:
            mlist.remove(hit)
            allpairs.append((hit, p))
        else:
            orphan_p.append(p)
    orphan_m += mlist

for o, n in allpairs:
    co, cn = "".join(o.split()), "".join(n.split())
    if co == cn:
        kind = "shift"
    elif cn == co + "A":
        kind = "add-A"
    elif cn == co + "E":
        kind = "add-E"
    else:
        kind = "OTHER"
    kinds[kind] = kinds.get(kind, 0) + 1
    if kind == "OTHER":
        print(f"OTHER: {o!r} -> {n!r}")

print(f"\npairs: {len(allpairs)} | kinds: {kinds}")
print(f"orphan-minus: {len(orphan_m)}")
for o in orphan_m:
    print(f"  M: {o!r}")
print(f"orphan-plus: {len(orphan_p)}")
for n in orphan_p:
    print(f"  P: {n!r}")
