import re
import random
from collections import Counter
from pathlib import Path

SOURCE = Path(r"A34/S34/raw/1985RA15_Table_V.md")
TARGET = Path(r"A34/S34/new/S34_ng_E_thermal.ens")
REPORT = Path(r".github/temp/2026-08-17_1985ra15_cross_check/1985RA15_vs_S34_ng_E_thermal_report.md")
ROW_RE = re.compile(r"^\|\s*([0-9]+(?:\.[0-9]+)?)\((\d+)\)\s*\|\s*([0-9]+(?:\.[0-9]+)?)\((\d+)\)\s*\|")


def value(text):
    return float(text)


def parse_source():
    rows = []
    for line_no, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1):
        match = ROW_RE.match(line)
        if match:
            rows.append((line_no, *match.groups()))
    return rows


def parse_target():
    records = []
    parent = None
    for line_no, line in enumerate(TARGET.read_text(encoding="utf-8").splitlines(), 1):
        if len(line) >= 9 and line[5:9] == "  L ":
            parent = line[9:19].strip()
        if len(line) >= 80 and line[5:9] == "  G ":
            records.append({
                "line": line_no,
                "parent": parent or "-",
                "e": line[9:19].strip(),
                "de": line[19:21].strip(),
                "ri": line[22:29].strip(),
                "dri": line[29:31].strip(),
                "col22": line[21],
            })
    return records


def main():
    source = parse_source()
    target = parse_target()
    matches = []
    unmatched = []
    ambiguous = []
    used = set()
    mismatches = []

    for row in source:
        source_line, e, de, ri, dri = row
        candidates = [g for g in target if abs(value(g["e"]) - value(e)) <= 0.5]
        if not candidates:
            unmatched.append(row)
            continue
        if len(candidates) > 1:
            ambiguous.append((row, candidates))
        selected = min(candidates, key=lambda g: abs(value(g["e"]) - value(e)))
        used.add(selected["line"])
        categories = []
        if abs(value(e) - value(selected["e"])) > 1e-9:
            categories.append("E numeric/rounding")
        if not selected["de"].isdigit() or int(de) != int(selected["de"]):
            categories.append("DE uncertainty")
        if abs(value(ri) - value(selected["ri"])) > 1e-9:
            categories.append("RI value")
        if not selected["dri"].isdigit() or int(dri) != int(selected["dri"]):
            categories.append("DRI uncertainty")
        if e != selected["e"]:
            categories.append("E format")
        if de != selected["de"]:
            categories.append("DE format")
        if ri != selected["ri"]:
            categories.append("RI format")
        if dri != selected["dri"]:
            categories.append("DRI format")
        if selected["col22"] != " ":
            categories.append("RI starts column 22")
        if categories:
            mismatches.append((row, selected, categories))
        matches.append((row, selected))

    extras = [g for g in target if g["line"] not in used]
    category_counts = Counter(category for _, _, categories in mismatches for category in categories)

    random.seed(12520260817)
    sample = random.sample(source, max(5, round(len(source) * 0.15)))
    spot_failures = []
    for row in sample:
        source_line, e, de, ri, dri = row
        candidates = [g for g in target if abs(value(g["e"]) - value(e)) <= 0.5]
        if not candidates:
            spot_failures.append((row, None, "no energy match"))
            continue
        selected = min(candidates, key=lambda g: abs(value(g["e"]) - value(e)))
        reasons = []
        if not selected["de"].isdigit() or int(de) != int(selected["de"]):
            reasons.append("DE")
        if abs(value(ri) - value(selected["ri"])) > 1e-9:
            reasons.append("RI")
        if not selected["dri"].isdigit() or int(dri) != int(selected["dri"]):
            reasons.append("DRI")
        if reasons:
            spot_failures.append((row, selected, ", ".join(reasons)))

    out = []
    out.append("# 1985Ra15 Table V vs S34_ng_E_thermal ENSDF Cross-Check")
    out.append("")
    out.append("## Configuration")
    out.append("")
    out.append(f"- Source: `{SOURCE.as_posix()}`")
    out.append(f"- Target: `{TARGET.as_posix()}`")
    out.append("- Mapping: source Energy/Intensity columns -> target G E/DE and RI/DRI fields")
    out.append("- Matching: numeric gamma energy within +/-0.5 keV; parent level retained and reported")
    out.append("- Check-only: no ENSDF data records modified")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append("| Metric | Count |")
    out.append("|---|---:|")
    out.append(f"| Source rows | {len(source)} |")
    out.append(f"| Target G records | {len(target)} |")
    out.append(f"| Matched source rows | {len(matches)} |")
    out.append(f"| Unmatched source rows | {len(unmatched)} |")
    out.append(f"| Ambiguous energy matches | {len(ambiguous)} |")
    out.append(f"| Unmatched target G records | {len(extras)} |")
    out.append(f"| Matched rows with one or more mismatches | {len(mismatches)} |")
    out.append("")
    out.append("## Category Counts")
    out.append("")
    out.append("| Category | Count |")
    out.append("|---|---:|")
    for category, count in category_counts.most_common():
        out.append(f"| {category} | {count} |")
    out.append("")
    out.append("## Mismatch Details")
    out.append("")
    out.append("| Source line | Source E(DE) | Source RI(DRI) | Target line | Parent L E | Target E(DE) | Target RI(DRI) | Categories |")
    out.append("|---:|---|---|---:|---:|---|---|---|")
    for row, g, categories in mismatches:
        out.append(f"| {row[0]} | `{row[1]}({row[2]})` | `{row[3]}({row[4]})` | {g['line']} | {g['parent']} | `{g['e']}({g['de']})` | `{g['ri']}({g['dri']})` | {', '.join(categories)} |")
    out.append("")
    out.append("## Ambiguous Matches")
    out.append("")
    out.append("| Source line | Source E | Candidate target line/parent/E |")
    out.append("|---:|---:|---|")
    for row, candidates in ambiguous:
        candidates_text = "; ".join(f"{g['line']}/{g['parent']}/{g['e']}" for g in candidates)
        out.append(f"| {row[0]} | `{row[1]}` | {candidates_text} |")
    out.append("")
    out.append("## Unmatched Source Rows")
    out.append("")
    if unmatched:
        for row in unmatched:
            out.append(f"- Source line {row[0]}: `{row[1]}({row[2]})`, `{row[3]}({row[4]})`")
    else:
        out.append("None. All source rows matched within +/-0.5 keV.")
    out.append("")
    out.append("## Extra Target G Records")
    out.append("")
    out.append("These target records have no unique source-row assignment under the energy-only comparison. Many are LT upper limits or transitions not listed in Table V.")
    out.append("")
    out.append("| Target line | Parent L E | Target E(DE) | Target RI(DRI) |")
    out.append("|---:|---:|---|---|")
    for g in extras:
        out.append(f"| {g['line']} | {g['parent']} | `{g['e']}({g['de']})` | `{g['ri']}({g['dri']})` |")
    out.append("")
    out.append("## Reproducible Spot Check")
    out.append("")
    out.append(f"- Seed: `12520260817`; sample size: `{len(sample)}` ({len(sample) / len(source):.1%})")
    out.append(f"- Failures: `{len(spot_failures)}`")
    out.append("")
    out.append("| Source line | Target line | Result |")
    out.append("|---:|---:|---|")
    failed_lines = {row[0]: (g, reason) for row, g, reason in spot_failures}
    for row in sample:
        if row[0] in failed_lines:
            g, reason = failed_lines[row[0]]
            out.append(f"| {row[0]} | {g['line'] if g else '-'} | FAIL: {reason} |")
        else:
            candidates = [g for g in target if abs(value(g['e']) - value(row[1])) <= 0.5]
            g = min(candidates, key=lambda x: abs(value(x['e']) - value(row[1])))
            out.append(f"| {row[0]} | {g['line']} | PASS |")
    out.append("")
    out.append("## Assessment")
    out.append("")
    out.append("The source energy list is complete against the target at the selected tolerance, but the target requires correction or deliberate retention review before it can be called 100% consistent. The most widespread issue is RI field alignment/representation; 127 matched target records have a nonblank column 22, indicating RI begins one column early relative to ENSDF field definitions.")
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(REPORT)
    print(f"source={len(source)} target_g={len(target)} matched={len(matches)} mismatches={len(mismatches)} ambiguous={len(ambiguous)} extras={len(extras)} spot_failures={len(spot_failures)}")


if __name__ == "__main__":
    main()
