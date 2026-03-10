from pathlib import Path
import re
import random

ENS_PATH = Path(r"d:\\X\\ND\\ENSDF\\A34\\Cl34\\new\\Cl34_33s_p_g.ens")
MRG_PATH = Path(r"d:\\X\\ND\\ENSDF\\A34\\Cl34\\raw\\1977DA02_1983WA27.mrg")
START_LEVEL = 1887.30
MAX_LEVEL = 5540.8

SOURCE_PAT = re.compile(r"34CL  G\s+([^\s]+)\s+([^\s]+)?\s*([^\s]*)")
FROM_PAT = re.compile(r"^\s*34CL cG RI\$from (1977Da02|1983Wa27)\.?")
QUOTED_PAT = re.compile(r"([<>]?\d+(?:\.\d+)?)\s*\{I([^}]+)\}\s*\((1977Da02|1983Wa27)\)")
OTHER_PAT = re.compile(r"Other:\s*(<)?\s*(\d+(?:\.\d+)?)\s*(?:\{I([^}]+)\})?\s*\((1977Da02|1983Wa27)\)")


def is_cg_comment(line: str) -> bool:
    marker = line[6:9] if len(line) >= 9 else ""
    return marker.startswith("cG") or marker.endswith("cG")


def parse_ens(path: Path):
    levels = []
    current = None
    current_gamma = None
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            rectype = line[7:8] if len(line) >= 8 else ""
            is_data_record = len(line) >= 7 and line[6:7] == " "
            if is_data_record and rectype == "L":
                energy_text = line[9:19].strip()
                try:
                    energy = float(energy_text)
                except ValueError:
                    current = None
                    current_gamma = None
                    continue
                current = {
                    "energy": energy,
                    "line": lineno,
                    "raw": line.rstrip("\n"),
                    "gammas": [],
                }
                levels.append(current)
                current_gamma = None
            elif is_data_record and rectype == "G" and current is not None:
                current_gamma = {
                    "eg": line[9:19].strip(),
                    "ri": line[22:29].strip(),
                    "dri": line[29:31].strip(),
                    "line": lineno,
                    "raw": line.rstrip("\n"),
                    "comments": [],
                }
                current["gammas"].append(current_gamma)
            elif current is not None and current_gamma is not None:
                if is_cg_comment(line):
                    current_gamma["comments"].append((lineno, line.rstrip("\n")))
    return [level for level in levels if START_LEVEL <= level["energy"] <= MAX_LEVEL]


def parse_mrg(path: Path):
    levels = []
    current = None
    current_gamma = None
    with path.open(encoding="utf-8", errors="replace") as handle:
        for lineno, line in enumerate(handle, start=1):
            text = line.rstrip("\n")
            if text.startswith(" LEVEL********************************* 34CL  L "):
                match = re.search(r"LEVEL\*+ 34CL  L\s+([0-9.]+)", text)
                if not match:
                    continue
                current = {
                    "energy": float(match.group(1)),
                    "line": lineno,
                    "gammas": [],
                }
                levels.append(current)
                current_gamma = None
            elif text.startswith(" GAMMA--------------------------------- 34CL  G ") and current is not None:
                current_gamma = {"line": lineno, "A": None, "B": None}
                current["gammas"].append(current_gamma)
            elif "1977DA02--->A" in text and current_gamma is not None:
                current_gamma["A"] = text
            elif "1983Wa27--->B" in text and current_gamma is not None:
                current_gamma["B"] = text
    return [level for level in levels if START_LEVEL <= level["energy"] <= MAX_LEVEL]


def source_dict(source_line: str | None):
    if not source_line:
        return None
    match = SOURCE_PAT.search(source_line)
    if not match:
        return None
    return {
        "eg": match.group(1),
        "ri": (match.group(2) or "").strip(),
        "dri": (match.group(3) or "").strip(),
        "raw": source_line,
    }


def decimal_places(text: str) -> int:
    clean = text.lstrip("<>")
    if "." in clean:
        return len(clean.split(".", 1)[1])
    return 0


def parse_numeric_ri(value_text: str, uncertainty_text: str):
    value_text = value_text.strip()
    uncertainty_text = uncertainty_text.strip()
    if not value_text:
        return None
    try:
        value = float(value_text)
    except ValueError:
        return None
    decimals = decimal_places(value_text)
    limit = None
    sigma = None
    if uncertainty_text in {"LT", "GT"}:
        limit = uncertainty_text
    elif uncertainty_text:
        try:
            sigma = int(uncertainty_text) * (10 ** (-decimals))
        except ValueError:
            sigma = None
    return {"value": value, "sigma": sigma, "limit": limit, "text": (value_text, uncertainty_text)}


def parse_comment_quote(value_text: str, uncertainty_text: str | None, has_lt: bool = False):
    try:
        value = float(value_text)
    except ValueError:
        return None
    decimals = decimal_places(value_text)
    sigma = None
    if uncertainty_text:
        sigma = int(uncertainty_text) * (10 ** (-decimals))
    return {"value": value, "sigma": sigma, "limit": "LT" if has_lt else None, "text": (value_text, uncertainty_text or "")}


def comment_mode(comment_text: str) -> str:
    if not comment_text:
        return "default-B"
    lowered = comment_text.lower()
    if "weighted average" in lowered or "unweighted average" in lowered:
        return "average"
    if "from 1977da02" in lowered:
        return "from-A"
    if "from 1983wa27" in lowered or "other:" in lowered:
        return "default-B"
    return "default-B"


def nearest_level(levels, energy):
    best = None
    best_delta = None
    for level in levels:
        delta = abs(level["energy"] - energy)
        if best is None or delta < best_delta:
            best = level
            best_delta = delta
    if best is None or best_delta is None or best_delta > 2.5:
        return None
    return best


def match_gamma(mrg_gammas, ens_gamma_energy: str):
    if ens_gamma_energy == "x":
        return None
    try:
        ens_value = float(ens_gamma_energy.replace("E", "e"))
    except ValueError:
        return None
    best = None
    best_delta = None
    for gamma in mrg_gammas:
        for key in ("B", "A"):
            source = gamma.get(key)
            if not source or source["eg"] in ("", "x"):
                continue
            try:
                delta = abs(float(source["eg"]) - ens_value)
            except ValueError:
                continue
            if best is None or delta < best_delta:
                best = gamma
                best_delta = delta
    if best is None or best_delta is None or best_delta > 3.0:
        return None
    return best


def main():
    ens_levels = parse_ens(ENS_PATH)
    mrg_levels = parse_mrg(MRG_PATH)
    findings = []
    compared_entries = []
    formatting_only = []
    average_entries = []
    from_a_entries = []

    for level in ens_levels:
        mrg_level = nearest_level(mrg_levels, level["energy"])
        if mrg_level is None:
            continue

        mrg_gammas = []
        for gamma in mrg_level["gammas"]:
            mrg_gammas.append({
                "A": source_dict(gamma.get("A")),
                "B": source_dict(gamma.get("B")),
            })

        for gamma in level["gammas"]:
            if gamma["eg"] == "x":
                continue
            matched = match_gamma(mrg_gammas, gamma["eg"])
            if matched is None:
                findings.append((gamma["line"], f"Level {level['energy']} gamma {gamma['eg']}: no matching MRG gamma found"))
                continue

            source_a = matched["A"]
            source_b = matched["B"]
            adopted = parse_numeric_ri(gamma["ri"], gamma["dri"])
            comment_text = " ".join(text for _, text in gamma["comments"] if "cG RI$" in text)
            mode = comment_mode(comment_text)
            compared_entries.append({
                "level": level["energy"],
                "line": gamma["line"],
                "eg": gamma["eg"],
                "adopted": gamma["raw"],
                "A": source_a["raw"] if source_a else None,
                "B": source_b["raw"] if source_b else None,
                "comments": [text for _, text in gamma["comments"] if "cG RI$" in text],
                "mode": mode,
            })

            source_a_numeric = parse_numeric_ri(source_a["ri"], source_a["dri"]) if source_a else None
            source_b_numeric = parse_numeric_ri(source_b["ri"], source_b["dri"]) if source_b else None

            if mode == "average":
                average_entries.append(gamma["line"])
            elif mode == "from-A":
                from_a_entries.append(gamma["line"])
                if source_a_numeric and adopted and (
                    adopted["limit"] != source_a_numeric["limit"] or
                    adopted["value"] != source_a_numeric["value"] or
                    adopted["sigma"] != source_a_numeric["sigma"]
                ):
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: adopted RI/DRI {gamma['ri']} {gamma['dri']} should follow A {source_a['ri']} {source_a['dri']}"
                    ))
            elif source_b and source_b["ri"]:
                if adopted and source_b_numeric:
                    if adopted["limit"] != source_b_numeric["limit"] or adopted["value"] != source_b_numeric["value"] or adopted["sigma"] != source_b_numeric["sigma"]:
                        findings.append((
                            gamma["line"],
                            f"Level {level['energy']} gamma {gamma['eg']}: adopted RI/DRI {gamma['ri']} {gamma['dri']} != default B {source_b['ri']} {source_b['dri']}"
                        ))
                    elif gamma["ri"] != source_b["ri"] or gamma["dri"] != source_b["dri"]:
                        formatting_only.append((
                            gamma["line"],
                            f"Level {level['energy']} gamma {gamma['eg']}: formatting-normalized match to B, adopted {gamma['ri']} {gamma['dri']} vs B {source_b['ri']} {source_b['dri']}"
                        ))
            elif source_b and not source_b["ri"] and gamma["ri"] and mode == "default-B":
                findings.append((
                    gamma["line"],
                    f"Level {level['energy']} gamma {gamma['eg']}: adopted has RI {gamma['ri']} {gamma['dri']} but B is Eg-only"
                ))

            if not comment_text:
                continue

            from_match = FROM_PAT.search(comment_text)
            if from_match and "Other:" not in comment_text:
                source_name = from_match.group(1)
                source = source_a if source_name == "1977Da02" else source_b
                source_numeric = parse_numeric_ri(source["ri"], source["dri"]) if source else None
                if source and source_numeric and adopted and (
                    adopted["limit"] != source_numeric["limit"] or
                    adopted["value"] != source_numeric["value"] or
                    adopted["sigma"] != source_numeric["sigma"]
                ):
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: RI comment says from {source_name} but adopted RI/DRI {gamma['ri']} {gamma['dri']} != source {source['ri']} {source['dri']}"
                    ))

            for quoted_value, quoted_unc, source_name in QUOTED_PAT.findall(comment_text):
                source = source_a if source_name == "1977Da02" else source_b
                if source is None:
                    findings.append((gamma["line"], f"Level {level['energy']} gamma {gamma['eg']}: comment quotes {source_name} but MRG source missing"))
                    continue
                quoted_numeric = parse_comment_quote(quoted_value.lstrip("<>"), quoted_unc)
                source_numeric = parse_numeric_ri(source["ri"], source["dri"])
                if quoted_numeric is None or source_numeric is None:
                    continue
                if quoted_numeric["value"] != source_numeric["value"] or quoted_numeric["sigma"] != source_numeric["sigma"]:
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: comment quote for {source_name} is {quoted_value}{{I{quoted_unc}}} but MRG has {source['ri']} {source['dri']}"
                    ))

            for has_lt, other_value, other_unc, source_name in OTHER_PAT.findall(comment_text):
                source = source_a if source_name == "1977Da02" else source_b
                if source is None:
                    findings.append((gamma["line"], f"Level {level['energy']} gamma {gamma['eg']}: Other quotes {source_name} but MRG source missing"))
                    continue
                other_numeric = parse_comment_quote(other_value, other_unc or None, has_lt=bool(has_lt))
                source_numeric = parse_numeric_ri(source["ri"], source["dri"])
                if other_numeric is None or source_numeric is None:
                    continue
                if other_numeric["value"] != source_numeric["value"]:
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: Other quote for {source_name} gives {other_value} but MRG has {source['ri']}"
                    ))
                if other_numeric["sigma"] != source_numeric["sigma"]:
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: Other quote uncertainty for {source_name} gives {other_unc} but MRG has {source['dri']}"
                    ))
                if other_numeric["limit"] != source_numeric["limit"]:
                    findings.append((
                        gamma["line"],
                        f"Level {level['energy']} gamma {gamma['eg']}: Other quote limit for {source_name} does not match MRG"
                    ))

    for line, message in sorted(findings):
        print(f"{line}: {message}")
    for line, message in sorted(formatting_only):
        print(f"{line}: {message}")
    print(f"TOTAL_FINDINGS={len(findings)}")
    print(f"TOTAL_FORMATTING_ONLY={len(formatting_only)}")
    print(f"TOTAL_AVERAGE_MODE={len(average_entries)}")
    print(f"TOTAL_FROM_A_MODE={len(from_a_entries)}")
    print(f"TOTAL_COMPARED_ENTRIES={len(compared_entries)}")

    sample_size = max(5, -(-len(compared_entries) // 20)) if compared_entries else 0
    random.seed(20260310)
    indices = sorted(random.sample(range(len(compared_entries)), sample_size)) if sample_size else []
    print(f"SPOTCHECK_SEED=20260310")
    print(f"SPOTCHECK_SAMPLE_SIZE={sample_size}")
    for index in indices:
        entry = compared_entries[index]
        print(f"SPOTCHECK {index}: level={entry['level']} gamma={entry['eg']} line={entry['line']}")
        print(f"  ADOPTED: {entry['adopted']}")
        if entry['B']:
            print(f"  B: {entry['B']}")
        if entry['A']:
            print(f"  A: {entry['A']}")
        for comment in entry['comments']:
            print(f"  COMMENT: {comment}")


if __name__ == "__main__":
    main()
