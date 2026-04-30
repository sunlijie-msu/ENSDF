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

    eg_s, ji, jf, dq_label, dco_s, delta_s, pol_s = parts
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
        "DQ": dq_label,
        "DCO": (dco_v, dco_u),
        "delta": delta_s,
        "POL": pol,
    })


# Parse ENS G records and attached cG comments
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


# Match source to ENS by nearest energy (<=2 keV)
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


# 1) Source->ENS measured value transcription check
transcription_issues = []
for s, e, dist in matches:
    ens_dco = e["DCO_D"] if e["DCO_D"] else e["DCO_Q"]
    if ens_dco is None:
        transcription_issues.append((s["Eg_text"], "missing DCO in ENS"))
    else:
        if abs(ens_dco[0] - s["DCO"][0]) > 1e-9 or abs(ens_dco[1] - s["DCO"][1]) > 1e-9:
            transcription_issues.append((s["Eg_text"], f"DCO mismatch source={s['DCO']} ens={ens_dco}"))

    if s["POL"] is not None:
        if e["POL"] is None:
            transcription_issues.append((s["Eg_text"], "missing POL in ENS"))
        else:
            if abs(e["POL"][0] - s["POL"][0]) > 1e-9 or abs(e["POL"][1] - s["POL"][1]) > 1e-9:
                transcription_issues.append((s["Eg_text"], f"POL mismatch source={s['POL']} ens={e['POL']}"))


# 2) DCO rule check from source D/Q label only (no Jpi inference)
# gate-specific anchors:
# label D: gate D->1.0, gate Q->0.5
# label Q: gate D->2.0, gate Q->1.0
dco_outliers = []
for s, e, dist in matches:
    gate = "D" if e["DCO_D"] is not None else ("Q" if e["DCO_Q"] is not None else None)
    if gate is None:
        continue

    val, unc = e["DCO_D"] if gate == "D" else e["DCO_Q"]
    if s["DQ"] == "D":
        exp = 1.0 if gate == "D" else 0.5
    else:
        exp = 2.0 if gate == "D" else 1.0

    z = abs(val - exp) / unc if unc > 0 else 999.0
    if z > 4.0:
        dco_outliers.append({
            "Eg": s["Eg_text"],
            "line": e["line"],
            "label": s["DQ"],
            "gate": gate,
            "value": val,
            "unc": unc,
            "expected": exp,
            "z": z,
        })


# 3) POL sign rule where leading E/M is explicit in ENS M field
pol_mismatches = []
for s, e, dist in matches:
    if e["POL"] is None:
        continue

    base = e["M"].strip("[]()").split("+")[0].strip()
    expected_sign = None
    if base.startswith("E"):
        expected_sign = "+"
    elif base.startswith("M"):
        expected_sign = "-"
    else:
        continue

    pol_val = e["POL"][0]
    ok = (pol_val > 0 and expected_sign == "+") or (pol_val < 0 and expected_sign == "-")
    if not ok:
        pol_mismatches.append({
            "Eg": s["Eg_text"],
            "line": e["line"],
            "M": e["M"],
            "POL": pol_val,
            "expected_sign": expected_sign,
        })


print(f"SOURCE rows: {len(source_rows)}")
print(f"Matched rows: {len(matches)}")
print(f"Transcription issues: {len(transcription_issues)}")
for t in transcription_issues:
    print("  ", t)

print(f"DCO outliers (>4 sigma): {len(dco_outliers)}")
for o in dco_outliers:
    print("  Eg={Eg} line={line} label={label} gate={gate} value={value}({unc}) exp~{expected} z={z:.1f}".format(**o))

print(f"POL sign mismatches (explicit E/M only): {len(pol_mismatches)}")
for p in pol_mismatches:
    print("  Eg={Eg} line={line} M={M} POL={POL:+} expected {expected_sign}".format(**p))
