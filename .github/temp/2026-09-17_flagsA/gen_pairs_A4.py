"""Generate exact, fail-safe edit pairs for the Flag A revision.

Rules implemented:
  R1: L-record flag A removed when the level has no Jpi (XREF irrelevant).
  R2: G-record flag A added when RI comes from 30Si(alpha,g),(a,n):
      - all G-records of pure-L levels (XREF == 'L')
      - mixed-L levels with explicit RI-origin evidence (hardcoded list).

Every pair: old = full line + "\n" + next-line-prefix (24 chars);
            new = modified line + "\n" + same prefix.
A mistyped space run can never match -> fail-safe.
READ-ONLY (writes only the pairs report under .github/temp).
"""
import json
import re

P = r"A34/S34/new/S34_adopted.ens"
raw = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")

def field(ln, a, b):
    return ln[a - 1:b].rstrip()

levels = []
cur = None
for i, ln in enumerate(lines):
    if len(ln) < 8:
        continue
    if ln[6] == "c":
        continue
    cont, typ = ln[5], ln[7]
    if typ == "L" and cont == " ":
        cur = {"idx": i + 1, "E": field(ln, 10, 19), "J": field(ln, 23, 39),
               "flag": ln[76], "xref": "", "gs": []}
        levels.append(cur)
    elif typ == "L" and cont == "X" and cur is not None:
        m = re.search(r"XREF=(\S+)", ln)
        if m:
            cur["xref"] = m.group(1)
    elif typ == "G" and cont == " " and cur is not None:
        cur["gs"].append({"idx": i + 1, "E": field(ln, 10, 19), "flag": ln[76]})

# ---------- R1: L removals ----------
removals = [(r["idx"], r["E"]) for r in levels if r["flag"] == "A" and not r["J"].strip()]

# ---------- R2: G adds ----------
adds = []  # (level_idx, level_E, g_idx, g_E, why)
for r in levels:
    if r["xref"] == "L":
        for g in r["gs"]:
            if g["flag"] == " ":
                adds.append((r["idx"], r["E"], g["idx"], g["E"], "pure-L"))

MIXED = {  # level energy -> {gamma energies}
    "10311.53": {"8188", "10315"},
    "10790": {"7486", "8662", "10784"},
    "10840.63": {"748.43", "6152.1", "8718"},
    "11024.95": {"7720", "8896", "11023"},
}
for r in levels:
    for lE, ges in MIXED.items():
        if r["E"] == lE:
            assert "L" in r["xref"], lE
            for g in r["gs"]:
                if g["E"] in ges:
                    assert g["flag"] == " ", (lE, g)
                    adds.append((r["idx"], r["E"], g["idx"], g["E"], "mixed-evidence"))
probs = []
for lE, ges in MIXED.items():
    found = {g["E"] for r in levels if r["E"] == lE for g in r["gs"]}
    missing = ges - found
    if missing:
        probs.append(f"mixed level {lE}: gamma(s) not found: {missing}")

def mk_edit(idx, mode):
    ln = lines[idx - 1]
    nxt = lines[idx] if idx < len(lines) else ""
    suffix = nxt[:24]
    old = ln + "\n" + suffix
    if mode == "remove":
        new_ln = ln[:76] + " " + ln[77:]
    else:
        new_ln = ln[:76] + "A" + ln[77:]
    new = new_ln + "\n" + suffix
    return old, new

report = []
report.append(f"R1 removals: {len(removals)}  |  R2 adds: {len(adds)}")
for idx, E in removals:
    old, new = mk_edit(idx, "remove")
    c_old, c_new = raw.count(old), raw.count(new)
    report.append(f"\n[R1] line {idx} level {E} old-count={c_old} new-count={c_new}")
    report.append(f"OLD>>>{old}")
    report.append(f"NEW>>>{new}")

for li, lE, gi, gE, why in adds:
    old, new = mk_edit(gi, "add")
    c_old, c_new = raw.count(old), raw.count(new)
    report.append(f"\n[R2-{why}] line {gi} level {lE} g={gE} old-count={c_old} new-count={c_new}")
    report.append(f"OLD>>>{old}")
    report.append(f"NEW>>>{new}")

if probs:
    report.append("\nPROBLEMS: " + "; ".join(probs))

out = "\n".join(report)
open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", "w", encoding="utf-8").write(out)
print(out[:1500])
print(f"\n... total pairs written: {len(removals) + len(adds)}")
