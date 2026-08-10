from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "XUNDL" / "A58"
ISOTOPES = ("Ca58", "Sc58", "Ti58", "V58", "Cr58", "Mn58")
TOKEN_RE = re.compile(r"([A-Za-z])(?:\(([^()]*)\))?")
ENERGY_RE = re.compile(r"^[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?$")
LABEL_ORDER = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def energy_text(line: str) -> str:
    return line[9:19].strip()


def energy_value(text: str):
    try:
        return float(text)
    except ValueError:
        return None


def is_l(line: str) -> bool:
    return len(line) >= 9 and line[5] == " " and line[7:9] == "L "


def source_title(path: Path) -> str:
    for line in path.read_text(encoding="ascii").splitlines():
        if len(line) >= 10 and line[5] == " " and line[7:9] == "  ":
            return line[9:].strip()
    return path.name


def parse_file(path: Path):
    levels = []
    xrefs = []
    xrecords = []
    current = None
    for number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.rstrip("\r\n")
        if len(line) >= 10 and line[7] == "X" and line[8].isalpha():
            xrecords.append((line[8], line[9:].strip()))
        if is_l(line):
            current = {"line": number, "energy_text": energy_text(line), "energy": energy_value(energy_text(line)), "tokens": [], "raw": line}
            levels.append(current)
        if current is not None and "XREF=" in line:
            value = line.split("XREF=", 1)[1].rstrip()
            current["xref_line"] = number
            current["xref_text"] = value
            current["tokens"] = list(TOKEN_RE.finditer(value))
            consumed = "".join(m.group(0) for m in current["tokens"])
            if consumed != value.replace(" ", ""):
                current.setdefault("errors", []).append("unparsed characters")
            labels = [m.group(1) for m in current["tokens"]]
            if " " in value:
                current.setdefault("errors", []).append("internal space")
            if labels != sorted(labels, key=LABEL_ORDER.index):
                current.setdefault("errors", []).append("non-alphabetical labels")
            if len(labels) != len(set(labels)):
                current.setdefault("errors", []).append("duplicate labels")
            xrefs.append(current)
    return levels, xrefs, xrecords


def normalize(text: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", text.upper())


def map_sources(adopted_path: Path, source_paths: list[Path], xrecords):
    mapped = {}
    used = set()
    for label, title in xrecords:
        target = normalize(title)
        candidates = [(p, normalize(source_title(p))) for p in source_paths if p not in used]
        exact = [p for p, value in candidates if value == target]
        if len(exact) == 1:
            mapped[label] = exact[0]
            used.add(exact[0])
            continue
        contains = [p for p, value in candidates if target and (target in value or value in target)]
        if len(contains) == 1:
            mapped[label] = contains[0]
            used.add(contains[0])
    return mapped


def main():
    for isotope in ISOTOPES:
        folder = BASE / isotope / "old"
        adopted_path = folder / f"{isotope}_adopted.ens"
        source_paths = sorted(p for p in folder.glob("*.ens") if p != adopted_path)
        levels, xrefs, xrecords = parse_file(adopted_path)
        mapped = map_sources(adopted_path, source_paths, xrecords)
        source_levels = {}
        for label, path in mapped.items():
            source_levels[label] = parse_file(path)[0]
        occurrences = defaultdict(list)
        findings = []
        tokens = 0
        for level in xrefs:
            for error in level.get("errors", []):
                findings.append(("XREF_STRUCTURE", level["xref_line"], level["xref_text"], error))
            for match in level["tokens"]:
                label, modifier = match.group(1), match.group(2)
                token = match.group(0)
                tokens += 1
                occurrences[(label, modifier)].append((level["xref_line"], level["energy_text"], token))
                if modifier is not None:
                    core = modifier[:-1] if modifier.endswith(("*", "?")) else modifier
                    marker = modifier[-1] if modifier.endswith(("*", "?")) else ""
                    if marker not in ("", "*", "?") or (core and not ENERGY_RE.match(core)):
                        findings.append(("BAD_MODIFIER", level["xref_line"], token, modifier))
                    if core and label in source_levels:
                        exact = [s for s in source_levels[label] if s["energy_text"] == core]
                        numeric = [s for s in source_levels[label] if s["energy"] is not None and energy_value(core) == s["energy"]]
                        if not exact:
                            kind = "ENERGY_TEXT_MISMATCH" if numeric else "ENERGY_NOT_IN_SOURCE"
                            detail = f"source={label} values=" + ",".join(s["energy_text"] for s in numeric[:3])
                            findings.append((kind, level["xref_line"], token, detail))
                    elif core and label not in mapped:
                        findings.append(("SOURCE_UNMAPPED", level["xref_line"], token, label))
        for (label, modifier), items in occurrences.items():
            if modifier and modifier.endswith("*") and len(items) < 2:
                findings.append(("AMBIGUITY_SINGLETON", items[0][0], f"{label}({modifier})", f"count={len(items)}"))
        for label in sorted({label for label, modifier in occurrences}):
            energy_star = [(modifier, items) for (lab, modifier), items in occurrences.items() if lab == label and modifier and modifier.endswith("*") and modifier[:-1]]
            by_energy = defaultdict(list)
            for modifier, items in energy_star:
                by_energy[modifier[:-1]].append((modifier, items))
            for energy, variants in by_energy.items():
                if len({modifier for modifier, _ in variants}) > 1:
                    findings.append(("ENERGY_STAR_INCONSISTENT", variants[0][1][0][0], label, energy))
        counts = Counter(kind for kind, *_ in findings)
        print(f"[{isotope}] adopted_levels={len(levels)} xref_lines={len(xrefs)} tokens={tokens} xrecords={len(xrecords)} sources={len(source_paths)} mapped={len(mapped)}")
        print("  findings=" + (", ".join(f"{k}:{v}" for k, v in sorted(counts.items())) if counts else "none"))
        grouped = defaultdict(list)
        for kind, line, token, detail in findings:
            grouped[(kind, token, detail)].append(line)
        for (kind, token, detail), lines in sorted(grouped.items()):
            print(f"  {kind}\tlines={','.join(map(str, lines))}\t{token}\t{detail}")
        print()


if __name__ == "__main__":
    main()
