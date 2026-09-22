"""Near-degenerate adopted levels: correct ENSDF uncertainty semantics.

DE digits are in units of the last digit of E (e.g. 6251.22 with DE=19 -> +-0.19 keV).
"""
import re
from pathlib import Path

TARGET = Path(r"D:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").split("\n")

levels = []
for i, ln in enumerate(lines, start=1):
    if len(ln) < 20 or ln[5] != " " or ln[6] != " " or ln[7] != "L":
        continue
    e_str = ln[9:19].strip()
    if not re.fullmatch(r"\d+(?:\.\d+)?", e_str):
        continue
    de_str = ln[19:21].strip()
    dec = len(e_str.split(".")[1]) if "." in e_str else 0
    sig = None
    if de_str.isdigit():
        sig = int(de_str) * 10 ** (-dec)
    levels.append(dict(line=i, e=float(e_str), e_str=e_str, de_str=de_str,
                       sig=sig, dec=dec, jpi=ln[21:39].strip(),
                       t=ln[39:49].strip(), gammas=[], xref=""))

bymap = {lv["line"]: lv for lv in levels}
cur = None
for i, ln in enumerate(lines, start=1):
    if len(ln) < 10 or ln[6] != " ":
        continue
    cont, typ = ln[5], ln[7]
    if cont == " " and typ == "L":
        cur = bymap.get(i)
        continue
    if cur is None:
        continue
    if cont == " " and typ == "G":
        cur["gammas"].append(ln.rstrip())
    elif typ == "L" and "XREF=" in ln:
        m = re.search(r"XREF=(\S*)", ln)
        if m:
            cur["xref"] = m.group(1)

def letters(s):
    return set(re.findall(r"[A-Za-z]", s))

def fmt(x, w=8):
    return f"{x:{w}.3f}" if x is not None else f"{'-':>{w}}"

pairs = []
for a, b in zip(levels, levels[1:]):
    d = b["e"] - a["e"]
    sig = None
    if a["sig"] is not None and b["sig"] is not None:
        sig = (a["sig"] ** 2 + b["sig"] ** 2) ** 0.5
    nsig = d / sig if sig else None
    pairs.append((d, sig, nsig, a, b))

out = []
out.append(f"levels: {len(levels)}   file lines: {len(lines)}")
out.append("DE interpreted as last-digit units of E (ENSDF convention).")
out.append("")
out.append("=== pairs with dE < 2 keV (sorted by dE) ===")
out.append(f"{'E1':>10} {'DE1':>8} {'E2':>10} {'DE2':>8} {'dE':>7} "
           f"{'sig':>8} {'n.sig':>6}  {'Jpi1':<12} {'Jpi2':<12} "
           f"{'ng':>3}/{'':<3} {'shared':<10} lines")
for d, sig, nsig, a, b in sorted(pairs, key=lambda r: r[0]):
    if d >= 2:
        break
    shared = ",".join(sorted(letters(a["xref"]) & letters(b["xref"])))
    out.append(
        f"{a['e_str']:>10} {fmt(a['sig'])} {b['e_str']:>10} {fmt(b['sig'])} "
        f"{d:7.3f} {fmt(sig)} {fmt(nsig, 6)}  {a['jpi']:<12} {b['jpi']:<12} "
        f"{len(a['gammas']):>3}/{len(b['gammas']):<3} {shared:<10} "
        f"{a['line']},{b['line']}")

out.append("")
out.append("=== A) energies AGREE within uncertainty (dE < sig) ===")
A = [r for r in pairs if r[2] is not None and r[2] < 1]
for d, sig, nsig, a, b in sorted(A, key=lambda r: r[0]):
    shared = ",".join(sorted(letters(a["xref"]) & letters(b["xref"])))
    out.append(f"dE={d:7.3f} sig={sig:8.3f} {nsig:5.2f}sig | "
               f"{a['e_str']}({a['jpi']})[{a['xref']}] vs "
               f"{b['e_str']}({b['jpi']})[{b['xref']}] | shared={shared or '-'}"
               f" | ng {len(a['gammas'])}/{len(b['gammas'])} | "
               f"L{a['line']},L{b['line']}")
out.append(f"count: {len(A)}")

out.append("")
out.append("=== B) subset of A with NO dataset reporting both (merge candidates) ===")
B = [r for r in A if not (letters(r[3]["xref"]) & letters(r[4]["xref"]))]
for d, sig, nsig, a, b in sorted(B, key=lambda r: r[0]):
    out.append(f"dE={d:7.3f} sig={sig:8.3f} {nsig:5.2f}sig | "
               f"{a['e_str']}({a['jpi']}) T={a['t'] or '-'} [{a['xref']}] vs "
               f"{b['e_str']}({b['jpi']}) T={b['t'] or '-'} [{b['xref']}] | "
               f"L{a['line']},L{b['line']}")
out.append(f"count: {len(B)}")

out.append("")
out.append("=== C) pairs with dE < 1 keV (any sigma) ===")
for d, sig, nsig, a, b in sorted(pairs, key=lambda r: r[0]):
    if d >= 1:
        break
    shared = ",".join(sorted(letters(a["xref"]) & letters(b["xref"])))
    out.append(f"dE={d:7.3f} sig={fmt(sig)} {a['e_str']}({a['jpi']}) "
               f"[{a['xref']}] vs {b['e_str']}({b['jpi']}) [{b['xref']}] "
               f"shared={shared or '-'} L{a['line']},L{b['line']}")

out.append("")
out.append("=== D) all pairs with dE < 10 keV and dE > sig (resolved) ===")
for d, sig, nsig, a, b in sorted(pairs, key=lambda r: r[0]):
    if d >= 10:
        break
    if sig is None or nsig >= 1:
        out.append(f"dE={d:7.3f} sig={fmt(sig)} {fmt(nsig, 6)}sig "
                   f"{a['e_str']}({a['jpi']}) vs {b['e_str']}({b['jpi']}) "
                   f"L{a['line']},L{b['line']}")

Path(r"D:\X\ND\ENSDF\.github\temp\close_levels\report2.txt").write_text(
    "\n".join(out) + "\n", encoding="utf-8")
print("written, sections:", len(out))
