import re, math, pathlib, random

src_md = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_I.md")
tbl4_md = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md")
out_path = pathlib.Path("XUNDL/2026OSAA_CT11035_152Gd_cascade_Jpi_check.md")

def spin_strip(jpi):
    if not jpi: return ""
    m = re.match(r"\(?(\d+)\)?", str(jpi))
    return m.group(1) if m else jpi

def parse_t1(lines):
    levels = {}
    for idx, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("|"): continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 9: continue
        if cells[0].startswith("$E_i$"): continue
        if re.fullmatch(r"[-: ]*", "".join(cells)): continue
        ei_m = re.match(r"([\d\.]+)", cells[0])
        ei = ei_m.group(1) if ei_m else ""
        jpi = cells[1]
        if ei:
            levels[float(ei)] = (ei, jpi)
    return levels

def parse_t4(lines):
    casc = []
    for idx, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("|"): continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 10: continue
        if cells[0].startswith("$E_i$"): continue
        if re.fullmatch(r"[-: ]*", "".join(cells)): continue
        ei_m = re.match(r"([\d\.]+)", cells[0])
        eg1_m = re.match(r"([\d\.]+)", cells[1])
        eg2_m = re.match(r"([\d\.]+)", cells[2])
        if not (ei_m and eg1_m and eg2_m): continue
        casc.append({
            "line": idx,
            "Ei": float(ei_m.group(1)), "Eg1": float(eg1_m.group(1)), "Eg2": float(eg2_m.group(1)),
            "J1": cells[6] if len(cells) > 6 else "",
            "J2": cells[7] if len(cells) > 7 else "",
            "J3": cells[8] if len(cells) > 8 else "",
        })
    return casc

def find_level(e_val, levels_dict, tol=0.7):
    best, best_diff = None, float("inf")
    for ei_f, (ei_str, jpi) in levels_dict.items():
        diff = abs(ei_f - e_val)
        if diff <= tol and diff < best_diff:
            best, best_diff = (ei_str, jpi, ei_f), diff
    return best

def check_j(label, j_t4, jpi_t1, matched_level_str):
    """Compare J between T4 and T1. Returns issue string or None."""
    j_t4_has = bool(j_t4.strip())
    j_t1_has = bool(jpi_t1.strip())
    j_t4_spin = spin_strip(j_t4)
    j_t1_spin = spin_strip(jpi_t1)

    if j_t4_has and j_t1_has:
        if j_t4_spin != j_t1_spin:
            return f"{label} mismatch: T4 has '{j_t4}', T1(Ei={matched_level_str}) has '{jpi_t1}'"
        return None  # both have spin, numbers match
    elif j_t4_has and not j_t1_has:
        return f"{label} T4 has spin '{j_t4}' but T1(Ei={matched_level_str}) has NO spin"
    elif not j_t4_has and j_t1_has:
        return f"{label} T4 has NO spin but T1(Ei={matched_level_str}) has '{jpi_t1}'"
    else:
        return None  # both blank - consistent

t1_lines = src_md.read_text(encoding="utf-8").splitlines()
t4_lines = tbl4_md.read_text(encoding="utf-8").splitlines()
levels_t1 = parse_t1(t1_lines)
cascades_t4 = parse_t4(t4_lines)

issues = []
matches = []

for c in cascades_t4:
    ei_t4 = c["Ei"]; eg1_t4 = c["Eg1"]; eg2_t4 = c["Eg2"]
    e_int_calc = round(ei_t4 - eg1_t4, 3)
    e_fin_calc = round(ei_t4 - eg1_t4 - eg2_t4, 3)

    L1 = find_level(ei_t4, levels_t1)
    L2 = find_level(e_int_calc, levels_t1)
    L3 = find_level(e_fin_calc, levels_t1)

    j1t1 = L1[1] if L1 else ""
    j2t1 = L2[1] if L2 else ""
    j3t1 = L3[1] if L3 else ""

    ei_t1 = L1[0] if L1 else "-"
    eint_t1 = L2[0] if L2 else "-"
    efin_t1 = L3[0] if L3 else "-"

    ci = []

    # Spin bidirectional consistency check
    r = check_j("J1", c["J1"], j1t1, ei_t1)
    if r: ci.append(r)
    r = check_j("J2", c["J2"], j2t1, eint_t1)
    if r: ci.append(r)
    r = check_j("J3", c["J3"], j3t1, efin_t1)
    if r: ci.append(r)

    # Level not found at all
    if not L1: ci.append(f"Level Ei={ei_t4} not found in T1")
    if not L2: ci.append(f"Intermediate level E={e_int_calc} not found in T1")
    if not L3: ci.append(f"Final level E={e_fin_calc} not found in T1")

    # Energy conservation check (only if levels found)
    if L1 and L2:
        de1 = abs(L1[2] - L2[2] - eg1_t4)
        if de1 > 0.5:
            ci.append(f"Energy1: |Ei_T1({L1[2]})-Eint_T1({L2[2]})|={L1[2]-L2[2]:.3f} vs Eg1(T4)={eg1_t4} (d={de1:.3f})")
    if L2 and L3:
        de2 = abs(L2[2] - L3[2] - eg2_t4)
        if de2 > 0.5:
            ci.append(f"Energy2: |Eint_T1({L2[2]})-Efin_T1({L3[2]})|={L2[2]-L3[2]:.3f} vs Eg2(T4)={eg2_t4} (d={de2:.3f})")

    entry = {
        "Ei": ei_t4, "Eg1": eg1_t4, "Eg2": eg2_t4,
        "E_int": e_int_calc, "E_fin": e_fin_calc,
        "J1t4": c["J1"], "J2t4": c["J2"], "J3t4": c["J3"],
        "J1t1": j1t1, "J2t1": j2t1, "J3t1": j3t1,
        "Ei_T1": ei_t1, "Eint_T1": eint_t1, "Efin_T1": efin_t1,
        "issues": ci, "t4_line": c["line"],
    }
    if ci:
        issues.append(entry)
    else:
        matches.append(entry)

# Categorize issues
def cat_has(entries, keyword):
    return sum(1 for e in entries if any(keyword in x for x in e["issues"]))

spin_mismatch = cat_has(issues, "mismatch")
t4_has_t1_blank = cat_has(issues, "T4 has spin")  # T4 has, T1 blank
t4_blank_t1_has = cat_has(issues, "T4 has NO spin")  # T4 blank, T1 has
level_nf = cat_has(issues, "not found in T1")
energy_mis = cat_has(issues, "Energy")

# 15% spot-check
seed = 15220260701; random.seed(seed)
n = len(matches); k = max(1, (15 * n + 99) // 100) if n else 0
sample = random.sample(matches, k) if k < n else []
sf = 0
for m in sample:
    for jt4, jt1, lbl in [(m["J1t4"], m["J1t1"], "J1"), (m["J2t4"], m["J2t1"], "J2"), (m["J3t4"], m["J3t1"], "J3")]:
        jt4_has = bool(jt4.strip()); jt1_has = bool(jt1.strip())
        if jt4_has != jt1_has:
            sf += 1; break
        if jt4_has and spin_strip(jt4) != spin_strip(jt1):
            sf += 1; break

out = []
out.append("# Cascade Jpi Cross-Check: Table IV vs Table I")
out.append("")
out.append("## Method")
out.append("")
out.append("- For each cascade: Ei, Eg1, Eg2, J1, J2, J3 in Table IV")
out.append("- Compute E_int = Ei - Eg1, E_fin = Ei - Eg1 - Eg2")
out.append("- Look up all 3 levels in Table I (tol +/-0.7 keV)")
out.append("- Bidirectional spin consistency: T4 and T1 must both have spin, or both be blank")
out.append("- If both have spin, compare spin numbers (no parity)")
out.append("- Check energy conservation: |Ei_T1 - Eint_T1| vs Eg1, |Eint_T1 - Efin_T1| vs Eg2")
out.append("")
out.append("## Summary")
out.append("")
out.append(f"| Metric | Count |")
out.append(f"|---|---:|")
out.append(f"| Total cascades in Table IV | {len(cascades_t4)} |")
out.append(f"| Fully consistent | {len(matches)} |")
out.append(f"| Cascades with issues | {len(issues)} |")
out.append(f"| - Spin mismatch (both have, numbers differ) | {spin_mismatch} |")
out.append(f"| - T4 has spin, T1 blank | {t4_has_t1_blank} |")
out.append(f"| - T4 blank, T1 has spin | {t4_blank_t1_has} |")
out.append(f"| - Level not found in T1 | {level_nf} |")
out.append(f"| - Energy conservation violation | {energy_mis} |")
out.append(f"| Spot-check failures | {sf}/{k} |")
out.append("")

if issues:
    out.append("## Inconsistency List")
    out.append("")
    out.append("| # | T4 Ln | Ei(T4) | Eg1 | Eg2 | E_int | E_fin | J1(T4) | J2(T4) | J3(T4) | J1(T1) | J2(T1) | J3(T1) | Ei(T1) | Eint(T1) | Efin(T1) | Issues |")
    out.append("|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|")
    for i, e in enumerate(issues, 1):
        iss_str = "; ".join(e["issues"])
        out.append(f"| {i} | {e['t4_line']} | {e['Ei']} | {e['Eg1']} | {e['Eg2']} | {e['E_int']} | {e['E_fin']} | {e['J1t4']} | {e['J2t4']} | {e['J3t4']} | {e['J1t1']} | {e['J2t1']} | {e['J3t1']} | {e['Ei_T1']} | {e['Eint_T1']} | {e['Efin_T1']} | {iss_str} |")

out.append("")
out.append("## Full Cascade List")
out.append("")
out.append("| # | T4 Ln | Ei(T4) | Eg1 | Eg2 | E_int | E_fin | J1(T4) | J2(T4) | J3(T4) | J1(T1) | J2(T1) | J3(T1) | Ei(T1) | Eint(T1) | Efin(T1) | Status |")
out.append("|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|")
all_e = sorted(issues + matches, key=lambda x: x["Ei"])
for i, e in enumerate(all_e, 1):
    st = "OK" if not e["issues"] else "ISSUE"
    out.append(f"| {i} | {e['t4_line']} | {e['Ei']} | {e['Eg1']} | {e['Eg2']} | {e['E_int']} | {e['E_fin']} | {e['J1t4']} | {e['J2t4']} | {e['J3t4']} | {e['J1t1']} | {e['J2t1']} | {e['J3t1']} | {e['Ei_T1']} | {e['Eint_T1']} | {e['Efin_T1']} | {st} |")

out_path.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote: {out_path.as_posix()}")
print(f"T4: {len(cascades_t4)} | OK: {len(matches)} | ISSUES: {len(issues)}")
print(f"  SpinMis: {spin_mismatch} | T4has_T1blank: {t4_has_t1_blank} | T4blank_T1has: {t4_blank_t1_has} | LevelNF: {level_nf} | EnergyMis: {energy_mis} | SpotFails: {sf}/{k}")
print()
print("=== ISSUE SUMMARY ===")
for e in issues:
    print(f"  L{e['t4_line']}: Ei={e['Ei']} Eg1={e['Eg1']} Eg2={e['Eg2']} | J1(T4)='{e['J1t4']}' T1='{e['J1t1']}' J2(T4)='{e['J2t4']}' T1='{e['J2t1']}' J3(T4)='{e['J3t4']}' T1='{e['J3t1']}'")
    for x in e["issues"]:
        print(f"    -> {x}")
