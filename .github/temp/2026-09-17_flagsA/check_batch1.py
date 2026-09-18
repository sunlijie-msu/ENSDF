"""Validate MY batch-1 literals vs authoritative r2_ops.txt strings."""
import re

auth = open(r".github/temp/2026-09-17_flagsA\r2_ops.txt", encoding="utf-8").read()
A = {}
cur = None
for ln in auth.split("\n"):
    m = re.match(r"\[(\S+) g=(\S+)\] run=(\d+)", ln)
    if m:
        cur = (m.group(1), m.group(2))
        A[cur] = {}
    elif ln.startswith("O1>>>") and cur:
        A[cur]["O1"] = ln[5:]
    elif ln.startswith("O2>>>") and cur:
        A[cur]["O2"] = ln[5:]
    elif ln.startswith("N2>>>") and cur:
        A[cur]["N2"] = ln[5:]

# ---- MY typed literals (batch 1: 11 lines) ----
MY = {}
MY[("10587", "7282")] = dict(
    C2=" 34S   G 7282         100       (E1)", run=40)
MY[("10587", "8458")] = dict(C2=" 34S   G 8458         60", run=52)
MY[("10625", "8496")] = dict(C2=" 34S   G 8496         100", run=51)
MY[("10625", "10623")] = dict(C2=" 34S   G 10623        100       E1", run=42)
MY[("10768", "8639")] = dict(C2=" 34S   G 8639         100       M1+E2    +0.3", run=31)
MY[("10768", "10766")] = dict(C2=" 34S   G 10766        10     LT", run=45)
MY[("10931", "8802")] = dict(C2=" 34S   G 8802         100       E1+M2    +0.154  17", run=25)
MY[("10994", "8865")] = dict(C2=" 34S   G 8865         100       M1+E2    +0.078  32", run=25)
MY[("11088", "7783")] = dict(C2=" 34S   G 7783         47", run=52)
MY[("11088", "8959")] = dict(C2=" 34S   G 8959         44", run=52)
MY[("11088", "11086")] = dict(C2=" 34S   G 11086        100       E2", run=42)

bad = 0
for key, spec in MY.items():
    a = A[key]
    C2, run = spec["C2"], spec["run"]
    ok = (len(C2) == 76 - run)
    if not ok:
        bad += 1
        print(f"LEN MISMATCH {key}: len(C2)={len(C2)} expected {76 - run} (run={run})")
        continue
    for tag, want in (("O1", C2 + " " * run), ("O2", C2 + " " * run + "@"), ("N2", C2 + " " * run + "A")):
        if a[tag] != want:
            bad += 1
            print(f"MISMATCH {key} {tag}:")
            print(f"   auth: {a[tag]!r}")
            print(f"   mine: {want!r}")
print("bad:", bad, "of", len(MY) * 3, "strings")
