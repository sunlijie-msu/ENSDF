"""Correct inventory: XREF lines have cont='X', type='L'. READ-ONLY."""
import re

P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

def field(ln, a, b):
    return ln[a - 1:b].rstrip()

levels = []
cur = None
for i, ln in enumerate(lines):
    if len(ln) < 8:
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
        cur["gs"].append({"idx": i + 1, "E": field(ln, 10, 19),
                          "RI": field(ln, 23, 29), "flag": ln[76]})

print("=== ALL L-records flag=A ===")
for r in levels:
    if r["flag"] == "A":
        print(f"line {r['idx']:5d} E={r['E']:10s} J='{r['J']:12s}' A  XREF={r['xref']}")

print("\n=== Levels with L in XREF ===")
for r in levels:
    if "L" not in r["xref"]:
        continue
    gs = " | ".join(f"{g['E']}[{g['flag'].strip() or '-'}]" for g in r["gs"])
    print(f"L {r['idx']:5d} E={r['E']:10s} J='{r['J']:12s}' Lflag={r['flag']}  XREF={r['xref'][:46]}")
    if gs:
        print(f"      Gs: {gs[:150]}")

print("\n=== G-records with flag A (file-wide) ===")
for r in levels:
    for g in r["gs"]:
        if g["flag"] == "A":
            print(f"line {g['idx']:5d} G E={g['E']:9s} RI={g['RI']:7s} A  [parent L {r['idx']} E={r['E']} J='{r['J'].strip()}']")
