"""Current-state inventory for Flag A revision:
- All L-records: energy, Jpi, col-77 flag, XREF of the level.
- All G-records of levels with 'L' in XREF: energy, RI, col-77 flag.
READ-ONLY.
"""
import re

P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

def field(ln, a, b):
    return ln[a - 1:b].rstrip()

records = []   # (idx, kind, dict)
cur_level = None
for i, ln in enumerate(lines):
    if len(ln) < 8:
        continue
    cont = ln[5]
    typ = ln[7]
    if typ == "L":
        cur_level = {
            "idx": i + 1, "E": field(ln, 10, 19), "J": field(ln, 23, 39),
            "flag": ln[76] if len(ln) > 76 else " ", "xref": "", "gs": [],
        }
        records.append(cur_level)
    elif typ == "X" and cur_level is not None and ln[7] == "X":
        m = re.match(r"\s*\S+\s*X\s+L\s+XREF=(\S+)", ln)
        if m and not cur_level["xref"]:
            cur_level["xref"] = m.group(1)
    elif typ == "G" and cur_level is not None:
        g = {
            "idx": i + 1, "E": field(ln, 10, 19), "RI": field(ln, 23, 29),
            "flag": ln[76] if len(ln) > 76 else " ",
        }
        cur_level["gs"].append(g)

G, L = "\u03b3", "\u03c0"
print("=== L-records with flag A (col77), whole file ===")
for r in records:
    if r["flag"] == "A":
        print(f"line {r['idx']:5d}  E={r['E']:9s} J='{r['J']:12s}' flag={r['flag']}  XREF={r['xref']}")

print("\n=== Levels with L in XREF: L-record flag + G-record flags ===")
n_missing_g = 0
for r in records:
    if "L" not in r["xref"]:
        continue
    gsum = ", ".join(f"{g['E']}({g['flag'].strip() or '-'})" for g in r["gs"][:12])
    print(f"L {r['idx']:5d} E={r['E']:10s} J='{r['J']:12s}' Lflag={r['flag']}  XREF={r['xref'][:44]}")
    if r["gs"]:
        print(f"          Gs: {gsum}")

print("\n=== All G-records with flag A (whole file, for reference) ===")
cnt = 0
for r in records:
    for g in r["gs"]:
        if g["flag"] == "A":
            cnt += 1
print("total A-flagged G-records:", cnt)
