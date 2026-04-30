from pathlib import Path
import re

raw_path = Path(r"A34/Cl34/raw/2014BI03.md")
ens_path = Path(r"A34/Cl34/new/Cl34_27al_12c_ang.ens")

raw = raw_path.read_text(encoding="utf-8")
ens_lines = ens_path.read_text(encoding="utf-8").splitlines()


def parse_unc(value_str, unc_digits_str):
    value = float(value_str)
    dec = len(value_str.split(".")[1]) if "." in value_str else 0
    unc = int(unc_digits_str) * (10 ** (-dec))
    return value, unc


def m_class_from_ens(m):
    """Return D, Q, mixed, bracket, unknown based on ENS M field text only."""
    s = m.strip()
    if not s:
        return "unknown"
    if s.startswith("[") and s.endswith("]"):
        return "bracket"
    base = s.strip("[]")
    if "+" in base or "(" in base or ")" in base:
        return "mixed"
    if base in ("D", "E1", "M1"):
        return "D"
    if base in ("Q", "E2", "M2"):
        return "Q"
    return "unknown"


def lead_em_sign(m):
    """Return expected POL sign if leading explicit E/M exists; else None."""
    base = m.strip().strip("[]()").split("+")[0].strip()
    if base.startswith("E"):
        return "+"
    if base.startswith("M"):
        return "-"
    return None


# Parse source table rows
source_rows = []
for ln in raw.splitlines():
    if not ln.startswith("|"):
        continue
    if "E_\\gamma" in ln or ":---" in ln:
        continue
    parts = [p.strip() for p in ln.strip("|").split("|")]
    if len(parts) != 7:
        continue

    eg_s, ji, jf, dq_gate, dco_s, delta_s, pol_s = parts
    mdco = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\((\d+)\)", dco_s)
    if not mdco:
        continue

    dco_v, dco_u = parse_unc(mdco.group(1), mdco.group(2))
    pol = None
    mpol = re.fullmatch(r"([+-]?[0-9]+(?:\.[0-9]+)?)\((\d+)\)", pol_s)
    if mpol:
        pol = parse_unc(mpol.group(1), mpol.group(2))

    source_rows.append({
        "Eg": float(eg_s),
        "Eg_text": eg_s,
        "gate": dq_gate,  # D or Q in source table
        "DCO": (dco_v, dco_u),
        "delta": delta_s,
        "POL": pol,
    })


# Parse ENS rows
ens_rows = []
for i, line in enumerate(ens_lines):
    if not line.startswith(" 34CL  G "):
        continue

    eg_s = line[9:19].strip()
    try:
        eg = float(eg_s)
    except ValueError:
        continue

    m_field = line[32:41].strip()
    block = []
    j = i + 1
    while j < len(ens_lines):
        nl = ens_lines[j]
        if nl.startswith(" 34CL  G ") or nl.startswith(" 34CL  L ") or nl.startswith(" 34CL d") or nl.startswith(" 34CL PN"):
            break
        block.append(nl)
        j += 1
    comment_text = " ".join(block)

    dco_q = None
    dco_d = None
    mq = re.search(r"R\{-DCO\}\(Q\)=([0-9]+(?:\.[0-9]+)?)\s*\{I(\d+)\}", comment_text)
    if mq:
        dco_q = parse_unc(mq.group(1), mq.group(2))
    md = re.search(r"R\{-DCO\}\(D\)=([0-9]+(?:\.[0-9]+)?)\s*\{I(\d+)\}", comment_text)
    if md:
        dco_d = parse_unc(md.group(1), md.group(2))

    pol = None
    mp = re.search(r"POL=([+-]?[0-9]+(?:\.[0-9]+)?)\s*\{I(\d+)\}", comment_text)
    if mp:
        pol = parse_unc(mp.group(1), mp.group(2))

    ens_rows.append({
        "line": i + 1,
        "Eg": eg,
        "M": m_field,
        "DCO_Q": dco_q,
        "DCO_D": dco_d,
        "POL": pol,
    })


# Match by nearest energy <=2 keV
matches = []
for s in source_rows:
    best = None
    best_dist = 999.0
    for e in ens_rows:
        d = abs(e["Eg"] - s["Eg"])
        if d < best_dist:
            best_dist = d
            best = e
    if best is not None and best_dist <= 2.0:
        matches.append((s, best, best_dist))


# A) transcription fidelity of measured data
transcription_issues = []
for s, e, _ in matches:
    source_dco = s["DCO"]
    ens_dco = e["DCO_D"] if s["gate"] == "D" else e["DCO_Q"]
    if ens_dco is None:
        transcription_issues.append((s["Eg_text"], f"missing R-DCO({s['gate']}) in ENS"))
    else:
        if abs(source_dco[0] - ens_dco[0]) > 1e-9 or abs(source_dco[1] - ens_dco[1]) > 1e-9:
            transcription_issues.append((s["Eg_text"], f"R-DCO({s['gate']}) mismatch source={source_dco} ens={ens_dco}"))

    if s["POL"] is not None:
        if e["POL"] is None:
            transcription_issues.append((s["Eg_text"], "missing POL in ENS"))
        else:
            if abs(s["POL"][0] - e["POL"][0]) > 1e-9 or abs(s["POL"][1] - e["POL"][1]) > 1e-9:
                transcription_issues.append((s["Eg_text"], f"POL mismatch source={s['POL']} ens={e['POL']}"))


# B) DCO-vs-multipolarity check (NO Jpi)
# source gate gives expected anchors:
# gate Q: D->0.5, Q->1.0 ; gate D: D->1.0, Q->2.0
dco_rule_flags = []
for s, e, _ in matches:
    mcls = m_class_from_ens(e["M"])
    if mcls not in ("D", "Q"):
        continue  # mixed/bracket/unknown are not strict-flagged

    if s["gate"] == "Q":
        val, unc = e["DCO_Q"] if e["DCO_Q"] else (None, None)
        if val is None:
            dco_rule_flags.append((s["Eg_text"], e["line"], "missing R-DCO(Q)", e["M"]))
            continue
        exp = 0.5 if mcls == "D" else 1.0
    else:
        val, unc = e["DCO_D"] if e["DCO_D"] else (None, None)
        if val is None:
            dco_rule_flags.append((s["Eg_text"], e["line"], "missing R-DCO(D)", e["M"]))
            continue
        exp = 1.0 if mcls == "D" else 2.0

    z = abs(val - exp) / unc if unc and unc > 0 else 999.0
    if z > 4.0:
        dco_rule_flags.append((s["Eg_text"], e["line"], f"DCO rule mismatch z={z:.1f}, gate={s['gate']}, value={val}({unc}), expected~{exp}", e["M"]))


# C) POL sign check where explicit E/M leading exists
pol_sign_flags = []
for s, e, _ in matches:
    if e["POL"] is None:
        continue
    exp_sign = lead_em_sign(e["M"])
    if exp_sign is None:
        continue
    pol_val = e["POL"][0]
    ok = (pol_val > 0 and exp_sign == "+") or (pol_val < 0 and exp_sign == "-")
    if not ok:
        pol_sign_flags.append((s["Eg_text"], e["line"], e["M"], pol_val, exp_sign))


print(f"SOURCE rows: {len(source_rows)}")
print(f"Matched rows: {len(matches)}")
print(f"Transcription issues: {len(transcription_issues)}")
for x in transcription_issues:
    print("  ", x)

print(f"DCO strict-rule flags (explicit D or Q only): {len(dco_rule_flags)}")
for x in dco_rule_flags:
    print("  ", x)

print(f"POL-sign flags (explicit E/M leading only): {len(pol_sign_flags)}")
for x in pol_sign_flags:
    print("  ", x)
