"""Verify every +/- pair in the adopted-file diff is flag-only (inserted A/E or A-position shift)."""
import subprocess

OUT = subprocess.run(
    ["git", "diff", "--no-color", "-U0", "--", "A34/S34/new/S34_adopted.ens"],
    capture_output=True, text=True, encoding="utf-8")
lines = OUT.stdout.replace("\r\n", "\n").split("\n")

minus, plus, pairs, issues, orphan_minus, orphan_plus = [], [], [], [], [], []
for ln in lines:
    if ln.startswith("---") or ln.startswith("+++"):
        continue
    if ln.startswith("-"):
        minus.append(ln[1:])
    elif ln.startswith("+"):
        plus.append(ln[1:])
    elif ln.startswith("@@"):
        if minus or plus:
            # flush previous hunk as pair list
            if len(minus) == len(plus):
                for o, n in zip(minus, plus):
                    pairs += [(o, n)]
            else:
                orphan_minus += minus[len(plus):] if len(minus) > len(plus) else []
                orphan_plus += plus[len(minus):] if len(plus) > len(minus) else []
                for o, n in zip(minus, plus):
                    pairs += [(o, n)]
            minus, plus = [], []
if minus or plus:
    if len(minus) == len(plus):
        pairs += list(zip(minus, plus))
    else:
        orphan_minus += minus[len(plus):] if len(minus) > len(plus) else []
        orphan_plus += plus[len(minus):] if len(plus) > len(minus) else []
        for o, n in zip(minus, plus):
            pairs += [(o, n)]

print(f"pair count: {len(pairs)} | orphan minus: {len(orphan_minus)} | orphan plus: {len(orphan_plus)}")
for o, n in pairs:
    co, cn = "".join(o.split()), "".join(n.split())
    if co == cn:
        kind = "fix/shift"
    elif cn == co + "A" or cn == co + "E":
        kind = "insert-" + cn[-1]
    else:
        kind = "!!! OTHER"
        issues.append((o, n))
    tag = o[9:19].strip()
    if kind == "!!! OTHER":
        print(f"{kind} | {o!r} -> {n!r}")
for o in orphan_minus:
    print(f"orphan-minus: {o!r}")
for n in orphan_plus:
    print(f"orphan-plus: {n!r}")
print(f"non-flag issues: {len(issues)}")
