import re
import random
import math
import pathlib

src_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_I.md")
tgt_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd.ens")
out_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_CC_cross_check.md")


def to_float(s):
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    try:
        return float(s.replace("E", "e"))
    except Exception:
        return None


def parse_md_cc(cc_raw):
    if cc_raw is None:
        return None, None, None
    t = cc_raw.strip()
    if not t:
        return None, None, None

    c = t
    c = c.replace("$", "").replace("\\times", "x").replace("×", "x").replace("−", "-")
    c = c.replace("^", "")
    c = c.replace("{", "").replace("}", "")
    c = c.replace("\\", "")
    c = re.sub(r"\s+", " ", c).strip()

    m = re.match(r"^([+\-]?\d+(?:\.\d+)?)\s*x\s*10\s*([+\-]?\d+)\s*\((\d+)\)\s*$", c, re.I)
    if m:
        return f"{m.group(1)}E{m.group(2)}", m.group(3), t

    m = re.match(r"^([+\-]?\d+(?:\.\d+)?E[+\-]?\d+)\s*\((\d+)\)\s*$", c, re.I)
    if m:
        return m.group(1).upper(), m.group(2), t

    m = re.match(r"^([+\-]?\d+(?:\.\d+)?)\s*\((\d+)\)\s*$", c)
    if m:
        return m.group(1), m.group(2), t

    return None, None, t


def parse_md_rows(lines):
    rows = []
    for idx, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 9:
            continue
        if cells[0].startswith("$E_i$"):
            continue
        if re.fullmatch(r"[-: ]*", "".join(cells)):
            continue

        ei_m = re.match(r"([\d\.]+)", cells[0])
        eg_m = re.match(r"([\d\.]+)", cells[2])
        if not ei_m or not eg_m:
            continue

        cc_raw = cells[8] if len(cells) > 8 else ""
        cc_val, cc_unc, cc_raw_kept = parse_md_cc(cc_raw)

        rows.append(
            {
                "md_line": idx,
                "Ei": ei_m.group(1),
                "Jpi": cells[1],
                "Eg": eg_m.group(1),
                "Mult": cells[6] if len(cells) > 6 else "",
                "CC_raw": cc_raw_kept,
                "CC_val": cc_val,
                "CC_unc": cc_unc,
            }
        )
    return rows


def parse_ens(lines):
    gammas = []
    current_level_e = ""
    current_level_line = None
    for ln, line in enumerate(lines, 1):
        if len(line) < 80:
            line = line + " " * (80 - len(line))
        if len(line) < 10:
            continue
        if line[5] == " " and line[6] == " " and line[7] == "L":
            current_level_e = line[9:19].strip()
            current_level_line = ln
        elif line[5] == " " and line[6] == " " and line[7] == "G":
            gammas.append(
                {
                    "level_Ei": current_level_e,
                    "level_line": current_level_line,
                    "line": ln,
                    "Eg": line[9:19].strip(),
                    "Mult": line[32:41].strip(),
                    "CC": line[55:62].strip(),
                    "DCC": line[62:64].strip(),
                }
            )
    return gammas


def near(a, b, tol):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


md_lines = src_path.read_text(encoding="utf-8").splitlines()
ens_lines = tgt_path.read_text(encoding="utf-8").splitlines()
md_rows = parse_md_rows(md_lines)
ens_gammas = parse_ens(ens_lines)
md_cc_rows = [r for r in md_rows if r["CC_val"] is not None]

LEVEL_TOL = 0.5
GAMMA_TOL = 0.3

used_ens = set()
comparisons = []

for r in md_cc_rows:
    lv_candidates = []
    for i, g in enumerate(ens_gammas):
        # Mandatory SKILL rule: match parent level first, then gamma energy.
        if i in used_ens:
            continue
        if near(r["Ei"], g["level_Ei"], LEVEL_TOL):
            lv_candidates.append((i, g))

    g_candidates = [(i, g) for (i, g) in lv_candidates if near(r["Eg"], g["Eg"], GAMMA_TOL)]

    if not g_candidates:
        comparisons.append(
            {
                "status": "MISSING_IN_ENS",
                "issue": "No gamma matched after parent-level-first matching",
                "md": r,
                "ens": None,
            }
        )
        continue

    g_candidates.sort(
        key=lambda x: (
            abs(float(r["Ei"]) - float(x[1]["level_Ei"])),
            abs(float(r["Eg"]) - float(x[1]["Eg"])),
        )
    )
    idx, best = g_candidates[0]
    used_ens.add(idx)

    issues = []
    md_cc = r["CC_val"]
    md_unc = r["CC_unc"] or ""
    ens_cc = best["CC"] or ""
    ens_unc = best["DCC"] or ""

    if not ens_cc:
        issues.append(f"VALUE_MISMATCH: source '{md_cc}' vs target ''")
    else:
        v_md = to_float(md_cc)
        v_en = to_float(ens_cc)
        if v_md is None or v_en is None:
            if md_cc != ens_cc:
                issues.append(f"VALUE_MISMATCH: source '{md_cc}' vs target '{ens_cc}'")
        else:
            if not math.isclose(v_md, v_en, rel_tol=0.02, abs_tol=0.0):
                issues.append(f"VALUE_MISMATCH: source '{md_cc}' vs target '{ens_cc}'")

    if md_unc != ens_unc:
        issues.append(f"UNCERTAINTY_MISMATCH: source '{md_unc}' vs target '{ens_unc}'")

    comparisons.append(
        {
            "status": "MATCH" if not issues else "MISMATCH",
            "issue": "; ".join(issues) if issues else "",
            "md": r,
            "ens": best,
        }
    )

extra = []
cc_added_on_md_nocc = []
for i, g in enumerate(ens_gammas):
    if i in used_ens:
        continue
    if g["CC"]:
        # If the transition exists in source MD (same parent level + Eg) but source alpha is blank,
        # classify as CC-added-on-source-noCC instead of true extra.
        found_md_same_transition = False
        found_md_same_transition_with_cc = False
        for r in md_rows:
            if near(r["Ei"], g["level_Ei"], LEVEL_TOL) and near(r["Eg"], g["Eg"], GAMMA_TOL):
                found_md_same_transition = True
                if r["CC_val"] is not None:
                    found_md_same_transition_with_cc = True
                break

        if found_md_same_transition and not found_md_same_transition_with_cc:
            cc_added_on_md_nocc.append(g)
        elif not found_md_same_transition:
            extra.append(g)

seed = 15220260630
random.seed(seed)
pool = [c for c in comparisons if c["ens"] is not None]
n = len(pool)
k = max(1, (15 * n + 99) // 100) if n else 0
sample = random.sample(pool, k) if (k and k < n) else pool

spot_fails = []
for c in sorted(sample, key=lambda x: (float(x["md"]["Ei"]), float(x["md"]["Eg"]))):
    md_cc = c["md"]["CC_val"]
    md_unc = c["md"]["CC_unc"] or ""
    en_cc = c["ens"]["CC"] or ""
    en_unc = c["ens"]["DCC"] or ""
    v_md = to_float(md_cc)
    v_en = to_float(en_cc)
    bad = []
    if (v_md is None or v_en is None):
        if md_cc != en_cc:
            bad.append(f"value {md_cc} vs {en_cc}")
    else:
        if not math.isclose(v_md, v_en, rel_tol=0.02, abs_tol=0.0):
            bad.append(f"value {md_cc} vs {en_cc}")
    if md_unc != en_unc:
        bad.append(f"unc {md_unc} vs {en_unc}")
    if bad:
        spot_fails.append((c, bad))

val_mis = sum(1 for c in comparisons if "VALUE_MISMATCH" in c["issue"])
unc_mis = sum(1 for c in comparisons if "UNCERTAINTY_MISMATCH" in c["issue"])
missing = sum(1 for c in comparisons if c["status"] == "MISSING_IN_ENS")
match = sum(1 for c in comparisons if c["status"] == "MATCH")

lines = []
lines.append("# CC Cross-Check: 2026OSAA Table I (MD) vs 2026OSAA CT11035 152Gd (ENS)")
lines.append("")
lines.append("## Task Configuration")
lines.append("")
lines.append("- Source: XUNDL/2026OSAA_CT11035_152Gd_Table_I.md")
lines.append("- Target: XUNDL/2026OSAA_CT11035_152Gd.ens")
lines.append("- Field mapping: MD alpha column -> ENS G-record CC (col 56-62), MD uncertainty -> ENS G-record DCC (col 63-64)")
lines.append("- Matching: parent level first (Ei within +/-0.5 keV), then gamma energy Eg within +/-0.3 keV")
lines.append("- Checks: CC value and CC uncertainty only")
lines.append("")
lines.append("## Summary")
lines.append("")
lines.append("| Metric | Count |")
lines.append("|---|---:|")
lines.append(f"| Source MD rows with CC | {len(md_cc_rows)} |")
lines.append(f"| Matched (value+uncertainty) | {match} |")
lines.append(f"| Value mismatches | {val_mis} |")
lines.append(f"| Uncertainty mismatches | {unc_mis} |")
lines.append(f"| Missing in ENS after matching | {missing} |")
lines.append(f"| Extra ENS CC (unpaired, no MD transition) | {len(extra)} |")
lines.append(f"| ENS CC added where MD has same transition but blank CC | {len(cc_added_on_md_nocc)} |")
lines.append(f"| Spot-check failures | {len(spot_fails)}/{k} |")
lines.append("")

lines.append("## Mismatch List (All)")
lines.append("")
lines.append("| Type | Source Ei | Source Eg | Source CC | Source DCC | Target line | Target Ei | Target Eg | Target CC | Target DCC | Detail |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
for c in comparisons:
    if c["status"] == "MATCH":
        continue
    md = c["md"]
    en = c["ens"]
    if en is None:
        lines.append(
            f"| Missing | {md['Ei']} | {md['Eg']} | {md['CC_val']} | {md['CC_unc'] or ''} | - | - | - | - | - | {c['issue']} |"
        )
    else:
        lines.append(
            f"| Mismatch | {md['Ei']} | {md['Eg']} | {md['CC_val']} | {md['CC_unc'] or ''} | {en['line']} | {en['level_Ei']} | {en['Eg']} | {en['CC']} | {en['DCC']} | {c['issue']} |"
        )

if not any(c["status"] != "MATCH" for c in comparisons):
    lines.append("| None | - | - | - | - | - | - | - | - | - | All matched |")

for g in cc_added_on_md_nocc:
    lines.append(
        f"| ENS CC Added | - | - | - | - | {g['line']} | {g['level_Ei']} | {g['Eg']} | {g['CC']} | {g['DCC']} | Same MD transition exists with blank source CC |"
    )

for g in extra:
    lines.append(
        f"| Extra ENS | - | - | - | - | {g['line']} | {g['level_Ei']} | {g['Eg']} | {g['CC']} | {g['DCC']} | Target has CC but no paired source CC row |"
    )

lines.append("")
lines.append("## Full CC List (Source CC Rows)")
lines.append("")
lines.append("| # | Source line | Source Ei | Source Jpi | Source Eg | Source Mult | Source CC | Source DCC | Target line | Target Ei | Target Eg | Target CC | Target DCC | Status |")
lines.append("|---:|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|")

idx = 0
for c in comparisons:
    idx += 1
    md = c["md"]
    en = c["ens"]
    if en is None:
        lines.append(
            f"| {idx} | {md['md_line']} | {md['Ei']} | {md['Jpi']} | {md['Eg']} | {md['Mult']} | {md['CC_val']} | {md['CC_unc'] or ''} | - | - | - | - | - | {c['status']} |"
        )
    else:
        lines.append(
            f"| {idx} | {md['md_line']} | {md['Ei']} | {md['Jpi']} | {md['Eg']} | {md['Mult']} | {md['CC_val']} | {md['CC_unc'] or ''} | {en['line']} | {en['level_Ei']} | {en['Eg']} | {en['CC'] or ''} | {en['DCC'] or ''} | {c['status']} |"
        )

lines.append("")
lines.append("## 15% Reproducible Random Spot-Check")
lines.append("")
lines.append(f"- Seed: {seed}")
lines.append(f"- Pool size: {n}")
lines.append(f"- Sample size: {k}")
lines.append(f"- Failures: {len(spot_fails)}")
if spot_fails:
    lines.append("")
    lines.append("| Source Ei | Source Eg | Target line | Issues |")
    lines.append("|---:|---:|---:|---|")
    for c, bad in spot_fails:
        lines.append(f"| {c['md']['Ei']} | {c['md']['Eg']} | {c['ens']['line']} | {'; '.join(bad)} |")

out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote: {out_path.as_posix()}")
print(
    f"MD CC rows: {len(md_cc_rows)} | MATCH: {match} | VALUE_MISMATCH: {val_mis} | "
    f"UNC_MISMATCH: {unc_mis} | MISSING: {missing} | EXTRA: {len(extra)} | CC_ADDED_ON_MD_NOCC: {len(cc_added_on_md_nocc)}"
)
