#!/usr/bin/env python3
from pathlib import Path
import re

p = Path(r"A34/Cl34/new/Cl34_27al_12c_ang.ens")
lines = p.read_text().splitlines()

records = []
current_level = None

def infer_from_dco(dco_q, dco_d):
    """
    Infer D/Q tendency from measured DCO only.
    Returns one of: D, Q, mixed-or-ambiguous, no-dco
    Rules from dataset header:
      D gate: ~1 => stretched dipole-like, ~2 => quadrupole/unstretched-dipole-like
      Q gate: ~0.5 => stretched dipole-like, ~1 => quadrupole/unstretched-dipole-like
    """
    if dco_q is None and dco_d is None:
        return "no-dco", "No measured DCO"

    votes = []
    notes = []

    if dco_d is not None:
        v, u = dco_d
        # Compare to 1.0 and 2.0 with uncertainty-aware soft classification
        z1 = abs(v - 1.0) / u if u > 0 else 999
        z2 = abs(v - 2.0) / u if u > 0 else 999
        if z1 <= 2.5 and z1 + 0.5 < z2:
            votes.append("D")
            notes.append(f"DCO(D)={v:.2f}±{u:.2f} closer to 1.0")
        elif z2 <= 2.5 and z2 + 0.5 < z1:
            votes.append("Q")
            notes.append(f"DCO(D)={v:.2f}±{u:.2f} closer to 2.0")
        else:
            votes.append("amb")
            notes.append(f"DCO(D)={v:.2f}±{u:.2f} ambiguous between 1.0 and 2.0")

    if dco_q is not None:
        v, u = dco_q
        # Compare to 0.5 and 1.0
        z05 = abs(v - 0.5) / u if u > 0 else 999
        z10 = abs(v - 1.0) / u if u > 0 else 999
        if z05 <= 2.5 and z05 + 0.5 < z10:
            votes.append("D")
            notes.append(f"DCO(Q)={v:.2f}±{u:.2f} closer to 0.5")
        elif z10 <= 2.5 and z10 + 0.5 < z05:
            votes.append("Q")
            notes.append(f"DCO(Q)={v:.2f}±{u:.2f} closer to 1.0")
        else:
            votes.append("amb")
            notes.append(f"DCO(Q)={v:.2f}±{u:.2f} ambiguous between 0.5 and 1.0")

    if all(v == "D" for v in votes):
        return "D", "; ".join(notes)
    if all(v == "Q" for v in votes):
        return "Q", "; ".join(notes)
    if "D" in votes and "Q" in votes:
        return "mixed-or-ambiguous", "; ".join(notes)
    return "mixed-or-ambiguous", "; ".join(notes)


def assigned_class(m):
    s = m.strip()
    if not s:
        return "none"
    if s.startswith("[") and s.endswith("]"):
        return "bracket"
    base = s.strip("[]()")
    # Keep this purely label-based (no Jpi/physics inference)
    if "D+Q" in base or "D(+Q)" in base or "Q(+D)" in base or "+" in base:
        # explicit mixed label or mixed E/M label
        if base in ("E1+M2", "M1+E2", "E1(+M2)", "M1(+E2)", "M2+E3", "M2(+E3)"):
            return "mixed"
        if "D" in base and "Q" in base:
            return "mixed"
        return "mixed"
    if base in ("D", "E1", "M1"):
        return "D"
    if base in ("Q", "E2", "M2"):
        return "Q"
    return "other"


def parse_dco(text, gate):
    m = re.search(rf"R\{{-DCO\}}\({gate}\)=([\d.]+)\s*\{{I(\d+)\}}", text)
    if not m:
        return None
    v_str, u_str = m.group(1), m.group(2)
    v = float(v_str)
    dec = len(v_str.split(".")[1]) if "." in v_str else 0
    u = int(u_str) * (10 ** (-dec))
    return v, u


for i, line in enumerate(lines):
    if line.startswith(" 34CL  L "):
        current_level = line[9:19].strip()
    if not line.startswith(" 34CL  G "):
        continue

    eg = line[9:19].strip()
    m = line[32:41].strip()
    if not m:
        continue

    # Gather attached comments
    block = []
    j = i + 1
    while j < len(lines):
        nl = lines[j]
        if nl.startswith(" 34CL  G ") or nl.startswith(" 34CL  L ") or nl.startswith(" 34CL d") or nl.startswith(" 34CL PN"):
            break
        block.append(nl)
        j += 1
    ctext = " ".join(block)

    has_pol = re.search(r"POL=([+-]?\d*\.?\d+)", ctext) is not None
    if has_pol:
        continue

    dco_q = parse_dco(ctext, "Q")
    dco_d = parse_dco(ctext, "D")

    acls = assigned_class(m)
    icls, inote = infer_from_dco(dco_q, dco_d)

    # Compatibility check using ONLY measured DCO vs assigned label class
    if acls == "bracket":
        compat = "N/A (bracketed)"
    elif icls == "no-dco":
        compat = "N/A (no DCO)"
    elif acls == "mixed":
        compat = "OK (mixed label accepts DCO ambiguity)"
    elif acls in ("D", "Q"):
        compat = "OK" if acls == icls else "FLAG"
    else:
        compat = "REVIEW"

    records.append({
        "line": i + 1,
        "level": current_level,
        "eg": eg,
        "M": m,
        "assigned": acls,
        "dco_q": dco_q,
        "dco_d": dco_d,
        "inferred": icls,
        "compat": compat,
        "note": inote,
    })

print("MEASUREMENT-ONLY RECHECK (NO J|p-BASED INFERENCE)")
print("M filter: assigned M present AND no POL")
print(f"count = {len(records)}")
print()

for r in records:
    dq = f"{r['dco_q'][0]:.2f}±{r['dco_q'][1]:.2f}" if r['dco_q'] else "-"
    dd = f"{r['dco_d'][0]:.2f}±{r['dco_d'][1]:.2f}" if r['dco_d'] else "-"
    print(f"line {r['line']:3d}  Ei={r['level']:<8} Eg={r['eg']:<7} M={r['M']:<9}  DCO(Q)={dq:<12} DCO(D)={dd:<12}")
    print(f"   assigned={r['assigned']:<8} inferred-from-DCO={r['inferred']:<18} result={r['compat']}")
    print(f"   note: {r['note']}")

flags = [r for r in records if r['compat'] == 'FLAG']
print()
print(f"FLAGS = {len(flags)}")
for f in flags:
    print(f"  line {f['line']}: Eg={f['eg']} M={f['M']} assigned={f['assigned']} inferred={f['inferred']}")
