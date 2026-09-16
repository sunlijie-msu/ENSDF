"""Dump each `2 L WIDTH*` record's level block comments and propose the replacement cL comment text."""
from pathlib import Path
import re

LINE = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

SYM = {
    "WIDTHN": "|G{-n}",
    "WIDTHG0": "|G{-|g0}",
    "WIDTHG": "|G{-|g}",
    "WIDTHA": "|G{-|a}",
    "WIDTHP": "|G{-p}",
    "WIDTH": "|G",
}


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


def parse(rec):
    """Return list of (symbol, value-string) for each field in the record."""
    body = rec[9:].strip()
    out = []
    for f in body.split("$"):
        f = f.strip()
        if not f:
            continue
        m = re.match(r"^(WIDTH\w*?)\s*(GT|LT|GE|LE|=)\s*(.+)$", f)
        if not m:
            out.append((f, "PARSE-ERROR"))
            continue
        key, op, rest = m.group(1), m.group(2), m.group(3).strip()
        sym = SYM.get(key, "|G?")
        parts = rest.split()
        val, unit = parts[0], (parts[1] if len(parts) > 1 else "")
        unc = parts[2] if len(parts) > 2 else ""
        if len(parts) > 3:
            out.append((key, "PARSE-ERROR:" + f))
            continue
        unit = {"ev": "eV", "kev": "keV", "mev": "MeV"}.get(unit.lower(), unit)
        s = f"{sym}{op if op in ('.',) else ''}"
        s = f"{sym}"
        if op == "GT":
            s += ">"
        elif op == "LT":
            s += "<"
        elif op == "GE":
            s += "|>"
        elif op == "LE":
            s += "|<"
        else:
            s += "="
        s += f"{val} {unit}".strip()
        if unc:
            s += f" {{I{unc}}}"
        out.append((key, s))
    return out


hits = [i for i, s in enumerate(LINE, 1) if s[7:8] == "L" and s[5:6] == "2" and "WIDTH" in s]
OUT = open(".github/temp/2026-09-16_widthg0/proposals.txt", "w", encoding="utf-8")

def P(*a):
    t = " ".join(str(x) for x in a)
    print(t)
    OUT.write(t + "\n")


P(f"data records = {len(hits)}\n")

for h in hits:
    p = next(j for j in range(h, 0, -1) if is_lrec(LINE[j - 1]))
    ls = LINE[p - 1]
    xr = ""
    for j in range(p + 1, len(LINE) + 1):
        if is_lrec(LINE[j - 1]) and j > p:
            break
        if LINE[j - 1][5:6] == "X" and "XREF" in LINE[j - 1]:
            xr = LINE[j - 1][14:].strip()
            break
    # full comment set of the level
    cl = []
    for j in range(p + 1, len(LINE) + 1):
        if is_lrec(LINE[j - 1]):
            break
        s = LINE[j - 1]
        if s[6:8] == "cL":
            cl.append((j, s.rstrip()))
    fields = parse(LINE[h - 1].rstrip())
    P(f"L{p} E={ls[9:19].strip():9s} J={ls[22:39].strip():9s} T={ls[39:49].strip():9s} XREF={xr}")
    P(f"   rec {h:5d}: {LINE[h-1].rstrip()!r}")
    for k, v in fields:
        P(f"      {k:8s} -> {v}")
    for j, c in cl:
        P(f"   cL {j:5d}: {c!r}")
    P("")

OUT.close()
