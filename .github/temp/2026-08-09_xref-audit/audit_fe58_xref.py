from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OLD = ROOT / "XUNDL" / "A58" / "Fe58" / "old"
ADOPTED = OLD / "Fe58_adopted.ens"

DATASET_RE = re.compile(r"^ 58FE  X([A-Zabcd])")
L_RE = re.compile(r"^ 58FE  L ")
XREF_RE = re.compile(r"XREF=(\S.*?)(?:\s{2,}|$)")
TOKEN_RE = re.compile(r"([A-Zabcd])(?:\(([^)]*)\))?")
ENERGY_RE = re.compile(r"^[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?$")


def parse_l_energy(line: str) -> tuple[str, float | None]:
    text = line[9:19].strip()
    try:
        return text, float(text)
    except ValueError:
        return text, None


def parse_source(path: Path):
    levels = []
    for number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.rstrip("\r\n")
        if L_RE.match(line):
            energy_text, energy = parse_l_energy(line)
            levels.append({"line": number, "energy_text": energy_text, "energy": energy, "raw": line})
    return levels


def parse_adopted():
    levels = []
    dataset_paths = {}
    lines = ADOPTED.read_text(encoding="ascii").splitlines()
    current = None
    for number, raw in enumerate(lines, 1):
        line = raw.rstrip("\r\n")
        match = DATASET_RE.match(line)
        if match:
            dataset_paths[match.group(1)] = line[7:].strip()
        if L_RE.match(line):
            energy_text, energy = parse_l_energy(line)
            current = {"line": number, "energy_text": energy_text, "energy": energy, "raw": line, "tokens": []}
            levels.append(current)
            continue
        if current is not None and "XREF=" in line:
            match = XREF_RE.search(line)
            if not match:
                current["syntax_errors"].append((number, "cannot isolate XREF value"))
                continue
            value = match.group(1)
            current["xref_line"] = number
            current["xref_text"] = value
            current["tokens"] = list(TOKEN_RE.finditer(value))
            labels = [m.group(1) for m in current["tokens"]]
            if " " in value:
                current.setdefault("syntax_errors", []).append((number, "internal space in XREF"))
            if labels != sorted(labels, key="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".index):
                current.setdefault("syntax_errors", []).append((number, "dataset labels not alphabetical"))
            if len(labels) != len(set(labels)):
                current.setdefault("syntax_errors", []).append((number, "duplicate dataset label"))
            consumed = "".join(m.group(0) for m in current["tokens"])
            if consumed != value.replace(" ", ""):
                current.setdefault("syntax_errors", []).append((number, f"unparsed text: {value!r}"))
    return levels, dataset_paths


def main():
    adopted, dataset_descriptions = parse_adopted()
    sources = {label: parse_source(OLD / name) for label, name in {
        "A": "Fe58_beta_decay_3.0_s.ens", "B": "Fe58_beta_decay_65.4_s.ens",
        "C": "Fe58_ec_decay_70.885_d.ens", "D": "Fe58_ec_decay_8.853_h.ens",
        "E": "Fe58_58ni_2b+_decay.ens", "F": "Fe58_13c_48ca_3ng.ens",
        "G": "Fe58_48ca_13c_3ng.ens", "H": "Fe58_54cr_6li_d.ens",
        "I": "Fe58_55mn_a_pg.ens", "J": "Fe58_56fe_t_p_pol_t_p.ens",
        "K": "Fe58_56fe_a_2he.ens", "L": "Fe58_ng_E_th.ens",
        "M": "Fe58_ng_n_n_resonances.ens", "N": "Fe58_57fe_d_p_pol_d_p.ens",
        "O": "Fe58_58fe_e_eP.ens", "P": "Fe58_58fe_n_nPg.ens",
        "Q": "Fe58_58fe_p_pP.ens", "R": "Fe58_58fe_d_dP_pol_d_dP.ens",
        "S": "Fe58_58fe_3he_3heP.ens", "T": "Fe58_58fe_a_aP.ens",
        "U": "Fe58_59co_g_p.ens", "V": "Fe58_59co_mu-_ng.ens",
        "W": "Fe58_59co_n_d.ens", "X": "Fe58_59co_p_2p.ens",
        "Y": "Fe58_59co_d_3he.ens", "Z": "Fe58_60ni_mu-_nupng.ens",
        "a": "Fe58_62ni_3he_7be.ens", "b": "Fe58_cu_k-_g.ens",
        "c": "Fe58_coulex.ens", "d": "Fe58_238u_64ni_xg.ens",
    }.items()}
    expected = set(dataset_descriptions)
    source_levels = {label: levels for label, levels in sources.items()}
    occurrences = defaultdict(list)
    findings = []
    total_tokens = 0

    for level in adopted:
        for line, message in level.get("syntax_errors", []):
            findings.append((line, "XREF_STRUCTURE", level.get("xref_text", ""), message))
        for match in level.get("tokens", []):
            label, modifier = match.group(1), match.group(2)
            token = match.group(0)
            total_tokens += 1
            occurrences[(label, modifier)].append((level["line"], level["energy_text"], token))
            if label not in expected:
                findings.append((level["line"], "UNKNOWN_DATASET", token, label))
            if modifier is not None:
                core = modifier[:-1] if modifier.endswith(("*", "?")) else modifier
                marker = modifier[-1] if modifier.endswith(("*", "?")) else ""
                if core and not ENERGY_RE.match(core):
                    findings.append((level["line"], "BAD_MODIFIER", token, modifier))
                if marker == "*" and core:
                    pass
                if marker not in ("", "*", "?"):
                    findings.append((level["line"], "BAD_MARKER", token, modifier))
            if label in source_levels and modifier is not None:
                core = modifier[:-1] if modifier.endswith(("*", "?")) else modifier
                if core:
                    exact = [x for x in source_levels[label] if x["energy_text"] == core]
                    numeric = [x for x in source_levels[label] if x["energy"] is not None and float(core) == x["energy"]]
                    if not exact and numeric:
                        findings.append((level["line"], "ENERGY_TEXT_MISMATCH", token, f"source={label} has {numeric[0]['energy_text']}"))
                    elif not exact:
                        findings.append((level["line"], "ENERGY_NOT_IN_SOURCE", token, f"source={label}"))

    # Ambiguous modifiers: (*) must identify one source level represented on >=2 adopted levels.
    for (label, modifier), items in sorted(occurrences.items(), key=lambda item: (item[0][0], item[0][1] or "")):
        if modifier is not None and modifier.endswith("*"):
            if len(items) < 2:
                findings.append((items[0][0], "AMBIGUITY_SINGLETON", f"{label}({modifier})", f"count={len(items)}"))
            if modifier[:-1] and any(other != modifier for (lab, other) in occurrences if lab == label and other and other.endswith("*") and other[:-1] == modifier[:-1]):
                findings.append((items[0][0], "AMBIGUITY_ENERGY_INCONSISTENT", f"{label}({modifier})", "same source energy has multiple forms"))

    # Compare energy-only and energy* tokens exactly across all occurrences.
    for (label, modifier), items in sorted(occurrences.items(), key=lambda item: (item[0][0], item[0][1] or "")):
        if modifier and modifier.endswith("*") and modifier[:-1]:
            same_energy = [(m, v) for (lab, m), vals in occurrences.items() if lab == label and m and m.endswith("*") and m[:-1] == modifier[:-1] for v in vals]
            if len(same_energy) != len(items):
                findings.append((items[0][0], "AMBIGUITY_REPETITION", f"{label}({modifier})", f"occurrences={len(items)}"))

    counts = Counter(kind for _, kind, *_ in findings)
    print(f"adopted_levels={len(adopted)} xref_tokens={total_tokens} datasets={len(expected)}")
    print("source_level_counts=" + ",".join(f"{label}:{len(source_levels[label])}" for label in sorted(source_levels)))
    print("finding_counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)) if counts else "finding_counts=none")
    grouped = defaultdict(list)
    for line, kind, token, detail in findings:
        grouped[(kind, token, detail)].append(line)
    for (kind, token, detail), lines in grouped.items():
        line_text = ",".join(str(line) for line in lines)
        print(f"{kind}\tlines={line_text}\t{token}\t{detail}")


if __name__ == "__main__":
    main()
